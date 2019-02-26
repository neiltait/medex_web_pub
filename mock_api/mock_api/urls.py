from django.urls import path

from .users import load_by_email

urlpatterns = [
    path('users/find_by_email', load_by_email, name='load_by_email'),
]
