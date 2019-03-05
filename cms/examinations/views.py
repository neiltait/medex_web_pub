from django.shortcuts import render
from examinations import request_handler
from home.utils import redirect_to_login
from users.models import User

from .forms import PrimaryExaminationInformationForm


def create_examination(request):
    form = PrimaryExaminationInformationForm()

    user = User.initialise_with_token(request)

    if not user.check_logged_in():
        return redirect_to_login()

    if request.method == 'POST':
        form = PrimaryExaminationInformationForm(request.POST)
        if form.is_valid():
            print(form)
        else:
            print("not valid")

    return render_create_examination_form(request, user)


def post_create_examination_form(request, user):
    if validate_post_create_examination(request):
        return post_create_examination_form(request)

    else:
        pass


def validate_post_create_examination(request):
    form = PrimaryExaminationInformationForm(request=request.POST)
    form.is_valid()
    pass


def post_new_examination(request):
    pass


def render_create_examination_form(request, user):
    locations = request_handler.get_locations_list()
    me_offices = request_handler.get_me_offices_list()

    context = {
        "session_user": user,
        "page_heading": "Add a new case",
        "sub_heading": "Primary information",
        "locations": locations,
        "me_offices": me_offices,
        "form": PrimaryExaminationInformationForm(),
    }
    alerts = []

    return render(request, "examinations/create.html", context)
