from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.views.generic.base import View
from rest_framework import status

from errors.models import GenericError, BadRequestResponse
from errors.utils import log_api_error, log_internal_error
from examinations.forms.patient_details import PrimaryExaminationInformationForm, SecondaryExaminationInformationForm, \
    BereavedInformationForm, UrgencyInformationForm
from examinations.forms.medical_team import MedicalTeamMembersForm
from examinations.forms.timeline_events import PreScrutinyEventForm, OtherEventForm, \
    AdmissionNotesEventForm, MeoSummaryEventForm, QapDiscussionEventForm, BereavedDiscussionEventForm, \
    MedicalHistoryEventForm
from examinations.forms.case_outcomes import OutstandingItemsForm
from examinations.models.case_breakdown import CaseBreakdown, CaseStatus
from examinations.models.case_outcomes import CaseOutcome
from examinations.models.core import Examination
from examinations.models.medical_team import MedicalTeam
from examinations.models.patient_details import PatientDetails
from examinations.reports import CoronerDownloadReport
from examinations.utils import event_form_parser, event_form_submitter, get_tab_change_modal_config, ReportGenerator
from home.forms import IndexFilterForm
from home.utils import redirect_to_examination, render_error
from medexCms.api import enums
from medexCms.mixins import LoginRequiredMixin, PermissionRequiredMixin
from medexCms.utils import fallback_to
from monitor.loggers import monitor


class CreateExaminationView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'can_create_examination'
    template = "examinations/create.html"

    @never_cache
    def get(self, request):
        status_code = status.HTTP_200_OK
        context = self.__set_create_examination_context(PrimaryExaminationInformationForm(), False)
        return render(request, self.template, context, status=status_code)

    @never_cache
    def post(self, request):
        add_another = False
        post_body = request.POST
        form = PrimaryExaminationInformationForm(post_body)

        if form.is_valid():
            response = Examination.create(form.to_object(), self.user.auth_token)
            if response.ok:
                monitor.log_case_create_event(self.user, response.json()['examinationId'], form.me_office)

                if form.CREATE_AND_CONTINUE_FLAG in post_body:
                    # scenario 1 - success
                    return self.__successful_post(response)
                else:
                    # scenario 1b - success and add another
                    add_another, form, status_code = self.__reset_form_to_add_another(add_another, form)
            else:
                # scenario 2 - api error
                monitor.log_case_create_event_unsuccessful(self.user, form.me_office, response.status_code)

                status_code = self.__process_api_error(form, response)
        else:
            # scenario 3 - cms validation error
            status_code = status.HTTP_400_BAD_REQUEST

        context = self.__set_return_to_create_examination_context(add_another, form, post_body)
        response = render(request, self.template, context, status=status_code)
        return response

    def __successful_post(self, response):
        examination_id = response.json()['examinationId']
        return redirect_to_examination(examination_id)

    def __reset_form_to_add_another(self, add_another, form):
        add_another = True
        form = PrimaryExaminationInformationForm()
        status_code = status.HTTP_200_OK
        return add_another, form, status_code

    def __set_return_to_create_examination_context(self, add_another, form, post_body):
        context = self.__set_create_examination_context(form, add_another)
        context['full_name'] = fallback_to(post_body.get("first_name"), "") + " " + fallback_to(
            post_body.get("last_name"), "")
        return context

    def __process_api_error(self, form, response):
        form_errors = form.register_form_errors(response.json())
        known_errors = form.register_known_api_errors(response.json())
        unknown_errors = form.register_unknown_api_errors(response.json())
        all_errors = known_errors + unknown_errors + form_errors

        if len(all_errors) > 0:
            for error in all_errors:
                log_api_error('case creation', error)
            status_code = response.status_code
        else:
            log_api_error('case creation', response.text)
            status_code = response.status_code
        return status_code

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
            "add_another": add_another
        }


class EditExaminationView(View):
    @never_cache
    def get(self, request, examination_id):
        return redirect('/cases/' + examination_id + '/patient-details')


class EditExaminationSectionBaseView(View):

    def __init__(self):
        self.examination = None
        self.error = None
        super().__init__()

    def dispatch(self, request, *args, **kwargs):
        if self.examination_section == enums.examination_sections.PATIENT_DETAILS:
            self.examination, self.case_status, self.error = PatientDetails.load_by_id(kwargs.get('examination_id'),
                                                                                       self.user.auth_token)
        elif self.examination_section == enums.examination_sections.MEDICAL_TEAM:
            self.examination, self.case_status, self.error = MedicalTeam.load_by_id(kwargs.get('examination_id'),
                                                                                    self.user.auth_token)
        elif self.examination_section == enums.examination_sections.CASE_BREAKDOWN:
            print('not implemented yet')
        elif self.examination_section == enums.examination_sections.CASE_OUTCOMES:
            print('not implemented yet')
        else:
            log_internal_error('EditExaminationSectionBaseView section load', 'Unknown examination section requested')

        if self.error is not None:
            return render_error(request, self.user, self.error)

        return super().dispatch(request, *args, **kwargs)


class PatientDetailsView(LoginRequiredMixin, PermissionRequiredMixin, EditExaminationSectionBaseView):
    permission_required = 'can_get_examination'
    template = 'examinations/edit_patient_details.html'
    examination_section = enums.examination_sections.PATIENT_DETAILS
    modal_config = get_tab_change_modal_config()

    def __init__(self):
        self.primary_form = None
        self.secondary_form = None
        self.bereaved_form = None
        self.urgency_form = None
        super().__init__()

    @never_cache
    def get(self, request, examination_id):
        status_code = status.HTTP_200_OK

        self.primary_form = PrimaryExaminationInformationForm().set_values_from_instance(self.examination)
        self.secondary_form = SecondaryExaminationInformationForm().set_values_from_instance(self.examination)
        self.bereaved_form = BereavedInformationForm().set_values_from_instance(self.examination)
        self.urgency_form = UrgencyInformationForm().set_values_from_instance(self.examination)

        context = self._set_patient_details_context(False)

        return render(request, self.template, context, status=status_code)

    @never_cache
    def post(self, request, examination_id):
        post_body = request.POST
        get_body = request.GET
        saved = False
        status_code = status.HTTP_200_OK

        self.primary_form = PrimaryExaminationInformationForm(post_body)
        self.secondary_form = SecondaryExaminationInformationForm(post_body)
        self.bereaved_form = BereavedInformationForm(post_body)
        self.urgency_form = UrgencyInformationForm(post_body)
        self.examination.set_values_from_forms(self.primary_form, self.secondary_form, self.bereaved_form,
                                               self.urgency_form)

        forms_valid = self._validate_patient_details_forms()

        if forms_valid:
            submission = self.primary_form.to_object()
            submission.update(self.secondary_form.for_request())
            submission.update(self.bereaved_form.for_request())
            submission.update(self.urgency_form.for_request())
            submission['id'] = examination_id

            response = self.examination.update(submission, self.user.auth_token)
            self.case_status = CaseStatus(response.json())

            if response.status_code == status.HTTP_200_OK and get_body.get('nextTab'):
                # scenario 1b - success and change tab
                return redirect('/cases/%s/%s' % (examination_id, get_body.get('nextTab')))

            elif response.status_code != status.HTTP_200_OK:
                # scenario 2 - api error
                status_code = self.__process_api_error(self.primary_form, response)

            else:
                # scenario 1a - success
                saved = True
        else:
            # scenario 3 - cms validation error
            status_code = status.HTTP_400_BAD_REQUEST

        context = self._set_patient_details_context(saved)

        return render(request, self.template, context, status=status_code)

    def __process_api_error(self, primary_form, response):
        form_errors = primary_form.register_form_errors(response.json())
        known_errors = primary_form.register_known_api_errors(response.json())
        unknown_errors = primary_form.register_unknown_api_errors(response.json())
        all_errors = known_errors + unknown_errors + form_errors

        if len(all_errors) > 0:
            for all_errors in all_errors:
                log_api_error('case creation', all_errors)
            status_code = response.status_code
        else:
            log_api_error('case creation', response.text)
            status_code = response.status_code
        return status_code

    def _set_patient_details_context(self, saved):
        me_offices = self.user.get_permitted_me_offices()
        error_count = self.primary_form.error_count + self.secondary_form.error_count + \
            self.bereaved_form.error_count + self.urgency_form.error_count

        return {
            'session_user': self.user,
            'case_status': self.case_status,
            'examination_id': self.examination.id,
            'patient': self.examination.case_header,
            'primary_info_form': self.primary_form,
            'secondary_info_form': self.secondary_form,
            'bereaved_info_form': self.bereaved_form,
            'urgency_info_form': self.urgency_form,
            'error_count': error_count,
            'tab_modal': self.modal_config,
            "me_offices": me_offices,
            "enums": enums,
            "saved": saved,
        }

    def _validate_patient_details_forms(self):
        return self.primary_form.is_valid() and self.secondary_form.is_valid() \
               and self.bereaved_form.is_valid() and self.urgency_form.is_valid()


class MedicalTeamView(LoginRequiredMixin, PermissionRequiredMixin, EditExaminationSectionBaseView):
    permission_required = 'can_get_examination'
    template = 'examinations/edit_medical_team.html'
    examination_section = enums.examination_sections.MEDICAL_TEAM
    modal_config = get_tab_change_modal_config()

    def __init__(self):
        self.form = None
        super().__init__()

    @never_cache
    def get(self, request, examination_id):
        status_code = status.HTTP_200_OK

        self.form = MedicalTeamMembersForm(medical_team=self.examination)

        context = self._set_context(False)

        return render(request, self.template, context, status=status_code)

    @never_cache
    def post(self, request, examination_id):
        post_body = request.POST
        get_body = request.GET
        status_code = status.HTTP_200_OK
        saved = False
        self.form = MedicalTeamMembersForm(request=post_body)

        if self.form.is_valid():
            response = self.examination.update(self.form.to_object(), self.user.auth_token)
            self.case_status = CaseStatus(response.json())

            if response.status_code == status.HTTP_200_OK and get_body.get('nextTab'):
                # scenario 1b - success and change tab
                return redirect('/cases/%s/%s' % (examination_id, get_body.get('nextTab')))

            elif response.status_code != status.HTTP_200_OK:
                # scenario 2 - api error
                status_code = self.__process_api_error(self.form, response)

            else:
                # scenario 1a - success
                saved = True
        else:
            status_code = status.HTTP_400_BAD_REQUEST

        context = self._set_context(saved)
        return render(request, self.template, context, status=status_code)

    def __process_api_error(self, medical_team_form, response):
        form_errors = medical_team_form.register_form_errors(response.json())
        known_errors = medical_team_form.register_known_api_errors(response.json())
        unknown_errors = medical_team_form.register_unknown_api_errors(response.json())
        all_errors = form_errors + known_errors + unknown_errors

        if len(all_errors) > 0:
            for all_errors in all_errors:
                log_api_error('medical team', all_errors)
            status_code = response.status_code
        else:
            log_api_error('medical team', response.text)
            status_code = response.status_code
        return status_code

    def _set_context(self, saved):
        return {
            'session_user': self.user,
            'examination_id': self.examination.examination_id,
            'case_status': self.case_status,
            'patient': self.examination.case_header,
            'form': self.form,
            'medical_examiners': self.examination.medical_examiner_lookup,
            'medical_examiners_officers': self.examination.medical_examiner_officer_lookup,
            'error_count': self.form.error_count,
            'errors': self.form.errors,
            'tab_modal': self.modal_config,
            'saved': saved,
            'enums': enums
        }


class CaseBreakdownView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'can_get_examination'
    template = 'examinations/edit_case_breakdown.html'
    examination_section = enums.examination_sections.CASE_BREAKDOWN

    def __init__(self):
        self.status_code = status.HTTP_200_OK
        self.amend_type = None
        self.form = None
        self.medical_team = None
        self.patient_details = None
        self.case_status = None
        super().__init__()

    @never_cache
    def get(self, request, examination_id):
        self._load_breakdown(examination_id)
        if self.error:
            return render_error(request, self.user, self.error)

        self.medical_team, self.case_status, error = MedicalTeam.load_by_id(examination_id, self.user.auth_token)
        self.patient_details, self.case_status, error = PatientDetails.load_by_id(examination_id, self.user.auth_token)
        self.amend_type = request.GET.get('amendType')

        context = self._set_context(examination_id)

        return render(request, self.template, context, status=self.status_code)

    @never_cache
    def post(self, request, examination_id):
        self.medical_team, self.case_status, error = MedicalTeam.load_by_id(examination_id, self.user.auth_token)
        self.patient_details, self.case_status, error = PatientDetails.load_by_id(examination_id, self.user.auth_token)
        self.form = event_form_parser(request.POST)
        if self.form.is_valid():
            response = event_form_submitter(self.user.auth_token, examination_id, self.form)
            self.log_timeline_create_event(examination_id,
                                           self.patient_details.medical_examiner_office_responsible,
                                           response,
                                           self.form.is_final)

            self.status_code = response.status_code
            self.form = None
        else:
            self.status_code = status.HTTP_400_BAD_REQUEST

        self._load_breakdown(examination_id)

        context = self._set_context(examination_id)

        return render(request, self.template, context, status=self.status_code)

    def log_timeline_create_event(self, examination_id, location_id, response, is_final):
        if response.ok:
            if is_final:
                monitor.log_create_timeline_event_successful(self.user, examination_id, location_id,
                                                             self.form.__class__.__name__,
                                                             response.json()['eventId'])
            else:
                monitor.log_save_draft_timeline_event_successful(self.user, examination_id, location_id,
                                                                 self.form.__class__.__name__,
                                                                 response.json()['eventId'])
        else:
            if is_final:
                monitor.log_create_timeline_event_unsuccessful(self.user, examination_id, location_id,
                                                               self.form.__class__.__name__,
                                                               response.status_code)
            else:
                monitor.log_save_draft_timeline_event_unsuccessful(self.user, examination_id, location_id,
                                                                   self.form.__class__.__name__,
                                                                   response.status_code)

    def _set_context(self, examination_id):
        forms = self.user.get_forms_for_role(self.examination)
        form_data = self._prepare_forms(self.examination.event_list, self.medical_team, self.patient_details, self.form,
                                        self.amend_type)

        return {
            'session_user': self.user,
            'examination_id': examination_id,
            'forms': forms,
            'qap': self.medical_team.qap,
            'pre_populated': self.examination.prepopulated_items,
            'case_breakdown': self.examination,
            'patient': self.examination.case_header,
            'form_data': form_data,
            'case_status': self.case_status,
            'enums': enums
        }

    def _load_breakdown(self, examination_id):
        self.examination, self.case_status, self.error = CaseBreakdown.load_by_id(examination_id, self.user.auth_token)

    def _prepare_forms(self, event_list, medical_team, patient_details, form, amend_type):
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
                form_data[latest_for_type.form_type] = latest_for_type \
                    .as_amendment_form(medical_team.qap, patient_details.representatives).make_active()
            else:
                form_type = '%sEventForm' % amend_type
                form_data[form_type] = form_data[form_type].make_active()

        if form:
            form_data[type(form).__name__] = form.make_active()

        return form_data


class CaseOutcomeView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'can_get_examination'
    template = 'examinations/case_outcome.html'
    examination_section = enums.examination_sections.CASE_OUTCOMES

    def __init__(self):
        self.status_code = status.HTTP_200_OK

    @never_cache
    def get(self, request, examination_id):
        self._load_case_outcome(examination_id)
        if self.error:
            return render_error(request, self.user, self.error)

        context = self._set_context()

        return render(request, self.template, context, status=self.status_code)

    @never_cache
    def post(self, request, examination_id):
        post_body = request.POST
        if CaseOutcome.SCRUTINY_CONFIRMATION_FORM_TYPE in post_body:
            result = CaseOutcome.complete_scrutiny(self.user.auth_token, examination_id)
        elif CaseOutcome.CORONER_REFERRAL_FORM_TYPE in post_body:
            result = CaseOutcome.confirm_coroner_referral(self.user.auth_token, examination_id)
        elif CaseOutcome.OUTSTANDING_ITEMS_FORM_TYPE in post_body:
            form = OutstandingItemsForm(post_body)
            result = CaseOutcome.update_outstanding_items(self.user.auth_token, examination_id, form.for_request())
        elif CaseOutcome.CLOSE_CASE_FORM_TYPE in post_body:
            result = CaseOutcome.close_case(self.user.auth_token, examination_id)
        else:
            result = GenericError(BadRequestResponse.new(), {'type': 'form', 'action': 'submitting'})

        if result and not result == status.HTTP_200_OK:
            log_api_error('case outcome update', result.get_message())
            self._log_case_outcome_unsuccessful(post_body, examination_id)
            return render_error(request, self.user, result)

        self._load_case_outcome(examination_id)
        context = self._set_context()

        self._log_case_outcome(post_body)

        return render(request, self.template, context, status=self.status_code)

    def _load_case_outcome(self, examination_id):
        self.case_outcome, self.case_status, self.error = CaseOutcome.load_by_id(examination_id, self.user.auth_token)

    def _set_context(self):
        return {
            'session_user': self.user,
            'examination_id': self.case_outcome.examination_id,
            'case_outcome': self.case_outcome,
            'case_status': self.case_status,
            'patient': self.case_outcome.case_header,
            'enums': enums,
        }

    def _log_case_outcome(self, post_body):
        if CaseOutcome.SCRUTINY_CONFIRMATION_FORM_TYPE in post_body:
            monitor.log_confirm_scrutiny(self.user, self.case_outcome.examination_id,
                                         'not available', self.case_outcome)

        elif CaseOutcome.CORONER_REFERRAL_FORM_TYPE in post_body:
            monitor.log_coroner_referral(self.user, self.case_outcome.examination_id,
                                         'not available', self.case_outcome)

        elif CaseOutcome.OUTSTANDING_ITEMS_FORM_TYPE in post_body:
            monitor.log_outstanding_items_submission(self.user, self.case_outcome.examination_id,
                                                     'not available', self.case_outcome)

        elif CaseOutcome.CLOSE_CASE_FORM_TYPE in post_body:
            monitor.log_case_closed(self.user, self.case_outcome.examination_id,
                                    'not available', self.case_outcome)

    def _log_case_outcome_unsuccessful(self, post_body, examination_id):
        if CaseOutcome.SCRUTINY_CONFIRMATION_FORM_TYPE in post_body:
            monitor.log_confirm_scrutiny_unsuccessful(self.user, examination_id, 'not available')

        elif CaseOutcome.CORONER_REFERRAL_FORM_TYPE in post_body:
            monitor.log_coroner_referral_unsuccessful(self.user, examination_id, 'not available')

        elif CaseOutcome.OUTSTANDING_ITEMS_FORM_TYPE in post_body:
            monitor.log_outstanding_items_submission_unsuccessful(self.user, examination_id, 'not available')

        elif CaseOutcome.CLOSE_CASE_FORM_TYPE in post_body:
            monitor.log_case_closed_unsuccessful(self.user, examination_id, 'not available')


class ClosedExaminationIndexView(LoginRequiredMixin, View):
    template = 'home/index.html'

    @never_cache
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


class CoronerReportDownloadView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'can_get_examination'
    template = 'examinations/templates/reports/coroner-referral-form.odt'

    @never_cache
    def get(self, request, examination_id):
        report, errors = CoronerDownloadReport.load_by_id(examination_id, self.user.auth_token)

        return ReportGenerator.create_report(self.template, report, filename="report.odt")
