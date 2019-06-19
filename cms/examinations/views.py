from django.shortcuts import render, redirect
from django.views.generic.base import View
from rest_framework import status

from errors.models import GenericError, BadRequestResponse
from errors.utils import log_unexpected_method, log_api_error
from errors.views import __handle_method_not_allowed_error
from examinations.forms import PrimaryExaminationInformationForm, SecondaryExaminationInformationForm, \
    BereavedInformationForm, UrgencyInformationForm, MedicalTeamMembersForm, PreScrutinyEventForm, OtherEventForm, \
    AdmissionNotesEventForm, MeoSummaryEventForm, QapDiscussionEventForm, BereavedDiscussionEventForm, \
    OutstandingItemsForm, MedicalHistoryEventForm
from examinations.models import PatientDetails, CaseBreakdown, MedicalTeam, CaseOutcome, Examination, PatientHeader
from examinations.utils import event_form_parser, event_form_submitter, get_tab_change_modal_config
from home.forms import IndexFilterForm
from home.utils import redirect_to_login, render_404, redirect_to_examination
from medexCms.api import enums
from medexCms.mixins import LoginRequiredMixin, PermissionRequiredMixin
from users.models import User


class CreateExaminationView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'can_create_examination'
    template = "examinations/create.html"

    def get(self, request):
        status_code = status.HTTP_200_OK
        context = self.__set_create_examination_context(PrimaryExaminationInformationForm(), False)
        return render(request, self.template, context, status=status_code)

    def post(self, request):
        add_another = False
        post_body = request.POST
        form = PrimaryExaminationInformationForm(post_body)

        if form.is_valid():
            response = Examination.create(form.to_object(), self.user.auth_token)

            if response.ok:
                if form.CREATE_AND_CONTINUE_FLAG in post_body:
                    examination_id = response.json()['examinationId']
                    return redirect_to_examination(examination_id)
                else:
                    add_another = True
                    form = PrimaryExaminationInformationForm()
                    status_code = status.HTTP_200_OK
            else:
                log_api_error('case creation', response.text)
                status_code = response.status_code
        else:
            status_code = status.HTTP_400_BAD_REQUEST

        context = self.__set_create_examination_context(form, add_another)
        context['full_name'] = post_body["first_name"] + " " + post_body["last_name"]
        return render(request, self.template, context, status=status_code)

    def __set_create_examination_context(self, form, add_another):
        me_offices = self.user.get_permitted_me_offices()

        return {
            "session_user": self.user,
            "page_heading": "Add a new case",
            "sub_heading": "Primary information",
            "me_offices": me_offices,
            "form": form,
            "enums": enums,
            "errors": form.errors,
            "add_another": add_another,
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

        log_unexpected_method(request.method, 'patient details')

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

    forms_valid = __validate_patient_details_forms(primary_info_form, secondary_info_form, bereaved_info_form,
                                                   urgency_info_form)
    if forms_valid:
        submission = primary_info_form.to_object()
        submission.update(secondary_info_form.for_request())
        submission.update(bereaved_info_form.for_request())
        submission.update(urgency_info_form.for_request())
        submission['id'] = examination.id

        response = PatientDetails.update(examination.id, submission, user.auth_token)

        if response.status_code == status.HTTP_200_OK and get_body.get('nextTab'):
            return None, None, None, redirect('/cases/%s/%s' % (examination.id, get_body.get('nextTab')))
        elif response.status_code != status.HTTP_200_OK:
            log_api_error('patient details update', response.text)
            status_code = response.status_code
        else:
            saved = True
            examination.case_header = PatientHeader(response.json().get("header"))
    else:
        status_code = status.HTTP_400_BAD_REQUEST

    context = __set_examination_patient_details_context(user, examination, primary_info_form, secondary_info_form,
                                                        bereaved_info_form, urgency_info_form, saved)

    return template, context, status_code, None


def __validate_patient_details_forms(primary_info_form, secondary_info_form, bereaved_info_form, urgency_info_form):
    primary_valid = primary_info_form.is_valid()
    secondary_valid = secondary_info_form.is_valid()
    bereaved_valid = bereaved_info_form.is_valid()
    urgency_valid = urgency_info_form.is_valid()

    return primary_valid and secondary_valid and bereaved_valid and urgency_valid


def __set_examination_patient_details_context(user, examination, primary_form, secondary_form, bereaved_form,
                                              urgency_form, saved):
    modal_config = get_tab_change_modal_config()
    me_offices = user.get_permitted_me_offices()

    error_count = primary_form.error_count + secondary_form.error_count + bereaved_form.error_count + \
        urgency_form.error_count
    return {
        'session_user': user,
        'examination_id': examination.id,
        'patient': examination.case_header,
        'primary_info_form': primary_form,
        'secondary_info_form': secondary_form,
        'bereaved_info_form': bereaved_form,
        'urgency_info_form': urgency_form,
        'error_count': error_count,
        'tab_modal': modal_config,
        "me_offices": me_offices,
        "enums": enums,
        "saved": saved,
    }


def examination_medical_team(request, examination_id):
    # get the current user
    user = User.initialise_with_token(request)
    if not user.check_logged_in():
        return redirect_to_login()

    saved = False

    # check the examination exists
    medical_team = MedicalTeam.load_by_id(examination_id, user.auth_token)
    # TODO add better 404 check (currently not possible from medical_team endpoint
    if not medical_team or not medical_team.case_header:
        return render_404(request, user, 'medical team')

    if request.method == 'GET':
        template, context, status_code = __get_medical_team_form(user, medical_team)

    elif request.method == 'POST':
        # attempt to post and get return form
        template, context, status_code, redirect_response = __post_medical_team_form(user, medical_team, request.POST, request.GET)

        if redirect_response:
            return redirect_response
    else:
        # the GET medical team form
        log_unexpected_method(request.method, 'create examination')
        template, context, status_code = __handle_method_not_allowed_error(user)

    # render the tab
    return render(request, template, context, status=status_code)


def __get_medical_team_form(user, medical_team):
    template = 'examinations/edit_medical_team.html'
    status_code = status.HTTP_200_OK

    if medical_team:
        form = MedicalTeamMembersForm(medical_team=medical_team)
    else:
        form = MedicalTeamMembersForm()

    context = __set_medical_team_context(user, medical_team, form, False)

    return template, context, status_code


def __post_medical_team_form(user, medical_team, post_body, get_body):
    template = 'examinations/edit_medical_team.html'
    saved = False
    form = MedicalTeamMembersForm(request=post_body)
    forms_valid = form.is_valid()

    if forms_valid:
        response = medical_team.update(form.to_object(), user.auth_token)

        if response.status_code == status.HTTP_200_OK and get_body.get('nextTab'):
            return None, None, None, redirect('/cases/%s/%s' % (medical_team.examination_id, get_body.get('nextTab')))
        elif response.status_code != status.HTTP_200_OK:
            log_api_error('patient details update', response.text)
            status_code = response.status_code
        else:
            saved = True
            status_code = response.status_code
    else:
        status_code = status.HTTP_400_BAD_REQUEST

    context = __set_medical_team_context(user, medical_team, form, saved)
    return template, context, status_code, None


def __set_medical_team_context(user, medical_team, form, saved):
    modal_config = get_tab_change_modal_config()
    return {
        'session_user': user,
        'examination_id': medical_team.examination_id,
        'patient': medical_team.case_header,
        'form': form,
        'medical_examiners': medical_team.medical_examiner_lookup,
        'medical_examiners_officers': medical_team.medical_examiner_officer_lookup,
        'error_count': form.error_count,
        'errors': form.errors,
        'tab_modal': modal_config,
        'saved': saved,
    }


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

    forms = user.get_forms_for_role(examination)

    medical_team = MedicalTeam.load_by_id(examination_id, user.auth_token)
    patient_details = PatientDetails.load_by_id(examination_id, user.auth_token)

    amend_type = request.GET.get('amendType')

    form_data = __prepare_forms(examination.event_list, medical_team, patient_details, form, amend_type)

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
        'form_data': form_data,
        'enums': enums,
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


def __prepare_forms(event_list, medical_team, patient_details, form, amend_type):
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
        bereaved_discussion_form.fill_from_draft(event_list.get_bereaved_discussion_draft(),
                                                 patient_details.representatives)
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

    if amend_type and not form:
        latest_for_type = event_list.get_latest_of_type(amend_type)
        if latest_for_type:
            form_data[latest_for_type.form_type] = latest_for_type.as_amendment_form(medical_team.qap,
                                                                                     patient_details.representatives)\
                .make_active()
        else:
            form_type = '%sEventForm' % amend_type
            form_data[form_type] = form_data[form_type].make_active()

    if form:
        form_data[type(form).__name__] = form.make_active()

    return form_data


def examination_case_outcome(request, examination_id):
    user = User.initialise_with_token(request)
    if not user.check_logged_in():
        return redirect_to_login()

    if request.method == 'GET':
        template, context, status_code = __get_examination_case_outcome(user, examination_id)

    elif request.method == 'POST':
        template, context, status_code = __post_examination_case_outcome(user, examination_id, request.POST)

    else:
        log_unexpected_method(request.method, 'case outcome')
        template, context, status_code = __handle_method_not_allowed_error(user)

    return render(request, template, context, status=status_code)


def __get_examination_case_outcome(user, examination_id):
    template, context, status_code = __load_case_outcome(user, examination_id)

    return template, context, status_code


def __post_examination_case_outcome(user, examination_id, post_body):
    if CaseOutcome.SCRUTINY_CONFIRMATION_FORM_TYPE in post_body:
        result = CaseOutcome.complete_scrutiny(user.auth_token, examination_id)
    elif CaseOutcome.CORONER_REFERRAL_FORM_TYPE in post_body:
        result = CaseOutcome.confirm_coroner_referral(user.auth_token, examination_id)
    elif CaseOutcome.OUTSTANDING_ITEMS_FORM_TYPE in post_body:
        form = OutstandingItemsForm(post_body)
        result = CaseOutcome.update_outstanding_items(user.auth_token, examination_id, form.for_request())
    elif CaseOutcome.CLOSE_CASE_FORM_TYPE in post_body:
        result = CaseOutcome.close_case(user.auth_token, examination_id)
    else:
        result = GenericError(BadRequestResponse.new(), {'type': 'form', 'action': 'submitting'})

    if result and not result == status.HTTP_200_OK:
        log_api_error('case outcome update', result.get_message())
        context = {
            'session_user': user,
            'error': result,
        }

        return 'errors/base_error.html', context, result.status_code

    template, context, status_code = __load_case_outcome(user, examination_id)
    return template, context, status_code


def __load_case_outcome(user, examination_id):
    template = 'examinations/case_outcome.html'
    status_code = status.HTTP_200_OK
    case_outcome, error = CaseOutcome.load_by_id(user.auth_token, examination_id)
    if error:
        context = {
            'session_user': user,
            'error': error,
        }

        return 'errors/base_error.html', context, error.status_code
    else:
        context = __set_examination_case_outcome_context(user, case_outcome)

        return template, context, status_code


def __set_examination_case_outcome_context(user, case_outcome):
    modal_config = get_tab_change_modal_config()

    return {
        'session_user': user,
        'examination_id': case_outcome.examination_id,
        'case_outcome': case_outcome,
        'patient': case_outcome.case_header,
        'enums': enums,
    }


class ClosedExaminationIndexView(LoginRequiredMixin, View):
    template = 'home/index.html'

    def get(self, request):
        status_code = status.HTTP_200_OK
        query_params = request.GET

        page_number = int(query_params.get('page_number')) if query_params.get('page_number') else 1
        page_size = 20

        form = IndexFilterForm(query_params, self.user.default_filter_options())
        self.user.load_closed_examinations(page_size, page_number, form.get_location_value(), form.get_person_value())

        context = self.set_context(form)

        return render(request, self.template, context, status=status_code)
    
    def set_context(self, form):
        return {
            'page_header': 'Closed Case Dashboard',
            'session_user': self.user,
            'form': form,
            'closed_list': True,
            'pagination_url': 'closed_examination_index',
        }
