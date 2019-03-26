from alerts import messages
from medexCms.test.utils import MedExTestCase
from permissions.forms import PermissionBuilderForm


class UsersFormsTests(MedExTestCase):

    #### PermissionBuilderForm tests

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
