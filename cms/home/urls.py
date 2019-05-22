from django.urls import path

from .views import ExaminationIndexView

urlpatterns = [
    path('', ExaminationIndexView.as_view(), name='index'),
]