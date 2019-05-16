from rest_framework import status

from unittest.mock import patch

from medexCms.test.mocks import SessionMocks, ExaminationMocks
from medexCms.test.utils import MedExTestCase

from .utils import redirect_to_landing, redirect_to_login


class HomeViewsTests(MedExTestCase):

    # Login tests

    def test_landing_on_login_page_loads_the_correct_template_with_empty_context(self):
        response = self.client.get('/login')
        self.assertTemplateUsed(response, 'home/login.html')
        try:
            self.assertEqual(self.get_context_value(response.context, 'email_address'), None)
            self.assertFalse('Test failed to produce expected key error')
        except KeyError:
            self.assertTrue('Test produced expected key error')

    def test_login_returns_redirect_to_landing_page_if_user_logged_in(self):
        self.set_auth_cookies()
        response = self.client.get('/login')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/')

    # Logout tests

    @patch('home.request_handler.end_session', return_value=SessionMocks.get_successful_logout_response())
    def test_logout_returns_redirect_to_login_page_on_submission(self, mock_logout):
        self.set_auth_cookies()
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/login')

    # Login callback tests

    @patch('home.request_handler.create_session', return_value=SessionMocks.get_successful_token_generation_response())
    def test_login_callback_returns_redirect_to_landing_page(self, mock_token_generation):
        response = self.client.get('/login-callback?code=c15be3d1-513f-49dc-94f9-47449c1cfeb8')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/')

    # Index tests

    def test_landing_on_the_landing_page_returns_the_correct_template(self):
        self.set_auth_cookies()
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'home/index.html')
        context_user = self.get_context_value(response.context, 'session_user')
        self.assertIsNot(context_user.examinations,  None)
        self.assertIs(type(context_user.examinations), list)

        count = len(ExaminationMocks.get_case_index_response_content().get('examinations'))
        self.assertEqual(len(context_user.examinations), count)

    @patch('users.request_handler.validate_session', return_value=SessionMocks.get_unsuccessful_validate_session_response())
    def test_landing_on_the_landing_page_redirects_to_login_if_the_user_not_logged_in(self, mock_auth_validation):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/login')

    def test_posting_filters_to_the_landing_page_returns_the_correctly_set_filters(self):
        self.set_auth_cookies()
        filter_options = {"location": '1'}
        response = self.client.post('/', filter_options)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'home/index.html')
        context_user = self.get_context_value(response.context, 'session_user')
        self.assertIsNot(context_user.examinations, None)
        self.assertIs(type(context_user.examinations), list)

        count = len(ExaminationMocks.get_case_index_response_content().get('examinations'))
        self.assertEqual(len(context_user.examinations), count)

        context_form = self.get_context_value(response.context, 'form')
        self.assertEqual(context_form.location, '1')
        self.assertEqual(context_form.person, None)

    # Settings index tests

    def test_landing_on_settigs_page_returns_the_correct_template_and_content_if_you_are_logged_in(self):
        self.set_auth_cookies()
        response = self.client.get('/settings')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'home/settings_index.html')

    @patch('users.request_handler.validate_session', return_value=SessionMocks.get_unsuccessful_validate_session_response())
    def test_landing_on_settigs_page_returns_the_correct_template_and_content_if_you_are_not_logged_in(self,
                                                                           mock_auth_validation):
        response = self.client.get('/settings')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/login')


class HomeFormsTests(MedExTestCase):
    pass


class HomeUtilsTests(MedExTestCase):

    # Redirect to landing tests

    def test_redirect_to_landing_returns_the_correct_status_code_and_path(self):
        result = redirect_to_landing()
        self.assertEqual(result.status_code, status.HTTP_302_FOUND)
        self.assertEqual(result.url, '/')

    # Redirect to login tests

    def test_redirect_to_login_returns_the_correct_status_code_and_path(self):
        result = redirect_to_login()
        self.assertEqual(result.status_code, status.HTTP_302_FOUND)
        self.assertEqual(result.url, '/login')
