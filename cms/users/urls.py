from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'new', views.create_user, name='create_user'),
  url(r'lookup', views.lookup_user, name='lookup_user')
]