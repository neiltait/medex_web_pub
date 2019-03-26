from rest_framework import status

from unittest.mock import patch

from medexCms.test import mocks
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

    @patch('users.request_handler.validate_session', return_value=mocks.SUCCESSFUL_VALIDATE_SESSION)
    @patch('permissions.request_handler.load_permissions_for_user', return_value=mocks.SUCCESSFUL_PERMISSION_LOAD)
    def test_login_returns_redirect_to_landing_page_if_user_logged_in(self, mock_auth_validation, mock_permission_load):
        self.set_auth_cookies()
        response = self.client.get('/login')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/')

    # Logout tests

    @patch('home.request_handler.end_session', return_value=mocks.SUCCESSFUL_LOGOUT)
    def test_logout_returns_redirect_to_login_page_on_submission(self, mock_logout):
        self.set_auth_cookies()
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/login')

    # Login callback tests

    @patch('home.request_handler.create_session', return_value=mocks.SUCCESSFUL_TOKEN_GENERATION)
    def test_login_callback_returns_redirect_to_landing_page(self, mock_token_generation):
        response = self.client.get('/login-callback?code=c15be3d1-513f-49dc-94f9-47449c1cfeb8')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/')

    # Index tests

    @patch('users.request_handler.validate_session', return_value=mocks.SUCCESSFUL_VALIDATE_SESSION)
    @patch('examinations.request_handler.load_examinations_index', return_value=mocks.SUCCESSFUL_CASE_INDEX)
    @patch('permissions.request_handler.load_permissions_for_user', return_value=mocks.SUCCESSFUL_PERMISSION_LOAD)
    def test_landing_on_the_landing_page_returns_the_correct_template(self, mock_auth_validation, mock_load_cases,
                                                                      mock_permission_load):
        self.set_auth_cookies()
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'home/index.html')
        context_user = self.get_context_value(response.context, 'session_user')
        self.assertIsNot(context_user.examinations,  None)
        self.assertIs(type(context_user.examinations), list)

        count = len(mocks.USERS_EXAMINATION_LIST)
        self.assertEqual(len(context_user.examinations), count)

    def test_landing_on_the_landing_page_redirects_to_login_if_the_user_not_logged_in(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/login')

    # Settings index tests

    @patch('users.request_handler.validate_session', return_value=mocks.SUCCESSFUL_VALIDATE_SESSION)
    @patch('permissions.request_handler.load_permissions_for_user', return_value=mocks.SUCCESSFUL_PERMISSION_LOAD)
    def test_landing_on_settigs_page_returns_the_correct_template_and_content_if_you_are_logged_in(self,
                                                                   mock_auth_validation, mock_permission_load):
        self.set_auth_cookies()
        response = self.client.get('/settings')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'home/settings_index.html')

    @patch('users.request_handler.validate_session', return_value=mocks.UNSUCCESSFUL_VALIDATE_SESSION)
    @patch('permissions.request_handler.load_permissions_for_user', return_value=mocks.SUCCESSFUL_PERMISSION_LOAD)
    def test_landing_on_settigs_page_returns_the_correct_template_and_content_if_you_are_not_logged_in(self,
                                                                           mock_auth_validation, mock_permission_load):
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
