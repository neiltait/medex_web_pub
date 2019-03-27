class IndexFilterForm:

    def __init__(self, form_data):
        self.location = form_data.get('location')
        self.person = form_data.get('person')
