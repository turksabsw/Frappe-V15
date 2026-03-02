# Frappe PIM - Product Information Management Module

## Project Overview
Enterprise-grade PIM system for Frappe Framework v15+ with ERPNext integration.
Implements Drupal-style entity/bundle pattern where every entity has a "type" with custom fields.

## Tech Stack
- **Framework**: Frappe v15+
- **ERP**: ERPNext v15+ (bidirectional sync)
- **Language**: Python 3.11+
- **Database**: MariaDB 10.6+
- **Frontend**: Frappe UI (standard DocType forms)

## Architecture Principles

### 1. Drupal-Style Type System
Every content entity has a configuration entity (type) that defines its field structure:
```
PIM Product Type → Product Master
PIM Attribute Type → PIM Attribute  
PIM Variant Type → Product Variant
```

### 2. Separation of Concerns
- **Product Family**: Defines WHICH attributes a product needs (structure)
- **Product Type**: Defines HOW a product is classified/merchandised (behavior)
- **Category**: Defines WHERE a product appears in navigation (taxonomy)

### 3. ERPNext Integration
- Bidirectional sync with Item DocType
- Conflict detection via timestamps
- Sync flags to prevent infinite loops
- Custom fields on Item for PIM data

## Module Path
```
frappe-bench/apps/frappe_pim/
├── frappe_pim/
│   ├── pim/
│   │   ├── doctype/
│   │   │   ├── pim_product_type/
│   │   │   ├── product_family/
│   │   │   ├── product_master/
│   │   │   ├── product_variant/
│   │   │   ├── pim_attribute/
│   │   │   ├── pim_attribute_type/
│   │   │   ├── pim_attribute_group/
│   │   │   ├── pim_attribute_option/
│   │   │   ├── pim_attribute_template/
│   │   │   └── [child_tables]/
│   │   └── utils/
│   ├── hooks.py
│   └── __init__.py
```

## Coding Standards

### Python
```python
# Always include these imports for DocType controllers
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils.nestedset import NestedSet  # For tree structures
from typing import Dict, List, Optional, Any
import re  # If using regex validation

# Class naming: Match DocType name in PascalCase
class PIMProductType(Document):  # For "PIM Product Type"
    pass

class ProductFamily(NestedSet):  # For tree DocTypes
    nsm_parent_field = "parent_family"
```

### Indentation
- Always use **4 spaces** (not 8, not tabs)
- Method definitions inside class should have one level of indentation

### ERPNext Sync Pattern
```python
def sync_to_erpnext(doc, method=None):
    # Prevent infinite sync loop
    if getattr(doc, '_from_erpnext_sync', False):
        return
    
    item = frappe.get_doc("Item", doc.erp_item)
    item._from_pim_sync = True
    # ... mapping logic
    item.save(ignore_permissions=True)
```

## Key Design Decisions

### Virtual vs Normal DocType
- **Product Master**: Virtual DocType → maps to ERPNext Item
- **Product Variant**: Normal DocType → syncs to ERPNext Item
- **All Type DocTypes**: Normal DocTypes (configuration entities)

### Child Tables Required
All child tables must have `istable = 1` in their JSON and proper parent link.

### Tree Structures (NestedSet)
Required fields for any tree DocType:
- `lft` (Int, hidden, read_only)
- `rgt` (Int, hidden, read_only)
- `parent_[name]` (Link to self)
- `is_group` (Check)

## Commands

### Run Tests
```bash
bench --site [site] run-tests --app frappe_pim
```

### Migrate
```bash
bench --site [site] migrate
```

### Clear Cache
```bash
bench --site [site] clear-cache
```

## Reference Files
When implementing, always refer to:
- @01_ARCHITECTURE.md - System architecture
- @02_CONFLICTS.md - Known issues and fixes
- @03_DOCTYPES_SPEC.md - Complete DocType specifications
- @04_CHILD_TABLES.md - All child table definitions
- @05_ERPNEXT_SYNC.md - ERPNext integration details
- @06_IMPLEMENTATION.md - Step-by-step implementation guide
