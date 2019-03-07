from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'new', views.create_user, name='create_user'),
  url(r'(?P<user_id>[\w\-]+)/add_permission', views.add_permission, name='add_permission')
]