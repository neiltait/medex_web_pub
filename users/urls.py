from django.conf.urls import url

from . import views

urlpatterns = [
  url('lookup', views.user_lookup, name='user_lookup'),
  url(r'manage/(?P<user_id>[\w\-]+)', views.manage_user, name='manage_user')
]