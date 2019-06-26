from locations.models import Location
from medexCms.test.utils import MedExTestCase


class LocationModelTests(MedExTestCase):

    # Location tests
    def test_initialise_with_id_returns_a_location_instance_with_the_id_set(self):
        location_id = 'afefwrgwr'
        result = Location.initialise_with_id(location_id)
        self.assertEqual(result.location_id, location_id)
