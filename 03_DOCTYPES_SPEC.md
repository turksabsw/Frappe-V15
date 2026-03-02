# 03 - Complete DocType Specifications

## DocType Categories

### Configuration DocTypes (Type Layer)
Define structure, managed by admins, rarely change:
- PIM Attribute Type
- PIM Product Type
- PIM Attribute Group
- PIM Attribute Template

### Content DocTypes (Entity Layer)
Hold actual data, managed by users:
- Product Family (NestedSet)
- Product Master (Virtual)
- Product Variant
- PIM Attribute
- PIM Attribute Option

### Child Table DocTypes
Used as child tables in other DocTypes:
- Family Attribute Template
- Family Variant Attribute
- Product Type Field
- Product Attribute Value
- Variant Axis Value

---

## 1. PIM Attribute Type

**Purpose**: Defines data types for attributes (like Drupal's field types)

```json
{
  "name": "PIM Attribute Type",
  "module": "PIM",
  "naming_rule": "By fieldname",
  "autoname": "field:type_code",
  "track_changes": 1,
  
  "fields": [
    {"fieldname": "type_name", "fieldtype": "Data", "reqd": 1, "in_list_view": 1, "translatable": 1},
    {"fieldname": "type_code", "fieldtype": "Data", "reqd": 1, "unique": 1, "in_list_view": 1},
    {"fieldname": "column_break_1", "fieldtype": "Column Break"},
    {"fieldname": "base_type", "fieldtype": "Select", "reqd": 1, 
     "options": "String\nInteger\nFloat\nBoolean\nDate\nDatetime\nJSON", 
     "default": "String", "in_list_view": 1},
    {"fieldname": "is_active", "fieldtype": "Check", "default": 1, "in_list_view": 1},
    {"fieldname": "is_standard", "fieldtype": "Check", "default": 0, "read_only": 1},
    
    {"fieldname": "section_break_options", "fieldtype": "Section Break", "label": "Options"},
    {"fieldname": "has_options", "fieldtype": "Check", "default": 0,
     "description": "If checked, values must come from predefined options"},
    {"fieldname": "supports_unit", "fieldtype": "Check", "default": 0,
     "description": "If checked, values can have unit of measurement"},
    {"fieldname": "default_unit", "fieldtype": "Data", "depends_on": "supports_unit"},
    
    {"fieldname": "section_break_validation", "fieldtype": "Section Break", "label": "Validation"},
    {"fieldname": "validation_regex", "fieldtype": "Data"},
    {"fieldname": "validation_message", "fieldtype": "Data", "translatable": 1},
    {"fieldname": "min_value", "fieldtype": "Float", "depends_on": "eval:['Integer','Float'].includes(doc.base_type)"},
    {"fieldname": "max_value", "fieldtype": "Float", "depends_on": "eval:['Integer','Float'].includes(doc.base_type)"},
    {"fieldname": "max_length", "fieldtype": "Int", "depends_on": "eval:doc.base_type=='String'"},
    
    {"fieldname": "section_break_ui", "fieldtype": "Section Break", "label": "UI Configuration"},
    {"fieldname": "input_component", "fieldtype": "Data", "description": "Vue component name for input"},
    {"fieldname": "display_component", "fieldtype": "Data", "description": "Vue component name for display"},
    {"fieldname": "icon", "fieldtype": "Data", "description": "FontAwesome icon class"}
  ]
}
```

**Controller Methods**:
```python
class PIMAttributeType(Document):
    def validate(self):
        self.validate_type_code()
        self.validate_constraints()
        self.validate_regex()
    
    def validate_value(self, value) -> dict:
        """Validate a value against this type's constraints.
        Returns: {"valid": bool, "errors": list}"""
```

---

## 2. PIM Product Type

**Purpose**: Drupal-style bundle - defines which fields a product has

```json
{
  "name": "PIM Product Type",
  "module": "PIM",
  "naming_rule": "By fieldname",
  "autoname": "field:type_code",
  "is_tree": 1,
  "nsm_parent_field": "parent_type",
  "track_changes": 1,
  
  "fields": [
    {"fieldname": "type_name", "fieldtype": "Data", "reqd": 1, "in_list_view": 1, "translatable": 1},
    {"fieldname": "type_code", "fieldtype": "Data", "reqd": 1, "unique": 1, "in_list_view": 1},
    {"fieldname": "column_break_1", "fieldtype": "Column Break"},
    {"fieldname": "parent_type", "fieldtype": "Link", "options": "PIM Product Type"},
    {"fieldname": "is_active", "fieldtype": "Check", "default": 1, "in_list_view": 1},
    
    {"fieldname": "section_break_description", "fieldtype": "Section Break"},
    {"fieldname": "description", "fieldtype": "Text Editor", "translatable": 1},
    {"fieldname": "icon", "fieldtype": "Attach Image"},
    
    {"fieldname": "section_break_fields", "fieldtype": "Section Break", "label": "Type-Specific Fields"},
    {"fieldname": "type_fields", "fieldtype": "Table", "options": "Product Type Field",
     "description": "Custom fields that will appear on products of this type"},
    
    {"fieldname": "section_break_families", "fieldtype": "Section Break", "label": "Family Configuration"},
    {"fieldname": "allowed_families", "fieldtype": "Table MultiSelect", "options": "Product Family",
     "description": "Which product families can use this type"},
    {"fieldname": "default_family", "fieldtype": "Link", "options": "Product Family"},
    
    {"fieldname": "section_break_attributes", "fieldtype": "Section Break", "label": "Attribute Configuration"},
    {"fieldname": "default_attribute_template", "fieldtype": "Link", "options": "PIM Attribute Template"},
    
    {"fieldname": "section_break_variants", "fieldtype": "Section Break", "label": "Variant Configuration"},
    {"fieldname": "allow_variants", "fieldtype": "Check", "default": 1},
    {"fieldname": "max_variant_levels", "fieldtype": "Int", "default": 3, "depends_on": "allow_variants"},
    {"fieldname": "variant_sku_pattern", "fieldtype": "Data", "depends_on": "allow_variants",
     "description": "Pattern for variant SKU. Use {parent_sku}, {color}, {size}, etc."}
  ]
}
```

**Controller Methods**:
```python
class PIMProductType(NestedSet):
    nsm_parent_field = "parent_type"
    
    def get_type_fields(self) -> list:
        """Get all custom fields for this type including inherited from parent types"""
    
    def get_allowed_families(self) -> list:
        """Get families that can use this type"""
    
    def validate_product(self, product_doc) -> dict:
        """Validate a product against this type's requirements"""
```

---

## 3. Product Family (NestedSet)

**Purpose**: Defines attribute structure for products - which attributes are required/optional

```json
{
  "name": "Product Family",
  "module": "PIM",
  "naming_rule": "By fieldname",
  "autoname": "field:family_code",
  "is_tree": 1,
  "nsm_parent_field": "parent_family",
  "track_changes": 1,
  
  "fields": [
    {"fieldname": "family_name", "fieldtype": "Data", "reqd": 1, "in_list_view": 1, "translatable": 1},
    {"fieldname": "family_code", "fieldtype": "Data", "reqd": 1, "unique": 1, "in_list_view": 1},
    {"fieldname": "column_break_basic", "fieldtype": "Column Break"},
    {"fieldname": "parent_family", "fieldtype": "Link", "options": "Product Family"},
    {"fieldname": "level", "fieldtype": "Int", "default": 1, "read_only": 1},
    
    {"fieldname": "section_break_tree", "fieldtype": "Section Break", "label": "Tree Structure", "collapsible": 1},
    {"fieldname": "lft", "fieldtype": "Int", "hidden": 1, "read_only": 1},
    {"fieldname": "rgt", "fieldtype": "Int", "hidden": 1, "read_only": 1},
    {"fieldname": "is_group", "fieldtype": "Check", "default": 0},
    {"fieldname": "is_leaf", "fieldtype": "Check", "default": 1},
    
    {"fieldname": "section_break_details", "fieldtype": "Section Break", "label": "Details"},
    {"fieldname": "description", "fieldtype": "Text Editor", "translatable": 1},
    {"fieldname": "image", "fieldtype": "Attach Image"},
    
    {"fieldname": "section_break_attributes", "fieldtype": "Section Break", "label": "Family Attributes"},
    {"fieldname": "attribute_template", "fieldtype": "Link", "options": "PIM Attribute Template"},
    {"fieldname": "family_attributes", "fieldtype": "Table", "options": "Family Attribute Template",
     "description": "Required and optional attributes for products in this family"},
    
    {"fieldname": "section_break_variants", "fieldtype": "Section Break", "label": "Variant Configuration"},
    {"fieldname": "allow_variants", "fieldtype": "Check", "default": 1},
    {"fieldname": "variant_axes", "fieldtype": "Table", "options": "Family Variant Attribute",
     "depends_on": "allow_variants", "description": "Attributes that can be used as variant axes"},
    {"fieldname": "max_variant_levels", "fieldtype": "Int", "default": 3, "depends_on": "allow_variants"},
    
    {"fieldname": "section_break_status", "fieldtype": "Section Break", "label": "Status"},
    {"fieldname": "enabled", "fieldtype": "Check", "default": 1, "in_list_view": 1},
    {"fieldname": "products_count", "fieldtype": "Int", "read_only": 1},
    {"fieldname": "children_count", "fieldtype": "Int", "read_only": 1},
    {"fieldname": "full_path", "fieldtype": "Small Text", "read_only": 1}
  ]
}
```

**Controller Methods**:
```python
class ProductFamily(NestedSet):
    nsm_parent_field = "parent_family"
    
    def get_inherited_attributes(self) -> list:
        """Get all attributes including inherited from ancestor families"""
    
    def get_all_attributes(self) -> list:
        """Get family_attributes + inherited_attributes combined"""
    
    def get_variant_axes(self) -> list:
        """Get allowed variant axes for this family"""
    
    def validate_product_attributes(self, product_doc) -> dict:
        """Check if product has all required attributes"""
```

---

## 4. Product Master (Virtual DocType)

**Purpose**: Main product entity - maps to ERPNext Item

```json
{
  "name": "Product Master",
  "module": "PIM",
  "is_virtual": 1,
  "naming_rule": "By fieldname",
  "autoname": "field:product_code",
  "track_changes": 1,
  
  "fields": [
    {"fieldname": "product_name", "fieldtype": "Data", "reqd": 1, "in_list_view": 1, "translatable": 1},
    {"fieldname": "product_code", "fieldtype": "Data", "reqd": 1, "unique": 1, "in_list_view": 1},
    {"fieldname": "column_break_basic", "fieldtype": "Column Break"},
    {"fieldname": "product_type", "fieldtype": "Link", "options": "PIM Product Type", "reqd": 1, "in_list_view": 1},
    {"fieldname": "product_family", "fieldtype": "Link", "options": "Product Family", "reqd": 1, "in_list_view": 1},
    {"fieldname": "status", "fieldtype": "Select", 
     "options": "Draft\nIn Review\nApproved\nPublished\nArchived", "default": "Draft", "in_list_view": 1},
    
    {"fieldname": "section_break_details", "fieldtype": "Section Break", "label": "Product Details"},
    {"fieldname": "short_description", "fieldtype": "Small Text", "translatable": 1},
    {"fieldname": "description", "fieldtype": "Text Editor", "translatable": 1},
    {"fieldname": "main_image", "fieldtype": "Attach Image"},
    
    {"fieldname": "section_break_classification", "fieldtype": "Section Break", "label": "Classification"},
    {"fieldname": "brand", "fieldtype": "Link", "options": "Brand"},
    {"fieldname": "manufacturer", "fieldtype": "Link", "options": "Manufacturer"},
    
    {"fieldname": "section_break_attributes", "fieldtype": "Section Break", "label": "Attributes"},
    {"fieldname": "attribute_values", "fieldtype": "Table", "options": "Product Attribute Value"},
    
    {"fieldname": "section_break_variants", "fieldtype": "Section Break", "label": "Variant Configuration"},
    {"fieldname": "is_template", "fieldtype": "Check", "default": 0,
     "description": "Check if this product will have variants"},
    {"fieldname": "has_variants", "fieldtype": "Check", "read_only": 1},
    
    {"fieldname": "section_break_quality", "fieldtype": "Section Break", "label": "Data Quality"},
    {"fieldname": "completeness_score", "fieldtype": "Percent", "read_only": 1},
    {"fieldname": "missing_attributes", "fieldtype": "Small Text", "read_only": 1},
    
    {"fieldname": "section_break_erp", "fieldtype": "Section Break", "label": "ERPNext Integration"},
    {"fieldname": "erp_item", "fieldtype": "Link", "options": "Item", "read_only": 1},
    {"fieldname": "sync_to_erp", "fieldtype": "Check", "default": 1},
    {"fieldname": "last_erp_sync", "fieldtype": "Datetime", "read_only": 1}
  ]
}
```

**Controller Methods**:
```python
class ProductMaster(Document):
    """Virtual DocType - maps to ERPNext Item"""
    
    # Required Virtual DocType methods
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
    
    # PIM-specific methods
    def get_effective_attribute_value(self, attribute_code) -> any:
        """Get attribute value with inheritance from parent"""
    
    def calculate_completeness(self) -> float:
        """Calculate completeness percentage based on family requirements"""
    
    def sync_to_erpnext(self):
        """Push changes to ERPNext Item"""
    
    def sync_from_erpnext(self):
        """Pull changes from ERPNext Item"""
```

---

## 5. Product Variant

**Purpose**: Sellable variant of a product (with specific size, color, etc.)

```json
{
  "name": "Product Variant",
  "module": "PIM",
  "naming_rule": "By fieldname",
  "autoname": "field:variant_code",
  "track_changes": 1,
  
  "fields": [
    {"fieldname": "variant_name", "fieldtype": "Data", "reqd": 1, "in_list_view": 1, "translatable": 1},
    {"fieldname": "variant_code", "fieldtype": "Data", "reqd": 1, "unique": 1, "in_list_view": 1,
     "description": "SKU for this variant"},
    {"fieldname": "column_break_basic", "fieldtype": "Column Break"},
    {"fieldname": "product_master", "fieldtype": "Link", "options": "Product Master", "reqd": 1, "in_list_view": 1},
    {"fieldname": "parent_variant", "fieldtype": "Link", "options": "Product Variant",
     "description": "For multi-level variants (e.g., color variant has size sub-variants)"},
    {"fieldname": "variant_level", "fieldtype": "Int", "default": 1, "read_only": 1},
    {"fieldname": "status", "fieldtype": "Select",
     "options": "Draft\nActive\nInactive\nOut of Stock\nArchived", "default": "Draft", "in_list_view": 1},
    
    {"fieldname": "section_break_axes", "fieldtype": "Section Break", "label": "Variant Axes"},
    {"fieldname": "axis_values", "fieldtype": "Table", "options": "Variant Axis Value",
     "description": "Values that define this variant (e.g., color=red, size=M)"},
    
    {"fieldname": "section_break_attributes", "fieldtype": "Section Break", "label": "Attribute Overrides"},
    {"fieldname": "attribute_overrides", "fieldtype": "Table", "options": "Product Attribute Value",
     "description": "Attributes that override the parent product values"},
    
    {"fieldname": "section_break_media", "fieldtype": "Section Break", "label": "Media"},
    {"fieldname": "image", "fieldtype": "Attach Image"},
    {"fieldname": "media", "fieldtype": "Table", "options": "Product Media"},
    
    {"fieldname": "section_break_inventory", "fieldtype": "Section Break", "label": "Inventory"},
    {"fieldname": "barcode", "fieldtype": "Data"},
    {"fieldname": "weight", "fieldtype": "Float"},
    {"fieldname": "weight_uom", "fieldtype": "Link", "options": "UOM"},
    
    {"fieldname": "section_break_quality", "fieldtype": "Section Break", "label": "Data Quality"},
    {"fieldname": "completeness_score", "fieldtype": "Percent", "read_only": 1},
    
    {"fieldname": "section_break_erp", "fieldtype": "Section Break", "label": "ERPNext Integration"},
    {"fieldname": "erp_item", "fieldtype": "Link", "options": "Item", "read_only": 1},
    {"fieldname": "sync_to_erp", "fieldtype": "Check", "default": 1},
    {"fieldname": "last_erp_sync", "fieldtype": "Datetime", "read_only": 1},
    {"fieldname": "erp_sync_status", "fieldtype": "Select",
     "options": "Not Synced\nSynced\nSync Failed\nPending", "default": "Not Synced", "read_only": 1}
  ]
}
```

**Controller Methods**:
```python
class ProductVariant(Document):
    def validate(self):
        self.validate_axis_values()
        self.validate_unique_combination()
        self.calculate_variant_level()
    
    def before_save(self):
        self.inherit_from_parent()
        self.calculate_completeness()
    
    def on_update(self):
        if self.sync_to_erp:
            self.sync_to_erpnext()
    
    def inherit_from_parent(self):
        """Inherit empty values from parent product/variant"""
    
    def get_effective_value(self, field) -> any:
        """Get value with inheritance chain: self → parent_variant → product_master"""
    
    def sync_to_erpnext(self):
        """Create/update ERPNext Item"""
    
    def generate_sku(self) -> str:
        """Generate SKU based on pattern from product_type"""
```

---

## 6. PIM Attribute

**Purpose**: Definition of a product attribute

```json
{
  "name": "PIM Attribute",
  "module": "PIM",
  "naming_rule": "By fieldname",
  "autoname": "field:attribute_code",
  "track_changes": 1,
  
  "fields": [
    {"fieldname": "attribute_name", "fieldtype": "Data", "reqd": 1, "in_list_view": 1, "translatable": 1},
    {"fieldname": "attribute_code", "fieldtype": "Data", "reqd": 1, "unique": 1, "in_list_view": 1},
    {"fieldname": "column_break_1", "fieldtype": "Column Break"},
    {"fieldname": "attribute_type", "fieldtype": "Link", "options": "PIM Attribute Type", "reqd": 1, "in_list_view": 1},
    {"fieldname": "attribute_group", "fieldtype": "Link", "options": "PIM Attribute Group", "in_list_view": 1},
    {"fieldname": "is_active", "fieldtype": "Check", "default": 1},
    
    {"fieldname": "section_break_behavior", "fieldtype": "Section Break", "label": "Behavior"},
    {"fieldname": "is_required", "fieldtype": "Check", "default": 0},
    {"fieldname": "is_variant_axis", "fieldtype": "Check", "default": 0,
     "description": "Can be used as variant differentiator (e.g., color, size)"},
    {"fieldname": "is_filterable", "fieldtype": "Check", "default": 0},
    {"fieldname": "is_comparable", "fieldtype": "Check", "default": 0},
    {"fieldname": "is_translatable", "fieldtype": "Check", "default": 0},
    
    {"fieldname": "section_break_options", "fieldtype": "Section Break", "label": "Options",
     "depends_on": "eval:frappe.db.get_value('PIM Attribute Type', doc.attribute_type, 'has_options')"},
    {"fieldname": "options", "fieldtype": "Table", "options": "PIM Attribute Option"},
    
    {"fieldname": "section_break_default", "fieldtype": "Section Break", "label": "Default Value"},
    {"fieldname": "default_value", "fieldtype": "Data"},
    {"fieldname": "help_text", "fieldtype": "Small Text", "translatable": 1},
    
    {"fieldname": "section_break_unit", "fieldtype": "Section Break", "label": "Unit of Measurement",
     "depends_on": "eval:frappe.db.get_value('PIM Attribute Type', doc.attribute_type, 'supports_unit')"},
    {"fieldname": "unit_group", "fieldtype": "Link", "options": "UOM"},
    
    {"fieldname": "section_break_display", "fieldtype": "Section Break", "label": "Display"},
    {"fieldname": "sort_order", "fieldtype": "Int", "default": 0}
  ]
}
```

---

## Child Table DocTypes Summary

| DocType Name | Parent DocTypes | Key Fields |
|--------------|-----------------|------------|
| Family Attribute Template | Product Family | attribute, required, default_value, sort_order |
| Family Variant Attribute | Product Family | attribute, is_required, level, sort_order |
| Product Type Field | PIM Product Type | fieldname, label, fieldtype, options, reqd |
| Product Attribute Value | Product Master, Product Variant | attribute, value_*, source, locale |
| Variant Axis Value | Product Variant | attribute, option |
| PIM Attribute Option | PIM Attribute | option_code, label, color_hex, sort_order |
| Product Media | Product Master, Product Variant | file, type, is_primary, sort_order |

See @04_CHILD_TABLES.md for complete child table specifications.
