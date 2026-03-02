# PIM Project Context for Auto-Claude
> Reference document for AI agent to understand project state and requirements

## Project Identity

- **App Name**: frappe_pim
- **Framework**: Frappe v15+
- **ERP Integration**: ERPNext v15+
- **Architecture**: Drupal-style Entity/Bundle pattern
- **Database**: MariaDB 10.6+

---

## Current State: BROKEN

The PIM application has critical issues preventing basic functionality:

| Component | Status | Blocker |
|-----------|--------|---------|
| PIM Attribute Type | ❌ BROKEN | Missing imports, wrong indentation |
| Product Family | ❌ BROKEN | References non-existent child tables |
| PIM Product Type | ⚠️ INCOMPLETE | Missing custom fields capability |
| Product Master | ⚠️ PARTIAL | Inconsistent field mappings |
| Product Variant | ❌ EMPTY | Controller has only `pass` |
| ERPNext Sync | ❌ MISSING | Custom fields not in fixtures |

---

## Core Concepts

### Drupal-Style Type System
```
Configuration Entity (Type) → Content Entity (Instance)

PIM Attribute Type → PIM Attribute
PIM Product Type → Product Master
Product Family → (defines structure for) Product Master
```

### Three-Layer Architecture
```
1. CONFIGURATION LAYER (Admin manages)
   - PIM Attribute Type: Defines attribute behavior
   - PIM Product Type: Defines product classification
   - Product Family: Defines required attributes (NestedSet tree)

2. CONTENT LAYER (Users work with)
   - PIM Attribute: Actual attribute definitions
   - Product Master: Virtual DocType mapping to Item
   - Product Variant: Sellable SKUs

3. ERPNEXT LAYER (Sync target)
   - Item: Standard ERPNext item with PIM custom fields
```

### Virtual DocType Pattern

Product Master is a **Virtual DocType** that doesn't have its own database table. Instead, it maps to ERPNext Item:

```python
# Virtual DocType MUST implement:
- get_list(args)      # List view data
- get_count(args)     # Total count for pagination
- get_stats(args)     # Statistics (can return {})
- load_from_db()      # Load single record
- db_insert()         # Create new record
- db_update()         # Update existing record
- delete()            # Delete record
```

### Child Table Pattern

Child tables in Frappe MUST have:
```json
{
  "istable": 1,
  "editable_grid": 1  // Optional, for better UX
}
```

And their Python controller can be empty:
```python
class ChildTableName(Document):
    pass
```

---

## Key Files Reference

### Must Fix
| File | Issue |
|------|-------|
| `pim_attribute_type.py` | Missing imports + indentation |
| `product_variant.py` | Empty controller |
| `product_master.py` | Inconsistent mappings |

### Must Create
| File | Purpose |
|------|---------|
| `family_attribute_template/` | Child table DocType |
| `family_variant_attribute/` | Child table DocType |
| `product_type_field/` | Child table DocType |
| `fixtures/custom_field.json` | ERPNext Item custom fields |

### Must Enhance
| File | Changes Needed |
|------|---------------|
| `pim_product_type.json` | Add type_fields, allowed_families |
| `hooks.py` | Verify fixtures export |

---

## Field Mapping Standard

Use these mappings consistently throughout the codebase:

### Product Master → ERPNext Item
```python
PM_TO_ITEM_MAPPING = {
    "product_name": "item_name",
    "product_code": "item_code",
    "product_family": "product_family",  # Custom field on Item
    "description": "description",
    "status": "pim_status",              # Custom field
    "brand": "pim_brand",                # Custom field
    "manufacturer": "pim_manufacturer",  # Custom field
}
```

### ERPNext Item → Product Master
```python
ITEM_TO_PM_MAPPING = {v: k for k, v in PM_TO_ITEM_MAPPING.items()}
```

---

## Sync Flag Pattern

To prevent infinite sync loops between PIM and ERPNext:

```python
# When syncing FROM PIM to ERPNext:
item_doc.flags._from_pim_sync = True
item_doc.save()

# In Item event handler, check flag:
def on_item_update(doc, method):
    if doc.flags.get("_from_pim_sync"):
        return  # Skip - change came from PIM
    # ... sync logic
```

---

## Frappe Coding Standards

### Imports Order
```python
# 1. Standard library
import re
import json
from typing import Dict, List, Optional

# 2. Frappe
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint, flt, now

# 3. Local app
from frappe_pim.pim.utils.cache import invalidate_cache
```

### Indentation
- 4 spaces per level (NO tabs)
- Class methods: 4 spaces from class
- Method body: 8 spaces from class

### Error Handling
```python
try:
    # risky operation
except Exception as e:
    frappe.log_error(
        message=str(e),
        title="PIM: Operation Failed"
    )
    frappe.throw(_("Operation failed: {0}").format(str(e)))
```

---

## Testing Commands

```bash
# Syntax check all Python files
find frappe_pim -name "*.py" -exec python -m py_compile {} \;

# Run migrations
bench --site frappe.local migrate

# Clear cache
bench --site frappe.local clear-cache

# Console testing
bench --site frappe.local console

# Run app tests
bench --site frappe.local run-tests --app frappe_pim
```

---

## Success Criteria

After all fixes are applied:

1. ✅ `bench migrate` completes without errors
2. ✅ Can create PIM Attribute Type via UI
3. ✅ Can create Product Family with attributes and variant axes
4. ✅ Can create PIM Product Type with custom fields
5. ✅ Can create Product Master (creates underlying Item)
6. ✅ Can create Product Variant with axis values
7. ✅ Item changes sync to Product Master
8. ✅ Product Master changes sync to Item
9. ✅ No circular import errors
10. ✅ All tests pass
