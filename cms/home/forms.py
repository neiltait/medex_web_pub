class IndexFilterForm:

    def __init__(self, query_params, defaults):
        self.location = query_params.get('location') if query_params.get('location') else defaults.get('location')
        self.person = query_params.get('person') if query_params.get('person') else defaults.get('person')
        self.status = query_params.get('status') if query_params.get('status') else ''

    def get_location_value(self):
        if self.location == 'all':
            return None
        else:
            return self.location

    def get_person_value(self):
        if self.person == 'all':
            return None
        else:
            return self.person

    def get_case_status(self):
        return self.status
