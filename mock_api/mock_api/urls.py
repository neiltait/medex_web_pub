from django.urls import path

from .me_offices import get_me_offices_list
from .locations import get_locations_list
from .users import load_by_email


urlpatterns = [
    path('users/find_by_email', load_by_email, name='load_by_email'),
    path('locations/get_locations_list', get_locations_list, name='get_locations_list'),
    path('me_offices/get_me_offices_list', get_me_offices_list, name='get_me_offices_list'),
]
