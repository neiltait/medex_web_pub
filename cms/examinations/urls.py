from django.conf.urls import url

from examinations.views import CreateExaminationView, ClosedExaminationIndexView
from . import views

urlpatterns = [
    url('create', CreateExaminationView.as_view(), name='create_examination'),
    url('closed', ClosedExaminationIndexView.as_view(), name='closed_examination_index'),
    url(r'(?P<examination_id>[\w\-]+)/patient-details', views.examination_patient_details,
        name='edit_examination_patient_details'),
    url(r'(?P<examination_id>[\w\-]+)/medical-team', views.examination_medical_team,
        name='edit_examination_medical_team'),
    url(r'(?P<examination_id>[\w\-]+)/case-breakdown', views.edit_examination_case_breakdown,
        name='edit_examination_case_breakdown'),
    url(r'(?P<examination_id>[\w\-]+)/case-outcome', views.examination_case_outcome,
        name='view_examination_case_outcome'),
    url(r'(?P<examination_id>[\w\-]+)', views.edit_examination, name='edit_examination'),
]
