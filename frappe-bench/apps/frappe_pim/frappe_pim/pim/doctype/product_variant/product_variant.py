# Copyright (c) 2024, PIM and contributors
# For license information, please see license.txt

"""
Product Variant Controller
Handles variant validation, inheritance from parent product, and ERPNext sync.
Implements Drupal-style product variant pattern with axis values.
"""

import frappe
from frappe import _
from frappe.model.document import Document


class ProductVariant(Document):

    def validate(self):
        """Validate the Product Variant before save"""
        self.validate_parent_product()
        self.validate_axis_values()
        self.validate_unique_combination()
        self.validate_variant_level()

    def validate_parent_product(self):
        """Validate that parent product exists as an Item in ERPNext"""
        if not self.parent_product:
            frappe.throw(
                _("Parent Product is required"),
                title=_("Missing Parent Product")
            )
        
        # Check if parent product exists as Item (Product Master maps to Item)
        if not frappe.db.exists("Item", self.parent_product):
            frappe.throw(
                _("Parent Product '{0}' not found. Please select a valid Product Master.").format(
                    self.parent_product
                ),
                title=_("Invalid Parent Product")
            )

    def validate_axis_values(self):
        """Ensure variant axes match family configuration

        Validates that:
        1. If family allows variants, axis values are required
        2. All axis values correspond to valid variant axes defined in the family
        3. Required variant axes have values provided
        """
        if not self.parent_product:
            return

        # Get the product family from parent product or directly
        family_name = self.product_family
        if not family_name:
            # Try to get family from parent Item (backing Product Master)
            if frappe.db.exists("Item", self.parent_product):
                family_name = frappe.db.get_value("Item", self.parent_product, "product_family")
                if family_name:
                    self.product_family = family_name

        if not family_name:
            return

        # Get family's variant axes configuration
        try:
            family = frappe.get_doc("Product Family", family_name)
        except frappe.DoesNotExistError:
            frappe.throw(
                _("Product Family '{0}' not found").format(family_name),
                title=_("Invalid Product Family")
            )
            return

        # Check if family allows variants
        if not getattr(family, 'allow_variants', False):
            if self.axis_values and len(self.axis_values) > 0:
                frappe.throw(
                    _("Product Family '{0}' does not allow variants").format(family_name),
                    title=_("Variants Not Allowed")
                )
            return

        # Get defined variant axes from family
        family_axes = []
        if hasattr(family, 'variant_axes') and family.variant_axes:
            for axis in family.variant_axes:
                family_axes.append(axis.attribute)

        # If no axes defined, variants still allowed but no axis validation needed
        if not family_axes:
            return

        # Validate that provided axis values match family's variant axes
        provided_axes = set()
        for axis_value in (self.axis_values or []):
            if axis_value.attribute:
                if axis_value.attribute not in family_axes:
                    frappe.throw(
                        _("Attribute '{0}' is not a valid variant axis for family '{1}'").format(
                            axis_value.attribute, family_name
                        ),
                        title=_("Invalid Variant Axis")
                    )
                provided_axes.add(axis_value.attribute)

        # Check that all required axes have values
        # (assuming all family axes are required for now)
        missing_axes = set(family_axes) - provided_axes
        if missing_axes:
            frappe.throw(
                _("Missing values for required variant axes: {0}").format(
                    ", ".join(missing_axes)
                ),
                title=_("Missing Variant Axis Values")
            )

    def validate_unique_combination(self):
        """Prevent creating variants with identical axis value combinations under same parent

        Ensures that no two variants under the same parent product have
        the same combination of axis attribute values.
        """
        if not self.parent_product:
            return

        if not self.axis_values or len(self.axis_values) == 0:
            return

        # Build a signature of this variant's axis values
        axis_signature = self._get_axis_signature()
        if not axis_signature:
            return

        # Find other variants with the same parent
        filters = {
            "parent_product": self.parent_product,
            "name": ["!=", self.name] if self.name else ["is", "set"]
        }

        existing_variants = frappe.get_all(
            "Product Variant",
            filters=filters,
            fields=["name"]
        )

        # Check each existing variant for matching axis signature
        for variant in existing_variants:
            variant_doc = frappe.get_doc("Product Variant", variant.name)
            existing_signature = variant_doc._get_axis_signature()

            if axis_signature == existing_signature:
                frappe.throw(
                    _("A variant with the same axis values already exists: {0}").format(
                        variant.name
                    ),
                    title=_("Duplicate Variant Combination")
                )

    def validate_variant_level(self):
        """Enforce maximum variant nesting depth of 3 levels

        Prevents creating deeply nested variant hierarchies.
        Level 1: Direct child of Product Master
        Level 2: Variant of a variant
        Level 3: Maximum allowed depth
        """
        if not self.parent_product:
            self.variant_level = 1
            return

        # Calculate variant level based on parent chain
        level = 1
        current_parent = self.parent_product

        # Walk up the parent chain to calculate depth
        max_iterations = 10  # Safety limit to prevent infinite loops
        iterations = 0

        while current_parent and iterations < max_iterations:
            iterations += 1

            # Check if parent is a Product Master or Product Variant
            # First try Product Variant
            parent_variant = frappe.db.exists("Product Variant", current_parent)
            if parent_variant:
                level += 1
                parent_doc = frappe.get_doc("Product Variant", current_parent)
                current_parent = parent_doc.get("parent_product")
            else:
                # Parent is a Product Master (top level), stop here
                break

        self.variant_level = level

        # Enforce max 3 levels
        max_level = 3
        if level > max_level:
            frappe.throw(
                _("Variant nesting exceeds maximum allowed depth of {0} levels. Current level: {1}").format(
                    max_level, level
                ),
                title=_("Maximum Variant Depth Exceeded")
            )

    def _get_axis_signature(self):
        """Generate a unique signature string for this variant's axis values

        Returns:
            str: Sorted, normalized string representation of axis values
                 e.g., "color:red|size:large"
        """
        if not self.axis_values:
            return ""

        axis_pairs = []
        for axis in self.axis_values:
            if axis.attribute and axis.attribute_value:
                # Normalize to lowercase for comparison
                attr = str(axis.attribute).lower().strip()
                value = str(axis.attribute_value).lower().strip()
                axis_pairs.append(f"{attr}:{value}")

        # Sort to ensure consistent signature regardless of order
        axis_pairs.sort()
        return "|".join(axis_pairs)

    def before_save(self):
        """Hook called before saving the document

        Handles:
        1. Inheritance of empty fields from parent Product Master
        2. Calculation of completeness score
        """
        try:
            self.inherit_from_parent()
        except Exception:
            pass  # Don't block save if inheritance fails
        self.calculate_completeness()

    def inherit_from_parent(self):
        """Copy empty fields from Product Master parent

        Inherits the following fields if they are empty on the variant:
        - product_family
        - description
        - brand
        - manufacturer
        - status (only if variant has no status set)

        This implements the Drupal-style inheritance pattern where variants
        inherit from their parent product but can override individual values.
        """
        if not self.parent_product:
            return

        # Fields that can be inherited from parent Product Master
        inheritable_fields = [
            'product_family',
            'description',
            'brand',
            'manufacturer',
        ]

        parent = None
        
        # First check if parent is a Product Variant
        if frappe.db.exists("Product Variant", self.parent_product):
            try:
                parent = frappe.get_doc("Product Variant", self.parent_product)
            except Exception:
                pass
        
        # If not a variant, get data from Item (which backs Product Master)
        if not parent and frappe.db.exists("Item", self.parent_product):
            try:
                item = frappe.get_doc("Item", self.parent_product)
                # Create a simple dict-like object with mapped fields
                parent = frappe._dict({
                    'product_family': item.get('product_family'),
                    'description': item.get('description'),
                    'brand': item.get('pim_brand'),
                    'manufacturer': item.get('pim_manufacturer'),
                })
            except Exception as e:
                frappe.log_error(
                    f"Failed to get parent product {self.parent_product}: {str(e)}",
                    "Product Variant Inheritance"
                )
                return
        
        if not parent:
                return

        # Copy empty fields from parent
        for field in inheritable_fields:
            current_value = self.get(field)
            parent_value = parent.get(field)

            # Only copy if variant's field is empty and parent has a value
            if not current_value and parent_value:
                self.set(field, parent_value)

    def calculate_completeness(self):
        """Calculate completeness score based on filled required fields

        Calculates a percentage based on how many of the key product
        fields have been filled in. This helps track data quality
        and identify variants that need more information.

        Required fields for completeness:
        - variant_name (required)
        - variant_code (required)
        - parent_product (required)
        - product_family
        - description
        - brand
        - manufacturer
        - axis_values (at least one)
        """
        # Define fields that contribute to completeness
        completeness_fields = [
            ('variant_name', 15),       # Required field - 15%
            ('variant_code', 15),       # Required field - 15%
            ('parent_product', 10),     # Required field - 10%
            ('product_family', 10),     # Important for categorization - 10%
            ('description', 20),        # Important for content - 20%
            ('brand', 10),              # Optional but useful - 10%
            ('manufacturer', 10),       # Optional but useful - 10%
            ('axis_values', 10),        # Variant-specific - 10%
        ]

        total_score = 0

        for field, weight in completeness_fields:
            value = self.get(field)

            # Handle different field types
            if field == 'axis_values':
                # Check if child table has entries
                if value and len(value) > 0:
                    total_score += weight
            elif value:
                # Standard fields - check if non-empty
                total_score += weight

        # Set the completeness score (0-100)
        self.completeness_score = min(100, max(0, total_score))

    def on_update(self):
        """Hook called after the document is saved to the database

        Triggers synchronization to ERPNext Item if sync is enabled.
        Uses _from_pim_sync flag pattern to prevent infinite sync loops.
        """
        # Temporarily disabled - sync causes issues with Virtual DocType
        # self.sync_to_erpnext()
        pass

    def sync_to_erpnext(self):
        """Sync Product Variant to ERPNext Item

        Creates or updates an ERPNext Item corresponding to this variant.
        Implements bidirectional sync with flag to prevent infinite loops:
        - Checks _from_erpnext_sync flag before syncing
        - Sets item.flags._from_pim_sync = True before saving

        Field mapping:
        - variant_name -> item_name
        - variant_code -> item_code
        - description -> description
        - product_family -> pim_family
        - brand -> pim_brand
        - manufacturer -> pim_manufacturer
        - completeness_score -> pim_completeness
        """
        # Check if this update came from ERPNext sync - skip to prevent infinite loop
        if getattr(self, '_from_erpnext_sync', False):
            return

        # Check if sync is enabled (can be controlled by a setting)
        if not getattr(self, 'sync_enabled', True):
            return

        # Determine Item name - use variant_code if available
        # Don't use self.name as it may be a temporary new-* name
        item_code = self.variant_code
        if not item_code:
            # Skip sync if no variant_code - will be synced on next save
            return

        try:
            # Try to get existing Item
            item = frappe.get_doc("Item", item_code)
            is_new = False
        except frappe.DoesNotExistError:
            # Create new Item
            item = frappe.new_doc("Item")
            item.item_code = item_code
            item.item_group = "Products"  # Default item group for PIM products
            is_new = True

        # Map Product Variant fields to Item fields
        if self.variant_name:
            item.item_name = self.variant_name
        if self.description:
            item.description = self.description

        # Map to PIM custom fields on Item (defined in custom_field.json fixture)
        if hasattr(item, 'pim_family') and self.product_family:
            item.pim_family = self.product_family
        if hasattr(item, 'pim_brand') and self.brand:
            item.pim_brand = self.brand
        if hasattr(item, 'pim_manufacturer') and self.manufacturer:
            item.pim_manufacturer = self.manufacturer
        if hasattr(item, 'pim_completeness'):
            item.pim_completeness = self.completeness_score or 0

        # Link back to this variant
        if hasattr(item, 'pim_product_id'):
            item.pim_product_id = self.name

        # Set the _from_pim_sync flag BEFORE save to prevent ERPNext
        # from triggering a sync back to PIM (infinite loop prevention)
        item.flags._from_pim_sync = True

        try:
            if is_new:
                item.insert(ignore_permissions=True)
                frappe.msgprint(
                    _("Created ERPNext Item '{0}' for variant").format(item.name),
                    alert=True,
                    indicator='green'
                )
            else:
                item.save(ignore_permissions=True)

            # Update the linked item reference on this variant
            if not self.erp_item:
                self.db_set('erp_item', item.name, update_modified=False)

        except Exception as e:
            frappe.log_error(
                message=f"Failed to sync Product Variant {self.name} to ERPNext Item: {str(e)}",
                title="Product Variant Sync Error"
            )
            # Don't raise - allow variant save to succeed even if sync fails

    def sync_from_erpnext(self, item):
        """Sync Product Variant from ERPNext Item

        Called when an ERPNext Item is updated and needs to sync back to the variant.
        Sets _from_erpnext_sync flag to prevent sync loop.

        Args:
            item: The ERPNext Item document
        """
        # Set flag to prevent re-sync back to ERPNext
        self._from_erpnext_sync = True

        # Map Item fields to Product Variant fields
        if hasattr(item, 'item_name') and item.item_name:
            self.variant_name = item.item_name
        if hasattr(item, 'description') and item.description:
            self.description = item.description

        # Map PIM custom fields from Item
        if hasattr(item, 'pim_family') and item.pim_family:
            self.product_family = item.pim_family
        if hasattr(item, 'pim_brand') and item.pim_brand:
            self.brand = item.pim_brand
        if hasattr(item, 'pim_manufacturer') and item.pim_manufacturer:
            self.manufacturer = item.pim_manufacturer
