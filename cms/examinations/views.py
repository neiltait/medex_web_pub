from django.shortcuts import render, redirect
from requests.models import Response
from rest_framework import status

from alerts import messages
from alerts.utils import generate_error_alert
from errors.models import GenericError
from examinations import request_handler
from examinations.forms import PrimaryExaminationInformationForm, SecondaryExaminationInformationForm, \
    BereavedInformationForm, UrgencyInformationForm, MedicalTeamMembersForm, PreScrutinyEventForm, OtherEventForm, \
    AdmissionNotesEventForm, MeoSummaryEventForm, QapDiscussionEventForm, BereavedDiscussionEventForm, \
    OutstandingItemsForm, MedicalHistoryEventForm
from examinations.models import PatientDetails, CaseBreakdown, MedicalTeam, CaseOutcome
from home.forms import IndexFilterForm
from home.utils import redirect_to_login, render_404, redirect_to_examination
from examinations.utils import event_form_parser, event_form_submitter, get_tab_change_modal_config
from locations import request_handler as location_request_handler
from locations.models import Location
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
    add_another = False

    if request.POST:
        form = PrimaryExaminationInformationForm(request.POST)
        if form.is_valid():
            response = request_handler.post_new_examination(form.to_object(), user.auth_token)
            if response.status_code == status.HTTP_200_OK:
                if 'create-and-continue' in request.POST:
                    examination_id = response.json()['examinationId']
                    return redirect_to_examination(examination_id)
                else:
                    add_another = True
                    form = None
                    status_code = status.HTTP_200_OK
            else:
                alerts.append(generate_error_alert(messages.ERROR_IN_FORM))
                status_code = response.status_code
        else:
            errors = form.errors
            alerts.append(generate_error_alert(messages.ERROR_IN_FORM))
            status_code = status.HTTP_400_BAD_REQUEST

    return render_create_examination_form(request, user, add_another, alerts, errors, status_code, form)


def render_create_examination_form(request, user, add_another, alerts=[], errors=None, status_code=status.HTTP_200_OK,
                                   form=None):
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
        "add_another": add_another
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
    saved = False

    examination = PatientDetails.load_by_id(examination_id, user.auth_token)
    if not examination:
        return render_404(request, user, 'case')

    if request.method == 'GET':
        primary_info_form = PrimaryExaminationInformationForm().set_values_from_instance(examination)
        secondary_info_form = SecondaryExaminationInformationForm().set_values_from_instance(examination)
        bereaved_info_form = BereavedInformationForm().set_values_from_instance(examination)
        urgency_info_form = UrgencyInformationForm().set_values_from_instance(examination)

    elif request.method == 'POST':

        primary_info_form = PrimaryExaminationInformationForm(request.POST)
        secondary_info_form = SecondaryExaminationInformationForm(request.POST)
        bereaved_info_form = BereavedInformationForm(request.POST)
        urgency_info_form = UrgencyInformationForm(request.POST)
        examination.set_primary_info_values(primary_info_form).set_secondary_info_values(secondary_info_form) \
            .set_bereaved_info_values(bereaved_info_form).set_urgency_info_values(urgency_info_form)

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
                saved = True
        else:
            error_count = primary_info_form.errors['count'] + secondary_info_form.errors['count'] + \
                          bereaved_info_form.errors['count'] + urgency_info_form.errors['count']
            status_code = status.HTTP_400_BAD_REQUEST

    modal_config = get_tab_change_modal_config()

    locations = location_request_handler.get_locations_list(user.auth_token)
    me_offices = location_request_handler.get_me_offices_list(user.auth_token)

    context = {
        'session_user': user,
        'examination_id': examination_id,
        'patient': examination.case_header,
        'primary_info_form': primary_info_form,
        'secondary_info_form': secondary_info_form,
        'bereaved_info_form': bereaved_info_form,
        'urgency_info_form': urgency_info_form,
        'error_count': error_count,
        'tab_modal': modal_config,
        "locations": locations,
        "me_offices": me_offices,
        "saved": saved
    }

    return render(request, 'examinations/edit_patient_details.html', context, status=status_code)


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
        'agreed_cause_of_death': examination.event_list.get_latest_agreed_cause_of_death(),
        'case_breakdown': examination,
        'bereaved_form': {"use_default_bereaved": True},
        'patient': examination.case_header,
        'form_data': form_data
    }

    return render(request, 'examinations/edit_case_breakdown.html', context, status=status_code)


def __post_case_breakdown_event(request, user, examination_id):
    form = event_form_parser(request.POST)
    if form.is_valid():
        response = event_form_submitter(user.auth_token, examination_id, form)
        status_code = response.status_code
        form = None
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
    bereaved_discussion_form = BereavedDiscussionEventForm(representatives=patient_details.representatives)
    medical_history_form = MedicalHistoryEventForm()

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
    if event_list.get_bereaved_discussion_draft():
        bereaved_discussion_form.fill_from_draft(event_list.get_bereaved_discussion_draft(), patient_details.representatives)
    if event_list.get_medical_history_draft():
        medical_history_form.fill_from_draft(event_list.get_medical_history_draft())

    form_data = {
        'PreScrutinyEventForm': pre_scrutiny_form,
        'OtherEventForm': other_notes_form,
        'AdmissionNotesEventForm': admission_notes_form,
        'MeoSummaryEventForm': meo_summary_form,
        'QapDiscussionEventForm': qap_discussion_form,
        'BereavedDiscussionEventForm': bereaved_discussion_form,
        'MedicalHistoryEventForm': medical_history_form
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
        if CaseOutcome.SCRUTINY_CONFIRMATION_FORM_TYPE in request.POST:
            result = CaseOutcome.complete_scrutiny(user.auth_token, examination_id)
        elif CaseOutcome.CORONER_REFERRAL_FORM_TYPE in request.POST:
            result = CaseOutcome.confirm_coroner_referral(user.auth_token, examination_id)
        elif CaseOutcome.OUTSTANDING_ITEMS_FORM_TYPE in request.POST:
            form = OutstandingItemsForm(request.POST)
            result = CaseOutcome.update_outstanding_items(user.auth_token, examination_id, form.for_request())
        elif CaseOutcome.CLOSE_CASE_FORM_TYPE in request.POST:
            result = CaseOutcome.close_case(user.auth_token, examination_id)
        else:
            # TODO refactor in to BadRequestResponse class
            response = Response()
            response.status_code = status.HTTP_400_BAD_REQUEST
            result = GenericError(response, {'type': 'form', 'action': 'submitting'})

        if result and not result == status.HTTP_200_OK:
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


def closed_examination_index(request):
    user = User.initialise_with_token(request)
    if not user.check_logged_in():
        return redirect_to_login()

    people = False

    if request.method == 'GET':
        user.load_closed_examinations()
        form = IndexFilterForm()
    elif request.method == 'POST':
        form = IndexFilterForm(request.POST)
        user.load_closed_examinations(location=form.location, person=form.person)
        filter_location = Location.initialise_with_id(request.POST.get('location'))
        people = filter_location.load_permitted_users(user.auth_token)
    locations = user.get_permitted_locations()

    context = {
        'page_header': 'Closed Case Dashboard',
        'session_user': user,
        'filter_locations': locations,
        'filter_people': people,
        'form': form,
        'closed_list': True
    }
    return render(request, 'home/index.html', context)
