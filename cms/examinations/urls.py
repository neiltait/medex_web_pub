from django.conf.urls import url

from . import views

urlpatterns = [
    url('create', views.create_examination, name='create_examination'),
    url(r'(?P<examination_id>[\w\-]+)/patient-details', views.edit_examination_patient_details,
        name='edit_examination_patient_details'),
    url(r'(?P<examination_id>[\w\-]+)/medical-team', views.edit_examination_medical_team,
        name='edit_examination_medical_team'),
    url(r'(?P<examination_id>[\w\-]+)', views.edit_examination, name='edit_examination'),
]
