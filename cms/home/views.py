from django.conf import settings
from django.shortcuts import render
from django.views.generic.base import View

from rest_framework import status

from home.forms import IndexFilterForm
from medexCms.mixins import LoginRequiredMixin, LoggedInMixin, PermissionRequiredMixin
from . import request_handler
from .utils import redirect_to_landing, redirect_to_login

from users.models import User


class DashboardView(LoginRequiredMixin, View):
    template = 'home/index.html'

    def get(self, request):
        status_code = status.HTTP_200_OK
        query_params = request.GET

        page_number = int(query_params.get('page_number')) if query_params.get('page_number') else 1
        page_size = 25

        form = IndexFilterForm(query_params, self.user.default_filter_options())
        self.user.load_examinations(page_size, page_number, form.get_location_value(), form.get_person_value())

        context = self.set_context(form)

        return render(request, self.template, context, status=status_code)

    def set_context(self, form):
        return {
            'page_header': '%s Dashboard' % self.user.display_role(),
            'session_user': self.user,
            'form': form,
            'pagination_url': 'index',
        }


class LoginCallbackView(View):

    def get(self, request):
        token_response = request_handler.create_session(request.GET.get('code'))
        response = redirect_to_landing()
        id_token = token_response.json().get('id_token')
        auth_token = token_response.json().get('access_token')
        refresh_token = token_response.json().get('refresh_token')
        response.set_cookie(settings.AUTH_TOKEN_NAME, auth_token)
        response.set_cookie(settings.ID_TOKEN_NAME, id_token)
        response.set_cookie(settings.REFRESH_TOKEN_NAME, refresh_token)
        return response


class LoginView(LoggedInMixin, View):
    template = 'home/login.html'

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

    def get(self, request):
        user = User.initialise_with_token(request)
        user.logout()

        response = redirect_to_login()
        response.delete_cookie(settings.AUTH_TOKEN_NAME)
        response.delete_cookie(settings.ID_TOKEN_NAME)
        return response


class SettingsIndexView(LoginRequiredMixin, PermissionRequiredMixin, View):
    template = 'home/settings_index.html'
    permission_required = 'can_get_users'

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
