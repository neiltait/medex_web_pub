from django.shortcuts import render, redirect
from rest_framework import status

from alerts import messages
from alerts.utils import generate_error_alert
from examinations import request_handler
from examinations.forms import PrimaryExaminationInformationForm, SecondaryExaminationInformationForm, \
    BereavedInformationForm, UrgencyInformationForm, MedicalTeamMembersForm, MedicalTeamAssignedTeamForm
from home.utils import redirect_to_login, redirect_to_landing
from locations import request_handler as location_request_handler
from people import request_handler as people_request_handler
from users.models import User


def create_examination(request):
    user = User.initialise_with_token(request)

    if not user.check_logged_in():
        return redirect_to_login()

    alerts = []
    errors = {"count": 0}
    status_code = status.HTTP_200_OK
    form = None

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

    return render_create_examination_form(request, user, alerts, errors, status_code, form)


def render_create_examination_form(request, user, alerts=[], errors=None, status_code=status.HTTP_200_OK, form=None):
    locations = location_request_handler.get_locations_list()
    me_offices = location_request_handler.get_me_offices_list()

    context = {
        "session_user": user,
        "page_heading": "Add a new case",
        "sub_heading": "Primary information",
        "locations": locations,
        "me_offices": me_offices,
        "form": form if form else PrimaryExaminationInformationForm(),
        "alerts": alerts,
        "errors": errors,
    }

    return render(request, "examinations/create.html", context, status=status_code)


def edit_examination(request, examination_id):
    return redirect('/cases/' + examination_id + '/patient-details')


def edit_examination_patient_details(request, examination_id):
    user = User.initialise_with_token(request)

    if not user.check_logged_in():
        return redirect_to_login()

    status_code = status.HTTP_200_OK
    error_count = 0
    primary_info_form = None
    secondary_info_form = None
    bereaved_info_form = None
    urgency_info_form = None

    if request.method == 'POST':
        primary_info_form = PrimaryExaminationInformationForm(request.POST)
        secondary_info_form = SecondaryExaminationInformationForm(request.POST)
        bereaved_info_form = BereavedInformationForm(request.POST)
        urgency_info_form = UrgencyInformationForm(request.POST)

        forms_valid = validate_patient_details_forms(primary_info_form, secondary_info_form, bereaved_info_form, urgency_info_form)
        if forms_valid:
            print('forms valid')
        else:
            error_count = primary_info_form.errors['count'] + secondary_info_form.errors['count'] + \
                          bereaved_info_form.errors['count'] + urgency_info_form.errors['count']
            status_code = status.HTTP_400_BAD_REQUEST

    modal_config = get_tab_change_modal_config()

    locations = location_request_handler.get_locations_list()
    me_offices = location_request_handler.get_me_offices_list()

    context = {
        'session_user': user,
        'examination_id': examination_id,
        'primary_info_form': primary_info_form,
        'secondary_info_form': secondary_info_form,
        'bereaved_info_form': bereaved_info_form,
        'urgency_info_form': urgency_info_form,
        'error_count': error_count,
        'tab_modal': modal_config,
        "locations": locations,
        "me_offices": me_offices,
    }

    return render(request, 'examinations/edit_patient_details.html', context, status=status_code)


def edit_examination_medical_team(request, examination_id):
    user = User.initialise_with_token(request)

    if not user.check_logged_in():
        return redirect_to_login()

    medical_examiners = people_request_handler.get_medical_examiners_list()
    medical_examiners_officers = people_request_handler.get_medical_examiners_officers_list()
    status_code = status.HTTP_200_OK
    error_count = 0
    medical_team_members_form = None
    medical_team_assigned_team_form = None

    if request.method == 'POST':
        medical_team_members_form = MedicalTeamMembersForm(request.POST)
        medical_team_assigned_team_form = MedicalTeamAssignedTeamForm(request.POST)

        forms_valid = medical_team_members_form.is_valid()
        if forms_valid:
            print('forms valid')
        else:
            error_count = medical_team_members_form.errors['count']
            status_code = status.HTTP_400_BAD_REQUEST

    modal_config = get_tab_change_modal_config()

    context = {
        'session_user': user,
        'examination_id': examination_id,
        'medical_team_form': medical_team_members_form,
        'medical_team_assigned_form': medical_team_assigned_team_form,
        'medical_examiners': medical_examiners,
        'medical_examiners_officers': medical_examiners_officers,
        'error_count': error_count,
        'tab_modal': modal_config,
    }

    return render(request, 'examinations/edit_medical_team.html', context, status=status_code)


def validate_patient_details_forms(primary_info_form, secondary_info_form, bereaved_info_form, urgency_info_form):
    primary_valid = primary_info_form.is_valid()
    secondary_valid = secondary_info_form.is_valid()
    bereaved_valid = bereaved_info_form.is_valid()
    urgency_valid = urgency_info_form.is_valid()

    return primary_valid and secondary_valid and bereaved_valid and urgency_valid


def get_tab_change_modal_config():
    return {
        'id': 'tab-change-modal',
        'content': 'You have unsaved changes, do you want to save them before continuing?',
        'confirm_btn_id': 'save-continue',
        'confirm_btn_text': 'Save and continue',
        'extra_buttons': [
            {
                'id': 'discard',
                'text': 'Discard and continue',
            }
        ],
    }
