class IndexFilterForm:

    def __init__(self, query_params, defaults):
        self.location = ''
        self.person = ''
        self.set_location_value(query_params.get('location'), defaults.get('location'))
        self.set_person_value(query_params.get('person'), defaults.get('person'))

    def set_location_value(self, query_location, default_location):
        if query_location and query_location == 'all':
            self.location = None
        elif query_location:
            self.location = query_location
        else:
            self.location = default_location

    def set_person_value(self, query_person, default_person):
        if query_person and query_person == 'all':
            self.person = None
        elif query_person:
            self.person = query_person
        else:
            self.person = default_person
