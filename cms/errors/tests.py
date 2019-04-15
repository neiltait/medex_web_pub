from alerts import messages
from errors.models import GenericError, NotFoundError
from errors.utils import handle_error
from medexCms.test.mocks import ExaminationMocks, SessionMocks
from medexCms.test.utils import MedExTestCase


class ErrorsModelTests(MedExTestCase):

    # GenericError tests

    def test_get_message_returns_the_base_message_with_the_action_and_object_in(self):
        action = 'loading'
        object_type = 'case'
        error_params = {
            'action': action,
            'type': object_type
        }
        error = GenericError(ExaminationMocks.get_unsuccessful_patient_details_load_response(), error_params)
        self.assertEqual(error.get_message(), messages.GENERAL_ERROR % (action, object_type))

    def test_status_code_returns_the_status_code_of_the_response_object(self):
        action = 'loading'
        object_type = 'case'
        error_params = {
            'action': action,
            'type': object_type
        }
        response = ExaminationMocks.get_unsuccessful_patient_details_load_response()
        error = GenericError(response, error_params)
        self.assertEqual(error.status_code, response.status_code)

    def test_stack_trace_returns_none_if_settings_debug_is_false(self):
        action = 'loading'
        object_type = 'case'
        error_params = {
            'action': action,
            'type': object_type
        }
        response = ExaminationMocks.get_unsuccessful_patient_details_load_response()
        error = GenericError(response, error_params)
        self.assertEqual(error.stack_trace, None)


class ErrorsUtilTests(MedExTestCase):

    def test_handle_error_returns_a_not_found_error_if_a_404_passed_in(self):
        response = ExaminationMocks.get_unsuccessful_patient_details_load_response()
        result = handle_error(response, {})
        self.assertEqual(type(result), NotFoundError)

    def test_handle_error_returns_a_generic_error_if_a_non_404_passed_in(self):
        response = SessionMocks.get_unsuccessful_validate_session_response()
        result = handle_error(response, {})
        self.assertEqual(type(result), GenericError)
