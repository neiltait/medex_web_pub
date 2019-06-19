from django.conf.urls import url

from permissions.views import AddPermissionView
from users.views import CreateUserView, UserListView

urlpatterns = [
  url(r'new', CreateUserView.as_view(), name='create_user'),
  url(r'(?P<user_id>[\w\-]+)/add_permission', AddPermissionView.as_view(), name='add_permission'),
  url(r'', UserListView.as_view(), name='user_list')
]