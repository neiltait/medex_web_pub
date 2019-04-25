from django.shortcuts import render, redirect
from rest_framework import status

from errors.models import GenericError, BadRequestResponse, MethodNotAllowedError
from errors.utils import log_unexpected_method
from errors.views import __handle_method_not_allowed_error
from examinations import request_handler
from examinations.forms import PrimaryExaminationInformationForm, SecondaryExaminationInformationForm, \
    BereavedInformationForm, UrgencyInformationForm, MedicalTeamMembersForm, PreScrutinyEventForm, OtherEventForm, \
    AdmissionNotesEventForm, MeoSummaryEventForm, QapDiscussionEventForm
from examinations.models import PatientDetails, CaseBreakdown, MedicalTeam, CaseOutcome, Examination
from home.utils import redirect_to_login, render_404, redirect_to_examination
from examinations.utils import event_form_parser, event_form_submitter, get_tab_change_modal_config
from locations.models import Location
from people import request_handler as people_request_handler
from users.models import User


def create_examination(request):
    user = User.initialise_with_token(request)
    if not user.check_logged_in():
        return redirect_to_login()

    if request.method == 'GET':
        template, context, status_code = __get_create_examination(user)

    elif request.POST:
        template, context, status_code, redirect_response = __post_create_examination(user, request.POST)
        if redirect_response:
            return redirect_response

    else:
        log_unexpected_method(request.method, 'create examination')
        template, context, status_code = __handle_method_not_allowed_error(user)

    return render(request, template, context, status=status_code)


def __get_create_examination(user):
    template = "examinations/create.html"
    status_code = status.HTTP_200_OK
    context = __set_create_examination_context(user, PrimaryExaminationInformationForm(), False)
    return template, context, status_code


def __post_create_examination(user, post_body):
    template = "examinations/create.html"
    add_another = False
    form = PrimaryExaminationInformationForm(post_body)
    if form.is_valid():
        response = Examination.create(form.to_object(), user.auth_token)
        if response.ok:
            if form.CREATE_AND_CONTINUE_FLAG in post_body:
                examination_id = response.json()['examinationId']
                return None, None, None, redirect_to_examination(examination_id)
            else:
                add_another = True
                form = PrimaryExaminationInformationForm()
                status_code = status.HTTP_200_OK
        else:
            status_code = response.status_code
    else:
        status_code = status.HTTP_400_BAD_REQUEST
    context = __set_create_examination_context(user, form, add_another)
    return template, context, status_code, None


def __set_create_examination_context(user, form, add_another):
    locations = Location.get_locations_list(user.auth_token)
    me_offices = Location.get_me_offices_list(user.auth_token)

    return {
        "session_user": user,
        "page_heading": "Add a new case",
        "sub_heading": "Primary information",
        "locations": locations,
        "me_offices": me_offices,
        "form": form,
        "errors": form.errors,
        "add_another": add_another
    }


def edit_examination(request, examination_id):
    return redirect('/cases/' + examination_id + '/patient-details')


def examination_patient_details(request, examination_id):
    user = User.initialise_with_token(request)

    if not user.check_logged_in():
        return redirect_to_login()

    examination = PatientDetails.load_by_id(examination_id, user.auth_token)
    if not examination:
        return render_404(request, user, 'case')

    if request.method == 'GET':
        template, context, status_code = __get_examination_patient_details(user, examination)

    elif request.method == 'POST':
        template, context, status_code, redirect_response = __post_examination_patient_details(user, request.POST,
                                                                                               examination, request.GET)

        if redirect_response:
            return redirect_response

    else:

        log_unexpected_method(request.method, 'create examination')

        template, context, status_code = __handle_method_not_allowed_error(user)

    return render(request, template, context, status=status_code)


def __get_examination_patient_details(user, examination):
    template = 'examinations/edit_patient_details.html'
    status_code = status.HTTP_200_OK

    primary_info_form = PrimaryExaminationInformationForm().set_values_from_instance(examination)
    secondary_info_form = SecondaryExaminationInformationForm().set_values_from_instance(examination)
    bereaved_info_form = BereavedInformationForm().set_values_from_instance(examination)
    urgency_info_form = UrgencyInformationForm().set_values_from_instance(examination)

    context = __set_examination_patient_details_context(user, examination, primary_info_form, secondary_info_form,
                                                        bereaved_info_form, urgency_info_form, False)
    return template, context, status_code


def __post_examination_patient_details(user, post_body, examination, get_body):
    template = 'examinations/edit_patient_details.html'
    saved = False
    status_code = status.HTTP_200_OK

    primary_info_form = PrimaryExaminationInformationForm(post_body)
    secondary_info_form = SecondaryExaminationInformationForm(post_body)
    bereaved_info_form = BereavedInformationForm(post_body)
    urgency_info_form = UrgencyInformationForm(post_body)
    examination.set_primary_info_values(primary_info_form).set_secondary_info_values(secondary_info_form) \
        .set_bereaved_info_values(bereaved_info_form).set_urgency_info_values(urgency_info_form)

    forms_valid = validate_patient_details_forms(primary_info_form, secondary_info_form, bereaved_info_form,
                                                 urgency_info_form)
    if forms_valid:
        submission = primary_info_form.to_object()
        submission.update(secondary_info_form.for_request())
        submission.update(bereaved_info_form.for_request())
        submission.update(urgency_info_form.for_request())
        submission['id'] = examination.examination_id

        response = PatientDetails.update(examination.examination_id, submission, user.auth_token)

        if response.status_code == status.HTTP_200_OK and get_body.get('nextTab'):
            return None, None, None, redirect('/cases/%s/%s' % (examination.examination_id, get_body.get('nextTab')))
        elif response.status_code != status.HTTP_200_OK:
            status_code = response.status_code
        else:
            saved = True
    else:
        status_code = status.HTTP_400_BAD_REQUEST

    context = __set_examination_patient_details_context(user, examination, primary_info_form, secondary_info_form,
                                                        bereaved_info_form, urgency_info_form, saved)

    return template, context, status_code, None


def __set_examination_patient_details_context(user, examination, primary_form, secondary_form, bereaved_form,
                                              urgency_form, saved):
    modal_config = get_tab_change_modal_config()
    locations = user.get_permitted_locations()
    me_offices = user.get_permitted_me_offices()

    error_count = primary_form.error_count + secondary_form.error_count + bereaved_form.error_count + \
        urgency_form.error_count
    return {
        'session_user': user,
        'examination_id': examination.examination_id,
        'patient': examination.case_header,
        'primary_info_form': primary_form,
        'secondary_info_form': secondary_form,
        'bereaved_info_form': bereaved_form,
        'urgency_info_form': urgency_form,
        'error_count': error_count,
        'tab_modal': modal_config,
        "locations": locations,
        "me_offices": me_offices,
        "saved": saved
    }


def edit_examination_medical_team(request, examination_id):
    # get the current user
    user = User.initialise_with_token(request)
    saved = False

    if not user.check_logged_in():
        return redirect_to_login()

    # check the examination exists
    # TODO add 404 check (currently not possible from medical_team endpoint
    medical_team = MedicalTeam.load_by_id(examination_id, user.auth_token)

    if request.method == 'POST':
        # attempt to post and get return form
        medical_team_members_form, status_code, errors, saved = __post_medical_team_form(request, examination_id,
                                                                                         user.auth_token, saved)
    else:
        # the GET medical team form
        medical_team_members_form, status_code, errors = __get_medical_team_form(medical_team=medical_team)

    # render the tab
    return __render_medical_team_tab(errors, examination_id, medical_team_members_form, request, status_code, user,
                                     medical_team.case_header, saved)


def __get_medical_team_form(medical_team=None):
    if medical_team:
        medical_team_members_form = MedicalTeamMembersForm(medical_team=medical_team)
    else:
        medical_team_members_form = MedicalTeamMembersForm()

    status_code = status.HTTP_200_OK
    errors = {'count': 0}
    return medical_team_members_form, status_code, errors


def __post_medical_team_form(request, examination_id, auth_token, saved):
    medical_team_members_form = MedicalTeamMembersForm(request.POST)
    forms_valid = medical_team_members_form.is_valid()

    if forms_valid:
        saved = True
        response = request_handler.update_medical_team(examination_id, medical_team_members_form.to_object(),
                                                       auth_token)
        status_code = response.status_code
        errors = {'count': 0}
    else:
        errors = medical_team_members_form.errors
        status_code = status.HTTP_400_BAD_REQUEST
    return medical_team_members_form, status_code, errors, saved


def __render_medical_team_tab(errors, examination_id, medical_team_members_form, request, status_code, user,
                              header_info, saved):

    medical_examiners = people_request_handler.get_medical_examiners_list_for_examination(user.auth_token,
                                                                                          examination_id)
    medical_examiners_officers = people_request_handler.get_medical_examiners_officers_list_for_examination(
        user.auth_token, examination_id)
    modal_config = get_tab_change_modal_config()
    context = {
        'session_user': user,
        'examination_id': examination_id,
        'patient': header_info,
        'form': medical_team_members_form,
        'medical_examiners': medical_examiners,
        'medical_examiners_officers': medical_examiners_officers,
        'error_count': errors['count'],
        'errors': errors,
        'tab_modal': modal_config,
        'saved': saved
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

    form = None

    if request.method == 'POST':
        form, status_code, errors = __post_case_breakdown_event(request, user, examination_id)

    examination = CaseBreakdown.load_by_id(user.auth_token, examination_id)

    if not type(examination) == CaseBreakdown:
        context = {
            'session_user': user,
            'error': examination,
        }

        return render(request, 'errors/base_error.html', context, status=examination.status_code)

    forms = user.get_forms_for_role()

    medical_team = MedicalTeam.load_by_id(examination_id, user.auth_token)
    patient_details = PatientDetails.load_by_id(examination_id, user.auth_token)

    form_data = __prepare_forms(examination.event_list, medical_team, patient_details, form)

    context = {
        'session_user': user,
        'examination_id': examination_id,
        'forms': forms,
        'qap': medical_team.qap,
        'proposed_cause_of_death': examination.event_list.get_latest_me_scrutiny_cause_of_death(),
        'case_breakdown': examination,
        'bereaved_form': {"use_default_bereaved": True},
        'patient': examination.case_header,
        'form_data': form_data
    }

    return render(request, 'examinations/edit_case_breakdown.html', context, status=status_code)


def __post_case_breakdown_event(request, user, examination_id):
    form = event_form_parser\
        (request.POST)
    if form.is_valid():
        response = event_form_submitter(user.auth_token, examination_id, form)
        status_code = response.status_code
        errors = {'count': 0}
    else:
        errors = form.errors
        status_code = status.HTTP_400_BAD_REQUEST
    return form, status_code, errors


def __prepare_forms(event_list, medical_team, patient_details, form):
    pre_scrutiny_form = PreScrutinyEventForm()
    other_notes_form = OtherEventForm()
    admission_notes_form = AdmissionNotesEventForm()
    meo_summary_form = MeoSummaryEventForm()
    qap_discussion_form = QapDiscussionEventForm()

    if event_list.get_me_scrutiny_draft():
        pre_scrutiny_form.fill_from_draft(event_list.get_me_scrutiny_draft())
    if event_list.get_other_notes_draft():
        other_notes_form.fill_from_draft(event_list.get_other_notes_draft())
    if event_list.get_latest_admission_draft():
        admission_notes_form.fill_from_draft(event_list.get_latest_admission_draft())
    if event_list.get_meo_summary_draft():
        meo_summary_form.fill_from_draft(event_list.get_meo_summary_draft())
    if event_list.get_qap_discussion_draft():
        qap_discussion_form.fill_from_draft(event_list.get_qap_discussion_draft(), medical_team.qap)

    form_data = {
        'PreScrutinyEventForm': pre_scrutiny_form,
        'OtherEventForm': other_notes_form,
        'AdmissionNotesEventForm': admission_notes_form,
        'MeoSummaryEventForm': meo_summary_form,
        'QapDiscussionEventForm': qap_discussion_form
    }

    if form:
        form_data[type(form).__name__] = form.make_active()

    return form_data


def examination_case_outcome(request, examination_id):
    status_code = status.HTTP_200_OK

    user = User.initialise_with_token(request)

    if not user.check_logged_in():
        return redirect_to_login()

    if request.method == 'POST':
        if  CaseOutcome.SCRUTINY_CONFIRMATION_FORM_TYPE in request.POST:
            result = CaseOutcome.complete_scrutiny(user.auth_token, examination_id)
        elif CaseOutcome.CORONER_REFERRAL_FORM_TYPE in request.POST:
            result = CaseOutcome.confirm_coroner_referral(user.auth_token, examination_id)
        else:
            result = GenericError(BadRequestResponse.new(), {'type': 'form', 'action': 'submitting'})

        if result and not result == status.HTTP_200_OK:
            context = {
                'session_user': user,
                'error': result,
            }

            return render(request, 'errors/base_error.html', context, status=result.status_code)

    elif request.method not in ["GET", "POST"]:
        result = MethodNotAllowedError()

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
