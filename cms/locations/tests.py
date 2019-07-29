from locations.models import Location, LocationCollection
from medexCms.test.utils import MedExTestCase


class LocationModelTests(MedExTestCase):

    # Location tests
    def test_initialise_with_id_returns_a_location_instance_with_the_id_set(self):
        location_id = 'afefwrgwr'
        result = Location.initialise_with_id(location_id)
        self.assertEqual(result.location_id, location_id)


class LocationCollectionModelTests(MedExTestCase):

    def get_list_of_locations(self):
        return [
            {
                'locationId': '1',
                'name': 'National',
                'parentId': '1',
                'type': Location.NATIONAL_TYPE
            },
            {
                'locationId': '2',
                'name': 'North',
                'parentId': '1',
                'type': Location.REGIONAL_TYPE
            },
            {
                'locationId': '3',
                'name': 'South',
                'parentId': '1',
                'type': Location.REGIONAL_TYPE
            },
            {
                'locationId': '4',
                'name': 'Heaven',
                'parentId': '3',
                'type': Location.TRUST_TYPE
            },
            {
                'locationId': '5',
                'name': 'Earth',
                'parentId': '3',
                'type': Location.TRUST_TYPE
            },
            {
                'locationId': '6',
                'name': 'Hell',
                'parentId': '2',
                'type': Location.TRUST_TYPE
            },
        ]

    def test_location_collection_initialises_from_api_json_dict(self):
        api_data = self.get_list_of_locations()

        location_collection = LocationCollection(api_data)

        self.assertIsNotNone(location_collection)

    def test_location_collection_returns_national_location_as_object(self):
        api_data = self.get_list_of_locations()

        location_collection = LocationCollection(api_data)
        national = location_collection.national

        self.assertIsInstance(national, Location)

    def test_location_collection_returns_for_national_if_no_national_location_present(self):
        api_data = [location for location in self.get_list_of_locations() if
                    location.get('type') != Location.NATIONAL_TYPE]

        location_collection = LocationCollection(api_data)
        national = location_collection.national

        self.assertIsNone(national)

    def test_location_collection_returns_regions_as_list_of_location_objects(self):
        api_data = self.get_list_of_locations()

        location_collection = LocationCollection(api_data)

        self.assertEqual(len(location_collection.regions), 2)

    def test_location_collection_returns_empty_list_if_no_regions_present(self):
        api_data = [location for location in self.get_list_of_locations() if
                    location.get('type') != Location.REGIONAL_TYPE]

        location_collection = LocationCollection(api_data)

        self.assertEqual(len(location_collection.regions), 0)

    def test_location_collection_returns_trusts_as_list_of_location_objects(self):
        api_data = self.get_list_of_locations()

        location_collection = LocationCollection(api_data)

        self.assertEqual(len(location_collection.trusts), 3)

    def test_location_collection_returns_empty_list_if_no_trusts_present(self):
        api_data = [location for location in self.get_list_of_locations() if
                    location.get('type') != Location.TRUST_TYPE]

        location_collection = LocationCollection(api_data)

        self.assertEqual(len(location_collection.trusts), 0)
