from django.conf.urls import url

from locations.views import LocationListView, ManageLocationView

urlpatterns = [
    url(r'(?P<location_id>[\w\-]+)/manage', ManageLocationView.as_view(), name='manage_location'),
    url(r'(?P<location_id>[\w\-]+)/list', LocationListView.as_view(), name='location_list'),
    url(r'list', LocationListView.as_view(), { 'location_id' : '00000000-0000-0000-0000-000000000000'}, name='location_list')
]
