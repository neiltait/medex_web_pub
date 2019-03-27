from medexCms.test import mocks
from medexCms.test.utils import MedExTestCase
from people.models import BereavedRepresentative


class PeopleModelsTest(MedExTestCase):

    ##### BereavedRepresentative tests

    def test_initialising_with_the_none_date_leads_no_appointment_details_set(self):
        bereaved = BereavedRepresentative(mocks.get_bereaved_representative())
        self.assertIsNone(bereaved.appointment_date)
        self.assertIsNone(bereaved.appointment_day)
        self.assertIsNone(bereaved.appointment_month)
        self.assertIsNone(bereaved.appointment_year)

    def test_initialising_with_the_no_date_leads_no_appointment_details_set(self):
        bereaved_data = mocks.get_bereaved_representative()
        bereaved_data['appointmentDate'] = None
        bereaved = BereavedRepresentative(bereaved_data)
        self.assertIsNone(bereaved.appointment_date)
        self.assertIsNone(bereaved.appointment_day)
        self.assertIsNone(bereaved.appointment_month)
        self.assertIsNone(bereaved.appointment_year)

    def test_initialising_with_the_valid_date_leads_appointment_details_being_set(self):
        bereaved_data = mocks.get_bereaved_representative()
        bereaved_data['appointmentDate'] = '2019-03-26T13:29:50.473Z'
        bereaved = BereavedRepresentative(bereaved_data)
        self.assertEqual(bereaved.appointment_day, 26)
        self.assertEqual(bereaved.appointment_month, 3)
        self.assertEqual(bereaved.appointment_year, 2019)
