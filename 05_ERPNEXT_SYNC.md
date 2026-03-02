# 05 - ERPNext Integration Specification

## Overview

The PIM system integrates bidirectionally with ERPNext's Item DocType.
This document specifies the sync mechanism, field mapping, and conflict resolution.

---

## Architecture

```
┌──────────────────────────┐                    ┌──────────────────────────┐
│      Frappe PIM          │                    │       ERPNext            │
├──────────────────────────┤                    ├──────────────────────────┤
│                          │                    │                          │
│  Product Master          │◄──── Sync ────────►│  Item (Template)         │
│  (Virtual DocType)       │                    │  (has_variants=1)        │
│                          │                    │                          │
│  Product Variant         │◄──── Sync ────────►│  Item (Variant)          │
│  (Normal DocType)        │                    │  (variant_of=parent)     │
│                          │                    │                          │
└──────────────────────────┘                    └──────────────────────────┘
```

---

## Custom Fields on ERPNext Item

These custom fields MUST be added to Item DocType via fixtures:

```json
// fixtures/custom_field.json
[
  {
    "doctype": "Custom Field",
    "dt": "Item",
    "fieldname": "pim_section",
    "fieldtype": "Section Break",
    "label": "PIM Integration",
    "insert_after": "description",
    "collapsible": 1
  },
  {
    "doctype": "Custom Field",
    "dt": "Item",
    "fieldname": "pim_product_id",
    "fieldtype": "Data",
    "label": "PIM Product ID",
    "insert_after": "pim_section",
    "read_only": 1,
    "description": "Linked Product Master or Product Variant name"
  },
  {
    "doctype": "Custom Field",
    "dt": "Item",
    "fieldname": "pim_product_type",
    "fieldtype": "Select",
    "label": "PIM Product Type",
    "insert_after": "pim_product_id",
    "options": "Product Master\nProduct Variant",
    "read_only": 1
  },
  {
    "doctype": "Custom Field",
    "dt": "Item",
    "fieldname": "pim_family",
    "fieldtype": "Link",
    "label": "PIM Family",
    "options": "Product Family",
    "insert_after": "pim_product_type"
  },
  {
    "doctype": "Custom Field",
    "dt": "Item",
    "fieldname": "pim_status",
    "fieldtype": "Select",
    "label": "PIM Status",
    "options": "\nDraft\nIn Review\nApproved\nPublished\nArchived",
    "insert_after": "pim_family"
  },
  {
    "doctype": "Custom Field",
    "dt": "Item",
    "fieldname": "pim_column_break",
    "fieldtype": "Column Break",
    "insert_after": "pim_status"
  },
  {
    "doctype": "Custom Field",
    "dt": "Item",
    "fieldname": "pim_sync_enabled",
    "fieldtype": "Check",
    "label": "PIM Sync Enabled",
    "default": "1",
    "insert_after": "pim_column_break"
  },
  {
    "doctype": "Custom Field",
    "dt": "Item",
    "fieldname": "pim_sync_direction",
    "fieldtype": "Select",
    "label": "Sync Direction",
    "options": "PIM Master\nERP Master\nBidirectional",
    "default": "Bidirectional",
    "insert_after": "pim_sync_enabled"
  },
  {
    "doctype": "Custom Field",
    "dt": "Item",
    "fieldname": "pim_last_synced",
    "fieldtype": "Datetime",
    "label": "Last PIM Sync",
    "read_only": 1,
    "insert_after": "pim_sync_direction"
  },
  {
    "doctype": "Custom Field",
    "dt": "Item",
    "fieldname": "pim_sync_status",
    "fieldtype": "Select",
    "label": "Sync Status",
    "options": "\nSynced\nPending\nConflict\nError",
    "read_only": 1,
    "insert_after": "pim_last_synced"
  }
]
```

---

## Field Mapping

### Product Master → Item

| Product Master Field | Item Field | Notes |
|---------------------|------------|-------|
| product_code | item_code | Primary key |
| product_name | item_name | |
| product_family | item_group | May need mapping logic |
| product_family | pim_family | Direct link |
| status | pim_status | Custom field |
| description | description | |
| brand | brand | Standard field |
| is_template | has_variants | |
| - | pim_product_id | Set to product_code |
| - | pim_product_type | Set to "Product Master" |

### Product Variant → Item

| Product Variant Field | Item Field | Notes |
|----------------------|------------|-------|
| variant_code | item_code | Primary key (SKU) |
| variant_name | item_name | |
| product_master.product_code | variant_of | Parent item |
| product_master.product_family | item_group | |
| status | pim_status | Custom field |
| barcode | barcodes[0].barcode | Child table |
| - | pim_product_id | Set to variant_code |
| - | pim_product_type | Set to "Product Variant" |

---

## Sync Implementation

### hooks.py Configuration

```python
# hooks.py

doc_events = {
    "Product Master": {
        "on_update": "frappe_pim.pim.sync.on_product_master_update",
        "on_trash": "frappe_pim.pim.sync.on_product_master_delete"
    },
    "Product Variant": {
        "on_update": "frappe_pim.pim.sync.on_product_variant_update",
        "on_trash": "frappe_pim.pim.sync.on_product_variant_delete"
    },
    "Item": {
        "on_update": "frappe_pim.pim.sync.on_item_update",
    }
}

fixtures = [
    {"dt": "Custom Field", "filters": [["dt", "=", "Item"], ["fieldname", "like", "pim_%"]]}
]
```

### Sync Module

```python
# frappe_pim/pim/sync.py

import frappe
from frappe import _
from frappe.utils import now_datetime
from typing import Optional


# ============================================================================
# SYNC FLAGS - Prevent infinite loops
# ============================================================================

def is_from_pim_sync(doc) -> bool:
    """Check if this update originated from PIM sync"""
    return getattr(doc, '_from_pim_sync', False) or \
           getattr(doc.flags, 'from_pim_sync', False)


def is_from_erp_sync(doc) -> bool:
    """Check if this update originated from ERP sync"""
    return getattr(doc, '_from_erp_sync', False) or \
           getattr(doc.flags, 'from_erp_sync', False)


def set_pim_sync_flag(doc):
    """Mark document as originating from PIM sync"""
    doc._from_pim_sync = True
    doc.flags.from_pim_sync = True


def set_erp_sync_flag(doc):
    """Mark document as originating from ERP sync"""
    doc._from_erp_sync = True
    doc.flags.from_erp_sync = True


# ============================================================================
# PIM → ERPNEXT SYNC
# ============================================================================

def on_product_master_update(doc, method=None):
    """Sync Product Master to ERPNext Item"""
    if is_from_erp_sync(doc):
        return
    
    if not doc.sync_to_erp:
        return
    
    sync_product_master_to_item(doc)


def sync_product_master_to_item(product):
    """Create or update ERPNext Item from Product Master"""
    item_code = product.product_code
    
    if frappe.db.exists("Item", item_code):
        item = frappe.get_doc("Item", item_code)
        set_pim_sync_flag(item)
    else:
        item = frappe.new_doc("Item")
        set_pim_sync_flag(item)
        item.item_code = item_code
    
    # Map fields
    item.item_name = product.product_name
    item.description = product.description
    item.has_variants = 1 if product.is_template else 0
    
    # Map to item_group (may need custom mapping)
    if product.product_family:
        # Option 1: Use family code as item_group
        # item.item_group = product.product_family
        
        # Option 2: Map to existing item_group or create
        item.item_group = get_or_create_item_group(product.product_family)
    
    # PIM custom fields
    item.pim_product_id = product.name
    item.pim_product_type = "Product Master"
    item.pim_family = product.product_family
    item.pim_status = product.status
    item.pim_last_synced = now_datetime()
    item.pim_sync_status = "Synced"
    
    # Set defaults if new
    if not item.name:
        item.stock_uom = frappe.db.get_single_value("Stock Settings", "stock_uom") or "Nos"
        item.is_stock_item = 1
    
    try:
        item.flags.ignore_permissions = True
        item.save()
        
        # Update Product Master with Item link
        if product.erp_item != item.name:
            frappe.db.set_value("Product Master", product.name, {
                "erp_item": item.name,
                "last_erp_sync": now_datetime()
            }, update_modified=False)
        
        frappe.db.commit()
        
    except Exception as e:
        frappe.log_error(
            f"Failed to sync Product Master {product.name} to Item: {str(e)}",
            "PIM Sync Error"
        )
        frappe.db.set_value("Product Master", product.name, {
            "erp_sync_status": "Sync Failed"
        }, update_modified=False)


def on_product_variant_update(doc, method=None):
    """Sync Product Variant to ERPNext Item"""
    if is_from_erp_sync(doc):
        return
    
    if not doc.sync_to_erp:
        return
    
    sync_product_variant_to_item(doc)


def sync_product_variant_to_item(variant):
    """Create or update ERPNext Item from Product Variant"""
    item_code = variant.variant_code
    
    if frappe.db.exists("Item", item_code):
        item = frappe.get_doc("Item", item_code)
        set_pim_sync_flag(item)
    else:
        item = frappe.new_doc("Item")
        set_pim_sync_flag(item)
        item.item_code = item_code
    
    # Get parent item code
    parent_item_code = None
    if variant.product_master:
        parent_item_code = frappe.db.get_value(
            "Product Master", variant.product_master, "product_code"
        )
    
    # Map fields
    item.item_name = variant.variant_name
    item.variant_of = parent_item_code
    
    # PIM custom fields
    item.pim_product_id = variant.name
    item.pim_product_type = "Product Variant"
    item.pim_status = variant.status
    item.pim_last_synced = now_datetime()
    item.pim_sync_status = "Synced"
    
    # Set defaults if new
    if not item.name:
        item.stock_uom = frappe.db.get_single_value("Stock Settings", "stock_uom") or "Nos"
        item.is_stock_item = 1
    
    # Map variant attributes to Item Variant Attributes
    if variant.axis_values and parent_item_code:
        item.attributes = []
        for axis in variant.axis_values:
            attr = frappe.get_doc("PIM Attribute", axis.attribute)
            option = frappe.get_doc("PIM Attribute Option", axis.option)
            
            item.append("attributes", {
                "attribute": attr.attribute_name,
                "attribute_value": option.label
            })
    
    try:
        item.flags.ignore_permissions = True
        item.save()
        
        # Update Product Variant with Item link
        frappe.db.set_value("Product Variant", variant.name, {
            "erp_item": item.name,
            "last_erp_sync": now_datetime(),
            "erp_sync_status": "Synced"
        }, update_modified=False)
        
        frappe.db.commit()
        
    except Exception as e:
        frappe.log_error(
            f"Failed to sync Product Variant {variant.name} to Item: {str(e)}",
            "PIM Sync Error"
        )
        frappe.db.set_value("Product Variant", variant.name, {
            "erp_sync_status": "Sync Failed"
        }, update_modified=False)


# ============================================================================
# ERPNEXT → PIM SYNC
# ============================================================================

def on_item_update(doc, method=None):
    """Sync ERPNext Item changes back to PIM"""
    if is_from_pim_sync(doc):
        return
    
    if not doc.pim_sync_enabled:
        return
    
    if doc.pim_sync_direction == "PIM Master":
        # PIM is master, don't sync back
        return
    
    if doc.pim_product_type == "Product Master":
        sync_item_to_product_master(doc)
    elif doc.pim_product_type == "Product Variant":
        sync_item_to_product_variant(doc)


def sync_item_to_product_master(item):
    """Update Product Master from ERPNext Item"""
    if not item.pim_product_id:
        return
    
    if not frappe.db.exists("Product Master", item.pim_product_id):
        return
    
    product = frappe.get_doc("Product Master", item.pim_product_id)
    set_erp_sync_flag(product)
    
    # Check for conflicts
    if should_check_conflict(item, product):
        conflict = detect_conflict(item, product)
        if conflict:
            handle_conflict(item, product, conflict)
            return
    
    # Map fields back
    product.product_name = item.item_name
    product.description = item.description
    
    try:
        product.flags.ignore_permissions = True
        product.save()
        
        frappe.db.set_value("Item", item.name, {
            "pim_last_synced": now_datetime(),
            "pim_sync_status": "Synced"
        }, update_modified=False)
        
    except Exception as e:
        frappe.log_error(
            f"Failed to sync Item {item.name} to Product Master: {str(e)}",
            "PIM Sync Error"
        )


def sync_item_to_product_variant(item):
    """Update Product Variant from ERPNext Item"""
    if not item.pim_product_id:
        return
    
    if not frappe.db.exists("Product Variant", item.pim_product_id):
        return
    
    variant = frappe.get_doc("Product Variant", item.pim_product_id)
    set_erp_sync_flag(variant)
    
    # Map fields back
    variant.variant_name = item.item_name
    
    try:
        variant.flags.ignore_permissions = True
        variant.save()
        
    except Exception as e:
        frappe.log_error(
            f"Failed to sync Item {item.name} to Product Variant: {str(e)}",
            "PIM Sync Error"
        )


# ============================================================================
# CONFLICT DETECTION & RESOLUTION
# ============================================================================

def should_check_conflict(item, product) -> bool:
    """Determine if conflict check is needed"""
    if not item.pim_last_synced:
        return False
    return item.pim_sync_direction == "Bidirectional"


def detect_conflict(item, product) -> Optional[dict]:
    """Detect if both sides changed since last sync"""
    last_sync = item.pim_last_synced
    
    item_modified_after_sync = item.modified > last_sync
    product_modified_after_sync = product.modified > last_sync
    
    if item_modified_after_sync and product_modified_after_sync:
        return {
            "item_modified": item.modified,
            "product_modified": product.modified,
            "last_sync": last_sync,
            "fields_in_conflict": find_conflicting_fields(item, product)
        }
    
    return None


def find_conflicting_fields(item, product) -> list:
    """Find which fields have different values"""
    conflicts = []
    
    field_mapping = {
        "item_name": "product_name",
        "description": "description"
    }
    
    for item_field, product_field in field_mapping.items():
        item_val = getattr(item, item_field, None)
        product_val = getattr(product, product_field, None)
        
        if item_val != product_val:
            conflicts.append({
                "field": item_field,
                "item_value": item_val,
                "product_value": product_val
            })
    
    return conflicts


def handle_conflict(item, product, conflict):
    """Handle sync conflict based on configuration"""
    # Mark as conflict for manual resolution
    frappe.db.set_value("Item", item.name, {
        "pim_sync_status": "Conflict"
    }, update_modified=False)
    
    # Log conflict for admin review
    frappe.log_error(
        f"Sync conflict detected:\n"
        f"Item: {item.name}\n"
        f"Product: {product.name}\n"
        f"Conflict details: {conflict}",
        "PIM Sync Conflict"
    )
    
    # Optionally notify admin
    # frappe.sendmail(...)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_or_create_item_group(family_name: str) -> str:
    """Get or create Item Group from Product Family"""
    family = frappe.get_doc("Product Family", family_name)
    
    # Check if item_group with same name exists
    if frappe.db.exists("Item Group", family.family_name):
        return family.family_name
    
    # Create new item_group
    item_group = frappe.new_doc("Item Group")
    item_group.item_group_name = family.family_name
    
    # Set parent if family has parent
    if family.parent_family:
        parent_family = frappe.get_doc("Product Family", family.parent_family)
        if frappe.db.exists("Item Group", parent_family.family_name):
            item_group.parent_item_group = parent_family.family_name
        else:
            item_group.parent_item_group = "All Item Groups"
    else:
        item_group.parent_item_group = "All Item Groups"
    
    item_group.insert(ignore_permissions=True)
    return item_group.name


def on_product_master_delete(doc, method=None):
    """Handle Product Master deletion"""
    # Option 1: Delete linked Item
    # frappe.delete_doc("Item", doc.erp_item, force=1)
    
    # Option 2: Just unlink
    if doc.erp_item and frappe.db.exists("Item", doc.erp_item):
        frappe.db.set_value("Item", doc.erp_item, {
            "pim_product_id": None,
            "pim_sync_status": None
        })


def on_product_variant_delete(doc, method=None):
    """Handle Product Variant deletion"""
    if doc.erp_item and frappe.db.exists("Item", doc.erp_item):
        frappe.db.set_value("Item", doc.erp_item, {
            "pim_product_id": None,
            "pim_sync_status": None
        })
```

---

## Testing Sync

```python
# Test sync from PIM to ERPNext
product = frappe.get_doc("Product Master", "PROD-001")
product.product_name = "Test Product Updated"
product.save()  # Should auto-sync to Item

# Verify
item = frappe.get_doc("Item", "PROD-001")
assert item.item_name == "Test Product Updated"
assert item.pim_sync_status == "Synced"

# Test sync from ERPNext to PIM
item.item_name = "Changed in ERPNext"
item.save()  # Should auto-sync back to Product Master

product.reload()
assert product.product_name == "Changed in ERPNext"
```
