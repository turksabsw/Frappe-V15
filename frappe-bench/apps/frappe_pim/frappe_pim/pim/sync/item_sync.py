# Copyright (c) 2024, Your Company and contributors
# For license information, please see license.txt

"""
Item Sync Module

Handles bidirectional synchronization between ERPNext Item and PIM Product Master.

This module provides event handlers for Item document events to ensure
that changes made to Items in ERPNext are reflected in Product Master.

The sync uses flags to prevent infinite loops:
- _from_pim_sync: Set by Product Master/Variant when modifying an Item
- from_pim: Set by erp_sync.py utility when creating/updating Items
- _from_variant_generation: Set during variant generation
- _from_erpnext_sync: Set by this module when syncing to Product Master
"""

import frappe
from frappe import _
from frappe.utils import cstr


def _is_from_pim(doc):
    """
    Check if this document operation originated from PIM.

    Checks multiple flag names for compatibility:
    - _from_pim_sync: Set by Product Master and Product Variant controllers
    - from_pim: Set by erp_sync.py utility functions and queue processor

    Args:
        doc: The document to check

    Returns:
        bool: True if operation originated from PIM
    """
    return (
        getattr(doc.flags, "_from_pim_sync", False)
        or getattr(doc.flags, "from_pim", False)
    )


def on_item_update(doc, method=None):
    """
    Handle Item on_update event.

    Syncs Item changes to Product Master if the Item was not updated
    from PIM (to prevent infinite loops).

    Args:
        doc: The Item document being updated
        method: The method name (unused, required by Frappe hooks)
    """
    # Skip if this update originated from PIM sync
    # Check both flag names: _from_pim_sync (set by Product Master/Variant)
    # and from_pim (set by erp_sync.py utility)
    if _is_from_pim(doc):
        return

    # Skip if this is a variant being created by PIM
    if getattr(doc.flags, "_from_variant_generation", False):
        return

    # Check if this Item has PIM data (was created/managed by PIM)
    if not _is_pim_managed_item(doc):
        return

    try:
        _sync_item_to_product_master(doc)
    except Exception as e:
        # Log error but don't block the Item save
        frappe.log_error(
            message=f"Failed to sync Item {doc.name} to Product Master: {str(e)}",
            title="PIM Sync Error"
        )


def on_item_insert(doc, method=None):
    """
    Handle Item after_insert event.

    If an Item is created directly in ERPNext (not via PIM), we may want
    to create a corresponding Product Master record or ignore it based
    on configuration.

    Args:
        doc: The Item document being inserted
        method: The method name (unused, required by Frappe hooks)
    """
    # Skip if this insert originated from PIM sync
    if _is_from_pim(doc):
        return

    # Skip if this is a variant being created by PIM
    if getattr(doc.flags, "_from_variant_generation", False):
        return

    # For now, we don't auto-create Product Master for new Items
    # This could be enabled via a setting in the future
    # _create_product_master_for_item(doc)

    # Just log for debugging purposes in development
    frappe.logger("pim_sync").debug(
        f"New Item {doc.name} created outside PIM"
    )


def on_item_trash(doc, method=None):
    """
    Handle Item on_trash event.

    When an Item is deleted, we need to handle the associated Product Master
    child tables. Since Product Master is a Virtual DocType, deleting the Item
    effectively deletes the Product Master too.

    Args:
        doc: The Item document being deleted
        method: The method name (unused, required by Frappe hooks)
    """
    # Skip if this delete originated from PIM sync
    if _is_from_pim(doc):
        return

    # Check if this Item has PIM data
    if not _is_pim_managed_item(doc):
        return

    try:
        _cleanup_product_master_data(doc.name)
    except Exception as e:
        # Log error but don't block the Item delete
        frappe.log_error(
            message=f"Failed to cleanup Product Master data for Item {doc.name}: {str(e)}",
            title="PIM Cleanup Error"
        )


def _is_pim_managed_item(doc):
    """
    Check if an Item is managed by PIM.

    An Item is considered PIM-managed if it has any PIM custom fields set,
    or if it has associated Product Master child table data.

    Args:
        doc: The Item document

    Returns:
        bool: True if PIM-managed, False otherwise
    """
    # Check for PIM custom fields
    pim_fields = [
        "custom_pim_sku",
        "custom_pim_status",
        "custom_pim_lifecycle_stage",
        "custom_pim_parent_product",
    ]

    for field in pim_fields:
        value = doc.get(field)
        if value:
            return True

    # Check for associated child table data
    child_tables = [
        "Product Media",
        "Product Attribute Value",
        "Product Price Item",
        "Product Channel",
        "Product Relation",
        "Product Supplier Item",
        "Product Certification Item",
        "Product Translation Item",
    ]

    for dt in child_tables:
        try:
            count = frappe.db.count(
                dt,
                {"parent": doc.name, "parenttype": "Product Master"}
            )
            if count > 0:
                return True
        except Exception:
            # Table might not exist
            pass

    return False


def _sync_item_to_product_master(item_doc):
    """
    Sync Item changes to Product Master.

    Since Product Master is a Virtual DocType that reads from Item,
    this function mainly ensures that any computed fields are updated
    and triggers any necessary events.

    Args:
        item_doc: The Item document
    """
    # Import the mapping from product_master module
    from frappe_pim.pim.doctype.product_master.product_master import (
        ITEM_TO_PM_MAPPING
    )

    # Log the sync for debugging
    frappe.logger("pim_sync").debug(
        f"Syncing Item {item_doc.name} changes to Product Master"
    )

    # If there are webhooks or notifications configured for Product Master,
    # we might want to trigger them here
    # For now, we just ensure the data is consistent

    # Update any cached data if caching is enabled
    cache_key = f"product_master_{item_doc.name}"
    frappe.cache().delete_value(cache_key)

    # Trigger after_change event for any listeners
    frappe.publish_realtime(
        "product_master_changed",
        {"product": item_doc.name},
        doctype="Product Master",
        docname=item_doc.name
    )


def _cleanup_product_master_data(item_name):
    """
    Clean up Product Master child table data when an Item is deleted.

    Since Product Master is a Virtual DocType, the "document" itself
    doesn't exist in the database. But the child tables do have their
    own records that need to be cleaned up.

    Args:
        item_name: The name of the Item being deleted
    """
    child_tables = [
        "Product Media",
        "Product Attribute Value",
        "Product Price Item",
        "Product Channel",
        "Product Relation",
        "Product Supplier Item",
        "Product Certification Item",
        "Product Translation Item",
    ]

    for dt in child_tables:
        try:
            frappe.db.delete(
                dt,
                {"parent": item_name, "parenttype": "Product Master"}
            )
            frappe.logger("pim_sync").debug(
                f"Cleaned up {dt} records for {item_name}"
            )
        except Exception as e:
            frappe.logger("pim_sync").warning(
                f"Could not clean up {dt} for {item_name}: {str(e)}"
            )

    # Clear any cached data
    cache_key = f"product_master_{item_name}"
    frappe.cache().delete_value(cache_key)

    frappe.logger("pim_sync").info(
        f"Cleaned up Product Master data for deleted Item {item_name}"
    )


def _create_product_master_for_item(item_doc):
    """
    Create a basic Product Master entry for an Item created outside PIM.

    This is a placeholder function that could be enabled via configuration
    to auto-create Product Master records for new Items.

    Args:
        item_doc: The Item document
    """
    # This function is not currently active
    # It would set basic PIM fields on the Item
    pass


# Utility function for manual sync trigger
@frappe.whitelist()
def sync_item_to_pim(item_name):
    """
    Manually trigger sync of an Item to Product Master.

    This can be called from a button or script to force sync
    an Item's changes to the PIM system.

    Args:
        item_name: The name of the Item to sync

    Returns:
        dict: Status of the sync operation
    """
    if not item_name:
        frappe.throw(_("Item name is required"))

    if not frappe.db.exists("Item", item_name):
        frappe.throw(_("Item {0} does not exist").format(item_name))

    item_doc = frappe.get_doc("Item", item_name)

    try:
        _sync_item_to_product_master(item_doc)
        return {
            "success": True,
            "message": _("Item {0} synced to PIM successfully").format(item_name)
        }
    except Exception as e:
        frappe.log_error(
            message=str(e),
            title=f"Manual PIM Sync Error for {item_name}"
        )
        return {
            "success": False,
            "message": _("Failed to sync: {0}").format(str(e))
        }


@frappe.whitelist()
def bulk_sync_items_to_pim(item_names):
    """
    Bulk sync multiple Items to Product Master.

    Args:
        item_names: List of Item names or JSON string of list

    Returns:
        dict: Summary of sync results
    """
    import json

    if isinstance(item_names, str):
        item_names = json.loads(item_names)

    if not item_names:
        frappe.throw(_("No items provided"))

    results = {
        "success": [],
        "failed": []
    }

    for item_name in item_names:
        result = sync_item_to_pim(item_name)
        if result.get("success"):
            results["success"].append(item_name)
        else:
            results["failed"].append({
                "item": item_name,
                "error": result.get("message")
            })

    return {
        "total": len(item_names),
        "synced": len(results["success"]),
        "failed": len(results["failed"]),
        "details": results
    }
