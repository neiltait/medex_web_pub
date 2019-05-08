from django.conf.urls import url

from users.views import CreateUserView
from . import views

urlpatterns = [
  url(r'new', CreateUserView.as_view(), name='create_user'),
  url(r'(?P<user_id>[\w\-]+)/add_permission', views.add_permission, name='add_permission')
]