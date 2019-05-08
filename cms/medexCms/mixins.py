from errors.utils import log_unexpected_method
from errors.views import handle_method_not_allowed_error
from home.utils import redirect_to_login
from users.models import User


class LoginRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        self.user = User.initialise_with_token(request)
        if not self.user.check_logged_in():
            return redirect_to_login()
        return super().dispatch(request, *args, **kwargs)

    def http_method_not_allowed(self, request, *args, **kwargs):
        log_unexpected_method(request.method, request.path)
        return handle_method_not_allowed_error(request, self.user)
