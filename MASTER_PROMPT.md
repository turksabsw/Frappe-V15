# Frappe PIM - Master Implementation Prompt

## 🎯 Mission
Implement a production-ready Product Information Management (PIM) system for Frappe Framework v15+ with full ERPNext integration using Drupal-style entity/type architecture.

---

## 📋 Context Files (Reference with @)

Load these files in Auto-Claude for complete context:

| File | Purpose | When to Use |
|------|---------|-------------|
| @CLAUDE.md | Project overview, tech stack, coding standards | Always load first |
| @01_ARCHITECTURE.md | System design, entity relationships, data flow | Understanding the big picture |
| @02_CONFLICTS.md | Known bugs and fixes | **MUST FIX FIRST** before any new work |
| @03_DOCTYPES_SPEC.md | Complete DocType specifications | When creating/modifying DocTypes |
| @04_CHILD_TABLES.md | Child table definitions | When child tables are missing |
| @05_ERPNEXT_SYNC.md | ERPNext integration code | When implementing sync |
| @06_IMPLEMENTATION.md | Step-by-step guide | Following implementation phases |

---

## 🚨 CRITICAL: Fix Conflicts First

Before ANY new development, resolve existing conflicts:

```
@02_CONFLICTS.md contains 7 critical issues that MUST be fixed:

1. pim_attribute_type.py - Missing imports (Document, re) and wrong indentation
2. pim_attribute_type.py - 8-space indent should be 4-space
3. Missing child tables - Family Attribute Template, Family Variant Attribute
4. PIM Product Type - No Drupal-style custom fields structure
5. Product Variant - Empty controller (just "pass")
6. Product Master - Inconsistent field mapping
7. ERPNext custom fields - Not defined in fixtures
```

**Auto-Claude Command:**
```
Read @02_CONFLICTS.md and fix ALL 7 conflicts in order.
For each conflict:
1. Show the current broken code
2. Show the fixed code
3. Apply the fix
4. Verify with syntax check
```

---

## 🏗️ Architecture Summary

### Drupal-Style Type System
```
Every entity has a TYPE that defines its structure:

PIM Product Type ──defines fields for──► Product Master
PIM Attribute Type ──defines behavior of──► PIM Attribute
Product Family ──defines required attrs for──► Products in family
```

### Key Distinctions
```
Product Family = WHAT data to collect (attribute structure)
Product Type = HOW product behaves (classification, business rules)
Category = WHERE product appears (navigation, merchandising)
```

### ERPNext Mapping
```
Product Master (Virtual) ←→ ERPNext Item (Template)
Product Variant ←→ ERPNext Item (Variant)
Bidirectional sync with conflict detection
```

---

## 📦 DocTypes to Implement/Fix

### Configuration Layer (Types)
- [x] PIM Attribute Type - needs import/indent fixes
- [ ] PIM Product Type - needs custom fields structure
- [ ] PIM Attribute Group - simple grouping
- [ ] PIM Attribute Template - reusable attribute sets

### Content Layer (Entities)
- [ ] Product Family (NestedSet) - needs child tables
- [ ] Product Master (Virtual) - needs field mapping fix
- [ ] Product Variant - needs full implementation
- [ ] PIM Attribute - needs options child table

### Child Tables (istable=1)
- [ ] Family Attribute Template
- [ ] Family Variant Attribute  
- [ ] Product Type Field
- [ ] Product Attribute Value
- [ ] Variant Axis Value
- [ ] PIM Attribute Option
- [ ] Product Media

---

## 🔄 Implementation Phases

### Phase 0: Fix Conflicts (Required)
```
Load: @02_CONFLICTS.md
Do: Fix all 7 conflicts
Verify: `python -m py_compile` passes for all files
```

### Phase 1: Child Tables
```
Load: @04_CHILD_TABLES.md
Do: Create all missing child table DocTypes
Verify: `bench migrate` succeeds
```

### Phase 2: Configuration DocTypes
```
Load: @03_DOCTYPES_SPEC.md (sections 1-2)
Do: Fix PIM Attribute Type, enhance PIM Product Type
Verify: Can create types with custom fields
```

### Phase 3: Product Family
```
Load: @03_DOCTYPES_SPEC.md (section 3)
Do: Implement attribute inheritance
Verify: Tree view works, inheritance correct
```

### Phase 4: Product Master & Variant
```
Load: @03_DOCTYPES_SPEC.md (sections 4-5)
Do: Fix Virtual DocType, implement Variant controller
Verify: CRUD operations work
```

### Phase 5: ERPNext Sync
```
Load: @05_ERPNEXT_SYNC.md
Do: Create sync module, add custom fields fixture
Verify: Bidirectional sync works
```

---

## 🤖 Auto-Claude Commands

### Quick Fix All Conflicts
```
You are implementing a Frappe PIM system. 

First, read @CLAUDE.md for project context.
Then, read @02_CONFLICTS.md and fix ALL conflicts.

For pim_attribute_type.py:
- Add: from frappe.model.document import Document
- Add: import re  
- Fix all method indentation from 8 spaces to 4 spaces

Create these missing child tables from @04_CHILD_TABLES.md:
- Family Attribute Template
- Family Variant Attribute
- Product Type Field

After each fix, verify with: python -m py_compile [file]
```

### Implement Product Variant
```
Read @03_DOCTYPES_SPEC.md section 5 for Product Variant specification.
Read @05_ERPNEXT_SYNC.md for sync implementation.

Implement full Product Variant controller with:
1. validate() - check parent, axis values, unique combination
2. before_save() - inherit from parent, calculate completeness
3. on_update() - sync to ERPNext
4. inherit_from_parent() - copy empty fields from parent
5. sync_to_erpnext() - create/update Item

Follow coding standards from @CLAUDE.md.
```

### Setup ERPNext Integration
```
Read @05_ERPNEXT_SYNC.md completely.

Create:
1. fixtures/custom_field.json with all pim_* fields for Item
2. frappe_pim/pim/sync.py with full sync implementation
3. Update hooks.py with doc_events and fixtures

Test sync in both directions.
```

---

## ✅ Acceptance Criteria

### Minimum Viable Product (MVP)
- [ ] All Python files pass syntax check
- [ ] `bench migrate` succeeds without errors
- [ ] Can create Product Type with custom fields
- [ ] Can create Product Family with attribute inheritance
- [ ] Can create Product Master
- [ ] Can create Product Variant with axis values
- [ ] PIM ↔ ERPNext sync works bidirectionally
- [ ] No duplicate data entry required

### Quality Gates
- [ ] All DocType controllers have proper imports
- [ ] All child tables have `istable=1`
- [ ] Tree structures have lft/rgt fields
- [ ] Virtual DocType implements all required methods
- [ ] Sync uses flags to prevent infinite loops
- [ ] Error handling with frappe.log_error

---

## 🔧 Debugging Commands

```bash
# Check Python syntax
find frappe_pim -name "*.py" -exec python -m py_compile {} \;

# Run migrations
bench --site [site] migrate

# Clear cache
bench --site [site] clear-cache

# Test in console
bench --site [site] console
>>> frappe.get_doc("Product Family", "test")

# Check DocType meta
>>> frappe.get_meta("Product Master").fields

# Test sync
>>> from frappe_pim.pim.sync import sync_product_master_to_item
>>> sync_product_master_to_item(product)
```

---

## 📁 Expected File Structure After Implementation

```
frappe_pim/
├── frappe_pim/
│   ├── pim/
│   │   ├── doctype/
│   │   │   ├── family_attribute_template/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── family_attribute_template.json
│   │   │   │   └── family_attribute_template.py
│   │   │   ├── family_variant_attribute/
│   │   │   ├── pim_attribute/
│   │   │   ├── pim_attribute_group/
│   │   │   ├── pim_attribute_option/
│   │   │   ├── pim_attribute_template/
│   │   │   ├── pim_attribute_type/
│   │   │   ├── pim_product_type/
│   │   │   ├── product_attribute_value/
│   │   │   ├── product_family/
│   │   │   ├── product_master/
│   │   │   ├── product_media/
│   │   │   ├── product_type_field/
│   │   │   ├── product_variant/
│   │   │   └── variant_axis_value/
│   │   ├── sync.py
│   │   └── __init__.py
│   ├── fixtures/
│   │   └── custom_field.json
│   ├── hooks.py
│   └── __init__.py
```

---

## 🚀 Start Here

```
1. Load this file in Auto-Claude: @MASTER_PROMPT.md
2. Load project context: @CLAUDE.md  
3. Fix conflicts: @02_CONFLICTS.md
4. Follow implementation phases above
5. Test after each phase
```

**Remember**: Always fix existing conflicts before adding new features!
