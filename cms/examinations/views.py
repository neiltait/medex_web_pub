from django.shortcuts import render, redirect
from rest_framework import status

from alerts import messages
from alerts.utils import generate_error_alert
from errors.models import NotFoundError
from examinations import request_handler
from examinations.forms import PrimaryExaminationInformationForm, SecondaryExaminationInformationForm, \
    BereavedInformationForm, UrgencyInformationForm, MedicalTeamMembersForm
from examinations.models import Examination, PatientDetails, CaseBreakdown, MedicalTeam
from home.utils import redirect_to_login, redirect_to_landing, render_404
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

    if request.POST:
        form = PrimaryExaminationInformationForm(request.POST)
        if form.is_valid():
            response = request_handler.post_new_examination(form.to_object(), user.auth_token)
            if response.status_code == status.HTTP_200_OK:
                if 'create-and-continue' in request.POST:
                    return redirect_to_landing()
                else:
                    form = None
                    status_code = status.HTTP_200_OK
            else:
                alerts.append(generate_error_alert(messages.ERROR_IN_FORM))
                status_code = response.status_code
        else:
            errors = form.errors
            alerts.append(generate_error_alert(messages.ERROR_IN_FORM))
            status_code = status.HTTP_400_BAD_REQUEST

    return render_create_examination_form(request, user, alerts, errors, status_code, form)


def render_create_examination_form(request, user, alerts=[], errors=None, status_code=status.HTTP_200_OK, form=None):
    locations = location_request_handler.get_locations_list(user.auth_token)
    me_offices = location_request_handler.get_me_offices_list(user.auth_token)

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

    if request.method == 'GET':
        examination = PatientDetails.load_by_id(examination_id, user.auth_token)
        if not examination:
            return render_404(request, user, 'case')

        primary_info_form = PrimaryExaminationInformationForm().set_values_from_instance(examination)
        secondary_info_form = SecondaryExaminationInformationForm().set_values_from_instance(examination)
        bereaved_info_form = BereavedInformationForm().set_values_from_instance(examination)
        urgency_info_form = UrgencyInformationForm().set_values_from_instance(examination)

    elif request.method == 'POST':

        primary_info_form = PrimaryExaminationInformationForm(request.POST)
        secondary_info_form = SecondaryExaminationInformationForm(request.POST)
        bereaved_info_form = BereavedInformationForm(request.POST)
        urgency_info_form = UrgencyInformationForm(request.POST)
        examination = PatientDetails().set_primary_info_values(primary_info_form)\
            .set_secondary_info_values(secondary_info_form).set_bereaved_info_values(bereaved_info_form)\
            .set_urgency_info_values(urgency_info_form)

        forms_valid = validate_patient_details_forms(primary_info_form, secondary_info_form, bereaved_info_form,
                                                     urgency_info_form)
        if forms_valid:
            submission = primary_info_form.to_object()
            submission.update(secondary_info_form.for_request())
            submission.update(bereaved_info_form.for_request())
            submission.update(urgency_info_form.for_request())
            submission['id'] = examination_id

            response = PatientDetails.update(examination_id, submission, user.auth_token)

            if response.status_code == status.HTTP_200_OK and request.GET.get('nextTab'):
                return redirect('/cases/%s/%s' % (examination_id, request.GET.get('nextTab')))
            elif response.status_code != status.HTTP_200_OK:
                status_code = response.status_code
        else:
            error_count = primary_info_form.errors['count'] + secondary_info_form.errors['count'] + \
                          bereaved_info_form.errors['count'] + urgency_info_form.errors['count']
            status_code = status.HTTP_400_BAD_REQUEST

    modal_config = get_tab_change_modal_config()

    locations = location_request_handler.get_locations_list(user.auth_token)
    me_offices = location_request_handler.get_me_offices_list(user.auth_token)

    patient = {
        "name": examination.full_name(),
        "nhs_number": examination.get_nhs_number()
    }

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
        "patient": patient
    }

    return render(request, 'examinations/edit_patient_details.html', context, status=status_code)


def edit_examination_medical_team(request, examination_id):
    # get the current user
    user = User.initialise_with_token(request)
    if not user.check_logged_in():
        return redirect_to_login()

    # check the examination exists
    examination = Examination.load_by_id(examination_id, user.auth_token)
    if not examination:
        return render_404(request, user, 'case')

    if request.method == 'POST':
        # attempt to post and get return form
        medical_team_members_form, status_code, errors = __post_medical_team_form(request, examination_id,
                                                                                  user.auth_token)
    else:
        # get a simple form
        medical_team = MedicalTeam.load_by_id(examination_id, user.auth_token)
        medical_team_members_form, status_code, errors = __get_medical_team_form(medical_team=medical_team)

    # render the tab
    return __render_medical_team_tab(errors, examination_id, medical_team_members_form, request, status_code, user)


def __get_medical_team_form(medical_team=None):
    if medical_team:
        medical_team_members_form = MedicalTeamMembersForm(medical_team=medical_team)
    else:
        medical_team_members_form = MedicalTeamMembersForm()

    status_code = status.HTTP_200_OK
    errors = {'count': 0}
    return medical_team_members_form, status_code, errors


def __post_medical_team_form(request, examination_id, auth_token):
    medical_team_members_form = MedicalTeamMembersForm(request.POST)
    forms_valid = medical_team_members_form.is_valid()
    if forms_valid:
        response = request_handler.update_medical_team(examination_id, medical_team_members_form.to_object(),
                                                       auth_token)
        status_code = response.status_code
        errors = {'count': 0}
    else:
        errors = medical_team_members_form.errors
        status_code = status.HTTP_400_BAD_REQUEST
    return medical_team_members_form, status_code, errors


def __render_medical_team_tab(errors, examination_id, medical_team_members_form, request, status_code, user):
    medical_examiners = people_request_handler.get_medical_examiners_list(user.auth_token)
    medical_examiners_officers = people_request_handler.get_medical_examiners_officers_list(user.auth_token)
    modal_config = get_tab_change_modal_config()
    context = {
        'session_user': user,
        'examination_id': examination_id,
        'form': medical_team_members_form,
        'medical_examiners': medical_examiners,
        'medical_examiners_officers': medical_examiners_officers,
        'error_count': errors['count'],
        'errors': errors,
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


def edit_examination_case_breakdown(request, examination_id):
    user = User.initialise_with_token(request)

    if not user.check_logged_in():
        return redirect_to_login()

    examination = CaseBreakdown.load_by_id(user.auth_token, examination_id)

    if not examination:
        context = {
            'session_user': user,
            'error': NotFoundError('case'),
        }

        return render(request, 'errors/base_error.html', context, status=status.HTTP_404_NOT_FOUND)

    status_code = status.HTTP_200_OK

    forms = user.get_forms_for_role()

    patient = {
        "name": examination.patient_name,
        "nhs_number": examination.nhs_number
    }

    context = {
        'session_user': user,
        'examination_id': examination_id,
        'forms': forms,
        'qap_form': examination.qap_discussion,
        'latest_admission_form': examination.latest_admission,
        'case_breakdown': examination,
        'patient': patient
    }

    return render(request, 'examinations/edit_case_breakdown.html', context, status=status_code)
