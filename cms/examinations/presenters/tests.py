from examinations.presenters.core import PatientHeader
from medexCms.test.mocks import ExaminationMocks
from medexCms.test.utils import MedExTestCase


class ExaminationsCorePresentersTests(MedExTestCase):

    # PatientHeader tests

    def test_patient_header_full_name_correctly_joins_first_and_last_names(self):
        patient_header_data = ExaminationMocks.get_patient_header_content()
        patient_header = PatientHeader(patient_header_data)
        full_name = patient_header.full_name
        self.assertEqual(full_name.split(' ')[0], patient_header_data.get('givenNames'))
        self.assertEqual(full_name.split(' ')[1], patient_header_data.get('surname'))
