from alerts import messages
from examinations.forms.medical_team import MedicalTeamMembersForm
from examinations.forms.patient_details import PrimaryExaminationInformationForm, SecondaryExaminationInformationForm, \
    BereavedInformationForm, UrgencyInformationForm
from examinations.forms.timeline_events import PreScrutinyEventForm, AdmissionNotesEventForm, QapDiscussionEventForm, \
    BereavedDiscussionEventForm
from examinations.models.medical_team import MedicalTeam, MedicalTeamMember
from examinations.models.patient_details import PatientDetails
from examinations.models.timeline_events import CaseQapDiscussionEvent, CaseBereavedDiscussionEvent
from medexCms.api import enums
from medexCms.test.mocks import ExaminationMocks, PeopleMocks
from medexCms.test.utils import MedExTestCase
from medexCms.utils import NONE_DATE
from people.models import BereavedRepresentative


class PatientDetailsFormsTests(MedExTestCase):
    # Primary Information Form
    def test_given_create_examination_without_first_name_when_submitted_does_not_validate(self):
        form = PrimaryExaminationInformationForm(request={'data': 'test'})
        result = form.is_valid()
        self.assertIsFalse(result)
        self.assertEqual(form.errors["first_name"], messages.ErrorFieldRequiredMessage('a given name'))

    def test_given_create_examination_with_first_name_submitted_does_validate(self):
        form = PrimaryExaminationInformationForm(request={'first_name': 'matt'})
        form.is_valid()
        self.assertIsFalse("first_name" in form.errors)

    def test_given_create_examination_without_last_name_when_submitted_does_not_validate(self):
        form = PrimaryExaminationInformationForm(request={'test': 'data'})
        result = form.is_valid()
        self.assertIsFalse(result)
        self.assertEqual(form.errors["last_name"], messages.ErrorFieldRequiredMessage('a surname'))

    def test_given_create_examination_with_name_greater_than_250_characters_does_not_validate(self):
        form = PrimaryExaminationInformationForm(request={'first_name': 'matt' * 40,
                                                          'last_name': 'matt' * 40})
        form.is_valid()
        self.assertIsTrue("first_name" in form.errors)
        self.assertIsTrue("last_name" in form.errors)

    def test_given_create_examination_with_first_name_greater_than_150_characters_does_not_validate(self):
        form = PrimaryExaminationInformationForm(request={'first_name': 'matt' * 40})
        form.is_valid()
        self.assertIsTrue("first_name" in form.errors)

    def test_given_create_examination_with_last_name_greater_than_150_characters_does_not_validate(self):
        form = PrimaryExaminationInformationForm(request={'last_name': 'nicks' * 40})
        form.is_valid()
        self.assertIsTrue("last_name" in form.errors)

    def test_given_create_examination_with_last_name_submitted_does_validate(self):
        form = PrimaryExaminationInformationForm(request={'last_name': 'nicks'})
        form.is_valid()
        self.assertIsFalse("last_name" in form.errors)

    def test_given_create_examination_without_gender_when_submitted_does_not_validate(self):
        form = PrimaryExaminationInformationForm(request={'test': 'data'})
        form.is_valid()
        self.assertEqual(form.errors["gender"], messages.NO_GENDER)

    def test_given_create_examination_with_gender_other_but_no_detail_when_submitted_does_not_validate(self):
        form = PrimaryExaminationInformationForm(request={'gender': 'Other'})
        form.is_valid()
        self.assertIsTrue("gender" in form.errors)

    def test_given_create_examination_with_gender_submitted_does_validate(self):
        form = PrimaryExaminationInformationForm(request={'gender': 'male'})
        form.is_valid()
        self.assertIsFalse("gender" in form.errors)

    def test_text_and_checkbox_group_validates_if_checkbox_is_ticked(self):
        # Given
        form = PrimaryExaminationInformationForm()
        textboxes = ['']
        checkbox = True

        # When
        group_valid = form.text_and_checkbox_group_is_valid(textboxes, checkbox)

        # Then
        self.assertTrue(group_valid)

    def test_text_and_checkbox_group_validates_if_textboxes_are_filled(self):
        # Given
        form = PrimaryExaminationInformationForm()
        textboxes = ['Filled']
        checkbox = False

        # When
        group_valid = form.text_and_checkbox_group_is_valid(textboxes, checkbox)

        # Then
        self.assertTrue(group_valid)

    def test_text_and_checkbox_group_does_not_validate_if_any_textbox_is_not_filled(self):
        # Given
        form = PrimaryExaminationInformationForm()
        textboxes = ['Filled', '']
        checkbox = False

        # When
        group_valid = form.text_and_checkbox_group_is_valid(textboxes, checkbox)

        # Then
        self.assertFalse(group_valid)

    def test_text_and_checkbox_group_does_not_validate_if_all_values_not_filled(self):
        # Given
        form = PrimaryExaminationInformationForm()
        textboxes = ['']
        checkbox = False

        # When
        group_valid = form.text_and_checkbox_group_is_valid(textboxes, checkbox)

        # Then
        self.assertFalse(group_valid)

    def test_nhs_number_group_does_validate_if_checkbox_ticked(self):
        form = PrimaryExaminationInformationForm({'nhs_number': '', 'nhs_number_not_known': True})
        form.is_valid()
        self.assertIsFalse("nhs_number" in form.errors)

    def test_nhs_number_group_does_validate_if_text_is_entered(self):
        form = PrimaryExaminationInformationForm({'nhs_number': 'ABC123', 'nhs_number_not_known': False})
        form.is_valid()
        self.assertIsFalse("nhs_number" in form.errors)

    def test_nhs_number_does_not_validate_if_nhs_number_too_long(self):
        form = PrimaryExaminationInformationForm({'nhs_number': '12345678901234567890123456789012345678901234567890'})
        form.is_valid()
        self.assertIsTrue("nhs_number" in form.errors)

    def test_nhs_number_does_not_validate_if_nhs_number_too_short(self):
        form = PrimaryExaminationInformationForm({'nhs_number': '1234'})
        form.is_valid()
        self.assertIsTrue("nhs_number" in form.errors)

    def test_nhs_number_group_does_not_validate_if_no_information_entered(self):
        form = PrimaryExaminationInformationForm({'nhs_number': ''})
        form.is_valid()
        self.assertEqual(form.errors["nhs_number"], messages.ErrorFieldRequiredMessage('an NHS number'))

    def test_time_of_death_group_does_validate_if_checkbox_ticked(self):
        form = PrimaryExaminationInformationForm({'time_of_death': '', 'time_of_death_not_known': True})
        form.is_valid()
        self.assertIsFalse("time_of_death" in form.errors)

    def test_time_of_death_group_does_validate_if_text_is_entered(self):
        form = PrimaryExaminationInformationForm({'time_of_death': 'ABC123', 'time_of_death_not_known': False})
        form.is_valid()
        self.assertIsFalse("time_of_death" in form.errors)

    def test_time_of_death_group_does_not_validate_if_no_information_entered(self):
        form = PrimaryExaminationInformationForm({'time_of_death': ''})
        form.is_valid()
        self.assertEqual(form.errors["time_of_death"], messages.ErrorFieldRequiredMessage('a time of death'))

    def test_date_of_birth_group_does_validate_if_checkbox_ticked(self):
        form = PrimaryExaminationInformationForm(
            {'day_of_birth': '', 'month_of_birth': '', 'year_of_birth': '', 'date_of_birth_not_known': True})
        form.is_valid()
        self.assertIsFalse("date_of_birth" in form.errors)

    def test_date_of_birth_group_does_validate_if_all_date_boxes_are_filled(self):
        form = PrimaryExaminationInformationForm(
            {'day_of_birth': '26', 'month_of_birth': '08', 'year_of_birth': '1978', 'date_of_birth_not_known': False})
        form.is_valid()
        self.assertIsFalse("date_of_birth" in form.errors)

    def test_date_of_birth_group_does_not_validate_if_date_boxes_are_filled_with_bad_date(self):
        form = PrimaryExaminationInformationForm(
            {'day_of_birth': '32', 'month_of_birth': '08', 'year_of_birth': '1978', 'date_of_birth_not_known': False})
        form.is_valid()
        self.assertIsTrue("date_of_birth" in form.errors)

    def test_date_of_birth_group_does_not_validate_if_no_information_entered(self):
        form = PrimaryExaminationInformationForm({'day_of_birth': '', 'month_of_birth': '', 'year_of_birth': ''})
        form.is_valid()
        self.assertEqual(form.errors["date_of_birth"], messages.ErrorFieldRequiredMessage('a date of birth'))

    def test_date_of_birth_group_does_not_validate_if_partial_information_entered(self):
        form = PrimaryExaminationInformationForm({'day_of_birth': '26', 'month_of_birth': '', 'year_of_birth': ''})
        form.is_valid()
        self.assertEqual(form.errors["date_of_birth"], messages.ErrorFieldRequiredMessage('a date of birth'))

    def test_date_of_death_group_does_validate_if_checkbox_ticked_and_time_of_death_checkbox_ticked(self):
        form = PrimaryExaminationInformationForm(
            {'day_of_death': '', 'month_of_death': '', 'year_of_death': '', 'date_of_death_not_known': True, 'time_of_death_not_known': True})
        form.is_valid()
        self.assertIsFalse("date_of_death" in form.errors)

    def test_date_of_death_group_does_validate_if_all_date_boxes_are_filled(self):
        form = PrimaryExaminationInformationForm(
            {'day_of_death': '26', 'month_of_death': '08', 'year_of_death': '1978'})
        form.is_valid()
        self.assertIsFalse("date_of_death" in form.errors)

    def test_date_of_death_group_does_not_validate_if_date_boxes_are_filled_with_bad_date(self):
        form = PrimaryExaminationInformationForm(
            {'day_of_death': '32', 'month_of_death': '08', 'year_of_death': '2019'})
        form.is_valid()
        self.assertIsTrue("date_of_death" in form.errors)

    def test_date_of_death_group_does_not_validate_if_no_information_entered(self):
        form = PrimaryExaminationInformationForm({'day_of_death': '', 'month_of_death': '', 'year_of_death': ''})
        form.is_valid()
        self.assertEqual(form.errors["date_of_death"], messages.ErrorFieldRequiredMessage('a date of death'))

    def test_date_of_death_group_does_not_validate_if_partial_information_entered(self):
        form = PrimaryExaminationInformationForm({'day_of_death': '26', 'month_of_death': '', 'year_of_death': ''})
        form.is_valid()
        self.assertEqual(form.errors["date_of_death"], messages.ErrorFieldRequiredMessage('a date of death'))

    def test_date_and_time_of_death_do_not_validate_if_unknown_but_time_is_known(self):
        form = PrimaryExaminationInformationForm({'day_of_death': '', 'month_of_death': '', 'year_of_death': '', 'date_of_death_not_known': True,
                                                  'time_of_death': '10:10'})
        form.is_valid()
        self.assertEqual(form.errors["date_of_death"], messages.DEATH_DATE_MISSING_WHEN_TIME_GIVEN)
        self.assertEqual(form.errors["time_of_death"], messages.DEATH_DATE_MISSING_WHEN_TIME_GIVEN)

    def test_place_of_death_does_not_validate_if_missing(self):
        form = PrimaryExaminationInformationForm({'test': 'data'})
        form.is_valid()
        self.assertEqual(form.errors["place_of_death"], messages.ErrorFieldRequiredMessage('a place of death'))

    def test_place_of_death_does_validate_if_present(self):
        form = PrimaryExaminationInformationForm({'place_of_death': "London"})
        form.is_valid()
        self.assertIsFalse("place_of_death" in form.errors)

    def test_me_office_does_not_validate_if_missing(self):
        form = PrimaryExaminationInformationForm({'test': 'data'})
        form.is_valid()
        self.assertEqual(form.errors["me_office"], messages.ME_OFFICE)

    def test_me_office_does_validate_if_present(self):
        form = PrimaryExaminationInformationForm({'me_office': 1})
        form.is_valid()
        self.assertIsFalse("me_office" in form.errors)

    def test_form_validates_with_required_data(self):
        # Given a complete form
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form = PrimaryExaminationInformationForm(form_data)

        # When it is validated
        form_is_valid = form.is_valid()

        # The whole form is valid
        self.assertIsTrue(form_is_valid)

    def test_form_validates_with_optional_data(self):
        # Given a complete form including optional data
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form_data['gender_details'] = 'example gender details'
        form_data['hospital_number_1'] = 'example hospital number 1'
        form_data['hospital_number_2'] = 'example hospital number 2'
        form_data['hospital_number_3'] = 'example hospital number 3'
        form_data['out_of_hours'] = True
        form = PrimaryExaminationInformationForm(form_data)

        # When it is validated
        form_is_valid = form.is_valid()

        # The whole form is valid
        self.assertIsTrue(form_is_valid)

    def test_form_stores_optional_data(self):
        # Given a complete form including optional data
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form_data['gender_details'] = 'example gender details'
        form_data['hospital_number_1'] = 'example hospital number 1'
        form_data['hospital_number_2'] = 'example hospital number 2'
        form_data['hospital_number_3'] = 'example hospital number 3'
        form_data['out_of_hours'] = True
        form = PrimaryExaminationInformationForm(form_data)

        # The optional data is parsed
        self.assertIs(form.gender_details, 'example gender details')
        self.assertIs(form.hospital_number_1, 'example hospital number 1')
        self.assertIs(form.hospital_number_2, 'example hospital number 2')
        self.assertIs(form.hospital_number_3, 'example hospital number 3')

    def test_form_correctly_passes_dob_and_dod_for_request_if_known(self):
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form_data['day_of_birth'] = '2'
        form_data['month_of_birth'] = '2'
        form_data['year_of_birth'] = '2019'
        form_data['day_of_death'] = '20'
        form_data['month_of_death'] = '2'
        form_data['year_of_death'] = '2019'
        form_data.pop('date_of_birth_not_known', None)
        form_data.pop('date_of_death_not_known', None)
        form = PrimaryExaminationInformationForm(form_data)

        result = form.to_object()
        self.assertNotEqual(result['dateOfBirth'], NONE_DATE)
        self.assertNotEqual(result['dateOfDeath'], NONE_DATE)

    def test_dates_are_blank_or_death_is_after_birth_date_returns_true_if_no_dates_given(self):
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form = PrimaryExaminationInformationForm(form_data)
        result = form.dates_are_blank_or_death_is_after_birth_date()
        self.assertIsTrue(result)

    def test_dates_are_blank_or_death_is_after_birth_date_returns_false_if_dod_is_before_dob(self):
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form_data['day_of_birth'] = '20'
        form_data['month_of_birth'] = '2'
        form_data['year_of_birth'] = '2019'
        form_data['day_of_death'] = '2'
        form_data['month_of_death'] = '2'
        form_data['year_of_death'] = '2019'
        form = PrimaryExaminationInformationForm(form_data)
        result = form.dates_are_blank_or_death_is_after_birth_date()
        self.assertIsFalse(result)

    def test_dates_are_blank_or_death_is_after_birth_date_returns_true_if_dod_is_after_dob(self):
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form_data['day_of_birth'] = '2'
        form_data['month_of_birth'] = '2'
        form_data['year_of_birth'] = '2019'
        form_data['day_of_death'] = '20'
        form_data['month_of_death'] = '2'
        form_data['year_of_death'] = '2019'
        form = PrimaryExaminationInformationForm(form_data)
        result = form.dates_are_blank_or_death_is_after_birth_date()
        self.assertIsTrue(result)

    def test_form_returns_is_invalid_if_dod_is_before_dob(self):
        form_data = ExaminationMocks.get_minimal_create_case_form_data()
        form_data['day_of_birth'] = '20'
        form_data['month_of_birth'] = '2'
        form_data['year_of_birth'] = '2019'
        form_data['day_of_death'] = '2'
        form_data['month_of_death'] = '2'
        form_data['year_of_death'] = '2019'
        form = PrimaryExaminationInformationForm(form_data)
        result = form.is_valid()
        self.assertIsFalse(result)

    def test_api_response_transformed_to_not_known_if_TOD_at_midnight(self):
        loaded_data = ExaminationMocks.get_patient_details_load_response_content()
        loaded_data['timeOfDeath'] = '00:00:00'

        patient_details = PatientDetails(loaded_data)
        form = PrimaryExaminationInformationForm()
        form.set_values_from_instance(patient_details)

        self.assertIsTrue(form.time_of_death_not_known)

    # Secondary Info Form tests

    def test_secondary_form_initialised_empty_returns_as_valid(self):
        form = SecondaryExaminationInformationForm()
        self.assertIsTrue(form.is_valid())

    def test_secondary_form_initialised_with_content_returns_as_valid(self):
        form = SecondaryExaminationInformationForm(ExaminationMocks.get_patient_details_secondary_info_form_data())
        self.assertIsTrue(form.is_valid())

    # Bereaved Info Form tests

    def test_bereaved_form_initialised_empty_returns_as_valid(self):
        form = BereavedInformationForm()
        self.assertIsTrue(form.is_valid())

    def test_bereaved_form_initialised_with_content_returns_as_valid(self):
        form = BereavedInformationForm(ExaminationMocks.get_patient_details_bereaved_form_data())
        self.assertIsTrue(form.is_valid())

    def test_bereaved_form_initialised_with_incomplete_date1_returns_as_invalid(self):
        form_data = ExaminationMocks.get_patient_details_bereaved_form_data()
        form_data['year_of_appointment_1'] = ''
        form = BereavedInformationForm(form_data)
        self.assertIsFalse(form.is_valid())

    def test_bereaved_form_initialised_with_invalid_date1_returns_as_invalid(self):
        form_data = ExaminationMocks.get_patient_details_bereaved_form_data()
        form_data['day_of_appointment_1'] = '31'
        form_data['month_of_appointment_1'] = '2'
        form = BereavedInformationForm(form_data)
        self.assertIsFalse(form.is_valid())

    def test_bereaved_form_initialised_with_incomplete_date2_returns_as_invalid(self):
        form_data = ExaminationMocks.get_patient_details_bereaved_form_data()
        form_data['year_of_appointment_2'] = ''
        form = BereavedInformationForm(form_data)
        self.assertIsFalse(form.is_valid())

    def test_bereaved_form_initialised_with_invalid_date2_returns_as_invalid(self):
        form_data = ExaminationMocks.get_patient_details_bereaved_form_data()
        form_data['day_of_appointment_2'] = '31'
        form_data['month_of_appointment_2'] = '2'
        form = BereavedInformationForm(form_data)
        self.assertIsFalse(form.is_valid())

    def test_form_initialised_from_db_correctly_sets_representatives(self):
        loaded_data = ExaminationMocks.get_patient_details_load_response_content()
        loaded_data['representatives'].append(PeopleMocks.get_bereaved_representative_response_dict())
        patient_details = PatientDetails(loaded_data)
        form = BereavedInformationForm()
        form.set_values_from_instance(patient_details)
        self.assertEqual(form.bereaved_name_1, loaded_data['representatives'][0]['fullName'])
        self.assertEqual(form.bereaved_name_2, '')

    # Urgency Info Form tests

    def test_urgency_form_initialised_empty_returns_as_valid(self):
        form = UrgencyInformationForm()
        self.assertIsTrue(form.is_valid())

    def test_urgency_form_initialised_with_content_returns_as_valid(self):
        form = UrgencyInformationForm(ExaminationMocks.get_patient_details_urgency_form_data())
        self.assertIsTrue(form.is_valid())


class MedicalTeamFormsTests(MedExTestCase):
    # Medical Team Form tests

    def test_medical_team_member_initialised_with_blank_nursing_team_information(self):
        mock_data = ExaminationMocks.get_medical_team_tab_form_data()
        form = MedicalTeamMembersForm(mock_data)
        nursing_team_information = form.nursing_team_information

        self.assertEquals(nursing_team_information, '')

    def test_medical_team_member_initialised_with_valid_medical_team_contains_lookups(self):
        medical_team = MedicalTeam(ExaminationMocks.get_medical_team_content(), ExaminationMocks.EXAMINATION_ID)

        self.assertGreater(len(medical_team.medical_examiner_lookup), 0)
        self.assertGreater(len(medical_team.medical_examiner_officer_lookup), 0)

    def test_medical_team_member_form_initialised_empty_returns_as_not_valid(self):
        form = MedicalTeamMembersForm()
        self.assertIsFalse(form.is_valid())
        self.assertEqual(form.errors['count'], 1)

    def test_medical_team_member_form_initialised_with_content_returns_as_valid(self):
        form = MedicalTeamMembersForm(ExaminationMocks.get_medical_team_tab_form_data())
        self.assertIsTrue(form.is_valid())

    def test_medical_team_member_form_initialised_with_valid_medical_team_returns_as_valid(self):
        medical_team = MedicalTeam(ExaminationMocks.get_medical_team_content(), ExaminationMocks.EXAMINATION_ID)
        form = MedicalTeamMembersForm(medical_team=medical_team)

        self.assertIsTrue(form.is_valid())

    def test_medical_team_member_form_without_consultant_1_is_not_valid(self):
        mock_data = ExaminationMocks.get_medical_team_tab_form_data()
        mock_data['consultant_name_1'] = ""
        mock_data['consultant_role_1'] = ""
        mock_data['consultant_organisation_1'] = ""
        mock_data['consultant_phone_number_1'] = ""
        form = MedicalTeamMembersForm(mock_data)

        self.assertIsFalse(form.is_valid())


class TimelineEventFormsTests(MedExTestCase):
    @staticmethod
    def get_participant_from_draft(draft_data):
        return MedicalTeamMember(name=draft_data["participantName"],
                                 role=draft_data["participantRole"],
                                 organisation=draft_data["participantOrganisation"],
                                 phone_number=draft_data["participantPhoneNumber"])

    @staticmethod
    def get_existing_bereaved_representative_from_draft(draft_data):
        return BereavedRepresentative({
            'fullName': draft_data.get("participantFullName"),
            'relationship': draft_data.get("participantRelationship"),
            'phoneNumber': draft_data.get("participantPhoneNumber")
        })

    # PreScrutinyEventForm

    def test_is_valid_returns_true_if_the_pre_scrutiny_form_is_valid(self):
        form = PreScrutinyEventForm({})
        self.assertIsTrue(form.is_valid())

    def test_for_request_correctly_maps_the_pre_scrutiny_form_for_the_api(self):
        me_thoughts = "Gentrify franzen heirloom raw denim gastropub activated charcoal listicle shaman."
        cod = 'Expected'
        possible_cod_1a = 'Cause of death'
        possible_cod_1b = ''
        possible_cod_1c = ''
        possible_cod_2 = ''
        ops = 'IssueAnMccd'
        gr = 'Yes'
        grt = 'Palliative care were called too late.'
        add_event_to_timeline = 'pre-scrutiny'

        form_data = {
            'me-thoughts': me_thoughts,
            'cod': cod,
            'possible-cod-1a': possible_cod_1a,
            'possible-cod-1b': possible_cod_1b,
            'possible-cod-1c': possible_cod_1c,
            'possible-cod-2': possible_cod_2,
            'ops': ops,
            'gr': gr,
            'grt': grt,
            'add-event-to-timeline': add_event_to_timeline
        }
        form = PreScrutinyEventForm(form_data)
        result = form.for_request()
        self.assertEqual(result.get('medicalExaminerThoughts'), me_thoughts)
        self.assertEqual(result.get('circumstancesOfDeath'), cod)
        self.assertEqual(result.get('causeOfDeath1a'), possible_cod_1a)
        self.assertEqual(result.get('causeOfDeath1b'), possible_cod_1b)
        self.assertEqual(result.get('causeOfDeath1c'), possible_cod_1c)
        self.assertEqual(result.get('causeOfDeath2'), possible_cod_2)
        self.assertEqual(result.get('outcomeOfPreScrutiny'), ops)
        self.assertEqual(result.get('clinicalGovernanceReview'), gr)
        self.assertEqual(result.get('clinicalGovernanceReviewText'), grt)
        self.assertEqual(result.get('isFinal'), True)

    # AdmissionNotesEventForm

    def test_is_valid_returns_true_if_the_admission_notes_form_is_valid(self):
        form = AdmissionNotesEventForm({})
        self.assertIsTrue(form.is_valid())

    def test_for_request_correctly_maps_the_admission_notes_form_for_the_api(self):
        admission_day = 2
        admission_month = 2
        admission_year = 2019
        admission_date_unknown = False
        admission_time = '10:00'
        admission_time_unknown = False
        admission_notes = "Gentrify franzen heirloom raw denim gastropub activated charcoal listicle shaman."
        coroner_referral = 'no'
        route_of_admission = 'ae'
        add_event_to_timeline = 'admission-notes'

        form_data = {
            'day_of_last_admission': admission_day,
            'month_of_last_admission': admission_month,
            'year_of_last_admission': admission_year,
            'date_of_last_admission_not_known': admission_date_unknown,
            'time_of_last_admission': admission_time,
            'time_of_last_admission_not_known': admission_time_unknown,
            'latest_admission_notes': admission_notes,
            'latest_admission_route': route_of_admission,
            'latest_admission_immediate_referral': coroner_referral,
            'add-event-to-timeline': add_event_to_timeline
        }

        form = AdmissionNotesEventForm(form_data)
        result = form.for_request()

        self.assertEqual(result.get("notes"), admission_notes)
        self.assertEqual(result.get("admittedDate"), form.admission_date())
        self.assertEqual(result.get("admittedTime"), admission_time)
        self.assertEqual(result.get('routeOfAdmission'), route_of_admission)
        self.assertEqual(result.get("immediateCoronerReferral"), False)
        self.assertEqual(result.get("isFinal"), True)

    def test_admission_date_returns_none_if_admission_date_unknown(self):
        admission_day = ''
        admission_month = ''
        admission_year = ''
        admission_date_unknown = enums.true_false.TRUE
        admission_time = '10:00'
        admission_time_unknown = enums.true_false.FALSE
        admission_notes = "Gentrify franzen heirloom raw denim gastropub activated charcoal listicle shaman."
        route_of_admission = 'ae'
        coroner_referral = 'no'
        add_event_to_timeline = 'admission-notes'

        form_data = {
            'day_of_last_admission': admission_day,
            'month_of_last_admission': admission_month,
            'year_of_last_admission': admission_year,
            'date_of_last_admission_not_known': admission_date_unknown,
            'time_of_last_admission': admission_time,
            'time_of_last_admission_not_known': admission_time_unknown,
            'latest_admission_notes': admission_notes,
            'latest_admission_route': route_of_admission,
            'latest-admission-suspect-referral': coroner_referral,
            'add-event-to-timeline': add_event_to_timeline
        }

        form = AdmissionNotesEventForm(form_data)
        result = form.admission_date()

        self.assertIsNone(result)

    # QapDiscussionEventForm

    def test_qap_discussion__request__maps_to_qap_discussion_api_put_request(self):
        # Given form data
        form_data = ExaminationMocks.get_mock_qap_discussion_form_data()
        form = QapDiscussionEventForm(form_data=form_data)

        # when we call data for an api request
        request = form.for_request()

        # then the data is not empty
        self.assertGreater(len(request), 0)

    def test_qap_discussion__request__maps_conversation_day_month_year_time_to_single_api_date(self):
        # Given form data with specific dates
        form_data = ExaminationMocks.get_mock_qap_discussion_form_data()
        form_data['qap_day_of_conversation'] = '20'
        form_data['qap_month_of_conversation'] = '5'
        form_data['qap_year_of_conversation'] = '2019'
        form_data['qap_time_of_conversation'] = '12:30'
        form = QapDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the returned date starts with the expected reverse date
        expected_date_start = '2019-05-20T12:30'
        self.assertTrue(request['dateOfConversation'].startswith(expected_date_start))

    def test_qap_discussion__request__maps_mccd_and_qap_combination_to_single_field(self):
        # Given form data with outcome that mccd is to be produced with decision version 1
        form_data = ExaminationMocks.get_mock_qap_discussion_form_data()
        form_data['qap-discussion-outcome'] = enums.outcomes.MCCD
        form_data['qap-discussion-outcome-decision'] = enums.outcomes.MCCD_FROM_QAP
        form = QapDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the outcome is mapped to option 1 - qap updates the decision
        self.assertEquals(request['qapDiscussionOutcome'], enums.outcomes.MCCD_FROM_QAP)

    def test_qap_discussion__request__maps_mccd_and_me_combination_to_single_field(self):
        # Given form data with outcome that mccd is to be produced with decision version 1
        form_data = ExaminationMocks.get_mock_qap_discussion_form_data()
        form_data['qap-discussion-outcome'] = enums.outcomes.MCCD
        form_data['qap-discussion-outcome-decision'] = enums.outcomes.MCCD_FROM_ME
        form = QapDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the outcome is mapped to option 2 - me's first decision
        self.assertEquals(request['qapDiscussionOutcome'], enums.outcomes.MCCD_FROM_ME)

    def test_qap_discussion__request__maps_mccd_and_agreement_combination_to_single_field(self):
        # Given form data with outcome that mccd is to be produced with decision version 1
        form_data = ExaminationMocks.get_mock_qap_discussion_form_data()
        form_data['qap-discussion-outcome'] = enums.outcomes.MCCD
        form_data['qap-discussion-outcome-decision'] = enums.outcomes.MCCD_FROM_QAP_AND_ME
        form = QapDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the outcome is mapped to option 3 - agreement
        self.assertEquals(request['qapDiscussionOutcome'], enums.outcomes.MCCD_FROM_QAP_AND_ME)

    def test_qap_discussion__request__maps_refer_to_coroner_and_100a_combination_to_single_field(self):
        # Given form data with outcome that mccd is to be produced with decision version 1
        form_data = ExaminationMocks.get_mock_qap_discussion_form_data()
        form_data['qap-discussion-outcome'] = enums.outcomes.CORONER
        form_data['qap-coroner-outcome-decision'] = enums.outcomes.CORONER_100A
        form = QapDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the outcome is mapped to coroner referral
        self.assertEquals(request['qapDiscussionOutcome'], enums.outcomes.CORONER_100A)

    def test_qap_discussion__request__maps_refer_to_coroner_and_investigation_combination_to_single_field(self):
        # Given form data with outcome that mccd is to be produced with decision version 1
        form_data = ExaminationMocks.get_mock_qap_discussion_form_data()
        form_data['qap-discussion-outcome'] = enums.outcomes.CORONER
        form_data['qap-coroner-outcome-decision'] = enums.outcomes.CORONER_INVESTIGATION
        form = QapDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the outcome is mapped to coroner referral
        self.assertEquals(request['qapDiscussionOutcome'], enums.outcomes.CORONER_INVESTIGATION)

    def test_qap_discussion__request__maps_default_qap_to_participant_if_discussion_type_qap_selected(self):
        # Given form data with the Default Qap radio button selected
        form_data = ExaminationMocks.get_mock_qap_discussion_form_data()
        form_data['qap-discussion-doctor'] = 'qap'
        form_data['qap-default__full-name'] = 'Default Qap'
        form_data['qap-other__full-name'] = 'Custom Qap'
        form = QapDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the default qap is assigned as participant
        self.assertEquals(request['participantName'], 'Default Qap')

    def test_qap_discussion__request__maps_custom_qap_to_participant_if_discussion_type_qap_selected(self):
        # Given form data with the Other Qap radio button selected
        form_data = ExaminationMocks.get_mock_qap_discussion_form_data()
        form_data['qap-discussion-doctor'] = 'other'
        form_data['qap-default__full-name'] = 'Default Qap'
        form_data['qap-other__full-name'] = 'Custom Qap'
        form = QapDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the custom qap is assigned as participant
        self.assertEquals(request['participantName'], 'Custom Qap')

    def test_qap_discussion__fill_from_draft__recalls_fields_from_api_event_draft(self):
        # Given draft data from the api
        draft_data = ExaminationMocks.get_mock_qap_discussion_draft_data()
        qap_draft = CaseQapDiscussionEvent(draft_data, 1)

        # When we fill a form using this data
        form = QapDiscussionEventForm().fill_from_draft(qap_draft, None)

        # Then the form is created
        self.assertEquals(draft_data["discussionDetails"], form.discussion_details)

    def test_qap_discussion__fill_from_draft__maps_single_conversation_date_to_day_month_year_time_fields(self):
        # Given draft data from the api with a specified test date
        draft_data = ExaminationMocks.get_mock_qap_discussion_draft_data()
        draft_data['dateOfConversation'] = "2019-04-08T08:30:00.000Z"
        qap_draft = CaseQapDiscussionEvent(draft_data, 1)

        # When we fill a form using this data
        form = QapDiscussionEventForm().fill_from_draft(qap_draft, None)

        # Then the form is filled with individual date fields
        self.assertEquals(form.day_of_conversation, 8)
        self.assertEquals(form.month_of_conversation, 4)
        self.assertEquals(form.year_of_conversation, 2019)
        self.assertEquals(form.time_of_conversation, "08:30")

    def test_qap_discussion__fill_from_draft__maps_null_conversation_date_to_empty_string_fields(self):
        # Given draft data from the api with a specified test date
        draft_data = ExaminationMocks.get_mock_qap_discussion_draft_data()
        draft_data['dateOfConversation'] = ""
        qap_draft = CaseQapDiscussionEvent(draft_data, 1)

        # When we fill a form using this data
        form = QapDiscussionEventForm().fill_from_draft(qap_draft, None)

        # Then the form is filled with individual date fields
        self.assertEquals(form.day_of_conversation, '')
        self.assertEquals(form.month_of_conversation, '')
        self.assertEquals(form.year_of_conversation, '')
        self.assertEquals(form.time_of_conversation, '')

    def test_qap_discussion__fill_from_draft__sets_type_as_qap_if_default_qap_matches_participant(self):
        # Given draft data from the api with a specified test date
        draft_data = ExaminationMocks.get_mock_qap_discussion_draft_data()
        qap_draft = CaseQapDiscussionEvent(draft_data, 1)

        # When we fill a form when the default
        qap_in_data = self.get_participant_from_draft(draft_data)
        form = QapDiscussionEventForm().fill_from_draft(qap_draft, default_qap=qap_in_data)

        # Then the form is filled with individual date fields
        self.assertEquals(form.discussion_participant_type, 'qap')

    def test_qap_discussion__fill_from_draft__sets_type_as_other_if_default_qap_doesnt_match_participant(self):
        # Given draft data from the api with a specified test date
        draft_data = ExaminationMocks.get_mock_qap_discussion_draft_data()
        qap_draft = CaseQapDiscussionEvent(draft_data, 1)

        # When we fill a form when the default
        any_medic = MedicalTeamMember(name='Any other qap')
        form = QapDiscussionEventForm().fill_from_draft(qap_draft, default_qap=any_medic)

        # Then the form is filled with individual date fields
        self.assertEquals(form.discussion_participant_type, 'other')

    # BereavedDiscussionEvent

    def test_bereaved_discussion__request__maps_to_bereaved_discussion_api_put_request(self):
        # Given form data
        form_data = ExaminationMocks.get_mock_bereaved_discussion_form_data()
        form = BereavedDiscussionEventForm(form_data=form_data)

        # when we call data for an api request
        request = form.for_request()

        # then the data is not empty
        self.assertGreater(len(request), 0)

    def test_bereaved_discussion__request__maps_conversation_day_month_year_time_to_single_api_date(self):
        # Given form data with specific dates
        form_data = ExaminationMocks.get_mock_bereaved_discussion_form_data()
        form_data['bereaved_day_of_conversation'] = '20'
        form_data['bereaved_month_of_conversation'] = '5'
        form_data['bereaved_year_of_conversation'] = '2019'
        form_data['bereaved_time_of_conversation'] = '12:30'
        form = BereavedDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the returned date starts with the expected reverse date
        expected_date_start = '2019-05-20T12:30'
        self.assertTrue(request['dateOfConversation'].startswith(expected_date_start))

    def test_bereaved_discussion__request__maps_no_concerns_to_a_single_field(self):
        # Given form data with outcome that there are no concerns
        form_data = ExaminationMocks.get_mock_bereaved_discussion_form_data()
        form_data['bereaved_discussion_outcome'] = BereavedDiscussionEventForm.BEREAVED_OUTCOME_NO_CONCERNS
        form = BereavedDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the combined outcomes are mapped to option 1 - Request_100a
        self.assertEquals(request['bereavedDiscussionOutcome'], BereavedDiscussionEventForm.REQUEST_OUTCOME_NO_CONCERNS)

    def test_bereaved_discussion__request__maps_concerns_leading_to_coroner_investigation_to_a_single_field(self):
        # Given form data with outcome that there are concerns and these should result in a 100a
        form_data = ExaminationMocks.get_mock_bereaved_discussion_form_data()
        form_data['bereaved_discussion_outcome'] = BereavedDiscussionEventForm.BEREAVED_OUTCOME_CONCERNS
        form_data[
            'bereaved_outcome_concerned_outcome'] = BereavedDiscussionEventForm.BEREAVED_CONCERNED_OUTCOME_CORONER
        form = BereavedDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the combined outcomes are mapped to option 2 - Coroner enquiry required
        self.assertEquals(request['bereavedDiscussionOutcome'], BereavedDiscussionEventForm.REQUEST_OUTCOME_CORONER)

    def test_bereaved_discussion__request__maps_concerns_leading_to_100a_to_a_single_field(self):
        # Given form data with outcome that there are concerns and these should result in a 100a
        form_data = ExaminationMocks.get_mock_bereaved_discussion_form_data()
        form_data['bereaved_discussion_outcome'] = BereavedDiscussionEventForm.BEREAVED_OUTCOME_CONCERNS
        form_data['bereaved_outcome_concerned_outcome'] = BereavedDiscussionEventForm.BEREAVED_CONCERNED_OUTCOME_100A
        form = BereavedDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the combined outcomes are mapped to option 3 - 100a required
        self.assertEquals(request['bereavedDiscussionOutcome'], BereavedDiscussionEventForm.REQUEST_OUTCOME_100A)

    def test_bereaved_discussion__request__maps_concerns_leading_to_agreement_to_a_single_field(self):
        # Given form data with outcome that there are concerns and these should result in a 100a
        form_data = ExaminationMocks.get_mock_bereaved_discussion_form_data()
        form_data['bereaved_discussion_outcome'] = BereavedDiscussionEventForm.BEREAVED_OUTCOME_CONCERNS
        form_data[
            'bereaved_outcome_concerned_outcome'] = BereavedDiscussionEventForm.BEREAVED_CONCERNED_OUTCOME_ADDRESSED
        form = BereavedDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the combined outcomes are mapped to option 4 - disagreements have been addressed
        self.assertEquals(request['bereavedDiscussionOutcome'], BereavedDiscussionEventForm.REQUEST_OUTCOME_ADDRESSED)

    def test_bereaved_discussion__request__maps_existing_rep_to_participant_if_existing_rep_selected(self):
        # Given form data with the Default Qap radio button selected
        form_data = ExaminationMocks.get_mock_bereaved_discussion_form_data()
        form_data['bereaved_rep_type'] = enums.people.BEREAVED_REP
        form_data['bereaved_existing_rep_name'] = 'Existing rep'
        form_data['bereaved_alternate_rep_name'] = 'Alternate rep'
        form = BereavedDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the default qap is assigned as participant
        self.assertEquals(request['participantFullName'], 'Existing rep')

    def test_bereaved_discussion__request__maps_alternate_rep_to_participant_if_alternate_rep_selected(self):
        # Given form data with the Default Qap radio button selected
        form_data = ExaminationMocks.get_mock_bereaved_discussion_form_data()
        form_data['bereaved_rep_type'] = enums.people.OTHER
        form_data['bereaved_existing_rep_name'] = 'Existing rep'
        form_data['bereaved_alternate_rep_name'] = 'Alternate rep'
        form = BereavedDiscussionEventForm(form_data=form_data)

        # when we call for an api request
        request = form.for_request()

        # then the default qap is assigned as participant
        self.assertEquals(request['participantFullName'], 'Alternate rep')

    def test_bereaved_discussion__fill_from_draft__recalls_fields_from_api_event_draft(self):
        # Given draft data from the api
        draft_data = ExaminationMocks.get_mock_bereaved_discussion_draft_data()
        bereaved_draft = CaseQapDiscussionEvent(draft_data, 1)

        # When we fill a form using this data
        form = QapDiscussionEventForm().fill_from_draft(bereaved_draft, None)

        # Then the form is created
        self.assertEquals(draft_data["discussionDetails"], form.discussion_details)

    def test_bereaved_discussion__fill_from_draft__maps_single_conversation_date_to_day_month_year_time_fields(self):
        # Given draft data from the api with a specified test date
        draft_data = ExaminationMocks.get_mock_bereaved_discussion_draft_data()
        draft_data['dateOfConversation'] = "2019-04-08T08:30:00.000Z"
        bereaved_draft = CaseBereavedDiscussionEvent(draft_data, 1)

        # When we fill a form using this data
        form = BereavedDiscussionEventForm().fill_from_draft(bereaved_draft, None)

        # Then the form is filled with individual date fields
        self.assertEquals(form.day_of_conversation, 8)
        self.assertEquals(form.month_of_conversation, 4)
        self.assertEquals(form.year_of_conversation, 2019)
        self.assertEquals(form.time_of_conversation, "08:30")

    def test_bereaved_discussion__fill_from_draft__maps_null_conversation_date_to_empty_string_fields(self):
        # Given draft data from the api with a specified test date
        draft_data = ExaminationMocks.get_mock_bereaved_discussion_draft_data()
        draft_data['dateOfConversation'] = ""
        bereaved_draft = CaseBereavedDiscussionEvent(draft_data, 1)

        # When we fill a form using this data
        form = BereavedDiscussionEventForm().fill_from_draft(bereaved_draft, None)

        # Then the form is filled with individual date fields
        self.assertEquals(form.day_of_conversation, '')
        self.assertEquals(form.month_of_conversation, '')
        self.assertEquals(form.year_of_conversation, '')
        self.assertEquals(form.time_of_conversation, '')

    def test_bereaved_discussion__fill_from_draft__sets_type_as_existing_if_existing_rep_matches_participant(self):
        # Given draft data from the api with a specified test date
        draft_data = ExaminationMocks.get_mock_bereaved_discussion_draft_data()
        bereaved_draft = CaseBereavedDiscussionEvent(draft_data, 1)

        # When we fill a form when the default
        representative_in_data = self.get_existing_bereaved_representative_from_draft(draft_data)
        form = BereavedDiscussionEventForm().fill_from_draft(bereaved_draft,
                                                             default_representatives=[representative_in_data])

        # Then the form is filled with individual date fields
        self.assertIsTrue(form.use_existing_bereaved)

    def test_bereaved_discussion__fill_from_draft__sets_type_as_other_if_existing_rep_doesnt_match_participant(self):
        # Given draft data from the api with a specified test date
        draft_data = ExaminationMocks.get_mock_bereaved_discussion_draft_data()
        bereaved_draft = CaseBereavedDiscussionEvent(draft_data, 1)

        # When we fill a form when the default
        mock_existing_rep = BereavedRepresentative(
            {
                "fullName": "mock",
                "relationship": "mock",
                "phoneNumber": "1234"
            }
        )
        form = BereavedDiscussionEventForm().fill_from_draft(bereaved_draft,
                                                             default_representatives=[mock_existing_rep])

        # Then the form is filled with individual date fields
        self.assertIsFalse(form.use_existing_bereaved)
