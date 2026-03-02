"""
PIM Attribute Controller
Manages attribute definitions for the PIM system
"""

import frappe
from frappe import _
from frappe.model.document import Document
import re


class PIMAttribute(Document):
    def validate(self):
        self.validate_attribute_code()
        self.validate_options()
        self.validate_linked_doctype()
        self.validate_value_constraints()

    def validate_attribute_code(self):
        """Ensure attribute_code is URL-safe slug"""
        if not self.attribute_code:
            # Auto-generate from name
            self.attribute_code = frappe.scrub(self.attribute_name)
        
        # Must be lowercase, no spaces, alphanumeric with underscores
        if not re.match(r'^[a-z][a-z0-9_]*$', self.attribute_code):
            frappe.throw(
                _("Attribute Code must start with a letter and contain only lowercase letters, numbers, and underscores"),
                title=_("Invalid Attribute Code")
            )

    def validate_options(self):
        """Validate options for Select/Multi Select types"""
        if self.data_type in ['Select', 'Multi Select']:
            # Options can be defined here OR via PIM Attribute Option DocType
            # So we don't require options to be set here
            if self.options:
                # Clean and deduplicate options if provided
                options_list = [opt.strip() for opt in self.options.split(',') if opt.strip()]
                if len(options_list) != len(set(options_list)):
                    frappe.throw(
                        _("Duplicate options found. Each option must be unique."),
                        title=_("Duplicate Options")
                    )
                self.options = ', '.join(options_list)

    def validate_linked_doctype(self):
        """Ensure linked_doctype is set for Link type"""
        if self.data_type == 'Link' and not self.linked_doctype:
            frappe.throw(
                _("Linked DocType is required for Link data type"),
                title=_("Missing Linked DocType")
            )

    def validate_value_constraints(self):
        """Validate min/max value constraints"""
        if self.data_type in ['Integer', 'Float']:
            if self.min_value is not None and self.max_value is not None:
                if self.min_value > self.max_value:
                    frappe.throw(
                        _("Minimum value cannot be greater than maximum value"),
                        title=_("Invalid Constraints")
                    )

    def before_save(self):
        """Clean up fields based on data type"""
        # Clear irrelevant fields based on data type
        if self.data_type not in ['Select', 'Multi Select']:
            self.options = None
        
        if self.data_type != 'Link':
            self.linked_doctype = None
        
        if self.data_type not in ['Integer', 'Float']:
            self.min_value = None
            self.max_value = None
            self.value_prefix = None
            self.value_suffix = None
        
        if self.data_type not in ['Text', 'Long Text']:
            self.max_length = None

    def on_trash(self):
        """Prevent deletion if attribute is in use"""
        if self.is_standard:
            frappe.throw(
                _("Standard attributes cannot be deleted"),
                title=_("Cannot Delete")
            )
        
        # Check if attribute is used in any product
        usage_count = frappe.db.count("Product Attribute Value", {"attribute": self.name})
        if usage_count > 0:
            frappe.throw(
                _("Cannot delete attribute '{0}' as it is used in {1} product(s)").format(
                    self.attribute_name, usage_count
                ),
                title=_("Attribute In Use")
            )

    def get_parsed_options(self):
        """Return options as a list - combines inline options and PIM Attribute Option records"""
        options = []
        
        # Get inline options (comma-separated in options field)
        if self.options:
            options.extend([opt.strip() for opt in self.options.split(',') if opt.strip()])
        
        # Get options from PIM Attribute Option DocType
        try:
            attribute_options = frappe.get_all(
                "PIM Attribute Option",
                filters={"attribute": self.name, "is_active": 1},
                fields=["option_value"],
                order_by="sort_order"
            )
            for opt in attribute_options:
                if opt.option_value and opt.option_value not in options:
                    options.append(opt.option_value)
        except Exception:
            pass  # Table may not exist yet
        
        return options


@frappe.whitelist()
def get_attribute_options(attribute):
    """Get options for a Select/Multi Select attribute"""
    doc = frappe.get_doc("PIM Attribute", attribute)
    return {
        "data_type": doc.data_type,
        "options": doc.get_parsed_options(),
        "linked_doctype": doc.linked_doctype,
        "is_required": doc.is_required
    }


@frappe.whitelist()
def validate_attribute_value(attribute, value):
    """Validate a value against attribute constraints"""
    doc = frappe.get_doc("PIM Attribute", attribute)
    errors = []
    
    # Required check
    if doc.is_required and not value:
        errors.append(_("Value is required"))
        return {"valid": False, "errors": errors}
    
    if not value:
        return {"valid": True, "errors": []}
    
    # Type-specific validation
    if doc.data_type in ['Select', 'Multi Select']:
        valid_options = doc.get_parsed_options()
        if doc.data_type == 'Select':
            if value not in valid_options:
                errors.append(_("Invalid option: {0}").format(value))
        else:
            values = [v.strip() for v in value.split(',')]
            invalid = [v for v in values if v not in valid_options]
            if invalid:
                errors.append(_("Invalid options: {0}").format(', '.join(invalid)))
    
    elif doc.data_type == 'Integer':
        try:
            int_val = int(value)
            if doc.min_value is not None and int_val < doc.min_value:
                errors.append(_("Value must be at least {0}").format(doc.min_value))
            if doc.max_value is not None and int_val > doc.max_value:
                errors.append(_("Value must be at most {0}").format(doc.max_value))
        except ValueError:
            errors.append(_("Value must be an integer"))
    
    elif doc.data_type == 'Float':
        try:
            float_val = float(value)
            if doc.min_value is not None and float_val < doc.min_value:
                errors.append(_("Value must be at least {0}").format(doc.min_value))
            if doc.max_value is not None and float_val > doc.max_value:
                errors.append(_("Value must be at most {0}").format(doc.max_value))
        except ValueError:
            errors.append(_("Value must be a number"))
    
    elif doc.data_type in ['Text', 'Long Text']:
        if doc.max_length and len(str(value)) > doc.max_length:
            errors.append(_("Value exceeds maximum length of {0}").format(doc.max_length))
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
