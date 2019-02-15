from django.conf.urls import url
from django.urls import include, path

from home import views

urlpatterns = [
  path('', views.index, name='index'),
  path('login', views.login, name='login'),
  path('logout', views.logout, name='logout'),
  path('forgotten-password', views.forgotten_password, name='forgotten-password'),
  path('forgotten-userid', views.forgotten_userid, name='forgotten-userid'),
  url(r'^users/', include('users.urls')),
]
