# Copyright (c) 2023, Frappe x FOSSUnited and Contributors
# See license.txt

import uuid

import frappe
from frappe.tests.utils import FrappeTestCase


class TestFOSSUserProfile(FrappeTestCase):
    def test_add_profile(self):
        # Given a user that does not have a FOSSUnitedProfile
        inserted_username = "wisharya"
        inserted_name = "wish arya"
        profiles_metadata = frappe.get_all(
            doctype="FOSS User Profile",
            filters={"username": inserted_username},
        )
        self.assertEqual(profiles_metadata, [])

        # When a FOSSUnitedProfile is created for the user
        # Note that a Frappe User needs to exist before a Profile can be created
        # Verify that only required values are provided below
        frappe_user = frappe.get_doc(
            {
                "doctype": "User",
                "username": inserted_username,
                # Create a unique email address as it is used as a database key
                "email": str(uuid.uuid4()) + "@fossunited.org",
                "first_name": "wish",
                "name": inserted_name,
                "full_name": inserted_name,
            },
        )
        frappe_user.db_insert()
        profile = frappe.get_doc(
            {
                "doctype": "FOSS User Profile",
                "user": frappe_user.name,
                "username": frappe_user.username,
                "is_published": 1,
            },
        )
        profile.db_insert()
        inserted_name = profile.name

        # Then verify that the Profile has been stored as expected
        profiles_metadata = frappe.get_all(
            doctype="FOSS User Profile",
            filters={"username": inserted_username},
        )
        self.assertEqual(profiles_metadata, [{"name": inserted_name}])
