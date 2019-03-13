from django.conf.urls import url
from django.urls import path

from .me_offices import get_me_offices_list
from .locations import get_locations_list
from .users import load_by_email
from .examinations import create_case
from .medical_examiners import get_medical_examiners_list
from .medical_examiners_officers import get_medical_examiners_officers_list

from . import locations, users

urlpatterns = [
    path('create-session', users.create_session, name='create_session'),
    path('users/validate-session', users.validate_session, name='validate_session'),
    path('users', users.users, name='users_path'),
    path('users/find_by_email', users.load_by_email, name='load_by_email'),
    url(r'users/(?P<user_id>[\w\-]+)/permissions', users.permissions, name='permissions_path'),
    url(r'users/(?P<user_id>[\w\-]+)', users.load_by_id, name='load_by_id'),
    path('locations/load_trusts_list', locations.load_trust_list, name='load_trust_list'),
    path('locations/load_regions_list', locations.load_regions_list, name='load_regions_list'),
    path('users/find_by_email', load_by_email, name='load_by_email'),
    path('locations/get_locations_list', get_locations_list, name='get_locations_list'),
    path('me_offices/get_me_offices_list', get_me_offices_list, name='get_me_offices_list'),
    path('cases/create', create_case, name='create_case'),
    path('people/get_medical_examiners_list', get_medical_examiners_list, name='medical_examiners_list'),
    path('people/get_medical_examiners_officers_list', get_medical_examiners_officers_list, name='medical_examiners_officers_list'),
]
