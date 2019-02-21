from django.conf.urls import url

from . import views

urlpatterns = [
  url('create', views.create_examination, name='create_examination'),
]