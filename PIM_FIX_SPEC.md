# PIM Fix Specification
> Auto-Claude Task Specification for Frappe PIM Critical Fixes

## Task Overview
**Complexity**: COMPLEX (8+ phases)
**Estimated Sessions**: 6-10
**Priority**: CRITICAL

Fix all critical issues in the Frappe PIM application that prevent basic functionality.

---

## Acceptance Criteria

### Must Pass
- [ ] All Python files pass `python -m py_compile`
- [ ] `bench --site [site] migrate` completes without errors
- [ ] Can create PIM Attribute Type without import errors
- [ ] Can create Product Family with child tables working
- [ ] Can create Product Master (Virtual DocType functional)
- [ ] Can create Product Variant with full controller logic
- [ ] ERPNext Item ↔ Product Master sync works bidirectionally
- [ ] No duplicate field mapping definitions

### Quality Gates
- [ ] PEP 8 compliant indentation (4 spaces per level)
- [ ] All imports at top of file
- [ ] No circular imports
- [ ] Sync uses flags to prevent infinite loops
- [ ] Error handling with `frappe.log_error()`

---

## Issues to Fix (Execute in Order)

### Issue 1: pim_attribute_type.py - Missing Imports
**File**: `frappe_pim/pim/doctype/pim_attribute_type/pim_attribute_type.py`
**Problem**: `Document` and `re` not imported but used
**Fix**:
- Add `from frappe.model.document import Document`
- Add `import re`
- Verify class inherits from Document

### Issue 2: pim_attribute_type.py - Wrong Indentation
**File**: Same as above
**Problem**: Methods have 8-space indent, should be 4-space
**Fix**:
- All method definitions: 4 spaces (one level inside class)
- All method bodies: 8 spaces (two levels)
- Remove extra 4 spaces throughout entire file

### Issue 3: Missing Child Table DocTypes
**Problem**: `product_family.json` references non-existent child tables
**Create these DocTypes**:

**3a. Family Attribute Template**
- Location: `frappe_pim/pim/doctype/family_attribute_template/`
- Type: `istable = 1`
- Fields:
  - `attribute` (Link → PIM Attribute, reqd, in_list_view)
  - `required` (Check, default 0, in_list_view)
  - `default_value` (Data)
  - `sort_order` (Int, default 0)

**3b. Family Variant Attribute**
- Location: `frappe_pim/pim/doctype/family_variant_attribute/`
- Type: `istable = 1`
- Fields:
  - `attribute` (Link → PIM Attribute, reqd, in_list_view)
  - `is_required` (Check, default 1, in_list_view)
  - `level` (Int, default 1, description "Variant level 1-3")
  - `sort_order` (Int, default 0)

**3c. Product Type Field**
- Location: `frappe_pim/pim/doctype/product_type_field/`
- Type: `istable = 1`
- Fields:
  - `fieldname` (Data, reqd, in_list_view)
  - `label` (Data, reqd, in_list_view)
  - `fieldtype` (Select: Data/Int/Float/Check/Select/Link/Table/Text Editor, reqd)
  - `options` (Data, description "For Select/Link fieldtypes")
  - `reqd` (Check)
  - `default_value` (Data)
  - `sort_order` (Int, default 0)

### Issue 4: PIM Product Type - Missing Drupal-Style Fields
**File**: `frappe_pim/pim/doctype/pim_product_type/pim_product_type.json`
**Problem**: No custom fields capability
**Add fields**:
- Section Break "Type-Specific Fields"
- `type_fields` (Table → Product Type Field)
- Section Break "Allowed Families"
- `allowed_families` (Table MultiSelect → Product Family)
- Section Break "Variant Configuration"
- `allow_variants` (Check, default 1)
- `default_attribute_template` (Link → PIM Attribute Template)

### Issue 5: Product Variant Controller is Empty
**File**: `frappe_pim/pim/doctype/product_variant/product_variant.py`
**Problem**: Only contains `pass`
**Implement**:
- `validate()`: Call all validation methods
- `before_save()`: Inherit from parent, calculate completeness
- `on_update()`: Sync to ERPNext if enabled
- `inherit_from_parent()`: Copy empty fields from Product Master
- `validate_axis_values()`: Ensure axes match family config
- `validate_unique_combination()`: No duplicate axis combinations
- `validate_variant_level()`: Max 3 levels deep
- `calculate_completeness()`: Calculate completeness_score
- `sync_to_erpnext()`: Create/update Item with `_from_pim_sync` flag

### Issue 6: Product Master Field Mapping Inconsistency
**File**: `frappe_pim/pim/doctype/product_master/product_master.py`
**Problem**: Multiple inconsistent field mappings throughout file
**Fix**:
- Define `PM_TO_ITEM_MAPPING` dict at module level (line ~10)
- Define `ITEM_TO_PM_MAPPING` as reverse
- Update `load_from_db()` to use `ITEM_TO_PM_MAPPING`
- Update `db_insert()` to use `PM_TO_ITEM_MAPPING`
- Update `db_update()` to use `PM_TO_ITEM_MAPPING`
- Remove all other inline mapping definitions

**Standard Mapping**:
```
PM_TO_ITEM_MAPPING = {
    "product_name": "item_name",
    "product_code": "item_code",
    "product_family": "product_family",
    "description": "description",
    "status": "pim_status",
    "brand": "pim_brand",
    "manufacturer": "pim_manufacturer",
}
```

### Issue 7: ERPNext Custom Fields Not in Fixtures
**Problem**: Item DocType missing required PIM custom fields
**Create**: `frappe_pim/frappe_pim/fixtures/custom_field.json`
**Fields to add to Item**:
- `pim_section` (Section Break, label "PIM Information", insert_after "description")
- `pim_product_id` (Link → Product Master, read_only, insert_after "pim_section")
- `pim_family` (Link → Product Family, insert_after "pim_product_id")
- `pim_status` (Select: Draft/Active/Discontinued/Archived, insert_after "pim_family")
- `pim_column` (Column Break)
- `pim_brand` (Data, insert_after "pim_column")
- `pim_manufacturer` (Data, insert_after "pim_brand")
- `pim_last_synced` (Datetime, read_only, insert_after "pim_manufacturer")
- `pim_sync_enabled` (Check, default 1, insert_after "pim_last_synced")
- `pim_sync_direction` (Select: pim_master/erp_master/bidirectional, default "pim_master")

**Update hooks.py**:
- Ensure `fixtures` list includes Custom Field export

---

## Verification Commands

After each fix, run:
```bash
# Check Python syntax
find frappe_pim -name "*.py" -exec python -m py_compile {} \;

# Run migrations
bench --site frappe.local migrate

# Clear cache
bench --site frappe.local clear-cache

# Test in console
bench --site frappe.local console
>>> frappe.get_meta("Product Family")
>>> frappe.get_meta("Product Variant")
>>> frappe.new_doc("PIM Attribute Type")
```

---

## File Dependency Order

Execute fixes in this exact order to avoid dependency errors:

1. `pim_attribute_type.py` (imports + indentation)
2. Child table DocTypes (Family Attribute Template, Family Variant Attribute, Product Type Field)
3. `pim_product_type.json` (add type_fields reference)
4. `fixtures/custom_field.json` (ERPNext custom fields)
5. `product_master.py` (field mapping consolidation)
6. `product_variant.py` (full implementation)
7. `hooks.py` (verify fixtures export)

---

## Session Boundaries

**Session 1**: Issues 1-2 (pim_attribute_type.py fixes)
**Session 2**: Issue 3a-3b (child table DocTypes)
**Session 3**: Issue 3c + Issue 4 (Product Type Field + PIM Product Type)
**Session 4**: Issue 7 (fixtures/custom_field.json)
**Session 5**: Issue 6 (Product Master field mapping)
**Session 6**: Issue 5 (Product Variant controller)
**Session 7**: Integration testing and fixes

---

## Notes for AI Agent

- Always use 4-space indentation for Python
- Child table DocTypes MUST have `istable: 1`
- Virtual DocTypes need all required methods: `get_list`, `get_count`, `get_stats`, `load_from_db`, `db_insert`, `db_update`, `delete`
- Use `doc.flags._from_pim_sync = True` to prevent sync loops
- Test each fix before moving to next issue
- Commit after each successful fix with descriptive message
