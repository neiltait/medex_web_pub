from django.views import View
from rest_framework import status
from django.shortcuts import render, redirect

from errors.utils import log_api_error
from locations.models import Location
from medexCms.mixins import LoginRequiredMixin, PermissionRequiredMixin
from permissions.forms import PermissionBuilderForm
from permissions.models import Permission
from users.views import ManageUserBaseView


class AddPermissionView(LoginRequiredMixin, PermissionRequiredMixin, ManageUserBaseView):
    permission_required = 'can_create_user_permission'
    template = 'users/permission_builder.html'

    def get(self, request, user_id):
        status_code = status.HTTP_200_OK

        context = self.__set_add_permission_context(PermissionBuilderForm(), False)
        return render(request, self.template, context, status=status_code)

    def post(self, request, user_id):
        post_body = request.POST
        status_code = status.HTTP_200_OK
        invalid = False
        form = PermissionBuilderForm(post_body)
        add_another = True if post_body.get('add_another') == "true" else False

        if form.is_valid():
            response = self.managed_user.add_permission(form, self.user.auth_token)

            if response.ok:
                if add_another:
                    form = PermissionBuilderForm()
                else:
                    return redirect('/settings')
            else:
                invalid = True
                log_api_error('permission creation', response.text)
                status_code = response.status_code

        else:
            invalid = True
            status_code = status.HTTP_400_BAD_REQUEST

        context = self.__set_add_permission_context(form, invalid)

        return render(request, self.template, context, status=status_code)

    def __set_add_permission_context(self, form, invalid):
        trusts = self.user.get_permitted_trusts()
        regions = self.user.get_permitted_regions()
        national = Location.get_national_location_id(self.user.auth_token)

        return {
            'session_user': self.user,
            'sub_heading': 'Add role and permission level',
            'form': form,
            'submit_path': 'add_permission',
            'invalid': invalid,
            'trusts': trusts,
            'regions': regions,
            'national': national,
            'managed_user': self.managed_user,
        }

class EditPermissionView(LoginRequiredMixin, PermissionRequiredMixin, ManageUserBaseView):
    permission_required = 'can_update_user_permission'
    template = 'users/permission_editor.html'

    def get(self, request, user_id, permission_id):
        status_code = status.HTTP_200_OK

        permission = Permission.load_by_id(user_id, permission_id, self.user.auth_token)

        context = self.__set_edit_permission_context(permission, False)
        return render(request, self.template, context, status=status_code)

    def post(self, request, user_id):
        post_body = request.POST
        status_code = status.HTTP_200_OK
        invalid = False
        form = PermissionBuilderForm(post_body)
        add_another = True if post_body.get('add_another') == "true" else False

        if form.is_valid():
            response = self.managed_user.add_permission(form, self.user.auth_token)

            if response.ok:
                if add_another:
                    form = PermissionBuilderForm()
                else:
                    return redirect('/settings')
            else:
                invalid = True
                log_api_error('permission creation', response.text)
                status_code = response.status_code

        else:
            invalid = True
            status_code = status.HTTP_400_BAD_REQUEST

        context = self.__set_edit_permission_context(form, invalid)

        return render(request, self.template, context, status=status_code)

    def __set_edit_permission_context(self, permission, invalid):
        trusts = self.user.get_permitted_trusts()
        regions = self.user.get_permitted_regions()
        national = Location.get_national_location_id(self.user.auth_token)

        form = PermissionBuilderForm.load_from_permission(permission, trusts, regions, national)
        return {
            'session_user': self.user,
            'sub_heading': 'Edit role and permission level',
            'form': form,
            'submit_path': 'edit_permission',
            'invalid': invalid,
            'trusts': trusts,
            'regions': regions,
            'national': national,
            'managed_user': self.managed_user,
            'permission': permission,
        }


class DeletePermissionView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'can_delete_user_permission'

    def get(self, request, user_id, permission_id):
        Permission.delete(user_id, permission_id, auth_token=self.user.auth_token)

        return self.__redirect_to_manage_user(user_id)

    def __redirect_to_manage_user(self, user_id):
        return redirect('/users/%s/manage' % user_id)

