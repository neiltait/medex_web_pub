import json

from django.shortcuts import render

import alerts
from alerts import messages
from alerts.utils import generate_error_alert
from examinations import request_handler
from home.utils import redirect_to_login, redirect_to_landing
from users.models import User
from rest_framework import status

from examinations.forms import PrimaryExaminationInformationForm


def create_examination(request):

    user = User.initialise_with_token(request)

    if not user.check_logged_in():
        return redirect_to_login()

    alerts = []
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
            alerts.append(generate_error_alert(messages.ERROR_IN_FORM))
            status_code = status.HTTP_400_BAD_REQUEST

    return render_create_examination_form(request, user, alerts, status_code)


def render_create_examination_form(request, user, alerts = [], status_code = status.HTTP_200_OK):
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
    }

    return render(request, "examinations/create.html", context, status=status_code)
