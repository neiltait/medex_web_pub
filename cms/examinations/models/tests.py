from datetime import datetime, timedelta

from examinations.models.core import ExaminationOverview
from examinations.models.patient_details import PatientDetails
from examinations.models.timeline_events import CaseInitialEvent
from examinations.templatetags.examination_filters import case_card_presenter
from medexCms.test.mocks import ExaminationMocks, PeopleMocks, DatatypeMocks
from medexCms.test.utils import MedExTestCase
from medexCms.utils import NONE_DATE, parse_datetime, NONE_TIME


class ExaminationsCoreModelsTests(MedExTestCase):
    # Examination tests

    def test_examination_placeholder(self):
        # Need to implement tests for the examination model
        pass

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


class ExaminationsMedicalTeamModelsTests(MedExTestCase):
    # MedicalTeam tests

    def test_medical_team_placeholder(self):
        # Need to implement tests for the medical team model
        pass

    # MedicalTeam tests

    def test_medical_team_member_placeholder(self):
        # Need to implement tests for the medical team member model
        pass


class ExaminationsCaseBreakdownModelsTests(MedExTestCase):
    # CaseBreakdown tests

    def test_case_breakdown_placeholder(self):
        # Need to implement tests for the case breakdown model
        pass

    # ExaminationEventList tests

    def test_examination_event_list_placeholder(self):
        # Need to implement tests for the examination event list model
        pass


class ExaminationsCaseOutcomeModelsTests(MedExTestCase):
    # CaseOutcome tests

    def test_case_outcome_placeholder(self):
        # Need to implement tests for the case outcome model
        pass


class ExaminationsTimelineEventsModelsTests(MedExTestCase):
    # InitialEvent tests
    def test_initial_event_does_display_date_in_correct_format(self):
        data = {'dateOfDeath': '2019-05-12T00:00:00'}

        event = CaseInitialEvent(data, None, None)

        self.assertEquals(event.display_date(), '12.05.2019')

    def test_initial_event_does_display_time_in_correct_format(self):
        data = {'timeOfDeath': '00:55:00'}

        event = CaseInitialEvent(data, None, None)

        self.assertEquals(event.display_time(), '00:55')

    def test_initial_event_does_display_unknown_for_default_none_date(self):
        data = {'dateOfDeath': NONE_DATE}

        event = CaseInitialEvent(data, None, None)

        self.assertEquals(event.display_date(), CaseInitialEvent.UNKNOWN)

    def test_initial_event_does_display_unknown_for_default_none_time(self):
        data = {'timeOfDeath': NONE_TIME}

        event = CaseInitialEvent(data, None, None)

        self.assertEquals(event.display_time(), CaseInitialEvent.UNKNOWN)
