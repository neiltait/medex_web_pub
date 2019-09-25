from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.views.generic.base import View

from rest_framework import status

from errors.utils import log_api_error
from home.utils import render_404
from medexCms.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .forms import CreateUserForm
from .models import User


class ManageUserBaseView(View):

    def dispatch(self, request, *args, **kwargs):
        self.managed_user = User.load_by_id(kwargs.get('user_id'), self.user.auth_token)
        if self.managed_user is None:
            return render_404(request, self.user, 'user')

        self.managed_user.load_permissions(self.user.auth_token)

        return super().dispatch(request, *args, **kwargs)


class CreateUserView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'can_invite_user'
    template = 'users/new.html'

    @never_cache
    def get(self, request):
        status_code = status.HTTP_200_OK
        context = self.__set_create_user_context(CreateUserForm(), False)
        return render(request, self.template, context, status=status_code)

    @never_cache
    def post(self, request):
        form = CreateUserForm(request.POST)

        if form.validate():
            response = User.create(form.response_to_dict(), self.user.auth_token)

            if response.ok:
                # 1. success
                return redirect('/users/%s/add_permission' % response.json()['userId'])
            else:
                # 2. api error
                log_api_error('user creation', response.text)
                form.register_response_errors(response)
                status_code = response.status_code
        else:
            # 3. front end error
            status_code = status.HTTP_400_BAD_REQUEST

        context = self.__set_create_user_context(form, True)
        return render(request, self.template, context, status=status_code)

    def __set_create_user_context(self, form, invalid):
        return {
            'session_user': self.user,
            'page_heading': 'Add a user',
            'form': form,
            'invalid': invalid,
        }


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'can_get_users'
    template = 'users/list.html'

    @never_cache
    def get(self, request):
        status_code = status.HTTP_200_OK
        users = User.get_all(self.user.auth_token)
        context = {
            'session_user': self.user,
            'page_heading': 'Users in the ME Network',
            'users': users
        }

        return render(request, self.template, context, status=status_code)


class ManageUserView(LoginRequiredMixin, PermissionRequiredMixin, ManageUserBaseView, View):
    permission_required = 'can_get_users'
    template = 'users/manage.html'

    def get(self, request, user_id):
        status_code = status.HTTP_200_OK
        context = {
            'session_user': self.user,
            'managed_user': self.managed_user,
        }

        return render(request, self.template, context, status=status_code)

