from django.conf.urls import url

from examinations.views import CreateExaminationView, ClosedExaminationIndexView, EditExaminationView, \
    PatientDetailsView, MedicalTeamView, CaseBreakdownView, CaseOutcomeView

urlpatterns = [
    url('create', CreateExaminationView.as_view(), name='create_examination'),
    url('closed', ClosedExaminationIndexView.as_view(), name='closed_examination_index'),
    url(r'(?P<examination_id>[\w\-]+)/patient-details', PatientDetailsView.as_view(), name='edit_patient_details'),
    url(r'(?P<examination_id>[\w\-]+)/medical-team', MedicalTeamView.as_view(), name='edit_medical_team'),
    url(r'(?P<examination_id>[\w\-]+)/case-breakdown', CaseBreakdownView.as_view(), name='edit_examination_case_breakdown'),
    url(r'(?P<examination_id>[\w\-]+)/case-outcome', CaseOutcomeView.as_view(), name='view_examination_case_outcome'),
    url(r'(?P<examination_id>[\w\-]+)', EditExaminationView.as_view(), name='edit_examination'),
]
