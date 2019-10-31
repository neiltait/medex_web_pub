import json

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from rest_framework import status

from home.forms import IndexFilterForm
from medexCms.api import enums
from medexCms.mixins import LoginRequiredMixin, LoggedInMixin, PermissionRequiredMixin
from . import request_handler
from .utils import redirect_to_landing, redirect_to_login, redirect_to_landing_with_filters
from django.views.decorators.cache import never_cache

from users.models import User


class CookiesPolicyView(View):
    template = 'home/cookies.html'

    @never_cache
    def get(self, request):
        return render(request, self.template, {}, status=status.HTTP_200_OK)


class DashboardView(LoginRequiredMixin, View):
    template = 'home/index.html'

    @never_cache
    def get(self, request):
        status_code = status.HTTP_200_OK
        query_params = request.GET

        page_number, page_size, page_error = self.calc_pagination(query_params)
        if page_error:
            return redirect_to_landing()

        form = IndexFilterForm(query_params, self.user.default_filter_options())
        self.user.load_examinations(page_size, page_number, form.get_location_value(), form.get_person_value(),
                                    form.get_case_status(), form.sorting_order)

        if self.page_number_exceeds_total_pages(page_number):
            return redirect_to_landing_with_filters(location=form.get_location_value(), person=form.get_person_value(),
                                                    status=form.get_case_status())

        context = self.set_context(form)

        return render(request, self.template, context, status=status_code)

    def page_number_exceeds_total_pages(self, page_number):
        return page_number > self.user.index_overview.page_count and page_number != 1

    def calc_pagination(self, query_params):
        page_number = int(query_params.get('page_number')) if query_params.get('page_number') else 1
        page_size = 25
        page_error = page_number < 1

        return page_number, page_size, page_error

    @staticmethod
    def active_filter_obj(filter_objs: dict, active_filter: str or None) -> dict or None:
        """
        Return filter object attribute of filter_class with 'filter' matching active_filter, or None if not
        found.
        """
        try:
            return next(
                filter_obj for filter_obj in filter_objs.values() if filter_obj['filter'] == active_filter
            )
        except StopIteration:
            return None

    @staticmethod
    def filter_count(filter_obj: dict or None, session_user_obj: User) -> int:
        """
        Return examination count for all filter_obj based on the User.index_overview object.
        """
        return getattr(session_user_obj.index_overview, filter_obj['index_overview_key']) if filter_obj \
            else session_user_obj.index_overview.total_cases

    def set_context(self, form):
        active_filter_obj = self.active_filter_obj(enums.filters, form.case_status)
        return {
            'page_header': '%s Dashboard' % self.user.display_role(),
            'session_user': self.user,
            'form': form,
            'pagination_url': 'index',
            'enums': enums,
            'active_filter_obj': active_filter_obj,
            'current_examination_count': self.filter_count(active_filter_obj, self.user),
            'page_examination_count': self.user.examinations_count()
        }


class LoginCallbackView(View):

    @never_cache
    def get(self, request):
        token_response = request_handler.create_session(request.GET.get('code'))
        response = redirect_to_landing()
        id_token = token_response.json().get('id_token')
        auth_token = token_response.json().get('access_token')
        refresh_token = token_response.json().get('refresh_token')
        response.set_cookie(settings.AUTH_TOKEN_NAME, auth_token, secure=settings.REQUIRE_HTTPS)
        response.set_cookie(settings.ID_TOKEN_NAME, id_token, secure=settings.REQUIRE_HTTPS)
        response.set_cookie(settings.REFRESH_TOKEN_NAME, refresh_token, secure=settings.REQUIRE_HTTPS)

        response.set_cookie(settings.DO_NOT_REFRESH_COOKIE, value="OKTA token is current",
                            max_age=settings.REFRESH_PERIOD, secure=settings.REQUIRE_HTTPS)

        return response


class LoginRefreshView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRefreshView, self).dispatch(request, *args, **kwargs)

    @never_cache
    def post(self, request):
        refresh_token = request.COOKIES.get(settings.REFRESH_TOKEN_NAME)
        if refresh_token:
            token_response = request_handler.refresh_session(refresh_token)
            response = HttpResponse(json.dumps({"status": "success"}), content_type="application/json", status=200)

            id_token = token_response.json().get('id_token')
            auth_token = token_response.json().get('access_token')
            refresh_token = token_response.json().get('refresh_token')
            response.set_cookie(settings.AUTH_TOKEN_NAME, auth_token, secure=settings.REQUIRE_HTTPS)
            response.set_cookie(settings.ID_TOKEN_NAME, id_token, secure=settings.REQUIRE_HTTPS)
            response.set_cookie(settings.REFRESH_TOKEN_NAME, refresh_token, secure=settings.REQUIRE_HTTPS)

            response.set_cookie(settings.DO_NOT_REFRESH_COOKIE, value="OKTA token is current",
                                max_age=settings.REFRESH_PERIOD, secure=settings.REQUIRE_HTTPS)

            return response

        return HttpResponse(json.dumps({"error": "could not refresh", "code": 400}),
                            content_type="application/json", status=400)


class LoginView(LoggedInMixin, View):
    template = 'home/login.html'

    @never_cache
    def get(self, request):
        status_code = status.HTTP_200_OK
        context = {
            'page_heading': 'Welcome to the Medical Examiners Service',
            'base_uri': settings.OP_DOMAIN,
            'client_id': settings.OP_ID,
            'cms_url': settings.CMS_URL,
            'issuer': settings.OP_ISSUER,
        }

        return render(request, self.template, context, status=status_code)


class LogoutView(View):

    @never_cache
    def get(self, request):
        user = User.initialise_with_token(request)
        user.logout()

        response = redirect_to_login()
        response.delete_cookie(settings.AUTH_TOKEN_NAME)
        response.delete_cookie(settings.ID_TOKEN_NAME)
        response.delete_cookie(settings.REFRESH_TOKEN_NAME)
        response.delete_cookie(settings.DO_NOT_REFRESH_COOKIE)
        return response


class SettingsIndexView(LoginRequiredMixin, PermissionRequiredMixin, View):
    template = 'home/settings_index.html'
    permission_required = 'can_get_users'

    @never_cache
    def get(self, request):
        status_code = status.HTTP_200_OK
        users = User.get_all(self.user.auth_token)

        context = {
            'session_user': self.user,
            'page_heading': 'Settings',
            'sub_heading': 'Overview',
            'user_count': len(users)
        }

        return render(request, self.template, context, status=status_code)


class AccessibilityPolicyView(View):
    template = 'home/accessibility.html'

    @never_cache
    def get(self, request):
        return render(request, self.template, {}, status=status.HTTP_200_OK)


class PrivacyPolicyView(View):
    template = 'home/privacy.html'

    @never_cache
    def get(self, request):
        return render(request, self.template, {}, status=status.HTTP_200_OK)
