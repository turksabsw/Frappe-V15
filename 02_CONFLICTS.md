# 02 - Known Conflicts and Resolution

## ⚠️ CRITICAL: Read Before Coding

This document lists all known issues in the current codebase that MUST be resolved.
When implementing, resolve these conflicts FIRST before adding new features.

---

## CONFLICT #1: Missing Imports in pim_attribute_type.py

### Problem
```python
# CURRENT (BROKEN):
import frappe
from frappe import _

class PIMAttributeType(Document):  # ❌ Document not imported
    def validate_type_code(self):
        if not re.match(r'^[a-z]...'):  # ❌ re not imported
```

### Solution
```python
# FIXED:
import frappe
from frappe import _
from frappe.model.document import Document  # ✅ Add this
import re  # ✅ Add this

class PIMAttributeType(Document):
    def validate_type_code(self):
        if not re.match(r'^[a-z]...'):
```

### Auto-Claude Command
```
Fix pim_attribute_type.py:
1. Add missing import: from frappe.model.document import Document
2. Add missing import: import re
3. Ensure class inherits from Document
```

---

## CONFLICT #2: Indentation Error in pim_attribute_type.py

### Problem
```python
class PIMAttributeType(Document):

        def validate(self):  # ❌ 8 spaces (should be 4)
            self.validate_type_code()
```

### Solution
```python
class PIMAttributeType(Document):

    def validate(self):  # ✅ 4 spaces
        self.validate_type_code()
```

### Auto-Claude Command
```
Fix indentation in pim_attribute_type.py:
- All method definitions should have 4-space indent (one level inside class)
- All method bodies should have 8-space indent (two levels)
- Remove extra 4 spaces from current indentation throughout the file
```

---

## CONFLICT #3: Missing Child Table DocTypes

### Problem
product_family.json references these child tables that don't exist:
- `Family Attribute Template` (options for family_attributes field)
- `Family Variant Attribute` (options for variant_axes field)

### Solution
Create two new child table DocTypes:

#### Family Attribute Template
```json
{
  "doctype": "DocType",
  "name": "Family Attribute Template",
  "module": "PIM",
  "istable": 1,
  "fields": [
    {"fieldname": "attribute", "fieldtype": "Link", "options": "PIM Attribute", "reqd": 1, "in_list_view": 1},
    {"fieldname": "required", "fieldtype": "Check", "default": 0, "in_list_view": 1},
    {"fieldname": "default_value", "fieldtype": "Data"},
    {"fieldname": "sort_order", "fieldtype": "Int", "default": 0}
  ]
}
```

#### Family Variant Attribute
```json
{
  "doctype": "DocType",
  "name": "Family Variant Attribute",
  "module": "PIM",
  "istable": 1,
  "fields": [
    {"fieldname": "attribute", "fieldtype": "Link", "options": "PIM Attribute", "reqd": 1, "in_list_view": 1},
    {"fieldname": "is_required", "fieldtype": "Check", "default": 1, "in_list_view": 1},
    {"fieldname": "level", "fieldtype": "Int", "default": 1, "description": "Variant level (1-3)"},
    {"fieldname": "sort_order", "fieldtype": "Int", "default": 0}
  ]
}
```

### Auto-Claude Command
```
Create missing child table DocTypes:

1. Create Family Attribute Template (istable=1):
   - attribute (Link → PIM Attribute, required)
   - required (Check)
   - default_value (Data)
   - sort_order (Int)

2. Create Family Variant Attribute (istable=1):
   - attribute (Link → PIM Attribute, required)
   - is_required (Check)
   - level (Int, 1-3)
   - sort_order (Int)

Place in: frappe_pim/pim/doctype/[name]/
Include both JSON and empty Python controller
```

---

## CONFLICT #4: PIM Product Type Missing Custom Fields Structure

### Problem
pim_product_type.json is too simple - no Drupal-style custom fields capability:
```json
// CURRENT - only basic fields
{
  "fields": [
    {"fieldname": "type_name", ...},
    {"fieldname": "type_code", ...},
    {"fieldname": "description", ...}
  ]
}
```

### Solution
Add child table for type-specific custom fields:
```json
{
  "fields": [
    // ... existing fields ...
    {
      "fieldname": "section_break_fields",
      "fieldtype": "Section Break",
      "label": "Type-Specific Fields"
    },
    {
      "fieldname": "type_fields",
      "fieldtype": "Table",
      "label": "Custom Fields",
      "options": "Product Type Field",
      "description": "Fields that will appear on products of this type"
    },
    {
      "fieldname": "section_break_families",
      "fieldtype": "Section Break",
      "label": "Allowed Families"
    },
    {
      "fieldname": "allowed_families",
      "fieldtype": "Table MultiSelect",
      "label": "Allowed Families",
      "options": "Product Family",
      "description": "Families that can use this product type"
    },
    {
      "fieldname": "section_break_variants",
      "fieldtype": "Section Break",
      "label": "Variant Configuration"
    },
    {
      "fieldname": "allow_variants",
      "fieldtype": "Check",
      "label": "Allow Variants",
      "default": 1
    },
    {
      "fieldname": "default_attribute_template",
      "fieldtype": "Link",
      "label": "Default Attribute Template",
      "options": "PIM Attribute Template"
    }
  ]
}
```

### Auto-Claude Command
```
Enhance pim_product_type.json with Drupal-style custom fields:

1. Add child table field "type_fields" (Table → Product Type Field)
2. Add "allowed_families" (Table MultiSelect → Product Family)
3. Add "allow_variants" (Check)
4. Add "default_attribute_template" (Link → PIM Attribute Template)

Create new child table DocType "Product Type Field":
- fieldname (Data, required)
- label (Data, required)
- fieldtype (Select: Data/Int/Float/Check/Select/Link/Table/Text Editor)
- options (Data, for Select/Link fieldtypes)
- reqd (Check)
- default_value (Data)
- sort_order (Int)
```

---

## CONFLICT #5: Product Variant Controller is Empty

### Problem
```python
# CURRENT product_variant.py:
class ProductVariant(Document):
    pass  # ❌ No logic at all
```

### Solution
Implement full variant controller with:
- Parent inheritance
- ERPNext sync
- Completeness calculation
- Axis value validation

### Auto-Claude Command
```
Implement product_variant.py controller:

1. Inheritance from parent_product:
   - inherit_from_parent() method
   - before_save hook to apply inheritance

2. ERPNext sync:
   - sync_to_erp() method
   - on_update hook for auto-sync
   - _from_pim_sync flag to prevent loops

3. Validation:
   - validate_axis_values() - ensure variant axes match family config
   - validate_unique_combination() - no duplicate axis combinations
   - validate_variant_level() - max 3 levels

4. Completeness:
   - calculate_completeness() method
   - before_save hook to update completeness_score

See @03_DOCTYPES_SPEC.md for full specification
```

---

## CONFLICT #6: Product Master Field Mapping Inconsistency

### Problem
product_master.py has inconsistent field mappings between Product Master and ERPNext Item:
```python
# Some places use:
"product_name": "item_name"

# Other places use:
"pim_status": "status"  # But also
"status": "pim_status"  # Reversed mapping!
```

### Solution
Create single source of truth for field mappings:

```python
# In product_master.py, define mappings once at module level:

# Product Master → Item (for saving to ERPNext)
PM_TO_ITEM_MAPPING = {
    "product_name": "item_name",
    "product_code": "item_code",
    "product_family": "item_group",  # Or custom field
    "status": "pim_status",  # Custom field on Item
    "brand": "pim_brand",  # Custom field on Item
    "manufacturer": "pim_manufacturer",  # Custom field on Item
}

# Item → Product Master (for loading from ERPNext)
ITEM_TO_PM_MAPPING = {v: k for k, v in PM_TO_ITEM_MAPPING.items()}
```

### Auto-Claude Command
```
Fix field mapping in product_master.py:

1. Define PM_TO_ITEM_MAPPING dict at module level
2. Define ITEM_TO_PM_MAPPING as reverse of above
3. Update load_from_db() to use ITEM_TO_PM_MAPPING
4. Update db_insert() and db_update() to use PM_TO_ITEM_MAPPING
5. Remove duplicate/inconsistent mapping definitions throughout file
```

---

## CONFLICT #7: ERPNext Custom Fields Not Defined

### Problem
The PIM system expects custom fields on ERPNext Item, but these aren't defined in fixtures:
- `pim_product_id`
- `pim_family`
- `pim_status`
- `pim_brand`
- `pim_manufacturer`
- `pim_last_synced`
- `pim_sync_enabled`

### Solution
Create custom fields fixture:

```json
// fixtures/custom_field.json
[
  {
    "doctype": "Custom Field",
    "dt": "Item",
    "fieldname": "pim_product_id",
    "fieldtype": "Link",
    "options": "Product Master",
    "label": "PIM Product",
    "insert_after": "item_name",
    "read_only": 1
  },
  {
    "doctype": "Custom Field",
    "dt": "Item",
    "fieldname": "pim_family",
    "fieldtype": "Link",
    "options": "Product Family",
    "label": "PIM Family",
    "insert_after": "item_group"
  },
  // ... more fields
]
```

### Auto-Claude Command
```
Create ERPNext custom fields fixture:

1. Create fixtures/custom_field.json with Item custom fields:
   - pim_product_id (Link → Product Master, read_only)
   - pim_family (Link → Product Family)
   - pim_status (Select: Draft/Active/Archived)
   - pim_brand (Data)
   - pim_manufacturer (Data)
   - pim_last_synced (Datetime, read_only)
   - pim_sync_enabled (Check, default 1)
   - pim_sync_direction (Select: pim_master/erp_master/bidirectional)

2. Update hooks.py to include fixture:
   fixtures = ["Custom Field"]
```

---

## Resolution Order

Execute conflict resolutions in this order:

1. **#1 & #2** - Fix pim_attribute_type.py (imports + indentation)
2. **#3** - Create missing child table DocTypes
3. **#4** - Enhance PIM Product Type
4. **#7** - Create ERPNext custom fields fixture
5. **#6** - Fix Product Master field mapping
6. **#5** - Implement Product Variant controller

---

## Verification Commands

After each fix, verify with:

```bash
# Check Python syntax
python -m py_compile frappe_pim/pim/doctype/*/[file].py

# Run Frappe migrate
bench --site [site] migrate

# Run tests
bench --site [site] run-tests --app frappe_pim --module frappe_pim.pim.doctype.[doctype]
```
