"""
PIM Attribute Group Controller
Manages attribute groups for organizing PIM attributes into logical categories
"""

import frappe
from frappe import _
from frappe.model.document import Document
import re


class PIMAttributeGroup(Document):
    def validate(self):
        self.validate_group_code()

    def validate_group_code(self):
        """Ensure group_code is URL-safe slug"""
        if not self.group_code:
            # Auto-generate from name
            self.group_code = frappe.scrub(self.group_name)

        # Must be lowercase, no spaces, alphanumeric with underscores
        if not re.match(r'^[a-z][a-z0-9_]*$', self.group_code):
            frappe.throw(
                _("Group Code must start with a letter and contain only lowercase letters, numbers, and underscores"),
                title=_("Invalid Group Code")
            )

    def before_save(self):
        """Prepare data before saving"""
        # Ensure sort_order is set
        if self.sort_order is None:
            self.sort_order = self.get_next_sort_order()

    def get_next_sort_order(self):
        """Get next available sort order"""
        max_order = frappe.db.sql("""
            SELECT MAX(sort_order) FROM `tabPIM Attribute Group`
        """)
        if max_order and max_order[0][0] is not None:
            return max_order[0][0] + 10
        return 10

    def on_trash(self):
        """Prevent deletion if group is in use or is standard"""
        if self.is_standard:
            frappe.throw(
                _("Standard attribute groups cannot be deleted"),
                title=_("Cannot Delete")
            )

        # Check if any attributes are using this group
        usage_count = frappe.db.count("PIM Attribute", {"attribute_group": self.name})
        if usage_count > 0:
            frappe.throw(
                _("Cannot delete attribute group '{0}' as it is used by {1} attribute(s). "
                  "Please reassign these attributes to another group first.").format(
                    self.group_name, usage_count
                ),
                title=_("Attribute Group In Use")
            )

    def on_update(self):
        """Handle post-update actions"""
        # Invalidate cache for attribute listings
        self.invalidate_cache()

    def invalidate_cache(self):
        """Clear relevant caches"""
        try:
            from frappe_pim.pim.utils.cache import invalidate_attribute_cache
            invalidate_attribute_cache(self, None)
        except ImportError:
            # Cache module may not be available
            pass


@frappe.whitelist()
def get_attribute_groups():
    """Get all attribute groups ordered by sort_order"""
    return frappe.get_all(
        "PIM Attribute Group",
        fields=["name", "group_name", "group_code", "icon", "color", "sort_order"],
        order_by="sort_order asc"
    )


@frappe.whitelist()
def get_attributes_by_group(group):
    """Get all attributes belonging to a specific group"""
    return frappe.get_all(
        "PIM Attribute",
        filters={"attribute_group": group},
        fields=[
            "name", "attribute_name", "attribute_code",
            "data_type", "is_required", "sort_order"
        ],
        order_by="sort_order asc"
    )


@frappe.whitelist()
def get_grouped_attributes():
    """Get all attributes organized by their groups"""
    groups = get_attribute_groups()
    result = []

    for group in groups:
        attributes = get_attributes_by_group(group.name)
        result.append({
            "group": group,
            "attributes": attributes
        })

    # Also include ungrouped attributes
    ungrouped = frappe.get_all(
        "PIM Attribute",
        filters={"attribute_group": ["is", "not set"]},
        fields=[
            "name", "attribute_name", "attribute_code",
            "data_type", "is_required", "sort_order"
        ],
        order_by="sort_order asc"
    )

    if ungrouped:
        result.append({
            "group": {
                "name": None,
                "group_name": _("Ungrouped"),
                "group_code": "ungrouped",
                "icon": None,
                "color": None,
                "sort_order": 9999
            },
            "attributes": ungrouped
        })

    return result


@frappe.whitelist()
def reorder_groups(order):
    """Reorder attribute groups based on provided order list

    Args:
        order: JSON string of list of group names in desired order
    """
    import json
    if isinstance(order, str):
        order = json.loads(order)

    for idx, group_name in enumerate(order):
        frappe.db.set_value(
            "PIM Attribute Group",
            group_name,
            "sort_order",
            (idx + 1) * 10,
            update_modified=False
        )

    frappe.db.commit()
    return {"success": True}
