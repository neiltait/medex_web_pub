from django.urls import reverse


class IndexFilterForm:

    def __init__(self, query_params, defaults):
        self.location = query_params.get('location') if query_params.get('location') else defaults.get('location')
        self.person = query_params.get('person') if query_params.get('person') else defaults.get('person')
        self.case_status = query_params.get('status') if query_params.get('status') else None
        self.base_url = IndexFilterForm.get_base_url_without_status(query_params)

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
        return self.case_status

    @classmethod
    def get_base_url_without_status(cls, query_params):
        base_url = "%s?" % reverse('index')

        location_parameter = query_params.get('location')
        if location_parameter:
            base_url = "%slocation=%s&" % (base_url, location_parameter)

        person_parameter = query_params.get('person')
        if person_parameter:
            base_url = "%sperson=%s&" % (base_url, person_parameter)

        return base_url
