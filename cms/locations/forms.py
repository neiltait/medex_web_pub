class LocationEditorForm:
    submit_btn_text = 'Save'

    def __init__(self, request=None):
        self.is_me_office_error = None

        if request:
            self.location_id = request.get('location_id')
            self.is_me_office = request.get('is_me_office')
        else:
            self.role = None

    @classmethod
    def load_from_location(cls, location):
        form = LocationEditorForm()
        print('load_from_location')
        print(location)
        form.location_id = location['locationId']
        form.is_me_office = location['isMeOffice']
        return form

    def is_valid(self):
        return True

    def to_dict(self):
        return {
            'locationId': self.location_id,
            'isMeOffice': self.is_me_office if self.is_me_office else False,
        }
