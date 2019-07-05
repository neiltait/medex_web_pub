from django.conf.urls import url

from permissions.views import AddPermissionView, DeletePermissionView, EditPermissionView
from users.views import CreateUserView, UserListView, ManageUserView

urlpatterns = [
    url(r'new', CreateUserView.as_view(), name='create_user'),
    url(r'(?P<user_id>[\w\-]+)/manage', ManageUserView.as_view(), name='manage_user'),
    url(r'(?P<user_id>[\w\-]+)/add_permission', AddPermissionView.as_view(), name='add_permission'),
    url(r'(?P<user_id>[\w\-]+)/edit_permission/(?P<permission_id>[\w\-]+)', EditPermissionView.as_view(),
        name="edit_permission"),
    url(r'(?P<user_id>[\w\-]+)/delete_permission/(?P<permission_id>[\w\-]+)', DeletePermissionView.as_view(),
        name='delete_permission'),
    url(r'', UserListView.as_view(), name='user_list')
]
