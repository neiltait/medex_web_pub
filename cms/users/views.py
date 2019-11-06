from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.views.generic.base import View

from rest_framework import status

from errors.utils import log_api_error
from home.utils import render_404
from medexCms.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .forms import CreateUserForm, ManageUserForm, EditUserProfileForm
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


class EditUserProfileView(LoginRequiredMixin, View):
    template = 'users/profile.html'

    def get(self, request):
        status_code = status.HTTP_200_OK
        form = EditUserProfileForm.from_user(self.user)

        context = {'session_user': self.user, 'form': form}

        return render(request, self.template, context)

    def post(self, request):
        form = EditUserProfileForm(request.POST)
        submission = form.response_to_dict()

        response = User.update_profile(submission, self.user.auth_token)

        if response.ok:
            # 1. success
            return redirect('/profile')
        else:
            # 2. api error
            form.register_response_errors(response)
            status_code = response.status_code

        context = {'session_user': self.user, 'form': form}
        return render(request, self.template, context=context, status=status_code)


class ManageUserView(LoginRequiredMixin, PermissionRequiredMixin, ManageUserBaseView, View):
    permission_required = 'can_get_users'
    template = 'users/manage.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.form = ManageUserForm()

    def get(self, request, user_id):
        self.form = ManageUserForm.from_user(self.managed_user)
        status_code = status.HTTP_200_OK

        return render(request, self.template, self.get_context(), status=status_code)

    def post(self, request, user_id):
        self.form = ManageUserForm(request.POST)
        submission = self.form.response_to_dict()
        submission["user_id"] = user_id

        response = User.update_profile(submission, self.user.auth_token, user_id)

        if response.ok:
            # 1. success
            return redirect('/users/%s/manage' % self.managed_user.user_id)
        else:
            # 2. api error
            self.form.register_response_errors(response)
            status_code = response.status_code

        return render(request, self.template, self.get_context(), status=status_code)

    def get_context(self):
        return {
            'session_user': self.user,
            'managed_user': self.managed_user,
            'form': self.form
        }
