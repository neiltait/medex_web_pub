from django.conf.urls import url

from . import views

urlpatterns = [
  url('lookup', views.user_lookup, name='user_lookup'),
]