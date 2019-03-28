from unittest.mock import patch

from locations.models import Location
from medexCms.test import mocks
from medexCms.test.utils import MedExTestCase
from people.models import DropdownPerson


class LocationModelTests(MedExTestCase):

    #### Location tests
    def test_initialise_with_id_returns_a_location_instance_with_the_id_set(self):
        location_id = 'afefwrgwr'
        result = Location.initialise_with_id(location_id)
        self.assertEqual(result.location_id, location_id)

    @patch('locations.request_handler.get_permitted_users', return_value=mocks.SUCCESSFUL_MEDICAL_EXAMINERS_LOAD)
    def test_load_permitted_users_returns_a_list_of_users(self, mock_user_load):
        location_id = 'afefwrgwr'
        location = Location.initialise_with_id(location_id)
        result = location.load_permitted_users(mocks.ACCESS_TOKEN)
        self.assertEqual(type(result), list)
        self.assertIsTrue(len(result) > 0)
        self.assertEqual(type(result[0]), DropdownPerson)
