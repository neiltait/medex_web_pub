from django.conf.urls import url
from django.urls import include, path

from home.views import DashboardView, LoginView, LogoutView, SettingsIndexView, LoginCallbackView, LoginRefreshView, \
    PrivacyPolicyView, AccessibilityPolicyView, CookiesPolicyView

urlpatterns = [
    path('', DashboardView.as_view(), name='index'),
    path('accessibility', AccessibilityPolicyView.as_view(), name='accessibility'),
    path('cookies', CookiesPolicyView.as_view(), name='cookies'),
    path('login', LoginView.as_view(), name='login'),
    path('login-callback', LoginCallbackView.as_view(), name='login_callback'),
    path('login-refresh', LoginRefreshView.as_view(), name='login_refresh'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('privacy', PrivacyPolicyView.as_view(), name='privacy'),
    path('settings', SettingsIndexView.as_view(), name='settings_index'),
    url(r'^users/', include('users.urls')),
    url(r'^locations/', include('locations.urls')),
    url(r'^cases/', include('examinations.urls')),
]
