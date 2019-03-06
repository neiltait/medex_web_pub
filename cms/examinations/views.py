from alerts import messages
from alerts.utils import generate_error_alert
from django.shortcuts import render
from examinations import request_handler
from examinations.forms import PrimaryExaminationInformationForm
from home.utils import redirect_to_login, redirect_to_landing
from rest_framework import status
from users.models import User


def create_examination(request):
    user = User.initialise_with_token(request)

    if not user.check_logged_in():
        return redirect_to_login()

    alerts = []
    errors = {"count": 0}
    status_code = status.HTTP_200_OK

    if request.method == 'POST':
        form = PrimaryExaminationInformationForm(request.POST)
        if form.is_valid():
            response = request_handler.post_new_examination(form.to_object())
            if response.status_code == status.HTTP_200_OK:
                return redirect_to_landing()
            else:
                alerts.append(generate_error_alert(messages.ERROR_IN_FORM))
                status_code = response.status_code
        else:
            errors = form.errors
            alerts.append(generate_error_alert(messages.ERROR_IN_FORM))
            status_code = status.HTTP_400_BAD_REQUEST

    return render_create_examination_form(request, user, alerts, errors, status_code)


def render_create_examination_form(request, user, alerts=[], errors=None, status_code=status.HTTP_200_OK):
    locations = request_handler.get_locations_list()
    me_offices = request_handler.get_me_offices_list()

    context = {
        "session_user": user,
        "page_heading": "Add a new case",
        "sub_heading": "Primary information",
        "locations": locations,
        "me_offices": me_offices,
        "form": PrimaryExaminationInformationForm(),
        "alerts": alerts,
        "errors": errors,
    }

    return render(request, "examinations/create.html", context, status=status_code)
