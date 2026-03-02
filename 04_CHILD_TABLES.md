# 04 - Child Table DocType Specifications

All child tables must have `"istable": 1` in their JSON definition.

---

## 1. Family Attribute Template

**Used in**: Product Family (family_attributes field)
**Purpose**: Define which attributes are required/optional for a product family

```json
{
  "doctype": "DocType",
  "name": "Family Attribute Template",
  "module": "PIM",
  "istable": 1,
  "track_changes": 0,
  
  "fields": [
    {
      "fieldname": "attribute",
      "fieldtype": "Link",
      "label": "Attribute",
      "options": "PIM Attribute",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "required",
      "fieldtype": "Check",
      "label": "Required",
      "default": 0,
      "in_list_view": 1,
      "description": "Must be filled for completeness"
    },
    {
      "fieldname": "default_value",
      "fieldtype": "Data",
      "label": "Default Value",
      "in_list_view": 1
    },
    {
      "fieldname": "sort_order",
      "fieldtype": "Int",
      "label": "Sort Order",
      "default": 0
    },
    {
      "fieldname": "inherited",
      "fieldtype": "Check",
      "label": "Inherited",
      "default": 0,
      "read_only": 1,
      "description": "Inherited from parent family"
    },
    {
      "fieldname": "inherited_from",
      "fieldtype": "Link",
      "label": "Inherited From",
      "options": "Product Family",
      "read_only": 1,
      "depends_on": "inherited"
    }
  ]
}
```

**Controller**: `family_attribute_template.py`
```python
import frappe
from frappe.model.document import Document

class FamilyAttributeTemplate(Document):
    pass  # Child tables typically don't need logic
```

---

## 2. Family Variant Attribute

**Used in**: Product Family (variant_axes field)
**Purpose**: Define which attributes can be used as variant axes

```json
{
  "doctype": "DocType",
  "name": "Family Variant Attribute",
  "module": "PIM",
  "istable": 1,
  "track_changes": 0,
  
  "fields": [
    {
      "fieldname": "attribute",
      "fieldtype": "Link",
      "label": "Attribute",
      "options": "PIM Attribute",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "is_required",
      "fieldtype": "Check",
      "label": "Required",
      "default": 1,
      "in_list_view": 1,
      "description": "Must be specified for every variant"
    },
    {
      "fieldname": "level",
      "fieldtype": "Int",
      "label": "Variant Level",
      "default": 1,
      "in_list_view": 1,
      "description": "1 = first level (e.g., color), 2 = second level (e.g., size)"
    },
    {
      "fieldname": "sort_order",
      "fieldtype": "Int",
      "label": "Sort Order",
      "default": 0
    }
  ]
}
```

---

## 3. Product Type Field

**Used in**: PIM Product Type (type_fields field)
**Purpose**: Define custom fields specific to a product type (Drupal-style bundle fields)

```json
{
  "doctype": "DocType",
  "name": "Product Type Field",
  "module": "PIM",
  "istable": 1,
  "track_changes": 0,
  
  "fields": [
    {
      "fieldname": "fieldname",
      "fieldtype": "Data",
      "label": "Field Name",
      "reqd": 1,
      "in_list_view": 1,
      "description": "Internal field name (snake_case)"
    },
    {
      "fieldname": "label",
      "fieldtype": "Data",
      "label": "Label",
      "reqd": 1,
      "in_list_view": 1,
      "translatable": 1
    },
    {
      "fieldname": "fieldtype",
      "fieldtype": "Select",
      "label": "Field Type",
      "reqd": 1,
      "in_list_view": 1,
      "options": "Data\nText\nText Editor\nInt\nFloat\nCurrency\nPercent\nCheck\nSelect\nLink\nDate\nDatetime\nAttach\nAttach Image"
    },
    {
      "fieldname": "options",
      "fieldtype": "Small Text",
      "label": "Options",
      "description": "For Select: newline-separated options. For Link: DocType name."
    },
    {
      "fieldname": "reqd",
      "fieldtype": "Check",
      "label": "Required",
      "default": 0,
      "in_list_view": 1
    },
    {
      "fieldname": "default_value",
      "fieldtype": "Data",
      "label": "Default Value"
    },
    {
      "fieldname": "description",
      "fieldtype": "Small Text",
      "label": "Description",
      "translatable": 1
    },
    {
      "fieldname": "sort_order",
      "fieldtype": "Int",
      "label": "Sort Order",
      "default": 0
    }
  ]
}
```

---

## 4. Product Attribute Value

**Used in**: Product Master (attribute_values), Product Variant (attribute_overrides)
**Purpose**: Store actual attribute values for products (EAV pattern)

```json
{
  "doctype": "DocType",
  "name": "Product Attribute Value",
  "module": "PIM",
  "istable": 1,
  "track_changes": 0,
  
  "fields": [
    {
      "fieldname": "attribute",
      "fieldtype": "Link",
      "label": "Attribute",
      "options": "PIM Attribute",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "value_type",
      "fieldtype": "Select",
      "label": "Value Type",
      "options": "String\nNumber\nBoolean\nOption\nMulti Option\nJSON",
      "default": "String",
      "read_only": 1
    },
    {
      "fieldname": "value_string",
      "fieldtype": "Data",
      "label": "Text Value",
      "depends_on": "eval:doc.value_type=='String'"
    },
    {
      "fieldname": "value_number",
      "fieldtype": "Float",
      "label": "Numeric Value",
      "depends_on": "eval:doc.value_type=='Number'"
    },
    {
      "fieldname": "value_boolean",
      "fieldtype": "Check",
      "label": "Boolean Value",
      "depends_on": "eval:doc.value_type=='Boolean'"
    },
    {
      "fieldname": "value_option",
      "fieldtype": "Link",
      "label": "Option Value",
      "options": "PIM Attribute Option",
      "depends_on": "eval:doc.value_type=='Option'"
    },
    {
      "fieldname": "value_multi_option",
      "fieldtype": "Small Text",
      "label": "Multi Option Values",
      "depends_on": "eval:doc.value_type=='Multi Option'",
      "description": "JSON array of option names"
    },
    {
      "fieldname": "value_json",
      "fieldtype": "JSON",
      "label": "JSON Value",
      "depends_on": "eval:doc.value_type=='JSON'"
    },
    {
      "fieldname": "display_value",
      "fieldtype": "Data",
      "label": "Display Value",
      "read_only": 1,
      "in_list_view": 1,
      "description": "Human-readable value for display"
    },
    {
      "fieldname": "unit",
      "fieldtype": "Data",
      "label": "Unit",
      "description": "Unit of measurement (if applicable)"
    },
    {
      "fieldname": "source",
      "fieldtype": "Select",
      "label": "Source",
      "options": "Manual\nInherited\nCalculated\nImported\nAPI",
      "default": "Manual"
    },
    {
      "fieldname": "locale",
      "fieldtype": "Link",
      "label": "Locale",
      "options": "Language",
      "description": "For translatable attributes"
    }
  ]
}
```

---

## 5. Variant Axis Value

**Used in**: Product Variant (axis_values field)
**Purpose**: Store the variant-defining attribute values (what makes this variant unique)

```json
{
  "doctype": "DocType",
  "name": "Variant Axis Value",
  "module": "PIM",
  "istable": 1,
  "track_changes": 0,
  
  "fields": [
    {
      "fieldname": "attribute",
      "fieldtype": "Link",
      "label": "Axis Attribute",
      "options": "PIM Attribute",
      "reqd": 1,
      "in_list_view": 1,
      "description": "Must be an attribute with is_variant_axis=True"
    },
    {
      "fieldname": "option",
      "fieldtype": "Link",
      "label": "Option Value",
      "options": "PIM Attribute Option",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "display_value",
      "fieldtype": "Data",
      "label": "Display Value",
      "read_only": 1,
      "in_list_view": 1,
      "fetch_from": "option.label"
    }
  ]
}
```

---

## 6. PIM Attribute Option

**Used in**: PIM Attribute (options field)
**Purpose**: Predefined options for select-type attributes

```json
{
  "doctype": "DocType",
  "name": "PIM Attribute Option",
  "module": "PIM",
  "istable": 1,
  "track_changes": 0,
  
  "fields": [
    {
      "fieldname": "option_code",
      "fieldtype": "Data",
      "label": "Option Code",
      "reqd": 1,
      "in_list_view": 1,
      "description": "Machine-readable code (e.g., 'red', 'xl')"
    },
    {
      "fieldname": "label",
      "fieldtype": "Data",
      "label": "Label",
      "reqd": 1,
      "in_list_view": 1,
      "translatable": 1,
      "description": "Human-readable label"
    },
    {
      "fieldname": "color_hex",
      "fieldtype": "Data",
      "label": "Color (Hex)",
      "description": "For color attributes, e.g., #FF0000"
    },
    {
      "fieldname": "image",
      "fieldtype": "Attach Image",
      "label": "Image",
      "description": "Visual representation of the option"
    },
    {
      "fieldname": "external_code",
      "fieldtype": "Data",
      "label": "External Code",
      "description": "Code for external systems (ERP, marketplace)"
    },
    {
      "fieldname": "sort_order",
      "fieldtype": "Int",
      "label": "Sort Order",
      "default": 0,
      "in_list_view": 1
    },
    {
      "fieldname": "is_active",
      "fieldtype": "Check",
      "label": "Active",
      "default": 1
    }
  ]
}
```

---

## 7. Product Media

**Used in**: Product Master (media), Product Variant (media)
**Purpose**: Store multiple media files for a product

```json
{
  "doctype": "DocType",
  "name": "Product Media",
  "module": "PIM",
  "istable": 1,
  "track_changes": 0,
  
  "fields": [
    {
      "fieldname": "file",
      "fieldtype": "Attach",
      "label": "File",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "media_type",
      "fieldtype": "Select",
      "label": "Type",
      "options": "Image\nVideo\nDocument\n3D Model\nAudio",
      "default": "Image",
      "in_list_view": 1
    },
    {
      "fieldname": "title",
      "fieldtype": "Data",
      "label": "Title",
      "translatable": 1
    },
    {
      "fieldname": "alt_text",
      "fieldtype": "Data",
      "label": "Alt Text",
      "translatable": 1,
      "description": "For accessibility and SEO"
    },
    {
      "fieldname": "is_primary",
      "fieldtype": "Check",
      "label": "Primary",
      "default": 0,
      "in_list_view": 1,
      "description": "Main image for product listing"
    },
    {
      "fieldname": "role",
      "fieldtype": "Select",
      "label": "Role",
      "options": "Main\nGallery\nThumbnail\nTechnical\nPackaging\nLifestyle",
      "default": "Gallery"
    },
    {
      "fieldname": "sort_order",
      "fieldtype": "Int",
      "label": "Sort Order",
      "default": 0
    }
  ]
}
```

---

## File Structure Template

For each child table, create these files:

```
frappe_pim/pim/doctype/[doctype_name]/
├── __init__.py          # Empty file
├── [doctype_name].json  # DocType definition
└── [doctype_name].py    # Python controller
```

### __init__.py
```python
# Empty file - required for Python module
```

### [doctype_name].py
```python
# Copyright (c) 2024, Frappe PIM Team
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class [ClassName](Document):
    # istable doctypes typically don't need methods
    pass
```

Class name should be PascalCase version of doctype name:
- `family_attribute_template` → `FamilyAttributeTemplate`
- `variant_axis_value` → `VariantAxisValue`
