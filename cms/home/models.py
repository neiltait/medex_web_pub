import math

from locations.models import Location
from people.models import DropdownPerson


class IndexOverview:

    wordsToCheck = ['trust', 'hospital', 'station']

    def __init__(self, location, response, page_size, page_number):
        self.location_name = None
        self.single_location = False
        self.location_id = location
        self.total_cases = response.get('countOfTotalCases')
        self.filtered_cases = response.get('countOfFilteredCases')
        self.urgent_cases = response.get('countOfUrgentCases')
        self.count_have_unknown_basic_details = response.get('countOfCasesHaveUnknownBasicDetails')
        self.count_scrutiny_ready = response.get('countOfCasesReadyForMEScrutiny')
        self.count_unassigned = response.get('countOfCasesUnassigned')
        self.count_scrutiny_complete = response.get('countOfCasesHaveBeenScrutinisedByME')
        self.count_additional_details_pending = response.get('countOfCasesPendingAdditionalDetails')
        self.count_qap_discussion_pending = response.get('countOfCasesPendingDiscussionWithQAP')
        self.count_representative_discussion_pending = response.get('countOfCasesPendingDiscussionWithRepresentative')
        self.count_final_outcome_outstanding = response.get('countOfCasesHaveFinalCaseOutstandingOutcomes')
        self.filter_locations = self.process_filter_locations(response.get('lookups').get('LocationFilterLookup'))
        self.filter_people = self.process_filter_people(response.get('lookups').get('UserFilterLookup'))
        self.set_location_display_name()
        self.page_size = page_size
        self.page_count = math.ceil(self.filtered_cases / page_size)
        self.page_range = range(self.page_count)
        self.page_number = page_number
        self.next_page = self.page_number + 1
        self.previous_page = self.page_number - 1

    def set_location_display_name(self):
        if self.location_id:
            for location in self.filter_locations:
                if location.location_id == self.location_id:
                    print(vars(location))
                    self.location_name = location.name
        else:
            self.location_name = 'All permitted locations'
            
        if self.location_name:
            self.single_location = any(word in self.location_name.lower() for word in self.wordsToCheck)
        else:
            self.single_location = False
        return self

    def process_filter_locations(self, locations_data):
        locations = []
        for location in locations_data:
            locations.append(Location().set_values(location))
        return locations

    def process_filter_people(self, people_data):
        people = []
        for person in people_data:
            people.append(DropdownPerson(person))
        return people
