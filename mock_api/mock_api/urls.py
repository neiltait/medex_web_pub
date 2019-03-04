from django.conf.urls import url
from django.urls import path

from . import locations, users

urlpatterns = [
    path('create-session', users.create_session, name='create_session'),
    path('users/validate-session', users.validate_session, name='validate_session'),
    path('users', users.users, name='users_path'),
    path('users/find_by_email', users.load_by_email, name='load_by_email'),
    url(r'users/(?P<user_id>[\w\-]+)', users.load_by_id, name='load_by_id'),
    path('locations/load_trusts_list', locations.load_trust_list, name='load_trust_list'),
]
