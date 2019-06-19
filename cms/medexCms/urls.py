from django.conf.urls import url
from django.urls import include, path

from home import views
from home.views import DashboardView, LoginView

urlpatterns = [
  path('', DashboardView.as_view(), name='index'),
  path('login', LoginView.as_view(), name='login'),
  path('login-callback', views.login_callback, name='login_callback'),
  path('logout', views.logout, name='logout'),
  path('settings', views.settings_index, name='settings_index'),
  url(r'^users/', include('users.urls')),
  url(r'^cases/', include('examinations.urls')),
]
