# 06 - Implementation Guide

## Overview

This guide provides step-by-step instructions for implementing the PIM system.
Follow the phases in order - each phase builds on the previous.

---

## Phase 0: Fix Existing Conflicts (MUST DO FIRST)

Before implementing new features, resolve all existing conflicts documented in @02_CONFLICTS.md.

### Step 0.1: Fix pim_attribute_type.py
```bash
# Navigate to the file
cd frappe_pim/pim/doctype/pim_attribute_type/

# Fix the imports and indentation
# See @02_CONFLICTS.md for exact changes needed
```

**Checklist:**
- [ ] Add `from frappe.model.document import Document`
- [ ] Add `import re`
- [ ] Fix indentation (8 spaces → 4 spaces for methods)
- [ ] Test: `python -m py_compile pim_attribute_type.py`

### Step 0.2: Create Missing Child Tables
Create these DocTypes (see @04_CHILD_TABLES.md for full specifications):

**Checklist:**
- [ ] Create `Family Attribute Template` (istable=1)
- [ ] Create `Family Variant Attribute` (istable=1)
- [ ] Create `Product Type Field` (istable=1)
- [ ] Create `Product Attribute Value` (istable=1)
- [ ] Create `Variant Axis Value` (istable=1)
- [ ] Create `Product Media` (istable=1)
- [ ] Run `bench migrate`

### Step 0.3: Update PIM Product Type
Add Drupal-style custom fields capability:

**Checklist:**
- [ ] Add `type_fields` Table field (→ Product Type Field)
- [ ] Add `allowed_families` Table MultiSelect (→ Product Family)
- [ ] Add `allow_variants` Check field
- [ ] Add `default_attribute_template` Link field
- [ ] Update Python controller
- [ ] Run `bench migrate`

---

## Phase 1: Core Configuration DocTypes

### Step 1.1: PIM Attribute Type (Complete)
Verify the DocType is working:

```bash
bench --site [site] console
>>> attr_type = frappe.get_doc({"doctype": "PIM Attribute Type", "type_name": "Text", "type_code": "text", "base_type": "String"})
>>> attr_type.insert()
```

**Test Checklist:**
- [ ] Can create attribute types
- [ ] Validation works (type_code format)
- [ ] Standard types are protected from deletion

### Step 1.2: PIM Attribute Group
Simple grouping DocType for organizing attributes.

```json
{
  "name": "PIM Attribute Group",
  "fields": [
    {"fieldname": "group_name", "fieldtype": "Data", "reqd": 1},
    {"fieldname": "group_code", "fieldtype": "Data", "unique": 1},
    {"fieldname": "sort_order", "fieldtype": "Int", "default": 0},
    {"fieldname": "parent_group", "fieldtype": "Link", "options": "PIM Attribute Group"}
  ]
}
```

**Checklist:**
- [ ] Create/update DocType JSON
- [ ] Create Python controller
- [ ] Test CRUD operations

### Step 1.3: PIM Attribute Template
Template for reusable attribute sets.

**Checklist:**
- [ ] Verify DocType exists and is correct
- [ ] Has child table for template attributes
- [ ] Test creating template with multiple attributes

---

## Phase 2: Product Family (NestedSet)

### Step 2.1: Verify Tree Structure
```bash
bench --site [site] console
>>> from frappe.utils.nestedset import rebuild_tree
>>> rebuild_tree("Product Family", "parent_family")
```

**Checklist:**
- [ ] Tree view works in Frappe UI
- [ ] lft/rgt values are correctly populated
- [ ] is_group/is_leaf flags work correctly
- [ ] full_path is auto-generated

### Step 2.2: Implement Attribute Inheritance
Add method to get inherited attributes from ancestors:

```python
def get_all_attributes(self):
    """Get family_attributes + inherited from ancestors"""
    all_attrs = []
    
    # Get ancestors using lft/rgt
    ancestors = frappe.get_all("Product Family",
        filters={"lft": ["<", self.lft], "rgt": [">", self.rgt]},
        fields=["name"],
        order_by="lft")
    
    # Collect attributes from ancestors (inherited)
    for ancestor in ancestors:
        ancestor_doc = frappe.get_doc("Product Family", ancestor.name)
        for attr in ancestor_doc.family_attributes:
            all_attrs.append({
                **attr.as_dict(),
                "inherited": True,
                "inherited_from": ancestor.name
            })
    
    # Add own attributes
    for attr in self.family_attributes:
        all_attrs.append({
            **attr.as_dict(),
            "inherited": False
        })
    
    return all_attrs
```

**Checklist:**
- [ ] get_all_attributes() returns inherited + own attributes
- [ ] get_variant_axes() returns allowed variant attributes
- [ ] Attribute inheritance marked correctly

---

## Phase 3: PIM Attribute with Options

### Step 3.1: Create PIM Attribute
```bash
bench --site [site] console
>>> attr = frappe.get_doc({
...     "doctype": "PIM Attribute",
...     "attribute_name": "Color",
...     "attribute_code": "color",
...     "attribute_type": "select",
...     "is_variant_axis": 1
... })
>>> attr.insert()
```

### Step 3.2: Add Options to Attribute
```python
attr.append("options", {
    "option_code": "red",
    "label": "Red",
    "color_hex": "#FF0000",
    "sort_order": 1
})
attr.append("options", {
    "option_code": "blue",
    "label": "Blue",
    "color_hex": "#0000FF",
    "sort_order": 2
})
attr.save()
```

**Checklist:**
- [ ] Can create attributes with different types
- [ ] Options work for Select/Multi Select types
- [ ] is_variant_axis flag works
- [ ] Validation based on attribute_type

---

## Phase 4: Product Master (Virtual DocType)

### Step 4.1: Verify Virtual DocType Protocol
The following methods MUST be implemented:

```python
class ProductMaster(Document):
    @staticmethod
    def get_list(args) -> list: ...
    
    @staticmethod  
    def get_count(args) -> int: ...
    
    @staticmethod
    def get_stats(args) -> dict: ...
    
    def load_from_db(self): ...
    def db_insert(self, ignore_if_duplicate=False): ...
    def db_update(self): ...
    def delete(self): ...
```

**Checklist:**
- [ ] All required methods implemented
- [ ] List view works
- [ ] Single view works
- [ ] Create operation works
- [ ] Update operation works
- [ ] Delete operation works

### Step 4.2: Fix Field Mapping
Implement consistent field mapping (see @02_CONFLICTS.md #6):

**Checklist:**
- [ ] PM_TO_ITEM_MAPPING defined once
- [ ] ITEM_TO_PM_MAPPING is reverse of above
- [ ] All methods use these mappings consistently

### Step 4.3: Implement Attribute Values
```python
def set_attribute_value(self, attribute_code, value):
    """Set an attribute value (EAV pattern)"""
    # Find existing or create new
    for attr_val in self.attribute_values:
        if attr_val.attribute == attribute_code:
            self._set_typed_value(attr_val, value)
            return
    
    # Create new
    self.append("attribute_values", {
        "attribute": attribute_code,
        # ... set value based on type
    })

def get_attribute_value(self, attribute_code):
    """Get an attribute value"""
    for attr_val in self.attribute_values:
        if attr_val.attribute == attribute_code:
            return self._get_typed_value(attr_val)
    return None
```

**Checklist:**
- [ ] Can set/get attribute values
- [ ] Values typed correctly based on attribute type
- [ ] Child table saves correctly

---

## Phase 5: Product Variant

### Step 5.1: Implement Full Controller
Replace empty `pass` with full implementation:

```python
class ProductVariant(Document):
    def validate(self):
        self.validate_product_master()
        self.validate_axis_values()
        self.validate_unique_combination()
        self.calculate_variant_level()
    
    def before_save(self):
        self.inherit_from_parent()
        self.generate_variant_name()
        self.calculate_completeness()
    
    def on_update(self):
        if self.sync_to_erp and not getattr(self, '_from_erp_sync', False):
            self.sync_to_erpnext()
    
    # ... implement all methods
```

**Checklist:**
- [ ] validate_product_master() - ensure parent exists
- [ ] validate_axis_values() - ensure valid axes
- [ ] validate_unique_combination() - no duplicate variants
- [ ] inherit_from_parent() - copy empty fields
- [ ] calculate_completeness() - percentage score
- [ ] sync_to_erpnext() - create/update Item

### Step 5.2: Multi-Level Variants
Support up to 3 variant levels:

```
Product Master: "T-Shirt"
└── Level 1: "T-Shirt - Red" (axis: color)
    └── Level 2: "T-Shirt - Red - M" (axis: size)
```

**Checklist:**
- [ ] parent_variant field links variants
- [ ] variant_level calculated correctly
- [ ] Max 3 levels enforced
- [ ] Inheritance follows chain

---

## Phase 6: ERPNext Integration

### Step 6.1: Install Custom Fields
```bash
bench --site [site] migrate
# Custom fields should be created from fixtures
```

Verify manually:
```bash
bench --site [site] console
>>> frappe.get_meta("Item").get_field("pim_product_id")
```

**Checklist:**
- [ ] All pim_* fields exist on Item
- [ ] Fields appear in correct section
- [ ] Default values set correctly

### Step 6.2: Implement Sync Module
Create `frappe_pim/pim/sync.py` with full implementation from @05_ERPNEXT_SYNC.md.

**Checklist:**
- [ ] sync.py created with all functions
- [ ] hooks.py configured with doc_events
- [ ] Sync flags prevent infinite loops
- [ ] Error handling in place

### Step 6.3: Test Sync
```python
# Create product in PIM
product = frappe.get_doc({
    "doctype": "Product Master",
    "product_name": "Test Product",
    "product_code": "TEST-001",
    "product_family": "...",
    "product_type": "...",
    "sync_to_erp": 1
})
product.insert()

# Verify Item created
item = frappe.get_doc("Item", "TEST-001")
assert item.item_name == "Test Product"
assert item.pim_product_id == "TEST-001"
```

**Checklist:**
- [ ] PIM → ERPNext sync works
- [ ] ERPNext → PIM sync works
- [ ] Conflict detection works
- [ ] Delete handling works

---

## Phase 7: Quality & Testing

### Step 7.1: Unit Tests
Create tests for each DocType:

```python
# test_product_family.py
def test_attribute_inheritance():
    # Create parent family with attributes
    parent = create_test_family("Parent")
    parent.append("family_attributes", {"attribute": "color", "required": 1})
    parent.save()
    
    # Create child family
    child = create_test_family("Child", parent_family=parent.name)
    child.save()
    
    # Verify inheritance
    all_attrs = child.get_all_attributes()
    assert len(all_attrs) >= 1
    assert any(a["attribute"] == "color" and a["inherited"] for a in all_attrs)
```

**Checklist:**
- [ ] Tests for Product Family tree operations
- [ ] Tests for attribute inheritance
- [ ] Tests for Product Master CRUD
- [ ] Tests for Product Variant generation
- [ ] Tests for ERPNext sync

### Step 7.2: Integration Tests
Test full workflows:

**Checklist:**
- [ ] Create complete product with variants
- [ ] Verify ERPNext Items created
- [ ] Test completeness calculation
- [ ] Test data consistency

---

## Verification Commands

After each phase, run:

```bash
# Check for Python syntax errors
find frappe_pim -name "*.py" -exec python -m py_compile {} \;

# Run migrations
bench --site [site] migrate

# Clear cache
bench --site [site] clear-cache

# Run tests
bench --site [site] run-tests --app frappe_pim

# Check for broken DocTypes
bench --site [site] console
>>> frappe.get_meta("Product Family")  # Should not error
>>> frappe.get_meta("Product Master")
>>> frappe.get_meta("Product Variant")
```

---

## Auto-Claude Execution Order

When using Auto-Claude, execute prompts in this order:

1. `@CLAUDE.md` - Load project context
2. `@02_CONFLICTS.md` - Fix existing issues first
3. `@04_CHILD_TABLES.md` - Create missing child tables
4. `@03_DOCTYPES_SPEC.md` - Implement/fix DocTypes
5. `@05_ERPNEXT_SYNC.md` - Setup integration
6. `@06_IMPLEMENTATION.md` - Verify each phase

Each prompt should be self-contained and atomic.
