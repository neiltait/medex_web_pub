from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.views.generic.base import View

from rest_framework import status

from errors.utils import log_api_error
from home.utils import render_404
from medexCms.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Location
from locations.forms import LocationEditorForm

class ManageLocationBaseView(View):

    def dispatch(self, request, *args, **kwargs):
        location_id = kwargs.get('location_id')

        print('dispatch')
        print(location_id)

        self.location = None
        self.parent = None

        if location_id != '00000000-0000-0000-0000-000000000000':
            print('location id is not 000')
            self.location = Location.load_by_id(kwargs.get('location_id'), self.user.auth_token)
            if self.location is None:
                return render_404(request, self.user, 'user')

            print('self.location??')
            print(self.location)
            if self.location['parentId'] != None:
                self.parent = Location.load_by_id(self.location['parentId'], self.user.auth_token)

        return super().dispatch(request, *args, **kwargs)


class LocationListView(LoginRequiredMixin, PermissionRequiredMixin, ManageLocationBaseView, View):
    permission_required = 'can_update_location'
    template = 'locations/list.html'

    @never_cache
    def get(self, request, location_id):
        status_code = status.HTTP_200_OK
        locations = Location.get_child_locations_list(location_id, self.user.auth_token)
        context = {
            'session_user': self.user,
            'page_heading': 'Locations',
            'locations': locations,
            'location': self.location,
            'parent': self.parent
        }

        return render(request, self.template, context, status=status_code)



class ManageLocationView(LoginRequiredMixin, PermissionRequiredMixin, ManageLocationBaseView):
    permission_required = 'can_update_location'
    template = 'locations/manage.html'

    def get(self, request, location_id):
        status_code = status.HTTP_200_OK

        context = self.__set_editor_location_context(self.location, False)
        return render(request, self.template, context, status=status_code)

    def post(self, request, location_id):
        post_body = request.POST
        print("post body:")
        print(post_body)
        form = LocationEditorForm(post_body)

        if form.is_valid():
            response = Location.update_location_me_office(form.to_dict(), location_id, self.user.auth_token)

            if response.ok:
                return redirect('/locations/%s/list' % location_id)
            else:
                invalid = True
                if response.status_code == 403:
                    form.is_me_office_error = "You dont have permission to change this location."
                log_api_error('location update', response.text)
                status_code = response.status_code
        else:
            invalid = True
            status_code = status.HTTP_400_BAD_REQUEST

        context = self.__set_editor_location_context(self.location, invalid, posted_form=form)
        return render(request, self.template, context, status=status_code)

    def __set_editor_location_context(self, location, invalid, posted_form=None):

        form = posted_form if posted_form else LocationEditorForm.load_from_location(location)
        return {
            'session_user': self.user,
            'location': self.location,
            'sub_heading': 'Edit location',
            'form': form,
            'submit_path': 'manage_location',
            'invalid': invalid
        }
