from django.conf.urls import url

from . import views

urlpatterns = [
  url('create', views.create_examination, name='create_examination'),
  url(r'(?P<examination_id>[\w\-]+)', views.edit_examination, name='edit_examination'),
]