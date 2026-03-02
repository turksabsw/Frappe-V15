# 01 - PIM System Architecture

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CONFIGURATION LAYER                                │
│  (Defines Structure - Admin manages these)                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐      │
│  │ PIM Attribute    │    │ PIM Product Type │    │  Product Family  │      │
│  │     Type         │    │                  │    │   (NestedSet)    │      │
│  ├──────────────────┤    ├──────────────────┤    ├──────────────────┤      │
│  │ - type_code      │    │ - type_code      │    │ - family_code    │      │
│  │ - base_type      │    │ - type_name      │    │ - parent_family  │      │
│  │ - has_options    │    │ - type_fields[]  │◄───│ - family_attrs[] │      │
│  │ - supports_unit  │    │ - allowed_fams[] │    │ - variant_axes[] │      │
│  │ - validation     │    │ - variant_config │    │ - attr_template  │      │
│  └────────┬─────────┘    └────────┬─────────┘    └────────┬─────────┘      │
│           │                       │                       │                 │
└───────────┼───────────────────────┼───────────────────────┼─────────────────┘
            │                       │                       │
            ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CONTENT LAYER                                   │
│  (Holds Data - Users work with these)                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────┐                                                       │
│  │  PIM Attribute   │    ┌──────────────────────────────────────────┐      │
│  ├──────────────────┤    │            Product Master                 │      │
│  │ - attribute_code │    │         (Virtual DocType)                 │      │
│  │ - attribute_type │────│                                          │      │
│  │ - attribute_group│    ├──────────────────────────────────────────┤      │
│  │ - options[]      │    │ - product_code (→ Item.item_code)        │      │
│  └──────────────────┘    │ - product_type (→ PIM Product Type)      │      │
│                          │ - product_family (→ Product Family)       │      │
│                          │ - attribute_values[] (EAV pattern)        │      │
│                          │ - is_template (for variants)              │      │
│                          └─────────────────┬────────────────────────┘      │
│                                            │                                │
│                                            │ parent_product                 │
│                                            ▼                                │
│                          ┌──────────────────────────────────────────┐      │
│                          │          Product Variant                  │      │
│                          ├──────────────────────────────────────────┤      │
│                          │ - variant_code (SKU)                      │      │
│                          │ - product_master (parent)                 │      │
│                          │ - variant_level (1-3)                     │      │
│                          │ - axis_values[] (color, size, etc.)       │      │
│                          │ - attribute_overrides[]                   │      │
│                          │ - erp_item (→ ERPNext Item)               │      │
│                          └──────────────────────────────────────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ Bidirectional Sync
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ERPNEXT LAYER                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────────────────────────┐                              │
│  │              ERPNext Item                 │                              │
│  ├──────────────────────────────────────────┤                              │
│  │ Standard Fields:                          │                              │
│  │ - item_code, item_name, item_group        │                              │
│  │ - has_variants, variant_of                │                              │
│  │                                           │                              │
│  │ PIM Custom Fields (to be added):          │                              │
│  │ - pim_product_id (Link → Product Master)  │                              │
│  │ - pim_family (Link → Product Family)      │                              │
│  │ - pim_last_synced (Datetime)              │                              │
│  │ - pim_sync_enabled (Check)                │                              │
│  │ - pim_sync_direction (Select)             │                              │
│  └──────────────────────────────────────────┘                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Drupal-Style Type Pattern Implementation

### The Bundle Concept
In Drupal, a "bundle" is a sub-type of an entity type. For example:
- Node entity has bundles: Article, Page, Blog Post
- Product entity has bundles: Physical, Digital, Subscription

In Frappe PIM:
```
PIM Product Type (bundle definition)
    └── defines which fields exist for products of this type
    
Product Master (content entity)
    └── product_type field links to bundle
    └── dynamically renders fields based on type
```

### Type-Specific Custom Fields
Each type can have different custom fields via child table:

```python
# PIM Product Type has child table: Product Type Field
class PIMProductType(Document):
    def get_type_fields(self):
        """Return all custom fields for this type"""
        return self.type_fields  # Child table
    
    def on_update(self):
        """When type changes, rebuild field cache"""
        self.rebuild_type_field_cache()
```

### Field Inheritance Chain
```
Product Family (attribute template)
    │
    ├── defines: family_attributes (required attributes)
    │
    └── Product Type (references family)
            │
            ├── defines: type_fields (additional type-specific fields)
            │
            └── Product Master (has both family attrs + type fields)
```

## Attribute System (EAV Pattern)

### Why EAV (Entity-Attribute-Value)?
- Products can have hundreds of different attributes
- Attributes vary by product type and family
- Adding new attributes shouldn't require schema changes

### Implementation
```
PIM Attribute (defines the attribute)
├── attribute_code: "color"
├── attribute_type: → PIM Attribute Type ("select")
├── attribute_group: → PIM Attribute Group ("Visual")
└── options: [PIM Attribute Option] (red, blue, green)

Product Attribute Value (child table on Product)
├── attribute: → PIM Attribute
├── value_string / value_number / value_json
└── source: "manual" / "inherited" / "calculated"
```

## Variant Hierarchy (Max 3 Levels)

```
Product Master: "Classic T-Shirt" (is_template=True)
│   └── attributes: brand, material, care_instructions
│
├── Level 1 Variant: "Classic T-Shirt - Navy"
│   │   └── axis: color = navy
│   │   └── overrides: images, color_code
│   │
│   ├── Level 2 Variant: "Classic T-Shirt - Navy - S" (SKU: CT-NVY-S)
│   │       └── axis: size = S
│   │       └── final sellable unit
│   │
│   └── Level 2 Variant: "Classic T-Shirt - Navy - M" (SKU: CT-NVY-M)
│
└── Level 1 Variant: "Classic T-Shirt - White"
    └── ...
```

### Variant Inheritance Rules
1. Empty fields inherit from parent
2. Non-empty fields override parent
3. Axis values are always explicit (never inherited)
4. SKU is required only at final variant level

## Category vs Family vs Type

| Aspect | Product Family | Product Type | Category |
|--------|---------------|--------------|----------|
| Purpose | Attribute structure | Business behavior | Navigation |
| Cardinality | One-to-one | One-to-one | Many-to-many |
| Inheritance | Attributes from parent family | Type fields | None |
| Example | Electronics > Computers > Laptops | "Standard Product" | Men's > Casual > Summer |
| Who manages | PIM Admin | PIM Admin | Merchandiser |

## Data Flow

### Product Creation Flow
```
1. Select Product Type
   └── System filters available families by type.allowed_families

2. Select Product Family
   └── System loads family_attributes + inherited attributes from ancestors

3. Fill Required Attributes
   └── Completeness score calculated

4. Create Variants (optional)
   └── Select variant axes from family.variant_axes
   └── Generate combinations

5. Sync to ERPNext
   └── Product Master → Item (template)
   └── Product Variant → Item (variant)
```

### Attribute Value Resolution
```python
def get_effective_value(product, attribute_code):
    """Get attribute value with inheritance"""
    
    # 1. Check product's own value
    value = product.get_attribute_value(attribute_code)
    if value is not None:
        return value
    
    # 2. Check parent product (if variant)
    if product.parent_product:
        parent = frappe.get_doc("Product Master", product.parent_product)
        return get_effective_value(parent, attribute_code)
    
    # 3. Check family default
    family = frappe.get_doc("Product Family", product.product_family)
    return family.get_default_value(attribute_code)
```
