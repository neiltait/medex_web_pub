from django.conf.urls import url
from django.urls import include, path

from home.views import DashboardView, LoginView, LogoutView, SettingsIndexView, LoginCallbackView

urlpatterns = [
  path('', DashboardView.as_view(), name='index'),
  path('login', LoginView.as_view(), name='login'),
  path('login-callback', LoginCallbackView.as_view(), name='login_callback'),
  path('logout', LogoutView.as_view(), name='logout'),
  path('settings', SettingsIndexView.as_view(), name='settings_index'),
  url(r'^users/', include('users.urls')),
  url(r'^cases/', include('examinations.urls')),
]
