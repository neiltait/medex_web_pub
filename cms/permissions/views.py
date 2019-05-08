from rest_framework import status
from django.shortcuts import render, redirect

from errors.utils import log_api_error
from medexCms.mixins import LoginRequiredMixin
from medexCms.views import MedExBaseView
from permissions.forms import PermissionBuilderForm
from users.views import ManageUserBaseView


class AddPermissionView(LoginRequiredMixin, ManageUserBaseView):
    template = 'users/permission_builder.html'

    def get(self, request):
        status_code = status.HTTP_200_OK

        context = self.__set_add_permission_context(PermissionBuilderForm(), False)
        return render(request, self.template, context, status=status_code)

    def post(self, request):
        post_body = request.POST
        form = PermissionBuilderForm(post_body)
        add_another = True if post_body.get('add_another') == "true" else False

        if form.is_valid():
            response = self.managed_user.add_permission(form, self.user.auth_token)

            if response.ok:
                if add_another:
                    return redirect('add_permission', user_id=self.managed_user.user_id)
                else:
                    return redirect('/settings')
            else:
                log_api_error('permission creation', response.text)
                status_code = response.status_code

        else:
            status_code = status.HTTP_400_BAD_REQUEST

        context = self.__set_add_permission_context(form, True)

        return render(request, self.template, context, status=status_code)

    def __set_add_permission_context(self, form, invalid):
        trusts = self.user.get_permitted_trusts()
        regions = self.user.get_permitted_regions()

        return {
            'session_user': self.user,
            'sub_heading': 'Add role and permission level',
            'form': form,
            'submit_path': 'add_permission',
            'invalid': invalid,
            'trusts': trusts,
            'regions': regions,
            'managed_user': self.managed_user,
        }
