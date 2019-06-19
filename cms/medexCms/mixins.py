from django.core.exceptions import ImproperlyConfigured

from errors.utils import log_unexpected_method
from errors.views import handle_method_not_allowed_error, handle_not_permitted_error, handle_no_role_error
from home.utils import redirect_to_login, redirect_to_landing
from users.models import User


class LoginRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        self.user = User.initialise_with_token(request)
        if not self.user.check_logged_in():
            return redirect_to_login()

        if self.user.roles is None:
            return handle_no_role_error(request, self.user)
        return super().dispatch(request, *args, **kwargs)

    def http_method_not_allowed(self, request, *args, **kwargs):
        log_unexpected_method(request.method, request.path)
        return handle_method_not_allowed_error(request, self.user)


class PermissionRequiredMixin:
    """Verify that the current user has all specified permissions."""
    permission_required = None

    def get_permission_required(self):
        """
        Override this method to override the permission_required attribute.
        Must return an iterable.
        """
        if self.permission_required is None:
            raise ImproperlyConfigured(
                '{0} is missing the permission_required attribute. Define {0}.permission_required, or override '
                '{0}.get_permission_required().'.format(self.__class__.__name__)
            )
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms

    def has_permission(self):
        """
        Override this method to customize the way permissions are checked.
        """
        perms = self.get_permission_required()
        for perm in perms:
            if not getattr(self.user.permitted_actions, perm, False):
                return False
        return True

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission(request)
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self, request):
        return handle_not_permitted_error(request, self.user)


class LoggedInMixin:

    def dispatch(self, request, *args, **kwargs):
        user = User.initialise_with_token(request)
        if user.check_logged_in():
            return redirect_to_landing()
        return super().dispatch(request, *args, **kwargs)

    def http_method_not_allowed(self, request, *args, **kwargs):
        log_unexpected_method(request.method, request.path)
        return handle_method_not_allowed_error(request, self.user)
