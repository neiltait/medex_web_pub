from django.shortcuts import render

from .forms import PrimaryExaminationInformationForm

from home.utils import redirect_to_login

from users.models import User


def create_examination(request):
    user = User.initialise_with_token(request)

    if not user.check_logged_in():
        return redirect_to_login()


    context = {
        'session_user': user,
        'page_heading': 'Add a new case',
        'sub_heading': 'Primary information',
        'form': PrimaryExaminationInformationForm()
    }
    alerts = []

    return render(request, 'examinations/create.html', context)


def edit_examination(request, examination_id):
    user = User.initialise_with_token(request)

    if not user.check_logged_in():
        return redirect_to_login()

    context = {
        'session_user': user,
        'examination_id': examination_id
    }

    return render(request, 'examinations/edit.html', context)
