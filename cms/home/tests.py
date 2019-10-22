from rest_framework import status

from unittest.mock import patch

from home.templatetags.home_filters import page_range_presenter, PAGE_PRESENTER_ITEM_MAX
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

    # Login refresh tests

    @patch('home.request_handler.refresh_session', return_value=SessionMocks.get_successful_refresh_token_response())
    def test_login_refresh_with_cookies_returns_success(self, mock_token_generation):
        self.set_auth_cookies()
        response = self.client.post('/login-refresh')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('home.request_handler.refresh_session', return_value=SessionMocks.get_successful_refresh_token_response())
    def test_login_refresh_without_cookies_returns_400(self, mock_token_generation):
        self.clear_auth_cookies()
        response = self.client.post('/login-refresh')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Index tests

    def test_landing_on_the_landing_page_returns_the_correct_template(self):
        self.set_auth_cookies()
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'home/index.html')
        context_user = self.get_context_value(response.context, 'session_user')
        self.assertIsNot(context_user.examinations, None)
        self.assertIs(type(context_user.examinations), list)

        count = len(ExaminationMocks.get_case_index_response_content().get('examinations'))
        self.assertEqual(len(context_user.examinations), count)

    @patch('examinations.request_handler.load_examinations_index',
           return_value=ExaminationMocks.get_successful_minimal_case_index_response())
    def test_landing_on_the_landing_page_renders_page_when_no_examinations_present(self, mock_response):
        self.set_auth_cookies()
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'home/index.html')

    @patch('users.request_handler.validate_session',
           return_value=SessionMocks.get_unsuccessful_validate_session_response())
    def test_landing_on_the_landing_page_redirects_to_login_if_the_user_not_logged_in(self, mock_auth_validation):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/login')

    def test_sending_filters_to_the_landing_page_returns_the_correctly_set_filters(self):
        self.set_auth_cookies()
        response = self.client.get('/?page_number=1&location=1')
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

    def test_sending_negative_page_number_to_the_landing_page_redirects_to_landing_root(self):
        self.set_auth_cookies()
        response = self.client.get('/?page_number=-1')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/')

    def test_sending_too_large_page_number_to_the_landing_page_redirects_to_landing_root(self):
        self.set_auth_cookies()
        response = self.client.get('/?page_number=10000')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/')

    def test_sending_too_large_page_number_to_the_landing_page_redirects_to_landing_root_with_filters(self):
        self.set_auth_cookies()
        response = self.client.get('/?page_number=10000&status=Unknown')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/?status=Unknown')
        
    def test_sending_location_and_person_filters_to_the_landing_page_builds_base_url_for_filter_buttons(self):
        self.set_auth_cookies()

        response = self.client.get('/')
        self.assertEqual(self.get_context_value(response.context, 'base_url'), '/?')

        response = self.client.get('/?location=bar')
        self.assertEqual(self.get_context_value(response.context, 'base_url'), '/?location=bar&')

        response = self.client.get('/?person=1')
        self.assertEqual(self.get_context_value(response.context, 'base_url'), '/?person=1&')

        response = self.client.get('/?person=1&location=bar')
        self.assertEqual(self.get_context_value(response.context, 'base_url'), '/?location=bar&person=1&')

    def test_page_filters_removed_when_landing_page_builds_base_url_for_filter_buttons(self):
        self.set_auth_cookies()

        response = self.client.get('/?person=1&location=bar&page_number=1')
        self.assertEqual(self.get_context_value(response.context, 'base_url'), '/?location=bar&person=1&')

    def test_case_status_removed_when_landing_page_builds_base_url_for_filter_buttons(self):
        self.set_auth_cookies()

        response = self.client.get('/?person=1&location=bar&page_number=1&case_status="Unassigned')
        self.assertEqual(self.get_context_value(response.context, 'base_url'), '/?location=bar&person=1&')

    # Settings index tests

    def test_landing_on_settigs_page_returns_the_correct_template_and_content_if_you_are_logged_in(self):
        self.set_auth_cookies()
        response = self.client.get('/settings')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'home/settings_index.html')

    @patch('users.request_handler.validate_session',
           return_value=SessionMocks.get_unsuccessful_validate_session_response())
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


class MockIndexOverview():
    def __init__(self, page_min, page_max, active_page):
        self.page_number = active_page
        self.page_range = range(page_min - 1, page_max)
        self.page_count = page_max


class HomeTemplateTagsTest(MedExTestCase):

    def test_page_range_presenter__in_trivial_case_returns_correct_number_of_pages(self):
        small_page_count = PAGE_PRESENTER_ITEM_MAX - 1
        index_overview = MockIndexOverview(1, small_page_count, 1)

        page_range = page_range_presenter(index_overview)

        self.assertEqual(len(page_range), small_page_count)

    def test_page_range_presenter_in_trivial_case_makes_selected_page_active(self):
        small_page_count = PAGE_PRESENTER_ITEM_MAX - 1
        selected_page_number = 5
        index_overview = MockIndexOverview(1, small_page_count, selected_page_number)

        page_range = page_range_presenter(index_overview)
        page_item = page_range[selected_page_number - 1]

        self.assertEqual(page_item['type'], 'active')

    def test_page_range_presenter_in_trivial_case_makes_non_selected_pages_links(self):
        small_page_count = PAGE_PRESENTER_ITEM_MAX - 1
        selected_page_number = 5
        index_overview = MockIndexOverview(1, small_page_count, selected_page_number)

        page_range = page_range_presenter(index_overview)
        page_item = page_range[0]

        self.assertEqual(page_item['type'], 'link')

    def test_page_range_presenter_truncates_number_of_items_to_maximum(self):
        big_item_count = PAGE_PRESENTER_ITEM_MAX + 50

        index_overview = MockIndexOverview(1, big_item_count, 1)

        page_range = page_range_presenter(index_overview)

        self.assertEqual(len(page_range), PAGE_PRESENTER_ITEM_MAX)

    def test_page_range_presenter_in_middle_of_large_range_puts_spacer_at_position_2(self):
        big_item_count = PAGE_PRESENTER_ITEM_MAX + 50
        active_page = 37
        index_overview = MockIndexOverview(1, big_item_count, active_page)

        page_range = page_range_presenter(index_overview)
        second_item = page_range[1]

        self.assertEqual(second_item['type'], 'spacer')

    def test_page_range_presenter_in_middle_of_large_range_puts_spacer_at_penultimate_position(self):
        big_item_count = PAGE_PRESENTER_ITEM_MAX + 50
        penultimate_position = PAGE_PRESENTER_ITEM_MAX - 2
        active_page = 37
        index_overview = MockIndexOverview(1, big_item_count, active_page)

        page_range = page_range_presenter(index_overview)
        penultimate_item = page_range[penultimate_position]

        self.assertEqual(penultimate_item['type'], 'spacer')

    def test_page_range_presenter_in_middle_of_large_range_puts_active_page_at_center(self):
        middle_index = PAGE_PRESENTER_ITEM_MAX // 2
        big_item_count = PAGE_PRESENTER_ITEM_MAX + 50
        active_page = 37
        index_overview = MockIndexOverview(1, big_item_count, active_page)

        page_range = page_range_presenter(index_overview)
        middle_item = page_range[middle_index]

        self.assertEqual(middle_item['page'], active_page)
        self.assertEqual(middle_item['type'], 'active')

    def test_page_range_presenter_at_start_of_large_range_doesnt_put_spacer_at_start(self):
        big_item_count = PAGE_PRESENTER_ITEM_MAX + 50

        index_overview_1 = MockIndexOverview(1, big_item_count, 1)
        index_overview_2 = MockIndexOverview(1, big_item_count, 2)
        index_overview_3 = MockIndexOverview(1, big_item_count, 3)

        page_range_1 = page_range_presenter(index_overview_1)
        page_range_2 = page_range_presenter(index_overview_2)
        page_range_3 = page_range_presenter(index_overview_3)

        self.assertNotEqual(page_range_1[1]['type'], 'spacer')
        self.assertNotEqual(page_range_2[1]['type'], 'spacer')
        self.assertNotEqual(page_range_3[1]['type'], 'spacer')

    def test_page_range_presenter_at_end_of_large_range_doesnt_put_spacer_at_end(self):
        big_item_count = PAGE_PRESENTER_ITEM_MAX + 50

        index_overview_1 = MockIndexOverview(1, big_item_count, big_item_count)
        index_overview_2 = MockIndexOverview(1, big_item_count, big_item_count - 1)
        index_overview_3 = MockIndexOverview(1, big_item_count, big_item_count - 2)

        page_range_1 = page_range_presenter(index_overview_1)
        page_range_2 = page_range_presenter(index_overview_2)
        page_range_3 = page_range_presenter(index_overview_3)

        self.assertNotEqual(page_range_1[PAGE_PRESENTER_ITEM_MAX - 2]['type'], 'spacer')
        self.assertNotEqual(page_range_2[PAGE_PRESENTER_ITEM_MAX - 2]['type'], 'spacer')
        self.assertNotEqual(page_range_3[PAGE_PRESENTER_ITEM_MAX - 2]['type'], 'spacer')
