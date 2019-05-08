from django.shortcuts import render, redirect
from django.views.generic.base import View

from rest_framework import status

from errors.utils import log_unexpected_method, log_api_error
from errors.views import __handle_method_not_allowed_error
from home.utils import redirect_to_login, render_404
from medexCms.mixins import LoginRequiredMixin

from .forms import CreateUserForm
from .models import User


class ManageUserBaseView(View):

    def dispatch(self, request, *args, **kwargs):
        self.managed_user = User.load_by_id(kwargs['user_id'], self.user.auth_token)
        if self.managed_user is None:
            return render_404(request, self.user, 'user')
        return super().dispatch(request, *args, **kwargs)


class CreateUserView(LoginRequiredMixin, View):
    template = 'users/new.html'

    def get(self, request):
        status_code = status.HTTP_200_OK
        context = self.__set_create_user_context(CreateUserForm(), False)
        return render(request, self.template, context, status=status_code)

    def post(self, request):
        form = CreateUserForm(request.POST)

        if form.validate():
            response = User.create(form.response_to_dict(), self.user.auth_token)

            if response.ok:
                return redirect('/users/%s/add_permission' % response.json()['userId'])
            else:
                log_api_error('user creation', response.text)
                status_code = response.status_code
        else:
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


# def add_permission(request, user_id):
#     user = User.initialise_with_token(request)
#     if not user.check_logged_in():
#         return redirect_to_login()
#
#     managed_user = User.load_by_id(user_id, user.auth_token)
#     if managed_user is None:
#         return render_404(request, user, 'user')
#
#     if request.method == 'GET':
#         template, context, status_code = __get_add_permission(user, managed_user)
#
#     elif request.method == 'POST':
#         template, context, status_code, redirect_response = __post_add_permission(user, managed_user, request.POST)
#
#         if redirect_response:
#             return redirect_response
#
#     else:
#         log_unexpected_method(request.method, 'add permission')
#         template, context, status_code = __handle_method_not_allowed_error(user)
#
#     return render(request, template, context, status=status_code)


# def __get_add_permission(user, managed_user):
#     template = 'users/permission_builder.html'
#     status_code = status.HTTP_200_OK
#
#     context = __set_add_permission_context(user, PermissionBuilderForm(), False, managed_user)
#     return template, context, status_code


# def __post_add_permission(user, managed_user, post_body):
#     template = 'users/permission_builder.html'
#
#     form = PermissionBuilderForm(post_body)
#     add_another = True if post_body.get('add_another') == "true" else False
#
#     if form.is_valid():
#         response = managed_user.add_permission(form, user.auth_token)
#
#         if response.ok:
#             if add_another:
#                 return None, None, None, redirect('add_permission', user_id=managed_user.user_id)
#             else:
#                 return None, None, None, redirect('/settings')
#         else:
#             log_api_error('permission creation', response.text)
#             status_code = response.status_code
#
#     else:
#         status_code = status.HTTP_400_BAD_REQUEST
#
#     context = __set_add_permission_context(user, form, True, managed_user)
#
#     return template, context, status_code, None


# def __set_add_permission_context(user, form, invalid, managed_user):
#     trusts = user.get_permitted_trusts()
#     regions = user.get_permitted_regions()
#
#     return {
#         'session_user': user,
#         'sub_heading': 'Add role and permission level',
#         'form': form,
#         'submit_path': 'add_permission',
#         'invalid': invalid,
#         'trusts': trusts,
#         'regions': regions,
#         'managed_user': managed_user,
#     }
