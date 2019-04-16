from django.shortcuts import render, redirect
from rest_framework import status

from alerts import messages
from alerts.utils import generate_error_alert
from examinations import request_handler
from examinations.forms import PrimaryExaminationInformationForm, SecondaryExaminationInformationForm, \
    BereavedInformationForm, UrgencyInformationForm, MedicalTeamMembersForm, PreScrutinyEventForm, OtherEventForm, \
    AdmissionNotesEventForm, MeoSummaryEventForm
from examinations.models import PatientDetails, CaseBreakdown, MedicalTeam, CaseOutcome
from home.utils import redirect_to_login, render_404, redirect_to_examination
from examinations.utils import event_form_parser, event_form_submitter, get_tab_change_modal_config
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
                    examination_id = response.json()['examinationId']
                    return redirect_to_examination(examination_id)
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
        examination = PatientDetails().set_primary_info_values(primary_info_form) \
            .set_secondary_info_values(secondary_info_form).set_bereaved_info_values(bereaved_info_form) \
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
    # TODO add 404 check (currently not possible from medical_team endpoint

    if request.method == 'POST':
        # attempt to post and get return form
        medical_team_members_form, status_code, errors = __post_medical_team_form(request, examination_id,
                                                                                  user.auth_token)
    else:
        # the GET medical team form
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
    medical_examiners = people_request_handler.get_medical_examiners_list_for_examination(user.auth_token,
                                                                                          examination_id)
    medical_examiners_officers = people_request_handler.get_medical_examiners_officers_list_for_examination(
        user.auth_token, examination_id)
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


def edit_examination_case_breakdown(request, examination_id):
    user = User.initialise_with_token(request)
    status_code = status.HTTP_200_OK

    if not user.check_logged_in():
        return redirect_to_login()

    examination = CaseBreakdown.load_by_id(user.auth_token, examination_id)
    form = None

    if request.method == 'POST':
        form, status_code, errors = __post_case_breakdown_event(request, user, examination_id)

    if not type(examination) == CaseBreakdown:
        context = {
            'session_user': user,
            'error': examination,
        }

        return render(request, 'errors/base_error.html', context, status=examination.status_code)

    forms = user.get_forms_for_role()

    form_data = __prepare_forms(examination.event_list, form)

    patient = {
        "name": examination.patient_name,
        "nhs_number": examination.nhs_number
    }

    context = {
        'session_user': user,
        'examination_id': examination_id,
        'forms': forms,
        # 'qap_form': examination.qap_discussion,
        'case_breakdown': examination,
        'patient': patient,
        'form_data': form_data
    }

    return render(request, 'examinations/edit_case_breakdown.html', context, status=status_code)


def __post_case_breakdown_event(request, user, examination_id):
    form = event_form_parser(request.POST)
    if form.is_valid():
        response = event_form_submitter(user.auth_token, examination_id, form)
        status_code = response.status_code
        errors = {'count': 0}
    else:
        errors = form.errors
        status_code = status.HTTP_400_BAD_REQUEST
    return form, status_code, errors


def __prepare_forms(event_list, form):
    pre_scrutiny_form = PreScrutinyEventForm()
    other_notes_form = OtherEventForm()
    admission_notes_form = AdmissionNotesEventForm()
    meo_summary_form = MeoSummaryEventForm()

    if event_list.get_me_scrutiny_draft():
        pre_scrutiny_form.fill_from_draft(event_list.get_me_scrutiny_draft())
    if event_list.get_other_notes_draft():
        other_notes_form.fill_from_draft(event_list.get_other_notes_draft())
    if event_list.get_latest_admission_draft():
        admission_notes_form.fill_from_draft(event_list.get_latest_admission_draft())
    if event_list.get_meo_summary_draft():
        meo_summary_form.fill_from_draft(event_list.get_meo_summary_draft())

    form_data = {
        'PreScrutinyEventForm': pre_scrutiny_form,
        'OtherEventForm': other_notes_form,
        'AdmissionNotesEventForm': admission_notes_form,
        'MeoSummaryEventForm': meo_summary_form
    }

    if form:
        form_data[type(form).__name__] = form.make_active()

    return form_data


def view_examination_case_outcome(request, examination_id):
    status_code = status.HTTP_200_OK

    user = User.initialise_with_token(request)

    if not user.check_logged_in():
        return redirect_to_login()

    if request.method == 'POST':
        if 'pre-scrutiny-confirmed' in request.POST:
            result = CaseOutcome.complete_scrutiny(user.auth_token, examination_id)

            if not result == status.HTTP_200_OK:
                context = {
                    'session_user': user,
                    'error': result,
                }

                return render(request, 'errors/base_error.html', context, status=result.status_code)

    case_outcome = CaseOutcome.load_by_id(user.auth_token, examination_id)

    if not type(case_outcome) == CaseOutcome:
        context = {
            'session_user': user,
            'error': case_outcome,
        }

        return render(request, 'errors/base_error.html', context, status=case_outcome.status_code)

    modal_config = get_tab_change_modal_config()

    context = {
        'session_user': user,
        'examination_id': examination_id,
        'case_outcome': case_outcome,
        'patient': case_outcome.case_header,
        'tab_modal': modal_config,
    }

    return render(request, 'examinations/case_outcome.html', context, status=status_code)
