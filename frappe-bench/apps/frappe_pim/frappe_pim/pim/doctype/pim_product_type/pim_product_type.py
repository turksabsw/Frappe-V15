# Copyright (c) 2024, PIM and contributors
# For license information, please see license.txt

"""
PIM Product Type Controller
Defines product types with Drupal-style custom fields and allowed families
"""

import frappe
from frappe import _
from frappe.model.document import Document
import re


class PIMProductType(Document):

    def validate(self):
        self.validate_type_code()

    def validate_type_code(self):
        """Ensure type_code is URL-safe slug"""
        if not self.type_code:
            self.type_code = frappe.scrub(self.type_name)

        if not re.match(r'^[a-z][a-z0-9_]*$', self.type_code):
            frappe.throw(
                _("Type Code must start with a letter and contain only lowercase letters, numbers, and underscores"),
                title=_("Invalid Type Code")
            )

    def before_save(self):
        """Auto-generate type_code if empty"""
        if not self.type_code:
            self.type_code = frappe.scrub(self.type_name)
