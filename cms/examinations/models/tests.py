from datetime import datetime, timedelta
from unittest.mock import patch

from errors.models import NotFoundError
from examinations.models.case_breakdown import CaseBreakdown, ExaminationEventList
from examinations.models.core import ExaminationOverview, CauseOfDeath
from examinations.models.medical_team import MedicalTeam, MedicalTeamMember
from examinations.models.patient_details import PatientDetails
from examinations.models.timeline_events import CaseInitialEvent, CaseClosedEvent, CaseOtherEvent, CasePreScrutinyEvent, \
    CaseQapDiscussionEvent, CaseMeoSummaryEvent, CaseAdmissionNotesEvent, CaseBereavedDiscussionEvent, \
    CaseMedicalHistoryEvent
from examinations.templatetags.examination_filters import case_card_presenter
from medexCms.test.mocks import ExaminationMocks, PeopleMocks, DatatypeMocks, SessionMocks
from medexCms.test.utils import MedExTestCase
from medexCms.utils import NONE_DATE, parse_datetime, NONE_TIME, API_DATE_FORMAT_4, key_not_empty


class ExaminationsCoreModelsTests(MedExTestCase):

    # ExaminationOverview tests

    def test_card_presenter_returns_a_correctly_formatted_dod_if_date_present(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])

        given_date = '2019-02-02T02:02:02.000Z'
        examination_overview.date_of_death = parse_datetime(given_date)

        presenter = case_card_presenter(examination_overview)
        result = presenter['banner_dod']
        expected_date = '02.02.2019'
        self.assertEqual(result, expected_date)

    def test_card_presenter_returns_a_correctly_formatted_dob_if_date_present(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])
        given_date = '2019-02-02T02:02:02.000Z'
        examination_overview.date_of_birth = parse_datetime(given_date)

        presenter = case_card_presenter(examination_overview)
        result = presenter['banner_dob']

        expected_date = '02.02.2019'
        self.assertEqual(result, expected_date)

    def test_card_presenter_returns_a_correctly_formatted_appointment_date_if_date_present(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])
        given_date = '2019-02-02T02:02:02.000Z'
        examination_overview.appointment_date = parse_datetime(given_date)

        presenter = case_card_presenter(examination_overview)
        result = presenter['appointment_date']

        expected_date = '02.02.2019'
        self.assertEqual(result, expected_date)

    def test_calc_age_correctly_calculates_the_age_if_dates_present(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])
        birth_date = '2018-02-02T02:02:02.000Z'
        death_date = '2019-02-02T02:02:02.000Z'
        examination_overview.date_of_birth = parse_datetime(birth_date)
        examination_overview.date_of_death = parse_datetime(death_date)
        result = examination_overview.calc_age()
        expected_age = 1
        self.assertEqual(result, expected_age)

    def test_calc_age_returns_none_if_date_of_birth_missing(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])
        death_date = '2019-02-02T02:02:02.000Z'
        examination_overview.date_of_birth = None
        examination_overview.date_of_death = parse_datetime(death_date)
        result = examination_overview.calc_age()

        self.assertIsNone(result)

    def test_calc_age_returns_none_if_date_of_death_missing(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])
        birth_date = '2019-02-02T02:02:02.000Z'
        examination_overview.date_of_birth = parse_datetime(birth_date)
        examination_overview.date_of_death = None
        result = examination_overview.calc_age()
        self.assertIsNone(result)

    def test_calc_age_returns_none_if__both_dates_missing(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])
        examination_overview.date_of_birth = None
        examination_overview.date_of_death = None
        result = examination_overview.calc_age()

        self.assertIsNone(result)

    def test_calc_last_admission_days_ago_returns_correct_number_of_days_if_date_of_admission_present(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])
        admission_date = datetime.today() - timedelta(days=1)
        examination_overview.last_admission = admission_date
        result = examination_overview.calc_last_admission_days_ago()
        expected_days = 1
        self.assertEqual(result, expected_days)

    def test_calc_last_admission_days_ago_returns_0_if_date_of_admission_missing(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])
        admission_date = None
        examination_overview.last_admission = parse_datetime(admission_date)
        result = examination_overview.calc_last_admission_days_ago()
        expected_days = 0
        self.assertEqual(result, expected_days)

    def test_calc_created_days_ago_returns_correct_number_of_days_if_case_created_date_present(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])
        case_created_date = datetime.today() - timedelta(days=1)
        examination_overview.case_created_date = case_created_date
        result = examination_overview.calc_created_days_ago()
        expected_days = 1
        self.assertEqual(result, expected_days)

    def test_calc_created_days_ago_returns_0_if_case_created_date_missing(self):
        examination_overview = ExaminationOverview(ExaminationMocks.get_case_index_response_content()
                                                   ['examinations'][0])
        case_created_date = None
        examination_overview.case_created_date = parse_datetime(case_created_date)
        result = examination_overview.calc_created_days_ago()
        expected_days = 0
        self.assertEqual(result, expected_days)

    def test_examination_overview_urgent_returns_true_if_urgency_score_gt_than_0_and_case_open(self):
        case_overview_data = ExaminationMocks.get_case_overview_content()
        case_overview_data['urgencyScore'] = 1000
        case_overview_data['open'] = True
        case_overview = ExaminationOverview(case_overview_data)
        self.assertIsTrue(case_overview.urgent())

    def test_examination_overview_urgent_returns_false_if_urgency_score_gt_than_0_but_case_closed(self):
        case_overview_data = ExaminationMocks.get_case_overview_content()
        case_overview_data['urgencyScore'] = 1000
        case_overview_data['open'] = False
        case_overview = ExaminationOverview(case_overview_data)
        self.assertIsFalse(case_overview.urgent())

    def test_examination_overview_urgent_returns_false_if_urgency_score_is_0_and_case_open(self):
        case_overview_data = ExaminationMocks.get_case_overview_content()
        case_overview_data['urgencyScore'] = 0
        case_overview_data['open'] = True
        case_overview = ExaminationOverview(case_overview_data)
        self.assertIsFalse(case_overview.urgent())

    def test_examination_overview_urgent_returns_false_if_urgency_score_is_0_and_case_closed(self):
        case_overview_data = ExaminationMocks.get_case_overview_content()
        case_overview_data['urgencyScore'] = 0
        case_overview_data['open'] = False
        case_overview = ExaminationOverview(case_overview_data)
        self.assertIsFalse(case_overview.urgent())


class ExaminationsPatientDetailsModelsTests(MedExTestCase):
    # PatientDetails tests

    def test_initialising_with_the_none_date_results_in_no_dob(self):
        loaded_data = ExaminationMocks.get_patient_details_load_response_content()
        loaded_data['dateOfBirth'] = NONE_DATE
        patient_details = PatientDetails(loaded_data)
        self.assertIsNone(patient_details.date_of_birth)
        self.assertIsNone(patient_details.day_of_birth)
        self.assertIsNone(patient_details.month_of_birth)
        self.assertIsNone(patient_details.year_of_birth)

    def test_initialising_with_the_none_date_results_in_no_dod(self):
        loaded_data = ExaminationMocks.get_patient_details_load_response_content()
        loaded_data['dateOfDeath'] = NONE_DATE
        patient_details = PatientDetails(loaded_data)
        self.assertIsNone(patient_details.date_of_death)
        self.assertIsNone(patient_details.day_of_death)
        self.assertIsNone(patient_details.month_of_death)
        self.assertIsNone(patient_details.year_of_death)

    def test_initialising_with_a_mode_of_disposal_and_the_enums_sets_the_mode_of_disposal(self):
        loaded_data = ExaminationMocks.get_patient_details_load_response_content()
        mode_of_disposal = list(DatatypeMocks.get_modes_of_disposal_list().keys())[0]
        loaded_data['modeOfDisposal'] = mode_of_disposal
        patient_details = PatientDetails(loaded_data, DatatypeMocks.get_modes_of_disposal_list())
        self.assertEqual(patient_details.mode_of_disposal, mode_of_disposal)

    def test_initialising_with_a_bereaved_sets_the_representatives(self):
        loaded_data = ExaminationMocks.get_patient_details_load_response_content()
        bereaved = PeopleMocks.get_bereaved_representative_response_dict()
        loaded_data['representatives'].append(bereaved)
        patient_details = PatientDetails(loaded_data, DatatypeMocks.get_modes_of_disposal_list())
        self.assertEqual(len(patient_details.representatives), 1)
        self.assertEqual(patient_details.representatives[0].full_name, bereaved['fullName'])

    def test_patient_details_load_by_id_returns_a_patient_details_object_if_successful(self):
        patient_details, error = PatientDetails.load_by_id(ExaminationMocks.EXAMINATION_ID, SessionMocks.ACCESS_TOKEN)
        self.assertIsNone(error)
        self.assertIsNotNone(patient_details)
        self.assertEquals(type(patient_details), PatientDetails)

    @patch('examinations.request_handler.load_modes_of_disposal',
           return_value=DatatypeMocks.get_unsuccessful_modes_of_disposal_response())
    def test_patient_details_load_by_id_returns_an_error_object_if_modes_of_disposal_load_fails(self,
                                                                                                mock_modes_of_disposal):
        patient_details, error = PatientDetails.load_by_id(ExaminationMocks.EXAMINATION_ID, SessionMocks.ACCESS_TOKEN)
        self.assertIsNone(patient_details)
        self.assertIsNotNone(error)
        self.assertEquals(type(error), NotFoundError)

    @patch('examinations.request_handler.load_patient_details_by_id',
           return_value=ExaminationMocks.get_unsuccessful_patient_details_load_response())
    def test_patient_details_load_by_id_returns_an_error_object_if_load_fails(self, mock_patient_details):
        patient_details, error = PatientDetails.load_by_id(ExaminationMocks.EXAMINATION_ID, SessionMocks.ACCESS_TOKEN)
        self.assertIsNone(patient_details)
        self.assertIsNotNone(error)
        self.assertEquals(type(error), NotFoundError)

    @patch('examinations.request_handler.update_patient_details',
           return_value=ExaminationMocks.get_unsuccessful_patient_details_update_response())
    def test_patient_details_update_returns_error_if_update_fails(self, mock_update):
        patient_details, load_error = PatientDetails.load_by_id(ExaminationMocks.EXAMINATION_ID,
                                                                SessionMocks.ACCESS_TOKEN)
        self.assertIsNone(load_error)
        self.assertIsNotNone(patient_details)
        error = patient_details.update(ExaminationMocks.get_patient_details_load_response_content(),
                                       SessionMocks.ACCESS_TOKEN)
        self.assertIsNotNone(error)

    @patch('examinations.request_handler.update_patient_details',
           return_value=ExaminationMocks.get_unsuccessful_patient_details_update_response())
    def test_patient_details_update_does_not_update_the_patient_header_on_failure(self, mock_update):
        updated_header_content = ExaminationMocks.get_patient_details_update_response_content().get('header')
        self.assertNotEqual(ExaminationMocks.get_patient_details_load_response_content().get('givenNames'),
                            updated_header_content.get('givenNames'))

        patient_details, load_error = PatientDetails.load_by_id(ExaminationMocks.EXAMINATION_ID,
                                                                SessionMocks.ACCESS_TOKEN)
        self.assertIsNone(load_error)
        self.assertIsNotNone(patient_details)

        starting_patient_header = patient_details.case_header
        self.assertEquals(starting_patient_header.given_names,
                          ExaminationMocks.get_patient_details_load_response_content().get('givenNames'))

        error = patient_details.update(ExaminationMocks.get_patient_details_load_response_content(),
                                       SessionMocks.ACCESS_TOKEN)
        self.assertIsNotNone(error)

        ending_patient_header = patient_details.case_header
        self.assertNotEquals(ending_patient_header.given_names, updated_header_content.get('givenNames'))
        self.assertEquals(starting_patient_header.given_names, ending_patient_header.given_names)

    def test_patient_details_full_name_correctly_joins_first_and_last_names(self):
        patient_details_data = ExaminationMocks.get_patient_details_load_response_content()
        patient_details = PatientDetails(patient_details_data)
        full_name = patient_details.full_name()
        self.assertEqual(full_name.split(' ')[0], patient_details_data.get('givenNames'))
        self.assertEqual(full_name.split(' ')[1], patient_details_data.get('surname'))

    def test_patient_details_get_nhs_number_returns_the_nhs_number_if_present(self):
        patient_details_data = ExaminationMocks.get_patient_details_load_response_content()
        patient_details = PatientDetails(patient_details_data)
        self.assertIsNotNone(patient_details)
        self.assertIsNotNone(patient_details.nhs_number)

        display_nhs_number = patient_details.get_nhs_number()

        self.assertEquals(patient_details.nhs_number, display_nhs_number)

    def test_patient_details_get_nhs_number_returns_unknown_if_number_not_present(self):
        patient_details_data = ExaminationMocks.get_patient_details_load_response_content()
        patient_details = PatientDetails(patient_details_data)
        self.assertIsNotNone(patient_details)
        patient_details.nhs_number = None

        display_nhs_number = patient_details.get_nhs_number()

        self.assertEquals(display_nhs_number, 'Unknown')


class ExaminationsMedicalTeamModelsTests(MedExTestCase):
    # MedicalTeam tests

    def test_medical_team_load_by_id_returns_a_medical_team_object_if_successful(self):
        medical_team, error = MedicalTeam.load_by_id(ExaminationMocks.EXAMINATION_ID, SessionMocks.ACCESS_TOKEN)
        self.assertIsNone(error)
        self.assertIsNotNone(medical_team)
        self.assertEquals(type(medical_team), MedicalTeam)

    @patch('examinations.request_handler.load_medical_team_by_id',
           return_value=ExaminationMocks.get_unsuccessful_medical_team_load_response())
    def test_medical_team_load_by_id_returns_an_error_object_if_load_fails(self, mock_load):
        medical_team, error = MedicalTeam.load_by_id(ExaminationMocks.EXAMINATION_ID, SessionMocks.ACCESS_TOKEN)
        self.assertIsNone(medical_team)
        self.assertIsNotNone(error)
        self.assertEquals(type(error), NotFoundError)

    def test_medical_team_update_returns_no_error_if_update_succeeds(self):
        medical_team, load_error = MedicalTeam.load_by_id(ExaminationMocks.EXAMINATION_ID, SessionMocks.ACCESS_TOKEN)
        self.assertIsNone(load_error)
        self.assertIsNotNone(medical_team)
        error = medical_team.update(ExaminationMocks.get_medical_team_load_response_content(),
                                    SessionMocks.ACCESS_TOKEN)
        self.assertIsNone(error)

    @patch('examinations.request_handler.update_medical_team',
           return_value=ExaminationMocks.get_unsuccessful_medical_team_update_response())
    def test_medical_team_update_returns_error_if_update_fails(self, mock_update):
        medical_team, load_error = MedicalTeam.load_by_id(ExaminationMocks.EXAMINATION_ID, SessionMocks.ACCESS_TOKEN)
        self.assertIsNone(load_error)
        self.assertIsNotNone(medical_team)
        error = medical_team.update(ExaminationMocks.get_medical_team_load_response_content(),
                                    SessionMocks.ACCESS_TOKEN)
        self.assertIsNotNone(error)

    # MedicalTeamMember tests

    def test_medical_team_member_from_dict_returns_none_when_not_given_a_dict(self):
        from_dict_response = MedicalTeamMember.from_dict(None)
        self.assertIsNone(from_dict_response)

    def test_medical_team_member_has_name_returns_true_if_a_value_is_present(self):
        medical_team_member = MedicalTeamMember.from_dict(PeopleMocks.get_medical_team_member_content('gp'))
        self.assertIsNotNone(medical_team_member)

        self.assertIsTrue(len(medical_team_member.name) > 0)

        self.assertIsTrue(medical_team_member.has_name())

    def test_medical_team_member_has_name_returns_falsnoe_if__value_is_present(self):
        medical_team_member = MedicalTeamMember.from_dict(PeopleMocks.get_medical_team_member_content('gp'))
        self.assertIsNotNone(medical_team_member)

        medical_team_member.name = None

        self.assertIsFalse(medical_team_member.has_name())

        medical_team_member.name = ''

        self.assertIsFalse(medical_team_member.has_name())

    def test_medical_team_member_has_valid_name_returns_true_if_name_is_within_character_limit(self):
        medical_team_member = MedicalTeamMember.from_dict(PeopleMocks.get_medical_team_member_content('gp'))
        self.assertIsNotNone(medical_team_member)

        self.assertIsTrue(len(medical_team_member.name) < 250)

        self.assertIsTrue(medical_team_member.has_valid_name())

    def test_medical_team_member_has_valid_name_returns_false_if_name_is_over_character_limit(self):
        medical_team_member = MedicalTeamMember.from_dict(PeopleMocks.get_medical_team_member_content('gp'))
        self.assertIsNotNone(medical_team_member)

        medical_team_member.name = "x" * 250
        self.assertEquals(len(medical_team_member.name), 250)

        self.assertIsFalse(medical_team_member.has_valid_name())

    def test_medical_team_member_has_name_if_needed_returns_true_if_no_fields_entered(self):
        medical_team_member = MedicalTeamMember()

        self.assertIsTrue(medical_team_member.has_name_if_needed())

    def test_medical_team_member_has_name_if_needed_returns_true_if_no_other_fields_entered(self):
        medical_team_member = MedicalTeamMember()
        medical_team_member.name = 'Dr Jones'

        self.assertIsTrue(medical_team_member.has_name_if_needed())

    def test_medical_team_member_has_name_if_needed_returns_true_if_name_and_role_entered(self):
        medical_team_member = MedicalTeamMember()
        medical_team_member.name = 'Dr Jones'
        medical_team_member.role = 'Consultant'

        self.assertIsTrue(medical_team_member.has_name_if_needed())

    def test_medical_team_member_has_name_if_needed_returns_true_if_name_and_org_entered(self):
        medical_team_member = MedicalTeamMember()
        medical_team_member.name = 'Dr Jones'
        medical_team_member.organisation = 'A NHS Trust'

        self.assertIsTrue(medical_team_member.has_name_if_needed())

    def test_medical_team_member_has_name_if_needed_returns_true_if_name_and_number_entered(self):
        medical_team_member = MedicalTeamMember()
        medical_team_member.name = 'Dr Jones'
        medical_team_member.phone_number = '01234 567890'

        self.assertIsTrue(medical_team_member.has_name_if_needed())

    def test_medical_team_member_has_name_if_needed_returns_true_if_name_role_and_org_entered(self):
        medical_team_member = MedicalTeamMember()
        medical_team_member.name = 'Dr Jones'
        medical_team_member.role = 'Consultant'
        medical_team_member.organisation = 'A NHS Trust'

        self.assertIsTrue(medical_team_member.has_name_if_needed())

    def test_medical_team_member_has_name_if_needed_returns_true_if_name_role_and_number_entered(self):
        medical_team_member = MedicalTeamMember()
        medical_team_member.name = 'Dr Jones'
        medical_team_member.role = 'Consultant'
        medical_team_member.phone_number = '01234 567890'

        self.assertIsTrue(medical_team_member.has_name_if_needed())

    def test_medical_team_member_has_name_if_needed_returns_true_if_name_org_and_number_entered(self):
        medical_team_member = MedicalTeamMember()
        medical_team_member.name = 'Dr Jones'
        medical_team_member.organisation = 'A NHS Trust'
        medical_team_member.phone_number = '01234 567890'

        self.assertIsTrue(medical_team_member.has_name_if_needed())

    def test_medical_team_member_has_name_if_needed_returns_true_if_name_role_org_and_number_entered(self):
        medical_team_member = MedicalTeamMember()
        medical_team_member.name = 'Dr Jones'
        medical_team_member.role = 'Consultant'
        medical_team_member.organisation = 'A NHS Trust'
        medical_team_member.phone_number = '01234 567890'

        self.assertIsTrue(medical_team_member.has_name_if_needed())

    def test_medical_team_member_has_name_if_needed_returns_false_if_role_entered_with_no_name(self):
        medical_team_member = MedicalTeamMember()
        medical_team_member.role = 'Consultant'

        self.assertIsFalse(medical_team_member.has_name_if_needed())

    def test_medical_team_member_has_name_if_needed_returns_false_if_org_entered_with_no_name(self):
        medical_team_member = MedicalTeamMember()
        medical_team_member.organisation = 'A NHS Trust'

        self.assertIsFalse(medical_team_member.has_name_if_needed())

    def test_medical_team_member_has_name_if_needed_returns_false_if_number_entered_with_no_name(self):
        medical_team_member = MedicalTeamMember()
        medical_team_member.phone_number = '01234 567890'

        self.assertIsFalse(medical_team_member.has_name_if_needed())

    def test_medical_team_member_has_name_if_needed_returns_false_if_role_and_org_entered_with_no_name(self):
        medical_team_member = MedicalTeamMember()
        medical_team_member.role = 'Consultant'
        medical_team_member.organisation = 'A NHS Trust'

        self.assertIsFalse(medical_team_member.has_name_if_needed())

    def test_medical_team_member_has_name_if_needed_returns_false_if_role_and_number_entered_with_no_name(self):
        medical_team_member = MedicalTeamMember()
        medical_team_member.role = 'Consultant'
        medical_team_member.phone_number = '01234 567890'

        self.assertIsFalse(medical_team_member.has_name_if_needed())

    def test_medical_team_member_has_name_if_needed_returns_false_if_org_and_number_entered_with_no_name(self):
        medical_team_member = MedicalTeamMember()
        medical_team_member.organisation = 'A NHS Trust'
        medical_team_member.phone_number = '01234 567890'

        self.assertIsFalse(medical_team_member.has_name_if_needed())

    def test_medical_team_member_has_name_if_needed_returns_false_if_role_org_and_number_entered_with_no_name(self):
        medical_team_member = MedicalTeamMember()
        medical_team_member.role = 'Consultant'
        medical_team_member.organisation = 'A NHS Trust'
        medical_team_member.phone_number = '01234 567890'

        self.assertIsFalse(medical_team_member.has_name_if_needed())

    def test_medical_team_member_to_object_returns_correct_json_object(self):
        medical_team_member = MedicalTeamMember.from_dict(PeopleMocks.get_medical_team_member_content('gp'))
        medical_team_member_dict = medical_team_member.to_object()

        self.assertIsTrue("name" in medical_team_member_dict)
        self.assertEqual(medical_team_member_dict.get('name'), medical_team_member.name)

        self.assertIsTrue("role" in medical_team_member_dict)
        self.assertEqual(medical_team_member_dict.get('role'), medical_team_member.role)

        self.assertIsTrue("organisation" in medical_team_member_dict)
        self.assertEqual(medical_team_member_dict.get('organisation'), medical_team_member.organisation)

        self.assertIsTrue("phone" in medical_team_member_dict)
        self.assertEqual(medical_team_member_dict.get('phone'), medical_team_member.phone_number)

        self.assertIsTrue("notes" in medical_team_member_dict)
        self.assertEqual(medical_team_member_dict.get('notes'), medical_team_member.notes)

        self.assertIsTrue("gmcNumber" in medical_team_member_dict)
        self.assertEqual(medical_team_member_dict.get('gmcNumber'), medical_team_member.gmc_number)


class ExaminationsCaseBreakdownModelsTests(MedExTestCase):
    # CaseBreakdown tests

    def test_case_breakdown_load_by_id_returns_case_breakdown_object_on_success(self):
        case_breakdown, error = CaseBreakdown.load_by_id(ExaminationMocks.EXAMINATION_ID,
                                                         SessionMocks.ACCESS_TOKEN)
        self.assertIsNone(error)
        self.assertIsNotNone(case_breakdown)
        self.assertEquals(type(case_breakdown), CaseBreakdown)

    @patch('examinations.request_handler.load_medical_team_by_id',
           return_value=ExaminationMocks.get_unsuccessful_medical_team_load_response())
    def test_case_breakdown_load_by_id_returns_an_error_object_if_medical_team_load_fails(self, mock_load):
        case_breakdown, error = CaseBreakdown.load_by_id(ExaminationMocks.EXAMINATION_ID, SessionMocks.ACCESS_TOKEN)
        self.assertIsNone(case_breakdown)
        self.assertIsNotNone(error)
        self.assertEquals(type(error), NotFoundError)

    @patch('examinations.request_handler.load_case_breakdown_by_id',
           return_value=ExaminationMocks.get_unsuccessful_case_breakdown_load_response())
    def test_case_breakdown_load_by_id_returns_an_error_object_if_load_fails(self, mock_load):
        case_breakdown, error = CaseBreakdown.load_by_id(ExaminationMocks.EXAMINATION_ID, SessionMocks.ACCESS_TOKEN)
        self.assertIsNone(case_breakdown)
        self.assertIsNotNone(error)
        self.assertEquals(type(error), NotFoundError)

    # ExaminationEventList tests

    def test_examination_event_list_parse_events_creates_a_list_including_all_events_in_the_data(self):
        patient_name = 'Joe Bloggs'
        event_list = ExaminationEventList({}, "0001-01-01T00:00:00", patient_name)
        self.assertEquals(len(event_list.events), 0)

        event_data = ExaminationMocks.get_case_breakdown_response_content().get('caseBreakdown')
        event_list.parse_events(event_data, patient_name)

        count_of_initial_events_in_data = 1
        count_of_closed_events_in_data = 1 if key_not_empty('caseClosed', event_data) else 0
        count_of_other_events_in_data = len(event_data.get('otherEvents').get('history')) if \
            key_not_empty('otherEvents', event_data) else 0
        count_of_scrutiny_events_in_data = len(event_data.get('preScrutiny').get('history')) if \
            key_not_empty('preScrutiny', event_data) else 0
        count_of_qap_events_in_data = len(event_data.get('qapDiscussion').get('history')) if \
            key_not_empty('qapDiscussion', event_data) else 0
        count_of_summary_events_in_data = len(event_data.get('meoSummary').get('history')) if \
            key_not_empty('meoSummary', event_data) else 0
        count_of_admission_events_in_data = len(event_data.get('admissionNotes').get('history')) if \
            key_not_empty('admissionNotes', event_data) else 0
        count_of_bereaved_events_in_data = len(event_data.get('bereavedDiscussion').get('history')) if \
            key_not_empty('bereavedDiscussion', event_data) else 0
        count_of_medical_events_in_data = len(event_data.get('medicalHistory').get('history')) if \
            key_not_empty('medicalHistory', event_data) else 0

        count_of_initial_events_in_list = 0
        count_of_closed_events_in_list = 0
        count_of_other_events_in_list = 0
        count_of_scrutiny_events_in_list = 0
        count_of_qap_events_in_list = 0
        count_of_summary_events_in_list = 0
        count_of_admission_events_in_list = 0
        count_of_bereaved_events_in_list = 0
        count_of_medical_events_in_list = 0

        for event in event_list.events:
            if type(event) == CaseInitialEvent:
                count_of_initial_events_in_list = count_of_initial_events_in_list + 1
            elif type(event) == CaseClosedEvent:
                count_of_closed_events_in_list = count_of_closed_events_in_list + 1
            elif type(event) == CaseOtherEvent:
                count_of_other_events_in_list = count_of_other_events_in_list + 1
            elif type(event) == CasePreScrutinyEvent:
                count_of_scrutiny_events_in_list = count_of_scrutiny_events_in_list + 1
            elif type(event) == CaseQapDiscussionEvent:
                count_of_qap_events_in_list = count_of_qap_events_in_list + 1
            elif type(event) == CaseMeoSummaryEvent:
                count_of_summary_events_in_list = count_of_summary_events_in_list + 1
            elif type(event) == CaseAdmissionNotesEvent:
                count_of_admission_events_in_list = count_of_admission_events_in_list + 1
            elif type(event) == CaseBereavedDiscussionEvent:
                count_of_bereaved_events_in_list = count_of_bereaved_events_in_list + 1
            elif type(event) == CaseMedicalHistoryEvent:
                count_of_medical_events_in_list = count_of_medical_events_in_list + 1

        self.assertEquals(count_of_initial_events_in_list, count_of_initial_events_in_data)
        self.assertEquals(count_of_closed_events_in_list, count_of_closed_events_in_data)
        self.assertEquals(count_of_other_events_in_list, count_of_other_events_in_data)
        self.assertEquals(count_of_scrutiny_events_in_list, count_of_scrutiny_events_in_data)
        self.assertEquals(count_of_qap_events_in_list, count_of_qap_events_in_data)
        self.assertEquals(count_of_summary_events_in_list, count_of_summary_events_in_data)
        self.assertEquals(count_of_admission_events_in_list, count_of_admission_events_in_data)
        self.assertEquals(count_of_bereaved_events_in_list, count_of_bereaved_events_in_data)
        self.assertEquals(count_of_medical_events_in_list, count_of_medical_events_in_data)

    def test_examination_event_list_parse_events_does_not_blow_up_if_it_recieves_an_unknown_event_type(self):
        patient_name = 'Joe Bloggs'
        event_list = ExaminationEventList({}, "0001-01-01T00:00:00", patient_name)
        self.assertEquals(len(event_list.events), 0)

        event_data = ExaminationMocks.get_case_breakdown_response_content().get('caseBreakdown')
        event_data['randomKey'] = event_data.get('otherEvents')

        try:
            event_list.parse_events(event_data, patient_name)
            # if the test reaches here the function completed without blowing up
            self.assertIsTrue(True)
        except:
            # function should not have thrown an error
            self.assertIsTrue(False)

    def test_examination_event_list_sort_events_oldest_to_newest_correctly_orders_events_with_oldest_first(self):

        def check_events_correctly_ordered(events_list):
            correctly_ordered = True
            previous_loop_date = None

            for event in events_list:
                if previous_loop_date:
                    next_date = parse_datetime(event.created_date)
                    if previous_loop_date > next_date:
                        correctly_ordered = False

                previous_loop_date = parse_datetime(event.created_date)

            return correctly_ordered

        patient_name = 'Joe Bloggs'
        event_data = ExaminationMocks.get_case_breakdown_response_content().get('caseBreakdown')
        event_list = ExaminationEventList(event_data, "0001-01-01T00:00:00", patient_name)

        is_correctly_ordered = check_events_correctly_ordered(event_list.events)

        if is_correctly_ordered:
            holder = event_list.events[0]
            event_list.events[0] = event_list.events[1]
            event_list.events[1] = holder
            is_correctly_ordered = check_events_correctly_ordered(event_list.events)

        self.assertIsFalse(is_correctly_ordered)

        event_list.sort_events_oldest_to_newest()

        is_correctly_ordered = check_events_correctly_ordered(event_list.events)

        self.assertIsTrue(is_correctly_ordered)


class ExaminationsCaseOutcomeModelsTests(MedExTestCase):
    # CaseOutcome tests

    def test_case_outcome_placeholder(self):
        # Need to implement tests for the case outcome model
        pass


class ExaminationsTimelineEventsModelsTests(MedExTestCase):
    # InitialEvent tests
    def test_initial_event_does_display_date_in_correct_format(self):
        data = {'dateOfDeath': '2019-05-12T00:00:00'}

        event = CaseInitialEvent(data, None)

        self.assertEquals(event.display_date(), '12.05.2019')

    def test_initial_event_does_display_time_in_correct_format(self):
        data = {'timeOfDeath': '00:55:00'}

        event = CaseInitialEvent(data, None)

        self.assertEquals(event.display_time(), '00:55')

    def test_initial_event_does_display_unknown_for_default_none_date(self):
        data = {'dateOfDeath': NONE_DATE}

        event = CaseInitialEvent(data, None)

        self.assertEquals(event.display_date(), CaseInitialEvent.UNKNOWN)

    def test_initial_event_does_display_unknown_for_default_none_time(self):
        data = {'timeOfDeath': NONE_TIME}

        event = CaseInitialEvent(data, None)

        self.assertEquals(event.display_time(), CaseInitialEvent.UNKNOWN)
