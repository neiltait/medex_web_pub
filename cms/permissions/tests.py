from alerts import messages
from medexCms.api import enums
from medexCms.test.mocks import PermissionMocks
from medexCms.test.utils import MedExTestCase

from permissions.forms import PermissionBuilderForm
from permissions.models import Permission


class PermissionModelsTests(MedExTestCase):

    # Permission tests
    def test_correctly_sets_values_on_init(self):
        permission = Permission(PermissionMocks.get_meo_permission_dict())
        self.assertEqual(permission.user_id, PermissionMocks.get_meo_permission_dict()['userId'])
        self.assertEqual(permission.permission_id, PermissionMocks.get_meo_permission_dict()['permissionId'])
        self.assertEqual(permission.location_id, PermissionMocks.get_meo_permission_dict()['locationId'])
        self.assertEqual(permission.user_role, PermissionMocks.get_meo_permission_dict()['userRole'])

    def test_correctly_sets_values_from_enum_role_values(self):
        me_permission = Permission(PermissionMocks.get_me_permission_dict())
        meo_permission = Permission(PermissionMocks.get_meo_permission_dict())

        self.assertEqual(me_permission.role_type, enums.roles.ME)
        self.assertEqual(meo_permission.role_type, enums.roles.MEO)

    def test_correctly_sets_values_from_legacy_values(self):
        me_legacy = Permission(PermissionMocks.get_legacy_me_permission_dict())
        meo_legacy = Permission(PermissionMocks.get_legacy_meo_permission_dict())

        self.assertEqual(me_legacy.role_type, enums.roles.ME)
        self.assertEqual(meo_legacy.role_type, enums.roles.MEO)


class PermissionsFormsTests(MedExTestCase):

    # PermissionBuilderForm tests
    def test_is_valid_returns_false_when_no_role_given(self):
        form_content = {
            'role': None,
            'permission_level': 'national',
            'region': None,
            'trust': None
        }
        form = PermissionBuilderForm(form_content)
        result = form.is_valid()
        self.assertIsFalse(result)
        self.assertEqual(form.role_error, messages.FIELD_MISSING % "a role")

    def test_is_valid_returns_false_when_no_level_given(self):
        form_content = {
            'role': 'me',
            'permission_level': None,
            'region': None,
            'trust': None
        }
        form = PermissionBuilderForm(form_content)
        result = form.is_valid()
        self.assertIsFalse(result)
        self.assertEqual(form.permission_level_error, messages.FIELD_MISSING % "a level")

    def test_is_valid_returns_false_when_no_trust_given_for_a_trust_level_permission(self):
        form_content = {
            'role': 'me',
            'permission_level': 'trust',
            'region': None,
            'trust': None
        }
        form = PermissionBuilderForm(form_content)
        result = form.is_valid()
        self.assertIsFalse(result)
        self.assertEqual(form.trust_error, messages.FIELD_MISSING % "a trust")

    def test_is_valid_returns_false_when_no_region_given_for_a_region_level_permission(self):
        form_content = {
            'role': 'me',
            'permission_level': 'regional',
            'region': None,
            'trust': None
        }
        form = PermissionBuilderForm(form_content)
        result = form.is_valid()
        self.assertIsFalse(result)
        self.assertEqual(form.region_error, messages.FIELD_MISSING % "a region")

    def test_is_valid_returns_false_when_no_role_or_level_given(self):
        form_content = {
            'role': None,
            'permission_level': None,
            'region': None,
            'trust': None
        }
        form = PermissionBuilderForm(form_content)
        result = form.is_valid()
        self.assertIsFalse(result)
        self.assertEqual(form.role_error, messages.FIELD_MISSING % "a role")
        self.assertEqual(form.permission_level_error, messages.FIELD_MISSING % "a level")

    def test_is_valid_returns_true_when_role_at_national_level_given_with_no_locations(self):
        form_content = {
            'role': 'me',
            'permission_level': 'national',
            'region': None,
            'trust': None
        }
        form = PermissionBuilderForm(form_content)
        result = form.is_valid()
        self.assertIsTrue(result)
        self.assertEqual(form.role_error, None)
        self.assertEqual(form.permission_level_error, None)
        self.assertEqual(form.region_error, None)
        self.assertEqual(form.trust_error, None)

    def test_is_valid_returns_true_when_role_at_regional_level_given_with_region_given(self):
        form_content = {
            'role': 'meo',
            'permission_level': 'regional',
            'region': '1',
            'trust': None
        }
        form = PermissionBuilderForm(form_content)
        result = form.is_valid()
        self.assertIsTrue(result)
        self.assertEqual(form.role_error, None)
        self.assertEqual(form.permission_level_error, None)
        self.assertEqual(form.region_error, None)
        self.assertEqual(form.trust_error, None)

    def test_is_valid_returns_true_when_role_at_trust_level_given_with_trust_given(self):
        form_content = {
            'role': 'sa',
            'permission_level': 'trust',
            'region': None,
            'trust': '1'
        }
        form = PermissionBuilderForm(form_content)
        result = form.is_valid()
        self.assertIsTrue(result)
        self.assertEqual(form.role_error, None)
        self.assertEqual(form.permission_level_error, None)
        self.assertEqual(form.region_error, None)
        self.assertEqual(form.trust_error, None)

    def test_to_dict_returns_form_fields_as_a_dict(self):
        role = 'sa'
        level = 'trust'
        trust = '1'
        form_content = {
            'role': role,
            'permission_level': level,
            'region': None,
            'trust': trust
        }
        user_id = 1
        form = PermissionBuilderForm(form_content)
        result = form.to_dict(user_id)
        self.assertEqual(result['userRole'], role)
        self.assertEqual(result['locationId'], trust)
        self.assertEqual(result['userId'], user_id)

    def test_trust_present_returns_false_when_a_trust_is_not_present(self):
        form_content = {
            'role': 'meo',
            'permission_level': 'regional',
            'region': '1',
            'trust': None
        }
        form = PermissionBuilderForm(form_content)

        self.assertIsNone(form.trust)
        self.assertIsFalse(form.trust_present())

        form.trust = ''
        self.assertEqual(form.trust, '')
        self.assertIsFalse(form.trust_present())

        form.trust = 'None'
        self.assertEqual(form.trust, 'None')
        self.assertIsFalse(form.trust_present())

    def test_trust_present_returns_true_when_a_trust_is_present(self):
        form_content = {
            'role': 'meo',
            'permission_level': 'trust',
            'region': None,
            'trust': '1'
        }
        form = PermissionBuilderForm(form_content)

        self.assertEqual(form.trust, form_content['trust'])
        self.assertIsTrue(form.trust_present())

    def test_region_present_returns_false_when_a_region_is_not_present(self):
        form_content = {
            'role': 'meo',
            'permission_level': 'trust',
            'region': None,
            'trust': '1'
        }
        form = PermissionBuilderForm(form_content)

        self.assertIsNone(form.region)
        self.assertIsFalse(form.region_present())

        form.region = ''
        self.assertEqual(form.region, '')
        self.assertIsFalse(form.region_present())

        form.region = 'None'
        self.assertEqual(form.region, 'None')
        self.assertIsFalse(form.region_present())

    def test_region_present_returns_true_when_a_region_is_present(self):
        form_content = {
            'role': 'meo',
            'permission_level': 'regional',
            'region': '1',
            'trust': None
        }
        form = PermissionBuilderForm(form_content)

        self.assertEqual(form.region, form_content['region'])
        self.assertIsTrue(form.region_present())

    def test_location_id_returns_the_region_id_if_its_present(self):
        form_content = {
            'role': 'meo',
            'permission_level': 'regional',
            'region': '1',
            'trust': None
        }
        form = PermissionBuilderForm(form_content)
        self.assertEqual(form.region, form_content['region'])
        self.assertEqual(form.location_id(), form.region)

    def test_location_id_returns_the_trust_id_if_its_present(self):
        form_content = {
            'role': 'meo',
            'permission_level': 'trust',
            'region': None,
            'trust': '2'
        }
        form = PermissionBuilderForm(form_content)
        self.assertEqual(form.trust, form_content['trust'])
        self.assertEqual(form.location_id(), form.trust)

    def test_location_id_returns_none_if_no_trust_or_region_present(self):
        form_content = {
            'role': 'meo',
            'permission_level': 'national',
            'region': None,
            'trust': None
        }
        form = PermissionBuilderForm(form_content)
        self.assertIsNone(form.region)
        self.assertIsNone(form.trust)
        self.assertIsNone(form.location_id())

    def test_permission_level_uses_permission_level_if_multiple_values_present_and_regional_level_specified(self):
        form_content = {
            'role': 'meo',
            'permission_level': 'regional',
            'region': 'region_id',
            'trust': 'trust_id'
        }
        form = PermissionBuilderForm(form_content)
        self.assertEqual(form.location_id(), 'region_id')

    def test_permission_level_uses_permission_level_if_multiple_values_present_and_trust_level_specified(self):
        form_content = {
            'role': 'meo',
            'permission_level': 'trust',
            'region': 'region_id',
            'trust': 'trust_id'
        }
        form = PermissionBuilderForm(form_content)
        self.assertEqual(form.location_id(), 'trust_id')
