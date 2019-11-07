from django.conf.urls import url


from examinations.views import CreateExaminationView, ClosedExaminationIndexView, EditExaminationView, \
    PatientDetailsView, MedicalTeamView, CaseBreakdownView, CaseOutcomeView, CoronerReportDownloadView, \
    FinancialReportsView, CaseSettingsIndexView, VoidCaseSuccess

urlpatterns = [
    url('create', CreateExaminationView.as_view(), name='create_examination'),
    url('closed', ClosedExaminationIndexView.as_view(), name='closed_examination_index'),
    url('financial-reports', FinancialReportsView.as_view(), name='financial_reports'),
    url('void-success', VoidCaseSuccess.as_view(), name='void-case-success'),
    url(r'(?P<examination_id>[\w\-]+)/case-settings', CaseSettingsIndexView.as_view(), name='case_settings'),
    url(r'(?P<examination_id>[\w\-]+)/patient-details', PatientDetailsView.as_view(), name='edit_patient_details'),
    url(r'(?P<examination_id>[\w\-]+)/medical-team', MedicalTeamView.as_view(), name='edit_medical_team'),
    url(r'(?P<examination_id>[\w\-]+)/case-breakdown', CaseBreakdownView.as_view(), name='edit_case_breakdown'),
    url(r'(?P<examination_id>[\w\-]+)/case-outcome', CaseOutcomeView.as_view(), name='view_case_outcome'),
    url(r'(?P<examination_id>[\w\-]+)/download-coroner-report', CoronerReportDownloadView.as_view(),
        name='download_coroner_report'),
    url(r'(?P<examination_id>[\w\-]+)', EditExaminationView.as_view(), name='edit_examination')

]
