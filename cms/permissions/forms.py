from alerts import messages


class PermissionBuilderForm:
    submit_btn_text = 'Save'

    def __init__(self, request=None):
        self.role_error = None
        self.permission_level_error = None
        self.trust_error = None
        self.region_error = None
        self.trust_name = None

        if request:
            self.role = request.get('role')
            self.permission_level = request.get('permission_level')
            self.region = request.get('region')
            self.trust = request.get('trust')
            self.national = request.get('national')
        else:
            self.role = None
            self.permission_level = None
            self.region = None
            self.trust = None
            self.national = None


    @classmethod
    def load_from_permission(cls, permission, trust_list, region_list, national_id):
        form = PermissionBuilderForm()
        form.role = permission.role_type

        if permission.location_id == national_id:
            form.national = national_id
        elif permission.location_id in [trust.location_id for trust in trust_list]:
            trust = [trust for trust in trust_list if trust.location_id==permission.location_id][0]
            form.trust = trust.location_id
            form.trust_name = trust.name

        elif permission.location_id in [region.location_id for region in region_list]:
            form.region = permission.location_id

        return form

    def is_valid(self):

        if self.role is None or self.role == '':
            self.role_error = messages.FIELD_MISSING % "a role"

        if self.permission_level is None or self.permission_level == '':
            self.permission_level_error = messages.FIELD_MISSING % "a level"

        if self.permission_level == 'trust' and not self.trust_present():
            self.trust_error = messages.FIELD_MISSING % "a trust"

        if self.permission_level == 'regional' and not self.region_present():
            self.region_error = messages.FIELD_MISSING % "a region"

        return False if self.role_error or self.permission_level_error \
                        or self.trust_error or self.region_error else True

    def trust_present(self):
        return self.trust is not None and self.trust != '' and self.trust != 'None'

    def region_present(self):
        return self.region is not None and self.region != '' and self.region != 'None'

    def location_id(self):
        if self.region_present():
            return self.region
        elif self.trust_present():
            return self.trust
        else:
            return self.national

    def to_dict(self, user_id):
        return {
            'userId': user_id,
            'userRole': self.role,
            'locationId': self.location_id()
        }
