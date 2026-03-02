# PIM Customization Guide

## Comprehensive Per-Customer Onboarding & Configuration Reference

**Version:** 1.0
**Last Updated:** February 2026
**Target Audience:** Implementation Teams, Solution Architects, Customer Success Engineers
**Scope:** Frappe PIM v15+ — 101 DocTypes, 24 Utility Modules, 15 API Endpoints, 5 Service Layers

---

## Executive Summary

Frappe PIM is an enterprise-grade Product Information Management system built on Frappe v15+ with deep ERPNext integration. It follows a **Drupal-style type/bundle pattern** where configuration entities (Product Types, Attribute Types, Product Families) define the field structure and behavior for content entities (Product Master, Product Variant, PIM Attribute).

This document catalogs **every customization surface** available during customer onboarding, organized into 15 domains. Each customization point includes:

- **What it is** — the DocType, field, or configuration option
- **When to configure** — at which onboarding phase this should be set
- **Who configures** — the role responsible (System Manager, PIM Manager, PIM User)
- **Business impact** — what business outcome the configuration drives

### How to Use This Guide

1. **New Deployments (Greenfield):** Follow the Recommended Onboarding Sequence (Section 16) end-to-end
2. **Migrations:** Use the Edge Cases section (Section 17) for migration-specific guidance, then selectively follow relevant domain sections
3. **Expanding Existing Setup:** Jump directly to the relevant customization domain section

---

## Table of Contents

### Customization Domains (Sections 1–15)

1. [Type System (Drupal-Style Bundle Pattern)](#1-type-system-drupal-style-bundle-pattern)
2. [Attribute System (EAV Pattern)](#2-attribute-system-eav-pattern)
3. [Global Settings (PIM Settings)](#3-global-settings-pim-settings)
4. [Channel Configuration](#4-channel-configuration)
5. [Workflow & Lifecycle](#5-workflow--lifecycle)
6. [Scoring & Quality](#6-scoring--quality)
7. [ERPNext Integration](#7-erpnext-integration)
8. [Roles & Permissions](#8-roles--permissions)
9. [Taxonomy & Navigation](#9-taxonomy--navigation)
10. [AI & Enrichment](#10-ai--enrichment)
11. [Media & Digital Assets](#11-media--digital-assets)
12. [Export & Integration](#12-export--integration)
13. [Internationalization](#13-internationalization)
14. [Bundling & Packaging](#14-bundling--packaging)
15. [MDM (Master Data Management)](#15-mdm-master-data-management)

### Implementation & Onboarding (Sections 16–18)

16. [Recommended Onboarding Configuration Sequence](#16-recommended-onboarding-configuration-sequence)
    - Phase 0: Global Configuration (PIM Settings)
    - Phase 1: Foundation Schema (Attribute Types, Groups, Attributes, Families)
    - Phase 2: Content Infrastructure (Product Types, Categories, Brands)
    - Phase 3: Quality & Governance (Roles, Permissions, Quality Policies)
    - Phase 4: Channel & Export Setup (Channels, Export Profiles)
    - Phase 5: Advanced Features (AI, GS1, Bundling, MDM)
    - Phase 6: Content Creation (Products, Variants, Media)
    - Phase 7: Go-Live (Workflow, Publishing, Sync Activation)
17. [Edge Cases & Deployment Scenarios](#17-edge-cases--deployment-scenarios)
    - 17.1 Greenfield vs. Migration
    - 17.2 Single vs. Multi-Company
    - 17.3 With vs. Without ERPNext
    - 17.4 Minimal vs. Full Setup
    - 17.5 Common Deployment Patterns
18. [Customer Archetype Deep-Dives](#18-customer-archetype-deep-dives)
    - 18.1 Fashion Retailer (complete configuration profile)
    - 18.2 Industrial Supplier (complete configuration profile)
    - 18.3 Food Manufacturer (complete configuration profile)
    - 18.4 Archetype Comparison Matrix

### Appendices

- [Appendix A: Additional Configurable Entities](#appendix-a-additional-configurable-entities)
- [Appendix B: Document Change Log](#appendix-b-document-change-log)
- [Appendix C: Glossary](#appendix-c-glossary)

---

## 1. Type System (Drupal-Style Bundle Pattern)

### Overview

The PIM implements a **Drupal-style type/bundle pattern** that separates *configuration entities* (which define structure) from *content entities* (which hold product data). This pattern enables each customer to define their own product data model without code changes.

**Architecture:**

```
┌─────────────────────┐     ┌──────────────────────┐     ┌────────────────────┐
│  PIM Product Type    │────▶│   Product Family      │────▶│   Product Master    │
│  (Bundle Definition) │     │   (Attribute Template) │     │   (Content Entity)  │
└─────────────────────┘     └──────────────────────┘     └────────────────────┘
         │                           │                           │
         │                           │                           ▼
         │                           │                   ┌────────────────────┐
         │                           │                   │   Product Variant   │
         │                           │                   │   (SKU-level)       │
         │                           ▼                   └────────────────────┘
         │                  ┌──────────────────────┐
         │                  │ Family Attribute      │
         │                  │ Template (child table) │
         │                  └──────────────────────┘
         ▼
┌─────────────────────┐
│  PIM Attribute Type  │
│  (Data Type Def)     │
└─────────────────────┘
```

### 1.1 PIM Product Type

**DocType:** `PIM Product Type`
**Purpose:** Defines a category of products with shared structural characteristics — the "bundle" in Drupal terminology.

> **Note:** This DocType defines the high-level classification of products. While the JSON definition may not exist in all installations (it can be created via Frappe's DocType builder), its conceptual role is central to the type system.

**Customization Points:**

| Field | Type | Purpose | Customization Impact |
|-------|------|---------|---------------------|
| `type_name` | Data | Display name of the product type | Customer-specific product taxonomy |
| `type_code` | Data | Unique slug identifier | Internal reference, affects API calls |
| `product_family` | Link → Product Family | Default family for this type | Determines which attributes appear on products |
| `fields` | Table → Product Type Field | Custom fields for this type | Extends the base product form per type |
| `has_variants` | Check | Whether products of this type support SKU variants | Business model decision |
| `description` | Text | Type description | Documentation for content teams |

**When to Configure:** Phase 1 of onboarding — immediately after PIM Settings
**Who Configures:** PIM Manager or Solution Architect
**Business Impact:** Determines the fundamental product data model for the entire deployment

#### Customer Archetype Examples — Product Types

**Fashion Retailer:**
```
Product Types:
  ├── Apparel          → has_variants: ✓  (Size, Color)
  ├── Footwear         → has_variants: ✓  (Size, Width, Color)
  ├── Accessories      → has_variants: ✓  (Color, Material)
  └── Gift Cards       → has_variants: ✗
```

**Industrial Supplier:**
```
Product Types:
  ├── Raw Material     → has_variants: ✗
  ├── Component        → has_variants: ✓  (Grade, Tolerance)
  ├── Assembly         → has_variants: ✓  (Configuration)
  ├── Tooling          → has_variants: ✗
  └── Safety Equipment → has_variants: ✓  (Size)
```

**Food Manufacturer:**
```
Product Types:
  ├── Fresh Produce    → has_variants: ✓  (Weight, Pack Size)
  ├── Packaged Food    → has_variants: ✓  (Pack Size, Flavor)
  ├── Beverage         → has_variants: ✓  (Volume, Flavor)
  └── Ingredient       → has_variants: ✓  (Grade, Weight)
```

### 1.2 PIM Attribute Type

**DocType:** `PIM Attribute Type`
**Purpose:** Defines the data types available for product attributes. This is the metadata layer that controls what kind of values can be stored.

**Customization Points:**

| Field | Type | Purpose | Customization Impact |
|-------|------|---------|---------------------|
| `type_name` | Data | Display name | UI labeling |
| `type_code` | Data | Unique identifier slug | Referenced by PIM Attribute `data_type` |
| `base_type` | Select | Underlying storage type | Determines validation behavior |
| `validation_rules` | JSON/Text | Type-specific validation | Data quality enforcement |

**Supported Data Types (12 total):**

| Data Type | Storage Field | Use Case Example |
|-----------|--------------|-----------------|
| `Text` | `value_text` | Product name, short description |
| `Long Text` | `value_long_text` | Full product description, care instructions |
| `Integer` | `value_int` | Pack quantity, minimum order quantity |
| `Float` | `value_float` | Weight, dimensions, percentage values |
| `Select` | `value_text` | Material type, target gender, season |
| `Multi Select` | `value_text` | Applicable certifications, features list |
| `Boolean` | `value_boolean` | Is organic, is recyclable, contains allergens |
| `Date` | `value_date` | Manufacturing date, expiry date |
| `Datetime` | `value_datetime` | Last quality check timestamp |
| `Link` | `value_link` | Reference to another DocType record |
| `Image` | `value_text` | Technical drawing, certification image |
| `File` | `value_text` | Safety datasheet, manual PDF |

**When to Configure:** Phase 1 — before creating PIM Attributes
**Who Configures:** System Manager (typically one-time setup)
**Business Impact:** Constrains the types of data that can be captured about products; incorrect type selection leads to data quality issues

### 1.3 Product Family

**DocType:** `Product Family`
**Module:** PIM
**Naming Rule:** `field:family_code` (named by the `family_code` field)
**Tree Structure:** Yes (`is_tree: true`, `nsm_parent_field: parent_family`) — supports hierarchical family structures using Frappe's NestedSet pattern.

Product Family is the **central configuration entity** that bridges the type system with the attribute system. Each Product Master must belong to exactly one Product Family, which determines:

1. Which attributes appear on the product form (via `Family Attribute Template`)
2. Which attributes define variants (via `Family Variant Attribute`)
3. SKU prefix naming conventions
4. Media requirements
5. Completeness thresholds
6. ERP Item Group mapping

#### Configurable Fields

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `family_name` | Data (required, translatable) | — | Display name | Localized per customer language |
| `family_code` | Data (required, unique) | — | Unique slug identifier | Used in API calls, SKU generation |
| `parent_family` | Link → Product Family | — | Parent in hierarchy | Enables attribute inheritance |
| `naming_series_prefix` | Data | — | SKU prefix (e.g., `TSH-`, `ELK-`) | Drives auto-generated product codes |
| `is_active` | Check | `1` | Enable/disable family | Controls product creation eligibility |
| `allow_variants` | Check | `1` | Products can have SKU variants | Fundamental business model decision |
| `inherit_parent_attributes` | Check | `1` | Auto-include parent family attributes | Reduces configuration duplication |
| `erp_item_group` | Link → Item Group | — | ERPNext Item Group mapping | Required for ERP sync; maps PIM family to ERP hierarchy |
| `attributes` | Table → Family Attribute Template | — | Attribute assignments for this family | **Core customization surface** — defines the product data model |
| `variant_attributes` | Table MultiSelect → Family Variant Attribute | — | Attributes that define variants | Determines SKU generation axes |
| `required_media_types` | Small Text | — | Comma-separated media types (e.g., `Main Image, Gallery, Video`) | Channel-specific media requirements |
| `min_images` | Int | `1` | Minimum images required per product | Quality gate for publishing |
| `completeness_threshold` | Percent | `80` | Minimum completeness score to be considered "complete" | Quality gate threshold |
| `description` | Text Editor | — | Family description | Internal documentation |

#### Child Table: Family Attribute Template

**DocType:** `Family Attribute Template` (child table, `istable: 1`)

This child table links PIM Attributes to a Product Family, defining which attributes appear on products of this family and how they behave.

| Field | Type | Purpose |
|-------|------|---------|
| `attribute` | Link → PIM Attribute (required) | Which attribute to include |
| `is_required_in_family` | Check (default: 0) | Whether this attribute is mandatory for products in this family |
| `default_value` | Small Text | Pre-filled value for new products |
| `sort_order` | Int (default: 0) | Display order in the product form |

#### Child Table: Family Variant Attribute

**DocType:** `Family Variant Attribute` (child table, `istable: 1`)

Specifies which attributes are used to generate product variants (SKUs). For example, a T-Shirt family might use "Size" and "Color" as variant-defining attributes.

| Field | Type | Purpose |
|-------|------|---------|
| `attribute` | Link → PIM Attribute (required) | The variant-defining attribute |
| `sort_order` | Int (default: 0) | Order of variant axes |

#### Permissions

| Role | Read | Write | Create | Delete | Export | Import |
|------|------|-------|--------|--------|--------|--------|
| System Manager | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PIM Manager | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PIM User | ✓ | — | — | — | — | — |

#### Customer Archetype Examples — Product Families

**Fashion Retailer:**
```
Product Families (Hierarchical):
  ├── Apparel
  │   ├── Tops              → prefix: TOP-, variants: [Size, Color]
  │   │   ├── T-Shirts      → prefix: TSH-, inherits Tops attributes
  │   │   ├── Shirts        → prefix: SHR-, inherits + adds Collar Type
  │   │   └── Sweaters      → prefix: SWT-, inherits + adds Knit Type
  │   ├── Bottoms           → prefix: BTM-, variants: [Size, Color]
  │   │   ├── Jeans         → prefix: JNS-, inherits + adds Fit, Wash
  │   │   └── Skirts        → prefix: SKR-, inherits + adds Length
  │   └── Outerwear         → prefix: OUT-, variants: [Size, Color]
  ├── Footwear
  │   ├── Sneakers          → prefix: SNK-, variants: [Size, Color, Width]
  │   └── Boots             → prefix: BTS-, variants: [Size, Color]
  └── Accessories
      ├── Bags              → prefix: BAG-, variants: [Color]
      └── Jewelry           → prefix: JWL-, variants: [Material, Size]

Key settings:
  - inherit_parent_attributes: ✓ (saves setup time across 12+ sub-families)
  - min_images: 4 (fashion requires multiple angles)
  - completeness_threshold: 90% (high bar for brand-conscious retailers)
  - required_media_types: "Main Image, Front, Back, Detail, Lifestyle"
```

**Industrial Supplier:**
```
Product Families (Flat or 2-level):
  ├── Fasteners             → prefix: FST-, variants: [Size, Grade]
  ├── Bearings              → prefix: BRG-, variants: [Size, Type]
  ├── Hydraulic Components  → prefix: HYD-, no variants
  ├── Electrical Components → prefix: ELC-, variants: [Rating, Connector]
  └── Safety Equipment      → prefix: SAF-, variants: [Size]

Key settings:
  - inherit_parent_attributes: ✗ (flat structure, each family is distinct)
  - min_images: 1 (technical products need fewer glamour shots)
  - completeness_threshold: 95% (safety-critical data must be complete)
  - required_media_types: "Main Image, Technical Drawing"
  - erp_item_group mapped to existing ERP structure
```

**Food Manufacturer:**
```
Product Families (Regulated hierarchy):
  ├── Dairy Products
  │   ├── Milk              → prefix: MLK-, variants: [Fat%, Pack Size]
  │   ├── Cheese            → prefix: CHS-, variants: [Type, Weight]
  │   └── Yogurt            → prefix: YGT-, variants: [Flavor, Pack Size]
  ├── Bakery
  │   ├── Bread             → prefix: BRD-, variants: [Type, Size]
  │   └── Pastries          → prefix: PST-, variants: [Flavor, Pack Size]
  └── Beverages
      ├── Juices            → prefix: JCE-, variants: [Flavor, Volume]
      └── Water             → prefix: WTR-, variants: [Volume, Type]

Key settings:
  - inherit_parent_attributes: ✓ (nutrition facts shared across categories)
  - min_images: 2 (front label + nutrition panel)
  - completeness_threshold: 98% (regulatory compliance requires near-complete data)
  - required_media_types: "Main Image, Nutrition Label, Ingredient List"
  - Special attributes: allergens, nutrition_facts, shelf_life_days, storage_temperature
```

### 1.4 How the Type System Connects to Product Data

The Product Master DocType is the **content entity** that stores actual product data. Its relationship to the type system:

**DocType:** `Product Master`
**Key Type System Fields:**

| Field | Type | Purpose |
|-------|------|---------|
| `product_name` | Data (required, translatable) | Product display name |
| `product_code` | Data (required, unique) | Auto-generated or manual product code |
| `product_family` | Link → Product Family (required) | **Determines attribute structure** |
| `status` | Select | Lifecycle state: `Draft`, `In Review`, `Approved`, `Published`, `End of Life`, `Archived` |
| `brand` | Link → Brand | Product brand reference |
| `manufacturer` | Link → Manufacturer | Product manufacturer reference |
| `attribute_values` | Table → Product Attribute Value | **EAV attribute values** (dynamic) |
| `media` | Table → Product Media | Product images and media files |
| `channels` | Table MultiSelect → Product Channel | Channel assignments |
| `erp_item` | Link → Item | Linked ERPNext Item |
| `auto_sync_to_erp` | Check (default: 1) | Enable auto-sync to ERPNext |

**Product Attribute Value** (child table, `istable: 1`) stores the actual attribute data using the EAV pattern:

| Field | Type | Purpose |
|-------|------|---------|
| `attribute` | Link → PIM Attribute | Which attribute this value is for |
| `locale` | Link → Language (default: `tr`) | Language/locale for this value |
| `value_text` | Small Text | Text value storage |
| `value_long_text` | Text | Long text value storage |
| `value_int` | Int | Integer value storage |
| `value_float` | Float (precision: 6) | Float value storage |
| `value_boolean` | Check | Boolean value storage |
| `value_date` | Date | Date value storage |
| `value_datetime` | Datetime | Datetime value storage |
| `value_link` | Dynamic Link | Link value storage (references `attribute.linked_doctype`) |
| `is_inherited` | Check (read-only) | Whether value was inherited from parent product |
| `inherited_from` | Data (read-only, hidden) | Source of inherited value |

### 1.5 Product Variant Configuration

**DocType:** `Product Variant`
**Purpose:** SKU-level records that inherit from Product Master and are differentiated by variant-defining attributes.

**Key Variant Configurable Fields:**

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `variant_name` | Data (translatable) | SKU display name | Naming conventions vary by industry |
| `variant_code` | Data (unique, no_copy) | SKU code | Auto-generated from family prefix + variant options |
| `product_master` | Link → Product Master | Parent product | Establishes inheritance chain |
| `product_family` | Link → Product Family (fetch_from master) | Family (inherited) | Read-only, cascaded from master |
| `status` | Select | `Draft`, `Active`, `Inactive`, `Archived` | Variant-level lifecycle |
| `option_1_attribute` through `option_4_attribute` | Link → PIM Attribute | Up to 4 variant-defining attributes | Number of axes varies by product type |
| `option_1_value` through `option_4_value` | Data | Values for each variant option | Actual differentiating values |
| `barcode` | Data | EAN/UPC barcode | Required for retail, optional for B2B |
| `price` / `cost_price` | Currency | Variant-level pricing | Per-variant pricing model |
| `weight` | Float (precision: 3) | Weight in kg | Logistics requirements |
| `length` / `width` / `height` | Float (precision: 2) | Dimensions in cm | Shipping calculations |
| `attribute_values` | Table → Product Attribute Value | Variant-specific EAV attributes | Override or supplement master attributes |
| `sync_to_erp` | Check (default: 1) | ERP sync control per variant | Selective sync |

### 1.6 Onboarding Context for the Type System

| Aspect | Details |
|--------|---------|
| **When to Configure** | Phase 1 — this is the **first** customization domain. Must be completed before any product data entry. |
| **Who Configures** | Solution Architect defines the model; PIM Manager implements it in the system. |
| **Dependencies** | PIM Settings must be configured first (for ERP sync direction). PIM Attributes and PIM Attribute Groups must exist before Product Families can reference them. |
| **Typical Duration** | 2–5 days for initial family structure depending on catalog complexity. |
| **Business Impact** | **Critical** — the type system is the foundation of the entire product data model. Changing it after products are created requires data migration. |
| **Reversibility** | Low — changing families or variant axes after product creation is disruptive. Plan carefully. |

#### Configuration Dependencies

```
PIM Settings (Global)
    └── PIM Attribute Groups (General, Dimensions, SEO, Technical)
        └── PIM Attributes (color, size, material, ...)
            └── Product Families (Apparel, Electronics, ...)
                ├── Family Attribute Templates (which attributes per family)
                ├── Family Variant Attributes (which attributes define SKUs)
                └── Product Types (optional high-level classification)
                    └── Product Master (actual product records)
                        └── Product Variant (SKU-level records)
```

---

## 2. Attribute System (EAV Pattern)

### Overview

The PIM attribute system implements an **Entity-Attribute-Value (EAV) pattern** that allows each customer to define an unlimited number of product attributes without schema changes. Rather than adding database columns for every possible product property, the EAV pattern stores attribute definitions centrally (`PIM Attribute`) and persists values in a generic child table (`Product Attribute Value`) with typed storage columns.

**Why EAV?** Traditional relational schemas require a fixed set of columns per table. A fashion retailer needs "sleeve_length" and "fabric_type" while an industrial supplier needs "torque_rating" and "ip_protection_class". The EAV pattern lets each deployment define its own attribute vocabulary at configuration time, making the PIM infinitely extensible without code changes.

**Architecture:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ATTRIBUTE DEFINITION LAYER                          │
│                                                                            │
│  ┌─────────────────┐     ┌─────────────────────┐                          │
│  │ PIM Attribute    │────▶│ PIM Attribute Group  │  (organizational bucket) │
│  │ Group            │     │ General, Dimensions, │                          │
│  │ (fa-cog, #3498db)│     │ SEO, Technical       │                          │
│  └─────────────────┘     └─────────────────────┘                          │
│           │                                                                │
│           ▼                                                                │
│  ┌─────────────────┐                                                      │
│  │ PIM Attribute    │  attribute_code: "color"                             │
│  │ data_type: Select│  options: "Red, Blue, Green"                         │
│  │ is_required: ✓   │  is_localizable: ✗                                  │
│  │ is_filterable: ✓ │  weight_in_completeness: 3                          │
│  └─────────────────┘                                                      │
└─────────────────────�────────────────────────────────────────────────────────┘
           │
           │  Linked via Family Attribute Template (child table)
           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        FAMILY BINDING LAYER                                │
│                                                                            │
│  ┌────────────────────────┐                                               │
│  │ Product Family          │                                               │
│  │ └── attributes (Table)  │─── Family Attribute Template ───┐             │
│  │     ├── color (required)│     attribute: PIM Attribute     │             │
│  │     ├── size  (required)│     is_required_in_family: ✓/✗   │             │
│  │     ├── material        │     default_value: "Cotton"      │             │
│  │     └── care_instr      │     sort_order: 10, 20, 30...   │             │
│  │                         │                                  │             │
│  │ └── variant_attributes  │─── Family Variant Attribute ────┘             │
│  │     ├── color           │     (which attributes define SKUs)            │
│  │     └── size            │                                               │
│  └────────────────────────┘                                               │
└─────────────────────────────────────────────────────────────────────────────┘
           │
           │  Product Master links to Product Family
           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        VALUE STORAGE LAYER                                 │
│                                                                            │
│  ┌─────────────────────────────────┐                                      │
│  │ Product Attribute Value          │  (child table of Product Master)     │
│  │ ├── attribute: "color"           │                                      │
│  │ │   locale: "tr"                 │                                      │
│  │ │   value_text: "Kırmızı"       │                                      │
│  │ ├── attribute: "color"           │                                      │
│  │ │   locale: "en"                 │                                      │
│  │ │   value_text: "Red"            │                                      │
│  │ ├── attribute: "weight"          │                                      │
│  │ │   value_float: 0.450           │                                      │
│  │ └── attribute: "is_organic"      │                                      │
│  │     value_boolean: 1             │                                      │
│  └─────────────────────────────────┘                                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1 PIM Attribute

**DocType:** `PIM Attribute`
**Module:** PIM
**Naming Rule:** `field:attribute_code` (named by the `attribute_code` field)
**Purpose:** Defines a single product attribute — its name, data type, validation constraints, display behavior, and completeness weight. This is the core building block of the entire product data model.

#### Configurable Fields

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `attribute_name` | Data (required, translatable) | — | Display name shown in product forms | Localized per customer language |
| `attribute_code` | Data (required, unique) | Auto-generated from name | URL-safe slug identifier | Referenced in APIs, exports, import mappings |
| `attribute_group` | Link → PIM Attribute Group | — | Organizational bucket | Groups attributes visually on the product form |
| `data_type` | Select (required) | `Text` | Data type — one of 12 types | Determines storage column, validation, and UI widget |
| `options` | Small Text | — | Comma-separated values for Select/Multi Select | Constrains allowed values; visible only when `data_type` ∈ {Select, Multi Select} |
| `linked_doctype` | Link → DocType | — | Target DocType for Link data type | Required when `data_type` = Link; enables referencing ERPNext records |
| `is_required` | Check | `0` | Whether value is mandatory globally | Global requirement across all families using this attribute |
| `is_unique` | Check | `0` | Whether value must be unique per product | Prevents duplicate attribute values (e.g., unique SKU identifier) |
| `min_value` | Float | — | Minimum numeric value | Visible for Integer/Float; enforces floor constraint |
| `max_value` | Float | — | Maximum numeric value | Visible for Integer/Float; enforces ceiling constraint |
| `max_length` | Int | — | Maximum character length | Visible for Text/Long Text; prevents overlong entries |
| `is_filterable` | Check | `0` | Show in filter/facet panel | Affects product list UX and channel export |
| `is_searchable` | Check | `0` | Include in full-text search | Performance impact — only enable for truly searchable fields |
| `show_in_grid` | Check | `1` | Display in list/grid views | Controls product list column visibility |
| `sort_order` | Int | `0` | Display order within group | Lower number = appears first |
| `weight_in_completeness` | Int | `1` | Completeness score weight | `0` = excluded from score; higher = more impact on product readiness |
| `is_localizable` | Check | `0` | Support per-locale values | When enabled, product can store different values per language |
| `is_standard` | Check (read-only) | `0` | System attribute flag | Standard attributes cannot be deleted; set by install hooks |
| `description` | Small Text | — | Internal documentation | Helps content teams understand the attribute's purpose |

#### Attribute Code Validation

The `attribute_code` is the system identifier for the attribute and follows strict validation rules enforced by the controller:

- Must start with a lowercase letter
- May contain only lowercase letters, numbers, and underscores
- Pattern: `^[a-z][a-z0-9_]*$`
- If not provided, auto-generated from `attribute_name` using `frappe.scrub()`

**Examples:** `color`, `sleeve_length`, `torque_rating_nm`, `ip_protection_class`

#### The 12 Data Types — Detailed Reference

Each data type maps to a specific storage column in the `Product Attribute Value` child table and controls the form widget, validation logic, and export behavior:

| # | Data Type | Storage Field | Frappe Widget | Validation | Best For |
|---|-----------|--------------|---------------|------------|----------|
| 1 | **Text** | `value_text` (Small Text) | Single-line input | `max_length` check | Product name, SKU code, short descriptions |
| 2 | **Long Text** | `value_long_text` (Text) | Multi-line textarea | `max_length` check | Full descriptions, care instructions, ingredients |
| 3 | **Integer** | `value_int` (Int) | Numeric input | `min_value`, `max_value` range check; must parse as integer | Pack quantity, MOQ, shelf life days |
| 4 | **Float** | `value_float` (Float, precision 6) | Numeric input with decimals | `min_value`, `max_value` range check; must parse as float | Weight (kg), dimensions (cm), percentage, concentration |
| 5 | **Select** | `value_text` (Small Text) | Dropdown select | Value must exist in comma-separated `options` list | Material type, season, gender, brand tier |
| 6 | **Multi Select** | `value_text` (Small Text) | Multi-select dropdown | Each comma-separated value must exist in `options` | Certifications, features, applicable markets |
| 7 | **Boolean** | `value_boolean` (Check) | Checkbox / toggle | N/A (always 0 or 1) | Is organic, is recyclable, contains allergens |
| 8 | **Date** | `value_date` (Date) | Date picker | Frappe date validation | Manufacturing date, expiry date, launch date |
| 9 | **Datetime** | `value_datetime` (Datetime) | Datetime picker | Frappe datetime validation | Last quality check, last enrichment timestamp |
| 10 | **Link** | `value_link` (Dynamic Link) | Link dropdown with search | Target exists in `linked_doctype`; `linked_doctype` is required | Reference to Brand, Manufacturer, Supplier, Item Group |
| 11 | **Image** | `value_text` (Small Text) | File path / URL input | N/A | Technical drawing URL, certification badge image |
| 12 | **File** | `value_text` (Small Text) | File upload / URL input | N/A | Safety datasheet PDF, user manual, test report |

#### Validation Pipeline

The PIM Attribute controller enforces a strict validation pipeline on every save:

```
validate()
    ├── validate_attribute_code()   → Slug format check (^[a-z][a-z0-9_]*$)
    ├── validate_options()          → Required for Select/Multi Select; deduplicates options
    ├── validate_linked_doctype()   → Required for Link type
    └── validate_value_constraints()→ min_value ≤ max_value for Integer/Float

before_save()
    ├── Clear `options` if not Select/Multi Select
    ├── Clear `linked_doctype` if not Link
    ├── Clear `min_value`/`max_value` if not Integer/Float
    └── Clear `max_length` if not Text/Long Text

on_trash()
    ├── Block deletion of standard attributes (is_standard = 1)
    └── Block deletion if used in any Product Attribute Value records
```

#### Runtime Value Validation API

The system provides a whitelisted API endpoint for validating attribute values at runtime:

**Endpoint:** `frappe.client.call("frappe_pim.pim.doctype.pim_attribute.pim_attribute.validate_attribute_value")`

**Parameters:** `attribute` (PIM Attribute name), `value` (string to validate)

**Validation checks performed:**
1. **Required check** — if `is_required` and value is empty → error
2. **Select validation** — value must be in the defined options list
3. **Multi Select validation** — each comma-separated value must be in the options list
4. **Integer validation** — must parse as int; must be within `min_value`/`max_value` range
5. **Float validation** — must parse as float; must be within `min_value`/`max_value` range
6. **Text length validation** — string length must not exceed `max_length`

**Returns:** `{"valid": true/false, "errors": [...]}`

#### Permissions

| Role | Read | Write | Create | Delete | Export | Import |
|------|------|-------|--------|--------|--------|--------|
| System Manager | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PIM Manager | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PIM User | ✓ | — | — | — | — | — |

### 2.2 PIM Attribute Group

**DocType:** `PIM Attribute Group`
**Module:** PIM
**Naming Rule:** `field:group_code` (named by the `group_code` field)
**Sort:** Sorted by `sort_order ASC` (lower number = first in UI)
**Purpose:** Organizes PIM Attributes into logical visual sections on the product form. Each attribute can belong to at most one group. Ungrouped attributes are displayed in a default "Ungrouped" section at the bottom.

#### Default Groups (Created at Installation)

The installation hook (`setup/install.py`) creates four standard attribute groups:

| Group Name | Group Code | Purpose | Example Attributes |
|------------|-----------|---------|-------------------|
| **General** | `general` | Basic product information | product_name, brand, description, category |
| **Dimensions** | `dimensions` | Physical measurements | weight, height, width, length, volume |
| **SEO** | `seo` | Search engine optimization | meta_title, meta_description, url_slug, keywords |
| **Technical** | `technical` | Technical specifications | voltage, wattage, ip_rating, torque, pressure |

These standard groups have `is_standard: 1` and **cannot be deleted**. However, their display properties (icon, color, sort_order, collapsibility) are fully customizable.

#### Configurable Fields

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `group_name` | Data (required, translatable) | — | Display name | Localized per customer language |
| `group_code` | Data (required, unique) | Auto-generated | URL-safe slug | Referenced in API calls and import templates |
| `sort_order` | Int | `0` (auto-set to next multiple of 10 on save via controller) | Display order | Controls section order on product form |
| `is_standard` | Check (read-only) | `0` | System group flag | Standard groups cannot be deleted |
| `icon` | Data | — | FontAwesome icon class | Visual indicator in group headers (e.g., `fa-cog`, `fa-ruler`, `fa-search`) |
| `color` | Color | — | Hex color code | Visual branding for group sections |
| `is_collapsible` | Check | `0` | Group section can collapse | Reduces visual clutter for dense forms |
| `is_collapsed_default` | Check | `0` | Start collapsed when viewing product | Only active when `is_collapsible` is enabled |
| `description` | Small Text | — | Group description | Internal documentation for implementation teams |

#### Group Code Validation

Same pattern as PIM Attribute: `^[a-z][a-z0-9_]*$`, auto-generated from `group_name` if not provided.

#### Sort Order Auto-Assignment

When a new group is created without an explicit `sort_order`, the controller auto-assigns the next available slot by incrementing the maximum existing sort_order by 10. This creates a natural spacing (10, 20, 30, ...) that allows inserting groups between existing ones without reordering.

#### API Endpoints

| Endpoint | Purpose | Returns |
|----------|---------|---------|
| `get_attribute_groups()` | List all groups ordered by sort_order | `[{name, group_name, group_code, icon, color, sort_order}]` |
| `get_attributes_by_group(group)` | List attributes in a specific group | `[{name, attribute_name, attribute_code, data_type, is_required, sort_order}]` |
| `get_grouped_attributes()` | All attributes organized by group | `[{group: {...}, attributes: [...]}]` — includes "Ungrouped" pseudo-group |
| `reorder_groups(order)` | Reorder groups by providing a JSON list of group names | `{"success": true}` |

#### Customer Archetype Examples — Attribute Groups

**Fashion Retailer:**
```
Attribute Groups:
  ├── General        (sort: 10, icon: fa-tshirt, color: #3498db)
  │   └── brand, collection, season, gender, style, occasion
  ├── Sizing         (sort: 20, icon: fa-ruler, color: #e74c3c)  ← custom group
  │   └── size, fit, size_chart_url, model_height, model_size
  ├── Materials      (sort: 30, icon: fa-layer-group, color: #2ecc71)  ← custom group
  │   └── fabric_type, fabric_composition, care_instructions, origin_country
  ├── SEO            (sort: 40, icon: fa-search, color: #9b59b6, collapsible: ✓)
  │   └── meta_title, meta_description, url_slug
  └── Compliance     (sort: 50, icon: fa-certificate, color: #f39c12)  ← custom group
      └── reach_compliant, oeko_tex, grs_certified
```

**Industrial Supplier:**
```
Attribute Groups:
  ├── General        (sort: 10, icon: fa-cog)
  │   └── part_number, manufacturer, series, category
  ├── Technical      (sort: 20, icon: fa-microchip, color: #e67e22)
  │   └── voltage, current, power_rating, operating_temp, ip_rating
  ├── Dimensions     (sort: 30, icon: fa-ruler-combined, color: #3498db)
  │   └── weight, height, width, depth, thread_size
  ├── Certifications (sort: 40, icon: fa-shield-alt, color: #27ae60)  ← custom group
  │   └── ul_listed, ce_marked, rohs_compliant, atex_rated
  └── Logistics      (sort: 50, icon: fa-truck, collapsible: ✓, collapsed: ✓)  ← custom group
      └── lead_time_days, moq, packaging_type, country_of_origin
```

**Food Manufacturer:**
```
Attribute Groups:
  ├── General        (sort: 10, icon: fa-apple-alt, color: #27ae60)
  │   └── brand, product_line, flavor, variant
  ├── Nutrition      (sort: 20, icon: fa-heartbeat, color: #e74c3c)  ← custom group
  │   └── calories, protein_g, fat_g, carbs_g, fiber_g, sodium_mg
  ├── Allergens      (sort: 30, icon: fa-exclamation-triangle, color: #f39c12)  ← custom group
  │   └── contains_gluten, contains_dairy, contains_nuts, contains_soy
  ├── Regulatory     (sort: 40, icon: fa-gavel, color: #8e44ad)  ← custom group
  │   └── organic_certified, halal, kosher, non_gmo, shelf_life_days
  ├── Storage        (sort: 50, icon: fa-thermometer-half, color: #2980b9)  ← custom group
  │   └── storage_temp_min, storage_temp_max, refrigeration_required
  └── SEO            (sort: 60, icon: fa-search, collapsible: ✓, collapsed: ✓)
      └── meta_title, meta_description, url_slug
```

### 2.3 PIM Attribute Template (Family-Attribute Binding)

The Attribute Template is **not a standalone DocType** — it is a **child table** (`Family Attribute Template`) embedded within `Product Family`. It serves as the binding layer that determines which PIM Attributes appear on products of a given family and how they behave within that family context.

> **Key Insight:** A PIM Attribute exists globally (one definition of "color" across the system), but each Product Family can independently control whether "color" is required, what its default value is, and where it appears in the form order. This is the **family-attribute-template linking pattern**.

**DocType:** `Family Attribute Template` (child table, `istable: 1`)
**Parent DocType:** `Product Family` (field: `attributes`)

#### Configurable Fields

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `attribute` | Link → PIM Attribute (required) | — | Which attribute to include in this family | Core product model definition |
| `is_required_in_family` | Check | `0` | Whether this attribute is mandatory **within this family** | Overrides or complements the global `is_required` on PIM Attribute |
| `default_value` | Small Text | — | Pre-filled value for new products in this family | Accelerates data entry; can encode business rules |
| `sort_order` | Int | `0` | Display order within the product form | Controls attribute layout per family |

#### The Two-Level Requirement Pattern

The PIM implements a **two-level requirement model** for attributes:

```
PIM Attribute.is_required = Global Requirement
    "This attribute MUST have a value on ANY product that uses it"
    Example: product_name is_required globally — every product needs a name

Family Attribute Template.is_required_in_family = Family-Level Requirement
    "This attribute is mandatory for products in THIS specific family"
    Example: fabric_type is required for the "Apparel" family but not for "Electronics"
```

**Effective requirement = Global OR Family-level.** If either flag is set, the attribute is mandatory for products in that family.

#### Default Value Strategies

The `default_value` field supports several strategies depending on the attribute's data type:

| Data Type | Default Value Example | Use Case |
|-----------|-----------------------|----------|
| Text | `"Standard"` | Default product line |
| Select | `"Unisex"` | Default gender for gender-neutral products |
| Integer | `"1"` | Default minimum order quantity |
| Float | `"0.0"` | Default weight placeholder |
| Boolean | `"1"` (checked) | Default "is_active" to true |
| Date | — (typically not pre-filled) | — |
| Multi Select | `"CE, RoHS"` | Pre-check common certifications |

#### Attribute Inheritance via Family Hierarchy

When a Product Family has `inherit_parent_attributes: 1` (default), it automatically inherits all attributes from its parent family. The inheritance chain follows the `parent_family` tree structure:

```
Apparel (parent)
    attributes: [brand, collection, season, gender, fabric_composition, care_instructions]

    └── Tops (child, inherit_parent_attributes: ✓)
        inherited: [brand, collection, season, gender, fabric_composition, care_instructions]
        own:       [sleeve_length, neckline]
        effective: [brand, collection, season, gender, fabric_composition, care_instructions,
                    sleeve_length, neckline]

        └── T-Shirts (grandchild, inherit_parent_attributes: ✓)
            inherited: [brand, collection, season, gender, fabric_composition,
                        care_instructions, sleeve_length, neckline]
            own:       [fit, print_type]
            effective: [brand, collection, season, gender, fabric_composition,
                        care_instructions, sleeve_length, neckline, fit, print_type]
```

**Key inheritance rules:**
- Inherited attributes appear on the product form alongside the family's own attributes
- The `is_required_in_family` flag is **not inherited** — each family independently controls what's required
- `default_value` is **not inherited** — each family can set its own defaults
- `sort_order` merges inherited and own attributes, allowing interleaving
- Setting `inherit_parent_attributes: 0` on a child family creates a clean break — no parent attributes carry over

#### Linking Pattern Summary

```
Step 1: Create PIM Attribute Groups
    general, dimensions, seo, technical + custom groups

Step 2: Create PIM Attributes
    color (Select, group: general, options: "Red, Blue, Green, Black, White")
    size  (Select, group: general, options: "XS, S, M, L, XL, XXL")
    weight_kg (Float, group: dimensions, min: 0.01, max: 50.0)
    ...

Step 3: Create Product Family with Attribute Template
    Family: "T-Shirts" (family_code: tshirts, prefix: TSH-)
    └── attributes (Family Attribute Template):
        ├── color       → required: ✓, default: —, sort: 10
        ├── size        → required: ✓, default: "M", sort: 20
        ├── fabric_type → required: ✓, default: "Cotton", sort: 30
        ├── weight_kg   → required: ✗, default: —, sort: 40
        └── care_instr  → required: ✗, default: "Machine wash cold", sort: 50

Step 4: Create Product Master in this Family
    Product Master auto-populates attribute form based on family's template
    └── attribute_values (Product Attribute Value):
        ├── color: "Red" (value_text)
        ├── size: "M" (value_text, from default)
        ├── fabric_type: "Cotton" (value_text, from default)
        ├── weight_kg: 0.250 (value_float)
        └── care_instr: "Machine wash cold" (value_text, from default)
```

### 2.4 Product Attribute Value (EAV Storage)

**DocType:** `Product Attribute Value` (child table, `istable: 1`)
**Parent DocTypes:** `Product Master` (field: `attribute_values`), `Product Variant` (field: `attribute_values`)
**Purpose:** The EAV value storage table — each row stores one attribute value for one product in one locale.

#### Storage Schema

| Field | Type | Purpose |
|-------|------|---------|
| `attribute` | Link → PIM Attribute (required) | References the attribute definition |
| `locale` | Link → Language (default: `tr`) | Language/locale for this value |
| `value_text` | Small Text | Storage for Text, Select, Multi Select, Image, File |
| `value_long_text` | Text | Storage for Long Text |
| `value_int` | Int | Storage for Integer |
| `value_float` | Float (precision: 6) | Storage for Float |
| `value_boolean` | Check | Storage for Boolean |
| `value_date` | Date | Storage for Date |
| `value_datetime` | Datetime | Storage for Datetime |
| `value_link` | Dynamic Link → `attribute.linked_doctype` | Storage for Link |
| `is_inherited` | Check (read-only) | Whether this value was inherited from parent product/variant |
| `inherited_from` | Data (read-only, hidden) | Source document of inheritance |

#### Multi-Locale Pattern

For **localizable attributes** (`is_localizable: 1`), the same attribute can have multiple rows in `Product Attribute Value` — one per locale:

```
Product: "Organic Cotton T-Shirt" (Product Master)
└── attribute_values:
    ├── attribute: "product_name", locale: "tr", value_text: "Organik Pamuklu Tişört"
    ├── attribute: "product_name", locale: "en", value_text: "Organic Cotton T-Shirt"
    ├── attribute: "product_name", locale: "de", value_text: "Bio-Baumwoll-T-Shirt"
    ├── attribute: "description", locale: "tr", value_long_text: "Yumuşak organik pamuktan..."
    ├── attribute: "description", locale: "en", value_long_text: "Made from soft organic cotton..."
    ├── attribute: "color", locale: "tr", value_text: "Kırmızı"    ← (non-localizable attributes
    └── attribute: "weight_kg", value_float: 0.250                      use a single row)
```

#### Value Inheritance (Master → Variant)

Product Variants can inherit attribute values from their parent Product Master. When a variant inherits a value:
- `is_inherited` = 1
- `inherited_from` = parent Product Master name
- The value is **read-only** on the variant until explicitly overridden

Variant-specific attributes (those listed in `Family Variant Attribute`) always have their own unique values and are never inherited.

#### Database Indexing

The installation hook creates a composite index for optimal EAV query performance:

```sql
CREATE INDEX IF NOT EXISTS idx_pav_parent_attr
    ON `tabProduct Attribute Value` (parent, attribute)
```

This index accelerates the most common query pattern: "Get all attribute values for a specific product."

### 2.5 Completeness Score Integration

Each PIM Attribute contributes to the product's completeness score based on its `weight_in_completeness` field:

| Weight | Meaning |
|--------|---------|
| `0` | Excluded from completeness calculation (informational-only attribute) |
| `1` | Standard weight (default) |
| `2-5` | Higher weight = more impact on completeness score |
| `5+` | Critical attribute — absence significantly impacts completeness |

**Example — Fashion Product Completeness:**

```
Attribute                weight_in_completeness    Impact
────────────────────     ─────────────────────     ──────
product_name             5                         Critical — always needed
description              4                         Very important for SEO
color                    3                         Important for filtering
fabric_composition       3                         Required for compliance
care_instructions        2                         Standard importance
meta_title               2                         SEO optimization
meta_description         2                         SEO optimization
model_height             1                         Nice-to-have
style_notes              0                         Excluded from score
```

The Product Family's `completeness_threshold` (default: 80%) determines when a product is considered "complete." Combined with attribute weights, this creates a flexible per-family quality gate.

### 2.6 Onboarding Context for the Attribute System

| Aspect | Details |
|--------|---------|
| **When to Configure** | Phase 1 — immediately after PIM Settings and before Product Families. Attribute Groups first, then PIM Attributes. |
| **Who Configures** | Solution Architect designs the attribute model; PIM Manager implements it. System Manager sets up standard groups at installation. |
| **Dependencies** | PIM Attribute Groups must exist before creating PIM Attributes (optional but recommended). PIM Attributes must exist before they can be added to Family Attribute Templates. |
| **Typical Duration** | 1–3 days for attribute group and attribute creation depending on catalog complexity (50–500+ attributes). |
| **Business Impact** | **Critical** — attributes define what data can be captured about products. Missing attributes mean missing data; wrong data types mean validation failures and export errors. |
| **Reversibility** | **Medium** — Attribute Groups can be freely reorganized. PIM Attributes can be renamed but not easily re-typed after values exist. Attributes in use cannot be deleted. |

#### Configuration Sequence

```
1. Review & customize Attribute Groups
   ├── Keep default groups (General, Dimensions, SEO, Technical)
   ├── Add industry-specific groups (Nutrition, Allergens, Certifications, etc.)
   └── Set display properties (icons, colors, sort_order, collapsibility)

2. Define PIM Attributes
   ├── Map customer's product data dictionary to PIM Attributes
   ├── Choose appropriate data_type for each attribute
   ├── Configure validation rules (min/max, max_length, options)
   ├── Set filterable/searchable flags for catalog UX
   ├── Assign completeness weights based on business priority
   └── Mark localizable attributes for multi-language support

3. Build Family Attribute Templates (inside Product Family)
   ├── Assign relevant attributes to each family
   ├── Set family-specific requirement flags
   ├── Configure default values for data entry acceleration
   ├── Set sort_order for form layout
   └── Verify inheritance chain for hierarchical families

4. Verify the complete attribute model
   ├── Create test product in each family
   ├── Confirm all expected attributes appear on form
   ├── Test validation rules (min/max, required, options)
   ├── Verify completeness score calculation
   └── Test localized attribute values if multi-language is enabled
```

#### Industry-Specific Attribute Planning Guide

**Fashion (200-400 attributes typical):**
```
Must-have attributes:
  General:     brand, collection, season, gender, style, occasion, target_age
  Sizing:      size, fit, size_chart, model_height, model_size
  Materials:   fabric_type, fabric_composition (%), care_instructions, origin
  Visual:      color, pattern, print_type, finish
  Compliance:  reach_compliant, oeko_tex, grs_certified, fur_free
  SEO:         meta_title, meta_description, url_slug, keywords

Key decisions:
  - color as Select (fixed palette) vs. Text (free-form)? → Select recommended
  - fabric_composition as Text vs. structured Float per fiber? → Text for simplicity
  - size as Select (per family) vs. Text? → Select with family-specific options
```

**Industrial / B2B (100-300 attributes typical):**
```
Must-have attributes:
  General:     part_number, manufacturer, series, product_line
  Technical:   voltage, current_rating, power_rating, frequency
  Physical:    operating_temp_min, operating_temp_max, ip_rating, weight_kg
  Dimensions:  height_mm, width_mm, depth_mm, thread_size
  Compliance:  ul_listed, ce_marked, rohs_compliant, atex_zone
  Logistics:   lead_time_days, moq, country_of_origin, hs_code

Key decisions:
  - Use Float with min/max for engineering values (enables range validation)
  - ip_rating as Select (IP20, IP44, IP65, IP67, IP68) — finite set
  - thread_size as Select (M3, M4, M5, M6...) — standardized values
  - Include linked_doctype attributes for referencing ERPNext Suppliers/Manufacturers
```

**Food & Beverage (150-350 attributes typical):**
```
Must-have attributes:
  General:     brand, product_line, flavor, variant_description
  Nutrition:   calories, protein_g, fat_g, saturated_fat_g, carbs_g, sugar_g,
               fiber_g, sodium_mg, serving_size, servings_per_container
  Allergens:   contains_gluten, contains_dairy, contains_nuts, contains_soy,
               contains_eggs, contains_fish, contains_shellfish, may_contain
  Regulatory:  organic_certified, halal, kosher, non_gmo, fair_trade
  Storage:     shelf_life_days, storage_temp_min_c, storage_temp_max_c,
               refrigeration_required, freeze_thaw_cycles
  Packaging:   net_weight_g, gross_weight_g, pack_size, units_per_case

Key decisions:
  - Nutrition values as Float with min_value: 0 (can't have negative calories)
  - Allergen flags as Boolean — simple yes/no for each allergen type
  - shelf_life_days as Integer with min_value: 1
  - Use completeness weights heavily — regulatory attributes get weight 5
```

---

## 3. Global Settings (PIM Settings)

### Overview

**DocType:** `PIM Settings`
**Module:** PIM
**Type:** Single (singleton — only one instance exists per site, `issingle: 1`)
**Track Changes:** Yes (`track_changes: 1`)

> **Implementation Status:** The `PIM Settings` DocType JSON definition (`pim_settings.json`) does not yet exist in the codebase as a committed file. The fields, APIs, and behaviors described below represent the **planned architecture** based on how the DocType is referenced throughout the codebase. Currently, `erp_sync.py` defensively reads `enable_erp_sync`, `auto_create_variant_from_item`, and `auto_create_item_from_variant` via `frappe.db.get_single_value()` calls that gracefully handle the DocType's absence (defaulting to `True` for sync enabled). Creating the PIM Settings DocType via Frappe's DocType builder is a prerequisite for enabling most of the functionality described in this section.

PIM Settings is the **global configuration hub** for the entire PIM system. It is the first DocType that must be configured during onboarding because nearly every other module reads its values at runtime. The settings are organized into **7 functional groups** covering ERP integration, channel defaults, AI enrichment, data quality, GS1/GDSN standards, and media management.

**When to Configure:** Phase 0 — the very first step in any PIM onboarding
**Who Configures:** System Manager (initial setup), PIM Manager (ongoing tuning)
**Business Impact:** Determines the operational envelope for the entire PIM — which features are active, how products flow to ERP, and what quality gates apply

#### Access Permissions

| Role | Read | Write | Create |
|------|------|-------|--------|
| System Manager | ✓ | ✓ | ✓ |
| PIM Manager | ✓ | ✓ | — |
| PIM User | ✓ (read-only) | — | — |

> **Note:** PIM Users can view the current settings (useful for understanding why certain features are enabled/disabled) but cannot modify them. Only System Manager and PIM Manager roles can change PIM Settings.

### 3.1 ERP Integration Settings

Controls the bidirectional synchronization between PIM and ERPNext Item DocType. This is the most consequential setting group — it determines whether the PIM operates as the system of record, a downstream consumer of ERP data, or a bidirectional peer.

| Field | Type | Default | Options | Description | Per-Customer Impact |
|-------|------|---------|---------|-------------|-------------------|
| `enable_erp_sync` | Check | `1` (enabled) | — | Master toggle for ERP synchronization | Disabling disconnects PIM from ERPNext entirely; use for standalone PIM deployments |
| `sync_direction` | Select | `Bidirectional` | `PIM to ERP`, `ERP to PIM`, `Bidirectional` | Direction of data flow between systems | Determines which system is the source of truth for product data |
| `sync_on_save` | Check | `1` (enabled) | — | Automatically sync when a product is saved | When disabled, sync must be triggered manually or via scheduled job |
| `auto_create_variant_from_item` | Check | `0` (disabled) | — | Auto-create PIM Product Variants when ERPNext Item variants are created | Enable for ERP-first workflows where variants originate in ERPNext |
| `auto_create_item_from_variant` | Check | `0` (disabled) | — | Auto-create ERPNext Items when PIM Product Variants are synced to ERP | Enable for PIM-first workflows where products originate in PIM |

**Visibility Dependencies:**
- `sync_direction` and `sync_on_save` are only visible when `enable_erp_sync` is enabled
- `auto_create_variant_from_item` is always visible (independent toggle)

#### Sync Direction Decision Guide

| Direction | Source of Truth | Use Case | Trade-offs |
|-----------|----------------|----------|------------|
| **PIM to ERP** | PIM is master | Content-first workflows where marketing team enriches products before ERP sees them | ERP changes to shared fields will be overwritten on next sync |
| **ERP to PIM** | ERP is master | Operations-first workflows where procurement creates items in ERP, then PIM enriches | PIM enrichment cannot modify ERP-sourced fields |
| **Bidirectional** | Both systems contribute | Collaborative workflows — ERP owns logistics fields, PIM owns marketing fields | Requires clear field ownership rules; risk of sync conflicts |

**Runtime Check:**
- `_is_pim_sync_enabled()` — internal helper in `erp_sync.py` that reads `enable_erp_sync` from PIM Settings; defaults to `True` if PIM Settings DocType doesn't exist
- Used by all sync functions in `erp_sync.py` to gate sync operations

#### Customer Archetype Recommendations — ERP Integration

```
Fashion Retailer (content-first):
  enable_erp_sync: ✓
  sync_direction: "PIM to ERP"
  sync_on_save: ✓
  auto_create_variant_from_item: ✗
  Rationale: Marketing/content team creates and enriches products in PIM.
  ERP receives finished product data for inventory and fulfillment.

Industrial Supplier (operations-first):
  enable_erp_sync: ✓
  sync_direction: "Bidirectional"
  sync_on_save: ✗ (manual sync — engineering review needed)
  auto_create_variant_from_item: ✓
  Rationale: Procurement creates Items in ERP, engineering adds specs in PIM.
  Both systems contribute data. Manual sync to avoid premature publication.

Food Manufacturer (compliance-driven):
  enable_erp_sync: ✓
  sync_direction: "PIM to ERP"
  sync_on_save: ✓
  auto_create_variant_from_item: ✗
  Rationale: Regulatory data must be validated in PIM before flowing to ERP.
  PIM is the compliance-checked source of truth.

Standalone PIM (no ERPNext):
  enable_erp_sync: ✗
  sync_direction: (irrelevant)
  sync_on_save: (irrelevant)
  auto_create_variant_from_item: ✗
  Rationale: PIM operates independently, exports data via channels/exports.
```

### 3.2 Channel Settings

Controls default behavior for product distribution channels and export operations.

| Field | Type | Default | Options | Description | Per-Customer Impact |
|-------|------|---------|---------|-------------|-------------------|
| `default_channel` | Link → Channel | — (none) | Any configured `Channel` record | Default distribution channel for new products | Determines which channel requirements are applied by default to new products |
| `auto_publish_to_default` | Check | `0` (disabled) | — | Automatically publish products to the default channel when marked as ready | When enabled, products reaching "Approved" status auto-publish; use with caution |
| `default_export_format` | Select | `JSON` | `JSON`, `XML`, `CSV`, `XLSX`, `BMEcat` | Default format for product data exports | Drives one-click export behavior; different channels may override this |

**Visibility Dependencies:**
- `auto_publish_to_default` is only visible when `default_channel` is set

#### Export Format Guide

| Format | Best For | Typical Channels |
|--------|----------|-----------------|
| **JSON** | API integrations, developer tools | Custom integrations, headless commerce |
| **XML** | Structured B2B data exchange | BMEcat, cXML, EDIFACT, GS1 XML |
| **CSV** | Bulk imports/exports, spreadsheet tools | Google Merchant, basic marketplace uploads |
| **XLSX** | Human-readable exports, customer review | Internal review, customer approval workflows |
| **BMEcat** | European B2B product catalogs | Procurement platforms, B2B marketplaces |

#### Customer Archetype Recommendations — Channel Settings

```
Fashion Retailer (multi-channel):
  default_channel: "Shopify" or "Web Store"
  auto_publish_to_default: ✗ (approval required before publishing)
  default_export_format: "JSON"
  Rationale: Fashion products need visual QA before going live. JSON for API integrations.

Industrial Supplier (B2B catalog):
  default_channel: "B2B Portal" or none
  auto_publish_to_default: ✗
  default_export_format: "BMEcat" or "XLSX"
  Rationale: B2B products require technical review. BMEcat for European procurement standards.

Food Manufacturer (regulated):
  default_channel: "Internal Catalog"
  auto_publish_to_default: ✗
  default_export_format: "XLSX"
  Rationale: Regulatory compliance requires multi-step review before any channel publish.

Small/Medium Business (simple):
  default_channel: "Trendyol" or "Shopify"
  auto_publish_to_default: ✓ (streamlined workflow)
  default_export_format: "CSV"
  Rationale: Lean teams need fast time-to-market. Auto-publish with quality score gate.
```

### 3.3 AI Enrichment Settings

Controls AI-powered content generation including product descriptions, attribute extraction, categorization, and translation. This is a premium feature that requires external API credentials.

| Field | Type | Default | Options | Description | Per-Customer Impact |
|-------|------|---------|---------|-------------|-------------------|
| `enable_ai_enrichment` | Check | `0` (disabled) | — | Master toggle for all AI features | When disabled, AI enrichment jobs, auto-categorization, and AI translation are all unavailable |
| `ai_provider` | Select | — (none) | `OpenAI`, `Anthropic`, `Google Gemini`, `Azure OpenAI` | AI service provider | Each provider has different capabilities, pricing, and data residency implications |
| `ai_api_key` | Password | — (none) | — | API key for the selected provider (stored encrypted in database) | **Security-sensitive** — stored using Frappe's password encryption; never exposed in API responses |
| `ai_model` | Data | — (none) | Free text (e.g., `gpt-4`, `claude-3-opus`, `gemini-pro`) | Specific model to use | Controls quality/cost/speed trade-off; newer models may not be available in all regions |
| `ai_require_approval` | Check | `1` (enabled) | — | Require human approval before applying AI-generated content | **Strongly recommended** — disabling allows AI to auto-apply content without review |

**Visibility Dependencies:**
- `ai_provider` is only visible when `enable_ai_enrichment` is enabled
- `ai_api_key` and `ai_model` are only visible when both `enable_ai_enrichment` is enabled AND `ai_provider` is selected
- `ai_require_approval` is visible when `enable_ai_enrichment` is enabled

#### AI Provider Comparison

| Provider | Models | Strengths | Considerations |
|----------|--------|-----------|---------------|
| **OpenAI** | `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo` | Best general-purpose quality; wide language support | US-hosted; data processing implications for EU customers |
| **Anthropic** | `claude-3-opus`, `claude-3-sonnet`, `claude-3-haiku` | Strong instruction-following; safety-focused | Good for regulated industries; available in US and EU |
| **Google Gemini** | `gemini-pro`, `gemini-1.5-pro` | Strong multimodal (image → text); competitive pricing | Google Cloud dependency; good for media-heavy catalogs |
| **Azure OpenAI** | Same as OpenAI via Azure | Enterprise compliance; regional data residency | Requires Azure subscription; complex setup (endpoint configuration) |

**Planned Runtime APIs** (to be implemented when PIM Settings DocType is created):
- `is_ai_enrichment_enabled()` — would return `True` only when `enable_ai_enrichment` AND `ai_provider` AND `ai_api_key` are all configured
- `get_ai_config()` — would return `{provider, model, require_approval}` dict, or `None` if not enabled
- `test_ai_connection()` — would test the API connection for each provider with a minimal request; returns `{status: "success"|"error"|"info", message: "..."}`

#### AI Connection Test Details

The `test_ai_connection()` API performs provider-specific validation:

| Provider | Test Method | Success Indicator |
|----------|------------|-------------------|
| OpenAI | `GET /v1/models` with Bearer auth | HTTP 200 |
| Anthropic | `POST /v1/messages` with minimal prompt | HTTP 200 |
| Google Gemini | `GET /v1/models` with API key param | HTTP 200 |
| Azure OpenAI | N/A — returns info message | Manual verification required |

#### Customer Archetype Recommendations — AI Enrichment

```
Fashion Retailer (high volume, creative content):
  enable_ai_enrichment: ✓
  ai_provider: "OpenAI" or "Anthropic"
  ai_model: "gpt-4" or "claude-3-sonnet"
  ai_require_approval: ✓
  Rationale: AI generates marketing descriptions, SEO titles, and translations.
  Human approval ensures brand voice consistency.

Industrial Supplier (technical accuracy paramount):
  enable_ai_enrichment: ✓ (for categorization only)
  ai_provider: "Anthropic"
  ai_model: "claude-3-opus"
  ai_require_approval: ✓ (always)
  Rationale: AI helps categorize/tag products but technical specs must be human-verified.
  Anthropic's instruction-following reduces hallucination risk for technical content.

Food Manufacturer (regulatory compliance):
  enable_ai_enrichment: ✗ or ✓ with strict approval
  ai_provider: (if enabled) "Anthropic" or "Azure OpenAI"
  ai_model: (if enabled) "claude-3-opus"
  ai_require_approval: ✓ (mandatory — regulatory risk)
  Rationale: AI-generated content for food products carries regulatory liability.
  If enabled, use only for non-regulatory fields (marketing copy, not nutrition facts).

Budget-Conscious / Minimal Setup:
  enable_ai_enrichment: ✗
  Rationale: AI adds recurring API costs. Small catalogs can be manually enriched.
```

### 3.4 Data Quality Settings

Controls the automated data quality scoring engine that evaluates products against configurable completeness and quality thresholds.

| Field | Type | Default | Options | Description | Per-Customer Impact |
|-------|------|---------|---------|-------------|-------------------|
| `enable_quality_scoring` | Check | `1` (enabled) | — | Master toggle for quality score calculation | Disabling removes quality scores from product views and removes publish gates |
| `minimum_quality_score` | Percent | `60` | 0–100 | Minimum quality score required for publishing | Higher threshold = stricter publish gate; lower = faster time-to-market |
| `block_publish_below_minimum` | Check | `0` (disabled) | — | Hard-block publishing products below the minimum quality score | When enabled, products cannot be published to any channel below the threshold |
| `auto_scan_on_save` | Check | `1` (enabled) | — | Automatically scan for data quality issues when a product is saved | Provides real-time quality feedback; disable for bulk import performance |

**Visibility Dependencies:**
- `minimum_quality_score`, `block_publish_below_minimum`, and `auto_scan_on_save` are only visible when `enable_quality_scoring` is enabled

**Validation Rules (enforced by controller):**
- `minimum_quality_score` must be between 0 and 100 (inclusive)

**Planned Runtime API** (to be implemented when PIM Settings DocType is created):
- `get_quality_config()` — would return `{enabled, minimum_score, block_publish, auto_scan}`

#### Quality Score vs. Publish Gate Matrix

| `enable_quality_scoring` | `block_publish_below_minimum` | Behavior |
|--------------------------|-------------------------------|----------|
| ✗ | (ignored) | No quality scoring; products can be published freely |
| ✓ | ✗ | Quality scores are calculated and displayed, but do not block publishing (advisory mode) |
| ✓ | ✓ | Quality scores are calculated AND products below `minimum_quality_score` cannot be published (enforcement mode) |

#### Customer Archetype Recommendations — Data Quality

```
Fashion Retailer (brand-conscious):
  enable_quality_scoring: ✓
  minimum_quality_score: 85
  block_publish_below_minimum: ✓
  auto_scan_on_save: ✓
  Rationale: Brand reputation requires high-quality product data.
  85% threshold ensures images, descriptions, and key attributes are filled.

Industrial Supplier (safety-critical):
  enable_quality_scoring: ✓
  minimum_quality_score: 95
  block_publish_below_minimum: ✓
  auto_scan_on_save: ✓
  Rationale: Missing technical specs or safety data can cause liability issues.
  95% threshold ensures near-complete product data before publication.

Food Manufacturer (regulatory):
  enable_quality_scoring: ✓
  minimum_quality_score: 98
  block_publish_below_minimum: ✓
  auto_scan_on_save: ✓
  Rationale: Regulatory requirements demand virtually complete product data.
  Only non-critical optional fields can be missing at publish time.

Startup / Quick Launch:
  enable_quality_scoring: ✓
  minimum_quality_score: 50
  block_publish_below_minimum: ✗ (advisory only)
  auto_scan_on_save: ✓
  Rationale: Focus on getting products live fast; improve quality over time.
  Scores are visible but don't block workflow.
```

### 3.5 GS1/GDSN Settings

Controls GS1 identifier validation and GDSN (Global Data Synchronisation Network) data pool integration. Required for customers participating in retail supply chains that mandate GS1 standards.

| Field | Type | Default | Options | Description | Per-Customer Impact |
|-------|------|---------|---------|-------------|-------------------|
| `enable_gs1_validation` | Check | `0` (disabled) | — | Validate GTINs (EAN/UPC barcodes) and other GS1 identifiers | When enabled, barcode fields are validated against GS1 check-digit algorithms |
| `gln` | Data | — (none) | 13-digit numeric string | Company Global Location Number | Identifies the organization in GS1 ecosystem; required for GDSN data pool submissions |
| `gs1_data_pool` | Select | — (none) | `1WorldSync`, `SA2 Worldsync`, `EDITEUR`, `GS1 Turkey` | GDSN data pool for product synchronization | Determines which data pool receives product information |
| `data_pool_api_key` | Password | — (none) | — | API key for the selected GDSN data pool (stored encrypted) | Required for automated GDSN synchronization |

**Visibility Dependencies:**
- `gln` and `gs1_data_pool` are only visible when `enable_gs1_validation` is enabled
- `data_pool_api_key` is only visible when `gs1_data_pool` is selected

**Validation Rules (enforced by controller):**
- `gln` must be exactly 13 digits (`^\d{13}$`)
- GLN check digit is validated using the GS1 standard algorithm (alternating multiply by 1 and 3, mod 10 check)
- Invalid GLN throws a user-friendly error: "GLN must be exactly 13 digits" or "Invalid GLN check digit"

#### GS1 Data Pool Guide

| Data Pool | Coverage | Use Case |
|-----------|----------|----------|
| **1WorldSync** | Global (largest GDSN data pool) | Multinational retailers and suppliers (Walmart, Carrefour, Metro) |
| **SA2 Worldsync** | Global | European-focused supply chains |
| **EDITEUR** | Publishing industry | Book and media publishers using ISBN/ISSN |
| **GS1 Turkey** | Turkey domestic | Turkish domestic retail and B2B supply chains |

#### Customer Archetype Recommendations — GS1/GDSN

```
Fashion Retailer (domestic):
  enable_gs1_validation: ✓
  gln: (customer's GS1 Turkey GLN)
  gs1_data_pool: "GS1 Turkey"
  Rationale: Turkish marketplaces (Trendyol, Hepsiburada, N11) require valid GTINs.

Multinational Supplier:
  enable_gs1_validation: ✓
  gln: (customer's global GLN)
  gs1_data_pool: "1WorldSync"
  Rationale: Global retailers mandate GDSN synchronization for product data.

B2B / Industrial (no retail):
  enable_gs1_validation: ✗
  Rationale: Industrial products often use proprietary part numbers, not GTINs.
  GS1 validation adds unnecessary constraints for non-retail workflows.

Startup / MVP:
  enable_gs1_validation: ✗
  Rationale: GS1 membership requires registration fees. Enable when scaling to retail.
```

### 3.6 Media Settings

Controls image processing, thumbnail generation, file size limits, and allowed formats for product media uploads.

| Field | Type | Default | Options | Description | Per-Customer Impact |
|-------|------|---------|---------|-------------|-------------------|
| `auto_generate_thumbnails` | Check | `1` (enabled) | — | Automatically generate thumbnail images when media is uploaded | Saves manual effort; ensure server has image processing capabilities (Pillow) |
| `thumbnail_size` | Int | `150` | 50–500 px | Maximum dimension (width or height) for generated thumbnails | Larger thumbnails = higher storage; smaller = faster page loads but lower quality |
| `max_image_size_mb` | Int | `10` | — | Maximum allowed image file size in megabytes | Protects server storage; too restrictive may block high-resolution product photography |
| `allowed_image_formats` | Data | `jpg,jpeg,png,webp,gif` | Comma-separated from: `jpg`, `jpeg`, `png`, `webp`, `gif`, `bmp`, `tiff`, `svg` | Allowed image file extensions | Controls which image formats can be uploaded |

**Visibility Dependencies:**
- `thumbnail_size` is only visible when `auto_generate_thumbnails` is enabled

**Validation Rules (enforced by controller):**
- `thumbnail_size` must be between 50 and 500 pixels (inclusive)
- `allowed_image_formats` entries are validated against the whitelist: `jpg`, `jpeg`, `png`, `webp`, `gif`, `bmp`, `tiff`, `svg`
- Invalid format names throw: "Invalid image format: {fmt}. Allowed: jpg, jpeg, png, webp, gif, bmp, tiff, svg"
- Format strings are normalized to lowercase on save

**Planned Runtime API** (to be implemented when PIM Settings DocType is created):
- `get_media_config()` — would return `{auto_thumbnails, thumbnail_size, max_size_mb, allowed_formats[]}`

#### Customer Archetype Recommendations — Media Settings

```
Fashion Retailer (image-heavy):
  auto_generate_thumbnails: ✓
  thumbnail_size: 300 (higher quality for visual product grid)
  max_image_size_mb: 20 (allow high-res photography)
  allowed_image_formats: "jpg,jpeg,png,webp"
  Rationale: Fashion relies on high-quality imagery. WebP for modern web performance.
  Large file size limit accommodates professional photography.

Industrial Supplier (technical drawings):
  auto_generate_thumbnails: ✓
  thumbnail_size: 150 (standard)
  max_image_size_mb: 15 (technical drawings can be large)
  allowed_image_formats: "jpg,jpeg,png,webp,svg,tiff"
  Rationale: SVG for scalable technical drawings. TIFF for lossless archival images.
  Standard thumbnails sufficient for product catalog grid.

Food Manufacturer (label compliance):
  auto_generate_thumbnails: ✓
  thumbnail_size: 200 (readable nutrition labels)
  max_image_size_mb: 10 (standard)
  allowed_image_formats: "jpg,jpeg,png,webp"
  Rationale: Nutrition labels must be readable even in thumbnails.
  Slightly larger thumbnail ensures legibility.

Minimal / Low Storage:
  auto_generate_thumbnails: ✗ (save processing and storage)
  max_image_size_mb: 5 (tight limit)
  allowed_image_formats: "jpg,jpeg,png"
  Rationale: Minimize storage costs. Only essential formats accepted.
```

### 3.7 Complete PIM Settings Field Reference

For quick reference, here is every configurable field in PIM Settings organized by section:

| # | Field Name | Group | Type | Default | Key Decision |
|---|-----------|-------|------|---------|-------------|
| 1 | `enable_erp_sync` | ERP Integration | Check | `1` | Connect to ERPNext? |
| 2 | `auto_create_variant_from_item` | ERP Integration | Check | `0` | ERP-first variant creation? |
| 3 | `sync_direction` | ERP Integration | Select | `Bidirectional` | Which system is master? |
| 4 | `sync_on_save` | ERP Integration | Check | `1` | Real-time or batch sync? |
| 5 | `default_channel` | Channel Settings | Link → Channel | — | Primary distribution channel? |
| 6 | `auto_publish_to_default` | Channel Settings | Check | `0` | Auto-publish on approval? |
| 7 | `default_export_format` | Channel Settings | Select | `JSON` | Primary export format? |
| 8 | `enable_ai_enrichment` | AI Enrichment | Check | `0` | Use AI for content? |
| 9 | `ai_provider` | AI Enrichment | Select | — | Which AI service? |
| 10 | `ai_api_key` | AI Enrichment | Password | — | API credentials |
| 11 | `ai_model` | AI Enrichment | Data | — | Which AI model? |
| 12 | `ai_require_approval` | AI Enrichment | Check | `1` | Human review for AI content? |
| 13 | `enable_quality_scoring` | Data Quality | Check | `1` | Track data quality? |
| 14 | `minimum_quality_score` | Data Quality | Percent | `60` | Publish threshold? |
| 15 | `block_publish_below_minimum` | Data Quality | Check | `0` | Hard-block or advisory? |
| 16 | `auto_scan_on_save` | Data Quality | Check | `1` | Real-time quality feedback? |
| 17 | `enable_gs1_validation` | GS1/GDSN | Check | `0` | GS1 barcode validation? |
| 18 | `gln` | GS1/GDSN | Data | — | Organization GLN |
| 19 | `gs1_data_pool` | GS1/GDSN | Select | — | GDSN data pool? |
| 20 | `data_pool_api_key` | GS1/GDSN | Password | — | Data pool credentials |
| 21 | `auto_generate_thumbnails` | Media Settings | Check | `1` | Auto-thumbnails? |
| 22 | `thumbnail_size` | Media Settings | Int | `150` | Thumbnail dimensions? |
| 23 | `max_image_size_mb` | Media Settings | Int | `10` | Upload size limit? |
| 24 | `allowed_image_formats` | Media Settings | Data | `jpg,jpeg,png,webp,gif` | Allowed formats? |

### 3.8 Configuration Matrices: Minimal vs. Enterprise Setup

#### Minimal Viable Configuration

The absolute minimum configuration to get a functional PIM instance running:

```
PIM Settings — Minimal Setup:
┌────────────────────────────────────────────────────┐
│  ERP Integration                                    │
│  ├── enable_erp_sync: ✗ (or ✓ with defaults)      │
│  └── (all other ERP fields use defaults)            │
│                                                     │
│  Channel Settings                                   │
│  ├── default_channel: (skip — configure later)      │
│  └── default_export_format: "JSON" (default)        │
│                                                     │
│  AI Enrichment                                      │
│  └── enable_ai_enrichment: ✗ (skip)                │
│                                                     │
│  Data Quality                                       │
│  ├── enable_quality_scoring: ✓ (default)            │
│  ├── minimum_quality_score: 60 (default)            │
│  └── block_publish_below_minimum: ✗ (default)       │
│                                                     │
│  GS1/GDSN                                          │
│  └── enable_gs1_validation: ✗ (skip)               │
│                                                     │
│  Media Settings                                     │
│  └── (all defaults are reasonable — no changes)     │
└────────────────────────────────────────────────────┘
Time to configure: 2 minutes
Settings changed from defaults: 0-1
```

#### Full Enterprise Configuration

Complete configuration for a multi-channel, AI-enabled, GS1-compliant enterprise deployment:

```
PIM Settings — Full Enterprise Setup:
┌────────────────────────────────────────────────────┐
│  ERP Integration                                    │
│  ├── enable_erp_sync: ✓                            │
│  ├── sync_direction: "Bidirectional"                │
│  ├── sync_on_save: ✓                               │
│  └── auto_create_variant_from_item: ✓              │
│                                                     │
│  Channel Settings                                   │
│  ├── default_channel: "Primary Web Store"           │
│  ├── auto_publish_to_default: ✗ (approval-gated)   │
│  └── default_export_format: "JSON"                  │
│                                                     │
│  AI Enrichment                                      │
│  ├── enable_ai_enrichment: ✓                       │
│  ├── ai_provider: "OpenAI" (or "Anthropic")        │
│  ├── ai_api_key: ●●●●●●●● (encrypted)             │
│  ├── ai_model: "gpt-4" (or "claude-3-sonnet")     │
│  └── ai_require_approval: ✓                        │
│                                                     │
│  Data Quality                                       │
│  ├── enable_quality_scoring: ✓                     │
│  ├── minimum_quality_score: 85                      │
│  ├── block_publish_below_minimum: ✓                │
│  └── auto_scan_on_save: ✓                          │
│                                                     │
│  GS1/GDSN                                          │
│  ├── enable_gs1_validation: ✓                      │
│  ├── gln: "8680000000000" (company GLN)            │
│  ├── gs1_data_pool: "1WorldSync" or "GS1 Turkey"  │
│  └── data_pool_api_key: ●●●●●●●● (encrypted)      │
│                                                     │
│  Media Settings                                     │
│  ├── auto_generate_thumbnails: ✓                   │
│  ├── thumbnail_size: 300                            │
│  ├── max_image_size_mb: 20                          │
│  └── allowed_image_formats: "jpg,jpeg,png,webp"    │
└────────────────────────────────────────────────────┘
Time to configure: 15-30 minutes (including API key setup)
Settings changed from defaults: 12-16
```

#### Setup Complexity by Customer Tier

| Customer Tier | Settings to Change | Time | Features Enabled |
|---------------|-------------------|------|-----------------|
| **Starter** (1 channel, no ERP) | 0–1 | 2 min | Quality scoring only |
| **Standard** (ERP sync, 1–3 channels) | 4–6 | 10 min | ERP sync + quality scoring |
| **Professional** (multi-channel, AI) | 8–12 | 20 min | ERP + AI + quality + media tuning |
| **Enterprise** (full GS1, multi-channel, AI) | 14–18 | 30 min | All features enabled and configured |

### 3.9 Onboarding Context for PIM Settings

| Aspect | Details |
|--------|---------|
| **When to Configure** | **Phase 0** — the absolute first step in any onboarding. All other configuration reads from PIM Settings. |
| **Who Configures** | System Manager performs initial setup. PIM Manager can adjust thresholds and enable/disable features post-launch. |
| **Dependencies** | None — PIM Settings is the root dependency. Everything else depends on it. |
| **Typical Duration** | 2 minutes (minimal) to 30 minutes (enterprise with API credentials). |
| **Business Impact** | **Critical** — determines which features are available, how data flows, and what quality gates apply across the entire system. |
| **Reversibility** | **High** — most settings can be changed at any time without data loss. Exception: disabling ERP sync after products have synced requires careful migration planning. |

#### Configuration Checklist

```
□ Step 1: Decide ERP Integration Strategy
  □ Will you use ERPNext? → enable_erp_sync
  □ Which system is source of truth? → sync_direction
  □ Real-time or batch sync? → sync_on_save

□ Step 2: Set Quality Baseline
  □ What quality threshold for publishing? → minimum_quality_score
  □ Advisory or enforcement mode? → block_publish_below_minimum
  □ Real-time quality feedback? → auto_scan_on_save

□ Step 3: Configure AI (if applicable)
  □ Which provider? → ai_provider
  □ Set API key → ai_api_key
  □ Choose model → ai_model
  □ Test connection → test_ai_connection()
  □ Require human approval? → ai_require_approval

□ Step 4: Configure GS1 (if applicable)
  □ Register company GLN with GS1 → gln
  □ Select data pool → gs1_data_pool
  □ Set data pool API key → data_pool_api_key

□ Step 5: Tune Media Settings
  □ Appropriate max file size? → max_image_size_mb
  □ Thumbnail quality needs? → thumbnail_size
  □ Allowed formats for the team? → allowed_image_formats

□ Step 6: Channel Defaults (can be deferred)
  □ Create at least one Channel record first
  □ Set default channel → default_channel
  □ Choose default export format → default_export_format
```

---

## 4. Channel Configuration

### Overview

The PIM channel system implements a **configuration-driven architecture** where distribution channels (Amazon, Shopify, Trendyol, WooCommerce, etc.) are defined as data records in the `Channel` DocType rather than as hard-coded marketplace modules. This means any marketplace can be configured at onboarding time without code changes — the system is infinitely extensible to new channels.

**Key Architectural Decisions:**

1. **Generic Channel DocType** — Each marketplace/storefront is a `Channel` record with connection settings, export preferences, and sync configuration
2. **Product Channel child table** — Links products to channels with per-channel publish status, sync tracking, and external IDs
3. **Export Profile binding** — Each channel can have one or more Export Profiles that control format, filtering, scheduling, and output
4. **Completeness gating** — Products must meet quality/completeness thresholds (defined in PIM Settings and Product Family) before publishing to any channel

**Architecture:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CHANNEL LAYER                                     │
│                                                                             │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐      │
│  │ Channel          │     │ Channel          │     │ Channel          │      │
│  │ "Amazon"         │     │ "Shopify"        │     │ "Trendyol"       │      │
│  │ type: Marketplace│     │ type: E-Commerce │     │ type: Marketplace│      │
│  │ sync: Export Only│     │ sync: Bidir.     │     │ sync: Export Only│      │
│  └────────┬────────┘     └────────┬────────┘     └────────┬────────┘      │
│           │                       │                       │                │
│           ▼                       ▼                       ▼                │
│  ┌─────────────────────────────────────────────────────────────────┐      │
│  │ Export Profile(s)                                                │      │
│  │ ├── amazon_full_feed    → Channel: Amazon, Format: CSV          │      │
│  │ ├── shopify_json        → Channel: Shopify, Format: JSON        │      │
│  │ ├── trendyol_xml        → Channel: Trendyol, Format: XML        │      │
│  │ └── bmecat_b2b          → Channel: B2B Portal, Format: BMEcat   │      │
│  └─────────────────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────────────┘
           │
           │  Product Channel (child table, per-product assignment)
           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          PRODUCT LAYER                                      │
│                                                                             │
│  ┌─────────────────────────────────────────────┐                           │
│  │ Product Master: "Organic Cotton T-Shirt"     │                           │
│  │ └── channels (Table MultiSelect):            │                           │
│  │     ├── Amazon    → Published ✓, Synced      │                           │
│  │     ├── Shopify   → Published ✓, Synced      │                           │
│  │     ├── Trendyol  → Published ✗, Pending     │                           │
│  │     └── N11       → Not Synced               │                           │
│  └─────────────────────────────────────────────┘                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.1 Channel DocType

**DocType:** `Channel`
**Module:** PIM
**Naming Rule:** `field:channel_code` (named by the `channel_code` field)
**Sort:** Sorted by `sort_order ASC` (lower number = first in lists)
**Track Changes:** Yes (`track_changes: 1`)
**Purpose:** Defines a distribution channel — a marketplace, e-commerce platform, social commerce platform, or any outlet where product data is published.

#### Configurable Fields

**Basic Settings:**

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `channel_name` | Data (required, translatable) | — | Display name (e.g., "Amazon Turkey", "Shopify US Store") | Customer-specific naming for each channel instance |
| `channel_code` | Data (required, unique) | Auto-generated | URL-safe slug (e.g., `amazon_tr`, `shopify_us`) | Used in API calls, export filenames, webhook URLs |
| `channel_type` | Select (required) | `E-Commerce` | Classification of channel | Organizational; does not affect behavior |
| `enabled` | Check | `1` | Enable/disable channel | Disabled channels are excluded from product publish and sync |
| `sort_order` | Int | `0` (auto-set to next multiple of 10 on save via `get_next_sort_order()` in controller) | Display order | Controls channel order in product forms and admin lists |

**Channel Type Options:**

| Type | Description | Typical Channels |
|------|-------------|-----------------|
| `E-Commerce` | Self-hosted online stores | Shopify, WooCommerce, Magento, custom web stores |
| `Marketplace` | Third-party marketplace platforms | Amazon, Trendyol, Hepsiburada, N11, eBay, Etsy, Walmart |
| `Social Commerce` | Social media shopping | Meta Commerce (Facebook/Instagram Shops), TikTok Shop |
| `Retail` | Physical retail / POS | In-store displays, POS systems, kiosk |
| `Wholesale` | B2B wholesale | Wholesale portals, distributor catalogs |
| `B2B Portal` | Business-to-business | BMEcat catalogs, procurement platforms |
| `Mobile App` | Mobile applications | Native apps, PWAs |
| `Other` | Custom or niche channels | Print catalogs, data pools, internal systems |

**Connection Settings:**

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `base_url` | Data (URL) | API endpoint URL for the channel | Must match the customer's marketplace API endpoint |
| `api_key` | Password (encrypted) | API authentication key | **Security-sensitive** — stored encrypted via Frappe's password encryption |
| `api_secret` | Password (encrypted) | API authentication secret | Required by marketplaces using key+secret auth (OAuth, HMAC) |
| `webhook_url` | Data (URL, read-only) | Auto-generated webhook URL for inbound sync | Generated from `{site_url}/api/method/frappe_pim.pim.api.webhook.handle?channel={channel_code}` |

**Export Settings:**

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `default_export_format` | Select | `JSON` | Default format for exports through this channel | `JSON`, `XML`, or `CSV` — overridden by Export Profile if linked |
| `export_language` | Link → Language | — | Language for product data export | Determines which locale's attribute values are exported |
| `export_currency` | Link → Currency | — | Currency for price exports | Required for multi-currency deployments |
| `include_variants` | Check | `1` | Include product variants in channel exports | Disable for channels that only accept parent products |
| `include_media` | Check | `1` | Include media URLs in exports | Disable for text-only data feeds |

**Synchronization Settings:**

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `sync_direction` | Select | `Export Only` | Data flow direction | `Export Only`, `Import Only`, or `Bidirectional` |
| `auto_sync` | Check | `0` | Enable automatic synchronization | When enabled, products auto-sync based on `sync_interval` |
| `sync_interval` | Select | `Daily` | Sync frequency | `Real-time`, `Hourly`, `Daily`, or `Weekly` |
| `last_sync` | Datetime (read-only) | — | Timestamp of last sync | For monitoring sync freshness |

**Status Fields (read-only):**

| Field | Type | Purpose |
|-------|------|---------|
| `connection_status` | Select | `Not Configured`, `Connected`, `Connection Failed`, `Authentication Error` |
| `last_connection_check` | Datetime | When connection was last tested |
| `error_message` | Small Text | Error details from last connection test or sync |
| `description` | Text Editor | Internal documentation and notes |

#### Channel Code Validation

Channel codes follow similar slug rules as other PIM entities:

- Must start with a lowercase letter
- May contain lowercase letters, numbers, underscores, and hyphens
- Pattern: `^[a-z][a-z0-9_-]*$`
- If not provided, auto-generated from `channel_name` via `frappe.scrub()`

**Examples:** `amazon_tr`, `shopify-us`, `trendyol`, `hepsiburada`, `n11`, `google_merchant`, `meta_commerce`, `tiktok_shop`

#### Connection Testing API

Each Channel provides a `test_connection()` whitelisted method that:

1. Sends an HTTP GET request to `base_url` with authentication headers
2. Sets `connection_status` based on HTTP response:
   - **200** → `Connected`
   - **401/403** → `Authentication Error`
   - **Other** → `Connection Failed`
   - **Timeout** → `Connection Failed` with timeout message
3. Updates `last_connection_check` timestamp
4. Returns `{status, message}` dict

#### Sync Trigger API

The `sync_now()` whitelisted method enqueues an immediate sync job:

```python
frappe.enqueue(
    "frappe_pim.pim.api.export.sync_channel",
    queue="long",
    channel=self.name,
    timeout=3600  # 1 hour timeout
)
```

#### Permissions

| Role | Read | Write | Create | Delete | Export | Import |
|------|------|-------|--------|--------|--------|--------|
| System Manager | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PIM Manager | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PIM User | ✓ | — | — | — | — | — |

#### Deletion Protection

A Channel cannot be deleted if it is referenced by any `Export Profile` records. The `on_trash` handler checks:

```python
profile_count = frappe.db.count("Export Profile", {"channel": self.name})
if profile_count > 0:
    frappe.throw("Cannot delete channel — used by N export profile(s)")
```

### 4.2 Product Channel (Product-to-Channel Binding)

**DocType:** `Product Channel` (child table, `istable: 1`)
**Parent DocType:** `Product Master` (field: `channels`, via Table MultiSelect)
**Purpose:** Links individual products to distribution channels and tracks per-channel publish and sync status.

#### Configurable Fields

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `channel` | Link → Channel (required) | — | Which channel this product is assigned to | Determines which marketplaces receive this product |
| `is_published` | Check | `0` | Whether the product is live on this channel | Controls channel visibility; toggled manually or via workflow |
| `published_date` | Datetime (read-only) | Auto-set on publish | When the product went live | Audit trail for compliance |
| `last_sync` | Datetime (read-only) | — | Last sync timestamp for this product-channel pair | Monitoring sync freshness per product |
| `sync_status` | Select (read-only) | `Not Synced` | Sync state | `Not Synced`, `Synced`, `Sync Failed`, `Pending` |
| `external_id` | Data (read-only) | — | Product ID in the external system | Maps PIM product to marketplace listing (e.g., Amazon ASIN) |
| `external_url` | Data (URL, read-only) | — | Product URL on the external channel | Direct link to the live marketplace listing |
| `error_message` | Small Text (read-only, hidden) | — | Error details from last sync attempt | Debugging failed syncs |

#### Channel Assignment Pattern

The Product Channel child table implements a **multi-assignment** pattern where each product can be independently assigned to multiple channels with individual tracking:

```
Product Master: "Organic Cotton T-Shirt"
└── channels (Product Channel):
    ├── channel: "amazon_tr"
    │   is_published: ✓, sync_status: "Synced"
    │   external_id: "B0C1234567", external_url: "https://amazon.com.tr/dp/B0C1234567"
    │
    ├── channel: "trendyol"
    │   is_published: ✓, sync_status: "Synced"
    │   external_id: "TY-98765", external_url: "https://trendyol.com/p-98765"
    │
    ├── channel: "shopify_us"
    │   is_published: ✗, sync_status: "Pending"
    │   (awaiting translation and US pricing)
    │
    └── channel: "hepsiburada"
        is_published: ✗, sync_status: "Not Synced"
        (product data incomplete for this channel)
```

### 4.3 Export Profile — Channel Export Configuration

**DocType:** `Export Profile`
**Module:** PIM
**Naming Rule:** `field:profile_code`
**Purpose:** Defines how product data is exported for a specific channel — format, filters, scheduling, and format-specific settings. Each Export Profile optionally links to a Channel.

> **Note:** Export Profiles are covered in detail in Section 12 (Export & Integration). This section focuses on the channel-relevant aspects.

#### Channel-Relevant Fields

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `channel` | Link → Channel | Target channel for this export | Binds the export to a specific distribution channel |
| `export_format` | Select (required) | Output format | `BMEcat 2005`, `BMEcat 1.2`, `CSV`, `JSON`, `XML`, `Excel` |
| `export_language` | Link → Language | Product data language | Selects which locale's attribute values to export |
| `export_currency` | Link → Currency | Price currency | Converts/selects prices for the target market |
| `completeness_threshold` | Percent | Minimum completeness for export | Only products meeting this threshold are included |
| `include_variants` | Check (default: 1) | Include variants | Some channels require flat product feeds |
| `include_media` | Check (default: 1) | Include media URLs | Required for visual channels, optional for data feeds |
| `upload_to_channel` | Check | Auto-upload to channel | Depends on `channel` being set; enables push-to-marketplace |

### 4.4 Completeness & Quality Gating for Channels

The PIM implements a **multi-layer quality gate** that determines whether a product can be published to a channel:

```
Layer 1: PIM Settings
    └── minimum_quality_score: 60 (global floor)
    └── block_publish_below_minimum: ✓/✗

Layer 2: Product Family
    └── completeness_threshold: 80% (per-family)
    └── required attributes via Family Attribute Template

Layer 3: Export Profile (per-channel)
    └── completeness_threshold: 90% (per-export)

Effective threshold = MAX(PIM Settings, Family, Export Profile)
```

**Completeness Score Calculation:**

The `completeness.py` module calculates scores using:

1. **Core required fields:** `product_name`, `product_code`, `short_description` (always required)
2. **Family required attributes:** Attributes marked as required in the Family Attribute Template (field: `is_required_in_family`; note: `completeness.py` currently filters on `is_required` which should be corrected to `is_required_in_family` to match the actual DocType field name)

```
Score = (filled_required / total_required) × 100
```

The score is recalculated on every `before_save` via doc_events hooks and stored in `completeness_score` on the Product Master and Product Variant.

### 4.5 Channel-Specific Configuration Guide — 12 Marketplaces

While the PIM's channel system is generic (any channel can be configured as a data record), each marketplace has **specific data requirements** that must be met for successful product listing. This section provides per-marketplace guidance for the 12 most commonly configured channels.

> **Important:** These requirements represent marketplace standards as of early 2026. Marketplace requirements evolve — always verify against current marketplace documentation. The PIM enforces these requirements through the completeness scoring system (attribute weights + family requirements) rather than hard-coded marketplace rules.

#### 4.5.1 Requirement Priority Levels

Each data requirement is classified into four priority levels:

| Level | Symbol | Meaning | PIM Mapping |
|-------|--------|---------|------------|
| **Critical** | 🔴 | Listing will be rejected without this field | `is_required: 1` on PIM Attribute + `weight_in_completeness: 5` |
| **Required** | 🟠 | Required for most categories; warnings if missing | `is_required_in_family: 1` + `weight_in_completeness: 3-4` |
| **Recommended** | 🟡 | Improves listing quality and search ranking | `weight_in_completeness: 2` |
| **Optional** | 🟢 | Nice-to-have; enhances product page | `weight_in_completeness: 0-1` |

#### 4.5.2 Amazon

**Channel Configuration:**

```
Channel:
  channel_name: "Amazon" (or "Amazon Turkey", "Amazon US", etc.)
  channel_code: "amazon" (or "amazon_tr", "amazon_us")
  channel_type: "Marketplace"
  base_url: "https://sellingpartnerapi-eu.amazon.com" (EU region)
  sync_direction: "Export Only" (typical) or "Bidirectional"
  sync_interval: "Hourly" (recommended for inventory)
  export_language: per-marketplace (tr, en, de, etc.)
  export_currency: per-marketplace (TRY, USD, EUR, etc.)
```

**Field Requirements:**

| Field / Attribute | Priority | Notes |
|-------------------|----------|-------|
| Product Title | 🔴 Critical | Max 200 chars; include brand, key features, size/color |
| Brand | 🔴 Critical | Must match Amazon Brand Registry |
| EAN/UPC (GTIN) | 🔴 Critical | Required for most categories; enable GS1 validation |
| Product Description | 🔴 Critical | HTML allowed; max 2000 chars |
| Bullet Points (5) | 🟠 Required | 5 feature bullet points; max 500 chars each |
| Category (Browse Node) | 🔴 Critical | Amazon-specific category ID |
| Price | 🔴 Critical | Must include currency |
| Main Image | 🔴 Critical | White background, min 1000×1000 px, JPEG/PNG |
| Additional Images (up to 8) | 🟡 Recommended | Lifestyle, detail, infographic |
| A+ Content | 🟡 Recommended | Enhanced brand content (HTML/modules) |
| Search Terms | 🟠 Required | Backend keywords; max 250 bytes |
| Weight / Dimensions | 🟠 Required | Required for FBA fulfillment |
| Manufacturer | 🟡 Recommended | |
| Part Number | 🟢 Optional | Manufacturer part number |
| Color / Size | 🟠 Required | For variant products |
| Material | 🟡 Recommended | For applicable categories |

**Media Requirements:**

| Type | Min Size | Max Size | Format | Background | Notes |
|------|----------|----------|--------|------------|-------|
| Main Image | 1000×1000 px | 10,000×10,000 px | JPEG, PNG | Pure white (RGB 255,255,255) | Mandatory |
| Additional Images | 1000×1000 px | 10,000×10,000 px | JPEG, PNG | Any | Up to 8 |
| Video | — | 5 min / 500 MB | MP4 | — | Seller-uploaded |

#### 4.5.3 Shopify

**Channel Configuration:**

```
Channel:
  channel_name: "Shopify" (or per-store instance)
  channel_code: "shopify" (or "shopify_us", "shopify_eu")
  channel_type: "E-Commerce"
  base_url: "https://{store}.myshopify.com/admin/api/2024-01"
  sync_direction: "Bidirectional" (recommended)
  sync_interval: "Real-time" (webhooks supported)
  include_variants: ✓
```

**Field Requirements:**

| Field / Attribute | Priority | Notes |
|-------------------|----------|-------|
| Product Title | 🔴 Critical | Max 255 chars |
| Product Description | 🔴 Critical | HTML supported; no limit (but SEO optimal ≤ 320 chars for meta) |
| Product Type | 🟡 Recommended | Shopify collection/type |
| Vendor (Brand) | 🟠 Required | Brand name |
| Price | 🔴 Critical | |
| Compare-at Price | 🟡 Recommended | Original price for sale display |
| SKU | 🔴 Critical | Per-variant |
| Barcode (EAN/UPC) | 🟡 Recommended | GTIN for Google integration |
| Weight | 🟠 Required | For shipping calculations |
| Main Image | 🔴 Critical | Min 2048×2048 recommended |
| Additional Images | 🟡 Recommended | No limit |
| SEO Title | 🟡 Recommended | Max 70 chars |
| SEO Description | 🟡 Recommended | Max 320 chars |
| Tags | 🟡 Recommended | Comma-separated for filtering |
| Variant Options (up to 3) | 🟠 Required | Color, Size, Material (max 3 axes) |
| Inventory Quantity | 🟠 Required | For inventory tracking |

**Media Requirements:**

| Type | Recommended Size | Max Size | Format | Notes |
|------|-----------------|----------|--------|-------|
| Product Image | 2048×2048 px | 4472×4472 px (20 MP) | JPEG, PNG, GIF, WebP | Up to 250 per product |
| Video | — | — | MP4, MOV (via URL) | External URL supported |
| 3D Model | — | — | GLB, USDZ | AR/3D product views |

#### 4.5.4 WooCommerce

**Channel Configuration:**

```
Channel:
  channel_name: "WooCommerce"
  channel_code: "woocommerce"
  channel_type: "E-Commerce"
  base_url: "https://{domain}/wp-json/wc/v3"
  api_key: Consumer Key
  api_secret: Consumer Secret
  sync_direction: "Bidirectional"
  sync_interval: "Hourly"
```

**Field Requirements:**

| Field / Attribute | Priority | Notes |
|-------------------|----------|-------|
| Product Name | 🔴 Critical | |
| Regular Price | 🔴 Critical | |
| Sale Price | 🟢 Optional | |
| Description | 🔴 Critical | HTML supported |
| Short Description | 🟠 Required | Excerpt for listings |
| SKU | 🔴 Critical | Must be unique |
| Categories | 🟠 Required | WooCommerce category taxonomy |
| Tags | 🟢 Optional | |
| Main Image | 🔴 Critical | |
| Gallery Images | 🟡 Recommended | No limit |
| Weight | 🟡 Recommended | For shipping |
| Dimensions (L×W×H) | 🟡 Recommended | For shipping |
| Stock Quantity | 🟠 Required | If stock management enabled |
| Barcode | 🟢 Optional | Via custom field or plugin |
| Brand | 🟡 Recommended | Via plugin (not native) |
| Attributes / Variations | 🟠 Required | For variable products |

**Media Requirements:**

| Type | Recommended Size | Format | Notes |
|------|-----------------|--------|-------|
| Product Image | 800×800 px min | JPEG, PNG, GIF, WebP | Theme-dependent |
| Gallery Images | Same | Same | Unlimited |

#### 4.5.5 Google Merchant Center

**Channel Configuration:**

```
Channel:
  channel_name: "Google Merchant Center"
  channel_code: "google_merchant"
  channel_type: "Marketplace"
  base_url: "https://shoppingcontent.googleapis.com/content/v2.1"
  sync_direction: "Export Only"
  default_export_format: "XML" (or feed URL)
  sync_interval: "Daily"
```

**Field Requirements:**

| Field / Attribute | Priority | Notes |
|-------------------|----------|-------|
| Title | 🔴 Critical | Max 150 chars; include brand + product type + attributes |
| Description | 🔴 Critical | Max 5000 chars; no HTML |
| Link (Product URL) | 🔴 Critical | Landing page URL |
| Image Link | 🔴 Critical | Min 100×100 px (non-apparel), 250×250 px (apparel) |
| Price | 🔴 Critical | With currency (e.g., "29.99 TRY") |
| Availability | 🔴 Critical | `in_stock`, `out_of_stock`, `preorder`, `backorder` |
| Brand | 🔴 Critical | (or `identifier_exists: false`) |
| GTIN (EAN/UPC) | 🔴 Critical | (or `identifier_exists: false`) |
| MPN | 🟠 Required | If GTIN not available |
| Condition | 🔴 Critical | `new`, `refurbished`, `used` |
| Google Product Category | 🔴 Critical | Google taxonomy ID |
| Additional Image Links | 🟡 Recommended | Up to 10 |
| Sale Price | 🟢 Optional | With effective dates |
| Color | 🟠 Required | For apparel |
| Size | 🟠 Required | For apparel |
| Gender | 🟠 Required | For apparel (`male`, `female`, `unisex`) |
| Age Group | 🟠 Required | For apparel (`newborn`...`adult`) |
| Material | 🟡 Recommended | |
| Pattern | 🟡 Recommended | |
| Shipping Weight | 🟡 Recommended | |
| Product Type (custom) | 🟡 Recommended | Your own category path |
| Custom Labels (0-4) | 🟢 Optional | For Shopping campaign segmentation |

**Media Requirements:**

| Type | Min Size | Recommended | Format | Notes |
|------|----------|-------------|--------|-------|
| Main Image | 100×100 px (250×250 apparel) | 800×800 px | JPEG, PNG, GIF, BMP, TIFF | No watermarks, no placeholders |
| Additional Images | Same | Same | Same | Up to 10 |

#### 4.5.6 Trendyol

**Channel Configuration:**

```
Channel:
  channel_name: "Trendyol"
  channel_code: "trendyol"
  channel_type: "Marketplace"
  base_url: "https://api.trendyol.com/sapigw"
  api_key: Supplier API Key
  api_secret: Supplier API Secret
  sync_direction: "Export Only"
  sync_interval: "Hourly"
  export_language: "tr"
  export_currency: "TRY"
```

**Field Requirements:**

| Field / Attribute | Priority | Notes |
|-------------------|----------|-------|
| Ürün Adı (Product Name) | 🔴 Critical | Turkish required; brand + product type + key attribute |
| Barkod (Barcode/GTIN) | 🔴 Critical | Valid EAN-13 or UPC required |
| Marka (Brand) | 🔴 Critical | Must exist in Trendyol's brand registry |
| Kategori (Category) | 🔴 Critical | Trendyol category ID (numeric) |
| Fiyat (Price) | 🔴 Critical | In TRY; must include VAT |
| Stok (Stock Quantity) | 🔴 Critical | Must be > 0 for listing |
| Açıklama (Description) | 🟠 Required | HTML supported |
| Ürün Ana Görsel (Main Image) | 🔴 Critical | White background, min 500×500 px |
| Ek Görseller (Additional Images) | 🟡 Recommended | Up to 7 |
| Renk (Color) | 🟠 Required | Must match Trendyol color palette |
| Beden (Size) | 🟠 Required | For apparel; Trendyol size chart |
| Cinsiyet (Gender) | 🟠 Required | For apparel categories |
| Stok Kodu (SKU) | 🔴 Critical | Unique per variant |
| KDV Oranı (VAT Rate) | 🟠 Required | 1%, 10%, 20% |
| Desi (Volumetric Weight) | 🟡 Recommended | For shipping cost calculation |
| Category Attributes | 🔴 Critical | Dynamic per-category required attributes from Trendyol API |

**Media Requirements:**

| Type | Min Size | Max Size | Format | Background | Notes |
|------|----------|----------|--------|------------|-------|
| Main Image | 500×500 px | — | JPEG, PNG | White (required) | Mandatory |
| Additional Images | 500×500 px | — | JPEG, PNG | Any | Up to 7 |

#### 4.5.7 Hepsiburada

**Channel Configuration:**

```
Channel:
  channel_name: "Hepsiburada"
  channel_code: "hepsiburada"
  channel_type: "Marketplace"
  base_url: "https://mpop-sit.hepsiburada.com/product/api" (or production URL)
  api_key: Merchant API Key
  sync_direction: "Export Only"
  sync_interval: "Hourly"
  export_language: "tr"
  export_currency: "TRY"
```

**Field Requirements:**

| Field / Attribute | Priority | Notes |
|-------------------|----------|-------|
| Ürün Adı (Product Name) | 🔴 Critical | Brand + Category + Key Attributes |
| Barkod (Barcode/GTIN) | 🔴 Critical | Valid EAN-13 required |
| Marka (Brand) | 🔴 Critical | Must be registered in Hepsiburada system |
| Kategori (Category) | 🔴 Critical | Hepsiburada category tree leaf node |
| Fiyat (Price) | 🔴 Critical | VAT-inclusive TRY price |
| Stok (Stock Quantity) | 🔴 Critical | |
| HepsiBurada SKU | 🔴 Critical | Mapped to variant SKU |
| Merchant SKU | 🔴 Critical | Your internal SKU |
| Açıklama (Description) | 🟠 Required | |
| Ana Görsel (Main Image) | 🔴 Critical | Min 500×500 px, white background |
| Ek Görseller (Additional Images) | 🟡 Recommended | Up to 5 |
| Renk (Color) | 🟠 Required | For applicable categories |
| Beden (Size) | 🟠 Required | For apparel |
| Cinsiyet (Gender) | 🟠 Required | For apparel |
| KDV Oranı (VAT Rate) | 🟠 Required | |
| Garanti Süresi (Warranty) | 🟡 Recommended | In months |
| Kargo Bilgileri (Shipping) | 🟡 Recommended | Volumetric weight |
| Category-Specific Attributes | 🔴 Critical | Dynamic required attributes per category |

**Media Requirements:**

| Type | Min Size | Format | Background | Notes |
|------|----------|--------|------------|-------|
| Main Image | 500×500 px | JPEG, PNG | White (required) | Mandatory |
| Additional Images | 500×500 px | JPEG, PNG | Any | Up to 5 |

#### 4.5.8 N11

**Channel Configuration:**

```
Channel:
  channel_name: "N11"
  channel_code: "n11"
  channel_type: "Marketplace"
  base_url: "https://api.n11.com/ws"
  api_key: N11 App Key
  api_secret: N11 App Secret
  sync_direction: "Export Only"
  sync_interval: "Hourly"
  export_language: "tr"
  export_currency: "TRY"
```

**Field Requirements:**

| Field / Attribute | Priority | Notes |
|-------------------|----------|-------|
| Ürün Başlığı (Product Title) | 🔴 Critical | Max 100 chars |
| Barkod (Barcode/GTIN) | 🟠 Required | Recommended but not always mandatory |
| Marka (Brand) | 🔴 Critical | N11 brand list |
| Kategori (Category) | 🔴 Critical | N11 category code |
| Fiyat (Price) | 🔴 Critical | TRY, VAT-inclusive |
| Stok (Stock Quantity) | 🔴 Critical | |
| Stok Kodu (SKU) | 🔴 Critical | Unique |
| Açıklama (Description) | 🟠 Required | HTML supported |
| Ana Görsel (Main Image) | 🔴 Critical | |
| Ek Görseller (Additional Images) | 🟡 Recommended | Up to 8 |
| Renk (Color) | 🟠 Required | For applicable categories |
| Beden (Size) | 🟠 Required | For apparel |
| Kargo Süresi (Shipping Duration) | 🟠 Required | Delivery days |
| Category Attributes | 🟠 Required | Dynamic per-category |

**Media Requirements:**

| Type | Min Size | Format | Notes |
|------|----------|--------|-------|
| Main Image | 400×400 px | JPEG, PNG | Mandatory |
| Additional Images | 400×400 px | JPEG, PNG | Up to 8 |

#### 4.5.9 eBay

**Channel Configuration:**

```
Channel:
  channel_name: "eBay"
  channel_code: "ebay"
  channel_type: "Marketplace"
  base_url: "https://api.ebay.com" (or sandbox)
  api_key: OAuth token
  sync_direction: "Bidirectional"
  sync_interval: "Hourly"
```

**Field Requirements:**

| Field / Attribute | Priority | Notes |
|-------------------|----------|-------|
| Title | 🔴 Critical | Max 80 chars |
| Description | 🔴 Critical | HTML supported |
| Category | 🔴 Critical | eBay category ID |
| Price | 🔴 Critical | Fixed price or auction start price |
| Condition | 🔴 Critical | New, Used, Refurbished, etc. |
| Quantity | 🔴 Critical | |
| SKU | 🟠 Required | For inventory tracking |
| EAN/UPC/ISBN | 🟠 Required | Product identifiers |
| Brand | 🟠 Required | |
| MPN | 🟡 Recommended | Manufacturer part number |
| Main Image | 🔴 Critical | Min 500×500 px |
| Additional Images (up to 24) | 🟡 Recommended | eBay allows many images |
| Item Specifics | 🟠 Required | Category-specific attributes |
| Shipping Details | 🔴 Critical | Shipping service and cost |
| Return Policy | 🔴 Critical | Required for most categories |
| Payment Methods | 🔴 Critical | |
| Color / Size | 🟠 Required | For multi-variation listings |
| Weight | 🟡 Recommended | For shipping calculation |

**Media Requirements:**

| Type | Min Size | Max Size | Format | Notes |
|------|----------|----------|--------|-------|
| Product Image | 500×500 px | 9000×9000 px | JPEG, PNG, GIF, TIFF | Up to 24 images |
| Gallery Image | 500×500 px | — | Same | First image is gallery |

#### 4.5.10 Etsy

**Channel Configuration:**

```
Channel:
  channel_name: "Etsy"
  channel_code: "etsy"
  channel_type: "Marketplace"
  base_url: "https://openapi.etsy.com/v3"
  api_key: Etsy API Key
  sync_direction: "Export Only"
  sync_interval: "Daily"
```

**Field Requirements:**

| Field / Attribute | Priority | Notes |
|-------------------|----------|-------|
| Title | 🔴 Critical | Max 140 chars |
| Description | 🔴 Critical | No HTML; plain text with line breaks |
| Price | 🔴 Critical | |
| Quantity | 🔴 Critical | |
| Category (Taxonomy ID) | 🔴 Critical | Etsy taxonomy |
| Who Made It | 🔴 Critical | `i_did`, `someone_else`, `collective` |
| Is Supply | 🔴 Critical | Is this a craft supply? |
| When Made | 🔴 Critical | Year/decade range |
| Main Image | 🔴 Critical | Min 2000 px on shortest side |
| Additional Images (up to 9) | 🟡 Recommended | |
| Tags (up to 13) | 🟠 Required | Max 20 chars each; critical for search |
| Materials | 🟡 Recommended | Up to 13 materials |
| Shipping Profile | 🔴 Critical | Pre-configured in Etsy |
| Personalization | 🟢 Optional | Buyer customization options |
| Variations (up to 2) | 🟠 Required | Only 2 variation axes allowed |
| SKU | 🟡 Recommended | Per variation |
| Weight | 🟡 Recommended | For shipping |

**Media Requirements:**

| Type | Recommended Size | Aspect Ratio | Format | Notes |
|------|-----------------|--------------|--------|-------|
| Listing Image | 2000×2000 px | Square (5:4 for search) | JPEG, PNG, GIF | Up to 10 images |
| Video | — | — | MP4 (5-15 sec) | 1 video per listing |

#### 4.5.11 Walmart

**Channel Configuration:**

```
Channel:
  channel_name: "Walmart Marketplace"
  channel_code: "walmart"
  channel_type: "Marketplace"
  base_url: "https://marketplace.walmartapis.com/v3"
  api_key: Client ID
  api_secret: Client Secret
  sync_direction: "Export Only"
  sync_interval: "Hourly"
  export_language: "en"
  export_currency: "USD"
```

**Field Requirements:**

| Field / Attribute | Priority | Notes |
|-------------------|----------|-------|
| Product Name | 🔴 Critical | Max 200 chars |
| Brand | 🔴 Critical | Registered brand |
| UPC/GTIN | 🔴 Critical | Required (no exemptions for most categories) |
| Price | 🔴 Critical | USD |
| Description | 🔴 Critical | Max 4000 chars |
| Short Description | 🟠 Required | Key features (bulleted) |
| Main Image | 🔴 Critical | Min 1000×1000 px, white background |
| Additional Images | 🟡 Recommended | Up to 15 |
| Category | 🔴 Critical | Walmart taxonomy |
| SKU | 🔴 Critical | Unique per seller |
| Shipping Weight | 🔴 Critical | Required for shipping calculation |
| Shelf Description | 🟡 Recommended | |
| Key Features (3-10) | 🟠 Required | Bullet points |
| Color / Size | 🟠 Required | For variant items |
| Manufacturer | 🟡 Recommended | |
| MPN | 🟡 Recommended | |
| Tax Code | 🟠 Required | Walmart tax code |
| Ship Methods | 🔴 Critical | Shipping options |

**Media Requirements:**

| Type | Min Size | Format | Background | Notes |
|------|----------|--------|------------|-------|
| Main Image | 1000×1000 px | JPEG, PNG | White | Mandatory |
| Additional Images | 1000×1000 px | Same | Any | Up to 15 |
| Hero Image | 2000×2000 px | Same | White | For featured placement |

#### 4.5.12 Meta Commerce (Facebook / Instagram Shops)

**Channel Configuration:**

```
Channel:
  channel_name: "Meta Commerce"
  channel_code: "meta_commerce"
  channel_type: "Social Commerce"
  base_url: "https://graph.facebook.com/v18.0"
  api_key: Commerce Manager Access Token
  sync_direction: "Export Only"
  sync_interval: "Daily"
```

**Field Requirements:**

| Field / Attribute | Priority | Notes |
|-------------------|----------|-------|
| Title | 🔴 Critical | Max 200 chars |
| Description | 🔴 Critical | Max 9999 chars; plain text |
| Product URL | 🔴 Critical | Link to product page |
| Image URL | 🔴 Critical | Min 500×500 px |
| Price | 🔴 Critical | With currency code |
| Availability | 🔴 Critical | `in stock`, `out of stock` |
| Brand | 🟠 Required | |
| GTIN / MPN | 🟠 Required | At least one identifier |
| Condition | 🔴 Critical | `new`, `refurbished`, `used` |
| Category (Google Product Category) | 🟠 Required | Uses Google taxonomy |
| Additional Images | 🟡 Recommended | Up to 10 |
| Color / Size / Pattern | 🟡 Recommended | For variant groups |
| Content ID | 🔴 Critical | Unique product ID in your catalog |
| Sale Price | 🟢 Optional | With effective dates |
| Gender | 🟡 Recommended | For apparel |
| Age Group | 🟡 Recommended | For apparel |
| Custom Labels (0-4) | 🟢 Optional | For ad segmentation |

**Media Requirements:**

| Type | Min Size | Max Size | Format | Notes |
|------|----------|----------|--------|-------|
| Product Image | 500×500 px | — | JPEG, PNG | No text overlays or watermarks |
| Additional Images | 500×500 px | — | Same | Up to 10 |
| Catalog Video | — | — | MP4 | Via Commerce Manager |

#### 4.5.13 TikTok Shop

**Channel Configuration:**

```
Channel:
  channel_name: "TikTok Shop"
  channel_code: "tiktok_shop"
  channel_type: "Social Commerce"
  base_url: "https://open-api.tiktokglobalshop.com"
  api_key: App Key
  api_secret: App Secret
  sync_direction: "Export Only"
  sync_interval: "Daily"
```

**Field Requirements:**

| Field / Attribute | Priority | Notes |
|-------------------|----------|-------|
| Product Title | 🔴 Critical | Max 255 chars |
| Description | 🔴 Critical | Max 10,000 chars; supports basic formatting |
| Category | 🔴 Critical | TikTok Shop category ID |
| Brand | 🟠 Required | Must apply for brand authorization |
| Price | 🔴 Critical | With currency |
| Stock Quantity | 🔴 Critical | |
| SKU | 🔴 Critical | |
| Main Image | 🔴 Critical | Min 600×600 px |
| Additional Images (up to 8) | 🟡 Recommended | |
| Product Video | 🟡 Recommended | Strongly recommended for engagement |
| Weight | 🟠 Required | For shipping |
| Dimensions (L×W×H) | 🟡 Recommended | Package dimensions |
| Color / Size | 🟠 Required | For variant products |
| Category Attributes | 🔴 Critical | TikTok-specific required attributes |
| Shipping Template | 🔴 Critical | Pre-configured in TikTok Seller Center |
| GTIN | 🟡 Recommended | |

**Media Requirements:**

| Type | Min Size | Max Size | Format | Notes |
|------|----------|----------|--------|-------|
| Main Image | 600×600 px | — | JPEG, PNG | Square ratio preferred |
| Additional Images | 600×600 px | — | JPEG, PNG | Up to 8 |
| Product Video | — | 60 sec | MP4 | Highly recommended |

### 4.6 Cross-Channel Requirements Comparison Matrix

The following matrix summarizes the critical and required fields across all 12 channels to help implementation teams identify common requirements and plan attribute configuration:

#### Core Field Requirements Across Channels

| Field | Amazon | Shopify | WooCommerce | Google Merchant | Trendyol | Hepsiburada | N11 | eBay | Etsy | Walmart | Meta Commerce | TikTok Shop |
|-------|--------|---------|-------------|----------------|----------|-------------|-----|------|------|---------|--------------|-------------|
| Product Title | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 |
| Description | 🔴 | 🔴 | 🔴 | 🔴 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 |
| Brand | 🔴 | 🟠 | 🟡 | 🔴 | 🔴 | 🔴 | 🔴 | 🟠 | — | 🔴 | 🟠 | 🟠 |
| Price | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 |
| GTIN (EAN/UPC) | 🔴 | 🟡 | 🟢 | 🔴 | 🔴 | 🔴 | 🟠 | 🟠 | — | 🔴 | 🟠 | 🟡 |
| SKU | 🟠 | 🔴 | 🔴 | — | 🔴 | 🔴 | 🔴 | 🟠 | 🟡 | 🔴 | — | 🔴 |
| Main Image | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 |
| Category | 🔴 | 🟡 | 🟠 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 |
| Stock Quantity | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟠 | 🔴 | 🔴 |
| Condition | — | — | — | 🔴 | — | — | — | 🔴 | 🔴 | — | 🔴 | — |
| Shipping Weight | 🟠 | 🟠 | 🟡 | 🟡 | 🟡 | 🟡 | — | 🟡 | 🟡 | 🔴 | — | 🟠 |

**Legend:** 🔴 Critical | 🟠 Required | 🟡 Recommended | 🟢 Optional | — Not applicable

#### Apparel-Specific Requirements

| Field | Amazon | Shopify | WooCommerce | Google Merchant | Trendyol | Hepsiburada | N11 | eBay | Etsy | Walmart | Meta Commerce | TikTok Shop |
|-------|--------|---------|-------------|----------------|----------|-------------|-----|------|------|---------|--------------|-------------|
| Color | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟡 | 🟠 |
| Size | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟠 | 🟡 | 🟠 |
| Gender | 🟡 | — | — | 🟠 | 🟠 | 🟠 | — | 🟡 | — | 🟡 | 🟡 | 🟡 |
| Material | 🟡 | — | — | 🟡 | 🟡 | 🟡 | — | 🟡 | 🟡 | 🟡 | — | 🟡 |
| Age Group | — | — | — | 🟠 | — | — | — | — | — | — | 🟡 | — |

#### Media Requirements Comparison

| Channel | Min Main Image | Recommended Size | Max Images | Video | White Background |
|---------|---------------|-----------------|------------|-------|-----------------|
| **Amazon** | 1000×1000 px | 2000×2000 px | 9 | ✓ (5 min) | Required (main) |
| **Shopify** | — | 2048×2048 px | 250 | ✓ (URL) | Not required |
| **WooCommerce** | 800×800 px | 1200×1200 px | Unlimited | Theme-dependent | Not required |
| **Google Merchant** | 100×100 px (250 apparel) | 800×800 px | 11 | ✗ | Not required |
| **Trendyol** | 500×500 px | 1000×1000 px | 8 | ✗ | Required (main) |
| **Hepsiburada** | 500×500 px | 1000×1000 px | 6 | ✗ | Required (main) |
| **N11** | 400×400 px | 800×800 px | 9 | ✗ | Not required |
| **eBay** | 500×500 px | 1600×1600 px | 24 | ✗ | Not required |
| **Etsy** | 2000 px (short side) | 2000×2000 px | 10 | ✓ (15 sec) | Not required |
| **Walmart** | 1000×1000 px | 2000×2000 px | 16 | ✗ | Required (main) |
| **Meta Commerce** | 500×500 px | 1024×1024 px | 11 | ✓ | Not required |
| **TikTok Shop** | 600×600 px | 1200×1200 px | 9 | ✓ (60 sec) | Not required |

### 4.7 Channel Configuration — Implementation Strategy

#### PIM Configuration to Meet Channel Requirements

Since the PIM uses a generic channel system, marketplace requirements must be enforced through **attribute configuration, completeness weights, and family-level requirements** rather than hard-coded channel rules.

**Strategy 1: Create channel-aware attributes**

```
PIM Attributes for channel compliance:
  ├── bullet_point_1 through bullet_point_5
  │   data_type: Text, max_length: 500
  │   Purpose: Amazon bullet points, Walmart key features
  │
  ├── google_product_category
  │   data_type: Text
  │   Purpose: Google Merchant & Meta Commerce taxonomy ID
  │
  ├── condition
  │   data_type: Select, options: "New, Refurbished, Used"
  │   Purpose: Google Merchant, eBay, Meta Commerce
  │
  ├── search_terms
  │   data_type: Text, max_length: 250
  │   Purpose: Amazon backend keywords
  │
  ├── age_group
  │   data_type: Select, options: "Newborn, Infant, Toddler, Kids, Adult"
  │   Purpose: Google Merchant, Meta Commerce (apparel)
  │
  └── shipping_profile_id
      data_type: Text
      Purpose: Etsy, TikTok Shop shipping template reference
```

**Strategy 2: Configure family-level requirements per target channel mix**

```
Family: "Fashion T-Shirts"
  Channel targets: Amazon, Trendyol, Hepsiburada, Shopify

  Attribute Template (configured for multi-channel):
  ├── product_name        → required: ✓, weight: 5  (all channels)
  ├── description         → required: ✓, weight: 5  (all channels)
  ├── short_description   → required: ✓, weight: 4  (Amazon, Walmart)
  ├── brand               → required: ✓, weight: 5  (all marketplaces)
  ├── color               → required: ✓, weight: 4  (all apparel)
  ├── size                → required: ✓, weight: 4  (all apparel)
  ├── gender              → required: ✓, weight: 3  (Trendyol, Google)
  ├── fabric_composition  → required: ✓, weight: 3  (compliance)
  ├── barcode             → required: ✓, weight: 5  (Amazon, Trendyol, Hepsiburada)
  ├── bullet_point_1..5   → required: ✗, weight: 2  (Amazon optimization)
  ├── search_terms        → required: ✗, weight: 1  (Amazon SEO)
  └── google_product_cat  → required: ✗, weight: 1  (Google Merchant)

  completeness_threshold: 90%
  min_images: 4

  Export Profiles:
  ├── "amazon_feed"       → completeness_threshold: 95%
  ├── "trendyol_feed"     → completeness_threshold: 90%
  └── "shopify_sync"      → completeness_threshold: 85%
```

**Strategy 3: Use Export Profile completeness thresholds for per-channel gates**

```
Export Profile completeness thresholds:
  ├── Amazon feed:        95% (strictest — GTIN, bullets, images all needed)
  ├── Walmart feed:       95% (strict — shipping weight mandatory)
  ├── Trendyol feed:      90% (Turkish content + images)
  ├── Hepsiburada feed:   90% (similar to Trendyol)
  ├── Google Merchant:    85% (feed-based, less strict)
  ├── Shopify:            80% (editable post-publish)
  ├── WooCommerce:        80% (editable post-publish)
  ├── eBay:               85% (listing quality affects rank)
  ├── Etsy:               80% (handmade/vintage focus)
  ├── N11:                85% (Turkish marketplace)
  ├── Meta Commerce:      75% (social commerce, iterative)
  └── TikTok Shop:        80% (social commerce)
```

### 4.8 Channel API Reference

| Endpoint | Method | Purpose | Returns |
|----------|--------|---------|---------|
| `get_channels(enabled_only=True)` | GET | List all channels ordered by sort_order | `[{name, channel_name, channel_code, channel_type, enabled, connection_status, sort_order}]` |
| `get_channel_types()` | GET | List available channel type options | `[{value, label}]` — 8 types |
| `bulk_enable_channels(channels, enable)` | POST | Enable/disable multiple channels | `{success: True, updated: N}` |
| `reorder_channels(order)` | POST | Reorder channels by name list | `{success: True}` |
| `Channel.test_connection()` | POST | Test channel API connectivity | `{status, message}` |
| `Channel.sync_now()` | POST | Trigger immediate sync | `{status: "success", message}` |

### 4.9 Customer Archetype Examples — Channel Configuration

#### Fashion Retailer (Turkey-focused, expanding globally)

```
Channels:
  ├── Trendyol         → type: Marketplace, sync: Export Only, interval: Hourly
  │   Export: XML, Turkish, TRY, completeness: 90%
  │
  ├── Hepsiburada      → type: Marketplace, sync: Export Only, interval: Hourly
  │   Export: XML, Turkish, TRY, completeness: 90%
  │
  ├── N11              → type: Marketplace, sync: Export Only, interval: Hourly
  │   Export: XML, Turkish, TRY, completeness: 85%
  │
  ├── Shopify (TR)     → type: E-Commerce, sync: Bidirectional, interval: Real-time
  │   Export: JSON, Turkish, TRY, completeness: 85%
  │
  ├── Shopify (US)     → type: E-Commerce, sync: Bidirectional, interval: Real-time
  │   Export: JSON, English, USD, completeness: 85%
  │
  └── Meta Commerce    → type: Social Commerce, sync: Export Only, interval: Daily
      Export: CSV, Turkish, TRY, completeness: 75%

Key decisions:
  - Turkish marketplaces (Trendyol, Hepsiburada, N11) get highest priority
  - Shopify instances per region for language/currency
  - Meta Commerce for social selling with lower completeness bar
  - No Amazon initially (can add later)
  - Hourly sync for marketplace inventory accuracy
```

#### B2B Industrial Supplier

```
Channels:
  ├── B2B Portal       → type: B2B Portal, sync: Export Only, interval: Daily
  │   Export: BMEcat 2005, English, EUR, completeness: 95%
  │
  ├── WooCommerce      → type: E-Commerce, sync: Bidirectional, interval: Hourly
  │   Export: JSON, English, USD, completeness: 90%
  │
  └── Amazon Business  → type: Marketplace, sync: Export Only, interval: Daily
      Export: CSV, English, USD, completeness: 95%

Key decisions:
  - BMEcat format for European B2B procurement portals
  - High completeness thresholds (95%) for safety-critical data
  - Daily sync is sufficient (slow-moving catalog)
  - No social commerce channels
```

#### Multi-Channel SMB (Turkish E-Commerce)

```
Channels:
  ├── Trendyol         → type: Marketplace, sync: Export Only, interval: Hourly
  ├── Hepsiburada      → type: Marketplace, sync: Export Only, interval: Hourly
  ├── N11              → type: Marketplace, sync: Export Only, interval: Hourly
  ├── Amazon TR        → type: Marketplace, sync: Export Only, interval: Hourly
  ├── eBay             → type: Marketplace, sync: Export Only, interval: Daily
  ├── Etsy             → type: Marketplace, sync: Export Only, interval: Daily
  └── TikTok Shop      → type: Social Commerce, sync: Export Only, interval: Daily

Key decisions:
  - All Turkish marketplaces active from day one
  - Hourly sync for high-traffic channels
  - Daily sync for lower-priority channels (eBay, Etsy, TikTok)
  - All exports in Turkish + TRY by default
  - Progressive channel addition: start with 3, expand to 7
```

### 4.10 Onboarding Context for Channel Configuration

| Aspect | Details |
|--------|---------|
| **When to Configure** | Phase 3 — after PIM Settings, Type System, and Attribute System are complete. Channels need the product data model to be defined first so that export mappings make sense. |
| **Who Configures** | PIM Manager creates Channel records and sets connection details. System Manager provides API credentials. |
| **Dependencies** | PIM Settings (default channel, export format), Product Families (completeness thresholds), PIM Attributes (channel-specific attributes must exist). |
| **Typical Duration** | 1 day for 2-3 channels; 3-5 days for 7+ channels with API configuration and testing. |
| **Business Impact** | **High** — channels are the monetization layer. Incorrect configuration delays time-to-market; missing required attributes cause listing rejections. |
| **Reversibility** | **High** — channels can be added, modified, enabled/disabled, or removed at any time without affecting product data. Deleting a channel does not delete product data. |

#### Configuration Checklist

```
□ Step 1: Identify Target Channels
  □ List all marketplaces the customer sells on
  □ Identify priority order (which channels go live first?)
  □ Note channel-specific requirements (GTIN, brand registry, etc.)

□ Step 2: Create Channel Records
  □ Create a Channel record for each target marketplace
  □ Set channel_type appropriately
  □ Configure connection settings (base_url, api_key, api_secret)
  □ Test connection for each channel
  □ Set sync_direction and sync_interval

□ Step 3: Configure Export Settings Per Channel
  □ Set export_language per channel (tr, en, de, etc.)
  □ Set export_currency per channel (TRY, USD, EUR, etc.)
  □ Choose default_export_format (JSON, XML, CSV)
  □ Enable/disable include_variants and include_media

□ Step 4: Create Export Profiles (if needed)
  □ Create an Export Profile for each channel that needs custom format
  □ Set completeness_threshold per profile (higher for strict channels)
  □ Configure format-specific options (CSV delimiter, BMEcat settings)
  □ Enable scheduling if auto-export is desired

□ Step 5: Create Channel-Specific Attributes
  □ Review the cross-channel requirements matrix (Section 4.6)
  □ Create missing attributes (bullet_points, search_terms, condition, etc.)
  □ Set appropriate completeness weights
  □ Add channel-specific attributes to relevant Product Families

□ Step 6: Set Default Channel in PIM Settings
  □ Navigate to PIM Settings → Channel Settings
  □ Set default_channel to the primary channel
  □ Configure auto_publish_to_default if desired
  □ Set default_export_format

□ Step 7: Test End-to-End
  □ Create a test product with all required attributes
  □ Assign product to each channel
  □ Run export for each channel and verify output
  □ Test sync_now() for each connected channel
  □ Verify completeness scoring gates are working
```

---
## 5. Workflow & Lifecycle

### Overview

Frappe PIM implements a **multi-state product lifecycle** that governs the progression of product data from initial creation through enrichment, approval, publication, and eventual retirement. The lifecycle system operates at two levels:

1. **Product Master Lifecycle** — 6 states governing the master product's journey from Draft to Published (or Archived)
2. **Product Variant Lifecycle** — 4 states governing individual SKU availability

Together these form **7 distinct lifecycle states** across the system (with "In Preparation" being the initial Draft enrichment phase, "In Production" mapping to Published, and approval gates controlling transitions). The Product Master `status` field has 6 values; the 7th conceptual state (**Assigned**) maps to Frappe's built-in `frappe.assign_to` assignment system rather than a status field option. The system also supports quality-gated transitions that act as **Awaiting Acceptance** and **Awaiting Approval** checkpoints.

> **Note:** No separate `workflow_state.py` module exists in the codebase. The lifecycle states are defined directly on the Product Master `status` Select field. The 7-state model described here maps the spec's architectural intent onto the implemented 6-value status field plus the Frappe assignment mechanism.

**Architecture:**

```
┌──────────────────────────────────────────────────────────────────────┐
│                    PRODUCT MASTER LIFECYCLE                          │
│                                                                      │
│  ┌─────────┐    ┌───────────┐    ┌──────────┐    ┌───────────┐     │
│  │  Draft   │───▶│ In Review │───▶│ Approved │───▶│ Published │     │
│  │(In Prep.)│    │(Awaiting  │    │(Awaiting │    │(In Prod.) │     │
│  └─────────┘    │ Approval) │    │Acceptance│    └─────┬─────┘     │
│       │          └─────┬─────┘    └──────────┘          │           │
│       │                │                                 │           │
│       │                │          ┌──────────────┐       │           │
│       │                │          │ End of Life  │◀──────┘           │
│       │                │          └──────┬───────┘                   │
│       │                │                 │                           │
│       │                ▼                 ▼                           │
│       │          ┌──────────┐     ┌──────────┐                      │
│       └─────────▶│ Archived │◀────│ Archived │                      │
│                  └──────────┘     └──────────┘                      │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                   PRODUCT VARIANT LIFECYCLE                          │
│                                                                      │
│  ┌─────────┐    ┌────────┐    ┌──────────┐    ┌──────────┐         │
│  │  Draft  │───▶│ Active │◀──▶│ Inactive │───▶│ Archived │         │
│  └─────────┘    └────────┘    └──────────┘    └──────────┘         │
└──────────────────────────────────────────────────────────────────────┘
```

### 5.1 Product Master Lifecycle States

**DocType:** `Product Master`
**Field:** `status` (Select, default: `Draft`)
**Options:** `Draft`, `In Review`, `Approved`, `Published`, `End of Life`, `Archived`

The Product Master lifecycle represents the 7 conceptual states of a product's journey through the PIM system:

| # | State | Conceptual Name | Description | Who Can Set | Quality Gate |
|---|-------|-----------------|-------------|-------------|-------------|
| 1 | `Draft` | **In Preparation** | Initial state. Product data is being created and enriched. Incomplete data is expected. | PIM User, PIM Manager | None — data entry phase |
| 2 | `In Review` | **Awaiting Approval** | Product has been submitted for review. Content team believes data is complete enough for approval. | PIM User (submits), PIM Manager (reviews) | Completeness score should meet family threshold |
| 3 | `Approved` | **Awaiting Acceptance** | Product data has been approved by a PIM Manager. Ready for channel publication pending final acceptance. | PIM Manager | `minimum_quality_score` from PIM Settings |
| 4 | `Published` | **In Production** | Product is live on one or more channels. Data changes should be controlled. | PIM Manager | `block_publish_below_minimum` gate |
| 5 | `End of Life` | **End of Life** | Product is being phased out. Still visible on channels but flagged for removal. | PIM Manager | None |
| 6 | `Archived` | **Archived** | Product is no longer active. Hidden from channels and excluded from exports. | PIM Manager, System Manager | None |
| 7 | *(Assigned)* | **Assigned** | Cross-cutting state — Frappe's built-in assignment system tracks which user "owns" a product at each stage. | Any role via `frappe.assign_to` | None |

#### Valid State Transitions

| From State | To State | Permission Required | Conditions |
|-----------|----------|-------------------|------------|
| `Draft` | `In Review` | PIM User or PIM Manager | Product has `product_name`, `product_code`, `product_family` filled |
| `Draft` | `Archived` | PIM Manager | Direct archival of incomplete products |
| `In Review` | `Approved` | PIM Manager | Review completed; completeness meets threshold |
| `In Review` | `Draft` | PIM Manager | Rejection — sent back for further enrichment |
| `In Review` | `Archived` | PIM Manager | Rejected and archived |
| `Approved` | `Published` | PIM Manager | Quality score ≥ `minimum_quality_score`; at least one channel assigned |
| `Approved` | `Draft` | PIM Manager | Revoked approval — needs rework |
| `Published` | `End of Life` | PIM Manager | Product phase-out initiated |
| `Published` | `Approved` | PIM Manager | Unpublish — remove from channels but retain approval |
| `End of Life` | `Archived` | PIM Manager | Final retirement |
| `End of Life` | `Published` | PIM Manager | Re-activation (rare) |
| `Archived` | `Draft` | PIM Manager | Re-open archived product for rework |

#### Transition Rules & Quality Gates

**Gate 1: Draft → In Review (Completeness Check)**
```
Condition: completeness_score >= Product Family.completeness_threshold
Default threshold: 80%

If completeness check fails:
  → Product stays in Draft
  → missing_attributes field shows which required attributes are unfilled
  → quality_issues field lists detected problems
```

**Gate 2: Approved → Published (Quality Score Check)**
```
Condition: PIM Settings.enable_quality_scoring == True
  AND completeness_score >= PIM Settings.minimum_quality_score

If PIM Settings.block_publish_below_minimum == True:
  → Hard block: cannot publish below threshold
If PIM Settings.block_publish_below_minimum == False:
  → Soft warning: can still publish with low quality
```

**Gate 3: Channel Publication Prerequisites**
```
Condition: Product must be "Approved" or "Published" status
  AND at least one channel assigned in Product Channel table
  AND channel.is_active == True

If auto_publish_to_default is enabled in PIM Settings:
  → Products reaching "Approved" status automatically get published
     to the default_channel
```

### 5.2 Product Variant Lifecycle States

**DocType:** `Product Variant`
**Field:** `status` (Select, default: `Draft`)
**Options:** `Draft`, `Active`, `Inactive`, `Archived`

Variant lifecycle is **independent** of the parent Product Master's lifecycle, allowing SKU-level availability control.

| State | Description | ERP Sync Behavior | Channel Visibility |
|-------|-------------|-------------------|-------------------|
| `Draft` | Variant just created; data being populated | Not synced | Hidden |
| `Active` | Variant is available for sale | Synced to ERPNext Item if `sync_to_erp` is enabled | Visible on assigned channels |
| `Inactive` | Temporarily unavailable (seasonal, stock-out) | Sync paused; ERP Item status may update | Hidden from channels |
| `Archived` | Permanently discontinued | Final sync to mark ERP Item inactive | Removed from channels |

**Variant Transition Matrix:**

| From | To | When | Business Example |
|------|-----|------|-----------------|
| `Draft` → `Active` | Variant data is complete | New SKU ready for sale |
| `Active` → `Inactive` | Temporary removal needed | Seasonal item out of season |
| `Inactive` → `Active` | Reactivation | Seasonal item back in stock |
| `Active` → `Archived` | Permanent discontinuation | SKU end-of-life |
| `Inactive` → `Archived` | Permanent discontinuation | Inactive SKU retired |

**Variant Completeness Controls:**

| Field | Type | Purpose |
|-------|------|---------|
| `completeness_score` | Percent (read-only) | Auto-calculated completeness |
| `missing_attributes` | Small Text (read-only) | List of unfilled required attributes |
| `is_complete` | Check (read-only) | Boolean flag: `True` when `completeness_score >= 100` |
| `last_completeness_check` | Datetime (read-only) | Timestamp of last calculation |

### 5.3 Lifecycle Event Hooks

The PIM system uses **Frappe's `doc_events` hook pattern** to trigger actions on lifecycle changes. These hooks are defined in `hooks.py` and run automatically:

| DocType | Event | Hook | Purpose |
|---------|-------|------|---------|
| Product Master | `before_save` | `completeness.calculate_score` | Recalculate completeness before every save |
| Product Master | `after_insert` | `inheritance.copy_family_attributes` | Copy family attribute templates to new product |
| Product Master | `on_update` | `cache.invalidate_product_cache` | Clear cache on any change |
| Product Variant | `before_save` | `completeness.calculate_variant_score` | Recalculate variant completeness |
| Product Variant | `after_insert` | `inheritance.inherit_from_master` | Inherit attributes from parent product |
| Product Variant | `on_update` | `cache.invalidate_variant_cache` | Clear variant cache |

**Scheduled Events:**

| Schedule | Task | Purpose |
|----------|------|---------|
| Hourly | `recalculate_stale_scores` | Recalculate completeness for products that may be stale (attribute or family changes) |
| Daily | `generate_scheduled_feeds` | Auto-generate export feeds for channels |
| Daily | `cleanup_orphan_media` | Remove orphaned Product Media records |
| Weekly | `optimize_eav_indexes` | Optimize EAV table indexes for query performance |

### 5.4 Workflow Customization Points

| Customization | Where | Default | Impact |
|--------------|-------|---------|--------|
| Master lifecycle states | `Product Master.status` field options | 6 states | Add/remove states via DocType customization |
| Variant lifecycle states | `Product Variant.status` field options | 4 states | Add/remove states via DocType customization |
| Quality gate threshold | PIM Settings → `minimum_quality_score` | 60% | Controls publish gate strictness |
| Quality enforcement mode | PIM Settings → `block_publish_below_minimum` | Off | Soft vs. hard publish blocking |
| Auto-publish on approval | PIM Settings → `auto_publish_to_default` | Off | Automate Draft→Published flow |
| Family completeness threshold | Product Family → `completeness_threshold` | 80% | Per-family minimum completeness |
| Completeness recalculation | Scheduler → `recalculate_stale_scores` | Hourly | Adjust frequency via scheduler config |
| Product duplication behavior | `duplicate_product()` API | Status reset to "Draft" | Duplicated products always start fresh |

### 5.5 Configuring Workflows for Frappe's Workflow Engine

> **Advanced Customization:** Beyond the built-in status field, Frappe's native **Workflow** feature (Setup → Workflow) can be layered on top to add more granular state machines with role-based transitions, email notifications, and multi-level approvals.

**Frappe Workflow Configuration for Product Master:**

```
Workflow Name: PIM Product Approval
Document Type: Product Master
States:
  - Draft           (Update allowed: PIM User, PIM Manager)
  - In Review       (Update allowed: PIM Manager)
  - Approved        (Update allowed: PIM Manager)
  - Published       (Update allowed: PIM Manager)
  - End of Life     (Update allowed: PIM Manager)
  - Archived        (Update allowed: System Manager)

Transitions:
  - Draft → In Review        Action: Submit for Review    Allowed: PIM User
  - In Review → Approved     Action: Approve              Allowed: PIM Manager
  - In Review → Draft        Action: Reject               Allowed: PIM Manager
  - Approved → Published     Action: Publish              Allowed: PIM Manager
  - Published → End of Life  Action: Phase Out             Allowed: PIM Manager
  - End of Life → Archived   Action: Archive              Allowed: PIM Manager
```

### 5.6 Customer Archetype Examples — Workflow Configuration

**Fashion Retailer (Fast-Moving, Seasonal):**
```
Workflow Strategy: Streamlined 4-state flow
  Draft → Approved → Published → Archived

Rationale:
  - Skip "In Review" — small team, PIM Manager self-approves
  - auto_publish_to_default: ✓ (speed to market)
  - minimum_quality_score: 60% (lower bar for seasonal velocity)
  - block_publish_below_minimum: ✗ (advisory only)
  - Seasonal products move to Archived at end of season

Variant Strategy:
  - Rapid Draft → Active transition
  - Heavy use of Inactive state for seasonal rotation
```

**Industrial Supplier (Compliance-Heavy):**
```
Workflow Strategy: Full 6-state flow with strict gates
  Draft → In Review → Approved → Published → End of Life → Archived

Rationale:
  - Mandatory "In Review" stage — technical specs verified by engineering
  - minimum_quality_score: 95% (regulatory compliance)
  - block_publish_below_minimum: ✓ (hard enforcement)
  - Frappe Workflow overlay with 2-level approval:
    Level 1: PIM User submits → PIM Manager approves content
    Level 2: PIM Manager submits → System Manager approves compliance
  - End of Life state used for regulatory sunset periods

Variant Strategy:
  - Strict completeness_threshold (98%) before Active
  - Variants rarely go Inactive — they go directly to Archived
```

**Food Manufacturer (Regulatory + Short Shelf Life):**
```
Workflow Strategy: Gate-heavy with auto-expiry
  Draft → In Review → Approved → Published → End of Life → Archived

Rationale:
  - "In Review" stage validates nutrition data, allergen declarations
  - minimum_quality_score: 98% (food safety)
  - block_publish_below_minimum: ✓ (hard block — regulatory risk)
  - End of Life triggered by shelf_life_days attribute expiry
  - Custom scheduler task to auto-move expired products to End of Life

Variant Strategy:
  - Pack size variants: rapid Draft → Active
  - Flavor variants: require full review cycle
  - Inactive used for temporary recalls
```

### 5.7 Onboarding Context for Workflow Configuration

**When to Configure:** Phase 3 — after Product Families and Attributes are set up, before product creation begins
**Who Configures:** PIM Manager (basic workflow) or Solution Architect (Frappe Workflow overlay)
**Business Impact:** Determines data governance rigor, time-to-market speed, and compliance enforcement level

**Onboarding Checklist — Workflow Setup:**

```
□ Step 1: Define Lifecycle Strategy
  □ Decide which lifecycle states the customer needs
  □ Map business process to PIM states (Draft → Published journey)
  □ Determine if "In Review" approval stage is needed
  □ Identify any custom states needed (via DocType customization)

□ Step 2: Configure Quality Gates in PIM Settings
  □ Navigate to PIM Settings → Data Quality section
  □ Set enable_quality_scoring: ✓
  □ Set minimum_quality_score (recommended: 60–95% depending on industry)
  □ Set block_publish_below_minimum (✓ for compliance-heavy, ✗ for velocity)
  □ Set auto_publish_to_default (✓ only for streamlined workflows)

□ Step 3: Configure Per-Family Completeness Thresholds
  □ Set completeness_threshold on each Product Family
  □ Higher for regulated product families (95–100%)
  □ Lower for fast-moving product families (60–80%)

□ Step 4: Configure Frappe Workflow (Optional)
  □ Create Workflow document in Frappe Desk
  □ Define states, transitions, and allowed roles
  □ Configure email notifications for state transitions
  □ Test workflow with sample products

□ Step 5: Test End-to-End
  □ Create a test product in Draft
  □ Transition through all states to Published
  □ Verify quality gates block at configured thresholds
  □ Verify channel publication works at Published state
  □ Test rejection flow (In Review → Draft)
```

---

## 6. Scoring & Quality

### Overview

Frappe PIM implements a **weighted completeness scoring system** that measures product data quality across multiple dimensions. The scoring engine calculates a percentage score (0–100%) based on the proportion of required fields, attributes, media, and descriptions that have been filled. This score drives **quality gates** that control workflow transitions and channel publication.

The system operates at two levels:
1. **Product Master Scoring** — combines core fields, dynamic attributes (weighted), descriptions, and media
2. **Product Variant Scoring** — focuses on variant-level required fields and variant-specific attributes

**Architecture:**

```
┌──────────────────────────────────────────────────────────────────────┐
│                     SCORING ENGINE ARCHITECTURE                      │
│                                                                      │
│  ┌─────────────────┐     ┌──────────────────────┐                   │
│  │ Core Fields     │     │ Dynamic Attributes   │                   │
│  │ (Fixed Weight)  │     │ (Configurable Weight)│                   │
│  │                 │     │                      │                   │
│  │ product_name    │     │ Per-attribute weight  │                   │
│  │ product_code    │     │ from PIM Attribute    │                   │
│  │ short_desc      │     │ weight_in_completeness│                   │
│  └────────┬────────┘     └──────────┬───────────┘                   │
│           │                          │                               │
│           ▼                          ▼                               │
│  ┌──────────────────────────────────────────────┐                   │
│  │          Completeness Score Engine            │                   │
│  │   completeness.py → calculate_score()         │                   │
│  │                                               │                   │
│  │   Score = (achieved_weight / total_weight)    │                   │
│  │           × 100                               │                   │
│  └────────────────────┬─────────────────────────┘                   │
│                       │                                              │
│           ┌───────────┼───────────┐                                 │
│           ▼           ▼           ▼                                  │
│  ┌──────────────┐ ┌────────┐ ┌──────────────────┐                  │
│  │ completeness │ │missing │ │ quality_issues   │                   │
│  │ _score (%)   │ │_attrs  │ │ (text feedback)  │                   │
│  └──────────────┘ └────────┘ └──────────────────┘                   │
│           │                                                          │
│           ▼                                                          │
│  ┌──────────────────────────────────────────────┐                   │
│  │          Quality Gate Evaluation              │                   │
│  │                                               │                   │
│  │  Gate 1: Family completeness_threshold        │                   │
│  │  Gate 2: PIM Settings minimum_quality_score   │                   │
│  │  Gate 3: block_publish_below_minimum          │                   │
│  └──────────────────────────────────────────────┘                   │
└──────────────────────────────────────────────────────────────────────┘
```

### 6.1 Scoring Dimensions

The Product Master completeness score is computed from **6 scoring dimensions** that together form a weighted composite score. Each dimension contributes to the overall `completeness_score` percentage.

> **Note:** The current scoring engine computes a single aggregate `completeness_score` as a flat weighted sum (via `completeness.py` and `product_master.py`). The 6 dimensions below represent the **conceptual model** for how scores decompose; per-dimension scoring breakdowns are a planned extension (see Section 6.8, `Product Score` DocType).

| # | Dimension | Weight Category | Source | Default Weight | Customizable? |
|---|-----------|----------------|--------|---------------|---------------|
| 1 | **Content** (Descriptions) | Fixed | `short_description` (5pts) + `long_description` (5pts) | 10 pts (~20%) | Via DocType customization |
| 2 | **Media** (Images & Files) | Fixed | `main_image` (10pts) + ≥3 media items (10pts) | 20 pts (~15%) | Via DocType customization |
| 3 | **SEO** (Search Optimization) | Via Attributes | SEO-group attributes with `weight_in_completeness` | Configurable per attribute | ✓ Per-attribute weight |
| 4 | **Translation** (Localization) | Via Attributes | Localizable attributes (`is_localizable: 1`) completeness | Configurable per attribute | ✓ Per-attribute weight |
| 5 | **Attributes** (Product Data) | Dynamic | Family Attribute Template required attributes | Configurable per attribute (default: 1) | ✓ Per-attribute weight |
| 6 | **Market** (Channel Readiness) | Via Channel Rules | Channel-specific required attributes and fields | Configurable per channel | ✓ Per-channel config |

#### How Weights Are Calculated

The scoring engine in `product_master.py` → `calculate_completeness_score()` and `completeness.py` → `calculate_score()` use a **weighted sum approach**:

```
Total Weight = Σ(attribute weights) + description_weight + media_weight
Achieved Weight = Σ(filled attribute weights) + filled_description_weight + filled_media_weight

Completeness Score = (Achieved Weight / Total Weight) × 100
```

**Weight Breakdown (Default Configuration):**

| Component | Points If Filled | Points If Empty | Weight Source |
|-----------|-----------------|-----------------|---------------|
| `short_description` | +5 | 0 | Fixed in `calculate_completeness_score()` |
| `long_description` | +5 | 0 | Fixed in `calculate_completeness_score()` |
| `main_image` | +10 | 0 | Fixed in `calculate_completeness_score()` |
| ≥3 media items | +10 | 0 | Fixed in `calculate_completeness_score()` |
| Each required attribute | +`weight_in_completeness` | 0 | From PIM Attribute (default: 1) |

### 6.2 Per-Attribute Weight Configuration

**DocType:** `PIM Attribute`
**Field:** `weight_in_completeness` (Int, default: 1)
**Section:** "Completeness Score"

This is the **primary customization surface** for scoring. Each attribute can be assigned a weight that controls its impact on the overall completeness score.

| Weight Value | Meaning | Use Case |
|-------------|---------|----------|
| `0` | **Excluded** — attribute does not affect completeness | Nice-to-have attributes (internal notes, etc.) |
| `1` | **Standard** — default weight for all attributes | Most product attributes |
| `2–5` | **Important** — higher impact on completeness | Key selling attributes (e.g., product title, key features) |
| `5–10` | **Critical** — major impact on completeness | Regulatory attributes (allergens, safety certifications) |
| `10+` | **Dominant** — significantly drives the score | Core identification attributes (brand, material composition) |

**Configuration Example — Fashion Retailer:**

```
Attribute: color          → weight_in_completeness: 5  (critical for fashion)
Attribute: size_range     → weight_in_completeness: 5  (critical for fashion)
Attribute: material       → weight_in_completeness: 3  (important)
Attribute: care_instr     → weight_in_completeness: 2  (important but not blocking)
Attribute: season         → weight_in_completeness: 1  (standard)
Attribute: internal_note  → weight_in_completeness: 0  (excluded from scoring)
```

**Configuration Example — Industrial Supplier:**

```
Attribute: material_grade    → weight_in_completeness: 10 (regulatory requirement)
Attribute: tolerance         → weight_in_completeness: 8  (engineering-critical)
Attribute: safety_cert       → weight_in_completeness: 10 (compliance-critical)
Attribute: technical_drawing → weight_in_completeness: 5  (important for ordering)
Attribute: min_order_qty     → weight_in_completeness: 3  (useful but not critical)
Attribute: color             → weight_in_completeness: 1  (standard for industrial)
```

### 6.3 Quality Issue Detection

Beyond the numeric completeness score, the Product Master controller runs **quality issue detection** that identifies specific data quality problems:

**Source:** `product_master.py` → `set_missing_attributes()`
**Field:** `quality_issues` (Small Text, read-only)

| Quality Check | Threshold | Issue Message | Severity |
|--------------|-----------|---------------|----------|
| Short description length | < 50 characters | "Short description is too brief" | Warning |
| No media attached | 0 media items | "No media attached" | Warning |
| No main image | `main_image` is empty | "No main image set" | Warning |
| Missing required attributes | `is_required: 1` attributes unfilled | Listed in `missing_attributes` field | Error |

**Quality Issues Output Format:**

```
quality_issues: "Short description is too brief; No main image set"
missing_attributes: "color, material, safety_certification"
```

### 6.4 Completeness Score Calculation — Dual Engine

The PIM uses **two scoring paths** that work together:

#### Path 1: Hook-Based Scoring (`completeness.py`)

Called automatically via `doc_events` → `before_save`:

```
Trigger: Product Master save or Product Variant save
Source: frappe_pim.pim.utils.completeness
Functions:
  - calculate_score(doc)     → Product Master scoring
  - calculate_variant_score(doc) → Product Variant scoring

Logic:
  1. Count filled core required fields (product_name, product_code, short_description)
  2. Query Family Attribute Template for required attributes (is_required=1)
  3. Check each required attribute against Product Attribute Value EAV table
  4. Score = (filled / total_required) × 100
```

#### Path 2: Controller-Based Scoring (`product_master.py`)

Called via `on_update`:

```
Trigger: Product Master on_update event
Source: ProductMaster.calculate_completeness_score()

Logic:
  1. Iterate Family Attribute Template entries
  2. Weight each attribute by PIM Attribute.weight_in_completeness
  3. Add fixed weights: short_description(5), long_description(5),
     main_image(10), ≥3 media(10)
  4. Score = (achieved_weight / total_weight) × 100
  5. Write directly to DB: frappe.db.set_value(..., update_modified=False)
```

**Key Difference:** Path 1 (completeness.py) uses **equal-weight required field counting**, while Path 2 (product_master.py controller) uses **weighted scoring** with per-attribute weights. Path 2 provides the richer, more customizable score.

### 6.5 Variant Completeness Scoring

**Source:** `completeness.py` → `calculate_variant_score()` + `product_variant.py` → `calculate_completeness()`

Variant scoring follows a similar pattern with key differences:

| Aspect | Product Master | Product Variant |
|--------|---------------|-----------------|
| Core required fields | `product_name`, `product_code`, `short_description` | `sku`, `variant_name` |
| Attribute source | Family Attribute Template (`is_required=1`) | Family Attribute Template (`is_required=1` AND `is_variant_attribute=1`) |
| Description weight | Short (5) + Long (5) | Not weighted |
| Media weight | Main image (10) + 3+ items (10) | Not weighted |
| `is_complete` flag | Not present | ✓ — set when `completeness_score >= 100` |
| Fallback scoring | N/A | Basic 4-field check (`variant_name`, `variant_code`, `product_master`, `status`) |

### 6.6 Quality Gates — Configuration Matrix

Quality gates connect scoring to workflow transitions. Here's how they interact:

| Gate | Configuration | Location | Default | Effect |
|------|--------------|----------|---------|--------|
| Family Completeness | `completeness_threshold` | Product Family | 80% | Products below threshold show warnings; affects Draft → In Review |
| Quality Score Minimum | `minimum_quality_score` | PIM Settings → Data Quality | 60% | Products below cannot be Published (if enforcement enabled) |
| Publish Block | `block_publish_below_minimum` | PIM Settings → Data Quality | Off | When On: hard-block publishing below minimum; When Off: advisory warning |
| Quality Scoring Toggle | `enable_quality_scoring` | PIM Settings → Data Quality | On | Master toggle — disabling removes all quality gates |
| Auto Scan on Save | `auto_scan_on_save` | PIM Settings → Data Quality | On | Automatic scoring on every save; disable for performance |

**Interaction Matrix:**

| `enable_quality_scoring` | `block_publish_below_minimum` | `auto_scan_on_save` | Behavior |
|--------------------------|-------------------------------|---------------------|----------|
| ✗ | — | — | No quality scoring at all; products can be published freely |
| ✓ | ✗ | ✓ | Scores calculated on save; advisory warnings but no blocking |
| ✓ | ✓ | ✓ | Full enforcement: scores calculated on save, publishing blocked below threshold |
| ✓ | ✓ | ✗ | Enforcement active but scores only updated hourly (via scheduler); risk of stale scores |

### 6.7 Completeness Summary API

**Function:** `completeness.get_completeness_summary(product_name)`
**Purpose:** Returns a detailed breakdown of the completeness calculation for debugging and UI display.

**Return Value:**

```json
{
  "product_name": "PROD-000001",
  "score": 72.5,
  "total_required": 8,
  "total_filled": 6,
  "core_fields": {
    "product_name": true,
    "product_code": true,
    "short_description": false
  },
  "attributes": {
    "color": true,
    "material": true,
    "size_range": false,
    "safety_cert": true,
    "care_instructions": true
  },
  "missing_core": ["short_description"],
  "missing_attributes": ["size_range"]
}
```

### 6.8 Data Quality Policy — Future Extension Points

> **Note:** The current implementation uses PIM Settings for global quality thresholds and PIM Attribute for per-attribute weights. The system is designed to support the following future extension points for more granular quality policies:

**Planned DocType: `Data Quality Policy`**

| Planned Field | Purpose | Current Workaround |
|--------------|---------|-------------------|
| `policy_name` | Named policy per product family or channel | Use Product Family `completeness_threshold` |
| `scoring_dimensions` | Define which dimensions apply | Use PIM Attribute `weight_in_completeness` (0 = excluded) |
| `dimension_weights` | Customize content/media/SEO/translation/attribute/market weights | Hardcoded weights in `calculate_completeness_score()` |
| `rules` | Per-dimension quality rules (min description length, required media count) | Hardcoded checks in `set_missing_attributes()` |
| `thresholds` | Per-policy publish thresholds | `minimum_quality_score` in PIM Settings (global) |

**Planned DocType: `Product Score`**

| Planned Field | Purpose | Current Workaround |
|--------------|---------|-------------------|
| `product` | Link to Product Master | `completeness_score` field on Product Master |
| `content_score` | Content dimension score (20%) | Included in aggregate `completeness_score` |
| `media_score` | Media dimension score (15%) | Included in aggregate `completeness_score` |
| `seo_score` | SEO dimension score (15%) | Included in aggregate `completeness_score` |
| `translation_score` | Translation dimension score (15%) | Not separately tracked |
| `attribute_score` | Attribute dimension score (20%) | Included in aggregate `completeness_score` |
| `market_score` | Market readiness score (15%) | Not separately tracked |
| `overall_score` | Weighted aggregate | `completeness_score` |
| `calculated_at` | Timestamp | `last_enrichment_date` |

**Target Scoring Weights (Design Intent):**

| Dimension | Target Weight | Current Implementation |
|-----------|--------------|----------------------|
| Content (descriptions) | 20% | Fixed 10pts (short_desc 5 + long_desc 5) |
| Media (images/files) | 15% | Fixed 20pts (main_image 10 + 3+ media 10) |
| SEO (search optimization) | 15% | Via SEO-group attributes with `weight_in_completeness` |
| Translation (localization) | 15% | Via localizable attributes with `weight_in_completeness` |
| Attributes (product data) | 20% | Dynamic via `weight_in_completeness` per attribute |
| Market (channel readiness) | 15% | Via channel-specific required attributes |

### 6.9 Customer Archetype Examples — Scoring Configuration

**Fashion Retailer (Visual-Heavy, Fast-Moving):**

```
Scoring Strategy: Media-heavy, moderate content
  minimum_quality_score: 70
  block_publish_below_minimum: ✗ (advisory for speed)

Attribute Weights:
  color:              weight=5  (critical for shopping)
  size_range:         weight=5  (critical for fit)
  material:           weight=3  (important for fabric)
  main_image:         Fixed 10pts (must have lifestyle imagery)
  3+ media:           Fixed 10pts (multiple angles + model shots)
  short_description:  Fixed 5pts  (for listing cards)
  long_description:   Fixed 5pts  (for product pages)

Expected Score Breakdown (sample product):
  Content: 10/10 (descriptions filled)
  Media: 20/20 (main image + 5 gallery images)
  Attributes: 13/16 (color=5, material=3, size=5 — all filled)
  Total: 43/46 = 93.5%
```

**Industrial Supplier (Data-Heavy, Compliance-Driven):**

```
Scoring Strategy: Attribute-heavy, strict enforcement
  minimum_quality_score: 95
  block_publish_below_minimum: ✓ (hard enforcement)

Attribute Weights:
  material_grade:     weight=10  (regulatory)
  tolerance:          weight=8   (engineering-critical)
  safety_cert:        weight=10  (compliance)
  technical_drawing:  weight=5   (ordering reference)
  min_order_qty:      weight=3   (procurement)
  dimensions:         weight=4   (logistics)
  main_image:         Fixed 10pts (product photo)
  short_description:  Fixed 5pts  (catalog listing)
  long_description:   Fixed 5pts  (technical spec)

Expected Score Breakdown (sample product):
  Content: 10/10 (descriptions filled)
  Media: 10/20 (product photo but only 1 image)
  Attributes: 38/40 (most critical attrs filled)
  Total: 58/70 = 82.9% — BELOW threshold, BLOCKED from publishing
```

**Food Manufacturer (Regulatory + Nutrition):**

```
Scoring Strategy: Compliance-dominant, media for packaging
  minimum_quality_score: 98
  block_publish_below_minimum: ✓ (food safety requirement)

Attribute Weights:
  allergens:           weight=10  (food safety law)
  nutrition_facts:     weight=10  (labeling law)
  ingredients_list:    weight=10  (labeling law)
  shelf_life_days:     weight=8   (freshness management)
  storage_temperature: weight=8   (cold chain)
  pack_size:           weight=5   (logistics)
  organic_cert:        weight=5   (premium positioning)
  main_image:          Fixed 10pts (product packaging)
  3+ media:            Fixed 10pts (nutrition label + ingredient list images)
  short_description:   Fixed 5pts
  long_description:    Fixed 5pts

Expected Score Breakdown (sample product):
  Content: 10/10
  Media: 20/20 (packaging + nutrition label + ingredient list images)
  Attributes: 56/56 (all regulatory attributes filled)
  Total: 86/86 = 100% — MEETS threshold, can publish
```

### 6.10 Onboarding Context for Scoring Configuration

**When to Configure:** Phase 3 — after Attributes are created, before product data entry begins
**Who Configures:** PIM Manager (attribute weights) + Solution Architect (quality gate strategy)
**Business Impact:** Determines data quality standards, publish-readiness criteria, and compliance enforcement

**Onboarding Checklist — Scoring Setup:**

```
□ Step 1: Enable Quality Scoring
  □ Navigate to PIM Settings → Data Quality
  □ Verify enable_quality_scoring is ✓ (default: enabled)
  □ Set minimum_quality_score based on industry:
    - Fashion/Retail: 60–75%
    - B2B/Industrial: 85–95%
    - Food/Pharma: 95–100%
  □ Set block_publish_below_minimum:
    - ✓ for compliance-heavy industries
    - ✗ for velocity-driven businesses

□ Step 2: Configure Per-Attribute Weights
  □ For each PIM Attribute, navigate to Completeness Score section
  □ Set weight_in_completeness based on attribute importance:
    - 0 = excluded (nice-to-have attributes)
    - 1 = standard (default, most attributes)
    - 3–5 = important (key selling points)
    - 8–10 = critical (regulatory/compliance)
  □ Verify that critical attributes have is_required: ✓

□ Step 3: Configure Per-Family Thresholds
  □ For each Product Family, set completeness_threshold
  □ Higher for regulated families (95–100%)
  □ Standard for general families (80%)
  □ Lower for fast-moving families (60–70%)

□ Step 4: Test Scoring Behavior
  □ Create a test product with partial data
  □ Verify completeness_score is calculated on save
  □ Check missing_attributes shows correct list
  □ Check quality_issues shows detected problems
  □ Verify publish gate blocks at configured threshold
  □ Use get_completeness_summary() API to debug any issues

□ Step 5: Validate Scheduled Recalculation
  □ Verify recalculate_stale_scores runs hourly
  □ Check that family/attribute changes trigger score updates
  □ Confirm scores stay current after bulk attribute changes
```

---

## 7. ERPNext Integration

### Overview

Frappe PIM provides a **deep, bidirectional integration** with ERPNext's Item DocType. This integration synchronizes product information between PIM (the content-enrichment layer) and ERPNext (the operational ERP layer covering inventory, purchasing, and sales). The integration is entirely optional — the PIM operates independently when ERPNext is not installed or when sync is disabled.

The integration surface consists of four layers:

1. **Global Sync Configuration** — PIM Settings fields that control sync direction, triggers, and behavior
2. **Doc Events (Hook-Based Sync)** — Automatic synchronization triggered on Item and Product Variant lifecycle events
3. **Per-Record Sync Controls** — Per-product and per-variant flags that control individual sync behavior
4. **Field Mappings** — Bidirectional mappings between Product Master/Variant fields and ERPNext Item fields

**Architecture:**

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     PIM ↔ ERPNext SYNC ARCHITECTURE                          │
│                                                                              │
│  ┌─────────────────────┐              ┌─────────────────────┐               │
│  │    PIM Settings     │              │  ERPNext Item        │               │
│  │  (Global Config)    │              │  DocType             │               │
│  │                     │              │                      │               │
│  │  enable_erp_sync    │              │  item_code           │               │
│  │  sync_direction     │              │  item_name           │               │
│  │  sync_on_save       │              │  item_group          │               │
│  │  auto_create_*      │              │  stock_uom           │               │
│  └──────────┬──────────┘              │  description         │               │
│             │                         │  barcodes            │               │
│             ▼                         └──────────┬───────────┘               │
│  ┌─────────────────────────────────────────────────────────────────┐        │
│  │                    erp_sync.py (Sync Engine)                    │        │
│  │                                                                 │        │
│  │  PIM → ERP Direction:                                           │        │
│  │    create_erp_item(variant)  → Creates Item from Variant        │        │
│  │    sync_to_erp_item(variant) → Updates Item from Variant        │        │
│  │                                                                 │        │
│  │  ERP → PIM Direction:                                           │        │
│  │    on_item_insert(doc)  → Creates Variant from Item             │        │
│  │    on_item_update(doc)  → Updates Variant from Item             │        │
│  │    on_item_delete(doc)  → Unlinks Variant from Item             │        │
│  │                                                                 │        │
│  │  Loop Prevention:                                               │        │
│  │    flags.from_pim = True  → Skip ERP→PIM on PIM-originated     │        │
│  │    flags.from_erp = True  → Skip PIM→ERP on ERP-originated     │        │
│  └─────────────────────────────────────────────────────────────────┘        │
│             │                         │                                      │
│             ▼                         ▼                                      │
│  ┌─────────────────────┐   ┌─────────────────────┐                         │
│  │   Product Master    │   │   Product Variant    │                         │
│  │                     │   │                      │                         │
│  │  erp_item (Link)    │   │  erp_item (Link)     │                         │
│  │  auto_sync_to_erp   │   │  sync_to_erp         │                         │
│  └─────────────────────┘   │  last_erp_sync       │                         │
│                            │  erp_sync_status      │                         │
│                            └──────────────────────┘                         │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────┐        │
│  │                    hooks.py (Doc Events)                        │        │
│  │                                                                 │        │
│  │  "Item": {                                                      │        │
│  │    "after_insert": erp_sync.on_item_insert                      │        │
│  │    "on_update":    erp_sync.on_item_update                      │        │
│  │    "on_trash":     erp_sync.on_item_delete                      │        │
│  │  }                                                              │        │
│  └─────────────────────────────────────────────────────────────────┘        │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 7.1 Sync Engine — `erp_sync.py`

**Module:** `frappe_pim.pim.utils.erp_sync`
**Purpose:** Central sync engine that handles all data flow between PIM and ERPNext.

The sync engine is implemented as a set of standalone functions (not a class) that are called both from doc_events hooks (for ERP → PIM direction) and from Product Variant controller methods (for PIM → ERP direction). All functions use **deferred imports** — `import frappe` is called inside each function body, allowing the module to be imported even when Frappe is not available (useful for testing and verification).

#### Core Functions

| Function | Direction | Trigger | Purpose |
|----------|-----------|---------|---------|
| `on_item_insert(doc)` | ERP → PIM | `hooks.py` doc_event `after_insert` on Item | Optionally creates a Product Variant when a new Item is created in ERPNext |
| `on_item_update(doc)` | ERP → PIM | `hooks.py` doc_event `on_update` on Item | Syncs Item field changes to the linked Product Variant |
| `on_item_delete(doc)` | ERP → PIM | `hooks.py` doc_event `on_trash` on Item | Clears the `erp_item` link on the Product Variant (does NOT delete the variant) |
| `create_erp_item(variant)` | PIM → ERP | `ProductVariant.after_insert()` | Creates a new ERPNext Item from a Product Variant |
| `sync_to_erp_item(variant)` | PIM → ERP | `ProductVariant.on_update()` | Updates the linked ERPNext Item with current Variant data |

#### Internal Helper Functions

| Function | Purpose |
|----------|---------|
| `_is_erpnext_installed()` | Checks if ERPNext is installed by verifying `Item` DocType exists; returns `False` gracefully if not |
| `_is_pim_sync_enabled()` | Reads `enable_erp_sync` from PIM Settings; defaults to `True` if PIM Settings DocType doesn't exist |
| `_get_item_group(variant, parent_doc)` | Resolves the correct Item Group for a new Item using Product Family → Item Group mapping, with "Products" fallback |
| `_create_product_variant_from_item(item)` | Internal function that creates a Product Variant from an ERPNext Item when auto-creation is enabled |

### 7.2 Bidirectional Field Mappings

The sync engine maintains explicit field mappings between PIM and ERPNext entities. These mappings determine which fields are synchronized and in which direction.

#### PIM → ERP Field Mapping (Product Variant → Item)

Used by `create_erp_item()` and `sync_to_erp_item()`:

| Product Variant Field | ERPNext Item Field | Sync Behavior | Notes |
|----------------------|-------------------|---------------|-------|
| `variant_name` | `item_name` | Create + Update | Display name of the product |
| `sku` / `variant_code` | `item_code` | Create only | Set at Item creation; becomes the Item's primary key |
| `description` | `description` | Create + Update | Product description text |
| `uom` | `stock_uom` | Create + Update | Unit of measure (defaults to "Nos" if empty) |
| `barcode` | `barcodes[0].barcode` | Create only | First barcode entry, type "EAN" |
| Product Family → `erp_item_group` | `item_group` | Create only | Resolved via `_get_item_group()` with fallback chain |
| — | `is_stock_item` | Create only | Always set to `1` (stock item) |

#### ERP → PIM Field Mapping (Item → Product Variant)

Used by `on_item_update()` and `_create_product_variant_from_item()`:

| ERPNext Item Field | Product Variant Field | Sync Behavior | Notes |
|-------------------|----------------------|---------------|-------|
| `item_name` | `variant_name` | Update | Display name flows from ERP to PIM |
| `item_code` | `sku` / `variant_code` | Create only | Set when auto-creating variant from Item |
| `description` | `description` | Create + Update | Description text |
| `stock_uom` | `uom` | Update | Unit of measure |
| `doc.name` | `erp_item` | Create + Update | Link back to the source Item |

#### Product Master ↔ Item Mapping

Product Master has a lighter integration surface than Product Variant:

| Product Master Field | ERPNext Item Field | Direction | Notes |
|---------------------|-------------------|-----------|-------|
| `erp_item` | (Link → Item) | PIM → ERP | Links Product Master to an ERPNext Item template |
| `auto_sync_to_erp` | — | Config only | Flag to enable/disable auto-sync for this product |
| Product Family → `erp_item_group` | `item_group` | PIM → ERP | Item Group is derived from Product Family mapping |

### 7.3 Item Group Resolution — `_get_item_group()`

When creating an ERPNext Item from a PIM Product Variant, the system must determine which `Item Group` to assign. The resolution follows a **waterfall fallback chain**:

```
Step 1: Try Product Family → erp_item_group mapping
  └── Check parent Product Master's product_family
  └── Check variant's own product_family
  └── Look up Product Family.erp_item_group (Link → Item Group)

Step 2: Try exact name match
  └── Does an Item Group with the family name exist?

Step 3: Fallback to default
  └── Use "Products" Item Group
  └── If "Products" doesn't exist → use first available Item Group
  └── Last resort → "All Item Groups"
```

**Customization Impact:** The `erp_item_group` field on Product Family is the **primary customization surface** for Item Group mapping. Each Product Family should be mapped to the appropriate ERPNext Item Group during onboarding.

**Configuration Example:**

```
Product Family: apparel     → erp_item_group: "Finished Goods - Apparel"
Product Family: electronics → erp_item_group: "Finished Goods - Electronics"
Product Family: raw_material → erp_item_group: "Raw Materials"
Product Family: packaging   → erp_item_group: "Consumables - Packaging"
```

### 7.4 Sync Direction Options

The `sync_direction` field in PIM Settings determines the data flow pattern between systems. This is one of the most critical onboarding decisions.

#### Option 1: PIM to ERP

```
┌────────────────┐                    ┌─────────────────┐
│  Product Variant│───── sync ───────▶│  ERPNext Item    │
│  (Source)       │                    │  (Destination)   │
│                 │   create_erp_item()│                  │
│  variant_name   │──▶ item_name      │                  │
│  sku            │──▶ item_code      │                  │
│  description    │──▶ description    │                  │
│  uom            │──▶ stock_uom     │                  │
└────────────────┘                    └─────────────────┘

  Trigger: ProductVariant.on_update() → sync_to_erp_if_enabled()
  Guard: variant.sync_to_erp == True AND variant.erp_item exists
  Flag: item.flags.from_pim = True (prevents reverse sync loop)
```

**Use Cases:**
- Content-first workflows (marketing creates products, ERP receives)
- PIM is the product data master; ERP handles inventory/fulfillment
- Typical for fashion retail, consumer goods, D2C brands

#### Option 2: ERP to PIM

```
┌────────────────┐                    ┌─────────────────┐
│  ERPNext Item   │───── sync ───────▶│  Product Variant │
│  (Source)       │                    │  (Destination)   │
│                 │  on_item_insert()  │                  │
│  item_name      │──▶ variant_name   │                  │
│  item_code      │──▶ sku            │                  │
│  description    │──▶ description    │                  │
│  stock_uom      │──▶ uom           │                  │
└────────────────┘                    └─────────────────┘

  Trigger: hooks.py doc_event on Item (after_insert, on_update, on_trash)
  Guard: _is_pim_sync_enabled() AND NOT doc.flags.from_pim
  Auto-Create: on_item_insert() + auto_create_variant_from_item setting
  Flag: variant.flags.from_erp = True (prevents reverse sync loop)
```

**Use Cases:**
- Operations-first workflows (procurement creates Items, PIM enriches)
- ERP is the product master; PIM adds marketing/channel content
- Typical for industrial suppliers, B2B distributors

#### Option 3: Bidirectional

```
┌────────────────┐                    ┌─────────────────┐
│  Product Variant│◀════ sync ═══════▶│  ERPNext Item    │
│                 │                    │                  │
│  variant_name   │◀═══▶ item_name    │                  │
│  description    │◀═══▶ description  │                  │
│  uom            │◀═══▶ stock_uom   │                  │
└────────────────┘                    └─────────────────┘

  Both directions active simultaneously
  Last-write-wins for shared fields (description, name, UOM)
  Loop prevention via flags.from_pim / flags.from_erp
```

**Use Cases:**
- Collaborative workflows where both teams contribute data
- ERP owns logistics fields (UOM, stock), PIM owns marketing fields (descriptions, media)
- Typical for large enterprises with separate procurement and marketing teams

**Risk:** Bidirectional sync can cause **field value oscillation** if both systems write to the same field simultaneously. The flag-based loop prevention (`from_pim` / `from_erp`) prevents infinite loops but does not prevent data conflicts. The **last write wins**.

### 7.5 Sync-on-Save Behavior

When `sync_on_save` is enabled in PIM Settings, synchronization happens automatically during document lifecycle events. The trigger chain differs by direction:

#### PIM → ERP (on Product Variant save)

```
ProductVariant.on_update()
  └── sync_to_erp_if_enabled()
        ├── Check: self.sync_to_erp == True?
        ├── Check: self.erp_item exists?
        ├── Call: erp_sync.sync_to_erp_item(self)
        │     ├── Check: _is_erpnext_installed()
        │     ├── Check: _is_pim_sync_enabled()
        │     ├── Load linked Item document
        │     ├── Apply field mappings (variant → item)
        │     ├── Set item.flags.from_pim = True
        │     ├── item.save(ignore_permissions=True)
        │     └── frappe.db.commit()
        └── Update: self.db_set('last_erp_sync', now())
```

#### PIM → ERP (on Product Variant insert — auto-create)

```
ProductVariant.after_insert()
  └── create_erp_item_if_enabled()
        ├── Check: self.sync_to_erp == True?
        └── Call: erp_sync.create_erp_item(self)
              ├── Check: _is_erpnext_installed()
              ├── Check: Item already exists? (by erp_item or sku)
              ├── Build Item data dict
              │     ├── item_code = variant.sku or variant.name
              │     ├── item_name = variant.variant_name or variant.name
              │     ├── item_group = _get_item_group(variant, parent)
              │     ├── stock_uom = variant.uom or "Nos"
              │     ├── is_stock_item = 1
              │     └── barcodes = [{barcode, barcode_type: "EAN"}]
              ├── Set item.flags.from_pim = True
              ├── item.insert(ignore_permissions=True)
              └── variant.db_set('erp_item', item.name)
```

#### ERP → PIM (on Item update)

```
Item.on_update  [via hooks.py doc_events]
  └── erp_sync.on_item_update(doc)
        ├── Check: _is_erpnext_installed()
        ├── Check: NOT doc.flags.from_pim (loop prevention)
        ├── Check: _is_pim_sync_enabled()
        ├── Find linked Product Variant (by erp_item field)
        ├── Apply field mappings (item → variant)
        ├── Set variant.flags.from_erp = True
        ├── variant.save(ignore_permissions=True)
        └── frappe.db.commit()
```

### 7.6 Loop Prevention — The Sync Flag Pattern

The sync engine uses a **flag-based pattern** to prevent infinite sync loops when both directions are active:

```
                  ┌───────────────────────────────┐
                  │      SYNC FLAG PATTERN         │
                  │                                │
                  │  PIM saves Variant              │
                  │    ↓                            │
                  │  sync_to_erp_item() runs        │
                  │    ↓                            │
                  │  Sets item.flags.from_pim=True  │
                  │    ↓                            │
                  │  item.save() triggers on_update │
                  │    ↓                            │
                  │  on_item_update() called         │
                  │    ↓                            │
                  │  Checks doc.flags.from_pim       │
                  │    ↓                            │
                  │  TRUE → SKIP (no reverse sync)  │
                  └───────────────────────────────┘
```

| Flag | Set By | Checked By | Purpose |
|------|--------|------------|---------|
| `doc.flags.from_pim` | `create_erp_item()`, `sync_to_erp_item()` | `on_item_insert()`, `on_item_update()` | Prevents ERP → PIM sync when the Item change originated from PIM |
| `variant.flags.from_erp` | `on_item_update()`, `_create_product_variant_from_item()` | (Variant controller if extended) | Marks Variant changes as ERP-originated; prevents PIM → ERP on next save |

**Key Behavior:** The `from_pim` flag is checked via `doc.get("flags", {}).get("from_pim")` — using safe dictionary access that returns `None` if flags are not set. The `from_erp` flag is set as a Python attribute (`variant.flags.from_erp = True`) using Frappe's built-in flags object.

> **Important Customization Note:** If custom code extends the Product Variant controller's `on_update()` method, it should check `self.flags.from_erp` before triggering any ERP-bound sync to maintain loop prevention.

### 7.7 Per-Record ERP Sync Fields

#### Product Variant — ERP Integration Fields

**DocType:** `Product Variant`
**Section:** "ERP Integration" (`section_break_erp`, collapsible)

| Field | Type | Default | Read-Only | Purpose | Per-Customer Impact |
|-------|------|---------|-----------|---------|-------------------|
| `erp_item` | Link → Item | — | ✓ | Reference to the linked ERPNext Item | Establishes the 1:1 mapping between Variant and Item |
| `sync_to_erp` | Check | `1` | ✗ | Enable/disable sync for this specific variant | Allows per-variant sync control; useful for draft/test variants |
| `last_erp_sync` | Datetime | — | ✓ | Timestamp of last successful sync | Audit trail; identifies stale syncs |
| `erp_sync_status` | Select | `Not Synced` | ✓ | Current sync state | Visual indicator of sync health |

**`erp_sync_status` Options:**

| Status | Meaning | When Set |
|--------|---------|----------|
| `Not Synced` | No sync has been attempted | Default for new variants |
| `Synced` | Last sync completed successfully | After successful `sync_to_erp_item()` |
| `Sync Failed` | Last sync encountered an error | When sync throws an exception |
| `Pending` | Sync is queued but not yet executed | When sync is deferred to background job |

#### Product Master — ERP Integration Fields

**DocType:** `Product Master`
**Section:** "ERP Integration" (`section_break_erp`, collapsible)

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `erp_item` | Link → Item | — | Links Product Master to an ERPNext Item template | For template-level ERP mapping (parent product) |
| `auto_sync_to_erp` | Check | `1` | Enable/disable auto-sync for products in this master | Controls whether variants inherit sync behavior |

### 7.8 Fixtures — Custom Fields on ERPNext Item

> **Note:** The PIM system is designed to extend the ERPNext Item DocType with custom fields via Frappe's fixtures mechanism. The `hooks.py` contains a commented-out fixtures configuration that defines the pattern for deploying custom fields:

```python
# fixtures = [
#     {
#         "dt": "Custom Field",
#         "filters": [["module", "=", "PIM"]]
#     },
#     {
#         "dt": "Role",
#         "filters": [["name", "in", ["PIM Manager", "PIM User"]]]
#     },
# ]
```

When fixtures are activated, custom fields are added to the ERPNext Item DocType to create a PIM-aware surface within ERPNext. These custom fields bridge PIM metadata into ERPNext so that ERP users can see PIM-enriched data without leaving the ERP interface.

#### Planned Custom Field Categories on ERPNext Item

Based on the sync architecture and PIM data model, the following custom field categories are designed for the Item DocType:

| Category | # Fields | Example Fields | Purpose |
|----------|----------|---------------|---------|
| **PIM Link Fields** | 3–5 | `pim_product_master`, `pim_variant_code`, `pim_sync_status` | Back-references from Item to PIM entities |
| **Content Fields** | 8–12 | `pim_short_description`, `pim_long_description`, `pim_seo_title`, `pim_meta_description`, `pim_keywords` | Marketing content synced from PIM |
| **Media Reference Fields** | 5–8 | `pim_main_image`, `pim_gallery_url`, `pim_video_url`, `pim_thumbnail`, `pim_media_count` | References to PIM media assets |
| **Channel Fields** | 5–8 | `pim_published_channels`, `pim_channel_status`, `pim_shopify_id`, `pim_trendyol_id`, `pim_amazon_asin` | Channel publishing status and external IDs |
| **Quality Fields** | 4–6 | `pim_completeness_score`, `pim_quality_status`, `pim_last_enrichment`, `pim_is_complete` | Data quality metrics from PIM |
| **Classification Fields** | 5–8 | `pim_product_family`, `pim_product_type`, `pim_category_path`, `pim_brand`, `pim_manufacturer` | PIM taxonomy and classification data |
| **Attribute Summary** | 8–12 | `pim_color`, `pim_size`, `pim_material`, `pim_weight_net`, `pim_dimensions` | Key EAV attributes flattened for ERP visibility |
| **Compliance Fields** | 5–7 | `pim_gs1_gtin`, `pim_hs_code`, `pim_country_of_origin`, `pim_safety_class`, `pim_allergens` | Regulatory and compliance data |
| **Sync Control Fields** | 3–5 | `pim_last_sync`, `pim_sync_direction`, `pim_sync_locked`, `pim_sync_error` | Sync state management |

**Total Planned:** 50+ custom fields across 9 categories

#### Custom Field Naming Convention

All PIM custom fields on ERPNext Item follow a strict naming convention:

```
Prefix:     pim_
Pattern:    pim_{category}_{field_name}
Example:    pim_short_description, pim_completeness_score, pim_sync_status
DocType:    Item
Module:     PIM
Insert After: (contextually placed within Item form sections)
```

This prefix convention ensures:
- No conflicts with ERPNext core fields or other app custom fields
- Easy identification of PIM-sourced data in the Item form
- Simple filtering: `Custom Field.fieldname LIKE 'pim_%'`

### 7.9 Item Group Mapping Strategy

Product Family → Item Group mapping is the bridge between PIM's hierarchical product taxonomy and ERPNext's Item Group tree. This mapping must be configured during onboarding for every Product Family.

**Field:** `Product Family.erp_item_group` (Link → Item Group)

#### Mapping Strategies

| Strategy | Description | When to Use |
|----------|-------------|------------|
| **1:1 Mapping** | Each Product Family maps to a unique Item Group | When PIM and ERP taxonomies are aligned |
| **Many:1 Mapping** | Multiple Product Families map to one Item Group | When ERP has a flatter hierarchy than PIM |
| **Hierarchical Mapping** | Product Family tree mirrors Item Group tree | When full taxonomy alignment is needed |
| **Default Mapping** | All families map to a single "PIM Products" Item Group | Quick-start for PIM-first workflows |

#### Customer Archetype Examples — Item Group Mapping

**Fashion Retailer:**

```
PIM Product Family          →  ERPNext Item Group
───────────────────────────────────────────────────
apparel                     →  Finished Goods - Apparel
  ├── tops                  →  Finished Goods - Apparel
  ├── bottoms               →  Finished Goods - Apparel
  ├── outerwear             →  Finished Goods - Apparel
footwear                    →  Finished Goods - Footwear
accessories                 →  Finished Goods - Accessories
gift_cards                  →  Services

Strategy: Many:1 — PIM has detailed families, ERP uses broad groups
```

**Industrial Supplier:**

```
PIM Product Family          →  ERPNext Item Group
───────────────────────────────────────────────────
raw_material                →  Raw Material
  ├── steel                 →  Raw Material - Steel
  ├── aluminum              →  Raw Material - Aluminum
components                  →  Sub Assemblies
  ├── fasteners             →  Sub Assemblies - Fasteners
  ├── bearings              →  Sub Assemblies - Bearings
assemblies                  →  Finished Goods
tooling                     →  Fixed Asset - Tools
safety_equipment            →  Consumable - Safety

Strategy: 1:1 — Both systems use detailed hierarchies
```

**Food Manufacturer:**

```
PIM Product Family          →  ERPNext Item Group
───────────────────────────────────────────────────
fresh_produce               →  Finished Goods - Fresh
packaged_food               →  Finished Goods - Packaged
beverages                   →  Finished Goods - Beverages
ingredients                 →  Raw Material - Ingredients
packaging_materials         →  Consumable - Packaging

Strategy: 1:1 with category alignment
```

### 7.10 ERPNext Detection and Graceful Degradation

The sync engine is designed to operate safely regardless of whether ERPNext is installed. Every sync function starts with an ERPNext installation check:

```
_is_erpnext_installed()
  └── frappe.db.exists("DocType", "Item")
        ├── True  → ERPNext is installed, sync can proceed
        └── False → ERPNext is not installed, return gracefully
```

**Graceful Degradation Behavior:**

| Scenario | Behavior | User Impact |
|----------|----------|-------------|
| ERPNext not installed | All sync functions return immediately; no errors | PIM works as standalone; ERP fields are empty |
| ERPNext installed, sync disabled | `_is_pim_sync_enabled()` returns `False`; sync skipped | PIM works independently; manual sync possible |
| ERPNext installed, sync enabled | Full bidirectional sync active | Products flow between PIM and ERP |
| ERPNext installed, Item DocType missing | `_is_erpnext_installed()` returns `False` | Treated as "not installed" |
| PIM Settings DocType missing | `_is_pim_sync_enabled()` defaults to `True` | Sync enabled by default (safe for fresh installs) |

**Error Handling:** All sync functions wrap their core logic in try/except blocks. Errors are logged to Frappe's Error Log (`frappe.log_error()`) with the title prefix "PIM ERP Sync Error". Sync failures do **not** prevent the source document from saving — they are non-blocking.

### 7.11 Edge Case: With vs. Without ERPNext

#### Without ERPNext (Standalone PIM)

When ERPNext is not installed:

| Feature | Behavior |
|---------|----------|
| Product creation | Works normally; ERP Integration tab fields are empty |
| `erp_item` field | Empty Link; Item DocType not available |
| `sync_to_erp` field | Can be toggled but has no effect |
| Sync triggers | All doc_events on Item are ignored (Item DocType doesn't exist) |
| Item Group mapping | `erp_item_group` on Product Family has no target DocType |
| Fixtures | Custom fields on Item are not installed |
| Export functionality | Fully operational — channels and exports work independently |

**Configuration:**
```
PIM Settings:
  enable_erp_sync: ✗
  (All other sync settings hidden or irrelevant)

Product Family:
  erp_item_group: (leave empty)
```

#### With ERPNext — Single Company

Standard configuration. One ERPNext Company, one set of Items, one-to-one sync.

```
PIM Settings:
  enable_erp_sync: ✓
  sync_direction: (choose based on workflow)
  sync_on_save: ✓ (recommended)

Product Family:
  erp_item_group: Map to company's Item Group hierarchy

Product Variant:
  sync_to_erp: ✓ (default)
  erp_item: Auto-linked on first sync
```

#### With ERPNext — Multi-Company

When ERPNext multi-company is enabled, additional considerations apply:

| Aspect | Single Company | Multi-Company |
|--------|---------------|---------------|
| Item scope | Items are global (shared across companies) | Items are global; pricing/stock per company |
| Item Group tree | Single hierarchy | Single hierarchy (shared) |
| PIM Family mapping | Straightforward 1:1 | Same mapping; Item Groups shared |
| Sync behavior | Standard | Standard — Items are company-independent |
| Pricing | One price per Item | Multiple Price Lists per company |
| Stock | One warehouse per Item | Multiple warehouses per company |

**Multi-Company Impact on PIM:** The core PIM ↔ Item sync is **unaffected** by multi-company because ERPNext Items are global entities (not company-scoped). However, the following related areas need attention:

- **Price Lists:** If PIM manages pricing, each company may need separate price list entries
- **Warehouses:** Stock quantities in PIM are informational; actual stock is per-warehouse in ERP
- **Item Groups:** The single Item Group tree serves all companies; PIM Family mapping remains consistent

### 7.12 Conflict Detection and Resolution

When bidirectional sync is enabled, field conflicts can occur when both PIM and ERPNext modify the same field between sync cycles.

#### Current Conflict Handling

| Scenario | Current Behavior | Notes |
|----------|-----------------|-------|
| PIM and ERP both update `description` | Last write wins | Whichever system saves last overwrites the other |
| PIM updates `variant_name`, ERP updates `item_name` | Each sync overwrites the other | These are mapped fields; last sync direction wins |
| ERP deletes Item | PIM Variant's `erp_item` is cleared | Variant is NOT deleted; it becomes unlinked |
| PIM deletes Variant | No effect on ERPNext Item | Item continues to exist in ERPNext |
| Concurrent saves in both systems | Race condition possible | The flag pattern prevents loops but not concurrent writes |

#### Conflict Mitigation Strategies

| Strategy | Implementation | Recommended For |
|----------|---------------|-----------------|
| **Choose a direction** | Set `sync_direction` to `PIM to ERP` or `ERP to PIM` | Most deployments — eliminates conflicts by design |
| **Field ownership** | Use PIM for content fields, ERP for logistics fields | Bidirectional setups with clear team responsibilities |
| **Manual sync only** | Set `sync_on_save: ✗`; trigger sync via API/button | When human review is needed before sync |
| **Disable per-variant** | Set `sync_to_erp: ✗` on specific variants | Draft/test variants that shouldn't sync yet |
| **Audit via timestamps** | Monitor `last_erp_sync` and Item `modified` | Identify stale or conflicting records |

### 7.13 Scheduled Sync Tasks

Beyond real-time sync-on-save, the PIM system supports background synchronization via Frappe's scheduler:

**From `hooks.py` → `scheduler_events`:**

| Schedule | Task | Relation to ERP Sync |
|----------|------|---------------------|
| `hourly` | `recalculate_stale_scores` | Recalculates completeness scores; indirectly affects sync readiness |
| `daily` | `generate_scheduled_feeds` | Export feeds may include ERP-synced data |
| `weekly` | `optimize_eav_indexes` | Optimizes query performance for EAV tables used in sync |

**Custom Sync Scheduling:** For customers needing batch sync (instead of real-time), a scheduled task can be configured to:
1. Query Product Variants where `sync_to_erp = 1` AND (`erp_sync_status = 'Not Synced'` OR `erp_sync_status = 'Sync Failed'`)
2. Iterate and call `sync_to_erp_item()` for each
3. Update `erp_sync_status` and `last_erp_sync`

### 7.14 Onboarding Context for ERPNext Integration

**When to Configure:** Phase 0 (PIM Settings) + Phase 1 (Product Family → Item Group mapping)
**Who Configures:** System Manager (initial sync settings), Solution Architect (sync direction strategy), PIM Manager (per-family Item Group mapping)
**Business Impact:** Determines whether PIM and ERP operate as an integrated system or independently; affects data flow, team workflows, and operational efficiency

**Onboarding Checklist — ERPNext Integration:**

```
□ Step 0: Verify ERPNext Installation
  □ Confirm ERPNext is installed: bench --site [site] list-apps
  □ Verify Item DocType exists: frappe.db.exists("DocType", "Item")
  □ If ERPNext is NOT installed → skip all sync config, set enable_erp_sync: ✗

□ Step 1: Configure PIM Settings — ERP Integration
  □ Navigate to PIM Settings → ERP Integration section
  □ Set enable_erp_sync: ✓
  □ Choose sync_direction based on business workflow:
    - "PIM to ERP" → PIM is source of truth (content-first)
    - "ERP to PIM" → ERP is source of truth (operations-first)
    - "Bidirectional" → Both contribute (requires field ownership plan)
  □ Set sync_on_save: ✓ for real-time sync, ✗ for batch/manual
  □ Set auto_create_variant_from_item:
    - ✓ if Items are created in ERP first
    - ✗ if products originate in PIM (default)

□ Step 2: Map Product Families to Item Groups
  □ For each Product Family:
    □ Open Product Family → Settings section
    □ Set erp_item_group to the appropriate ERPNext Item Group
    □ Verify the Item Group exists in ERPNext
  □ If using hierarchical mapping:
    □ Ensure parent families map to parent Item Groups
    □ Verify inheritance doesn't create mismatches

□ Step 3: Activate Fixtures (if custom fields needed)
  □ Uncomment fixtures section in hooks.py
  □ Run: bench --site [site] migrate
  □ Verify custom fields appear on Item DocType
  □ Check all pim_* fields are properly placed

□ Step 4: Test Sync Flow
  □ Create a test Product Variant with sync_to_erp: ✓
  □ Verify ERPNext Item is created automatically
  □ Check erp_item link is established
  □ Verify erp_sync_status shows "Synced"
  □ Check last_erp_sync timestamp is set
  □ Modify Variant description → verify Item description updates
  □ (If bidirectional) Modify Item name → verify Variant name updates

□ Step 5: Test Edge Cases
  □ Delete Item in ERPNext → verify Variant.erp_item is cleared
  □ Create Item in ERPNext → verify auto-create behavior (if enabled)
  □ Set sync_to_erp: ✗ on a variant → verify no sync on save
  □ Disable enable_erp_sync → verify all sync stops
  □ Re-enable → verify sync resumes

□ Step 6: Document Field Ownership (Bidirectional only)
  □ Define which team owns which fields:
    - PIM team: descriptions, media, attributes, channel data
    - ERP team: UOM, stock, pricing, accounting
  □ Communicate to both teams
  □ Configure read-only permissions if needed
```

---

## 8. Roles & Permissions

### Overview

Frappe PIM implements a **three-tier role model** to govern access across all PIM DocTypes. Roles are created automatically during app installation (`install.py → create_default_roles()`) and follow a consistent escalation pattern:

1. **System Manager** — Full unrestricted access (Frappe built-in role)
2. **PIM Manager** — Full PIM-specific access (custom role)
3. **PIM User** — Restricted content-contributor access (custom role)

Beyond these base roles, the PIM system supports:
- **Category-based permission** via `PIM Category Permission` DocType — restricts users to specific product categories/families
- **Data Steward assignments** via `Data Steward` DocType — designates ownership and accountability for product data quality
- **Workflow-state gating** — certain lifecycle transitions require specific roles (see Section 5)

**Architecture:**

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         Frappe Permission Layer                         │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────────────────────┐ │
│  │ System       │   │ PIM Manager  │   │ PIM User                    │ │
│  │ Manager      │   │              │   │                              │ │
│  │ Full access  │   │ Full PIM     │   │ Read-only on config          │ │
│  │ + system     │   │ access       │   │ Read+Write on content        │ │
│  └──────────────┘   └──────────────┘   └──────────────────────────────┘ │
├──────────────────────────────────────────────────────────────────────────┤
│                       PIM-Specific Extensions                           │
│  ┌──────────────────────────┐   ┌───────────────────────────────────┐   │
│  │ PIM Category Permission  │   │ Data Steward                      │   │
│  │ Restrict by Product      │   │ Ownership & quality               │   │
│  │ Family / Category        │   │ accountability per product set    │   │
│  └──────────────────────────┘   └───────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

### 8.1 Default Roles — Installation & Configuration

**Source:** `frappe_pim/pim/setup/install.py` → `create_default_roles()`

During `bench --site [site] install-app frappe_pim`, two custom roles are automatically created:

```python
roles = ["PIM Manager", "PIM User"]
for role in roles:
    if not frappe.db.exists("Role", role):
        frappe.get_doc({
            "doctype": "Role",
            "role_name": role,
            "desk_access": 1,
            "is_custom": 1
        }).insert(ignore_permissions=True)
```

**Role Properties:**

| Property | PIM Manager | PIM User |
|----------|-------------|----------|
| `desk_access` | `1` (has Desk UI access) | `1` (has Desk UI access) |
| `is_custom` | `1` (created by PIM app) | `1` (created by PIM app) |
| Removable? | Yes, but breaks all PIM permissions | Yes, but breaks content contributor access |

**When to Configure:** Phase 1 — roles exist after installation; user assignment happens during team onboarding
**Who Configures:** System Manager assigns roles to users via **User** DocType → Roles tab
**Business Impact:** Determines who can view, create, edit, delete, export, and import product data

### 8.2 PIM Manager Role

**Purpose:** Full administrative access to all PIM features. This role is intended for product managers, catalog administrators, and implementation team leads.

**Permission Grants:**

| DocType | Read | Write | Create | Delete | Export | Import |
|---------|------|-------|--------|--------|--------|--------|
| Product Master | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Product Variant | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Product Family | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PIM Attribute | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PIM Attribute Group | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Channel | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Export Profile | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Brand | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Manufacturer | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

**Key Capabilities:**
- **Delete products** — only PIM Manager and System Manager can delete Product Master / Product Variant records
- **Import data** — bulk data import via Frappe's Data Import tool is restricted to PIM Manager
- **Configure attributes** — create, modify, and delete attribute definitions (PIM Attribute, PIM Attribute Group)
- **Manage families** — full CRUD on Product Family including tree hierarchy restructuring
- **Channel management** — create and configure sales channels, export profiles
- **Approve workflow transitions** — can transition products to "Approved" or "Archived" states (see Section 5)

**Typical Users:**
- Product Information Manager
- Catalog Manager / Category Manager
- Solution Architect (during implementation)
- Data Quality Lead

### 8.3 PIM User Role

**Purpose:** Content contributor access for day-to-day product enrichment. This role is designed for team members who create and edit product data but should not modify system configuration or delete records.

**Permission Grants:**

| DocType | Read | Write | Create | Delete | Export | Import |
|---------|------|-------|--------|--------|--------|--------|
| Product Master | ✓ | ✓ | ✓ | ✗ | ✓ | ✗ |
| Product Variant | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| Product Family | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| PIM Attribute | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| PIM Attribute Group | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Channel | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Export Profile | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Brand | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Manufacturer | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |

**Key Differences from PIM Manager:**
1. **Read-only on configuration DocTypes** — Product Family, PIM Attribute, PIM Attribute Group, Channel, Export Profile, Brand, Manufacturer are all read-only
2. **No delete permission** — cannot delete any PIM records, even Product Master/Variant
3. **No import permission** — cannot use Frappe's bulk Data Import tool
4. **No export on Product Variant** — can export Product Master data but not variant-level data
5. **Content creation focus** — can create and edit Product Master and Product Variant records, which is the primary enrichment workflow

**Typical Users:**
- Content Editor / Product Copywriter
- Digital Merchandiser
- Product Data Entry Specialist
- Supplier data contributor

### 8.4 Permission Comparison Matrix

The following matrix provides a consolidated view of all permission grants across all PIM DocTypes:

| DocType | System Manager | PIM Manager | PIM User |
|---------|----------------|-------------|----------|
| Product Master | Full (RWCDIE) | Full (RWCDIE) | R, W, C, E |
| Product Variant | Full (RWCDIE) | Full (RWCDIE) | R, W, C |
| Product Family | Full (RWCDIE) | Full (RWCDIE) | R only |
| PIM Attribute | Full (RWCDIE) | Full (RWCDIE) | R only |
| PIM Attribute Group | Full (RWCDIE) | Full (RWCDIE) | R only |
| Channel | Full (RWCDIE) | Full (RWCDIE) | R only |
| Export Profile | Full (RWCDIE) | Full (RWCDIE) | R only |
| Brand | Full (RWCDIE) | Full (RWCDIE) | R only |
| Manufacturer | Full (RWCDIE) | Full (RWCDIE) | R only |

> **Legend:** R = Read, W = Write, C = Create, D = Delete, I = Import, E = Export

**Child Table DocTypes** (Product Attribute Value, Product Channel, Product Media, Product Relation, Family Attribute Template, Family Variant Attribute) inherit permissions from their parent DocType at runtime and do not define independent permission blocks.

### 8.5 PIM Category Permission DocType

**DocType:** `PIM Category Permission`
**Purpose:** Provides **category-based access control** — restricts individual users or roles to specific Product Families (categories) within the PIM hierarchy. This enables scenarios where different teams manage different product lines.

> **Note:** This DocType extends the base role model with fine-grained, family-level access. While the DocType definition may be provisioned separately (it is referenced in the spec but not present in all installations), its design pattern follows Frappe's User Permission model.

**Conceptual Fields:**

| Field | Type | Purpose | Customization Impact |
|-------|------|---------|---------------------|
| `user` | Link → User | The user being restricted | Per-user category access |
| `role` | Link → Role | Optional: apply to all users with this role | Role-level category access |
| `product_family` | Link → Product Family | The family to grant access to | Scopes data visibility |
| `include_descendants` | Check | Also grant access to child families in hierarchy | Hierarchy-aware permissions |
| `permission_level` | Select | `Read Only`, `Read + Write`, `Full Access` | Granularity of access |

**Use Cases:**

```
Fashion Retailer — Category-Based Team Structure:
  ├── Team A (Womenswear)
  │   └── PIM Category Permission:
  │       user: sarah@brand.com
  │       product_family: Womenswear
  │       include_descendants: ✓
  │       permission_level: Full Access
  │
  ├── Team B (Menswear)
  │   └── PIM Category Permission:
  │       user: john@brand.com
  │       product_family: Menswear
  │       include_descendants: ✓
  │       permission_level: Read + Write
  │
  └── Team C (Accessories — External agency)
      └── PIM Category Permission:
          user: agency@external.com
          product_family: Accessories
          include_descendants: ✗
          permission_level: Read + Write
```

**Integration with Frappe User Permission:**

PIM Category Permission works alongside Frappe's built-in **User Permission** system. When configured:

1. A user with `PIM User` role sees **all** PIM data by default
2. Adding a `PIM Category Permission` record **restricts** their view to only products within the specified family
3. If `include_descendants` is checked, all child families in the NestedSet tree are also accessible
4. Multiple `PIM Category Permission` records can be created for the same user (granting access to multiple families)

**Implementation Pattern:**

```python
# Conceptual permission query condition
# Applied as permission_query_conditions on Product Master
def get_product_permission_query(user):
    """Restrict Product Master visibility based on PIM Category Permission."""
    if "System Manager" in frappe.get_roles(user):
        return ""  # System Manager sees everything

    if "PIM Manager" in frappe.get_roles(user):
        return ""  # PIM Manager sees everything

    # For PIM User, check category permissions
    permitted_families = get_permitted_families(user)
    if permitted_families:
        return f"`tabProduct Master`.product_family IN ({permitted_families})"
    return ""  # No restriction if no category permissions defined
```

**When to Configure:** Phase 3 — after team structure and product families are established
**Who Configures:** System Manager or PIM Manager
**Business Impact:** Enables large organizations to divide product management responsibilities across teams while preventing unauthorized modifications

### 8.6 Data Steward Assignments

**DocType:** `Data Steward`
**Purpose:** Assigns **data ownership and quality accountability** to specific users for defined product scopes. Data Stewards are responsible for ensuring data completeness, accuracy, and timeliness within their assigned scope.

> **Note:** This DocType is part of the MDM (Master Data Management) layer of PIM. It creates accountability chains for product data quality.

**Conceptual Fields:**

| Field | Type | Purpose | Customization Impact |
|-------|------|---------|---------------------|
| `steward_user` | Link → User | The user designated as Data Steward | Accountability assignment |
| `steward_name` | Data | Display name | UI display |
| `scope_type` | Select | `Product Family`, `Brand`, `Channel`, `All` | What scope the steward covers |
| `scope_value` | Dynamic Link | The specific family, brand, or channel | Granular assignment |
| `is_primary` | Check | Primary steward (receives escalations) | Escalation routing |
| `notification_enabled` | Check | Receive quality alerts | Alert configuration |
| `quality_threshold` | Percent | Minimum acceptable completeness | Quality gating |

**Data Steward Responsibility Model:**

```
Enterprise Data Stewardship Structure:
  │
  ├── Chief Data Steward (PIM Manager role)
  │   scope_type: All
  │   Responsibilities:
  │     - Overall data quality KPIs
  │     - Escalation resolution
  │     - Policy enforcement
  │
  ├── Category Steward (PIM Manager or PIM User role)
  │   scope_type: Product Family
  │   scope_value: Electronics
  │   Responsibilities:
  │     - Category-level completeness targets
  │     - Attribute accuracy within category
  │     - New product onboarding for category
  │
  ├── Brand Steward (PIM User role)
  │   scope_type: Brand
  │   scope_value: Samsung
  │   Responsibilities:
  │     - Brand guideline compliance
  │     - Brand-specific attribute accuracy
  │     - Media quality for brand products
  │
  └── Channel Steward (PIM User role)
      scope_type: Channel
      scope_value: Amazon
      Responsibilities:
        - Channel readiness compliance
        - Channel-specific field completion
        - Listing quality monitoring
```

**Integration Points:**
- **Data Quality Policy** (Section 6) — stewards are notified when products in their scope fall below quality thresholds
- **Workflow transitions** (Section 5) — stewards may be required approvers for lifecycle state changes
- **Scoring system** (Section 6) — steward performance can be tracked via aggregate scores of their product scope
- **Notification Rules** — PIM Notification Rules can target Data Stewards for automated alerts

**When to Configure:** Phase 3 — after product families and quality policies are established
**Who Configures:** PIM Manager
**Business Impact:** Creates clear accountability for data quality; enables quality dashboards per steward; drives completeness improvements through ownership

### 8.7 Workflow-State Permission Gating

Role permissions interact with the workflow lifecycle (Section 5) to control **who can perform specific state transitions**:

| Transition | Required Role | Notes |
|------------|---------------|-------|
| → In Preparation | PIM User, PIM Manager | Initial creation state |
| In Preparation → In Production | PIM User, PIM Manager | Begin enrichment |
| In Production → Assigned | PIM Manager | Assign to specific user |
| Assigned → Awaiting Acceptance | PIM User (assignee) | Submit enriched product |
| Awaiting Acceptance → Awaiting Approval | PIM Manager | Accept enrichment |
| Awaiting Approval → Approved | PIM Manager | Final approval gate |
| Approved → Archived | PIM Manager | Retire product |
| Any → In Preparation | PIM Manager | Reset/rework |

**Key Principle:** PIM Users can perform day-to-day enrichment transitions (create, enrich, submit), but only PIM Managers can perform supervisory transitions (assign, accept, approve, archive, reset).

### 8.8 Custom Role Configuration for Specific Deployments

While PIM ships with two roles, customers can **create additional custom roles** via Frappe's Role DocType for more granular access:

| Custom Role | Typical Use Case | Configuration Approach |
|-------------|-----------------|----------------------|
| PIM Reviewer | QA/review-only access (read + comment, no write) | Copy PIM User permissions, remove write/create |
| PIM Importer | Bulk data import specialist | Copy PIM User, add import on Product Master |
| Category Admin | Full access to specific product families only | PIM Manager + PIM Category Permission restrictions |
| Brand Portal User | External supplier/brand contributor | PIM User + strict category permission + limited DocType access |
| Data Steward | Quality-focused role | PIM User + Data Steward assignment + notification rules |

**How to Create:**
1. Navigate to **Setup → Role** in Frappe Desk
2. Create a new Role (e.g., `PIM Reviewer`)
3. Go to each PIM DocType's Permission settings and add the new role with desired grants
4. Assign the role to users via **User → Roles** tab

#### Customer Archetype Examples — Roles & Permissions

**Fashion Retailer (50+ users):**
```
Roles:
  ├── System Manager (2 users) — IT admin, full system access
  ├── PIM Manager (5 users) — Category managers, one per department
  ├── PIM User (30 users) — Content editors, copywriters, photographers
  ├── PIM Reviewer (10 users) — QA team, brand compliance reviewers
  └── Brand Portal User (5 users) — External agencies for localization

Category Permissions:
  ├── Womenswear team → Family: Womenswear (include descendants)
  ├── Menswear team → Family: Menswear (include descendants)
  ├── Kidswear team → Family: Kidswear (include descendants)
  └── Accessories team → Family: Accessories (include descendants)
```

**Industrial Supplier (10 users):**
```
Roles:
  ├── System Manager (1 user) — IT/ERP admin
  ├── PIM Manager (2 users) — Product manager + technical writer
  └── PIM User (7 users) — Engineers contributing technical specs

No category permissions needed — small team, all products visible to all
```

**Food Manufacturer (25 users):**
```
Roles:
  ├── System Manager (1 user) — IT admin
  ├── PIM Manager (3 users) — Category managers per product line
  ├── PIM User (15 users) — R&D, marketing, regulatory team
  └── Data Steward (6 users) — Regulatory compliance stewards per region

Category Permissions:
  ├── Fresh Produce team → Family: Fresh (include descendants)
  ├── Packaged Foods team → Family: Packaged (include descendants)
  └── Beverages team → Family: Beverages (include descendants)

Data Stewards:
  ├── EU Regulatory Steward → scope: Channel (EU Markets)
  ├── US Regulatory Steward → scope: Channel (US Markets)
  └── Halal Certification Steward → scope: Brand (Halal-certified lines)
```

### 8.9 Permission API & Runtime Access

**Source:** `frappe_pim/pim/api/permission.py`

The PIM app exposes a minimal permission API for UI integration:

```python
# frappe_pim/pim/api/permission.py
import frappe

def has_app_permission():
    """Check if the current user has access to the PIM app.

    Used by hooks.py → add_to_apps_screen for the /apps page.
    Currently returns True (all desk users can see the PIM app icon).
    """
    return True
```

This function is referenced in `hooks.py`:

```python
add_to_apps_screen = [
    {
        "name": "frappe_pim",
        "logo": "/assets/frappe_pim/images/pim-logo.png",
        "title": "PIM",
        "route": "/app/pim",
        "has_permission": "frappe_pim.pim.api.permission.has_app_permission"
    }
]
```

**Customization Opportunity:** Override `has_app_permission()` to restrict PIM app visibility to only users with `PIM Manager` or `PIM User` roles:

```python
def has_app_permission():
    """Restrict PIM app visibility to PIM role holders."""
    user_roles = frappe.get_roles(frappe.session.user)
    return bool(set(user_roles) & {"System Manager", "PIM Manager", "PIM User"})
```

**Additional Permission Hooks (commented in hooks.py):**

```python
# Custom permission conditions for DocTypes
# permission_query_conditions = {
#     "Product Master": "frappe_pim.pim.permissions.get_product_permission_query",
# }

# Custom has_permission check
# has_permission = {
#     "Product Master": "frappe_pim.pim.permissions.has_product_permission",
# }
```

These hooks are pre-configured but commented out. To enable category-based permission filtering:

1. Implement `get_product_permission_query()` that reads `PIM Category Permission` records
2. Uncomment the `permission_query_conditions` hook in `hooks.py`
3. Run `bench --site [site] clear-cache`

### 8.10 Onboarding Checklist — Roles & Permissions

```
Phase 1 — Installation (Automatic):
  ✓ PIM Manager and PIM User roles created by install.py
  ✓ Default permissions applied to all PIM DocTypes

Phase 2 — User Setup:
  □ Identify team members and their required access levels
  □ Assign PIM Manager role to catalog administrators
  □ Assign PIM User role to content contributors
  □ Create any custom roles needed (PIM Reviewer, Brand Portal User, etc.)
  □ Configure custom role permissions on each PIM DocType

Phase 3 — Category Permissions (if needed):
  □ Define product family → team mappings
  □ Create PIM Category Permission records per user or role
  □ Test that users can only see their assigned families
  □ Enable permission_query_conditions hook if using category filtering

Phase 4 — Data Stewardship (if needed):
  □ Define stewardship scope model (by family, brand, or channel)
  □ Create Data Steward records for each steward
  □ Configure notification rules for quality alerts
  □ Set quality thresholds per steward scope
```

---

## 9. Taxonomy & Navigation

### Overview

Frappe PIM provides a **multi-layered taxonomy system** that enables customers to organize products into hierarchical classification structures. The taxonomy layer operates independently from the Product Family hierarchy (Section 1.3) and supports multiple concurrent classification schemes — such as a merchandising taxonomy, a regulatory taxonomy, and a channel-specific taxonomy.

**Key Design Principles:**
1. **Product Family = Structural Hierarchy** — determines which attributes a product has (data model)
2. **Taxonomy = Navigational Hierarchy** — determines how products are organized for browsing, search, and channel publishing (user-facing)
3. **Category = Product Classification** — the actual node where a product is placed within a taxonomy
4. **Multiple Taxonomies per Product** — a single product can be classified in several taxonomies simultaneously

**Architecture:**

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        Taxonomy Architecture                            │
│                                                                          │
│  ┌─────────────┐    ┌─────────────────┐    ┌─────────────────────────┐  │
│  │  Taxonomy    │──▶│  Taxonomy Node   │──▶│ Node Attribute           │  │
│  │  (Root)      │    │  (NestedSet      │    │ Suggestion               │  │
│  │              │    │   Tree Node)     │    │ (Recommended attrs)      │  │
│  └─────────────┘    └─────────────────┘    └─────────────────────────┘  │
│                             │                                            │
│                             ▼                                            │
│                     ┌─────────────────┐                                  │
│                     │  Category        │                                 │
│                     │  (NestedSet      │                                 │
│                     │   Classification)│                                 │
│                     └─────────────────┘                                  │
│                             │                                            │
│                             ▼                                            │
│                     ┌─────────────────┐                                  │
│                     │  Product Master  │                                 │
│                     │  (classified in  │                                 │
│                     │   categories)    │                                 │
│                     └─────────────────┘                                  │
└──────────────────────────────────────────────────────────────────────────┘
```

### 9.1 Product Family as Primary Hierarchy (NestedSet)

**DocType:** `Product Family`
**Tree Support:** `is_tree: true`, `nsm_parent_field: "parent_family"`
**Module:** PIM

Product Family serves as the **primary structural hierarchy** in PIM. It uses Frappe's built-in **NestedSet Model** (Modified Preorder Tree Traversal / MPTT) for efficient tree operations.

**NestedSet Implementation Details:**

When `is_tree: true` is set in the DocType JSON, Frappe automatically:
- Adds `lft` (left) and `rgt` (right) integer columns to the database table
- Provides tree-view rendering in the Desk list view
- Enforces parent-child integrity via the `nsm_parent_field`
- Supports efficient subtree queries (all descendants, ancestors, siblings)

**Tree Fields:**

| Field | Type | Purpose | Customization Impact |
|-------|------|---------|---------------------|
| `parent_family` | Link → Product Family | Parent node in hierarchy | Defines tree structure |
| `lft` | Int (auto) | Left value for MPTT | Auto-calculated, do not modify directly |
| `rgt` | Int (auto) | Right value for MPTT | Auto-calculated, do not modify directly |

**Hierarchy Example:**

```
Product Family Tree (is_tree: true, nsm_parent_field: parent_family):

Root
├── Apparel (lft=1, rgt=14)
│   ├── Tops (lft=2, rgt=7)
│   │   ├── T-Shirts (lft=3, rgt=4)
│   │   └── Shirts (lft=5, rgt=6)
│   └── Bottoms (lft=8, rgt=13)
│       ├── Pants (lft=9, rgt=10)
│       └── Skirts (lft=11, rgt=12)
├── Footwear (lft=15, rgt=20)
│   ├── Athletic (lft=16, rgt=17)
│   └── Formal (lft=18, rgt=19)
└── Accessories (lft=21, rgt=24)
    └── Bags (lft=22, rgt=23)
```

**Tree Query Patterns:**

```python
# Get all descendants of "Apparel" using NestedSet
# (any node where lft > 1 AND rgt < 14)
descendants = frappe.get_all("Product Family",
    filters={"lft": [">", apparel_lft], "rgt": ["<", apparel_rgt]})

# Get all ancestors of "T-Shirts"
# (any node where lft < 3 AND rgt > 4)
ancestors = frappe.get_all("Product Family",
    filters={"lft": ["<", tshirt_lft], "rgt": [">", tshirt_rgt]})

# Count products in a subtree (including all descendants)
product_count = frappe.db.count("Product Master",
    filters={"product_family": ["in", [f.name for f in descendants]]})
```

**Attribute Inheritance Through Hierarchy:**

When `inherit_parent_attributes` is checked on a Product Family (default: `1`), all Family Attribute Template entries from ancestor families are automatically available to products in child families. This means:

1. Attributes defined on "Apparel" are inherited by "Tops", "T-Shirts", "Shirts", etc.
2. Each child family can add **additional** attributes beyond what's inherited
3. Child families cannot **remove** inherited attributes, only add to them

**When to Configure:** Phase 1 — Product Family hierarchy is one of the first structures established
**Who Configures:** PIM Manager or Solution Architect
**Business Impact:** Defines the primary product classification that drives attribute assignment, completeness scoring, and ERP Item Group mapping

### 9.2 Category DocType

**DocType:** `Category`
**Purpose:** Provides a **navigational/browsable classification** hierarchy independent of Product Family. Categories are used for customer-facing navigation, channel-specific categorization, and cross-cutting classification schemes.

> **Note:** This DocType is referenced in the system specification for taxonomy/navigation purposes. While not present in all installations, it follows the NestedSet pattern established by Product Family.

**Conceptual Design:**

| Field | Type | Purpose | Customization Impact |
|-------|------|---------|---------------------|
| `category_name` | Data (required, translatable) | Display name | Multi-language navigation labels |
| `category_code` | Data (required, unique) | Unique identifier slug | API reference, URL generation |
| `parent_category` | Link → Category | Parent in hierarchy | Defines tree structure (NestedSet) |
| `taxonomy` | Link → Taxonomy | Which taxonomy this category belongs to | Multi-taxonomy support |
| `is_active` | Check | Enable/disable category | Controls navigation visibility |
| `image` | Attach Image | Category image | Visual navigation |
| `description` | Text Editor | Category description | Storefront display |
| `sort_order` | Int | Display order among siblings | Navigation ordering |
| `seo_title` | Data | SEO-optimized title | Channel/website SEO |
| `seo_description` | Small Text | SEO meta description | Channel/website SEO |
| `channel_category_mapping` | Small Text / JSON | Marketplace category ID mappings | Maps PIM categories to channel taxonomies |

**Category vs. Product Family:**

| Aspect | Product Family | Category |
|--------|---------------|----------|
| Primary purpose | Define product data structure (attributes) | Define navigation/browsing hierarchy |
| Affects attributes? | Yes — determines which attributes a product has | No — does not affect product attributes |
| Products per node | Exactly one family per product | Multiple categories per product |
| Tree structure | NestedSet (`is_tree: true`) | NestedSet (planned) |
| ERP mapping | Maps to Item Group | Maps to channel categories |
| Configured by | PIM Manager (Phase 1) | PIM Manager (Phase 2-3) |

**Multiple Categories per Product:**

Unlike Product Family (which is a strict one-to-one assignment), a single Product Master can be classified in **multiple categories** across different taxonomies:

```
Product: "Organic Cotton T-Shirt" (PM-001)
  ├── Product Family: Apparel > Tops > T-Shirts   (structural — defines attributes)
  │
  ├── Category in Merchandising Taxonomy:
  │   └── Men's > Casual > T-Shirts & Polos
  │
  ├── Category in Amazon Taxonomy:
  │   └── Clothing > Men > Shirts > T-Shirts
  │
  ├── Category in Google Product Category:
  │   └── Apparel & Accessories > Clothing > Shirts & Tops
  │
  └── Category in Sustainability Taxonomy:
      └── Eco-Friendly > Organic Cotton > Certified GOTS
```

### 9.3 Taxonomy DocType

**DocType:** `Taxonomy`
**Purpose:** Defines a **classification scheme** (a named tree of categories). Each taxonomy represents a different way to organize products — e.g., a merchandising taxonomy, a channel taxonomy, or a regulatory taxonomy.

> **Note:** This DocType is part of the planned taxonomy system. It follows the pattern of a container/parent that owns a tree of Taxonomy Nodes.

**Conceptual Design:**

| Field | Type | Purpose | Customization Impact |
|-------|------|---------|---------------------|
| `taxonomy_name` | Data (required) | Display name | UI labeling |
| `taxonomy_code` | Data (required, unique) | Unique identifier | API reference |
| `taxonomy_type` | Select | `Merchandising`, `Channel`, `Regulatory`, `Internal`, `Custom` | Classification purpose |
| `is_active` | Check | Enable/disable entire taxonomy | Controls visibility |
| `description` | Text | Taxonomy description | Documentation |
| `owner_channel` | Link → Channel | If channel-specific, which channel | Channel taxonomy binding |
| `is_hierarchical` | Check | Whether nodes form a tree (vs. flat tags) | Structure type |
| `max_depth` | Int | Maximum hierarchy depth | Constraint enforcement |
| `allow_multiple_parents` | Check | DAG support (node in multiple parents) | Polyhierarchy support |

**Pre-Built Taxonomy Types:**

| Taxonomy Type | Purpose | Example Use Case |
|---------------|---------|-----------------|
| `Merchandising` | Customer-facing product navigation | Website category tree, in-store taxonomy |
| `Channel` | Marketplace-specific classification | Amazon Browse Nodes, Google Product Categories |
| `Regulatory` | Compliance classification | Hazmat classification, allergen categories |
| `Internal` | Internal organization | Procurement categories, warehouse zones |
| `Custom` | Customer-defined | Any other classification scheme |

#### Customer Archetype Examples — Taxonomies

**Fashion Retailer:**
```
Taxonomies:
  ├── Merchandising Taxonomy (customer-facing)
  │   ├── Women's
  │   │   ├── Dresses → Casual Dresses, Evening Dresses, ...
  │   │   ├── Tops → T-Shirts, Blouses, Sweaters, ...
  │   │   └── Bottoms → Jeans, Skirts, Pants, ...
  │   ├── Men's
  │   │   ├── Shirts → Dress Shirts, Casual Shirts, ...
  │   │   └── Pants → Chinos, Jeans, Trousers, ...
  │   └── Kids
  │
  ├── Amazon Category Taxonomy (channel-specific)
  │   └── Mapped to Amazon Browse Node IDs
  │
  ├── Trendyol Category Taxonomy (channel-specific)
  │   └── Mapped to Trendyol category IDs
  │
  └── Season/Collection Taxonomy (internal)
      ├── SS2026 (Spring/Summer 2026)
      ├── FW2026 (Fall/Winter 2026)
      └── Evergreen
```

**Industrial Supplier:**
```
Taxonomies:
  ├── UNSPSC Taxonomy (industry standard)
  │   └── United Nations Standard Products & Services Code hierarchy
  │
  ├── Internal Procurement Taxonomy
  │   ├── Raw Materials
  │   │   ├── Metals → Steel, Aluminum, Copper, ...
  │   │   └── Plastics → ABS, Polycarbonate, Nylon, ...
  │   ├── Components
  │   │   ├── Fasteners → Bolts, Nuts, Screws, ...
  │   │   └── Electronics → Resistors, Capacitors, ...
  │   └── Equipment
  │
  └── Hazmat Classification Taxonomy (regulatory)
      ├── Class 1: Explosives
      ├── Class 2: Gases
      ├── Class 3: Flammable Liquids
      └── ...
```

**Food Manufacturer:**
```
Taxonomies:
  ├── GPC Taxonomy (GS1 Global Product Classification)
  │   └── Standard GPC hierarchy for GDSN compliance
  │
  ├── Allergen Classification Taxonomy (regulatory)
  │   ├── Contains Gluten
  │   ├── Contains Dairy
  │   ├── Contains Nuts
  │   └── ...
  │
  ├── Dietary Classification Taxonomy
  │   ├── Vegan
  │   ├── Vegetarian
  │   ├── Kosher
  │   ├── Halal
  │   └── Organic
  │
  └── Retail Channel Taxonomy
      └── Mapped to retailer-specific planogram categories
```

### 9.4 Taxonomy Node DocType

**DocType:** `Taxonomy Node`
**Purpose:** Represents a **single node** within a Taxonomy tree. Each node can have children (forming a hierarchy) and can have associated attribute suggestions.

> **Note:** This DocType implements the NestedSet pattern for efficient hierarchical queries within each taxonomy.

**Conceptual Design:**

| Field | Type | Purpose | Customization Impact |
|-------|------|---------|---------------------|
| `node_name` | Data (required, translatable) | Display name | Multi-language category labels |
| `node_code` | Data (required, unique) | Unique identifier | API reference |
| `taxonomy` | Link → Taxonomy | Parent taxonomy | Taxonomy grouping |
| `parent_node` | Link → Taxonomy Node | Parent node in tree | Hierarchy structure (NestedSet) |
| `is_leaf` | Check | Whether this is a leaf node (no children) | UI behavior |
| `is_active` | Check | Enable/disable node | Controls visibility |
| `sort_order` | Int | Display order among siblings | Navigation ordering |
| `external_id` | Data | External system category ID | Channel mapping |
| `image` | Attach Image | Node image/icon | Visual navigation |
| `description` | Text | Node description | Documentation / storefront |
| `attribute_suggestions` | Table → Node Attribute Suggestion | Recommended attributes for products in this node | Data quality guidance |

**Node Attribute Suggestion Pattern:**

Each Taxonomy Node can define **recommended attributes** for products classified under it. This creates a guidance system that helps content editors know which attributes are important for products in each category:

```
Taxonomy Node: Electronics > Laptops
  Attribute Suggestions:
    ├── screen_size (Required) — "Screen diagonal in inches"
    ├── processor_type (Required) — "CPU model/brand"
    ├── ram_size (Required) — "RAM in GB"
    ├── storage_type (Recommended) — "SSD, HDD, or Hybrid"
    ├── storage_capacity (Recommended) — "Storage in GB/TB"
    ├── battery_life (Optional) — "Battery life in hours"
    └── weight (Optional) — "Weight in kg"
```

### 9.5 Node Attribute Suggestion DocType

**DocType:** `Node Attribute Suggestion`
**Purpose:** Child table of Taxonomy Node that **recommends** which PIM Attributes are relevant for products classified in that node. Unlike Family Attribute Template (which enforces attributes), this provides **guidance** without enforcement.

**Conceptual Design:**

| Field | Type | Purpose | Customization Impact |
|-------|------|---------|---------------------|
| `attribute` | Link → PIM Attribute | The recommended attribute | Attribute guidance |
| `importance` | Select | `Required`, `Recommended`, `Optional` | Priority guidance |
| `help_text` | Small Text | Guidance for content editors | Contextual help |
| `default_value` | Data | Suggested default value for this category | Pre-population |

**Comparison: Attribute Template vs. Attribute Suggestion:**

| Aspect | Family Attribute Template | Node Attribute Suggestion |
|--------|--------------------------|---------------------------|
| DocType parent | Product Family | Taxonomy Node |
| Enforcement level | **Mandatory** — attribute appears on product form | **Advisory** — appears as guidance/recommendation |
| Affects completeness? | Yes — required attributes count toward completeness | Optional — can be configured to influence scoring |
| Inheritance | Inherits from parent family if `inherit_parent_attributes` | Does not inherit |
| Purpose | Defines product data model | Guides content enrichment |

### 9.6 Channel-Specific Taxonomy Mapping

Each sales channel (Section 4) typically requires products to be classified in the channel's own taxonomy. The taxonomy system bridges PIM's internal categories to channel-specific categories:

**Channel Category Mapping Pattern:**

| Channel | Category System | Mapping Approach |
|---------|----------------|-----------------|
| Amazon | Browse Node IDs (numeric) | Map Taxonomy Node → Amazon Browse Node ID |
| Google Merchant | Google Product Categories (hierarchical text) | Map Taxonomy Node → GPC path string |
| Trendyol | Trendyol Category IDs (numeric) | Map Taxonomy Node → Trendyol category ID |
| Hepsiburada | Hepsiburada Category IDs | Map Taxonomy Node → Hepsiburada category ID |
| N11 | N11 Category IDs | Map Taxonomy Node → N11 category ID |
| Shopify | Collections (flat or smart) | Map Taxonomy Node → Shopify collection handle |
| WooCommerce | WP Category IDs | Map Taxonomy Node → WooCommerce category ID |
| eBay | eBay Category IDs | Map Taxonomy Node → eBay category ID |
| Etsy | Etsy Taxonomy IDs | Map Taxonomy Node → Etsy taxonomy ID |
| Walmart | Walmart Product Type | Map Taxonomy Node → Walmart product type path |
| Meta Commerce | Facebook Product Categories | Map Taxonomy Node → Meta category ID |
| TikTok Shop | TikTok Category IDs | Map Taxonomy Node → TikTok category ID |

**Implementation Pattern:**

```python
# Each Taxonomy Node can store external_id per channel
# The channel export process reads the mapped category:

def get_channel_category(product, channel):
    """Resolve the channel-specific category for a product.

    1. Find the product's taxonomy node for the channel's taxonomy
    2. Read the external_id from the taxonomy node
    3. Return the mapped channel category ID
    """
    channel_taxonomy = frappe.db.get_value("Taxonomy",
        {"owner_channel": channel, "taxonomy_type": "Channel"})

    if not channel_taxonomy:
        return None

    # Find the product's classification in this taxonomy
    product_node = frappe.db.get_value("Product Category Assignment",
        {"product": product, "taxonomy": channel_taxonomy},
        "taxonomy_node")

    if product_node:
        return frappe.db.get_value("Taxonomy Node", product_node, "external_id")

    return None
```

### 9.7 Navigation Hierarchy Configuration Per Customer

The taxonomy system is **fully configurable per customer** — each deployment can define:

1. **How many taxonomies** — from 1 (simple merchandising) to 10+ (complex multi-channel)
2. **Hierarchy depth** — from 2 levels (flat) to 7+ levels (deep departmental)
3. **Node naming** — customer-specific terminology and translations
4. **Channel mappings** — which PIM categories map to which marketplace categories
5. **Attribute suggestions per node** — what data is important for each category

**Configuration Decision Tree:**

```
Q: How many sales channels does the customer use?
├── 0-1 channels → Single merchandising taxonomy may suffice
├── 2-4 channels → Merchandising + per-channel taxonomies
└── 5+ channels → Merchandising + channel taxonomies + mapping automation

Q: Does the customer need regulatory classification?
├── No → Skip regulatory taxonomy
├── Food/Pharma → Allergen + GPC taxonomies
└── Industrial → Hazmat + UNSPSC taxonomies

Q: Does the customer need internal classification?
├── No → Use merchandising taxonomy for all purposes
├── Yes → Add internal taxonomy (procurement, warehouse, etc.)
└── Multi-company → Consider per-company internal taxonomies

Q: How deep should the hierarchy be?
├── Simple catalog (< 1000 SKUs) → 2-3 levels
├── Medium catalog (1K-50K SKUs) → 3-5 levels
└── Enterprise catalog (50K+ SKUs) → 5-7 levels
```

### 9.8 Taxonomy vs. Product Family — When to Use Which

A common question during onboarding is: **"Should I use Product Family or Category/Taxonomy to organize my products?"**

**Answer: Use both.** They serve different purposes:

| Decision Factor | Use Product Family | Use Taxonomy/Category |
|----------------|-------------------|----------------------|
| "Products need different fields" | ✓ Family defines which attributes appear | — |
| "Products need different navigation paths" | — | ✓ Categories define navigation |
| "Products belong to one group exclusively" | ✓ One family per product | — |
| "Products can be in multiple groups" | — | ✓ Multiple categories per product |
| "Group determines ERP Item Group" | ✓ Family → Item Group mapping | — |
| "Group determines channel category" | — | ✓ Taxonomy Node → Channel category |
| "Group affects completeness scoring" | ✓ Family attributes drive completeness | Optionally via attribute suggestions |
| "Group is for end-user browsing" | — | ✓ Categories power storefront navigation |

**Recommended Configuration Pattern:**

```
Product Family (Structural — configure first):
  Used for: Attribute assignment, ERP mapping, data model
  Depth: 2-4 levels
  Examples: Electronics > Computers > Laptops
            Food > Packaged > Snacks

Taxonomy (Navigational — configure second):
  Used for: Browsing, channel publishing, cross-cutting classification
  Depth: 3-7 levels
  Examples: Merchandising: Men's > Clothing > Casual > T-Shirts
            Amazon: Clothing > Men > Shirts > T-Shirts
            Allergen: Contains > Dairy > Lactose
```

### 9.9 Onboarding Checklist — Taxonomy & Navigation

```
Phase 1 — Product Family Hierarchy (during initial setup):
  □ Design the structural family hierarchy (2-4 levels)
  □ Create Product Family records with parent_family relationships
  □ Assign attributes via Family Attribute Template
  □ Map each family to ERPNext Item Group (if ERP sync enabled)
  □ Set inherit_parent_attributes for child families

Phase 2 — Merchandising Taxonomy (after products are loaded):
  □ Create a Taxonomy record (type: Merchandising)
  □ Build the taxonomy node hierarchy
  □ Add translations for multi-language deployments
  □ Classify products into taxonomy nodes
  □ Configure attribute suggestions for key nodes

Phase 3 — Channel Taxonomies (when channels are configured):
  □ Create a Taxonomy per active channel (type: Channel)
  □ Import or manually build channel category hierarchies
  □ Map PIM taxonomy nodes to channel category IDs (external_id)
  □ Verify mappings by running test channel exports

Phase 4 — Additional Taxonomies (as needed):
  □ Create regulatory taxonomies (allergen, hazmat, etc.) if applicable
  □ Create internal taxonomies (procurement, warehouse) if needed
  □ Set up attribute suggestions for regulatory compliance nodes
  □ Configure multi-taxonomy product classification rules
```

---

## 10. AI & Enrichment

### Overview

Frappe PIM includes a comprehensive **AI-powered product enrichment** system that automates content generation, attribute extraction, product categorization, and multi-language translation. The system supports **6 AI providers** (Anthropic, OpenAI, Google Gemini, Azure OpenAI, AWS Bedrock, Custom), includes a **human-in-the-loop approval workflow**, and provides a **Jinja2-based prompt templating system** for full customization of AI behavior.

**Architecture:**

```
┌──────────────────────────────────────────────────────────┐
│                    AI Enrichment Pipeline                  │
│                                                            │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │ AI Enrichment│───▶│  AI Provider  │───▶│ AI Approval  │ │
│  │    Job       │    │  (6 options)  │    │    Queue     │ │
│  └──────┬──────┘    └──────────────┘    └──────┬───────┘ │
│         │                                        │         │
│         │           ┌──────────────┐             │         │
│         └──────────▶│  AI Prompt   │             │         │
│                     │  Template    │             │         │
│                     └──────────────┘             │         │
│                                                  ▼         │
│                                          ┌────────────┐   │
│                                          │  Product    │   │
│                                          │  Master     │   │
│                                          └────────────┘   │
└──────────────────────────────────────────────────────────┘
```

**Key DocTypes:**

| DocType | Purpose | Naming | Submittable |
|---------|---------|--------|-------------|
| `AI Enrichment Job` | Batch AI processing orchestrator | `AIJ-.YYYY.-.#####` | Yes |
| `AI Prompt Template` | Jinja2 prompt configuration | `APT-.####` | No |
| `AI Approval Queue` | Human-in-the-loop review items | Hash-based | No |

### 10.1 AI Provider Selection

The PIM supports 6 AI provider backends. Provider selection is configured at two levels:

1. **Global default** — `PIM Settings` → `ai_provider` field
2. **Per-job override** — `AI Enrichment Job` → `ai_provider` field
3. **Per-template default** — `AI Prompt Template` → `default_ai_provider` field

**Supported Providers:**

| Provider | Options Value | Models | Context Window | Pricing (Input/Output per 1M tokens) |
|----------|--------------|--------|---------------|--------------------------------------|
| **Anthropic** | `Anthropic` | Claude 3.5 Sonnet (latest), Claude 3 Opus/Sonnet/Haiku, Claude 2.1/2.0 | 100K–200K tokens | $0.25–$15.00 / $1.25–$75.00 |
| **OpenAI** | `OpenAI` | GPT-4o (latest), GPT-4 Turbo, GPT-4, GPT-3.5 Turbo | 4K–128K tokens | Varies by model |
| **Google Gemini** | `Google Gemini` | Gemini 1.5 Pro/Flash, Gemini Pro/Pro Vision, Gemini 2.0 Flash (experimental) | 32K–2M tokens | $0.075–$3.50 / $0.30–$10.50 |
| **Azure OpenAI** | `Azure OpenAI` | Same as OpenAI (deployed to Azure endpoints) | Same as OpenAI | Enterprise pricing |
| **AWS Bedrock** | `AWS Bedrock` | Claude, Titan, Llama models via Bedrock | Varies | AWS Bedrock pricing |
| **Custom** | `Custom` | User-defined provider implementation | Configurable | N/A |

**Provider Configuration in PIM Settings:**

| Setting Field | Type | Purpose |
|--------------|------|---------|
| `enable_ai_enrichment` | Check | Master toggle — disables all AI features when unchecked |
| `ai_provider` | Select | Default provider for all AI operations |
| `ai_api_key` | Password | API key (encrypted storage via Frappe's password field type) |
| `ai_model` | Data | Default model identifier (e.g., `claude-3-sonnet`, `gpt-4-turbo`) |
| `ai_require_approval` | Check | Whether AI suggestions require manual approval before being applied |

**When to Configure:** Phase 3 of onboarding — after Product Families and Channels are set up, before bulk content generation
**Who Configures:** System Manager (API credentials), PIM Manager (model selection, approval settings)
**Business Impact:** Determines AI content quality, cost per enrichment, and data residency compliance

#### Provider Implementation Details

Each provider is implemented as a Python class extending `BaseAIProvider`:

```
frappe_pim/pim/utils/ai_providers/
├── __init__.py
├── base.py              ← Abstract base class + MockAIProvider
├── anthropic.py         ← AnthropicProvider (Claude models)
├── openai_provider.py   ← OpenAIProvider + AzureOpenAIProvider
└── gemini.py            ← GeminiProvider
```

**Base Provider Interface:**
- `generate(prompt, system_prompt, **kwargs)` → `AIResponse`
- `generate_with_messages(messages, **kwargs)` → `AIResponse`
- `estimate_tokens(text)` → `int`
- `calculate_cost(input_tokens, output_tokens)` → `float`
- `get_model_info()` → `dict` (context window, pricing, capabilities)
- `health_check()` → `bool`

**AIResponse Data Class:**
- `content` — Generated text
- `input_tokens` — Token count for prompt
- `output_tokens` — Token count for response
- `cost` — Estimated USD cost
- `model` — Model identifier used
- `metadata` — Provider-specific metadata

**Utility Functions (from `base.py`):**
- `get_api_key_from_settings(provider)` — Fetches encrypted API key from PIM Settings
- `get_provider_config_from_settings()` — Returns complete provider configuration
- `validate_api_key(key, provider)` — Validates API key format per provider
- `parse_json_response(response)` — Extracts JSON from AI text responses

#### Customer Archetype — AI Provider Selection

| Customer Profile | Recommended Provider | Rationale |
|-----------------|---------------------|-----------|
| **Fashion Retailer** (creative descriptions, high volume) | OpenAI GPT-4o or Anthropic Claude 3.5 Sonnet | Best creative writing quality; Sonnet offers strong price-performance |
| **Industrial Supplier** (technical accuracy, regulated) | Anthropic Claude 3 Opus or Azure OpenAI GPT-4 | Opus excels at technical accuracy; Azure for enterprise data residency |
| **Food Manufacturer** (multi-language, compliance) | Anthropic Claude 3.5 Sonnet + DeepL for translation | Good balance of quality and cost; DeepL for regulatory-grade translation |
| **Budget-Conscious Startup** | Google Gemini 1.5 Flash | Lowest cost per token with 1M context window |

### 10.2 AI Enrichment Job

**DocType:** `AI Enrichment Job`
**Purpose:** Orchestrates batch AI enrichment across multiple products. This is the primary workflow object for running AI operations at scale.

**Naming Rule:** `AIJ-.YYYY.-.#####` (e.g., `AIJ-2026-00042`)
**Submittable:** Yes — jobs are submitted for processing via Frappe's Submit workflow

#### Job Types (9 enrichment operations)

| Job Type | Value | What It Does | Typical Use Case |
|----------|-------|-------------|-----------------|
| **Description Generation** | `Description Generation` | Generate short/long product descriptions | Initial catalog enrichment |
| **Attribute Extraction** | `Attribute Extraction` | Extract attribute values from text/images | Migration from unstructured data |
| **Classification Suggestion** | `Classification Suggestion` | Suggest product categories across taxonomies | Multi-channel category mapping |
| **Image Analysis** | `Image Analysis` | Analyze product images for attributes, alt text | Image-heavy catalogs |
| **SEO Optimization** | `SEO Optimization` | Generate SEO titles, meta descriptions, keywords | E-commerce channel preparation |
| **Translation** | `Translation` | Translate product content to target locale | Multi-market expansion |
| **Content Enhancement** | `Content Enhancement` | Improve existing content quality | Quality score improvement |
| **Quality Check** | `Quality Check` | Validate content against quality rules | Pre-publish validation |
| **Custom** | `Custom` | User-defined enrichment via custom prompt | Industry-specific enrichment |

#### Job Status Lifecycle

```
Draft → Queued → Processing → Completed
                     │              ↗
                     └──→ Partially Completed
                     │
                     └──→ Failed
                     │
                     └──→ Cancelled
```

| Status | Color | Meaning |
|--------|-------|---------|
| `Draft` | Blue | Job configured but not yet submitted |
| `Queued` | Blue | Submitted and waiting for processing |
| `Processing` | Blue | Actively processing products |
| `Completed` | Blue | All products processed successfully |
| `Partially Completed` | Blue | Some products failed, others succeeded |
| `Failed` | Blue | Job-level failure (all products) |
| `Cancelled` | Blue | Manually cancelled by user |

#### Configurable Fields — AI Configuration Section

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `ai_provider` | Select | `Anthropic` | Provider for this job (overrides global) | Per-job provider selection |
| `ai_model` | Data | — | Specific model (e.g., `claude-3-opus`) | Controls quality vs. cost |
| `prompt_template` | Link → AI Prompt Template | — | Template defining prompt structure | Reusable prompt configurations |
| `custom_prompt` | Text | — | Ad-hoc prompt (used when no template) | Jinja2 variables supported |
| `temperature` | Float | `0.7` | Generation randomness (0.0–1.0) | Lower = deterministic, higher = creative |
| `max_tokens` | Int | `2000` | Maximum response length | Caps cost per product |

#### Configurable Fields — Target Scope

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `target_locale` | Link → PIM Locale | — | Locale for translation/localization jobs |
| `target_channel` | Link → Channel | — | Channel to optimize content for |
| `target_attributes` | Small Text | — | Comma-separated attribute codes to enrich |
| `overwrite_existing` | Check | `0` | Replace existing values vs. fill-empty-only |

#### Configurable Fields — Product Selection

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `selection_method` | Select | `Manual Selection` | How to select products for processing |
| `filter_product_family` | Link → Product Family | — | Filter by family (with sub-families) |
| `filter_product_category` | Link → Product Category | — | Filter by category |
| `filter_channel` | Link → Channel | — | Filter by channel assignment |
| `filter_query` | Small Text | — | JSON filter query (advanced) |
| `include_variants` | Check | `1` | Include product variants in processing |
| `max_products` | Int | `0` (unlimited) | Cap on number of products to process |
| `skip_completed` | Check | `1` | Skip products already enriched |
| `only_incomplete` | Check | `0` | Only process below completeness threshold |
| `min_completeness_gap` | Percent | — | Minimum gap below threshold to qualify |
| `products` | Table → Job Product Item | — | Manual product selection (for Manual Selection method) |

**Product Selection Methods (6 options):**

| Method | Value | Description |
|--------|-------|-------------|
| Manual Selection | `Manual Selection` | Pick specific products via child table |
| Product Family | `Product Family` | All products in a family (and sub-families) |
| Product Category | `Product Category` | All products in a category |
| Channel | `Channel` | Products assigned to a specific channel |
| Filter Query | `Filter Query` | JSON-based filter (e.g., `{"product_type": "Simple", "enabled": 1}`) |
| All Products | `All Products` | Every product in the system |

#### Configurable Fields — Processing Settings

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `batch_size` | Int | `10` | Products per processing batch |
| `retry_on_failure` | Check | `1` | Auto-retry failed products |
| `max_retries` | Int | `3` | Maximum retry attempts per product |
| `require_approval` | Check | `1` | Send suggestions to approval queue |
| `auto_apply_high_confidence` | Check | `0` | Auto-apply above confidence threshold |
| `auto_apply_threshold` | Percent | `95` | Minimum confidence for auto-approval |
| `notify_on_completion` | Check | `1` | Send notification when job completes |
| `notification_users` | Small Text | — | Comma-separated email list for notifications |

#### Cost Tracking Fields (read-only, auto-populated)

| Field | Type | Purpose |
|-------|------|---------|
| `total_tokens_used` | Int | Total API tokens consumed |
| `input_tokens` | Int | Tokens used for prompts |
| `output_tokens` | Int | Tokens used for responses |
| `estimated_cost` | Currency | Estimated API cost (USD) |
| `cost_per_product` | Currency | Average cost per product enriched |

#### Permission Matrix

| Role | Create | Read | Write | Submit | Cancel | Delete |
|------|--------|------|-------|--------|--------|--------|
| System Manager | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PIM Manager | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PIM User | ✓ | ✓ | ✓ | ✓ | — | — |

### 10.3 AI Prompt Template

**DocType:** `AI Prompt Template`
**Purpose:** Defines reusable, version-controlled prompt configurations for AI enrichment jobs. Uses **Jinja2 templating** for dynamic prompt construction with product data.

**Naming Rule:** `APT-.####` (e.g., `APT-0015`)

#### Template Configuration Fields

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `template_name` | Data (required, translatable) | — | Display name | User-facing identification |
| `template_code` | Data (unique) | — | Slug identifier (e.g., `desc-gen-fashion`) | Referenced in API calls and automation |
| `is_active` | Check | `1` | Enable/disable template | Controls availability |
| `is_default` | Check | `0` | Set as default for its job type | Only one default per job type |
| `job_type` | Select (required) | — | 9 job types (same as AI Enrichment Job) | Determines when this template is offered |
| `version` | Data | `1.0` | Template version tracking | Supports iterative prompt improvement |

#### AI Configuration Defaults

Each template can specify recommended AI settings that override global defaults:

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `default_ai_provider` | Select | — | Recommended provider for this template |
| `default_ai_model` | Data | — | Recommended model (e.g., `claude-3-sonnet`) |
| `default_temperature` | Float | `0.7` | Recommended temperature |
| `default_max_tokens` | Int | `2000` | Recommended max tokens |
| `requires_json_output` | Check | `0` | Whether template expects JSON output |

#### Scope & Applicability Rules

Templates can be scoped to specific product types, families, channels, and locales:

| Field | Type | Purpose |
|-------|------|---------|
| `applicable_product_types` | Small Text | Comma-separated product types (empty = all) |
| `applicable_families` | Small Text | Comma-separated product families (empty = all) |
| `applicable_channels` | Small Text | Comma-separated channels (empty = all) |
| `applicable_locales` | Small Text | Comma-separated locales (empty = all) |
| `target_attributes` | Small Text | Attribute codes this template generates values for |

#### Prompt Engineering — System & User Prompts

Templates use **Jinja2 syntax** for dynamic prompt construction:

**System Prompt** (`system_prompt` field, Code type with Jinja mode):
Sets the AI's role and behavioral context. Supports variables:
- `{{ company_name }}` — Customer's company name
- `{{ channel.name }}` — Target channel name
- `{{ channel.type }}` — Target channel type

**User Prompt Template** (`user_prompt_template` field, Code type with Jinja mode, **required**):
The main product data prompt. Available variables:
- `{{ product }}` — Full product object (SKU, name, description, etc.)
- `{{ attributes }}` — Product attribute values
- `{{ channel }}` — Target channel configuration
- `{{ locale }}` — Target locale
- `{{ category }}` — Product category
- `{{ family }}` — Product family
- `{{ existing_values }}` — Current attribute values

**Example — Fashion Description Template:**
```jinja
You are a fashion copywriter for {{ channel.name }}.

Product: {{ product.product_name }}
SKU: {{ product.sku }}
Category: {{ category }}
Brand: {{ product.brand }}
Material: {{ attributes.material }}
Color: {{ attributes.color }}
Season: {{ attributes.season }}

Write a compelling product description (150-300 words) that:
- Highlights key features and materials
- Uses emotional, lifestyle-oriented language
- Includes relevant keywords for {{ channel.name }} SEO
- Matches the brand voice for {{ product.brand }}

{% if existing_values.short_description %}
Current description (improve upon): {{ existing_values.short_description }}
{% endif %}
```

#### Output Configuration

| Field | Type | Default | Options | Purpose |
|-------|------|---------|---------|---------|
| `output_format` | Select | `Plain Text` | Plain Text, JSON, Markdown, HTML | Expected response format |
| `output_schema` | JSON | — | — | JSON schema for structured output validation |
| `post_processing` | Select | `None` | None, Trim Whitespace, Extract JSON, Parse Key-Value, Custom | Post-processing pipeline |
| `post_processing_script` | Code (Python) | — | — | Custom Python function for post-processing |

#### Few-Shot Examples

Templates support **in-context learning** with example inputs and outputs:

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `include_examples` | Check | `1` | Whether to include examples in prompt |
| `max_examples` | Int | `3` | Maximum examples to include |
| `examples` | JSON | — | Array of `{input: ..., output: ...}` objects |

#### Output Validation

| Field | Type | Purpose |
|-------|------|---------|
| `enable_output_validation` | Check | Enable validation of AI responses |
| `validation_rules` | JSON | Array of validation rules `[{field, rule, message}]` |
| `min_output_length` | Int | Minimum character count for valid output |
| `max_output_length` | Int | Maximum character count (truncated if exceeded) |
| `forbidden_patterns` | Small Text | Regex patterns that must NOT appear (one per line) |

#### Usage Statistics (auto-tracked, read-only)

| Field | Type | Purpose |
|-------|------|---------|
| `total_uses` | Int | Number of times template has been used |
| `successful_uses` | Int | Number of successful enrichments |
| `average_confidence` | Percent | Average confidence score of results |
| `last_used_at` | Datetime | When template was last used |
| `average_tokens` | Int | Average tokens consumed per use |

#### Permission Matrix

| Role | Create | Read | Write | Delete |
|------|--------|------|-------|--------|
| System Manager | ✓ | ✓ | ✓ | ✓ |
| PIM Manager | ✓ | ✓ | ✓ | ✓ |
| PIM User | — | ✓ | — | — |

### 10.4 AI Approval Queue

**DocType:** `AI Approval Queue`
**Purpose:** Implements the **human-in-the-loop** review system where AI-generated suggestions are queued for manual approval before being applied to products.

**Naming Rule:** Hash-based (auto-generated)

#### Approval Workflow

```
AI Enrichment Job
       │
       ▼
  AI generates content
       │
       ├──▶ confidence ≥ auto_apply_threshold → "Auto Approved" → Apply to Product
       │
       └──▶ confidence < threshold → "Pending" → Manual Review
                                                      │
                                          ┌───────────┼───────────┐
                                          ▼           ▼           ▼
                                      "Approved"  "Rejected"  "Expired"
                                          │           │
                                          ▼           ▼
                                   Apply to Product   Log for
                                                   model improvement
```

#### Configurable Fields

| Field | Type | Options/Default | Purpose |
|-------|------|----------------|---------|
| `product` | Link → Item (required) | — | Product being enriched |
| `enrichment_type` | Select (required) | `description`, `title`, `keywords`, `translation`, `attributes`, `meta_description`, `bullet_points` | Type of AI content |
| `language` | Link → Language | `en` | Content language |
| `status` | Select (required) | `Pending`, `Approved`, `Rejected`, `Auto Approved`, `Expired` (default: Pending) | Review status |
| `original_content` | Long Text | — | Current product content (for comparison) |
| `suggested_content` | Long Text (required) | — | AI-generated suggestion |
| `rejection_reason` | Small Text | — | Why the content was rejected |
| `notes` | Small Text | — | Reviewer notes |

#### AI Metadata (read-only)

| Field | Type | Purpose |
|-------|------|---------|
| `confidence_score` | Percent | AI confidence in the suggestion |
| `model_used` | Data | AI model that generated the content |
| `tokens_used` | Int | Token consumption for this suggestion |
| `estimated_cost` | Currency (6 decimal precision) | Cost of generating this suggestion |
| `metadata` | Code (JSON) | Additional provider-specific metadata |

#### Auto-Approval Configuration

| Field | Type | Purpose |
|-------|------|---------|
| `auto_approved` | Check (read-only) | Whether this was auto-approved |
| `auto_approval_rule` | Data (read-only) | Which rule triggered auto-approval |
| `approval_threshold` | Percent | Confidence threshold for auto-approval |

#### Permission Matrix

| Role | Create | Read | Write | Delete |
|------|--------|------|-------|--------|
| System Manager | ✓ | ✓ | ✓ | ✓ |
| PIM Manager | — | ✓ | ✓ | — |
| PIM User | — | ✓ | — | — |

> **Note:** PIM Managers can approve/reject items (write access) but cannot create or delete queue entries directly — they are created by the AI Enrichment Job.

### 10.5 AI-Powered Services

#### 10.5.1 AI Enrichment Service

**Module:** `frappe_pim.pim.services.ai_enrichment`

The core enrichment service provides **10 enrichment types** with default prompt templates and provider-agnostic operation:

| Enrichment Type | Enum | Description |
|----------------|------|-------------|
| Short Description | `description_short` | Concise product summary (50–150 words) |
| Long Description | `description_long` | Detailed product description (200–500 words) |
| SEO Title | `seo_title` | Search-optimized product title |
| Bullet Points | `bullet_points` | Feature bullet point extraction |
| Keywords | `keywords` | Keyword and tag suggestions |
| Tags | `tags` | Product tagging |
| Category Suggestion | `category_suggestion` | Automatic category recommendation |
| Attribute Extraction | `attribute_extraction` | Extract attribute values from text/images |
| Image Alt Text | `image_alt_text` | Accessibility alt text generation |
| Meta Description | `meta_description` | SEO meta description |

**Confidence Levels:**

| Level | Threshold | Action |
|-------|-----------|--------|
| High | ≥ 0.80 | Auto-apply if enabled |
| Medium | ≥ 0.60 | Recommended for review |
| Low | ≥ 0.40 | Requires manual review |
| Very Low | < 0.40 | Flagged for re-generation |

#### 10.5.2 AI Categorization Service

**Module:** `frappe_pim.pim.services.ai_categorization`

Automatic product categorization across **10 taxonomy types**:

| Taxonomy | Enum | Use Case |
|----------|------|----------|
| GPC | `gpc` | GS1 Global Product Classification |
| UNSPSC | `unspsc` | UN Standard Products and Services Code |
| Google Product Category | `google_product_category` | Google Merchant Center |
| Amazon Browse Node | `amazon_browse_node` | Amazon marketplace |
| Facebook Category | `facebook_category` | Meta Commerce |
| Trendyol Category | `trendyol_category` | Trendyol marketplace |
| Hepsiburada Category | `hepsiburada_category` | Hepsiburada marketplace |
| N11 Category | `n11_category` | N11 marketplace |
| eBay Category | `ebay_category` | eBay marketplace |
| Custom | `custom` | Customer-defined taxonomy |

**Match Types:**

| Match Type | Description |
|-----------|-------------|
| Exact | Direct string match against taxonomy |
| Semantic | AI semantic understanding of product data |
| Keyword | Keyword-based matching rules |
| Attribute | Attribute value-based mapping |
| Historical | Based on previous categorization patterns |
| Rule-based | Configured categorization rules |
| Fallback | Default category when no match found |

**Confidence Levels for Categories:**

| Level | Threshold |
|-------|-----------|
| Very High | ≥ 0.95 |
| High | ≥ 0.85 |
| Medium | ≥ 0.70 |
| Low | ≥ 0.50 |
| Very Low | < 0.50 |

#### 10.5.3 AI Translation Service

**Module:** `frappe_pim.pim.services.ai_translation`

Multi-language product content translation with **5 provider options** and intelligent optimization:

**Translation Providers:**

| Provider | Best For | Cost |
|----------|---------|------|
| OpenAI (GPT-4) | Creative content, brand voice | Higher |
| Anthropic (Claude) | Technical accuracy, long text | Higher |
| Google Gemini | Balance of quality and cost | Medium |
| Google Translate | Basic translations, high volume | Low |
| DeepL | European languages, formal content | Medium |

**Translatable Content Types (10 types):**

| Content Type | Enum | Notes |
|-------------|------|-------|
| Product Title | `product_title` | SEO-aware translation |
| Short Description | `short_description` | Preserves tone and style |
| Long Description | `long_description` | Full HTML/markdown support |
| Bullet Points | `bullet_points` | Preserves formatting |
| Keywords | `keywords` | Localized keyword research |
| Meta Description | `meta_description` | SEO meta tag optimization |
| SEO Title | `seo_title` | Search-optimized per locale |
| Attribute Value | `attribute_value` | Context-aware value translation |
| Category Name | `category_name` | Taxonomy localization |
| Brand Description | `brand_description` | Brand voice preservation |

**Translation Quality Levels:**

| Quality | Threshold | Action |
|---------|-----------|--------|
| Excellent | ≥ 0.90 | Auto-apply |
| Good | ≥ 0.75 | Recommended for light review |
| Acceptable | ≥ 0.60 | Needs brief review |
| Needs Review | ≥ 0.40 | Requires thorough review |
| Poor | < 0.40 | Reject and re-translate |

**Key Features:**
- **Glossary enforcement** — Domain-specific terminology consistency (4 match types: exact, case-insensitive, whole-word, regex)
- **Translation memory** — Cache previous translations for cost optimization and consistency
- **Quality scoring** — Automatic quality assessment of translations

### 10.6 AI Enrichment API Endpoints

The PIM exposes REST API endpoints for AI operations:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `frappe_pim.api.ai_enrichment.enrich_product` | POST | Real-time or async enrichment for a single product |
| `frappe_pim.api.ai_enrichment.get_enrichment_jobs` | GET | List and filter enrichment jobs |
| `frappe_pim.api.ai_enrichment.get_job_statistics` | GET | Aggregate statistics across all jobs |
| `frappe_pim.api.ai_enrichment.create_enrichment_job` | POST | Programmatically create a new job |
| `frappe_pim.api.ai_enrichment.submit_job` | POST | Submit a draft job for processing |
| `frappe_pim.api.ai_enrichment.get_job_types` | GET | List available enrichment types |
| `frappe_pim.api.ai_enrichment.get_ai_providers` | GET | List available AI providers |

### 10.7 Customer Archetype — AI Configuration Profiles

**Fashion Retailer (High Volume, Creative):**
```
Provider: Anthropic Claude 3.5 Sonnet
Key Templates:
  ├── desc-gen-fashion      → Description Generation (temp: 0.8)
  ├── seo-optimize-fashion  → SEO Optimization (temp: 0.5)
  ├── attr-extract-fashion  → Attribute Extraction (temp: 0.3)
  └── translate-fashion     → Translation (per target locale)

Approval: Auto-apply ≥ 90% confidence, manual review below
Batch Size: 25 products
Selection: By Product Family (Apparel, Footwear, Accessories)
```

**Industrial Supplier (Technical, Regulated):**
```
Provider: Azure OpenAI GPT-4 (data residency)
Key Templates:
  ├── desc-gen-technical    → Description Generation (temp: 0.3)
  ├── attr-extract-spec     → Attribute Extraction (temp: 0.2)
  ├── classify-unspsc       → Classification (UNSPSC taxonomy)
  └── quality-check-safety  → Quality Check (safety data validation)

Approval: All suggestions require manual review (require_approval: ✓)
Batch Size: 10 products (higher accuracy per product)
Selection: By Product Category (Raw Material, Component)
```

**Food Manufacturer (Compliance, Multi-Language):**
```
Provider: Anthropic Claude 3 Opus (accuracy)
Key Templates:
  ├── desc-gen-food         → Description Generation (temp: 0.4)
  ├── classify-gpc          → Classification (GPC taxonomy)
  ├── translate-regulatory  → Translation (with glossary enforcement)
  └── attr-extract-nutrition → Attribute Extraction (nutrition data)

Approval: Auto-apply ≥ 95% for descriptions, all translations manual
Batch Size: 15 products
Translation Provider: DeepL for EU languages, Anthropic for others
Glossary: Allergen terms, nutritional vocabulary, regulatory terminology
```

### 10.8 Onboarding Checklist — AI & Enrichment

```
Phase 1 — Provider Setup:
  □ Decision: Enable AI enrichment? (enable_ai_enrichment)
  □ Select primary AI provider (ai_provider)
  □ Obtain and configure API key (ai_api_key) — encrypted storage
  □ Select model (ai_model) based on quality/cost/speed needs
  □ Test connection via PIM Settings → test_ai_connection()

Phase 2 — Approval Workflow:
  □ Decision: Require human approval? (ai_require_approval)
  □ If yes: Set auto_apply_threshold (recommended: 90–95%)
  □ Configure notification recipients for completed jobs
  □ Assign PIM Managers as approval reviewers

Phase 3 — Prompt Templates:
  □ Create templates for each enrichment type needed
  □ Configure scope rules (product types, families, channels)
  □ Add few-shot examples for industry-specific content
  □ Set output validation rules (min/max length, forbidden patterns)
  □ Test templates with small product batches

Phase 4 — Categorization Setup (if multi-channel):
  □ Enable auto-categorization for target taxonomies
  □ Import or configure taxonomy hierarchies
  □ Test with sample products across each channel
  □ Review confidence scores and adjust thresholds

Phase 5 — Translation Setup (if multi-language):
  □ Select translation provider(s) per language pair
  □ Build domain glossary for consistent terminology
  □ Create translation templates per content type
  □ Seed translation memory with existing translations
  □ Run pilot translation batch and review quality scores
```

---

## 11. Media & Digital Assets

### Overview

The PIM provides a **media management system** for product images, videos, documents, and other digital assets. Media is managed through the **Product Media child table** attached to both Product Master and Product Variant DocTypes, with a **Pillow-based image processing pipeline** for automatic optimization, thumbnail generation, and WebP conversion.

> **Note:** The current implementation uses Frappe's built-in file management system for storage (local filesystem at `/files/` and `/private/files/`). Dedicated Digital Asset, Asset Rendition, S3 storage, and CDN integration DocTypes are part of the planned architecture but not yet implemented. This section documents the **current** media capabilities and the **planned** extension points.

**Architecture:**

```
┌──────────────────────────────────────────────────────────────────┐
│                     Product Media System                          │
│                                                                    │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────────────┐ │
│  │ Product      │───▶│ Product Media │───▶│ media.py             │ │
│  │ Master       │    │ (child table) │    │ Image Processing     │ │
│  └─────────────┘    └──────────────┘    │                      │ │
│  ┌─────────────┐           │            │ ┌──────────────────┐ │ │
│  │ Product      │───▶ (same child      │ │ process_product_ │ │ │
│  │ Variant      │    table)            │ │ image()          │ │ │
│  └─────────────┘                       │ ├──────────────────┤ │ │
│                                         │ │ generate_        │ │ │
│                                         │ │ thumbnail()      │ │ │
│                                         │ ├──────────────────┤ │ │
│                                         │ │ convert_to_      │ │ │
│                                         │ │ webp()           │ │ │
│                                         │ ├──────────────────┤ │ │
│                                         │ │ optimize_image() │ │ │
│                                         │ └──────────────────┘ │ │
│                                         └──────────────────────┘ │
│                                                                    │
│  Storage: Frappe File System                                       │
│  ├── /files/ (public)                                              │
│  └── /private/files/ (private)                                     │
└──────────────────────────────────────────────────────────────────┘
```

### 11.1 Product Media Child Table

**DocType:** `Product Media`
**Purpose:** Child table linking media files to Product Master and Product Variant records. Supports per-variant, per-locale, and per-channel media assignment.

**Parent DocTypes:** Product Master (`media` table field), Product Variant (`media` table field)
**Grid Configuration:** Editable grid (`editable_grid: 1`) — inline editing in parent form

#### Field Reference

| Field | Type | Default | Required | In List | Purpose | Per-Customer Impact |
|-------|------|---------|----------|---------|---------|-------------------|
| `file` | Attach | — | ✓ | ✓ (3 cols) | File attachment (image, video, document) | All media files uploaded here |
| `media_type` | Select | `Gallery` | — | ✓ (2 cols) | Media classification | Determines display logic |
| `title` | Data | — | — | ✓ (2 cols) | Media title | Used in alt attributes and CMS |
| `alt_text` | Data | — | — | — | Alternative text for accessibility | SEO and accessibility compliance |
| `sort_order` | Int | `0` | — | ✓ (1 col) | Display ordering | Controls image gallery sequence |
| `apply_to_variant` | Link → Product Variant | — | — | — | Variant-specific media | Leave empty for all variants |
| `locale` | Link → Language | — | — | — | Locale-specific media | Leave empty for all locales |
| `channel` | Link → Channel | — | — | — | Channel-specific media | Leave empty for all channels |

#### Media Types (7 options)

| Media Type | Value | Use Case | Channel Relevance |
|-----------|-------|----------|------------------|
| **Main Image** | `Main Image` | Primary product photo | Required by all channels |
| **Gallery** | `Gallery` | Additional product photos | Most channels use 5–8 gallery images |
| **Thumbnail** | `Thumbnail` | Small preview image | Auto-generated by processing pipeline |
| **360 View** | `360 View` | 360-degree product view | Supported by Amazon, Shopify |
| **Video** | `Video` | Product video | Required for some Amazon categories |
| **Document** | `Document` | PDF datasheets, manuals | B2B channels, technical products |
| **Other** | `Other` | Miscellaneous media | Catch-all classification |

#### Per-Variant, Per-Locale, Per-Channel Media Strategy

The three optional Link fields on Product Media enable sophisticated media strategies:

**Per-Variant Media:**
```
Product: T-Shirt Basic (TSH-001)
├── Media: front-photo.jpg         → apply_to_variant: (empty) = all variants
├── Media: back-photo.jpg          → apply_to_variant: (empty) = all variants
├── Media: red-swatch.jpg          → apply_to_variant: TSH-001-RED
├── Media: blue-swatch.jpg         → apply_to_variant: TSH-001-BLU
└── Media: green-swatch.jpg        → apply_to_variant: TSH-001-GRN
```

**Per-Locale Media:**
```
Product: Organic Honey (HON-001)
├── Media: honey-jar-en.jpg        → locale: en (English packaging photo)
├── Media: honey-jar-tr.jpg        → locale: tr (Turkish packaging photo)
├── Media: honey-jar-de.jpg        → locale: de (German packaging photo)
└── Media: honey-nutrition.jpg     → locale: (empty) = all locales
```

**Per-Channel Media:**
```
Product: Running Shoe X1 (SHO-001)
├── Media: shoe-main-1500x1500.jpg   → channel: Amazon (meets 1500px requirement)
├── Media: shoe-main-1000x1000.jpg   → channel: Shopify (optimized for web)
├── Media: shoe-lifestyle.jpg        → channel: Trendyol (lifestyle shot preferred)
└── Media: shoe-technical-spec.jpg   → channel: (empty) = all channels
```

### 11.2 Product Master & Variant Media Fields

**Product Master** has the following media-related fields:

| Field | Type | Purpose |
|-------|------|---------|
| `main_image` | Attach Image | Primary product image (quick access) |
| `media` | Table → Product Media | Full media gallery (child table) |

**Product Variant** has the following media-related fields:

| Field | Type | Purpose |
|-------|------|---------|
| `image` | Attach Image | Primary variant image |
| `media` | Table → Product Media | Variant-specific media gallery |

### 11.3 Image Processing Pipeline

**Module:** `frappe_pim.pim.utils.media`

The media utility provides an automated image processing pipeline using **Pillow (PIL)** for:
1. Image resizing and optimization
2. Thumbnail generation (3 preset sizes)
3. WebP format conversion
4. EXIF orientation correction
5. Background job processing for large files

#### Processing Configuration Constants

| Constant | Value | Purpose | Customization |
|----------|-------|---------|---------------|
| `DEFAULT_THUMBNAIL_SIZES` | `{"small": (150, 150), "medium": (300, 300), "large": (600, 600)}` | Preset thumbnail dimensions | Modify for channel-specific sizes |
| `DEFAULT_QUALITY` | `85` | JPEG/PNG compression quality | Lower = smaller files, less quality |
| `DEFAULT_WEBP_QUALITY` | `80` | WebP compression quality | 80 typically provides 25–35% savings |
| `MAX_DIMENSION` | `2048` | Maximum width/height after resize | Increase for high-res catalogs |
| `LARGE_FILE_THRESHOLD` | `10 * 1024 * 1024` (10 MB) | Threshold for background processing | Files above this are processed async |

#### Main Processing Functions

**`process_product_image(file_path, product_name, ...)`**
The primary entry point for image processing. Orchestrates the full pipeline:

| Parameter | Type | Default | Purpose |
|-----------|------|---------|---------|
| `file_path` | str | (required) | Path or Frappe file URL |
| `product_name` | str | None | For logging and file naming |
| `max_dimension` | int | `2048` | Max width/height |
| `quality` | int | `85` | Output quality (1–100) |
| `generate_thumbnails` | bool | `True` | Create thumbnail variants |
| `convert_webp` | bool | `True` | Create WebP version |
| `async_processing` | bool | `False` | Force background job |

**Returns:**
```python
{
    "success": True,
    "original_path": "/files/product-image.jpg",
    "processed_path": "/files/product-image_processed.jpg",
    "thumbnails": {
        "small": "/files/product-image_small.jpg",    # 150x150
        "medium": "/files/product-image_medium.jpg",   # 300x300
        "large": "/files/product-image_large.jpg"      # 600x600
    },
    "webp_path": "/files/product-image.webp",
    "error": None
}
```

**`generate_thumbnail(source_path, size, quality, output_path)`**
Generate individual thumbnails with preset or custom dimensions:
- Preset names: `"small"` (150x150), `"medium"` (300x300), `"large"` (600x600)
- Custom dimensions: `(200, 200)`, `(800, 600)`, etc.
- Preserves aspect ratio using `Image.Resampling.LANCZOS`

**`convert_to_webp(source_path, quality, output_path, lossless)`**
Convert images to WebP format for web optimization:
- Lossy mode: `quality` parameter (1–100), method 6 (best compression)
- Lossless mode: `lossless=True` for pixel-perfect conversion
- Supports transparency (RGBA → WebP)

**`get_image_info(file_path)`**
Extract image metadata without loading full image:
- Returns: `{width, height, format, mode, file_size, file_size_human}`

**`optimize_image(source_path, output_path, max_dimension, quality)`**
Optimize images for web delivery — resize, compress, strip metadata.

#### Supported Image Formats

| Format | Input | Output | WebP Convert | Notes |
|--------|-------|--------|-------------|-------|
| JPEG (.jpg, .jpeg) | ✓ | ✓ | ✓ | Progressive JPEG output, quality-based compression |
| PNG (.png) | ✓ | ✓ | ✓ | Optimized compression, no quality parameter |
| GIF (.gif) | ✓ | ✓ | ✓ | Static frames only |
| WebP (.webp) | ✓ | ✓ | — | Already in target format |
| BMP (.bmp) | ✓ | ✓ | ✓ | Converted to compressed format |
| TIFF (.tiff, .tif) | ✓ | ✓ | ✓ | Common in print/industrial workflows |

#### Background Processing

Files exceeding `LARGE_FILE_THRESHOLD` (10 MB) are automatically enqueued as Frappe background jobs:

```python
frappe.enqueue(
    "frappe_pim.pim.utils.media.process_product_image",
    queue="long",
    timeout=600,       # 10-minute timeout
    async_processing=True
)
```

This prevents request timeout for large catalog images and allows processing to continue in the background.

#### Upload Hook Integration

The function `process_product_media_on_upload(doc, method)` can be connected to Frappe `doc_events` for automatic processing when media is uploaded:

```python
# hooks.py configuration example
doc_events = {
    "File": {
        "after_insert": "frappe_pim.pim.utils.media.process_product_media_on_upload"
    }
}
```

When triggered, it:
1. Checks if the uploaded file is an image (by extension)
2. Runs `process_product_image()` with default settings
3. Stores thumbnail paths in `doc.thumbnail_small`, `doc.thumbnail_medium`, `doc.thumbnail_large`
4. Stores WebP path in `doc.webp_url`

### 11.4 Media Maintenance — Orphan Cleanup

**Module:** `frappe_pim.pim.tasks.scheduled`
**Function:** `cleanup_orphan_media()`
**Schedule:** Daily (via Frappe scheduler)

This scheduled task identifies and deletes Product Media records orphaned from deleted Product Masters:
- Uses `LEFT JOIN` query for efficient detection
- Processes in batches (max 1000 records per run)
- Commits after each deletion for transactional safety
- Logs errors for failed deletions

### 11.5 Media Requirements Per Channel

Different sales channels have varying image requirements. While the PIM does not enforce these automatically in the current implementation, the following reference guides channel-specific media configuration:

| Channel | Min Image Size | Recommended Size | Max File Size | Required Images | Preferred Format |
|---------|---------------|-----------------|--------------|----------------|-----------------|
| **Amazon** | 1000×1000 px | 2000×2000 px | 10 MB | 1 main + 6 gallery | JPEG, PNG |
| **Shopify** | 800×800 px | 2048×2048 px | 20 MB | 1 main + unlimited | JPEG, PNG, GIF |
| **WooCommerce** | 600×600 px | 1200×1200 px | Varies | 1 main + gallery | JPEG, PNG, WebP |
| **Google Merchant** | 100×100 px | 800×800 px | 16 MB | 1 required | JPEG, PNG, GIF, WebP, BMP, TIFF |
| **Trendyol** | 500×500 px | 1200×1200 px | 5 MB | 1 main + 3 gallery | JPEG, PNG |
| **Hepsiburada** | 500×500 px | 1000×1000 px | 5 MB | 1 main + gallery | JPEG, PNG |
| **N11** | 500×500 px | 1000×1000 px | 5 MB | 1 main + gallery | JPEG, PNG |
| **eBay** | 500×500 px | 1600×1600 px | 12 MB | 1 main + 11 gallery | JPEG, PNG |
| **Etsy** | 2000×2000 px | 2700×2025 px | 20 MB | 1 main + 9 gallery | JPEG, PNG, GIF |
| **Walmart** | 1000×1000 px | 2000×2000 px | 5 MB | 1 main + 3 gallery | JPEG, PNG |
| **Meta Commerce** | 500×500 px | 1024×1024 px | 8 MB | 1 required | JPEG, PNG |
| **TikTok Shop** | 600×600 px | 1200×1200 px | 5 MB | 1 main + 8 gallery | JPEG, PNG |

### 11.6 Planned Extensions (Not Yet Implemented)

The following capabilities are part of the planned architecture but not yet implemented:

| Feature | Description | Planned DocType/Module |
|---------|-------------|----------------------|
| **Digital Asset** | Standalone asset management with metadata, tagging, usage tracking | `Digital Asset` DocType |
| **Asset Rendition** | Named variants of assets (e.g., "web-optimized", "print-ready", "mobile") | `Asset Rendition` DocType |
| **S3 Storage Backend** | Amazon S3 / S3-compatible object storage integration | `frappe_pim.pim.services.s3_storage` |
| **CDN Configuration** | CloudFront, Cloudflare, or custom CDN URL generation | PIM Settings → CDN configuration |
| **Image Variant Generation** | Automated per-channel image variant creation (resize, crop, overlay) | `frappe_pim.pim.services.image_variants` |
| **Video Processing** | Video thumbnail extraction, transcoding, streaming URLs | Future service module |
| **DAM Integration** | Integration with external DAM systems (Bynder, Cloudinary, etc.) | Future API module |

### 11.7 Customer Archetype — Media Configuration

**Fashion Retailer:**
```
Media Strategy:
  ├── Main Image: White background, 2000x2000 px minimum
  ├── Gallery: 6-8 images (front, back, detail, on-model, flat lay, swatch)
  ├── 360 View: Required for footwear and premium items
  ├── Video: Optional product videos for hero items
  ├── Per-Variant: Color-specific images (swatch + on-model)
  ├── Per-Channel: Amazon (1500x1500), Shopify (2048x2048), Trendyol (1200x1200)
  └── WebP: Enabled for all e-commerce channels

Processing Settings:
  ├── max_dimension: 2048
  ├── quality: 90 (high quality for fashion)
  ├── generate_thumbnails: ✓ (small for catalog, medium for PDP, large for zoom)
  └── convert_webp: ✓
```

**Industrial Supplier:**
```
Media Strategy:
  ├── Main Image: Product photo on white or contextual background
  ├── Gallery: 2-4 images (product, dimensions, technical detail)
  ├── Document: Safety datasheets (SDS), installation manuals, spec sheets
  ├── Per-Variant: Configuration-specific images only
  ├── Per-Channel: Standard sizing for B2B portals
  └── WebP: Optional (B2B users often use older browsers)

Processing Settings:
  ├── max_dimension: 1600
  ├── quality: 85 (standard quality)
  ├── generate_thumbnails: ✓ (medium for catalog listing)
  └── convert_webp: Optional
```

**Food Manufacturer:**
```
Media Strategy:
  ├── Main Image: Product packaging photo (localized per market)
  ├── Gallery: 3-5 images (front, back, nutrition label, serving suggestion)
  ├── Document: Allergen declarations, certification documents
  ├── Per-Locale: Market-specific packaging photos (different languages on label)
  ├── Per-Channel: Marketplace-compliant images
  └── WebP: Enabled for all channels

Processing Settings:
  ├── max_dimension: 2048
  ├── quality: 90 (packaging detail quality)
  ├── generate_thumbnails: ✓ (all sizes)
  └── convert_webp: ✓
```

### 11.8 Onboarding Checklist — Media & Digital Assets

```
Phase 1 — Media Standards Definition:
  □ Define image size requirements per channel (see Section 11.5)
  □ Define media types needed (Main Image, Gallery, Video, Document, 360)
  □ Decide on WebP conversion policy
  □ Set maximum file size limits

Phase 2 — Processing Configuration:
  □ Verify Pillow is installed (pip install Pillow)
  □ Install libwebp-dev system package for WebP support
  □ Configure DEFAULT_THUMBNAIL_SIZES in media.py if custom sizes needed
  □ Set MAX_DIMENSION based on highest channel requirement
  □ Configure LARGE_FILE_THRESHOLD for background processing

Phase 3 — Media Strategy per Product Family:
  □ Document minimum image count per Product Family
  □ Define per-variant media requirements (color swatches, etc.)
  □ Define per-locale media requirements (localized packaging, etc.)
  □ Define per-channel media requirements (size, format)

Phase 4 — Upload and Processing:
  □ Upload product images via Product Master form (media child table)
  □ Verify automatic processing (thumbnails, WebP) works correctly
  □ Assign media types and sort orders
  □ Set variant, locale, and channel assignments where needed

Phase 5 — Validation and Maintenance:
  □ Verify orphan media cleanup task is scheduled (daily)
  □ Check that all products have required media for target channels
  □ Review completeness scores for media dimension
  □ Monitor disk space usage for media files
```

---

## 12. Export & Integration

### Overview

The PIM provides a comprehensive **data export and integration framework** that enables product data to flow out of the system into downstream channels, partners, trading platforms, and ERPs. The export system is built around the **Export Profile DocType** — a reusable, configurable export definition that controls format, filtering, scheduling, and output options. The PIM supports both **generic formats** (CSV, JSON, XML, Excel) and **industry-standard B2B interchange formats** (BMEcat 2005/1.2), with planned extensions for cXML, EDIFACT, GS1 XML, and UBL.

> **Note:** The current implementation includes a fully functional Export Profile DocType, BMEcat 2005 export module with lxml-based XML generation, and API endpoints for CSV, JSON, XML, and Excel export. Import Configuration, Webhook Configuration, PIM Notification Rule, and additional industry-standard formats (cXML, EDIFACT, GS1 XML, UBL) are part of the planned architecture. This section documents **current** capabilities and **planned** extension points.

**Architecture:**

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                       PIM Export & Integration System                          │
│                                                                                │
│  ┌──────────────────┐   ┌────────────────┐   ┌────────────────────────────┐ │
│  │  Export Profile   │──▶│ Export API      │──▶│  Output Formats            │ │
│  │  (Configuration)  │   │ (api/export.py) │   │                            │ │
│  │  ┌──────────────┐│   │ ┌────────────┐ │   │  ┌──────────────────────┐  │ │
│  │  │ Format        ││   │ │export_bmecat│ │   │  │ BMEcat 2005 / 1.2   │  │ │
│  │  │ Filter        ││   │ │export_csv   │ │   │  │ CSV                  │  │ │
│  │  │ Schedule      ││   │ │export_json  │ │   │  │ JSON                 │  │ │
│  │  │ BMEcat Config ││   │ │generate_feed│ │   │  │ XML (Generic)        │  │ │
│  │  │ Output Config ││   │ └────────────┘ │   │  │ Excel (XLSX)         │  │ │
│  │  └──────────────┘│   └────────────────┘   │  │ ─ ─ ─ ─ ─ ─ ─ ─ ─   │  │ │
│  └──────────────────┘           │             │  │ cXML    (planned)     │  │ │
│            │                    │             │  │ EDIFACT (planned)     │  │ │
│            ▼                    ▼             │  │ GS1 XML (planned)     │  │ │
│  ┌──────────────────┐   ┌────────────────┐   │  │ UBL     (planned)     │  │ │
│  │  Scheduler        │   │ Background Job │   │  └──────────────────────┘  │ │
│  │  (daily cron)     │──▶│ Queue (long)   │   └────────────────────────────┘ │
│  │  generate_        │   │ timeout: 3600s │                                   │
│  │  scheduled_feeds  │   └────────────────┘                                   │
│  └──────────────────┘                                                         │
│                                                                                │
│  ┌──────────────────────────────────────────────────────────────────────────┐ │
│  │  Planned Extensions                                                       │ │
│  │  ┌───────────────────┐ ┌──────────────────┐ ┌────────────────────────┐  │ │
│  │  │ Import             │ │ Webhook           │ │ PIM Notification Rule  │  │ │
│  │  │ Configuration      │ │ Configuration     │ │ (event-based alerts)   │  │ │
│  │  │ (inbound feeds)    │ │ (outbound events) │ │                        │  │ │
│  │  └───────────────────┘ └──────────────────┘ └────────────────────────┘  │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 12.1 Export Profile DocType

**DocType:** `Export Profile`
**Module:** PIM
**Naming Rule:** `field:profile_code` (named by the `profile_code` field)
**Track Changes:** Yes

The Export Profile is the **central configuration entity** for data exports. Each profile defines a complete export specification including output format, product filtering criteria, format-specific options, scheduling, and output settings. Profiles are linked to Channels for channel-specific export feeds.

#### Configurable Fields

**Basic Settings:**

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `profile_name` | Data (required, translatable) | — | Display name | Customer-specific naming for team reference |
| `profile_code` | Data (required, unique) | — | Unique slug identifier (auto-generated from name) | Used in API calls, filenames, cache keys |
| `export_format` | Select (required) | `CSV` | Output format: `BMEcat 2005`, `BMEcat 1.2`, `CSV`, `JSON`, `XML`, `Excel` | Determines downstream system compatibility |
| `enabled` | Check | `1` | Enable/disable this profile | Controls availability for manual and scheduled runs |
| `sort_order` | Int | `0` | Display order in profile listings | UI organization |

**Channel Settings:**

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `channel` | Link → Channel | — | Distribution channel for this export | Ties export to a specific marketplace or partner |
| `export_language` | Link → Language | — | Language for exported product data | Determines translation locale used in export |
| `export_currency` | Link → Currency | — | Currency for price exports | Must match target market pricing |
| `include_prices` | Check | `1` | Include pricing information | Some channels require prices, others don't |

**Product Filter:**

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `product_family` | Link → Product Family | — | Restrict export to specific family | Enables family-specific export feeds |
| `status_filter` | Select | — | Filter by status: `Draft`, `Active`, `Inactive`, `Archived` | Controls which products go to downstream |
| `completeness_threshold` | Percent | `0` | Minimum completeness score (0–100) | Quality gate — only export "ready" products |
| `include_variants` | Check | `1` | Include Product Variants in export | Business decision: master-only vs. SKU-level feeds |
| `include_media` | Check | `1` | Include product image/media URLs | Some formats don't need media references |

**Format Options (CSV-specific):**

| Field | Type | Default | Depends On | Purpose |
|-------|------|---------|-----------|---------|
| `csv_delimiter` | Select | `Comma (,)` | `export_format === 'CSV'` | Field delimiter: `Comma (,)`, `Semicolon (;)`, `Tab`, `Pipe (\|)` |
| `csv_encoding` | Select | `UTF-8` | `export_format === 'CSV'` | Character encoding: `UTF-8`, `UTF-8-BOM`, `ISO-8859-1`, `Windows-1252` |

**Format Options (XML/JSON-specific):**

| Field | Type | Default | Depends On | Purpose |
|-------|------|---------|-----------|---------|
| `xml_root_element` | Data | `products` | XML or BMEcat formats | Root element name for XML exports |
| `pretty_print` | Check | `1` | XML, JSON, or BMEcat formats | Format output with indentation for readability |

**BMEcat Settings (conditional — shown only for BMEcat formats):**

| Field | Type | Default | Depends On | Purpose |
|-------|------|---------|-----------|---------|
| `bmecat_supplier_id` | Data | — | BMEcat formats | `SUPPLIER_ID` element in BMEcat catalog (required for BMEcat) |
| `bmecat_supplier_name` | Data | — | BMEcat formats | `SUPPLIER_NAME` element in BMEcat catalog (required for BMEcat) |
| `bmecat_catalog_id` | Data | — | BMEcat formats | `CATALOG_ID` element in BMEcat catalog |
| `bmecat_catalog_version` | Data | `1.0` | BMEcat formats | `CATALOG_VERSION` element in BMEcat catalog |

**Scheduling:**

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `is_scheduled` | Check | `0` | Enable automatic scheduled exports | Automates recurring export tasks |
| `schedule_frequency` | Select | `Daily` | Frequency: `Daily`, `Weekly`, `Monthly` | Controls export cadence |
| `schedule_time` | Time | — | Time of day to run (server time) | Schedule to avoid peak hours |
| `last_export` | Datetime (read-only) | — | Timestamp of last export run | Monitoring / auditing |

**Output Settings:**

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `output_filename` | Data | `{profile_code}_{date}.{ext}` | Filename pattern with placeholders: `{date}`, `{time}`, `{profile}` | Customizable naming for file management |
| `compress_output` | Check | `0` | Compress output as ZIP archive | Reduces file size for large catalogs |
| `upload_to_channel` | Check | `0` | Auto-upload to linked channel (requires channel link) | Automates delivery to marketplace |
| `last_file` | Attach (read-only) | — | Most recent exported file | Quick download access |

**Status (read-only):**

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `export_status` | Select | `Never Run` | Status: `Never Run`, `Running`, `Completed`, `Failed` |
| `last_product_count` | Int | — | Number of products in last export |
| `error_message` | Small Text | — | Error details if last export failed |

**Permissions:**

| Role | Read | Write | Create | Delete | Export | Import |
|------|------|-------|--------|--------|--------|--------|
| System Manager | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PIM Manager | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PIM User | ✓ | — | — | — | — | — |

**Controller Validations (export_profile.py):**

The Export Profile controller enforces the following validation rules:
- **Profile Code** must be a URL-safe slug: lowercase, starts with a letter, contains only `a-z`, `0-9`, `_`, `-`
- **BMEcat Settings** validation: `bmecat_supplier_id` and `bmecat_supplier_name` are required when export format is BMEcat 2005 or BMEcat 1.2
- **Schedule Settings** validation: `schedule_time` is required when `is_scheduled` is enabled
- **Completeness Threshold** must be between 0 and 100
- Auto-generates `output_filename` if not provided (format: `{profile_code}_{date}.{ext}`)
- Cache invalidation on update (`pim:export_profile:{name}` and `pim:all_export_profiles`)

**When to Configure:** Phase 3 of onboarding — after channels and product families are set up
**Who Configures:** PIM Manager
**Business Impact:** Controls how product data reaches downstream systems, marketplaces, and partners

### 12.2 Export Formats

The PIM supports 6 export formats organized into **Generic** and **Industry Standard** categories:

#### 12.2.1 Generic Formats

| Format | Extension | Status | Use Case |
|--------|-----------|--------|----------|
| **CSV** | `.csv` | ✅ Implemented | Spreadsheet import, ERP feeds, simple data exchange |
| **JSON** | `.json` | ✅ Implemented | API integration, web applications, modern data exchange |
| **XML** | `.xml` | ✅ Implemented | Generic XML feeds, custom integrations |
| **Excel** | `.xlsx` | ✅ Implemented (via Export Profile format selection) | Business user review, manual data exchange |

**CSV Export Features:**
- Configurable delimiter (comma, semicolon, tab, pipe)
- Configurable encoding (UTF-8, UTF-8-BOM, ISO-8859-1, Windows-1252)
- Optional header row
- Product attribute flattening (EAV values resolved to columns)
- Async background job support for large catalogs

**JSON Export Features:**
- Metadata envelope with generation timestamp, product count, format version
- Nested product attributes as key-value dictionaries
- Media references as structured array
- Pretty-print formatting option
- Async background job support

**XML Export Features:**
- Configurable root element name
- Product attributes as child elements
- Pretty-print formatting option
- lxml-based generation (requires `lxml` package)

#### 12.2.2 Industry Standard Formats

| Format | Extension | Status | Use Case |
|--------|-----------|--------|----------|
| **BMEcat 2005** | `.xml` | ✅ Implemented | B2B electronic product catalogs (German/EU standard) |
| **BMEcat 1.2** | `.xml` | ✅ Implemented (via profile format selection) | Legacy BMEcat compatibility |
| **cXML** | `.xml` | 🔲 Planned | Ariba Network procurement integration |
| **EDIFACT** | `.edi` | 🔲 Planned | UN/EDIFACT electronic data interchange |
| **GS1 XML** | `.xml` | 🔲 Planned | GS1 Global Data Synchronisation Network |
| **UBL** | `.xml` | 🔲 Planned | OASIS Universal Business Language |

#### 12.2.3 BMEcat Export (Detailed)

BMEcat is a **German standard for electronic product data exchange** widely used in B2B e-commerce. The PIM includes a fully functional BMEcat 2005 export module (`pim/export/bmecat.py`) with the following features:

**BMEcat XML Structure:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<BMECAT xmlns="http://www.bmecat.org/bmecat/2005"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        version="2005">
  <HEADER>
    <GENERATOR_INFO>Frappe PIM BMEcat Exporter</GENERATOR_INFO>
    <CATALOG>
      <LANGUAGE>deu</LANGUAGE>
      <CATALOG_ID>CATALOG001</CATALOG_ID>
      <CATALOG_VERSION>1.0</CATALOG_VERSION>
      <CATALOG_NAME>Product Catalog CATALOG001</CATALOG_NAME>
      <GENERATION_DATE>2026-02-27T14:30:00</GENERATION_DATE>
      <TERRITORY>DE</TERRITORY>
      <CURRENCY>EUR</CURRENCY>
    </CATALOG>
    <SUPPLIER>
      <SUPPLIER_ID>SUPPLIER001</SUPPLIER_ID>
      <SUPPLIER_NAME>Default Supplier</SUPPLIER_NAME>
    </SUPPLIER>
  </HEADER>
  <T_NEW_CATALOG>
    <ARTICLE mode="new">
      <SUPPLIER_AID>SKU-001</SUPPLIER_AID>
      <ARTICLE_DETAILS>
        <DESCRIPTION_SHORT>Product Name</DESCRIPTION_SHORT>
        <DESCRIPTION_LONG>Full description...</DESCRIPTION_LONG>
        <EAN>4006381333931</EAN>
        <MANUFACTURER_AID>MPN-001</MANUFACTURER_AID>
      </ARTICLE_DETAILS>
      <ARTICLE_FEATURES>
        <FEATURE>
          <FNAME>Weight</FNAME>
          <FVALUE>2.5</FVALUE>
          <FUNIT>kg</FUNIT>
        </FEATURE>
      </ARTICLE_FEATURES>
      <ARTICLE_ORDER_DETAILS>
        <ORDER_UNIT>C62</ORDER_UNIT>
        <CONTENT_UNIT>C62</CONTENT_UNIT>
        <NO_CU_PER_OU>1</NO_CU_PER_OU>
        <QUANTITY_MIN>1</QUANTITY_MIN>
      </ARTICLE_ORDER_DETAILS>
      <ARTICLE_PRICE_DETAILS>
        <ARTICLE_PRICE price_type="net_list">
          <PRICE_AMOUNT>99.95</PRICE_AMOUNT>
          <PRICE_CURRENCY>EUR</PRICE_CURRENCY>
        </ARTICLE_PRICE>
      </ARTICLE_PRICE_DETAILS>
      <MIME_INFO>
        <MIME>
          <MIME_TYPE>image/jpeg</MIME_TYPE>
          <MIME_SOURCE>https://site.com/image.jpg</MIME_SOURCE>
          <MIME_PURPOSE>normal</MIME_PURPOSE>
          <MIME_ORDER>1</MIME_ORDER>
        </MIME>
      </MIME_INFO>
    </ARTICLE>
  </T_NEW_CATALOG>
</BMECAT>
```

**BMEcat Export Capabilities:**
- **Transaction type:** `T_NEW_CATALOG` (full catalog export)
- **Article details:** Description short/long, EAN/GTIN, manufacturer article ID
- **Features/Attributes:** All PIM Attribute values mapped to `FEATURE` elements with name, value, and unit
- **Order details:** Order unit (defaults to C62 = piece per UN/CEFACT), content unit, minimum order quantity
- **Price details:** Net list price with currency, tax rate, price factor, and lower bound
- **Media/MIME:** Primary image and additional media from Product Media child table, with MIME type detection
- **Multi-language:** Language mapped from Frappe Language to ISO 639-2 codes (12 language mappings)
- **Validation:** Built-in `validate_bmecat_xml()` function for structural validation
- **Article count:** `get_article_count()` utility for post-export verification

**ISO 639-2 Language Mapping (BMEcat):**

| Frappe Code | ISO 639-2 | Language |
|-------------|-----------|----------|
| `en` | `eng` | English |
| `de` | `deu` | German |
| `fr` | `fra` | French |
| `es` | `spa` | Spanish |
| `it` | `ita` | Italian |
| `nl` | `nld` | Dutch |
| `pl` | `pol` | Polish |
| `tr` | `tur` | Turkish |
| `ru` | `rus` | Russian |
| `zh` | `zho` | Chinese |
| `ja` | `jpn` | Japanese |
| `ko` | `kor` | Korean |

### 12.3 Export API Endpoints

The export system provides a rich set of API endpoints via `frappe_pim.pim.api.export` and `frappe_pim.pim.doctype.export_profile.export_profile`:

#### API Reference

| Endpoint | Method | Parameters | Description |
|----------|--------|-----------|-------------|
| `export_bmecat` | POST | `profile_name`, `products`, `supplier_id`, `supplier_name`, `catalog_id`, `catalog_version`, `language`, `territory`, `currency`, `include_prices`, `include_media`, `include_variants`, `async_export` | Export to BMEcat 2005 XML |
| `export_csv` | POST | `profile_name`, `products`, `product_family`, `status_filter`, `completeness_threshold`, `delimiter`, `include_header`, `async_export` | Export to CSV |
| `export_json` | POST | `profile_name`, `products`, `product_family`, `status_filter`, `completeness_threshold`, `include_attributes`, `include_media`, `pretty_print`, `async_export` | Export to JSON |
| `run_export` | POST | `profile_name`, `async_mode` | Trigger export for any profile (auto-detects format) |
| `generate_feed` | POST | `profile` | Background job handler for scheduled/queued exports |
| `get_export_status` | GET | `profile_name` | Get current export status |
| `download_export` | GET | `profile_name` or `file_url` | Download latest export file |
| `get_export_profiles` | GET | `enabled_only`, `format_filter` | List all export profiles |
| `preview_export_data` | GET | `profile_name`, `limit` | Preview products that would be exported |
| `get_export_history` | GET | `profile_name`, `limit` | Get export history log |
| `get_export_formats` | GET | — | Get available format definitions with categories |
| `get_profiles_by_channel` | GET | `channel` | Get profiles linked to a specific channel |
| `get_scheduled_profiles` | GET | — | Get all enabled scheduled profiles |
| `bulk_enable_profiles` | POST | `profiles`, `enable` | Bulk enable/disable multiple profiles |

#### API Usage Examples

**Run a BMEcat export using a profile:**
```python
import frappe

# Using Export Profile
result = frappe.call(
    "frappe_pim.pim.api.export.export_bmecat",
    profile_name="standard_bmecat_de"
)
print(result["file_url"])  # /private/files/standard_bmecat_de_20260227.xml

# With direct parameters (no profile needed)
result = frappe.call(
    "frappe_pim.pim.api.export.export_bmecat",
    supplier_id="MYCOMPANY-DE",
    supplier_name="My Company GmbH",
    catalog_id="CAT2026",
    catalog_version="2.0",
    language="deu",
    currency="EUR",
    include_prices=True,
    include_media=True
)
```

**Run a CSV export with filtering:**
```python
result = frappe.call(
    "frappe_pim.pim.api.export.export_csv",
    product_family="Apparel",
    status_filter="Active",
    completeness_threshold=80,
    delimiter=";",
    include_header=True
)
print(result["row_count"])  # 1,234
```

**Async (background) export for large catalogs:**
```python
result = frappe.call(
    "frappe_pim.pim.api.export.export_json",
    profile_name="full_catalog_json",
    async_export=True
)
print(result["job_id"])  # Background job ID for status tracking
```

**Preview before exporting:**
```python
preview = frappe.call(
    "frappe_pim.pim.api.export.preview_export_data",
    profile_name="amazon_feed",
    limit=5
)
print(f"Total products: {preview['total_products']}")
for p in preview["preview"]:
    print(f"  {p.product_code} — {p.product_name} ({p.completeness_score}%)")
```

### 12.4 Scheduled Export Feeds

The PIM supports **automated scheduled exports** via Frappe's scheduler framework. The `generate_scheduled_feeds` task runs daily and processes all Export Profiles with `is_scheduled = 1` and `enabled = 1`.

**Scheduler Configuration (hooks.py):**

```python
scheduler_events = {
    "daily": [
        "frappe_pim.pim.tasks.scheduled.generate_scheduled_feeds",
    ],
}
```

**How Scheduled Exports Work:**

1. The daily scheduler triggers `generate_scheduled_feeds()`
2. All profiles matching `enabled = 1` AND `is_scheduled = 1` are queried
3. Each profile is enqueued as a **background job** (`queue="long"`, `timeout=3600s`)
4. The `generate_feed()` function auto-detects the export format and calls the appropriate handler:
   - BMEcat 2005 / 1.2 → `export_bmecat()`
   - CSV → `export_csv()`
   - JSON → `export_json()`
   - XML → `_export_generic_xml()`
5. The profile's `export_status`, `last_export`, and `last_file` are updated on completion or failure
6. Errors are logged to Frappe's Error Log with title "PIM Export Error"

**Customization Points for Scheduling:**

| Setting | Options | Impact |
|---------|---------|--------|
| `schedule_frequency` | Daily, Weekly, Monthly | Controls how often the profile is evaluated |
| `schedule_time` | Time value | Time of day for export (server timezone) |
| `completeness_threshold` | 0–100% | Quality gate — scheduled exports only include "ready" products |
| `compress_output` | Check | Enables ZIP compression for large scheduled feeds |
| `upload_to_channel` | Check | Automatically delivers file to linked channel |

### 12.5 Export Profile — Customer Archetype Examples

#### Fashion Retailer Export Profiles

```
Export Profiles:
  ├── amazon_bmecat_de
  │   ├── Format: BMEcat 2005
  │   ├── Channel: Amazon DE
  │   ├── Language: German (de)
  │   ├── Currency: EUR
  │   ├── Completeness Threshold: 90%
  │   ├── Include Variants: ✓
  │   ├── Include Prices: ✓
  │   ├── Scheduled: ✓ (Daily, 02:00)
  │   └── BMEcat Supplier ID: FASHION-DE-001
  │
  ├── shopify_json_full
  │   ├── Format: JSON
  │   ├── Channel: Shopify
  │   ├── Language: English (en)
  │   ├── Currency: USD
  │   ├── Completeness Threshold: 80%
  │   ├── Include Variants: ✓
  │   ├── Include Media: ✓
  │   ├── Pretty Print: ✓
  │   └── Scheduled: ✓ (Daily, 03:00)
  │
  ├── wholesale_csv_partners
  │   ├── Format: CSV
  │   ├── Delimiter: Semicolon (;)
  │   ├── Encoding: UTF-8-BOM (Excel-friendly)
  │   ├── Product Family: Apparel
  │   ├── Status Filter: Active
  │   ├── Include Variants: ✗ (master-level only)
  │   ├── Include Prices: ✓
  │   └── Scheduled: ✓ (Weekly)
  │
  └── internal_review_xlsx
      ├── Format: Excel
      ├── Status Filter: Draft
      ├── Completeness Threshold: 0%
      ├── Include Variants: ✓
      └── Scheduled: ✗ (manual/on-demand)
```

#### Industrial Supplier Export Profiles

```
Export Profiles:
  ├── procurement_bmecat_2005
  │   ├── Format: BMEcat 2005
  │   ├── Language: German (de)
  │   ├── Currency: EUR
  │   ├── Completeness Threshold: 95%
  │   ├── Include Variants: ✓
  │   ├── Include Prices: ✓
  │   ├── BMEcat Supplier ID: IND-SUPPLY-001
  │   ├── BMEcat Catalog Version: 3.2
  │   ├── Scheduled: ✓ (Daily, 01:00)
  │   └── Compress Output: ✓
  │
  ├── erp_sync_csv
  │   ├── Format: CSV
  │   ├── Delimiter: Tab
  │   ├── Encoding: UTF-8
  │   ├── Completeness Threshold: 100%
  │   ├── Status Filter: Active
  │   ├── Include Variants: ✓
  │   └── Scheduled: ✓ (Daily, 00:30)
  │
  └── safety_datasheets_xml
      ├── Format: XML
      ├── Product Family: Safety Equipment
      ├── Root Element: safety_products
      ├── Include Media: ✓ (datasheet PDFs)
      └── Scheduled: ✓ (Weekly)
```

#### Food Manufacturer Export Profiles

```
Export Profiles:
  ├── retailer_feed_json
  │   ├── Format: JSON
  │   ├── Channel: (retailer-specific)
  │   ├── Completeness Threshold: 85%
  │   ├── Include Variants: ✓ (pack sizes)
  │   ├── Include Media: ✓
  │   ├── Pretty Print: ✗ (compact for API)
  │   └── Scheduled: ✓ (Daily, 04:00)
  │
  ├── regulatory_xml_export
  │   ├── Format: XML
  │   ├── Product Family: Packaged Food
  │   ├── Root Element: food_products
  │   ├── Include Variants: ✓
  │   └── Scheduled: ✓ (Monthly)
  │
  └── distributor_bmecat
      ├── Format: BMEcat 1.2 (legacy compatibility)
      ├── Language: English (en)
      ├── Currency: GBP
      ├── BMEcat Supplier ID: FOOD-MFG-UK
      ├── Completeness Threshold: 90%
      └── Scheduled: ✓ (Weekly)
```

### 12.6 Import Configuration (Planned)

> **Status:** Part of the planned architecture. Not yet implemented as a DocType.

The Import Configuration DocType is designed to handle **inbound product data** from external sources such as supplier feeds, ERP exports, spreadsheet uploads, and partner data submissions.

**Planned Capabilities:**

| Feature | Description |
|---------|-------------|
| **Source Types** | File upload (CSV, XLSX, XML, JSON), API endpoint, FTP/SFTP polling |
| **Field Mapping** | Configurable mapping between source columns and PIM fields |
| **Import Field Mapping** (child table) | Source field → PIM field mapping with transformation rules |
| **Validation Rules** | Required fields, data type validation, uniqueness constraints |
| **Duplicate Handling** | Skip, Update, Create New — configurable per-field |
| **Attribute Mapping** | Map source columns to PIM EAV attributes |
| **Media Import** | Import images from URLs or file references |
| **Scheduling** | Automated import from FTP/API sources on schedule |
| **Error Handling** | Row-level error logging with ability to retry failed rows |
| **Dry Run Mode** | Preview changes before committing to database |

**Planned Import Field Mapping Pattern:**

```
Import Configuration: "Supplier A Feed"
  └── Import Field Mappings:
      ├── source: "artikelnummer"  → target: "product_code"  (transform: uppercase)
      ├── source: "bezeichnung"    → target: "product_name"  (transform: trim)
      ├── source: "beschreibung"   → target: "short_description" (transform: strip_html)
      ├── source: "gewicht_kg"     → target: attribute:"weight" (transform: float)
      ├── source: "farbe"          → target: attribute:"color"  (transform: lookup_option)
      ├── source: "ean"            → target: "barcode"  (transform: validate_gtin)
      └── source: "bild_url"       → target: media (transform: download_image)
```

### 12.7 Webhook Configuration (Planned)

> **Status:** Part of the planned architecture. DocType JSON and delivery utilities (`webhook_triggers.py`, `webhook_delivery.py`) are referenced in the spec but not yet implemented.

The Webhook Configuration DocType is designed to enable **real-time event-driven integration** by sending HTTP callbacks to external systems when product data changes occur in the PIM.

**Planned Webhook Events:**

| Event | Trigger | Payload |
|-------|---------|---------|
| `product.created` | New Product Master inserted | Product data with attributes |
| `product.updated` | Product Master saved | Changed fields + full product data |
| `product.approved` | Product moves to "Approved" status | Product data with approval metadata |
| `product.archived` | Product moves to "Archived" status | Product name + archive reason |
| `variant.created` | New Product Variant inserted | Variant data with parent reference |
| `variant.updated` | Product Variant saved | Changed variant fields |
| `attribute.changed` | PIM Attribute value modified | Attribute name, old value, new value |
| `media.uploaded` | New Product Media added | Media URL, type, product reference |
| `export.completed` | Export Profile run completes | Profile name, format, file URL, count |
| `export.failed` | Export Profile run fails | Profile name, error message |
| `score.changed` | Completeness score changes | Product name, old score, new score |
| `channel.published` | Product published to channel | Product, channel, listing URL |

**Planned Webhook Configuration Fields:**

| Field | Type | Purpose |
|-------|------|---------|
| `webhook_name` | Data | Display name for the webhook |
| `webhook_url` | Data | Target HTTP endpoint URL |
| `http_method` | Select | `POST`, `PUT`, `PATCH` |
| `events` | Table MultiSelect | List of events to subscribe to |
| `secret` | Password | HMAC secret for payload signing |
| `content_type` | Select | `application/json`, `application/xml` |
| `headers` | Code (JSON) | Custom HTTP headers |
| `enabled` | Check | Enable/disable webhook |
| `retry_count` | Int | Number of retries on failure (default: 3) |
| `retry_interval` | Int | Seconds between retries (default: 60) |
| `product_family_filter` | Link → Product Family | Only trigger for specific family |
| `channel_filter` | Link → Channel | Only trigger for specific channel |

**Planned Webhook Delivery Pattern:**

```
Event: product.approved
  ↓
Webhook Configuration: "ERP Sync Webhook"
  ├── URL: https://erp.company.com/api/product-updates
  ├── Method: POST
  ├── Secret: hmac_sha256_key
  ├── Headers: {"X-PIM-Event": "product.approved"}
  └── Payload:
      {
        "event": "product.approved",
        "timestamp": "2026-02-27T14:30:00Z",
        "product": {
          "name": "PROD-001",
          "product_code": "TSH-BLK-XL",
          "product_name": "Classic T-Shirt",
          "status": "Approved",
          "completeness_score": 95
        },
        "signature": "sha256=abc123..."
      }
```

### 12.8 PIM Notification Rule (Planned)

> **Status:** Part of the planned architecture. Not yet implemented as a DocType.

The PIM Notification Rule DocType is designed to provide **internal alerting and notification** within the Frappe Desk UI and via email/Slack when significant events occur in the PIM system.

**Planned Notification Events:**

| Event Category | Events |
|----------------|--------|
| **Product Lifecycle** | Product created, approved, rejected, archived |
| **Quality** | Completeness score drops below threshold, quality policy violation |
| **Export** | Export completed, export failed, scheduled export missed |
| **AI** | AI enrichment completed, AI suggestion pending approval |
| **Channel** | Product published to channel, listing sync failed |
| **Collaboration** | Product assigned for review, feedback submitted |

**Planned Notification Channels:**

| Channel | Method |
|---------|--------|
| **Desk Notification** | Frappe in-app notification bell |
| **Email** | SMTP-based email notification |
| **Slack** | Slack webhook integration |
| **Microsoft Teams** | Teams webhook integration |
| **Custom Webhook** | Generic HTTP callback |

**Planned Notification Rule Fields:**

| Field | Type | Purpose |
|-------|------|---------|
| `rule_name` | Data | Display name |
| `event` | Select | Triggering event |
| `condition` | Code (Python) | Optional condition expression |
| `recipients` | Table MultiSelect → User | Notification recipients |
| `channels` | Multi Select | Delivery channels (Desk, Email, Slack, Teams) |
| `subject_template` | Data | Email/notification subject (Jinja) |
| `body_template` | Text Editor | Notification body (Jinja) |
| `enabled` | Check | Enable/disable rule |
| `product_family_filter` | Link → Product Family | Scope to specific family |
| `channel_filter` | Link → Channel | Scope to specific channel |

### 12.9 External Integration Points

The PIM system provides multiple integration surfaces for connecting with external systems:

#### 12.9.1 Current Integration Points

| Integration Point | Direction | Mechanism | Status |
|-------------------|-----------|-----------|--------|
| **ERPNext Item Sync** | Bidirectional | `doc_events` hooks on Item/Product | ✅ Active |
| **Export Profile Feeds** | Outbound | Profile-based scheduled/manual export | ✅ Active |
| **BMEcat Catalog Export** | Outbound | Industry-standard XML generation | ✅ Active |
| **CSV/JSON/XML API** | Outbound | API endpoints for data extraction | ✅ Active |
| **Frappe REST API** | Bidirectional | Standard Frappe CRUD endpoints for all DocTypes | ✅ Active |
| **Background Job Queue** | Internal | `frappe.enqueue()` for long-running exports | ✅ Active |
| **Scheduled Tasks** | Internal | Daily feed generation via scheduler | ✅ Active |

#### 12.9.2 Planned Integration Points

| Integration Point | Direction | Mechanism | Status |
|-------------------|-----------|-----------|--------|
| **Import Configuration** | Inbound | File/API/FTP-based product import | 🔲 Planned |
| **Webhook Delivery** | Outbound | Event-driven HTTP callbacks | 🔲 Planned |
| **PIM Notification Rule** | Internal/External | Event-based alerts (Desk, Email, Slack) | 🔲 Planned |
| **cXML Procurement** | Outbound | Ariba Network/procurement platform integration | 🔲 Planned |
| **EDIFACT** | Outbound | UN/EDIFACT message generation | 🔲 Planned |
| **GS1 XML / GDSN** | Outbound | GS1 Global Data Sync Network export | 🔲 Planned |
| **UBL** | Outbound | OASIS Universal Business Language | 🔲 Planned |
| **S3 Storage** | Outbound | AWS S3/compatible object storage for exports | 🔲 Planned |
| **FTP/SFTP Delivery** | Outbound | File transfer to partner systems | 🔲 Planned |

#### 12.9.3 Frappe REST API Integration Pattern

Since all PIM DocTypes are standard Frappe DocTypes, they are automatically accessible via the Frappe REST API. This provides a universal integration surface for any external system:

```
# CRUD Operations (available for all PIM DocTypes)
GET    /api/resource/Export Profile                     # List profiles
GET    /api/resource/Export Profile/{name}              # Get specific profile
POST   /api/resource/Export Profile                     # Create profile
PUT    /api/resource/Export Profile/{name}              # Update profile
DELETE /api/resource/Export Profile/{name}              # Delete profile

# Custom Endpoints
POST   /api/method/frappe_pim.pim.api.export.run_export
POST   /api/method/frappe_pim.pim.api.export.export_bmecat
POST   /api/method/frappe_pim.pim.api.export.export_csv
POST   /api/method/frappe_pim.pim.api.export.export_json
GET    /api/method/frappe_pim.pim.api.export.get_export_status
GET    /api/method/frappe_pim.pim.api.export.download_export
GET    /api/method/frappe_pim.pim.api.export.preview_export_data
GET    /api/method/frappe_pim.pim.api.export.get_export_profiles
GET    /api/method/frappe_pim.pim.api.export.get_export_history
GET    /api/method/frappe_pim.pim.api.export.get_export_formats

# Export Profile Controller Methods
POST   /api/method/frappe_pim.pim.doctype.export_profile.export_profile.get_export_profiles
POST   /api/method/frappe_pim.pim.doctype.export_profile.export_profile.get_export_formats
POST   /api/method/frappe_pim.pim.doctype.export_profile.export_profile.run_export
POST   /api/method/frappe_pim.pim.doctype.export_profile.export_profile.preview_export
POST   /api/method/frappe_pim.pim.doctype.export_profile.export_profile.bulk_enable_profiles
POST   /api/method/frappe_pim.pim.doctype.export_profile.export_profile.get_profiles_by_channel
POST   /api/method/frappe_pim.pim.doctype.export_profile.export_profile.get_scheduled_profiles
```

### 12.10 Field Mapping Customization

Field mapping customization controls how PIM product data is transformed and mapped to export output fields. The current implementation uses a **default field set** pattern with planned support for fully customizable mappings:

#### Current Default Export Fields (CSV)

```python
default_fields = [
    "name",                 # Internal document name
    "product_name",         # Display name
    "product_code",         # SKU/product code
    "status",               # Lifecycle status
    "short_description",    # Short description
    "product_family",       # Product Family link
    "completeness_score",   # Data completeness percentage
    "created",              # Creation timestamp
    "modified"              # Last modified timestamp
]
```

#### BMEcat Field Mapping (Automatic)

The BMEcat exporter maps PIM fields to BMEcat XML elements automatically:

| PIM Field | BMEcat Element | Notes |
|-----------|---------------|-------|
| `variant_code` / `product_code` | `SUPPLIER_AID` | Falls back to document name |
| `variant_name` / `product_name` | `DESCRIPTION_SHORT` | Required in BMEcat |
| `description` / `short_description` | `DESCRIPTION_LONG` | HTML stripped automatically |
| `barcode` / `ean` | `EAN` | GTIN/EAN barcode |
| `manufacturer_part_number` | `MANUFACTURER_AID` | Manufacturer's article number |
| `stock_uom` | `ORDER_UNIT` | Defaults to C62 (piece) per UN/CEFACT |
| `minimum_order_qty` | `QUANTITY_MIN` | Defaults to 1 |
| `price` / `standard_rate` | `PRICE_AMOUNT` | Net list price |
| `tax_rate` | `TAX` | Tax percentage |
| `image` | `MIME_SOURCE` (first) | Primary product image |
| `media` (child table) | `MIME_INFO` entries | Additional media with type detection |
| `attribute_values` (EAV) | `ARTICLE_FEATURES` → `FEATURE` | All attributes with name, value, unit |

#### Planned Custom Field Mapping (Export Profile Field child table)

The planned `Export Profile Field` child table would allow customers to define exactly which fields to include in each export and how to transform them:

| Field | Type | Purpose |
|-------|------|---------|
| `source_field` | Data | PIM field name or attribute code |
| `target_field` | Data | Output column/element name |
| `field_type` | Select | `DocType Field`, `Attribute`, `Computed` |
| `transform` | Select | `None`, `Uppercase`, `Lowercase`, `Strip HTML`, `Truncate`, `Custom` |
| `default_value` | Data | Value if source is empty |
| `include_in_export` | Check | Toggle field inclusion |
| `sort_order` | Int | Column order in output |

### 12.11 Export File Management

Export files are managed through Frappe's built-in File doctype with PIM-specific conventions:

**Storage Location:**
- Private files stored in `Home/Exports` folder (falls back to `Home` if folder doesn't exist)
- Files are created as private (`is_private = 1`) by default
- File naming pattern: `{profile_code}_{YYYYMMDD_HHMMSS}.{extension}`

**File Extension Mapping:**

| Export Format | Extension |
|--------------|-----------|
| BMEcat 2005 | `.xml` |
| BMEcat 1.2 | `.xml` |
| CSV | `.csv` |
| JSON | `.json` |
| XML | `.xml` |
| Excel | `.xlsx` |
| Compressed | `.zip` (when `compress_output` is enabled) |

**Export Log (Planned):**
The `PIM Export Log` DocType is referenced in the code for tracking export history across profiles. This would store:
- Export profile reference
- Export format
- Status (success/failure)
- File URL
- Product count
- Timestamps
- Error messages

### 12.12 Onboarding Checklist — Export & Integration

```
Phase 1 — Prerequisites:
  □ Ensure product families and channels are configured (Sections 1, 4)
  □ Ensure products have completeness scores calculated (Section 6)
  □ Verify channel-specific field requirements are met (Section 4)

Phase 2 — Export Profile Setup:
  □ Create Export Profile for each output requirement:
    □ Define export format (CSV/JSON/XML/BMEcat/Excel)
    □ Set product filters (family, status, completeness threshold)
    □ Configure format-specific options:
      □ CSV: delimiter, encoding
      □ BMEcat: supplier ID, supplier name, catalog ID, version
      □ XML/JSON: root element, pretty print
    □ Link to channel if applicable
    □ Set language and currency for the target market
    □ Configure output filename pattern
    □ Enable compression if needed for large catalogs

Phase 3 — Scheduling:
  □ Enable scheduled exports for automated feed generation
  □ Set schedule frequency (Daily/Weekly/Monthly)
  □ Set schedule time (choose off-peak hours in server timezone)
  □ Verify daily scheduler task is running:
    frappe_pim.pim.tasks.scheduled.generate_scheduled_feeds

Phase 4 — Testing & Validation:
  □ Use preview_export_data() to verify product filtering
  □ Run a manual export and verify output format
  □ For BMEcat: validate XML with validate_bmecat_xml()
  □ Verify file is saved to Home/Exports folder
  □ Test download via download_export() API
  □ For scheduled exports: verify cron triggers correctly

Phase 5 — Integration:
  □ Set up external system to consume export files
  □ For channel uploads: enable upload_to_channel on relevant profiles
  □ Monitor export status via get_export_status() API
  □ Review Error Log for any export failures
  □ Set up alerting for failed scheduled exports (planned: PIM Notification Rule)

Phase 6 — Ongoing Maintenance:
  □ Monitor export file disk usage
  □ Archive old export files periodically
  □ Review and update completeness thresholds as data matures
  □ Adjust schedule frequency based on downstream requirements
  □ Update BMEcat catalog version on major product data changes
```

---

## 13. Internationalization

### Overview

Frappe PIM implements a **multi-layer internationalization (i18n) architecture** that enables product content to be managed in multiple languages simultaneously. Rather than creating custom locale DocTypes, the PIM leverages Frappe's built-in **Language** DocType as its locale backbone while extending it with PIM-specific localization mechanisms at three levels:

1. **Field-Level Translation** — Frappe's native `translatable: 1` property on key display fields
2. **Attribute-Level Localization** — Per-locale attribute values via the EAV pattern (`Product Attribute Value` child table)
3. **Asset-Level Localization** — Per-locale media assignments via `Product Media` child table

**Architecture:**

```
┌────────────────────────────────────────────────────────────────────────────┐
│                         Frappe Language DocType                            │
│                    (Built-in locale management)                            │
│         en │ tr │ de │ fr │ es │ it │ nl │ pl │ ru │ zh │ ja │ ko         │
└──────┬─────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴───────────┘
       │
       ├──────────────────────────────────────────────────────────────┐
       │                                                              │
       ▼                                                              ▼
┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐
│  Field-Level i18n    │    │  Attribute-Level i18n │    │  Asset-Level i18n    │
│  (translatable: 1)   │    │  (EAV locale column)  │    │  (media locale)      │
│                      │    │                       │    │                       │
│  • product_name      │    │  Product Attribute    │    │  Product Media        │
│  • short_description │    │  Value child table    │    │  child table          │
│  • long_description  │    │  with locale field    │    │  with locale field    │
│  • family_name       │    │  (default: "tr")      │    │  (Link → Language)    │
│  • brand_name        │    │                       │    │                       │
│  • attribute_name    │    │  PIM Attribute        │    │  Channel              │
│  • variant_name      │    │  is_localizable flag  │    │  export_language      │
│  • channel_name      │    │                       │    │                       │
│  • group_name        │    │                       │    │  Export Profile       │
│  • manufacturer_name │    │                       │    │  export_language      │
│  • profile_name      │    │                       │    │                       │
└──────────────────────┘    └──────────────────────┘    └──────────────────────┘
```

**When to Configure:** Phase 2 of onboarding — after Product Families and Attributes, before content entry
**Who Configures:** PIM Manager (locale strategy), PIM User (content translation)
**Business Impact:** Determines how many markets a customer can serve from a single PIM instance and whether product content is truly localized vs. merely translated

---

### 13.1 Locale Management via Frappe Language DocType

**DocType:** `Language` (Frappe Core)
**Purpose:** Provides the master list of available locales for all i18n functionality throughout the PIM.

The PIM does **not** implement a custom `PIM Locale` DocType. Instead, it references Frappe's built-in `Language` DocType wherever locale selection is required. This design ensures:

- Consistency with Frappe framework UI language settings
- No duplication of locale master data
- Automatic availability of all Frappe-supported languages
- Compatibility with ERPNext multi-language features

**Default Locale:** The system defaults to **Turkish (`tr`)** as evidenced by the `Product Attribute Value` child table's `locale` field default value. This reflects the application's initial deployment context but is fully configurable per customer.

#### Locale Configuration Points

| DocType | Field | Purpose | Default |
|---------|-------|---------|---------|
| `Product Attribute Value` | `locale` | Locale for this attribute value | `tr` (Turkish) |
| `Product Media` | `locale` | Locale for this media item | Empty (all locales) |
| `Channel` | `export_language` | Default language for channel exports | — |
| `Export Profile` | `export_language` | Language for export output | — |

#### How to Change the Default Locale

For non-Turkish deployments, the default locale should be reconfigured during onboarding:

```python
# Option 1: Change the default at DocType level (System Manager)
# Navigate to Customize Form → Product Attribute Value → locale field
# Change the "Default" value from "tr" to your primary locale (e.g., "en", "de")

# Option 2: Set via API when creating attribute values programmatically
doc.append("attribute_values", {
    "attribute": "product_description",
    "locale": "en",  # Override default
    "value_text": "English product description"
})

# Option 3: Use bulk_update_attribute with explicit locale
frappe.call(
    "frappe_pim.pim.doctype.product_master.product_master.bulk_update_attribute",
    products=["PROD-001", "PROD-002"],
    attribute="short_description",
    value="New description text",
    locale="en"  # Specify target locale
)
```

#### Supported Languages (12 ISO 639 Mappings)

The BMEcat export module provides the definitive language code mapping used across the PIM for ISO 639-2 compliance in international trade data:

| ISO 639-1 | ISO 639-2 | Language | Common Use Case |
|-----------|-----------|----------|-----------------|
| `en` | `eng` | English | Global marketplace default |
| `de` | `deu` | German | BMEcat exports, DACH region |
| `fr` | `fra` | French | EU compliance, Canada |
| `es` | `spa` | Spanish | LATAM, Spain marketplace |
| `it` | `ita` | Italian | Southern EU |
| `nl` | `nld` | Dutch | Benelux region |
| `pl` | `pol` | Polish | Eastern EU |
| `tr` | `tur` | Turkish | Trendyol, Hepsiburada, N11 |
| `ru` | `rus` | Russian | CIS markets |
| `zh` | `zho` | Chinese | Asia-Pacific, AliExpress |
| `ja` | `jpn` | Japanese | Japan marketplace |
| `ko` | `kor` | Korean | South Korea marketplace |

> **Note:** Additional languages can be added via Frappe's Language DocType. The ISO 639-2 mapping in the BMEcat export module (`_get_language_code()`) defaults unknown codes to `"eng"` (English) and can be extended as needed.

---

### 13.2 Field-Level Translation (Frappe Translatable Property)

**Mechanism:** Frappe's built-in `translatable: 1` field property
**Storage:** Frappe's `Translation` DocType (core framework)
**Purpose:** Provides UI-level translations for key display fields across the PIM

When a field is marked as `translatable: 1` in the DocType JSON definition, Frappe automatically:
1. Stores translations in the core `Translation` DocType
2. Renders the translated value based on the user's UI language
3. Falls back to the source language if no translation exists

#### Translatable Fields Reference

| DocType | Field | Type | Translation Purpose |
|---------|-------|------|-------------------|
| **Product Master** | `product_name` | Data | Product display name across markets |
| **Product Master** | `short_description` | Small Text | Brief product summary for listings |
| **Product Master** | `long_description` | Text Editor | Full product description for detail pages |
| **Product Variant** | `variant_name` | Data | SKU-level display name |
| **Product Family** | `family_name` | Data | Category display in multi-language UI |
| **Brand** | `brand_name` | Data | Brand display for international markets |
| **Manufacturer** | `manufacturer_name` | Data | Manufacturer display name |
| **PIM Attribute** | `attribute_name` | Data | Attribute label in multi-language forms |
| **PIM Attribute Group** | `group_name` | Data | Attribute group tab labels |
| **Channel** | `channel_name` | Data | Channel display in multi-language UI |
| **Export Profile** | `profile_name` | Data | Export profile label |

**Customization Impact:** These fields use Frappe's standard translation mechanism. For customers operating in multiple languages, these translations should be populated during onboarding to ensure the PIM interface and reports render correctly in each user's language.

#### Field-Level Translation vs. Attribute-Level Localization

It is important to understand the distinction between these two mechanisms:

| Aspect | Field-Level Translation | Attribute-Level Localization |
|--------|------------------------|------------------------------|
| **Mechanism** | Frappe `translatable: 1` | EAV `locale` column on `Product Attribute Value` |
| **Storage** | Frappe `Translation` DocType | `Product Attribute Value` child table rows |
| **Scope** | DocType display field labels & values | Dynamic attribute values per product |
| **Use Case** | UI rendering for PIM users | Product content for end consumers |
| **Granularity** | Per-field per-DocType record | Per-attribute per-product per-locale |
| **Export Support** | Not directly exported | Exported via locale-aware queries |
| **Default** | User's UI language | `tr` (Turkish) on attribute values |
| **Configured By** | System Manager / Frappe Translation Manager | PIM User / Content Editor |

---

### 13.3 Attribute-Level Localization (EAV Multi-Locale Pattern)

**DocType (Child Table):** `Product Attribute Value`
**Parent DocTypes:** `Product Master` (field: `attribute_values`), `Product Variant`
**Purpose:** Stores product attribute values with per-locale granularity, enabling the same product to have different attribute values for different languages.

This is the **primary i18n mechanism for product content** in the PIM. The EAV pattern naturally supports multi-locale values because each attribute value row includes a `locale` field that links to Frappe's `Language` DocType.

#### Product Attribute Value — Locale-Relevant Fields

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `attribute` | Link → PIM Attribute | — (required) | Which attribute this value belongs to |
| `locale` | Link → Language | `tr` | Language/locale for this specific value |
| `value_text` | Small Text | — | Text values (name, short desc) |
| `value_long_text` | Text | — | Long text values (full descriptions) |
| `value_int` | Int | — | Integer values (quantities) |
| `value_float` | Float (6 precision) | — | Decimal values (dimensions) |
| `value_boolean` | Check | — | Boolean values (certifications) |
| `value_date` | Date | — | Date values (manufacture date) |
| `value_datetime` | Datetime | — | Timestamp values |
| `value_link` | Dynamic Link | — | Reference values |
| `is_inherited` | Check (read-only) | `0` | Whether value was inherited from parent family |
| `inherited_from` | Data (read-only, hidden) | — | Source family of inherited value |

#### How Multi-Locale Attribute Values Work

For a localizable attribute (e.g., `product_description`), a product stores **one row per locale**:

```
Product: TSHIRT-001
┌────────────────────────┬────────┬───────────────────────────────┐
│ Attribute              │ Locale │ Value                         │
├────────────────────────┼────────┼───────────────────────────────┤
│ product_description    │ tr     │ Pamuklu erkek tişört          │
│ product_description    │ en     │ Cotton men's t-shirt          │
│ product_description    │ de     │ Herren-T-Shirt aus Baumwolle  │
│ product_description    │ fr     │ T-shirt homme en coton        │
│ care_instructions      │ tr     │ 30°C'de yıkayınız            │
│ care_instructions      │ en     │ Wash at 30°C                  │
│ material_composition   │ tr     │ %100 Pamuk                    │
│ material_composition   │ en     │ 100% Cotton                   │
│ weight                 │ tr     │ 0.250                         │
│ [weight has same value for all locales — non-localizable]       │
└────────────────────────┴────────┴───────────────────────────────┘
```

> **Key Insight:** Non-localizable attributes (like `weight`, `dimensions`, `barcode`) only need a single row regardless of how many locales are configured. Only attributes flagged with `is_localizable = 1` need per-locale rows.

#### The is_localizable Flag on PIM Attribute

**DocType:** `PIM Attribute`
**Field:** `is_localizable` (Check, default: `0`)
**Section:** Localization

This flag determines whether an attribute can have different values per locale:

| is_localizable | Behavior | Example Attributes |
|---------------|----------|-------------------|
| `0` (default) | Single value for all locales | weight, width, height, barcode, GTIN, pack_quantity |
| `1` | Separate value per locale row | product_name, description, care_instructions, material_name, color_name, size_label |

**Decision Guide — Which Attributes to Localize:**

| Attribute Category | Localize? | Rationale |
|-------------------|-----------|-----------|
| Text descriptions | ✅ Yes | Content varies by language |
| Names and labels | ✅ Yes | Display text varies by market |
| Care/usage instructions | ✅ Yes | Regulatory text varies by region |
| Material compositions | ✅ Yes | Naming conventions differ |
| Numeric measurements | ❌ No | Universal values (weight, dimensions) |
| Barcodes/identifiers | ❌ No | Global identifiers |
| Boolean flags | ❌ No | True/false is language-agnostic |
| Dates | ❌ No | Dates are universal |
| Select options (codes) | ❌ No | Internal codes are language-agnostic |
| Select option labels | ✅ Yes | Display labels vary by language |

---

### 13.4 Asset-Level Localization (Media Per Locale)

**DocType (Child Table):** `Product Media`
**Parent DocTypes:** `Product Master`, `Product Variant`
**Purpose:** Associates media files with products, with optional per-locale and per-channel targeting.

#### Product Media — Locale-Relevant Fields

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `file` | Attach | — (required) | The media file |
| `media_type` | Select | `Gallery` | Type: Main Image, Gallery, Thumbnail, 360 View, Video, Document, Other |
| `title` | Data | — | Display title for the media item |
| `alt_text` | Data | — | Accessibility alternative text |
| `locale` | Link → Language | — (empty = all) | Target locale for this media |
| `channel` | Link → Channel | — (empty = all) | Target channel for this media |
| `apply_to_variant` | Link → Product Variant | — (empty = all) | Restrict to specific variant |
| `sort_order` | Int | `0` | Display ordering |

**How Locale-Specific Media Works:**

```
Product: TSHIRT-001
┌────────────────────────┬────────────┬────────┬─────────────────────────────┐
│ File                   │ Media Type │ Locale │ Purpose                     │
├────────────────────────┼────────────┼────────┼─────────────────────────────┤
│ tshirt_main.jpg        │ Main Image │ (all)  │ Universal product photo     │
│ tshirt_lifestyle_tr.jpg│ Gallery    │ tr     │ Turkish market lifestyle    │
│ tshirt_lifestyle_de.jpg│ Gallery    │ de     │ German market lifestyle     │
│ size_guide_tr.pdf      │ Document   │ tr     │ Turkish size guide          │
│ size_guide_en.pdf      │ Document   │ en     │ English size guide          │
│ care_label_eu.jpg      │ Document   │ de     │ EU care label (German)      │
└────────────────────────┴────────────┴────────┴─────────────────────────────┘
```

> **Tip:** When `locale` is left empty, the media applies to all locales. Use locale-specific media for size guides, care labels, regulatory documents, and market-specific lifestyle imagery.

---

### 13.5 Channel-Level Language Configuration

Each distribution channel can specify a default export language, ensuring product content is exported in the correct language for the target marketplace.

#### Channel DocType — Language Fields

| Field | Type | Purpose |
|-------|------|---------|
| `export_language` | Link → Language | Default language for product data exported to this channel |
| `export_currency` | Link → Currency | Currency for price exports (related i18n concern) |

#### Export Profile — Language Fields

| Field | Type | Purpose |
|-------|------|---------|
| `export_language` | Link → Language | Language for exported product data |
| `export_currency` | Link → Currency | Currency for price exports |

#### Channel-Language Mapping Matrix

| Channel | Primary Language | Typical Languages | Currency |
|---------|-----------------|-------------------|----------|
| **Amazon TR** | Turkish (`tr`) | `tr` | TRY |
| **Amazon DE** | German (`de`) | `de`, `en` | EUR |
| **Amazon US** | English (`en`) | `en`, `es` | USD |
| **Amazon FR** | French (`fr`) | `fr` | EUR |
| **Trendyol** | Turkish (`tr`) | `tr` | TRY |
| **Hepsiburada** | Turkish (`tr`) | `tr` | TRY |
| **N11** | Turkish (`tr`) | `tr` | TRY |
| **Shopify** | Configurable | Store language | Store currency |
| **WooCommerce** | Configurable | Site language | Site currency |
| **Google Merchant** | Market-specific | Country language | Country currency |
| **eBay** | Market-specific | `en`, `de`, `fr` | Market currency |
| **Etsy** | English (`en`) | `en` | USD/EUR/GBP |
| **Walmart** | English (`en`) | `en`, `es` | USD |
| **Meta Commerce** | Configurable | Account language | Account currency |
| **TikTok Shop** | Market-specific | Country language | Country currency |

#### BMEcat Export Language Handling

The BMEcat export module includes a dedicated language code conversion function for ISO 639-2 compliance:

```python
# Language code conversion for BMEcat XML exports
# Frappe uses ISO 639-1 (2-letter), BMEcat requires ISO 639-2 (3-letter)

# Default export language: "deu" (German) — standard for BMEcat in DACH region
# Configured via: Export Profile → export_language field

# Conversion map (12 languages):
# en → eng | de → deu | fr → fra | es → spa
# it → ita | nl → nld | pl → pol | tr → tur
# ru → rus | zh → zho | ja → jpn | ko → kor
# Unknown → eng (fallback)
```

---

### 13.6 Translation Workflow

While the PIM does not yet implement a formal `PIM Translation Status` tracking DocType, the following translation workflow can be established using the existing infrastructure:

#### Recommended Translation Workflow

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐     ┌──────────────┐
│  1. Author   │────▶│  2. Translate │────▶│  3. Review     │────▶│  4. Publish   │
│  (Primary    │     │  (Add locale  │     │  (QA check     │     │  (Export to   │
│   locale)    │     │   rows)       │     │   per locale)  │     │   channels)   │
└─────────────┘     └──────────────┘     └───────────────┘     └──────────────┘
     │                     │                     │                     │
     ▼                     ▼                     ▼                     ▼
 Create product      Add attribute          Verify all            Channel export
 with primary        values for each        required locales      with per-channel
 locale attributes   target locale          have complete         export_language
                                            translations          selection
```

**Step 1 — Author in Primary Locale:**
```python
# Create product with primary locale attribute values
product = frappe.get_doc({
    "doctype": "Product Master",
    "product_name": "Pamuklu Tişört",
    "product_family": "Apparel",
    "attribute_values": [
        {
            "attribute": "short_description",
            "locale": "tr",
            "value_text": "Yumuşak pamuklu erkek tişört"
        },
        {
            "attribute": "care_instructions",
            "locale": "tr",
            "value_long_text": "30°C'de yıkayınız. Çamaşır kurutma makinesi kullanmayınız."
        }
    ]
})
product.insert()
```

**Step 2 — Translate to Target Locales:**
```python
# Add English translations
product = frappe.get_doc("Product Master", "TSHIRT-001")
product.append("attribute_values", {
    "attribute": "short_description",
    "locale": "en",
    "value_text": "Soft cotton men's t-shirt"
})
product.append("attribute_values", {
    "attribute": "care_instructions",
    "locale": "en",
    "value_long_text": "Wash at 30°C. Do not tumble dry."
})
product.save()
```

**Step 3 — Bulk Translation via API:**
```python
# Bulk update attribute values across multiple products
frappe.call(
    "frappe_pim.pim.doctype.product_master.product_master.bulk_update_attribute",
    products=["TSHIRT-001", "TSHIRT-002", "TSHIRT-003"],
    attribute="short_description",
    value="Soft cotton men's t-shirt",
    locale="en"
)
```

#### Translation Completeness Tracking

While formal translation status tracking is not yet implemented as a standalone DocType, translation completeness can be measured through the scoring system:

- **Translation Score** contributes **15%** to the overall product completeness score (see Section 6)
- Translation completeness is computed by checking what percentage of localizable attributes have values for each required locale
- The score formula: `translation_score = (localized_attributes_filled / total_localizable_attributes) × 100`

**Planned Enhancement:** The architecture references `PIM Translation Status` as a planned child table that would track per-product, per-locale translation status with fields for:
- `locale` — Target language
- `status` — Translation state (Pending, In Progress, Translated, Reviewed, Published)
- `translator` — Assigned translator (User)
- `reviewed_by` — Reviewer (User)
- `completion_percentage` — Percentage of localizable attributes translated
- `last_translated` — Timestamp of last translation update

---

### 13.7 Multi-Language Attribute Planning Guide

When onboarding a new customer, the i18n strategy must be planned based on:

1. **Number of target markets** — determines how many locales need to be configured
2. **Content differentiation** — whether markets need truly localized content vs. simple translation
3. **Channel language requirements** — each marketplace has specific language requirements
4. **Regulatory requirements** — some markets require product information in the local language

#### Per-Customer Locale Planning Matrix

| Consideration | Single-Market | Regional (2-5 Markets) | Global (6+ Markets) |
|--------------|--------------|----------------------|---------------------|
| **Primary locale** | Customer's language | HQ language | English (typical) |
| **Additional locales** | None | Market languages | All target languages |
| **Localizable attributes** | Minimal (descriptions only) | All text attributes | All text + select labels |
| **Media localization** | None | Size guides, labels | Full market-specific media |
| **Translation workflow** | N/A | Manual or AI-assisted | Professional + AI review |
| **Export profiles** | 1 per channel | 1 per market × channel | Matrix of market × channel |
| **Translation score weight** | Can be reduced | Standard (15%) | May increase (20-25%) |

---

### 13.8 Customer Archetype Examples — Internationalization

#### Fashion Retailer (Turkey-based, EU expansion)

```
Primary Locale: tr (Turkish)
Target Locales: tr, en, de
Localizable Attributes:
  ├── product_name          → tr, en, de
  ├── short_description     → tr, en, de
  ├── long_description      → tr, en, de
  ├── care_instructions     → tr, en, de  (regulatory requirement)
  ├── material_composition  → tr, en, de  (EU labeling regulation)
  ├── color_name            → tr, en, de
  └── size_label            → tr, en, de  (EU/UK sizing differences)

Non-Localizable Attributes:
  ├── weight, width, height, depth  (universal)
  ├── barcode, gtin                  (global identifiers)
  └── material_percentage            (numeric, universal)

Channel Language Configuration:
  ├── Trendyol        → export_language: tr
  ├── Hepsiburada     → export_language: tr
  ├── Amazon DE       → export_language: de
  ├── Shopify (INT)   → export_language: en
  └── Google Merchant  → export_language: per-market

Media Localization:
  ├── Product photos   → locale: (all) — same images globally
  ├── Size guides      → locale: tr, en, de — region-specific sizing
  └── Care labels      → locale: de — EU care symbol requirements
```

#### Industrial Supplier (Germany-based, pan-European)

```
Primary Locale: de (German)
Target Locales: de, en, fr, nl, pl
Localizable Attributes:
  ├── product_name            → de, en, fr, nl, pl
  ├── technical_description   → de, en  (only major markets)
  ├── safety_warnings         → de, en, fr, nl, pl  (mandatory per market)
  ├── application_notes       → de, en
  └── material_name           → de, en, fr

Non-Localizable Attributes:
  ├── tolerance_grade, tensile_strength  (universal specs)
  ├── din_standard, iso_standard         (standard references)
  └── gtin, ean                          (identifiers)

Channel Language Configuration:
  ├── BMEcat Export (DE)    → export_language: de (default for BMEcat)
  ├── BMEcat Export (EN)    → export_language: en
  ├── Webshop (DE)          → export_language: de
  ├── Webshop (INT)         → export_language: en
  └── Amazon EU             → export_language: per-marketplace

Media Localization:
  ├── Technical drawings    → locale: (all) — language-independent
  ├── Safety datasheets     → locale: de, en, fr — regulatory per region
  └── Installation guides   → locale: de, en — major markets only
```

#### Food Manufacturer (Multi-national, strict labeling)

```
Primary Locale: en (English)
Target Locales: en, de, fr, es, it, nl
Localizable Attributes:
  ├── product_name              → all 6 locales
  ├── ingredients_list          → all 6 locales  (EU Regulation 1169/2011)
  ├── allergen_statement        → all 6 locales  (mandatory per market)
  ├── nutritional_claims        → all 6 locales  (health claim regulations)
  ├── storage_instructions      → all 6 locales
  ├── preparation_instructions  → all 6 locales
  └── flavor_description        → all 6 locales

Non-Localizable Attributes:
  ├── calories, fat, protein, carbohydrates  (numeric)
  ├── net_weight, gross_weight               (numeric)
  ├── barcode, gtin                           (identifiers)
  └── shelf_life_days                         (numeric)

Channel Language Configuration:
  ├── Amazon (per market)   → export_language: market language
  ├── Shopify (INT)         → export_language: en
  ├── Google Merchant       → export_language: per-country
  └── BMEcat (GDSN)        → export_language: en (primary)

Media Localization:
  ├── Product photos        → locale: (all) — universal
  ├── Nutrition labels      → locale: per market — regulatory format
  ├── Allergen warnings     → locale: per market — regulatory text
  └── Recipe cards          → locale: per market — marketing content
```

---

### 13.9 Translation API Reference

#### Bulk Attribute Update with Locale

```python
# API: frappe_pim.pim.doctype.product_master.product_master.bulk_update_attribute
# Method: POST (whitelisted)

frappe.call({
    "method": "frappe_pim.pim.doctype.product_master.product_master.bulk_update_attribute",
    "args": {
        "products": ["PROD-001", "PROD-002", "PROD-003"],
        "attribute": "short_description",
        "value": "Updated English description",
        "locale": "en"  // Defaults to "tr" if omitted
    }
})

# Response:
{
    "updated": 3,
    "errors": []
}
```

#### Get Family Attributes (Including Localization Metadata)

```python
# API: frappe_pim.pim.doctype.product_master.product_master.get_family_attributes
# Method: GET (whitelisted)

frappe.call({
    "method": "frappe_pim.pim.doctype.product_master.product_master.get_family_attributes",
    "args": {
        "family": "Apparel"
    }
})

# Response includes is_localizable flag per attribute:
[
    {
        "attribute": "short_description",
        "attribute_name": "Short Description",
        "attribute_code": "short_description",
        "data_type": "Text",
        "is_required": 1,
        "is_filterable": 0,
        "is_localizable": 1,  // This attribute needs per-locale values
        "group": "General",
        "from_family": "Apparel"
    },
    {
        "attribute": "weight",
        "attribute_name": "Weight",
        "attribute_code": "weight",
        "data_type": "Float",
        "is_required": 1,
        "is_filterable": 1,
        "is_localizable": 0,  // Single value for all locales
        "group": "Dimensions",
        "from_family": "Apparel"
    }
]
```

#### Querying Locale-Specific Attribute Values

```python
# Get all attribute values for a product in a specific locale
values = frappe.get_all(
    "Product Attribute Value",
    filters={
        "parent": "PROD-001",
        "parenttype": "Product Master",
        "locale": "en"
    },
    fields=["attribute", "locale", "value_text", "value_long_text",
            "value_int", "value_float", "value_boolean"]
)

# Get translation completeness for a product
product = frappe.get_doc("Product Master", "PROD-001")
family_attrs = get_family_attributes(product.product_family)
localizable_attrs = [a for a in family_attrs if a["is_localizable"]]
target_locales = ["tr", "en", "de"]

for locale in target_locales:
    locale_values = [
        row for row in product.attribute_values
        if row.locale == locale and row.attribute in [a["attribute"] for a in localizable_attrs]
    ]
    filled = len([v for v in locale_values if v.value_text or v.value_long_text])
    total = len(localizable_attrs)
    completeness = (filled / total * 100) if total else 100
    print(f"  {locale}: {completeness:.0f}% ({filled}/{total} attributes)")
```

---

### 13.10 Integration with AI Translation Service

The PIM architecture references an AI Translation service (`services/ai_translation.py`) for automated translation of product content. While this service is part of the planned feature set, when available it would integrate with the i18n infrastructure as follows:

**AI-Assisted Translation Workflow:**

```
┌──────────────┐    ┌─────────────────┐    ┌──────────────────┐    ┌──────────────┐
│ Source Text   │───▶│ AI Translation  │───▶│ Human Review     │───▶│ Save to EAV  │
│ (Primary      │    │ Service         │    │ (Approval Queue) │    │ (Product     │
│  Locale)      │    │                 │    │                  │    │  Attribute   │
└──────────────┘    └─────────────────┘    └──────────────────┘    │  Value)      │
                                                                    └──────────────┘
```

**Integration Points:**
- Source text read from `Product Attribute Value` rows for the primary locale
- AI provider configured in PIM Settings (see Section 10: AI & Enrichment)
- Translated text written back as new `Product Attribute Value` rows with the target locale
- Human-in-the-loop review via `AI Approval Queue` (see Section 10)
- Confidence thresholds from AI Enrichment settings control auto-approval

---

### 13.11 Onboarding Checklist — Internationalization

```
Phase 1 — Locale Strategy Planning:
  □ Identify primary locale for the customer's base market
  □ List all target locales (markets to serve)
  □ Verify target languages exist in Frappe's Language DocType
  □ Decide default locale for Product Attribute Value (change from "tr" if needed)
  □ Document which attributes need to be localizable

Phase 2 — Attribute Localization Setup:
  □ For each PIM Attribute that needs translation:
    □ Set is_localizable = 1
    □ Verify attribute data type supports localization (Text, Long Text, Select labels)
  □ For non-localizable attributes (numeric, boolean, identifiers):
    □ Verify is_localizable = 0 (default)

Phase 3 — Channel Language Configuration:
  □ For each Channel:
    □ Set export_language to the channel's target language
    □ Set export_currency for the target market
  □ For each Export Profile:
    □ Set export_language for the export target
    □ If BMEcat: verify ISO 639-2 code mapping is correct
    □ Create separate export profiles for different language versions if needed

Phase 4 — Media Localization:
  □ Identify which media types need per-locale versions:
    □ Size guides (if sizing differs by region)
    □ Regulatory labels (care labels, nutrition labels, safety data)
    □ Marketing materials (market-specific lifestyle imagery)
  □ Upload locale-specific media with the locale field set
  □ Upload universal media with locale field empty

Phase 5 — Content Translation:
  □ Enter product content in primary locale first
  □ Translate localizable attributes to each target locale:
    □ Manual entry for high-value content
    □ Bulk API for repetitive translations
    □ AI translation for scale (if enabled)
  □ Populate Frappe Translation records for translatable display fields
    (product_name, family_name, brand_name, attribute labels)

Phase 6 — Verification:
  □ Verify each product has attribute values for all required locales
  □ Check translation completeness via scoring (15% weight)
  □ Test channel exports in each target language
  □ Verify BMEcat exports include correct ISO 639-2 language codes
  □ Confirm media locale assignments are correct
  □ Validate regulatory content translations (care labels, allergen statements)
```

---

## 14. Bundling & Packaging

### Overview

The PIM provides a comprehensive bundling and packaging subsystem that supports product bundles, GS1 packaging hierarchies, barcode generation, and GS1 standards validation. This enables customers to manage product kits, multi-packs, tiered pricing bundles, and logistics packaging levels — all with full GS1 compliance.

**Architecture:**

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   PIM Bundle     │────▶│  PIM Bundle Slot  │────▶│ Product Variant  │
│   (Kit/Pack Def) │     │  (Component)      │     │ or Product Master│
└──────────────────┘     └──────────────────┘     └──────────────────┘
         │                                                │
         ▼                                                ▼
┌──────────────────┐                            ┌──────────────────────┐
│ PIM Bundle Tier  │                            │ Product Barcode Item │
│ (Volume Pricing) │                            │ (EAN/UPC/GTIN/QR)   │
└──────────────────┘                            └──────────────────────┘

┌──────────────────────┐     ┌──────────────────┐
│ GS1 Packaging        │────▶│  Package Variant  │
│ Hierarchy            │     │  (Pack-Level SKU) │
└──────────────────────┘     └──────────────────┘

Utility Layer:
  gs1_validation.py   → GTIN/GLN/SSCC validation & check digit calculation
  barcode_generator.py → EAN-13, UPC-A, Code 128, QR code generation
  bundle.py           → Bundle pricing, slot management, ERPNext sync
```

### 14.1 PIM Bundle

**DocType:** `PIM Bundle`
**Module:** PIM
**Naming Rule:** `field:bundle_code`
**Purpose:** Defines product bundles — combinations of products sold together as kits, multi-packs, or configurable collections.

#### Configurable Fields

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `bundle_name` | Data (required) | — | Display name for the bundle | Customer-visible bundle names |
| `bundle_code` | Data (required, unique) | — | URL-safe unique identifier | Used in API calls, export feeds |
| `bundle_type` | Select (required) | — | Static / Configurable / Dynamic / Build Your Own | Determines bundle behavior model |
| `status` | Select | `Draft` | Draft / Active / Inactive / Archived | Controls bundle availability |
| `pricing_method` | Select (required) | — | Sum of Components / Fixed Price / Fixed Discount / Percentage Discount / Tiered Pricing | Core pricing strategy for bundle |
| `base_price` | Currency | — | Reference price for discount calculations | Used when pricing_method involves discounts |
| `discount_type` | Select | — | Percentage / Fixed Amount | Type of discount applied |
| `discount_value` | Float | — | Discount amount | Actual discount applied to bundle |
| `currency` | Link → Currency | — | Bundle pricing currency | Must match customer's operating currency |
| `slots` | Table → PIM Bundle Slot | — | Component items in the bundle | **Core customization** — defines bundle contents |
| `tiered_pricing` | Table → PIM Bundle Tier | — | Volume-based pricing tiers | Enables quantity-break pricing |
| `min_items` | Int | — | Minimum items in bundle | Validation constraint for BYO bundles |
| `max_items` | Int | `0` | Maximum items (0 = unlimited) | Limits bundle size |
| `allow_duplicates` | Check | `0` | Allow same product multiple times | BYO and configurable bundles |
| `require_all_slots` | Check | `0` | All slots must be filled | Strict bundle completion requirement |
| `filter_category` | Link → Product Family | — | Dynamic bundle category filter | Auto-populates dynamic bundles from family |
| `filter_product_type` | Link → PIM Product Type | — | Dynamic bundle type filter | Restricts dynamic bundle products |
| `filter_brand` | Link → Brand | — | Dynamic bundle brand filter | Brand-specific bundles |
| `available_channels` | Table MultiSelect → Bundle Channel | — | Channels where bundle is available | Per-channel bundle availability |
| `valid_from` | Date | — | Bundle validity start | Seasonal/promotional bundles |
| `valid_to` | Date | — | Bundle validity end | Auto-deactivate after date |
| `erp_product_bundle` | Link → Product Bundle | — | Linked ERPNext Product Bundle | ERP integration for inventory/invoicing |
| `auto_sync_to_erp` | Check | `0` | Automatically sync to ERPNext | Enables bidirectional bundle sync |
| `total_items` | Int (read-only) | — | Total items in bundle | Computed from slots |
| `calculated_price` | Currency (read-only) | — | Current calculated price | Computed based on pricing_method |
| `savings_amount` | Currency (read-only) | — | Amount saved vs. individual | Marketing: shows bundle value |
| `savings_percent` | Percent (read-only) | — | Percentage saved | Marketing: shows bundle value |

**Bundle Types Explained:**

| Type | Customer Selects? | Items Pre-defined? | Filter-Based? | Use Case |
|------|------------------|--------------------|--------------|----------|
| **Static** | No | Yes | No | Fixed kit (e.g., "Starter Pack" with specific items) |
| **Configurable** | From slot options | Slots defined, options vary | No | "Choose your color" within pre-set slots |
| **Dynamic** | No | No | Yes | Rule-based inclusion (e.g., "All accessories under €20") |
| **Build Your Own** | Yes, freely | No | Optional | Customer builds their own bundle from catalog |

**When to Configure:** Phase 3 — after products, families, and channels are set up
**Who Configures:** PIM Manager (bundle structure), Sales/Marketing (pricing)
**Business Impact:** Drives cross-sell/upsell strategy, affects margin calculations, and maps to ERPNext Product Bundle for inventory/invoicing

### 14.2 PIM Bundle Slot

**DocType:** `PIM Bundle Slot` (child table of PIM Bundle)
**Purpose:** Defines individual component slots within a bundle, with configurability options, quantity constraints, and dependency rules.

#### Configurable Fields

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `slot_name` | Data | — | Display name (e.g., "Main Product", "Accessory 1") | Customer-visible slot labels |
| `slot_code` | Data | — | Unique identifier within bundle | API reference for slot |
| `product_variant` | Link → Product Variant | — | Specific variant for this slot | Fixed-product slots |
| `product_master` | Link → Product Master | — | Product master (alternative to variant) | Template-level slots |
| `qty` | Float | `1` | Default quantity for slot | Per-component quantity |
| `is_required` | Check | `1` | Slot must be filled | Optional vs. mandatory components |
| `is_configurable` | Check | `0` | Customer can choose different product | Enables "choose your..." UX |
| `allow_qty_change` | Check | `0` | Customer can adjust quantity | Flexible quantity bundles |
| `min_qty` | Float | `1` | Minimum quantity allowed | Quantity validation |
| `max_qty` | Float | `0` | Maximum quantity (0 = unlimited) | Quantity limits |
| `sort_order` | Int | `0` | Display order in bundle | Controls slot presentation sequence |
| `price_modifier_type` | Select | — | Fixed Amount / Percentage | How slot price is adjusted |
| `price_modifier` | Float | — | Amount to add/subtract | Slot-level pricing override |
| `allowed_category` | Link → Product Family | — | Restrict configurable slot to family | Limits configurable choices by category |
| `allowed_product_type` | Link → PIM Product Type | — | Restrict to product type | Limits configurable choices by type |
| `allowed_brand` | Link → Brand | — | Restrict to brand | Brand-specific slot options |
| `filter_expression` | Small Text | — | Custom JSON filter expression | Advanced filtering for slot options |
| `depends_on_slot` | Data | — | Slot code this depends on | Sequential selection (e.g., "pick size after color") |
| `excluded_with_slot` | Data | — | Slot code mutually exclusive with | "Either A or B, not both" logic |

### 14.3 PIM Bundle Tier

**DocType:** `PIM Bundle Tier` (child table of PIM Bundle)
**Purpose:** Defines volume-based pricing tiers for bundles using tiered pricing.

#### Configurable Fields

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `min_qty` | Int | Minimum quantity for this tier | Tier entry threshold |
| `max_qty` | Int | Maximum quantity for this tier | Tier ceiling |
| `discount_type` | Select | Percentage / Fixed Amount | Type of volume discount |
| `discount_value` | Float | Discount amount for this tier | Actual savings at this volume |
| `price` | Currency | Flat tier price (alternative to discount) | Direct price-per-unit at volume |

**Example Tiered Pricing:**

```
Bundle: "Office Supply Kit"
Pricing Method: Tiered Pricing

Tier 1: 1-9 units   → No discount (base price: $49.99)
Tier 2: 10-24 units → 10% discount ($44.99 each)
Tier 3: 25-99 units → 20% discount ($39.99 each)
Tier 4: 100+ units  → 30% discount ($34.99 each)
```

### 14.4 GS1 Packaging Hierarchy

**DocType:** `GS1 Packaging Hierarchy`
**Module:** PIM
**Purpose:** Implements the GS1 packaging level standard, enabling customers to define how products are packaged at different levels (each, inner pack, case, pallet) with proper GTIN identifiers at each level.

> **GS1 Standard:** The packaging hierarchy follows the GS1 General Specifications for trade item identification at multiple packaging levels, using indicator digits in GTIN-14 to distinguish levels.

#### Configurable Fields

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `product_master` | Link → Product Master | Base product | Links hierarchy to product |
| `product_variant` | Link → Product Variant | Specific variant (optional) | Variant-level packaging |
| `packaging_level` | Select | Each / Inner Pack / Case / Pallet / Display | Standard GS1 packaging levels |
| `level_gtin` | Data | GTIN for this packaging level | GS1-compliant identifier per level |
| `indicator_digit` | Data | GTIN-14 indicator digit (0-9) | Identifies packaging level in GTIN-14 |
| `quantity_per_level` | Int | Units contained at this level | How many of the lower level fit |
| `parent_level` | Link → GS1 Packaging Hierarchy | Parent packaging level | Builds the nesting hierarchy |
| `dimensions_length` | Float | Package length | Physical dimensions for logistics |
| `dimensions_width` | Float | Package width | Physical dimensions for logistics |
| `dimensions_height` | Float | Package height | Physical dimensions for logistics |
| `dimensions_uom` | Select | Unit of measurement (cm/in/mm) | Dimensional UOM |
| `gross_weight` | Float | Gross weight at this level | Logistics weight |
| `weight_uom` | Select | Weight unit (kg/lb/g) | Weight UOM |

**GS1 Packaging Level Example:**

```
Product: "Premium Olive Oil 500ml" (GTIN-13: 8690123456789)

Packaging Hierarchy:
├── Level 0 (Each):      GTIN-13: 8690123456789  (1 bottle)
│   └── Level 1 (Inner): GTIN-14: 18690123456786 (6-pack, indicator: 1)
│       └── Level 2 (Case):  GTIN-14: 28690123456783 (24-pack = 4 inner, indicator: 2)
│           └── Level 3 (Pallet): GTIN-14: 38690123456780 (480 = 20 cases, indicator: 3)

Each level has:
  - Unique GTIN with indicator digit
  - Quantity of child units
  - Physical dimensions & weight
  - Barcode generation capability
```

**When to Configure:** Phase 3 — after products have GTINs assigned
**Who Configures:** PIM Manager (structure), Supply Chain (dimensions/weights)
**Business Impact:** Required for GS1-compliant supply chain integration, GDSN data synchronization, and retailer compliance

### 14.5 Package Variant

**DocType:** `Package Variant`
**Module:** PIM
**Purpose:** Represents pack-level SKU variants — products that differ only in packaging quantity (e.g., single bottle vs. 6-pack vs. case of 24).

#### Configurable Fields

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `variant_name` | Data | Display name for the package variant | Customer-visible pack size name |
| `variant_code` | Data | Unique identifier | SKU-level identifier |
| `product_master` | Link → Product Master | Base product | Links to parent product |
| `packaging_hierarchy` | Link → GS1 Packaging Hierarchy | GS1 packaging level | Ties to formal GS1 hierarchy |
| `pack_quantity` | Int | Number of units in this package | Core pack size definition |
| `pack_uom` | Link → UOM | Unit of measurement | Pack-level UOM |
| `pack_gtin` | Data | GTIN for this package size | GS1-compliant pack identifier |
| `pack_weight` | Float | Total weight of pack | Logistics information |
| `is_default` | Check | Default package variant | Used when no pack size specified |

### 14.6 GS1 Validation (`gs1_validation.py`)

**Module:** `frappe_pim.pim.utils.gs1_validation`
**Purpose:** Comprehensive GS1 standards validation and generation utility supporting GTIN-8/12/13/14, GLN, SSCC, and GSIN identifiers.

#### Supported GS1 Identifier Types

| Identifier | Digits | Purpose | Validation Function |
|-----------|--------|---------|-------------------|
| **GTIN-8** | 8 | Small product barcodes (EAN-8) | `validate_gtin8()` |
| **GTIN-12** | 12 | North American products (UPC-A) | `validate_gtin12()` |
| **GTIN-13** | 13 | Global retail products (EAN-13) | `validate_gtin13()` |
| **GTIN-14** | 14 | Packaging levels (ITF-14) | `validate_gtin14()` |
| **GLN** | 13 | Location identification (warehouses, stores) | `validate_gln()` |
| **SSCC** | 18 | Shipping container/pallet tracking | `validate_sscc()` |
| **GSIN** | 17 | Shipment identification | `validate_gsin()` |

#### Core Validation Functions

**Check Digit Algorithm (GS1 Standard Modulo-10):**

```python
# The GS1 check digit algorithm works for all GS1 keys
from frappe_pim.pim.utils.gs1_validation import (
    calculate_check_digit,
    verify_check_digit,
    validate_gtin,
    validate_gln,
    validate_sscc,
)

# Calculate check digit for a GTIN-13
check = calculate_check_digit("629104150021")  # Returns '3'
# Full GTIN: 6291041500213

# Verify an existing check digit
is_valid = verify_check_digit("6291041500213")  # Returns True

# Validate any GTIN format (auto-detects type)
result = validate_gtin("4006381333931")
# result.is_valid → True
# result.identifier_type → "GTIN_13"
# result.normalized → "4006381333931"
# result.check_digit → "1"
```

**Validation Results:**

Each validation function returns a `ValidationResult` dataclass:

```python
@dataclass
class ValidationResult:
    is_valid: bool               # Whether the identifier is valid
    identifier: str              # Original input
    identifier_type: str | None  # "GTIN_13", "GLN", "SSCC", etc.
    normalized: str | None       # Cleaned/normalized identifier
    check_digit: str | None      # The check digit
    errors: list[str] | None     # Validation errors
    warnings: list[str] | None   # Non-fatal warnings
```

#### GS1 Prefix Lookup

The module includes a comprehensive GS1 country prefix database (130+ countries) for identifying the origin of a GTIN:

```python
from frappe_pim.pim.utils.gs1_validation import get_gs1_prefix_info

info = get_gs1_prefix_info("8690123456789")
# {'prefix': '869', 'organization': 'GS1 Turkey', 'country': 'Turkey'}
```

#### Hook Integration

GS1 validation can be automatically enforced on document save via Frappe hooks:

```python
# In hooks.py:
doc_events = {
    "Product Master": {
        "validate": "frappe_pim.pim.utils.gs1_validation.validate_gtin_on_save"
    },
    "Supplier": {
        "validate": "frappe_pim.pim.utils.gs1_validation.validate_gln_on_save"
    }
}
```

#### Batch Validation

```python
from frappe_pim.pim.utils.gs1_validation import validate_identifiers

results = validate_identifiers(
    ["4006381333931", "INVALID123", "8690123456789"],
    identifier_type="gtin"
)
# results["valid_count"] → 2
# results["invalid_count"] → 1
```

#### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `frappe_pim.pim.utils.gs1_validation.api_validate_gtin` | POST | Validate a GTIN (includes prefix info) |
| `frappe_pim.pim.utils.gs1_validation.api_validate_gln` | POST | Validate a GLN |
| `frappe_pim.pim.utils.gs1_validation.api_validate_sscc` | POST | Validate an SSCC |
| `frappe_pim.pim.utils.gs1_validation.api_calculate_check_digit` | POST | Calculate check digit for any GS1 identifier |

### 14.7 Barcode Generation (`barcode_generator.py`)

**Module:** `frappe_pim.pim.utils.barcode_generator`
**Dependencies:** `python-barcode` (linear barcodes), `qrcode` (QR codes)
**Purpose:** Generate barcode images in SVG or PNG format for products, packaging, and logistics.

#### Supported Barcode Formats (12 total)

| Format | Enum Value | Digits/Data | Primary Use |
|--------|-----------|-------------|------------|
| **EAN-13** | `ean13` | 13 digits | Global retail product identification |
| **EAN-8** | `ean8` | 8 digits | Small product identification |
| **UPC-A** | `upca` | 12 digits | North American retail |
| **Code 128** | `code128` | ASCII text | Logistics, shipping labels |
| **Code 39** | `code39` | Alphanumeric | Industrial applications |
| **ISBN-13** | `isbn13` | 13 digits (978/979) | Book identification |
| **ISBN-10** | `isbn10` | 10 chars | Legacy book identification |
| **ISSN** | `issn` | 8 chars | Serial publication identification |
| **ITF** | `itf` | Even-length digits | GTIN-14 outer packaging (cases, pallets) |
| **PZN** | `pzn` | 7-8 digits | German pharmaceutical products |
| **JAN** | `jan` | 13 digits | Japanese Article Number (= EAN-13) |
| **QR Code** | `qr` | Any text/URL | Mobile scanning, product info URLs |

#### Barcode Configuration

```python
from frappe_pim.pim.utils.barcode_generator import (
    BarcodeConfig, BarcodeFormat, ImageFormat,
    generate_barcode, generate_ean13, generate_qr_code,
)

# Custom barcode configuration
config = BarcodeConfig(
    format=BarcodeFormat.EAN13,
    image_format=ImageFormat.SVG,   # SVG (scalable) or PNG (raster)
    width=None,                      # Module width in mm (None = default)
    height=None,                     # Bar height in mm (None = default)
    include_text=True,               # Human-readable text below bars
    text_distance=5.0,               # Text-to-bars distance in mm
    font_size=10,                    # Font size for text
    quiet_zone=6.5,                  # Quiet zone width in mm
    background="white",              # Background color
    foreground="black",              # Bar color
    dpi=300,                         # DPI for PNG output
)

# Generate EAN-13 barcode
result = generate_ean13("8690123456789")
# result.success → True
# result.svg_content → "<svg>...</svg>"
# result.image_base64 → "PHN2Zy..." (base64 encoded)
```

#### QR Code Configuration

```python
from frappe_pim.pim.utils.barcode_generator import (
    QRConfig, QRErrorCorrection, generate_qr_code,
)

qr_config = QRConfig(
    version=None,                              # Auto-detect version (1-40)
    error_correction=QRErrorCorrection.MEDIUM,  # L(7%) / M(15%) / Q(25%) / H(30%)
    box_size=10,                               # Pixels per module
    border=4,                                  # Border width in modules
    fill_color="black",                        # Module color
    back_color="white",                        # Background color
)

result = generate_qr_code(
    "https://example.com/product/PROD-001",
    config=qr_config
)
```

#### Product Barcode Generation (Frappe Integration)

```python
# Generate barcode from Product Master document
from frappe_pim.pim.utils.barcode_generator import (
    generate_product_barcode,
    save_barcode_to_file,
)

# Generate barcode in memory
result = generate_product_barcode("PROD-001", barcode_format="ean13")
# Returns dict with image_base64, svg_content, etc.

# Generate and save as Frappe File attachment
file_result = save_barcode_to_file("PROD-001", barcode_format="ean13")
# file_result["file_url"] → "/files/barcode_PROD-001_ean13.png"
```

#### Batch Generation

```python
from frappe_pim.pim.utils.barcode_generator import generate_barcodes_batch

items = [
    {"data": "8690123456789", "format": "ean13"},
    {"data": "SHIP-2026-001", "format": "code128"},
    {"data": "https://example.com/p/123", "format": "qr"},
]
results = generate_barcodes_batch(items)
# Returns list of BarcodeResult objects
```

#### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `api_generate_barcode` | POST | Generate barcode from data + format |
| `api_generate_qr` | POST | Generate QR code with custom settings |
| `api_generate_product_barcode` | POST | Generate barcode from Product Master |
| `api_save_product_barcode` | POST | Generate and save as Frappe File |
| `api_get_supported_formats` | GET | List all supported barcode/image formats |

### 14.8 Product Barcode Item

**DocType:** `Product Barcode Item` (child table)
**Purpose:** Manages multiple barcode identifiers per product or variant, supporting different barcode types, UOM-specific barcodes, and validity periods.

#### Configurable Fields

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `barcode_type` | Select | EAN-13 / UPC-A / EAN-8 / UPC-E / Code 128 / Code 39 / QR Code / ISBN / ISSN / GTIN-14 / Other | Barcode standard used |
| `barcode` | Data | Barcode value | Actual barcode number |
| `is_primary` | Check | Mark as primary barcode | Default barcode for exports |
| `apply_to_variant` | Link → Product Variant | Apply to specific variant only | Variant-specific barcodes |
| `apply_to_uom` | Link → UOM | Apply to specific UOM (Box, Carton, Pallet) | Pack-level barcode assignment |
| `valid_from` | Date | Barcode validity start | Seasonal/rotational barcode management |
| `valid_to` | Date | Barcode validity end | Barcode retirement tracking |
| `notes` | Small Text | Additional notes | Documentation for barcode assignments |

### 14.9 Customer Archetype Examples — Bundling & Packaging

#### Fashion Retailer (Multi-pack and Gift Sets)

```
Bundles:
  ├── "3-Pack Basic Tees"
  │     Type: Static
  │     Pricing: Fixed Discount (15%)
  │     Slots:
  │       ├── Tee #1: Classic Tee (White, customer picks size)  → configurable
  │       ├── Tee #2: Classic Tee (Navy, customer picks size)   → configurable
  │       └── Tee #3: Classic Tee (Black, customer picks size)  → configurable
  │
  ├── "Complete Outfit Builder"
  │     Type: Build Your Own
  │     Pricing: Percentage Discount (10%)
  │     Constraints: min_items: 3, max_items: 5
  │     Slot Categories: Tops, Bottoms, Accessories
  │
  └── "Holiday Gift Set"
        Type: Static
        Pricing: Fixed Price ($79.99)
        Valid: Nov 1 – Dec 31
        Channels: E-Commerce, Retail

Barcodes:
  ├── Individual items: EAN-13 (GS1 Turkey prefix 869)
  ├── Multi-packs: GTIN-14 with indicator digit
  └── Gift sets: Unique EAN-13 per set SKU

GS1 Packaging:
  ├── Each (1 item): GTIN-13
  ├── Inner Pack (3-pack): GTIN-14 (indicator: 1)
  └── Case (12 inner): GTIN-14 (indicator: 2)
```

#### Industrial Supplier (Component Kits)

```
Bundles:
  ├── "Fastener Assortment Kit"
  │     Type: Static
  │     Pricing: Sum of Components (no discount)
  │     Slots: 12 fixed components with specific quantities
  │     ERP Sync: auto_sync_to_erp ✓ (maps to ERPNext Product Bundle)
  │
  └── "Custom Tooling Package"
        Type: Configurable
        Pricing: Tiered
        Tiers:
          ├── 1-4 kits:   Base price ($299)
          ├── 5-19 kits:  10% off ($269.10)
          └── 20+ kits:   20% off ($239.20)

Barcodes:
  ├── Components: Code 128 (alphanumeric part numbers)
  ├── Kits: EAN-13 (retail) + Code 128 (internal)
  └── Pallets: SSCC (18-digit shipping container code)

GS1 Packaging (Component: M10 Bolt):
  ├── Each (1 bolt): No barcode (bulk item)
  ├── Box (100 bolts): GTIN-14 (indicator: 1), 500g
  ├── Case (20 boxes = 2000): GTIN-14 (indicator: 2), 12kg
  └── Pallet (48 cases = 96,000): SSCC, 620kg
```

#### Food Manufacturer (Multi-Pack and Displays)

```
Bundles:
  ├── "Variety 12-Pack"
  │     Type: Static
  │     Pricing: Fixed Price
  │     Slots: 4×Flavor A, 4×Flavor B, 4×Flavor C
  │
  └── "POS Display Bundle"
        Type: Static
        Pricing: Sum of Components
        Includes: Display stand + 24 units
        Channels: Retail only

Barcodes:
  ├── Individual: EAN-13 (per flavor)
  ├── Multi-pack: EAN-13 (unique per pack config)
  └── Trade units: ITF-14 (GTIN-14 in ITF symbology)

GS1 Packaging (Product: "Organic Juice 250ml"):
  ├── Each:      GTIN-13: 8690123456789
  ├── 6-Pack:    GTIN-14: 18690123456786 (indicator: 1)
  ├── Tray (4×6=24): GTIN-14: 28690123456783 (indicator: 2)
  ├── Case (6 trays=144): GTIN-14: 38690123456780 (indicator: 3)
  └── Pallet (80 cases): SSCC: 389012345000000012
```

### 14.10 Onboarding Checklist — Bundling & Packaging

```
Phase 1 — GS1 Setup:
  □ Obtain GS1 Company Prefix from national GS1 organization
  □ Configure barcode_type default in PIM Settings (EAN-13 for EU/TR, UPC-A for NA)
  □ Decide on GTIN assignment strategy (manual vs. auto-generated)
  □ Verify GS1 prefix in gs1_validation.py prefix database
  □ If GDSN participation: configure GDSN sync service

Phase 2 — Product Barcode Assignment:
  □ Assign primary GTIN to each Product Master
  □ For multi-barcode products:
    □ Add Product Barcode Item entries for each barcode type
    □ Mark primary barcode with is_primary ✓
    □ Assign variant-specific barcodes via apply_to_variant
    □ Assign UOM-specific barcodes via apply_to_uom (Box, Carton, Pallet)
  □ Run batch GTIN validation via validate_identifiers()
  □ Generate barcode images for catalog/label printing

Phase 3 — Packaging Hierarchy:
  □ For products requiring multi-level packaging:
    □ Define each level in GS1 Packaging Hierarchy
    □ Assign GTIN-14 with correct indicator digit per level
    □ Enter dimensions and weights per packaging level
    □ Link parent-child relationships between levels
  □ Create Package Variants for pack-size SKUs
  □ Validate all GTIN-14 check digits

Phase 4 — Bundle Configuration:
  □ Identify bundle types needed (static kits, configurable, BYO)
  □ For each bundle:
    □ Create PIM Bundle with appropriate bundle_type and pricing_method
    □ Define slots with products, quantities, and configurability
    □ Set channel availability via available_channels
    □ If tiered pricing: define PIM Bundle Tier entries
    □ Set validity dates for promotional bundles
  □ If ERPNext integration:
    □ Link erp_product_bundle to corresponding ERPNext Product Bundle
    □ Enable auto_sync_to_erp for automatic sync
  □ Test bundle pricing calculations
  □ Generate bundle-level barcodes

Phase 5 — Verification:
  □ Validate all GTINs pass check digit verification
  □ Verify packaging hierarchy levels have correct indicator digits
  □ Test barcode generation for all formats needed (EAN-13, ITF-14, QR, etc.)
  □ Verify bundle pricing calculations match expected values
  □ Test ERPNext Product Bundle sync (if enabled)
  □ Confirm barcode images render correctly in exports
```

---

## 15. MDM (Master Data Management)

### Overview

The PIM includes a full MDM (Master Data Management) subsystem for managing the "single source of truth" for product data across multiple systems. The MDM layer provides golden record management, source system tracking, survivorship rules for merge conflict resolution, data steward governance, and event-sourced merge history.

**Architecture:**

```
┌──────────────────┐     ┌──────────────────────┐     ┌──────────────────┐
│  Source System    │────▶│   Golden Record       │◀────│  Source System    │
│  (ERP)           │     │   (Single Truth)       │     │  (Import/API)    │
└──────────────────┘     └──────────────────────┘     └──────────────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    ▼              ▼              ▼
          ┌──────────────┐ ┌────────────┐ ┌────────────────┐
          │ Survivorship │ │ Golden     │ │ Data Steward   │
          │ Rule         │ │ Record     │ │ (Governance)   │
          │ (Conflict    │ │ Source     │ │                │
          │  Resolution) │ │ (Sources)  │ │                │
          └──────────────┘ └────────────┘ └────────────────┘

Service Layer:
  merge_survive.py  → Merge execution, survivorship application, event sourcing
  mdm_tasks.py      → Background MDM tasks (auto-merge, validation, cleanup)
```

**Key MDM Concepts:**

| Concept | Implementation | Purpose |
|---------|---------------|---------|
| **Golden Record** | `Golden Record` DocType | Single authoritative version of a product across all sources |
| **Source System** | `Source System` DocType | External system providing product data (ERP, import, API) |
| **Survivorship** | `Survivorship Rule` DocType | Rules determining which source's value "wins" per field |
| **Data Steward** | `Data Steward` DocType | Human governance role responsible for data quality |
| **Merge/Survive** | `merge_survive.py` service | Execution engine for merging records according to rules |
| **Event Sourcing** | Merge history in Golden Record | Full audit trail of all merge operations |

### 15.1 Golden Record

**DocType:** `Golden Record`
**Module:** PIM
**Naming Rule:** `field:golden_record_code`
**Purpose:** Represents the single authoritative version of a product's data, assembled from one or more source systems using survivorship rules.

#### Configurable Fields — Basic Information

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `record_name` | Data (required) | — | Display name for golden record | Human-readable record title |
| `golden_record_code` | Data (required, unique) | — | Unique identifier | Used in API calls and references |
| `product_master` | Link → Product Master | — | Canonical product linked to record | Maps golden record to PIM product |
| `status` | Select | `Draft` | Draft / Active / Merged / Archived | Record lifecycle state |

#### Configurable Fields — Survivorship Configuration

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `survivorship_rule` | Select | — | Most Recent / Highest Confidence / Source Priority / Manual Override / Most Complete | **Core MDM decision** — how field-level conflicts are resolved |
| `source_priority_order` | Small Text | — | Comma-separated source priority (e.g., "ERP,PIM,Import") | Defines which system's data takes precedence |
| `merge_mode` | Select | — | Automatic / Manual Review Required / AI Assisted | Controls human-in-the-loop for merges |
| `auto_merge_threshold` | Percent | `95` | Confidence threshold for auto-merge | Above this threshold, merge happens without review |

**Survivorship Rules Explained:**

| Rule | When "Wins" | Best For |
|------|------------|----------|
| **Most Recent** | Latest-updated value | Fast-changing data (prices, stock levels) |
| **Highest Confidence** | Value with highest confidence score | Data from verified/audited sources |
| **Source Priority** | Value from highest-priority source | Clear system hierarchy (ERP → PIM → Import) |
| **Manual Override** | Manually selected value | Critical data requiring human judgment |
| **Most Complete** | Record with most populated fields | Enrichment scenarios with partial data |

#### Configurable Fields — Source Records

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `source_records` | Table → Golden Record Source | Products & sources contributing to record | **Core MDM surface** — which sources feed the golden record |

#### Configurable Fields — Data Quality Metrics (Read-Only)

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `confidence_score` | Percent | Overall data accuracy confidence | Quality indicator for the merged record |
| `data_completeness` | Percent | Percentage of fields with valid data | Completeness tracking |
| `match_score` | Percent | How well sources matched during merge | Indicates deduplication confidence |
| `quality_issues` | Small Text | Identified data quality issues | Highlights data problems for stewards |

#### Configurable Fields — Data Governance

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `data_steward` | Link → Data Steward | User responsible for maintaining record | Assigns accountability for data quality |
| `steward_assigned_at` | Datetime (read-only) | When steward was assigned | Audit trail |
| `approved_by` | Link → User (read-only) | User who approved the record | Approval tracking |
| `approved_at` | Datetime (read-only) | When approved | Approval timestamp |

#### Configurable Fields — Merge Tracking (Read-Only)

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `last_merged_at` | Datetime | When last merge was performed | Merge recency tracking |
| `merge_count` | Int | Number of merge operations performed | Activity tracking |
| `last_validated_at` | Datetime | When record was last validated | Validation recency |
| `validation_status` | Select | Pending / Valid / Invalid / Needs Review | Current validation state |

#### Configurable Fields — Field-Level Tracking

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `field_sources` | JSON | Maps each field to its source system | Full provenance per field |
| `field_confidence` | JSON | Confidence score per field | Granular data quality assessment |

**Field-Level Tracking Example:**

```json
// field_sources — which source provided each field value
{
    "product_name": "ERP",
    "short_description": "PIM",
    "long_description": "Import",
    "weight": "ERP",
    "color": "PIM",
    "material": "Import"
}

// field_confidence — confidence score for each field
{
    "product_name": 98.5,
    "short_description": 95.0,
    "long_description": 72.3,
    "weight": 99.9,
    "color": 90.0,
    "material": 65.0
}
```

**When to Configure:** Phase 2-3 — after source systems and product families are defined
**Who Configures:** PIM Manager (structure), Data Steward (ongoing governance)
**Business Impact:** Determines the authoritative version of product data; critical for multi-system environments

### 15.2 Golden Record Source

**DocType:** `Golden Record Source` (child table of Golden Record)
**Purpose:** Tracks each source product contributing to a Golden Record, including confidence scoring and sync metadata.

#### Configurable Fields

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `source_product` | Link → Product Master | — | Product contributing to golden record | Maps source product to merged record |
| `source_system` | Select | — | ERP / PIM / Import / API / Manual / External | Identifies the originating system |
| `confidence_score` | Percent | — | Data confidence for this source (0-100%) | Influences survivorship when using Highest Confidence |
| `is_primary` | Check | `0` | Mark as primary/authoritative source | Primary source has implicit priority |
| `is_winning` | Check (read-only) | `0` | Won based on survivorship rules | Indicates which source currently "wins" |
| `added_at` | Datetime (read-only) | — | When added to golden record | Audit trail |
| `last_synced_at` | Datetime (read-only) | — | Last sync from source | Tracks data freshness |
| `external_id` | Data | — | ID from external system | Cross-system mapping |
| `notes` | Small Text | — | Notes about source record | Documentation for merge decisions |

### 15.3 Source System

**DocType:** `Source System`
**Module:** PIM
**Naming Rule:** `field:system_code`
**Purpose:** Defines external systems that provide product data to the PIM, with connection configuration, sync settings, and default confidence levels.

#### Configurable Fields

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `system_name` | Data (required) | — | Display name for the source system | Human-readable system name |
| `system_code` | Data (required, unique) | — | Unique identifier slug | Referenced in survivorship rules and APIs |
| `system_type` | Select | — | ERP / PIM / Import / API / Manual / E-Commerce / Marketplace / Supplier Portal / Data Pool | Classification of source system |
| `is_active` | Check | `1` | Enable/disable this source | Controls whether system participates in MDM |
| `connection_type` | Select | — | REST API / Database / File Import / Webhook / Manual | How data arrives from this system |
| `base_url` | Data | — | API base URL (if applicable) | Connection endpoint |
| `api_key_field` | Password | — | API key or credentials | Secure credential storage |
| `default_confidence` | Percent | `80` | Default confidence for data from this source | Baseline trust level for this system's data |
| `sync_direction` | Select | `Inbound` | Inbound / Outbound / Bidirectional | Data flow direction |
| `sync_frequency` | Select | `Manual` | Real-time / Hourly / Daily / Weekly / Manual | How often data syncs |
| `field_mapping` | JSON | — | Field name mapping between systems | Transforms external field names to PIM fields |
| `priority` | Int | `50` | Default priority (1=highest, 100=lowest) | Used by Source Priority survivorship rule |
| `last_sync_at` | Datetime (read-only) | — | Last successful sync | Monitoring metric |
| `total_records_synced` | Int (read-only) | `0` | Total records synced from this source | Volume tracking |
| `error_count` | Int (read-only) | `0` | Total sync errors | Error monitoring |

**When to Configure:** Phase 1-2 — during initial system setup, before golden records
**Who Configures:** System Manager (connection), PIM Manager (confidence/priority)
**Business Impact:** Defines the data landscape; incorrect confidence or priority settings lead to wrong values winning in merges

### 15.4 Survivorship Rule

**DocType:** `Survivorship Rule`
**Module:** PIM
**Naming Rule:** `field:rule_code`
**Purpose:** Defines the strategy for selecting the "winning" value when merging records from multiple sources. Survivorship rules are the core of MDM conflict resolution.

#### Configurable Fields — Basic

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `rule_name` | Data (required, translatable) | — | Display name | Human-readable rule identifier |
| `rule_code` | Data (required, unique) | — | Unique identifier slug | Referenced in golden records and APIs |
| `rule_type` | Select (required) | — | Source Priority / Most Recent / Highest Confidence / Authoritative Source / Most Complete / Custom | **Core MDM decision** — the conflict resolution strategy |
| `enabled` | Check | `1` | Enable/disable rule | Active/inactive control |
| `is_default` | Check | `0` | Default rule for Golden Record merges | Fallback rule when no specific rule is assigned |

#### Configurable Fields — Rule Scope

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `applies_to` | Select (required) | `All Fields` | All Fields / Specific Fields / Field Pattern / Field Groups | Determines which fields this rule governs |
| `specific_fields` | Small Text | — | Comma-separated field names (depends on `applies_to == 'Specific Fields'`) | Per-field rule assignment |
| `field_pattern` | Data | — | Regex pattern for field name matching (depends on `applies_to == 'Field Pattern'`) | Pattern-based field targeting (e.g., `^attr_.*`) |
| `field_groups` | Small Text | — | Comma-separated attribute groups (depends on `applies_to == 'Field Groups'`) | Group-based rule assignment |

#### Configurable Fields — Source Priority Configuration

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `source_priorities` | Table → Source Priority Item | Priority ranking of source systems (lower rank = higher priority) | **Visible when rule_type = 'Source Priority'** — defines the system hierarchy |

#### Configurable Fields — Confidence Configuration

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `min_confidence_threshold` | Percent | `0` | Minimum confidence for a value to be considered | **Visible when rule_type = 'Highest Confidence'** — filters low-quality data |
| `prefer_manual_confidence` | Check | `0` | Manual confidence overrides source defaults | Allows stewards to override system scores |

#### Configurable Fields — Authoritative Source Configuration

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `authoritative_source` | Link → Source System | — | The source whose values always win (if available) | **Visible when rule_type = 'Authoritative Source'** — single system of record |
| `allow_fallback` | Check | `1` | Use other sources when authoritative has no value | Prevents empty fields when auth source is incomplete |
| `fallback_rule_type` | Select | — | Source Priority / Most Recent / Highest Confidence | Fallback strategy when authoritative source is empty |

#### Configurable Fields — Custom Rule Configuration

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `custom_method` | Data | Dotted path to custom Python method (e.g., `frappe_pim.mdm.custom_rules.my_rule`) | **Visible when rule_type = 'Custom'** — extensibility point |
| `custom_params` | JSON | Parameters to pass to the custom method | Custom rule configuration |

#### Configurable Fields — Tie-Breaker Configuration

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `tiebreaker_rule` | Select | `Most Recent` | Most Recent / First Encountered / Longest Value / Shortest Value / Alphabetical | How to break ties when values have equal priority/confidence |
| `prefer_non_empty` | Check | `1` | Empty/null values are always deprioritized | Ensures populated fields win over empty ones |
| `trim_whitespace` | Check | `1` | Trim whitespace when comparing values | Prevents whitespace-only values from winning |

#### Configurable Fields — Usage Statistics (Read-Only)

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `times_applied` | Int | Number of times rule has been applied | Rule usage monitoring |
| `last_applied_at` | Datetime | When rule was last used | Recency tracking |
| `fields_affected` | Int | Total fields determined by this rule | Impact measurement |
| `average_candidates` | Float | Average candidate values per field | Merge complexity metric |

**Field-Level Survivorship Example:**

```
Scenario: Merging product data from 3 sources

Source Systems:
  ERP (priority: 1, confidence: 95%)  — authoritative for: weight, dimensions, price
  PIM (priority: 2, confidence: 90%)  — authoritative for: descriptions, marketing copy
  Import (priority: 3, confidence: 70%) — bulk data with lower confidence

Survivorship Rules:
  ├── "erp-authoritative" (Authoritative Source)
  │     applies_to: Specific Fields (weight, width, height, depth, list_price)
  │     authoritative_source: ERP
  │     allow_fallback: ✓ (falls back to Source Priority if ERP has no value)
  │
  ├── "content-most-complete" (Most Complete)
  │     applies_to: Field Groups (Marketing Content)
  │     tiebreaker: Longest Value (prefer richer descriptions)
  │
  └── "default-source-priority" (Source Priority, is_default: ✓)
        applies_to: All Fields
        source_priorities: ERP (1) → PIM (2) → Import (3)
        prefer_non_empty: ✓

Result for Product "Widget X":
  product_name:      "Widget X Pro"      ← ERP (Source Priority, rank 1)
  short_description: "Premium widget..." ← PIM (Most Complete, longest)
  weight:            2.5 kg              ← ERP (Authoritative Source)
  color:             "Blue"              ← ERP (Source Priority, rank 1)
  care_instructions: "Hand wash..."      ← Import (only source with value, prefer_non_empty)
```

### 15.5 Data Steward

**DocType:** `Data Steward`
**Module:** PIM
**Purpose:** Defines data stewardship assignments for human governance of product data quality. Data stewards are responsible for specific domains of product data and have defined capabilities and responsibilities.

#### Configurable Fields — Basic Information

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `steward` | Link → User (required) | — | User assigned as data steward | Maps Frappe user to stewardship role |
| `steward_name` | Data (read-only, fetched) | — | Full name from User | Display convenience |
| `role` | Select | — | Data Owner / Custodian / Quality Analyst / Domain Expert / Approver | Defines steward's level of authority |
| `status` | Select | `Active` | Active / Inactive / On Leave / Expired | Availability status |

#### Configurable Fields — Stewardship Domain

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `domain` | Select | — | Product Family / Brand / Channel / Attribute Group / All Products | **Scope of responsibility** — what data this steward governs |
| `domain_value` | Dynamic Link | — | Specific domain entity (e.g., "Electronics" Product Family) | Narrows scope to specific family/brand/channel |
| `include_children` | Check | `0` | Apply to child categories (for Product Family trees) | Extends scope to family sub-tree |
| `priority` | Int | `5` | Priority 1-10 for conflict resolution between stewards | Resolves overlapping steward assignments |

**Steward Roles Explained:**

| Role | Authority Level | Typical Responsibilities |
|------|----------------|------------------------|
| **Data Owner** | Highest | Strategic decisions about data standards, defines rules |
| **Approver** | High | Approves changes, publishes products, merges records |
| **Domain Expert** | Medium | Verifies domain-specific data accuracy |
| **Custodian** | Medium | Day-to-day data maintenance and enrichment |
| **Quality Analyst** | Focused | Reviews quality scores, identifies issues, runs audits |

#### Configurable Fields — Responsibilities (Permissions)

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `can_approve` | Check | `0` | Can approve pending changes & enrichment | Controls approval authority |
| `can_publish` | Check | `0` | Can publish products to channels | Controls publication authority |
| `can_merge` | Check | `0` | Can merge duplicate records | Controls golden record merge authority |
| `can_delete` | Check | `0` | Can delete products in domain | Controls deletion authority |
| `can_assign_stewards` | Check | `0` | Can assign other stewards | Delegation authority |
| `receives_notifications` | Check | `1` | Gets notifications for domain changes | Automated alerting |

#### Configurable Fields — Validity & Escalation

| Field | Type | Default | Purpose | Per-Customer Impact |
|-------|------|---------|---------|-------------------|
| `valid_from` | Date | Today | Start of stewardship | Role activation date |
| `valid_until` | Date | — (blank = permanent) | End of stewardship | Temporary assignments |
| `backup_steward` | Link → Data Steward | — | User to assume during absence | Ensures continuity |
| `escalation_to` | Link → Data Steward | — | User to escalate unresolved issues | Escalation path |

#### Configurable Fields — Performance Metrics (Read-Only)

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `products_in_domain` | Int | Number of products under stewardship | Workload measurement |
| `pending_approvals` | Int | Items pending approval | Backlog tracking |
| `avg_quality_score` | Percent | Average data quality score in domain | Quality KPI |
| `last_activity` | Datetime | Last stewardship activity | Activity monitoring |

**When to Configure:** Phase 2-3 — after product families and user roles are set up
**Who Configures:** PIM Manager or System Manager
**Business Impact:** Ensures accountability for data quality; without stewards, data governance is informal and error-prone

### 15.6 Merge & Survivorship Service (`merge_survive.py`)

**Module:** `frappe_pim.pim.services.merge_survive`
**Purpose:** The execution engine for MDM merge operations. This service applies survivorship rules to resolve field-level conflicts when merging product records from multiple sources into a Golden Record.

#### Key Functions

| Function | Purpose | Arguments |
|----------|---------|-----------|
| `merge_records()` | Execute a merge of source records into a golden record | `golden_record_name`, `source_products`, `survivorship_rule` |
| `apply_survivorship()` | Apply a survivorship rule to determine winning values | `candidates`, `rule`, `field_name` |
| `calculate_confidence()` | Calculate confidence scores for merged fields | `golden_record`, `field_sources` |
| `create_merge_event()` | Record a merge event for audit trail (event sourcing) | `golden_record`, `action`, `details` |

#### Merge Flow

```
┌────────────┐     ┌─────────────────┐     ┌──────────────────┐
│ Identify   │────▶│ Load Source      │────▶│ Apply            │
│ Duplicate  │     │ Records          │     │ Survivorship     │
│ Candidates │     │                  │     │ Rules            │
└────────────┘     └─────────────────┘     └──────────────────┘
                                                     │
                                                     ▼
┌────────────┐     ┌─────────────────┐     ┌──────────────────┐
│ Update     │◀────│ Record Merge    │◀────│ Resolve          │
│ Product    │     │ Event (Audit)   │     │ Conflicts        │
│ Master     │     │                 │     │ (Per Field)      │
└────────────┘     └─────────────────┘     └──────────────────┘
```

**Merge Process Steps:**

1. **Identify Candidates** — Find potential duplicate products via matching rules
2. **Load Source Records** — Fetch all source product data from Golden Record Source entries
3. **Apply Survivorship Rules** — For each field, apply the applicable survivorship rule:
   - Check if a field-specific rule exists (Specific Fields / Field Pattern / Field Groups)
   - If not, use the default survivorship rule
4. **Resolve Conflicts** — Use tie-breaker rules when values have equal priority
5. **Record Merge Event** — Create event-sourced audit entry with full before/after data
6. **Update Product Master** — Write winning values to the canonical Product Master

#### Event Sourcing

All merge operations are recorded as immutable events, providing a complete audit trail:

```python
# Example merge event structure (stored in merge history)
{
    "event_type": "merge",
    "timestamp": "2026-02-15T14:30:00Z",
    "golden_record": "GR-001",
    "action": "merge_records",
    "sources": ["PROD-001", "PROD-002", "PROD-003"],
    "survivorship_rule": "default-source-priority",
    "field_results": {
        "product_name": {
            "winner": "PROD-001",
            "source_system": "ERP",
            "value": "Widget X Pro",
            "rule_applied": "Source Priority",
            "confidence": 98.5,
            "candidates": [
                {"product": "PROD-001", "value": "Widget X Pro", "source": "ERP"},
                {"product": "PROD-002", "value": "Widget X", "source": "Import"},
                {"product": "PROD-003", "value": "Widget-X", "source": "API"}
            ]
        },
        "weight": {
            "winner": "PROD-001",
            "source_system": "ERP",
            "value": 2.5,
            "rule_applied": "Authoritative Source",
            "confidence": 99.9
        }
    },
    "performed_by": "steward@example.com",
    "merge_mode": "Automatic"
}
```

### 15.7 MDM Background Tasks (`mdm_tasks.py`)

**Module:** `frappe_pim.pim.tasks.mdm_tasks`
**Purpose:** Background task scheduler for automated MDM operations.

| Task | Schedule | Purpose |
|------|----------|---------|
| Auto-merge candidates | Configurable | Merge records above auto_merge_threshold |
| Validation refresh | Daily | Re-validate golden records for data quality |
| Confidence recalculation | After sync | Update confidence scores after source sync |
| Steward notifications | Real-time | Notify stewards of pending approvals |
| Stale record cleanup | Weekly | Archive inactive golden records |

### 15.8 Customer Archetype Examples — MDM

#### Fashion Retailer (Product data from ERP + supplier feeds)

```
Source Systems:
  ├── ERPNext (system_type: ERP, priority: 1, confidence: 95%)
  │     Authoritative for: SKU, price, stock, weight
  │     sync_direction: Bidirectional
  │     sync_frequency: Real-time
  │
  ├── Supplier Data Feed (system_type: Supplier Portal, priority: 3, confidence: 70%)
  │     Provides: Product descriptions, images, material info
  │     sync_direction: Inbound
  │     sync_frequency: Weekly
  │
  └── PIM Manual Entry (system_type: PIM, priority: 2, confidence: 90%)
        Authoritative for: Marketing descriptions, SEO content
        sync_direction: Outbound
        sync_frequency: Real-time

Survivorship Rules:
  ├── "erp-master" (Authoritative Source, ERP)
  │     Scope: price, stock_qty, weight, dimensions
  │     Fallback: Most Recent
  │
  ├── "content-best" (Most Complete)
  │     Scope: Field Group = Marketing Content
  │     Tiebreaker: Longest Value
  │
  └── "default" (Source Priority, is_default: ✓)
        Order: ERP (1) → PIM (2) → Supplier (3)

Data Stewards:
  ├── Product Manager → domain: All Products, role: Data Owner
  │     can_approve: ✓, can_publish: ✓, can_merge: ✓
  │
  ├── Content Writer → domain: Attribute Group = Marketing, role: Custodian
  │     can_approve: ✗, can_publish: ✗
  │
  └── Category Manager → domain: Product Family = Apparel, role: Approver
        can_approve: ✓, can_publish: ✓, include_children: ✓
```

#### Industrial Supplier (Multi-ERP consolidation)

```
Source Systems:
  ├── SAP ERP (system_type: ERP, priority: 1, confidence: 98%)
  │     Authoritative for: Part number, technical specs, price
  │     sync_direction: Bidirectional
  │     connection_type: REST API
  │
  ├── Legacy Oracle DB (system_type: ERP, priority: 2, confidence: 85%)
  │     Provides: Historical product data, alternate part numbers
  │     sync_direction: Inbound
  │     connection_type: Database
  │
  ├── Supplier Catalogs (system_type: Data Pool, priority: 4, confidence: 60%)
  │     Provides: Descriptions, images, certifications
  │     sync_direction: Inbound
  │     connection_type: File Import
  │
  └── PIM (system_type: PIM, priority: 3, confidence: 92%)
        Authoritative for: Enriched descriptions, channel-ready content
        sync_direction: Outbound

Survivorship Rules:
  ├── "sap-technical" (Authoritative Source, SAP)
  │     Scope: Field Pattern = ^(part_number|tolerance|tensile|din_|iso_)
  │     allow_fallback: ✓ (fallback: Source Priority)
  │
  ├── "specs-highest-confidence" (Highest Confidence)
  │     Scope: Field Group = Technical Specifications
  │     min_confidence_threshold: 80%
  │
  └── "default" (Source Priority, is_default: ✓)
        Order: SAP (1) → Oracle (2) → PIM (3) → Supplier (4)

Golden Record Configuration:
  merge_mode: Manual Review Required  (industrial parts need human verification)
  auto_merge_threshold: 98%           (only auto-merge near-perfect matches)
```

#### Food Manufacturer (Regulatory data + supply chain)

```
Source Systems:
  ├── ERP (priority: 1, confidence: 95%)
  │     Authoritative for: Weight, ingredients, nutritional values
  │
  ├── Regulatory System (priority: 1, confidence: 99%)
  │     Authoritative for: Allergen statements, health claims
  │     Note: Same priority as ERP — different field scope
  │
  ├── GDSN Data Pool (priority: 2, confidence: 88%)
  │     Provides: Standardized product data for retailer sync
  │
  └── PIM (priority: 3, confidence: 90%)
        Authoritative for: Marketing content, recipe cards

Survivorship Rules:
  ├── "regulatory-mandatory" (Authoritative Source, Regulatory)
  │     Scope: Specific Fields (allergen_statement, health_claims,
  │            ingredients_list, nutritional_info)
  │     allow_fallback: ✗  ← CRITICAL: NO fallback for regulatory data
  │
  ├── "weight-erp" (Authoritative Source, ERP)
  │     Scope: Specific Fields (net_weight, gross_weight, drained_weight)
  │
  └── "default" (Source Priority)
        Order: Regulatory (1) → ERP (2) → GDSN (3) → PIM (4)

Data Stewards:
  ├── Regulatory Affairs → domain: Attribute Group = Regulatory, role: Data Owner
  │     can_approve: ✓, can_merge: ✓, can_delete: ✗
  │     Note: Regulatory steward CANNOT delete — only archive
  │
  └── Quality Manager → domain: All Products, role: Quality Analyst
        can_approve: ✓, receives_notifications: ✓
        escalation_to: Regulatory Affairs steward
```

### 15.9 Onboarding Checklist — MDM

```
Phase 1 — Source System Registration:
  □ Inventory all systems that provide product data
  □ For each source system:
    □ Create Source System record with system_code and system_type
    □ Set connection_type and base_url (if applicable)
    □ Assign default_confidence based on data quality assessment
    □ Set priority (1 = highest) relative to other sources
    □ Configure sync_direction and sync_frequency
    □ Define field_mapping JSON for external-to-PIM field translation

Phase 2 — Survivorship Rule Definition:
  □ Identify field-level authority ("who owns which data?")
  □ Create survivorship rules:
    □ At minimum: one default rule (is_default: ✓) with Source Priority
    □ Per authoritative system: rules for fields they "own"
    □ Per field group: rules for marketing, technical, regulatory content
  □ Set tie-breaker preferences (Most Recent is safest default)
  □ Enable prefer_non_empty on all rules (prevents empty values winning)
  □ If custom logic needed: implement Custom rule type with custom_method

Phase 3 — Data Steward Assignment:
  □ Identify data governance stakeholders
  □ For each steward:
    □ Create Data Steward record linked to Frappe User
    □ Assign role (Data Owner, Approver, Custodian, etc.)
    □ Define domain scope (Product Family, Brand, Channel, etc.)
    □ Set responsibility checkboxes (can_approve, can_publish, can_merge, etc.)
    □ Set validity period (valid_from, valid_until if temporary)
    □ Assign backup_steward for coverage
    □ Configure escalation_to for unresolved issues
  □ Verify no domain gaps (every product family has a steward)

Phase 4 — Golden Record Creation:
  □ For each canonical product:
    □ Create Golden Record with product_master link
    □ Add source records via Golden Record Source child table
    □ Assign survivorship_rule or use default
    □ Set merge_mode (Automatic for clean data, Manual Review for uncertain)
    □ Set auto_merge_threshold (95% recommended starting point)
    □ Assign data_steward
  □ Run initial merge for existing products
  □ Review field_sources and field_confidence for accuracy

Phase 5 — Automation Setup:
  □ Configure MDM background tasks schedule
  □ Enable auto-merge for high-confidence matches
  □ Set up steward notifications (receives_notifications: ✓)
  □ Test merge flow end-to-end:
    □ Import data from multiple sources
    □ Verify survivorship rules produce correct winners
    □ Check event sourcing audit trail
    □ Confirm steward notification delivery
  □ Document custom survivorship rules for future reference

Phase 6 — Ongoing Governance:
  □ Monitor Data Steward performance metrics (avg_quality_score, pending_approvals)
  □ Review Survivorship Rule statistics (times_applied, fields_affected)
  □ Audit golden record validation_status for issues
  □ Periodically review and adjust source system confidence scores
  □ Archive obsolete golden records (status → Archived)
```

---

## Appendix A: Additional Configurable Entities

This appendix catalogs all remaining customizable DocTypes not covered in the main domain sections (1–15). These entities span product data, pricing, competitive intelligence, compliance templates, partner collaboration, and branding. Each is documented with its full field reference, customization impact, and onboarding context.

> **Implementation Status Legend:**
> - ✅ **Implemented** — DocType JSON exists in the codebase with full field definitions
> - 🔧 **Planned** — Documented in architecture specs; DocType not yet created

---

### A.1 Product Master — Complete Field Reference

**DocType:** `Product Master`
**Module:** PIM
**Naming Rule:** `field:product_code`
**Status:** ✅ Implemented
**Allow Rename:** No
**Track Changes:** Yes
**Image Field:** `main_image`

The Product Master is the **primary content entity** in the PIM — the record where all product information converges. It is referenced throughout sections 1–15 in context of type system binding, attribute values, channel publishing, scoring, and ERP sync. This appendix provides the **complete field structure** as defined in the DocType JSON.

#### Field Structure (9 Sections)

**Section 1 — Header (Identity)**

| Field | Type | Required | List View | Filter | Translatable | Purpose |
|-------|------|----------|-----------|--------|--------------|---------|
| `product_name` | Data | ✓ | ✓ | ✓ | ✓ | Display name — customer-facing product title |
| `product_code` | Data | ✓ | ✓ | — | — | Unique identifier (auto-generated or manual); used as document `name` |
| `product_family` | Link → Product Family | ✓ | ✓ | ✓ | — | Determines attribute template, variant axes, completeness thresholds |
| `status` | Select | — | ✓ | ✓ | — | Lifecycle state: `Draft`, `In Review`, `Approved`, `Published`, `End of Life`, `Archived` |

**Section 2 — Basic Information**

| Field | Type | Required | Filter | Purpose |
|-------|------|----------|--------|---------|
| `brand` | Link → Brand | — | ✓ | Brand association (see [A.5 Brand](#a5-brand)) |
| `manufacturer` | Link → Manufacturer | — | — | Manufacturer association (see [A.6 Manufacturer](#a6-manufacturer)) |
| `main_image` | Attach Image | — | — | Primary product image (used as DocType `image_field`) |

**Section 3 — Descriptions**

| Field | Type | Translatable | Purpose |
|-------|------|--------------|---------|
| `short_description` | Small Text | ✓ | Brief summary for listings (recommended max 160 chars for SEO) |
| `long_description` | Text Editor | ✓ | Full product description with HTML formatting |

**Section 4 — Dynamic Attributes (EAV)**

| Field | Type | Options | Purpose |
|-------|------|---------|---------|
| `attribute_values` | Table | Product Attribute Value | Dynamic attribute values — structure determined by Product Family's attribute template (see Section 2) |

**Section 5 — Media Gallery**

| Field | Type | Options | Purpose |
|-------|------|---------|---------|
| `media` | Table | Product Media | Product images, videos, documents — per-variant and per-locale (see Section 11) |

**Section 6 — Product Relations**

| Field | Type | Options | Purpose |
|-------|------|---------|---------|
| `relations` | Table | Product Relation | Cross-sell, up-sell, accessories, spare parts links between products |

**Section 7 — Channel Assignment**

| Field | Type | Options | Purpose |
|-------|------|---------|---------|
| `channels` | Table MultiSelect | Product Channel | Channel publishing targets (see Section 4) |

**Section 8 — Data Quality (Read-Only)**

| Field | Type | Read-Only | Purpose |
|-------|------|-----------|---------|
| `completeness_score` | Percent | ✓ | Auto-calculated completeness percentage (see Section 6) |
| `missing_attributes` | Small Text | ✓ | List of required but unfilled attributes |
| `quality_issues` | Small Text | ✓ | Active data quality issues |
| `last_enrichment_date` | Datetime | ✓ | Timestamp of last AI enrichment |

**Section 9 — ERP Integration (Collapsible)**

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `erp_item` | Link → Item | — | Linked ERPNext Item (template-level) |
| `auto_sync_to_erp` | Check | `1` | Enable automatic synchronization to ERPNext on save |

**Section 10 — Metadata (Collapsible)**

| Field | Type | Read-Only | Purpose |
|-------|------|-----------|---------|
| `created_by_import` | Check | ✓ | Flag indicating product was created via data import |
| `source_system` | Data | ✓ | Originating system identifier (for MDM, see Section 15) |
| `external_id` | Data | — | External system ID for cross-reference mapping |

#### Permissions Matrix

| Role | Read | Write | Create | Delete | Export | Import |
|------|------|-------|--------|--------|--------|--------|
| System Manager | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PIM Manager | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PIM User | ✓ | ✓ | ✓ | — | ✓ | — |

#### Customization Impact

- **Product Family selection** is the single most important decision per product — it determines the entire attribute structure, variant axes, and completeness calculation
- **Status field** options are fixed in the DocType (`Draft`, `In Review`, `Approved`, `Published`, `End of Life`, `Archived`) — extending lifecycle states requires DocType customization
- **Channel assignment** via `channels` Table MultiSelect determines which marketplaces receive the product data
- **auto_sync_to_erp** defaults to enabled — disable per-product for staged ERP rollouts

**When to Configure:** Product Masters are created during Phase 4 of onboarding (after families, attributes, and channels are set up)
**Who Configures:** PIM User (creation), PIM Manager (approval/publishing)

---

### A.2 Product Variant — SKU-Level Configuration

**DocType:** `Product Variant`
**Module:** PIM
**Naming Rule:** `field:variant_code`
**Status:** ✅ Implemented
**Allow Rename:** No
**Track Changes:** Yes

Product Variants represent individual SKUs within a Product Master. The variant system supports up to **4 distinguishing option axes** (e.g., Size, Color, Material, Width), with each axis linked to a PIM Attribute.

#### Field Structure (9 Sections)

**Section 1 — Identity**

| Field | Type | Required | Unique | Translatable | Purpose |
|-------|------|----------|--------|--------------|---------|
| `variant_name` | Data | ✓ | — | ✓ | Display name for the variant |
| `variant_code` | Data | ✓ | ✓ | — | Unique SKU code (used as document `name`) |
| `product_master` | Link → Product Master | ✓ | — | — | Parent product |
| `product_family` | Link → Product Family | — | — | — | Read-only, fetched from Product Master |
| `status` | Select | — | — | — | `Draft`, `Active`, `Inactive`, `Archived` |

**Section 2 — Variant Options (Up to 4 Axes)**

| Field | Type | Purpose |
|-------|------|---------|
| `option_1_attribute` | Link → PIM Attribute | First distinguishing axis (e.g., Size) |
| `option_1_value` | Data | Value for axis 1 (e.g., "XL") |
| `option_2_attribute` | Link → PIM Attribute | Second axis (e.g., Color) |
| `option_2_value` | Data | Value for axis 2 (e.g., "Navy Blue") |
| `option_3_attribute` | Link → PIM Attribute | Third axis (optional, collapsible) |
| `option_3_value` | Data | Value for axis 3 |
| `option_4_attribute` | Link → PIM Attribute | Fourth axis (optional, collapsible) |
| `option_4_value` | Data | Value for axis 4 |

> **Collapsible behavior:** Section "Additional Options" (axes 3–4) collapses automatically when `option_3_attribute` and `option_4_attribute` are empty, reducing form clutter for simple 1–2 axis products.

**Section 3 — Inventory & Pricing**

| Field | Type | Precision | Purpose |
|-------|------|-----------|---------|
| `barcode` | Data | — | EAN/UPC barcode for the variant |
| `stock_quantity` | Int | — | Current stock quantity (default: 0) |
| `weight` | Float | 3 | Weight in kilograms |
| `price` | Currency | — | Selling price |
| `cost_price` | Currency | — | Cost price |

**Section 4 — Dimensions (Collapsible)**

| Field | Type | Precision | Read-Only | Purpose |
|-------|------|-----------|-----------|---------|
| `length` | Float | 2 | — | Length in centimeters |
| `width` | Float | 2 | — | Width in centimeters |
| `height` | Float | 2 | — | Height in centimeters |
| `volume` | Float | 2 | ✓ | Calculated volume (L × W × H) |

**Section 5 — Attribute Values (EAV)**

| Field | Type | Options | Purpose |
|-------|------|---------|---------|
| `attribute_values` | Table | Product Attribute Value | Dynamic attribute values (same EAV pattern as Product Master) |

**Section 6 — Media (Collapsible)**

| Field | Type | Options | Purpose |
|-------|------|---------|---------|
| `image` | Attach Image | — | Primary variant image |
| `media` | Table | Product Media | Additional images and media files |

**Section 7 — ERP Integration (Collapsible)**

| Field | Type | Default | Read-Only | Purpose |
|-------|------|---------|-----------|---------|
| `erp_item` | Link → Item | — | ✓ | Linked ERPNext Item (auto-synced) |
| `sync_to_erp` | Check | `1` | — | Enable automatic ERP sync |
| `last_erp_sync` | Datetime | — | ✓ | Timestamp of last sync |
| `erp_sync_status` | Select | `Not Synced` | ✓ | `Not Synced`, `Synced`, `Sync Failed`, `Pending` |

**Section 8 — Data Quality**

| Field | Type | Read-Only | Purpose |
|-------|------|-----------|---------|
| `completeness_score` | Percent | ✓ | Percentage of required attributes filled |
| `missing_attributes` | Small Text | ✓ | List of unfilled required attributes |
| `last_completeness_check` | Datetime | ✓ | Timestamp of last completeness calculation |
| `is_complete` | Check | ✓ | Boolean flag: all required attributes filled |

**Section 9 — Notes (Collapsible)**

| Field | Type | Purpose |
|-------|------|---------|
| `internal_notes` | Text Editor | Internal notes (not exported to channels) |

#### Permissions Matrix

| Role | Read | Write | Create | Delete | Export | Import |
|------|------|-------|--------|--------|--------|--------|
| System Manager | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PIM Manager | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PIM User | ✓ | ✓ | ✓ | — | — | — |

#### Variant Generation Engine (`variant_generator.py`)

The variant generator provides automated SKU creation from Product Master and family-defined variant axes.

**Key Functions:**

| Function | Purpose |
|----------|---------|
| `generate_variants()` | Create variants from axis attribute option combinations |
| `generate_sku()` | Generate SKU codes from configurable patterns |
| `preview_variant_combinations()` | Preview without creating — for validation |
| `bulk_generate_variants()` | Batch creation across multiple Product Masters |
| `validate_variant_combination()` | Check uniqueness of attribute combinations |
| `delete_variants_for_master()` | Remove all variants for a Product Master |

**SKU Pattern Placeholders:**

| Placeholder | Resolves To | Example |
|-------------|-------------|---------|
| `{master}` | Product Master code | `TSH-001` |
| `{master_name}` | Product Master name | `Basic Tee` |
| `{idx}` | Sequential index | `001`, `002`, ... |
| `{uuid}` | Unique identifier | `a1b2c3d4` |
| `{attribute_name}` | Attribute value | `{color}` → `navy` |

**Configuration Constraints:**
- Maximum **4 axis attributes** per variant generation
- SKU segment normalization: max 10 characters per segment, alphanumeric + hyphens only
- `skip_existing` flag prevents duplicate variant creation
- `inherit_attributes` flag copies non-axis attributes from parent Product Master

**When to Configure:** After Product Family variant attributes are defined (Phase 3 of onboarding)
**Who Configures:** PIM Manager (generation rules), PIM User (individual variants)

---

### A.3 Product Series

**DocType:** `Product Series`
**Status:** 🔧 Planned

Product Series groups related products into a named collection that spans a single product line or generation. Unlike Product Collections (which are merchandising-focused), Product Series represents a manufacturing/design lineage.

**Planned Customization Points:**

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `series_name` | Data | Display name (e.g., "Galaxy S24", "iPhone 16") | Customer product taxonomy |
| `series_code` | Data | Unique identifier slug | Internal reference |
| `brand` | Link → Brand | Brand for the series | Brand-specific grouping |
| `year` / `season` | Data / Select | Release period | Fashion/seasonal businesses |
| `products` | Table → Product Master | Products in this series | Group membership |
| `is_active` | Check | Active/inactive toggle | Lifecycle management |

**Customer Archetype Examples:**

- **Fashion Retailer:** Series per season/collection — "Spring 2026", "FW26 Premium"
- **Electronics:** Series per product generation — "Galaxy S24", "ThinkPad T16 Gen 3"
- **Automotive:** Series per model year — "Corolla 2026", "Model 3 Highland"

**When to Configure:** Phase 4 — after Product Masters are created
**Who Configures:** PIM Manager

---

### A.4 Product Collection

**DocType:** `Product Collection`
**Status:** 🔧 Planned

Product Collections provide **merchandising-focused groupings** — curated sets of products for marketing campaigns, seasonal promotions, or thematic displays. Collections differ from families (structural) and series (lineage) by being ephemeral and marketing-driven.

**Planned Customization Points:**

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `collection_name` | Data | Display name | Campaign-specific naming |
| `collection_code` | Data | Unique identifier | URL slugs, API references |
| `collection_type` | Select | Manual / Dynamic (rule-based) | Automation level |
| `start_date` / `end_date` | Date | Active period | Seasonal/campaign windows |
| `products` | Table → Product Master | Included products | Manual curation |
| `dynamic_rules` | JSON | Auto-populate rules (by family, brand, attribute) | Dynamic collection logic |
| `cover_image` | Attach Image | Collection cover image | Marketing assets |
| `description` | Text Editor | Collection description | Customer-facing content |

**When to Configure:** Ongoing — as marketing campaigns arise
**Who Configures:** PIM Manager or Marketing team

---

### A.5 Brand

**DocType:** `Brand`
**Module:** PIM
**Naming Rule:** `field:brand_code`
**Status:** ✅ Implemented
**Allow Rename:** Yes
**Track Changes:** Yes
**Sort:** `brand_name ASC`

Brand is a standalone reference entity linked from Product Master. It provides brand identity information for channel publishing, export profiles, and filtering.

#### Complete Field Reference

| Field | Type | Required | Unique | Translatable | Purpose |
|-------|------|----------|--------|--------------|---------|
| `brand_name` | Data | ✓ | — | ✓ | Display name (translatable for multi-locale deployments) |
| `brand_code` | Data | ✓ | ✓ | — | Unique slug identifier (e.g., `nike`, `apple`, `samsung`) |
| `enabled` | Check | — | — | — | Enable/disable toggle (default: enabled) |
| `logo` | Attach Image | — | — | — | Brand logo image |
| `website` | Data (URL) | — | — | — | Brand website URL |
| `description` | Text Editor | — | — | — | Detailed brand description |

#### Permissions Matrix

| Role | Read | Write | Create | Delete | Export | Import |
|------|------|-------|--------|--------|--------|--------|
| System Manager | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PIM Manager | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PIM User | ✓ | — | — | — | — | — |

> **Note:** PIM Users have **read-only** access to brands — only PIM Managers can create or modify brand records.

**When to Configure:** Phase 2 — before creating Product Masters
**Who Configures:** PIM Manager
**Business Impact:** Brands appear on product forms, channel exports, and data quality policies. Incorrect brand setup leads to misattributed products across all channels.

---

### A.6 Manufacturer

**DocType:** `Manufacturer`
**Module:** PIM
**Naming Rule:** `field:manufacturer_code`
**Status:** ✅ Implemented
**Allow Rename:** Yes
**Track Changes:** Yes
**Sort:** `manufacturer_name ASC`

Manufacturer records identify the physical producer of products, independent of brand. A single manufacturer may produce products for multiple brands (e.g., Foxconn manufactures for Apple, Dell, HP).

#### Complete Field Reference

| Field | Type | Required | Unique | Translatable | Purpose |
|-------|------|----------|--------|--------------|---------|
| `manufacturer_name` | Data | ✓ | — | ✓ | Display name |
| `manufacturer_code` | Data | ✓ | ✓ | — | Unique slug identifier (e.g., `foxconn`, `jabil`) |
| `enabled` | Check | — | — | — | Enable/disable toggle (default: enabled) |
| `logo` | Attach Image | — | — | — | Manufacturer logo |
| `website` | Data (URL) | — | — | — | Manufacturer website |
| `description` | Text Editor | — | — | — | Detailed manufacturer description |

#### Permissions Matrix

| Role | Read | Write | Create | Delete | Export | Import |
|------|------|-------|--------|--------|--------|--------|
| System Manager | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PIM Manager | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PIM User | ✓ | — | — | — | — | — |

**When to Configure:** Phase 2 — alongside brands, before Product Master creation
**Who Configures:** PIM Manager
**Business Impact:** Required for supply chain traceability; some channels (e.g., Amazon) require manufacturer information for product listings. Distinct from Brand when private-label/white-label products are involved.

---

### A.7 Price Rule

**DocType:** `Price Rule`
**Status:** 🔧 Planned

Price Rules define automated pricing adjustments based on conditions — discounts, promotions, tiered pricing, and channel-specific markups. The PIM's price resolution engine (`price_resolver.py`) supports a **7-layer priority system** that evaluates pricing rules in order.

#### Price Resolution Layers (Priority Order)

| Layer | Priority | Source | Purpose |
|-------|----------|--------|---------|
| 1 | Highest | Contract Price | Customer-specific negotiated pricing |
| 2 | High | Channel Listing Price | Marketplace-specific listing price |
| 3 | Medium | Channel Price List | Channel's ERPNext price list |
| 4 | Low | Fallback Price List | System default price list |
| 5 | Applied | Currency Conversion | Convert to requested currency |
| 6 | Applied | Pricing Rules | Discounts, promotions, tiered pricing |
| 7 | Applied | Guardrails | Min/max price enforcement, MAP compliance |

**Planned Customization Points:**

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `rule_name` | Data | Display name | Rule identification |
| `rule_type` | Select | Discount / Markup / Fixed / Tiered | Pricing strategy |
| `apply_on` | Select | Product / Family / Brand / Channel | Scope of rule |
| `discount_percentage` | Percent | Percentage discount | Price reduction |
| `min_qty` / `max_qty` | Int | Quantity thresholds | Volume-based pricing |
| `valid_from` / `valid_to` | Date | Effective period | Seasonal promotions |
| `channel` | Link → Channel | Channel-specific pricing | Marketplace price differentiation |
| `priority` | Int | Rule evaluation order | Conflict resolution |

**Guardrail Configuration:**

| Guardrail | Purpose | Business Impact |
|-----------|---------|----------------|
| `min_price` | Floor price enforcement | Prevents below-cost sales |
| `max_price` | Ceiling price enforcement | Prevents pricing errors |
| `enforce_map` | Minimum Advertised Price | Legal compliance for MAP-protected brands |

**When to Configure:** Phase 5 — after products and channels are established
**Who Configures:** PIM Manager with pricing authority
**Business Impact:** Incorrect pricing rules can result in financial loss (below-cost sales) or legal issues (MAP violations)

---

### A.8 PIM Contract Price

**DocType:** `PIM Contract Price`
**Status:** 🔧 Planned

Contract Prices capture customer-specific negotiated pricing that overrides all other price resolution layers (Layer 1 — highest priority in the price resolver).

**Planned Customization Points:**

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `customer` | Link → Customer | ERPNext customer reference | Customer-specific pricing |
| `product` | Link → Product Master | Product reference | Per-product pricing |
| `variant` | Link → Product Variant | SKU-level pricing (optional) | SKU-specific overrides |
| `contract_price` | Currency | Negotiated price | Customer agreement |
| `currency` | Link → Currency | Price currency | Multi-currency support |
| `min_qty` | Int | Minimum order quantity | Volume commitment |
| `valid_from` / `valid_to` | Date | Contract period | Time-bound pricing |
| `contract_reference` | Data | Contract document number | Audit trail |

**When to Configure:** Per customer agreement (ongoing)
**Who Configures:** PIM Manager or Sales team
**Business Impact:** Enables B2B pricing differentiation; contract prices take absolute priority in the 7-layer resolution

---

### A.9 PIM Customer Segment & Target Segment

**DocType:** `PIM Customer Segment`
**Status:** 🔧 Planned

**DocType:** `Target Segment`
**Status:** 🔧 Planned

Customer Segments group end consumers or business customers into behavioral/demographic cohorts for targeted pricing, content personalization, and channel strategy.

**PIM Customer Segment — Planned Fields:**

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `segment_name` | Data | Display name (e.g., "Premium", "Value") | Customer targeting |
| `segment_code` | Data | Unique identifier | API references |
| `segment_type` | Select | B2B / B2C / Wholesale / Retail | Business model |
| `pricing_tier` | Link → Price Rule | Default pricing tier | Segment-based pricing |
| `channels` | Table MultiSelect | Preferred channels | Channel targeting |
| `description` | Text Editor | Segment description | Internal documentation |

**Target Segment — Planned Fields:**

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `segment` | Link → PIM Customer Segment | Segment reference | Segment binding |
| `product` | Link → Product Master | Product reference | Product-segment mapping |
| `priority` | Int | Targeting priority | Multi-segment ranking |

**When to Configure:** Phase 5 — after products and channels are established
**Who Configures:** PIM Manager or Marketing team

---

### A.10 Competitive Intelligence DocTypes

#### A.10.1 Competitor Analysis

**DocType:** `Competitor Analysis`
**Status:** 🔧 Planned

Tracks competitor pricing, positioning, and product information for market intelligence and pricing strategy.

**Planned Customization Points:**

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `competitor_name` | Data | Competitor identity | Market landscape mapping |
| `product` | Link → Product Master | Our equivalent product | Product-level competitive tracking |
| `competitor_product_name` | Data | Competitor's product name | Cross-reference |
| `competitor_price` | Currency | Competitor's price | Price benchmarking |
| `competitor_url` | Data (URL) | Product page URL | Monitoring source |
| `last_checked` | Datetime | Last monitoring timestamp | Data freshness |
| `price_position` | Select | Above / At / Below our price | Quick position assessment |
| `notes` | Text Editor | Analysis notes | Strategic insights |

#### A.10.2 Market Insight

**DocType:** `Market Insight`
**Status:** 🔧 Planned

Captures market-level intelligence about trends, demand signals, and category dynamics.

**Planned Customization Points:**

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `insight_title` | Data | Insight headline | Knowledge management |
| `insight_type` | Select | Trend / Demand / Competitor / Regulatory | Categorization |
| `product_family` | Link → Product Family | Affected product family | Scoped relevance |
| `channel` | Link → Channel | Relevant channel | Channel-specific insights |
| `impact_level` | Select | High / Medium / Low | Prioritization |
| `source` | Data | Information source | Credibility assessment |
| `valid_until` | Date | Insight expiry | Timeliness management |
| `description` | Text Editor | Full insight description | Detailed analysis |

#### A.10.3 Digital Shelf Snapshot

**DocType:** `Digital Shelf Snapshot`
**Status:** 🔧 Planned

Point-in-time captures of product visibility, positioning, and content quality across digital channels — the "digital shelf" analytics concept.

**Planned Customization Points:**

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `product` | Link → Product Master | Monitored product | Product-level tracking |
| `channel` | Link → Channel | Monitored channel | Per-channel visibility |
| `snapshot_date` | Date | Capture date | Trend tracking |
| `search_rank` | Int | Search result position | SEO/visibility KPI |
| `buy_box_winner` | Check | Owns the buy box (Amazon) | Revenue-critical metric |
| `content_score` | Percent | Content quality score | Quality benchmarking |
| `price_displayed` | Currency | Price shown to consumers | Price consistency audit |
| `reviews_count` | Int | Number of reviews | Social proof tracking |
| `average_rating` | Float | Average review rating | Reputation monitoring |
| `in_stock` | Check | Availability status | Inventory visibility |

**When to Configure (all competitive intelligence):** Phase 6 — after products are published to channels
**Who Configures:** PIM Manager or Market Intelligence team
**Business Impact:** Competitive intelligence drives pricing decisions, content optimization, and channel strategy adjustments

---

### A.11 Product Feedback

**DocType:** `Product Feedback`
**Status:** 🔧 Planned

Captures internal and external feedback about product data quality, content accuracy, and improvement suggestions. Integrates with the Data Quality scoring system (Section 6).

**Planned Customization Points:**

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `product` | Link → Product Master | Feedback target | Product-level tracking |
| `feedback_type` | Select | Quality Issue / Content Suggestion / Error Report / Enhancement | Categorization |
| `severity` | Select | Critical / High / Medium / Low | Prioritization |
| `reported_by` | Link → User | Person reporting | Accountability |
| `assigned_to` | Link → User | Assigned resolver | Workflow routing |
| `status` | Select | Open / In Progress / Resolved / Closed / Won't Fix | Lifecycle tracking |
| `field_name` | Data | Specific field with issue | Targeted correction |
| `current_value` | Text | Current incorrect value | Before/after comparison |
| `suggested_value` | Text | Proposed correction | Improvement proposal |
| `resolution_notes` | Text Editor | Resolution details | Knowledge base |

**When to Configure:** Ongoing — as products are reviewed and published
**Who Configures:** PIM User (creation), PIM Manager (resolution)

---

### A.12 Display & Output Templates

#### A.12.1 Display Template

**DocType:** `Display Template`
**Status:** 🔧 Planned

Display Templates define how product information is rendered for different output contexts — web pages, print catalogs, marketplace listings, and POS displays.

**Planned Customization Points:**

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `template_name` | Data | Template display name | Template management |
| `template_code` | Data | Unique identifier | API/programmatic reference |
| `output_type` | Select | Web / Print / Marketplace / POS / Email | Rendering context |
| `product_family` | Link → Product Family | Family-specific template | Family-tailored layouts |
| `channel` | Link → Channel | Channel-specific template | Channel-specific rendering |
| `template_html` | Code (HTML) | Jinja2/HTML template | Visual layout definition |
| `included_fields` | Table | Fields to include | Content selection |
| `css_styles` | Code (CSS) | Custom styling | Brand-consistent presentation |
| `is_default` | Check | Default for output type | Fallback template |

#### A.12.2 Datasheet Template

**DocType:** `Datasheet Template`
**Status:** 🔧 Planned

Datasheet Templates define the layout and content of printable/downloadable product datasheets — technical specification documents, product cards, or catalog pages.

**Planned Customization Points:**

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `template_name` | Data | Template display name | Template identification |
| `template_code` | Data | Unique identifier | Programmatic reference |
| `product_family` | Link → Product Family | Family-specific layout | Technical vs. consumer datasheets |
| `format` | Select | PDF / HTML / DOCX | Output format |
| `page_size` | Select | A4 / Letter / A3 | Print configuration |
| `orientation` | Select | Portrait / Landscape | Layout direction |
| `header_template` | Code (HTML) | Header Jinja2 template | Branding |
| `body_template` | Code (HTML) | Body Jinja2 template | Content layout |
| `footer_template` | Code (HTML) | Footer Jinja2 template | Legal/contact info |
| `include_qr_code` | Check | Embed product QR code | Quick digital access |
| `include_barcode` | Check | Embed barcode image | Logistics reference |
| `attribute_groups` | Table MultiSelect | Which attribute groups to include | Content scoping |

**When to Configure:** Phase 5 — after attribute system is fully configured
**Who Configures:** PIM Manager or Design team
**Business Impact:** Templates ensure consistent brand presentation across all output channels; different product families typically require different datasheet layouts

---

### A.13 Industry-Specific Compliance DocTypes

#### A.13.1 Nutrition Facts

**DocType:** `Nutrition Facts`
**Status:** 🔧 Planned

Captures standardized nutritional information for food and beverage products, supporting regulatory compliance across multiple jurisdictions (FDA, EU Regulation 1169/2011, Turkish Food Codex).

**Planned Customization Points:**

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `product` | Link → Product Master | Product reference | Product binding |
| `serving_size` | Data | Serving size description | Regulatory requirement |
| `servings_per_container` | Float | Number of servings | Pack size calculation |
| `calories` | Float | Energy (kcal) | Mandatory nutrition fact |
| `total_fat` | Float | Total fat (g) | Mandatory nutrition fact |
| `saturated_fat` | Float | Saturated fat (g) | Mandatory nutrition fact |
| `trans_fat` | Float | Trans fat (g) | Mandatory in some jurisdictions |
| `cholesterol` | Float | Cholesterol (mg) | Mandatory nutrition fact |
| `sodium` | Float | Sodium (mg) | Mandatory nutrition fact |
| `total_carbohydrates` | Float | Total carbs (g) | Mandatory nutrition fact |
| `dietary_fiber` | Float | Dietary fiber (g) | Mandatory nutrition fact |
| `total_sugars` | Float | Total sugars (g) | Mandatory nutrition fact |
| `added_sugars` | Float | Added sugars (g) | FDA requirement |
| `protein` | Float | Protein (g) | Mandatory nutrition fact |
| `vitamin_d` | Float | Vitamin D (mcg) | FDA requirement |
| `calcium` | Float | Calcium (mg) | Regulatory requirement |
| `iron` | Float | Iron (mg) | Regulatory requirement |
| `potassium` | Float | Potassium (mg) | FDA requirement |
| `allergens` | Text | Allergen statement | Critical regulatory field |
| `ingredients_list` | Text | Full ingredients list | Mandatory in all jurisdictions |
| `regulatory_standard` | Select | FDA / EU 1169/2011 / Codex | Jurisdiction selection |

**When to Configure:** Phase 3 — alongside attribute templates for food product families
**Who Configures:** Quality/Regulatory team
**Business Impact:** **Critical regulatory requirement** — missing or inaccurate nutrition facts can result in product recalls, fines, and legal liability

#### A.13.2 Chemical Usage Instruction

**DocType:** `Chemical Usage Instruction`
**Status:** 🔧 Planned

Safety and usage instructions for chemical, cleaning, or pharmaceutical products — supporting GHS (Globally Harmonized System), SDS (Safety Data Sheets), and CLP (Classification, Labelling, Packaging) compliance.

**Planned Customization Points:**

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `product` | Link → Product Master | Product reference | Product binding |
| `hazard_classification` | Select | GHS categories | Safety classification |
| `signal_word` | Select | Danger / Warning / None | Regulatory labeling |
| `hazard_statements` | Table | H-statements (GHS) | Hazard communication |
| `precautionary_statements` | Table | P-statements (GHS) | Safety instructions |
| `pictograms` | Table MultiSelect | GHS pictogram codes | Visual hazard symbols |
| `first_aid_instructions` | Text Editor | First aid measures | Emergency response |
| `storage_instructions` | Text Editor | Storage requirements | Handling guidelines |
| `disposal_instructions` | Text Editor | Disposal methods | Environmental compliance |
| `sds_document` | Attach | Safety Data Sheet (PDF) | Regulatory document |
| `cas_number` | Data | CAS Registry Number | Chemical identification |
| `un_number` | Data | UN transport number | Transport regulations |

**When to Configure:** Phase 3 — alongside attribute templates for chemical product families
**Who Configures:** Regulatory/Safety team
**Business Impact:** **Critical safety requirement** — GHS compliance is legally mandated for chemical products in most jurisdictions

---

### A.14 Social & Digital Presence

#### A.14.1 Social Media Link

**DocType:** `Social Media Link`
**Status:** 🔧 Planned

Links product or brand records to their social media presence across platforms — enabling social commerce tracking, influencer attribution, and content syndication.

**Planned Customization Points:**

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `parent_type` | Select | Product Master / Brand / Product Collection | Link scope |
| `parent` | Dynamic Link | Parent record reference | Flexible linking |
| `platform` | Select | Instagram / TikTok / Facebook / Pinterest / YouTube / X / LinkedIn | Platform selection |
| `profile_url` | Data (URL) | Profile/page URL | Social presence reference |
| `handle` | Data | Platform handle (@username) | Quick reference |
| `follower_count` | Int | Current followers | Reach metric |
| `is_verified` | Check | Verified account | Trust signal |

#### A.14.2 PIM Event

**DocType:** `PIM Event`
**Status:** 🔧 Planned

Tracks significant product lifecycle events — launches, discontinuations, recalls, price changes, and campaign activations — providing an event timeline for audit and analytics.

**Planned Customization Points:**

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `event_name` | Data | Event title | Event identification |
| `event_type` | Select | Launch / Discontinue / Recall / Price Change / Campaign / Seasonal | Event categorization |
| `event_date` | Date | Event date | Timeline tracking |
| `products` | Table → Product Master | Affected products | Scope definition |
| `channels` | Table MultiSelect | Affected channels | Channel targeting |
| `description` | Text Editor | Event details | Context documentation |
| `status` | Select | Planned / Active / Completed / Cancelled | Event lifecycle |
| `created_by` | Link → User | Event creator | Accountability |

**When to Configure:** Ongoing — as product lifecycle events occur
**Who Configures:** PIM Manager

---

### A.15 Partner Collaboration DocTypes

#### A.15.1 Partner Submission

**DocType:** `Partner Submission`
**Status:** 🔧 Planned

Enables external partners (suppliers, distributors, brand owners) to submit product data for review and ingestion into the PIM. Implements a review/approval workflow before data enters the main product catalog.

**Planned Customization Points:**

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `submission_title` | Data | Submission title | Identification |
| `partner` | Link → Brand Portal User | Submitting partner | Source tracking |
| `submission_type` | Select | New Product / Update / Bulk Upload | Submission categorization |
| `product_family` | Link → Product Family | Target product family | Structure alignment |
| `status` | Select | Submitted / Under Review / Approved / Rejected / Revision Required | Review workflow |
| `submitted_data` | JSON | Structured product data payload | Data ingestion |
| `review_notes` | Text Editor | Reviewer comments | Quality feedback |
| `reviewed_by` | Link → User | Approver | Accountability |
| `approved_product` | Link → Product Master | Created/updated product | Result tracking |
| `rejection_reason` | Text | Rejection explanation | Partner communication |

#### A.15.2 Brand Portal User

**DocType:** `Brand Portal User`
**Status:** 🔧 Planned

Manages external user access to the Brand Portal — a limited-access interface where brand owners, suppliers, and partners can submit product data, review published content, and access digital assets.

**Planned Customization Points:**

| Field | Type | Purpose | Per-Customer Impact |
|-------|------|---------|-------------------|
| `user` | Link → User | Frappe user reference | Authentication |
| `portal_role` | Select | Brand Owner / Supplier / Distributor / Reviewer | Access level |
| `brands` | Table MultiSelect → Brand | Accessible brands | Brand-scoped access |
| `product_families` | Table MultiSelect → Product Family | Accessible families | Family-scoped access |
| `can_submit_products` | Check | Permission to submit new products | Data submission |
| `can_view_analytics` | Check | Permission to view analytics | Reporting access |
| `can_download_assets` | Check | Permission to download media | Asset distribution |
| `max_submissions_per_month` | Int | Submission rate limit | Abuse prevention |
| `portal_language` | Link → Language | Preferred interface language | i18n personalization |
| `status` | Select | Active / Suspended / Pending Approval | Access lifecycle |

**When to Configure:** Phase 6 — after internal PIM is fully operational
**Who Configures:** PIM Manager or Partner Relations team
**Business Impact:** Partner collaboration portals significantly reduce manual data entry; proper access controls prevent unauthorized data modifications

---

### A.16 SEO Validation Engine (`seo_validator.py`)

While SEO fields are part of the Product Master attribute system, the SEO validation engine provides a configurable quality layer documented here for completeness.

**Validated SEO Fields:**

| Field | Required | Optimal Length | Scoring Weight |
|-------|----------|----------------|----------------|
| `seo_meta_title` | Yes | 30–60 characters | Component of quality grade |
| `seo_meta_description` | Yes | 120–160 characters | Component of quality grade |
| `seo_meta_keywords` | Yes | 3–10 keywords | Component of quality grade |
| `seo_canonical_url` | No | Valid HTTP/HTTPS URL | Component of quality grade |

**Quality Scoring Formula:**
- **60%** Completeness weight (are all SEO fields filled?)
- **40%** Quality weight (do values meet optimal length/format criteria?)

**Grade Scale:**
| Grade | Minimum Score | Assessment |
|-------|---------------|------------|
| A | 90+ | Excellent SEO |
| B | 80+ | Good SEO |
| C | 70+ | Acceptable |
| D | 60+ | Needs improvement |
| F | <60 | Poor — action required |

**Placeholder Detection:** The validator catches common placeholder values: `lorem ipsum`, `test`, `placeholder`, `tbd`, `n/a`, `xxx`, `todo`

**Key API Functions:**

| Function | Purpose |
|----------|---------|
| `validate_seo_fields()` | Doc event hook — runs on save |
| `get_seo_completeness()` | Quick completeness percentage |
| `check_seo_quality()` | Full quality grade (A–F) with breakdown |
| `get_seo_recommendations()` | Actionable improvement suggestions |
| `get_products_with_seo_issues()` | Find products with SEO problems |
| `generate_seo_report()` | CSV or dict SEO audit report |
| `bulk_check_seo()` | Multi-product validation |

**When to Configure:** Phase 4 — alongside product content creation
**Who Configures:** Content team or SEO specialist

---

### A.17 Summary: All DocTypes by Implementation Status

The following table provides a complete inventory of all DocTypes referenced in this appendix, their implementation status, and the section of the main guide where their primary customization context is documented.

#### Implemented DocTypes (✅)

| DocType | Naming Rule | Primary Section | Appendix Section |
|---------|-------------|-----------------|------------------|
| Product Master | `field:product_code` | Sections 1, 5, 6, 7 | A.1 |
| Product Variant | `field:variant_code` | Sections 1, 7 | A.2 |
| Brand | `field:brand_code` | Section 1 | A.5 |
| Manufacturer | `field:manufacturer_code` | Section 1 | A.6 |

#### Planned DocTypes (🔧)

| DocType | Category | Appendix Section |
|---------|----------|------------------|
| Product Series | Product Grouping | A.3 |
| Product Collection | Marketing/Merchandising | A.4 |
| Price Rule | Pricing | A.7 |
| PIM Contract Price | Pricing | A.8 |
| PIM Customer Segment | Segmentation | A.9 |
| Target Segment | Segmentation | A.9 |
| Competitor Analysis | Competitive Intelligence | A.10.1 |
| Market Insight | Competitive Intelligence | A.10.2 |
| Digital Shelf Snapshot | Competitive Intelligence | A.10.3 |
| Product Feedback | Quality Management | A.11 |
| Display Template | Output Templates | A.12.1 |
| Datasheet Template | Output Templates | A.12.2 |
| Nutrition Facts | Regulatory Compliance | A.13.1 |
| Chemical Usage Instruction | Regulatory Compliance | A.13.2 |
| Social Media Link | Digital Presence | A.14.1 |
| PIM Event | Product Lifecycle | A.14.2 |
| Partner Submission | Partner Collaboration | A.15.1 |
| Brand Portal User | Partner Collaboration | A.15.2 |

---

### A.18 Customer Archetype Examples — Additional Entities

#### Fashion Retailer — Additional Entity Configuration

```
Brands:
  ├── own-brand (brand_code: "own-brand", enabled: ✓)
  │     Products: 60% of catalog
  │     Brand Portal: N/A (internal)
  │
  ├── partner-brand-a (brand_code: "partner-a", enabled: ✓)
  │     Products: 25% of catalog
  │     Brand Portal User: partner-a@supplier.com
  │       portal_role: Brand Owner
  │       can_submit_products: ✓
  │       max_submissions_per_month: 50
  │
  └── partner-brand-b (brand_code: "partner-b", enabled: ✓)
        Products: 15% of catalog
        Brand Portal User: partner-b@supplier.com
          portal_role: Supplier
          can_submit_products: ✓
          can_download_assets: ✓

Product Collections:
  ├── "Summer Sale 2026" (collection_type: Manual, start: 2026-06-01, end: 2026-08-31)
  ├── "New Arrivals" (collection_type: Dynamic, rule: created_in_last_30_days)
  └── "Bestsellers" (collection_type: Dynamic, rule: top_50_by_sales)

Competitive Intelligence:
  ├── Competitor Analysis: Track top 3 competitors per product family
  ├── Digital Shelf Snapshots: Weekly for Amazon, Trendyol
  └── Market Insights: Seasonal trend reports per product family
```

#### Industrial Supplier — Additional Entity Configuration

```
Manufacturers:
  ├── manufacturer-a (manufacturer_code: "mfr-a", enabled: ✓)
  │     Products: 200+ components
  │     Website: https://manufacturer-a.com
  │
  ├── manufacturer-b (manufacturer_code: "mfr-b", enabled: ✓)
  │     Products: 150+ raw materials
  │
  └── manufacturer-c (manufacturer_code: "mfr-c", enabled: ✓)
        Products: 80+ assemblies

Chemical Usage Instructions:
  ├── Cleaning agents → GHS classification required
  │     hazard_classification: Category 2 (Eye Irritation)
  │     signal_word: Warning
  │     pictograms: GHS07 (Exclamation Mark)
  │     sds_document: Required for all chemical products
  │
  └── Lubricants → CLP compliance
        cas_number: Required
        storage_instructions: Mandatory
        disposal_instructions: Per local regulations

Datasheet Templates:
  ├── "Technical Datasheet" (format: PDF, A4 Portrait)
  │     Includes: Technical attributes, dimensions, certifications
  │     QR code: ✓, Barcode: ✓
  │
  └── "Safety Datasheet" (format: PDF, A4 Portrait)
        Includes: GHS data, first aid, storage, disposal
        Required for: Chemical product families
```

#### Food Manufacturer — Additional Entity Configuration

```
Nutrition Facts:
  ├── Regulatory standard: EU 1169/2011 (primary market)
  │     Required fields: All mandatory EU nutrients
  │     Allergen statement: MANDATORY (bolded allergens)
  │     Ingredients list: MANDATORY (descending order by weight)
  │
  ├── Secondary standard: FDA (US export)
  │     Additional fields: Added sugars, Vitamin D, Potassium
  │     Serving size format: US customary units
  │
  └── Turkish market: Turkish Food Codex
        Language: Turkish
        Additional requirements: Halal certification reference

Product Series:
  ├── "Organic Line" (brand: own-brand, year: 2026)
  ├── "Kids Range" (brand: own-brand, year: 2026)
  └── "Professional Chef" (brand: own-brand, year: 2025)

Display Templates:
  ├── "Product Card" (output_type: Web)
  │     Includes: Nutrition facts panel, allergen badges, organic logo
  │
  └── "Catalog Page" (output_type: Print, A4 Landscape)
        Includes: Product photo, nutrition table, ingredients, barcodes
```

---

## 16. Recommended Onboarding Configuration Sequence

### Overview

This section defines the **dependency-ordered configuration chain** for deploying Frappe PIM for a new customer. Each phase builds on the previous, and the ordering ensures that dependent entities (e.g., Product Master) are never configured before their prerequisites (e.g., Product Family, PIM Attribute).

> **Important:** This is the recommended sequence for **Greenfield deployments**. For migrations, see [Section 17: Edge Cases](#17-edge-cases--deployment-scenarios) for modifications to this sequence.

### Dependency Graph

```
Phase 0: PIM Settings (Global)
  │
  ├──▶ Phase 1: Foundation Schema
  │      ├── PIM Attribute Type
  │      ├── PIM Attribute Group
  │      ├── PIM Attribute + PIM Attribute Option
  │      └── Product Family + Family Attribute Template + Family Variant Attribute
  │              │
  │              ├──▶ Phase 2: Content Infrastructure
  │              │      ├── PIM Product Type
  │              │      ├── Category (NestedSet)
  │              │      ├── Taxonomy + Taxonomy Node
  │              │      ├── Brand
  │              │      └── Manufacturer
  │              │              │
  │              │              ├──▶ Phase 3: Quality & Governance
  │              │              │      ├── Data Quality Policy
  │              │              │      ├── Scoring Weights (PIM Settings)
  │              │              │      ├── Roles & Permissions
  │              │              │      ├── PIM Category Permission
  │              │              │      └── Data Steward
  │              │              │              │
  │              │              │              ├──▶ Phase 4: Channel & Export Setup
  │              │              │              │      ├── Channel (Sales Channels)
  │              │              │              │      ├── Export Profile
  │              │              │              │      ├── Channel Attribute Requirement
  │              │              │              │      └── Channel Locale
  │              │              │              │              │
  │              │              │              │              ├──▶ Phase 5: Advanced Features
  │              │              │              │              │      ├── AI Configuration (Providers, Prompts)
  │              │              │              │              │      ├── GS1 Packaging Hierarchy
  │              │              │              │              │      ├── PIM Bundle
  │              │              │              │              │      ├── Price Rule
  │              │              │              │              │      └── MDM (Source Systems, Survivorship)
  │              │              │              │              │
  │              │              │              │              └──▶ Phase 6: Content Creation
  │              │              │              │                     ├── Product Master
  │              │              │              │                     ├── Product Variant
  │              │              │              │                     ├── Product Attribute Value
  │              │              │              │                     ├── Product Media
  │              │              │              │                     └── Product Channel Assignment
  │              │              │              │                            │
  │              │              │              │                            └──▶ Phase 7: Go-Live
  │              │              │              │                                   ├── Workflow Activation
  │              │              │              │                                   ├── Channel Publishing
  │              │              │              │                                   ├── Export Feed Scheduling
  │              │              │              │                                   └── ERPNext Sync Activation
```

### Phase 0: Global Configuration (PIM Settings)

**Duration:** 30 minutes – 1 hour
**Role:** System Manager
**Dependency:** None — this is the root of all configuration

| Step | Setting | DocType / Field | Description |
|------|---------|-----------------|-------------|
| 0.1 | Enable ERP Sync | `PIM Settings.enable_erp_sync` | Decide whether ERPNext integration is active |
| 0.2 | Sync Direction | `PIM Settings.sync_direction` | `PIM to ERP`, `ERP to PIM`, or `Bidirectional` |
| 0.3 | Default Company | `PIM Settings.default_company` | For ERPNext Item creation |
| 0.4 | Auto-Sync on Save | `PIM Settings.auto_sync_on_save` | Enable/disable automatic sync trigger |
| 0.5 | AI Enrichment | `PIM Settings.enable_ai_enrichment` | Enable AI-powered content generation |
| 0.6 | AI Provider | `PIM Settings.ai_provider` | `OpenAI`, `Anthropic`, `Google Gemini`, etc. |
| 0.7 | AI API Key | `PIM Settings.ai_api_key` | Provider API key (password field) |
| 0.8 | AI Model | `PIM Settings.ai_model` | Model identifier (e.g., `gpt-4o`, `claude-3-sonnet`) |
| 0.9 | Quality Scoring | `PIM Settings.enable_quality_scoring` | Enable multi-dimensional scoring |
| 0.10 | Min Quality Score | `PIM Settings.minimum_quality_score` | Threshold for channel publishing (0–100) |
| 0.11 | Media Max Size | `PIM Settings.max_file_size_mb` | Maximum upload size in MB |
| 0.12 | Allowed Formats | `PIM Settings.allowed_image_formats` | Comma-separated list (e.g., `jpg,png,webp`) |

**Checkpoint:** Run `frappe.get_doc("PIM Settings")` to verify all fields are populated.

### Phase 1: Foundation Schema

**Duration:** 2–8 hours (depends on product complexity)
**Role:** PIM Manager / Solution Architect
**Dependency:** Phase 0 complete

#### Step 1.1: PIM Attribute Types

Verify or customize the built-in data types. The system ships with 12 default types:

| Order | Attribute Type | Notes |
|-------|---------------|-------|
| 1 | Text | Short text values |
| 2 | Long Text | Descriptions, care instructions |
| 3 | Integer | Whole numbers |
| 4 | Float | Decimal values |
| 5 | Select | Single-choice dropdown |
| 6 | Multi Select | Multiple-choice |
| 7 | Boolean | Yes/No flags |
| 8 | Date | Date values |
| 9 | Datetime | Date+time values |
| 10 | Link | Reference to another DocType |
| 11 | Image | Image file reference |
| 12 | File | Document file reference |

> **Action:** Review and add any custom types needed (e.g., `Color Swatch`, `URL`, `JSON`).

#### Step 1.2: PIM Attribute Groups

Create or customize the 4 default groups from installation:

| Order | Group | `group_code` | Purpose |
|-------|-------|-------------|---------|
| 1 | General | `general` | Core product attributes |
| 2 | Dimensions | `dimensions` | Physical measurements |
| 3 | SEO | `seo` | Search optimization fields |
| 4 | Technical | `technical` | Technical specifications |

> **Action:** Add industry-specific groups (e.g., `Nutrition`, `Compliance`, `Safety`).

#### Step 1.3: PIM Attributes

Create all product attributes the customer needs. Each attribute must specify:

| Configuration | Required | Example |
|---------------|----------|---------|
| `attribute_name` | Yes | "Color" |
| `attribute_code` | Yes | "color" |
| `data_type` | Yes | Link → PIM Attribute Type |
| `attribute_group` | Yes | Link → PIM Attribute Group |
| `is_required` | No | Whether attribute is mandatory |
| `is_filterable` | No | Available in product search filters |
| `is_variant_axis` | No | Used to generate SKU variants |
| `is_translatable` | No | Supports multi-locale values |

> **Action:** Create 10–100+ attributes depending on product complexity.

#### Step 1.4: PIM Attribute Options

For `Select` and `Multi Select` attributes, define the allowed values:

```
Attribute: "Color"
  Options: Red, Blue, Green, Black, White, Navy, ...

Attribute: "Material"
  Options: Cotton, Polyester, Silk, Linen, Wool, ...

Attribute: "Certification"
  Options: ISO 9001, ISO 14001, OEKO-TEX, GOTS, ...
```

#### Step 1.5: Product Families

Create the product family hierarchy. This is the **most critical configuration decision**:

| Configuration | Impact |
|---------------|--------|
| `family_name` / `family_code` | Identity of the family |
| `parent_family` | Hierarchy (enables attribute inheritance) |
| `naming_series_prefix` | SKU auto-numbering (e.g., `TSH-`, `BLT-`) |
| `allow_variants` | Whether products support SKU variants |
| `inherit_parent_attributes` | Pull attributes from parent family |
| `erp_item_group` | Maps to ERPNext Item Group |
| `attributes` (child table) | Assigns attributes to this family |
| `variant_attributes` (child table) | Defines variant axes |

> **Action:** Build the family tree, assign attributes, configure variant axes.

**Checkpoint:** Verify family-attribute template completeness — every family should have all required attributes assigned.

### Phase 2: Content Infrastructure

**Duration:** 1–4 hours
**Role:** PIM Manager
**Dependency:** Phase 1 complete (families and attributes exist)

| Step | Entity | DocType | Notes |
|------|--------|---------|-------|
| 2.1 | Product Types | PIM Product Type | Classify product categories (e.g., Apparel, Electronics) |
| 2.2 | Categories | Category | Build NestedSet navigation hierarchy |
| 2.3 | Taxonomies | Taxonomy + Taxonomy Node | Channel-specific classification trees |
| 2.4 | Brands | Brand | Register all brand identities |
| 2.5 | Manufacturers | Manufacturer | Register all manufacturers |

**Checkpoint:** Navigate the Category tree to verify hierarchy. Confirm all brands/manufacturers are registered.

### Phase 3: Quality & Governance

**Duration:** 1–3 hours
**Role:** PIM Manager + System Manager
**Dependency:** Phase 1–2 complete (families, categories exist for permission scoping)

| Step | Entity | DocType | Notes |
|------|--------|---------|-------|
| 3.1 | Roles | Frappe Role (PIM Manager, PIM User) | Assign roles to users |
| 3.2 | Category Permissions | PIM Category Permission | Restrict users to specific product categories |
| 3.3 | Data Stewards | Data Steward | Assign category/family ownership |
| 3.4 | Quality Policies | Data Quality Policy | Define per-family/brand/channel quality rules |
| 3.5 | Scoring Weights | PIM Settings (scoring fields) | Customize dimension weights if needed |

**Key Decision:** Decide the minimum quality score for channel publishing. The default is controlled by `PIM Settings.minimum_quality_score`.

**Checkpoint:** Create a test user with PIM User role and verify they can only see permitted categories.

### Phase 4: Channel & Export Setup

**Duration:** 2–6 hours (depends on number of channels)
**Role:** PIM Manager
**Dependency:** Phase 1–3 complete (attributes exist for channel requirement mapping)

| Step | Entity | DocType | Notes |
|------|--------|---------|-------|
| 4.1 | Sales Channels | Channel / PIM Sales Channel | Enable target marketplaces |
| 4.2 | Channel Locales | Channel Locale (child table) | Set language per channel |
| 4.3 | Attribute Requirements | Channel Attribute Requirement | Define per-channel required fields |
| 4.4 | Export Profiles | Export Profile | Configure export format, filters, scheduling |
| 4.5 | Feed Scheduling | Export Profile.schedule_type | Set `Daily`, `Weekly`, or `Manual` |

**Per-Channel Configuration Checklist:**

| Channel | Critical Fields | Media Minimum | Special Requirements |
|---------|----------------|---------------|---------------------|
| Amazon | ASIN, Brand, Bullet Points | 7 images | A+ Content, Product Type |
| Shopify | Handle, Vendor, Tags | 1 image | Metafields |
| WooCommerce | SKU, Categories, Tags | 1 image | Short Description |
| Google Merchant | GTIN, MPN, Condition | 1 image | Google Product Category |
| Trendyol | Barcode, Category ID | 4 images | Turkish descriptions |
| Hepsiburada | Barcode, Category ID | 3 images | Turkish descriptions |
| N11 | Product Code, Category | 3 images | Turkish descriptions |
| eBay | EAN/UPC, Condition, MPN | 1 image | Item Specifics |
| Etsy | Materials, Tags (13 max) | 5 images | Who Made It, When Made |
| Walmart | GTIN, Brand, Shelf Description | 4 images | Rich Media |
| Meta Commerce | Content ID, Brand | 4 images | Commerce Manager fields |
| TikTok Shop | Category, Brand | 5 images | Video required for some categories |

**Checkpoint:** Run completeness check on a sample product for each enabled channel.

### Phase 5: Advanced Features (Optional)

**Duration:** 2–8 hours (only enable what the customer needs)
**Role:** PIM Manager / System Manager
**Dependency:** Phase 4 complete

| Step | Feature | When to Enable | DocTypes |
|------|---------|---------------|----------|
| 5.1 | AI Enrichment | Customer wants auto-generated content | AI Prompt Template, AI Enrichment Job |
| 5.2 | GS1 Packaging | Products with GTIN hierarchy | GS1 Packaging Hierarchy, Package Variant |
| 5.3 | Bundling | Customer sells product bundles | PIM Bundle, PIM Bundle Slot, PIM Bundle Tier |
| 5.4 | Pricing Rules | Complex pricing (tiered, contract) | Price Rule, PIM Contract Price |
| 5.5 | MDM | Multiple source systems feeding PIM | Source System, Survivorship Rule, Golden Record |
| 5.6 | Competitor Tracking | Competitive analysis needed | Competitor Analysis, Market Insight, Digital Shelf Snapshot |
| 5.7 | Partner Portal | Brands/suppliers submit product data | Partner Submission, Brand Portal User |
| 5.8 | Compliance Templates | Industry-specific regulations | Nutrition Facts, Chemical Usage Instruction |
| 5.9 | Display Templates | Custom product display/output | Display Template, Datasheet Template |

**Checkpoint:** Test each enabled feature with sample data before proceeding.

### Phase 6: Content Creation

**Duration:** Days to weeks (depends on catalog size)
**Role:** PIM User / PIM Manager
**Dependency:** Phase 1–4 complete (schema, quality, channels exist)

| Step | Action | DocType | Bulk Method |
|------|--------|---------|-------------|
| 6.1 | Create Products | Product Master | Import via Data Import Tool or API |
| 6.2 | Set Attribute Values | Product Attribute Value | Batch update via `bulk_update_attribute` API |
| 6.3 | Generate Variants | Product Variant | Variant Generator (`variant_generator.py`) |
| 6.4 | Upload Media | Product Media | Bulk upload via file manager |
| 6.5 | Add Translations | Product Translation Item | AI Translation service or manual entry |
| 6.6 | Assign Channels | Product Channel (child table) | Bulk assignment via API |
| 6.7 | Assign Categories | Product Master.category | Batch update |

**Checkpoint:** Run quality scoring on all products. Identify products below the minimum quality threshold and enrich them.

### Phase 7: Go-Live

**Duration:** 1–2 hours (final activation)
**Role:** PIM Manager + System Manager
**Dependency:** Phase 6 complete with sufficient product data quality

| Step | Action | Configuration | Notes |
|------|--------|--------------|-------|
| 7.1 | Activate Workflow | Set products to `In Production` state | Begin the lifecycle workflow |
| 7.2 | Enable ERP Sync | Verify `PIM Settings.enable_erp_sync` | Activate bidirectional sync |
| 7.3 | Publish to Channels | Move products to `Approved` state | Products meeting channel completeness are eligible |
| 7.4 | Enable Feed Scheduling | Set Export Profile schedule | Automated daily/weekly feeds |
| 7.5 | Enable Webhooks | Configure webhook endpoints | Real-time notifications to external systems |
| 7.6 | Monitor Quality Dashboard | Review Product Score records | Track quality trends |
| 7.7 | Train Users | Handover to customer team | Provide role-specific training |

**Final Checklist:**

- [ ] All Product Families have complete attribute templates
- [ ] All enabled channels have attribute requirements configured
- [ ] Quality policies match customer business rules
- [ ] At least one export profile per active channel
- [ ] ERP sync tested with sample products (if enabled)
- [ ] User roles and category permissions verified
- [ ] Backup taken before go-live

---

## 17. Edge Cases & Deployment Scenarios

### Overview

Not every PIM deployment follows the standard Greenfield path. This section addresses the four major deployment variations and how they modify the standard onboarding sequence from Section 16.

### 17.1 Greenfield vs. Migration

#### Greenfield Deployment

**Definition:** Brand-new PIM deployment with no existing product data.

**Approach:** Follow the Phase 0–7 sequence from Section 16 exactly.

**Advantages:**
- Clean data model from day one
- No legacy data issues
- Full control over attribute design

**Key Decisions:**
| Decision | Impact | Guidance |
|----------|--------|----------|
| Attribute granularity | Fine-grained vs. coarse attributes | Start with the attributes you need today; add more later |
| Family depth | Flat vs. deep hierarchy | Keep to 2–3 levels unless business requires more |
| Naming conventions | SKU format, family codes | Define conventions early — changing later is costly |
| Variant strategy | Which attributes are variant axes | Choose carefully — variant axes cannot be easily changed after products are created |

#### Migration Deployment

**Definition:** Moving product data from an existing system (spreadsheets, legacy PIM, ERP, e-commerce platform).

**Modified Sequence:**

```
Standard Phase 0–3   →   Migration Mapping Phase   →   Data Import   →   Phase 4–7
                                │
                                ├── Map source fields to PIM attributes
                                ├── Map source categories to Product Families
                                ├── Map source product types to PIM Product Types
                                ├── Define data cleansing rules
                                ├── Create attribute value mappings (normalization)
                                └── Define duplicate detection strategy
```

**Additional Steps for Migration:**

| Step | Action | Notes |
|------|--------|-------|
| M.1 | Source Analysis | Audit the existing data: field coverage, quality, completeness |
| M.2 | Schema Mapping | Map source fields → PIM Attributes + Attribute Groups |
| M.3 | Value Normalization | Create lookup tables for inconsistent values (e.g., "Red", "red", "RED" → "Red") |
| M.4 | Family Assignment | Map source categories → Product Families |
| M.5 | Import Configuration | Set up Import Configuration DocType (planned) or Data Import Tool |
| M.6 | Test Import | Import a small batch (50–100 products) and verify |
| M.7 | Quality Audit | Run scoring on imported products to identify gaps |
| M.8 | Enrichment Pass | Use AI enrichment to fill gaps in descriptions, SEO fields |
| M.9 | Full Import | Import remaining products in batches |
| M.10 | Validation | Run completeness checks for all target channels |

**Migration-Specific Risks:**

| Risk | Mitigation |
|------|-----------|
| Data loss during mapping | Create a complete source → target field mapping document before import |
| Duplicate products | Enable MDM Golden Record matching during import |
| Missing variant data | May need to reconstruct variant structures from flat SKU data |
| Broken media links | Download and re-upload all product images; don't rely on external URLs |
| Inconsistent attribute values | Normalize before import using PIM Attribute Option lists |

**MDM Integration for Migration:**

For migrations from multiple source systems, enable the MDM module (Section 15):

1. Register each source system as a `Source System` record
2. Define `Survivorship Rule` entries for field-level conflict resolution
3. Import data from each source
4. The `merge_survive.py` service will create `Golden Record` entries
5. Review and approve merged records via the Golden Record interface

### 17.2 Single vs. Multi-Company

#### Single Company

**Definition:** Standard deployment with one company entity.

**Approach:** Standard Phase 0–7. Set `PIM Settings.default_company` once and all ERP sync operations use this company.

**Configuration:**
| Setting | Value |
|---------|-------|
| `PIM Settings.default_company` | The single company name |
| ERP Item creation | All Items belong to one company |
| Price lists | Single company price lists |
| Warehouses | Single company warehouses |

#### Multi-Company

**Definition:** ERPNext is configured with multiple companies (e.g., regional subsidiaries, holding company structure).

**Modified Sequence:**

| Phase | Modification |
|-------|-------------|
| Phase 0 | Set `default_company` to the primary company |
| Phase 1 | Product Families may need per-company variants if product lines differ |
| Phase 2 | Brands may be shared or company-specific |
| Phase 4 | Channels may be company-specific (e.g., Company A → Amazon EU, Company B → Amazon US) |
| Phase 6 | Products may need company-specific pricing and warehouse assignments |

**Key Considerations:**

| Area | Single Company | Multi-Company |
|------|---------------|---------------|
| Product Master | One record per product | One record per product (shared) |
| ERPNext Item | One Item per product | One Item per product per company (or shared) |
| Price Lists | One set | Per-company price lists |
| Warehouses | Single company stock | Per-company warehouses |
| User Permissions | Category-based only | Category-based + company-based |
| Export Profiles | No company filter needed | May need per-company export profiles |
| Channels | Assigned freely | May need company-specific channel assignments |

**Configuration Pattern for Multi-Company:**

```
Company A (Turkey):
  ├── Channels: Trendyol, Hepsiburada, N11
  ├── Export Profiles: Turkish marketplace feeds
  ├── Price Lists: TRY prices
  └── Users: Turkish content team

Company B (Germany):
  ├── Channels: Amazon DE, eBay DE
  ├── Export Profiles: BMEcat, German marketplace feeds
  ├── Price Lists: EUR prices
  └── Users: German content team

Shared:
  ├── Product Master (shared product data)
  ├── Product Families (shared schema)
  ├── Attributes (shared attribute definitions)
  └── Media (shared images/assets)
```

### 17.3 With vs. Without ERPNext

#### With ERPNext (Full Integration)

**Definition:** Frappe PIM is deployed alongside ERPNext with bidirectional sync enabled.

**Approach:** Standard Phase 0–7 with ERP-specific steps.

**ERPNext-Specific Configuration:**

| Setting | Impact |
|---------|--------|
| `PIM Settings.enable_erp_sync` = `1` | Activates sync engine |
| `PIM Settings.sync_direction` | Controls data flow direction |
| `PIM Settings.auto_sync_on_save` | Real-time vs. manual sync |
| `PIM Settings.default_company` | Required for Item creation |
| Product Family.`erp_item_group` | Maps PIM families to ERP Item Groups |

**ERPNext Dependencies (in onboarding order):**

1. Item Groups must exist in ERPNext before mapping to Product Families
2. UOM (Unit of Measure) list must be set up in ERPNext
3. Price Lists must be created in ERPNext for pricing sync
4. Warehouses must exist for stock sync
5. Company must exist for multi-company scenarios

**Sync Field Mapping (implemented in `item_sync.py`):**

| PIM Field | ERPNext Field | Direction |
|-----------|---------------|-----------|
| `product_name` | `item_name` | Bidirectional |
| `product_code` | `item_code` | PIM → ERP |
| `short_description` | `description` | PIM → ERP |
| `barcode` | `barcodes` (child table) | PIM → ERP |
| `weight` | `weight_per_unit` | PIM → ERP |
| `weight_uom` | `weight_uom` | PIM → ERP |
| `brand` | `brand` | Bidirectional |
| `manufacturer` | `manufacturer` | PIM → ERP |

**Custom Fields on ERPNext Item (from `fixtures/custom_field.json`):**

50+ custom fields are added to the ERPNext Item DocType to store PIM-sourced data, including:
- `pim_product_id` — link back to Product Master
- `pim_sync_status` — sync state indicator
- `pim_last_sync` — timestamp of last sync
- `pim_quality_score` — product quality score from PIM
- `pim_lifecycle_state` — current workflow state
- Channel-specific identifiers (Amazon ASIN, Trendyol Barcode, etc.)

#### Without ERPNext (Standalone PIM)

**Definition:** Frappe PIM deployed as a standalone product information system without ERPNext.

**Modified Sequence:**

| Phase | Modification |
|-------|-------------|
| Phase 0 | Set `enable_erp_sync` = `0` and skip all ERP-related settings |
| Phase 1 | Skip `erp_item_group` mapping on Product Families |
| Phase 2 | No Item Group dependency |
| Phase 3 | No ERP-related permissions needed |
| Phase 7 | No ERP sync activation |

**What Still Works Without ERPNext:**

| Feature | Available? | Notes |
|---------|-----------|-------|
| Product Management | ✅ Yes | Full product lifecycle |
| Attribute System | ✅ Yes | Complete EAV pattern |
| Channel Publishing | ✅ Yes | All 12 channels |
| Quality Scoring | ✅ Yes | All 6 dimensions |
| AI Enrichment | ✅ Yes | All providers |
| Media Management | ✅ Yes | Full media pipeline |
| Export/Import | ✅ Yes | All export formats |
| MDM | ✅ Yes | Golden records, source systems |
| Bundling | ✅ Yes | Product bundles |
| i18n | ✅ Yes | Multi-language support |
| Workflow | ✅ Yes | 7-state lifecycle |
| Pricing | ⚠️ Partial | PIM Price Rules work, but no ERP Price List sync |
| Stock/Inventory | ❌ No | Requires ERPNext |
| Sales Orders | ❌ No | Requires ERPNext |
| Purchase Management | ❌ No | Requires ERPNext |

**Standalone PIM Settings:**

```python
# Minimal PIM Settings for standalone deployment
{
    "enable_erp_sync": 0,
    "sync_direction": "",          # Not applicable
    "auto_sync_on_save": 0,        # Not applicable
    "default_company": "",         # Not applicable
    "enable_ai_enrichment": 1,     # Recommended
    "enable_quality_scoring": 1,   # Recommended
    "minimum_quality_score": 70,
    "max_file_size_mb": 10,
    "allowed_image_formats": "jpg,png,webp"
}
```

### 17.4 Minimal vs. Full Setup

#### Minimal Viable Configuration

**Definition:** The absolute minimum configuration to start creating and managing products.

**Time:** 1–2 hours
**Suitable for:** Proof of concept, small catalog (<100 products), single-channel

| Component | Minimum Required |
|-----------|-----------------|
| PIM Settings | `enable_erp_sync`, `minimum_quality_score` |
| Attribute Types | Use the 12 built-in types (no customization needed) |
| Attribute Groups | Use the 4 default groups (General, Dimensions, SEO, Technical) |
| Attributes | 5–10 core attributes (name, description, price, weight, color) |
| Product Families | 1–3 families |
| Channels | 1 channel |
| Export Profiles | 1 export profile |
| Roles | PIM Manager (1 user), PIM User (1–2 users) |
| Quality | Default scoring weights (no customization) |

**Minimal Configuration Sequence:**

```
1. PIM Settings (5 min)          → Set basic flags
2. Product Family (15 min)       → Create 1-3 families with attributes
3. Brand (5 min)                 → Create primary brand
4. Channel (10 min)              → Enable primary sales channel
5. Export Profile (10 min)       → Create export for primary channel
6. Products (ongoing)            → Start creating products
```

#### Full Enterprise Configuration

**Definition:** Complete configuration leveraging all PIM capabilities.

**Time:** 2–4 weeks
**Suitable for:** Enterprise deployments, large catalog (1000+ products), multi-channel, multi-language

| Component | Enterprise Configuration |
|-----------|------------------------|
| PIM Settings | All sections configured (ERP, AI, Quality, GS1, Media) |
| Attribute Types | 12 built-in + custom types as needed |
| Attribute Groups | 4 defaults + 5–10 custom groups |
| Attributes | 50–200+ attributes |
| Product Families | 10–50+ families with deep hierarchy |
| Channels | 4–12 channels |
| Export Profiles | 1–3 per channel |
| Roles | PIM Manager, PIM User, Data Steward, category-scoped permissions |
| Quality | Custom policies per family/brand/channel |
| AI | Configured with prompts, approval workflows |
| MDM | Source systems, survivorship rules, golden records |
| GS1 | Full packaging hierarchy |
| Bundling | Bundle configurations |
| i18n | 3–10 languages |
| Competitors | Tracking enabled |
| Partner Portal | Brand portal users |
| Display Templates | Product cards, datasheets, catalogs |
| Compliance | Nutrition facts, chemical SDS, certifications |

**Enterprise Configuration Sequence:**

```
Week 1: Foundation
  ├── Day 1: PIM Settings + Attribute Types + Groups
  ├── Day 2-3: Attributes (50-200+) + Options
  ├── Day 4-5: Product Families (hierarchy + templates)

Week 2: Infrastructure
  ├── Day 1: Categories + Taxonomies + Brands + Manufacturers
  ├── Day 2: Roles + Permissions + Data Stewards
  ├── Day 3: Quality Policies + Scoring Customization
  ├── Day 4-5: Channel Setup (all target marketplaces)

Week 3: Advanced Features + Data
  ├── Day 1: AI Configuration + Prompt Templates
  ├── Day 2: GS1 + Bundling + Pricing Rules
  ├── Day 3: MDM Setup (if migrating from multiple sources)
  ├── Day 4-5: Begin data import / content creation

Week 4: Go-Live
  ├── Day 1-2: Content enrichment + quality scoring review
  ├── Day 3: User training
  ├── Day 4: ERP sync activation + channel publishing tests
  ├── Day 5: Go-live + monitoring
```

### 17.5 Common Deployment Patterns

| Pattern | Description | Typical Setup |
|---------|-------------|---------------|
| **PIM + ERPNext + Marketplace** | Full stack: ERP for operations, PIM for product content, marketplace for sales | All phases, ERP sync bidirectional |
| **PIM + Shopify** | PIM as content hub feeding Shopify storefront | No ERPNext, Shopify channel only |
| **PIM + Multiple Marketplaces** | Central PIM distributing to many channels | All channels, export profiles per channel |
| **PIM as MDM Hub** | PIM as golden record system for multiple sources | MDM module, survivorship rules, import configs |
| **PIM + ERPNext (no channels)** | Internal product master with ERP sync only | ERP sync, no channels, internal use only |
| **PIM for Catalog Generation** | PIM feeding print/digital catalog systems | Display Templates, Datasheet Templates, Export |

---

## 18. Customer Archetype Deep-Dives

### Overview

This section provides **complete configuration profiles** for three representative customer types. Each profile covers the full onboarding sequence with specific values, showing exactly what gets configured for each customer type.

### 18.1 Archetype: Fashion Retailer

**Business Profile:**
- **Industry:** Fashion & Apparel
- **Catalog Size:** 2,000–10,000 SKUs
- **Products:** Clothing, footwear, accessories
- **Markets:** Turkey, Germany, EU
- **Channels:** Trendyol, Hepsiburada, Amazon, Shopify (own webshop)
- **Languages:** Turkish (primary), English, German
- **ERPNext:** Yes (full integration)

#### Phase 0: PIM Settings

```python
{
    "enable_erp_sync": 1,
    "sync_direction": "PIM to ERP",
    "auto_sync_on_save": 1,
    "default_company": "Fashion House TR",
    "enable_ai_enrichment": 1,
    "ai_provider": "OpenAI",
    "ai_model": "gpt-4o",
    "enable_quality_scoring": 1,
    "minimum_quality_score": 75,
    "max_file_size_mb": 10,
    "allowed_image_formats": "jpg,png,webp"
}
```

#### Phase 1: Foundation Schema

**Attribute Groups (6 total):**

| Group | Code | Attributes |
|-------|------|-----------|
| General | `general` | Brand, Season, Year, Target Gender, Age Group, Collection |
| Dimensions | `dimensions` | Weight (g), Length (cm), Width (cm), Height (cm) |
| Apparel | `apparel` | Material Composition, Care Instructions, Country of Origin, Size Chart |
| Colors & Variants | `colors_variants` | Color, Size, Color Family, Pattern |
| SEO | `seo` | Meta Title, Meta Description, Keywords, URL Slug |
| Compliance | `compliance` | OEKO-TEX Certified, CE Marking, Textile Composition Label |

**Key Attributes (30+ total):**

| Attribute | Code | Type | Variant Axis? | Filterable? | Translatable? |
|-----------|------|------|--------------|-------------|---------------|
| Color | `color` | Select | ✅ Yes | ✅ Yes | ❌ No |
| Size | `size` | Select | ✅ Yes | ✅ Yes | ❌ No |
| Material Composition | `material_composition` | Text | ❌ No | ❌ No | ✅ Yes |
| Care Instructions | `care_instructions` | Long Text | ❌ No | ❌ No | ✅ Yes |
| Season | `season` | Select | ❌ No | ✅ Yes | ❌ No |
| Target Gender | `target_gender` | Select | ❌ No | ✅ Yes | ❌ No |
| Pattern | `pattern` | Select | ❌ No | ✅ Yes | ✅ Yes |
| Fabric Weight (gsm) | `fabric_weight_gsm` | Float | ❌ No | ❌ No | ❌ No |

**Product Families (4 families):**

| Family | Code | Parent | Variants | Variant Axes | ERP Item Group | SKU Prefix |
|--------|------|--------|----------|-------------|----------------|------------|
| Apparel | `apparel` | — | ✅ | — | Finished Goods | `APP-` |
| → Tops | `tops` | Apparel | ✅ | Size, Color | Tops | `TOP-` |
| → Bottoms | `bottoms` | Apparel | ✅ | Size, Color | Bottoms | `BTM-` |
| Footwear | `footwear` | — | ✅ | Size, Color, Width | Footwear | `SHO-` |
| Accessories | `accessories` | — | ✅ | Color, Material | Accessories | `ACC-` |

#### Phase 4: Channel Configuration

| Channel | Priority | Languages | Min Images | Export Format |
|---------|----------|-----------|-----------|---------------|
| Trendyol | Primary | Turkish | 4 | API / JSON |
| Hepsiburada | Primary | Turkish | 3 | API / JSON |
| Amazon DE | Secondary | German, English | 7 | Amazon Flat File |
| Shopify (Own) | Secondary | Turkish, English, German | 5 | Shopify API |

**Export Profiles:**

| Profile | Channel | Format | Schedule | Filters |
|---------|---------|--------|----------|---------|
| `trendyol-daily` | Trendyol | JSON | Daily | Active + Approved + Trendyol-assigned |
| `hepsiburada-daily` | Hepsiburada | JSON | Daily | Active + Approved + Hepsiburada-assigned |
| `amazon-de-weekly` | Amazon DE | XML | Weekly | Active + Approved + Amazon-assigned + DE locale |
| `shopify-full` | Shopify | JSON | Daily | Active + Approved + Shopify-assigned |

#### Phase 5: Advanced Features

| Feature | Enabled | Configuration |
|---------|---------|--------------|
| AI Enrichment | ✅ | Auto-generate descriptions in TR/EN/DE; human review for marketing copy |
| Quality Scoring | ✅ | Min 75; custom weights: Media 25%, Content 20%, SEO 15%, Translation 20%, Attribute 15%, Market 5% |
| GS1 | ✅ | GTIN-13 barcodes for all products |
| Bundling | ✅ | Gift sets, outfit bundles |
| MDM | ❌ | Single source (PIM is master) |

#### Typical Product Example

```
Product Master: "Essential Cotton V-Neck T-Shirt"
  ├── Family: Tops (inherits from Apparel)
  ├── Brand: "FashionHouse"
  ├── Product Type: Apparel
  ├── Categories: Men > Tops > T-Shirts
  ├── Attributes:
  │     Material Composition: "100% Organic Cotton"
  │     Care Instructions: "Machine wash 30°C, tumble dry low"
  │     Season: "Spring/Summer 2026"
  │     Target Gender: "Male"
  │     Fabric Weight: 180 gsm
  │
  ├── Variants (Size × Color = 30 SKUs):
  │     TOP-001-S-BLK, TOP-001-S-WHT, TOP-001-S-NVY, ...
  │     TOP-001-M-BLK, TOP-001-M-WHT, TOP-001-M-NVY, ...
  │     TOP-001-L-BLK, TOP-001-L-WHT, TOP-001-L-NVY, ...
  │     ...
  │
  ├── Media: 8 images (front, back, detail, lifestyle × 2 colors)
  ├── Translations: TR ✅, EN ✅, DE ✅
  ├── Channels: Trendyol ✅, Hepsiburada ✅, Amazon DE ✅, Shopify ✅
  └── Quality Score: 92/100
```

---

### 18.2 Archetype: Industrial Supplier

**Business Profile:**
- **Industry:** Industrial Parts & Components
- **Catalog Size:** 50,000–200,000 SKUs
- **Products:** Fasteners, bearings, seals, tools, safety equipment
- **Markets:** Germany, EU, Turkey
- **Channels:** Own B2B webshop (Shopify/WooCommerce), Amazon Business, BMEcat feeds to procurement platforms
- **Languages:** German (primary), English, French, Dutch, Polish
- **ERPNext:** Yes (bidirectional sync — ERP is also a data source)

#### Phase 0: PIM Settings

```python
{
    "enable_erp_sync": 1,
    "sync_direction": "Bidirectional",
    "auto_sync_on_save": 0,       # Manual sync — controlled batches
    "default_company": "IndustrieTeile GmbH",
    "enable_ai_enrichment": 1,
    "ai_provider": "Anthropic",
    "ai_model": "claude-3-sonnet",
    "enable_quality_scoring": 1,
    "minimum_quality_score": 85,   # Higher threshold for B2B
    "max_file_size_mb": 25,        # Large technical drawings
    "allowed_image_formats": "jpg,png,webp,tiff"
}
```

#### Phase 1: Foundation Schema

**Attribute Groups (8 total):**

| Group | Code | Attributes |
|-------|------|-----------|
| General | `general` | Brand, Manufacturer Part Number, Product Line |
| Dimensions | `dimensions` | Length, Width, Height, Diameter, Thread Size, Weight |
| Technical | `technical` | Material Grade, Tensile Strength, Temperature Range, Pressure Rating |
| Compliance | `compliance` | ISO Certifications, CE Marking, RoHS, REACH, DIN Standard |
| Packaging | `packaging` | Unit of Sale, Pack Quantity, Min Order Qty, Lead Time |
| SEO | `seo` | Meta Title, Meta Description, Technical Keywords |
| Safety | `safety` | SDS Required, GHS Pictograms, PPE Required, ATEX Zone |
| Procurement | `procurement` | HS Code, Country of Origin, ECCN, Customs Tariff |

**Key Attributes (80+ total):**

| Attribute | Code | Type | Variant Axis? | Filterable? |
|-----------|------|------|--------------|-------------|
| Material Grade | `material_grade` | Select | ✅ Yes | ✅ Yes |
| Tolerance Class | `tolerance_class` | Select | ✅ Yes | ✅ Yes |
| Thread Size | `thread_size` | Select | ✅ Yes | ✅ Yes |
| Surface Treatment | `surface_treatment` | Select | ✅ Yes | ✅ Yes |
| Tensile Strength | `tensile_strength` | Float | ❌ No | ✅ Yes |
| Temperature Range | `temp_range` | Text | ❌ No | ✅ Yes |
| DIN Standard | `din_standard` | Multi Select | ❌ No | ✅ Yes |
| ISO Certification | `iso_certification` | Multi Select | ❌ No | ✅ Yes |

**Product Families (12+ families):**

| Family | Code | Variants | Variant Axes | SKU Prefix |
|--------|------|----------|-------------|------------|
| Fasteners | `fasteners` | ✅ | Thread Size, Material Grade, Length | `FST-` |
| → Bolts | `bolts` | ✅ | Thread Size, Material, Length, Head Type | `BLT-` |
| → Nuts | `nuts` | ✅ | Thread Size, Material Grade | `NUT-` |
| → Screws | `screws` | ✅ | Thread Size, Material, Length, Drive Type | `SCR-` |
| Bearings | `bearings` | ✅ | Inner Diameter, Tolerance | `BRG-` |
| Seals | `seals` | ✅ | Material, Diameter, Temperature Class | `SEL-` |
| Tools | `tools` | ❌ | — | `TLS-` |
| Safety Equipment | `safety_equip` | ✅ | Size | `SAF-` |

#### Phase 4: Channel Configuration

| Channel | Priority | Languages | Export Format |
|---------|----------|-----------|---------------|
| B2B Webshop (WooCommerce) | Primary | DE, EN | WooCommerce API |
| Amazon Business | Secondary | DE, EN | Amazon Flat File |
| BMEcat Feed (Procurement) | Primary | DE, EN, FR | BMEcat 2005 XML |

**Export Profiles:**

| Profile | Channel | Format | Schedule |
|---------|---------|--------|----------|
| `bmecat-master` | Procurement Portals | BMEcat 2005 XML | Weekly |
| `webshop-sync` | WooCommerce | JSON | Daily |
| `amazon-business` | Amazon Business | Amazon XML | Weekly |
| `etim-export` | ETIM Classification | CSV | Monthly |

#### Phase 5: Advanced Features

| Feature | Enabled | Configuration |
|---------|---------|--------------|
| AI Enrichment | ✅ | Generate technical descriptions from specs; auto-translate DE→EN/FR/NL/PL |
| Quality Scoring | ✅ | Min 85; weights: Attribute 35%, Content 20%, SEO 10%, Translation 20%, Media 10%, Market 5% |
| GS1 | ✅ | Full GTIN hierarchy for packaging levels |
| MDM | ✅ | 3 source systems (ERP, Supplier Portal, Legacy DB) |
| Compliance | ✅ | Chemical SDS, GHS pictograms, CE marking |
| Competitor Tracking | ✅ | Digital shelf monitoring on key platforms |

#### Typical Product Example

```
Product Master: "Hexagon Head Bolt DIN 933 8.8"
  ├── Family: Bolts (inherits from Fasteners)
  ├── Manufacturer: "BUFAB"
  ├── Product Type: Component
  ├── Categories: Fasteners > Bolts > Hex Bolts > DIN 933
  ├── Attributes:
  │     DIN Standard: "DIN 933"
  │     Material Grade: "8.8 Steel"
  │     Surface Treatment: "Hot-dip Galvanized"
  │     Tensile Strength: 800 MPa
  │     Proof Load: 580 MPa
  │     HS Code: "7318.15.90"
  │     ISO Certification: "ISO 4017"
  │
  ├── Variants (Thread × Length × Material = 200+ SKUs):
  │     BLT-933-M8x20-88-HDG, BLT-933-M8x25-88-HDG, ...
  │     BLT-933-M10x20-88-HDG, BLT-933-M10x25-88-HDG, ...
  │     BLT-933-M12x30-88-HDG, BLT-933-M12x40-88-HDG, ...
  │
  ├── Media: 3 images (product photo, technical drawing, dimension diagram)
  ├── Documents: SDS PDF, test certificate
  ├── Translations: DE ✅, EN ✅, FR ✅, NL ✅, PL ✅
  ├── Channels: Webshop ✅, Amazon Business ✅, BMEcat ✅
  ├── GS1 Packaging: Each → Inner Pack (10) → Carton (100) → Pallet (4000)
  └── Quality Score: 88/100
```

---

### 18.3 Archetype: Food Manufacturer

**Business Profile:**
- **Industry:** Food & Beverage Manufacturing
- **Catalog Size:** 500–5,000 SKUs
- **Products:** Packaged foods, beverages, ingredients
- **Markets:** Turkey, EU (Germany, France, Italy, Netherlands)
- **Channels:** Own website, Trendyol, Retail chain portals (via BMEcat/GDSN)
- **Languages:** Turkish (primary), English, German, French
- **ERPNext:** Yes (PIM to ERP — PIM is product master)
- **Compliance:** FDA (if US), EU 1169/2011, Turkish Food Codex, Halal certification

#### Phase 0: PIM Settings

```python
{
    "enable_erp_sync": 1,
    "sync_direction": "PIM to ERP",
    "auto_sync_on_save": 1,
    "default_company": "AnadoluGıda A.Ş.",
    "enable_ai_enrichment": 1,
    "ai_provider": "OpenAI",
    "ai_model": "gpt-4o",
    "enable_quality_scoring": 1,
    "minimum_quality_score": 90,    # Very high — regulatory compliance
    "max_file_size_mb": 15,
    "allowed_image_formats": "jpg,png,webp"
}
```

#### Phase 1: Foundation Schema

**Attribute Groups (9 total):**

| Group | Code | Attributes |
|-------|------|-----------|
| General | `general` | Brand, Product Line, Country of Origin |
| Dimensions | `dimensions` | Net Weight, Gross Weight, Volume, Pack Size |
| Nutrition | `nutrition` | Calories, Fat, Protein, Carbs, Sugar, Sodium, Fiber |
| Allergens | `allergens` | Contains Gluten, Contains Dairy, Contains Nuts, Contains Soy, Contains Eggs |
| Ingredients | `ingredients` | Ingredient List, Ingredient Source, Processing Method |
| Compliance | `compliance` | Halal Certified, Organic Certified, Non-GMO, Kosher |
| Storage | `storage` | Storage Temperature, Shelf Life (days), Packaging Type |
| SEO | `seo` | Meta Title, Meta Description, Keywords |
| Regulatory | `regulatory` | EU Food Category, Turkish Food Codex Category, FDA Product Code |

**Key Attributes (60+ total):**

| Attribute | Code | Type | Variant Axis? | Translatable? |
|-----------|------|------|--------------|---------------|
| Net Weight | `net_weight` | Float | ✅ Yes | ❌ No |
| Pack Size | `pack_size` | Select | ✅ Yes | ❌ No |
| Flavor | `flavor` | Select | ✅ Yes | ✅ Yes |
| Calories (kcal/100g) | `calories_100g` | Float | ❌ No | ❌ No |
| Fat (g/100g) | `fat_100g` | Float | ❌ No | ❌ No |
| Protein (g/100g) | `protein_100g` | Float | ❌ No | ❌ No |
| Contains Gluten | `contains_gluten` | Boolean | ❌ No | ❌ No |
| Ingredient List | `ingredient_list` | Long Text | ❌ No | ✅ Yes |
| Shelf Life (days) | `shelf_life_days` | Integer | ❌ No | ❌ No |
| Storage Temperature | `storage_temp` | Select | ❌ No | ❌ No |
| Halal Certified | `halal_certified` | Boolean | ❌ No | ❌ No |

**Product Families (5 families):**

| Family | Code | Variants | Variant Axes | SKU Prefix |
|--------|------|----------|-------------|------------|
| Fresh Produce | `fresh_produce` | ✅ | Weight, Pack Size | `FRS-` |
| Packaged Food | `packaged_food` | ✅ | Pack Size, Flavor | `PKG-` |
| → Snacks | `snacks` | ✅ | Pack Size, Flavor | `SNK-` |
| → Dairy | `dairy` | ✅ | Pack Size, Fat Content | `DRY-` |
| Beverage | `beverage` | ✅ | Volume, Flavor | `BEV-` |
| Ingredient | `ingredient` | ✅ | Grade, Weight | `ING-` |

#### Phase 4: Channel Configuration

| Channel | Priority | Languages | Export Format |
|---------|----------|-----------|---------------|
| Own Website | Primary | TR, EN | JSON API |
| Trendyol | Primary | Turkish | Trendyol API |
| Retail Chain Portal | Primary | TR, EN, DE | BMEcat / GS1 XML |
| Google Merchant | Secondary | TR, EN | Google Shopping Feed |

#### Phase 5: Advanced Features

| Feature | Enabled | Configuration |
|---------|---------|--------------|
| AI Enrichment | ✅ | Generate marketing descriptions; NOT for nutritional data (regulatory) |
| Quality Scoring | ✅ | Min 90; weights: Attribute 30%, Content 15%, Media 15%, Translation 15%, SEO 10%, Market 15% |
| GS1 | ✅ | Full GTIN-13 + GTIN-14 packaging hierarchy |
| Nutrition Facts | ✅ | EU 1169/2011 + Turkish Food Codex compliance |
| Compliance Templates | ✅ | Allergen declarations, halal certificates, organic certificates |

**Compliance Configuration:**

| Regulation | DocType | Required Fields |
|-----------|---------|----------------|
| EU 1169/2011 | Nutrition Facts | Energy, Fat, Saturates, Carbs, Sugars, Protein, Salt per 100g |
| Turkish Food Codex | Nutrition Facts | Same as EU + halal certification reference |
| FDA (if US market) | Nutrition Facts | Added Sugars, Vitamin D, Potassium, US serving sizes |
| Allergen Declaration | PIM Attribute (Boolean flags) | 14 EU allergens as individual attributes |
| Halal | PIM Attribute (Boolean) | Certificate number, certifying body, expiry date |

#### Typical Product Example

```
Product Master: "Organic Honey — Anatolian Blossom"
  ├── Family: Packaged Food
  ├── Brand: "AnadoluGıda"
  ├── Product Type: Packaged Food
  ├── Categories: Food > Spreads > Honey > Organic
  ├── Attributes:
  │     Ingredient List: "100% Organic Anatolian Blossom Honey"
  │     Country of Origin: "Turkey"
  │     Calories: 320 kcal/100g
  │     Carbohydrates: 80g/100g
  │     Sugar: 75g/100g
  │     Fat: 0g/100g
  │     Protein: 0.3g/100g
  │     Halal Certified: Yes
  │     Organic Certified: Yes
  │     Shelf Life: 730 days
  │     Storage Temperature: Room Temperature
  │
  ├── Variants (Weight):
  │     PKG-HONEY-250  (250g jar)
  │     PKG-HONEY-500  (500g jar)
  │     PKG-HONEY-1000 (1kg jar)
  │     PKG-HONEY-5000 (5kg bulk)
  │
  ├── Nutrition Facts: EU 1169/2011 ✅, Turkish Food Codex ✅
  ├── Allergen Declaration: No allergens present ✅
  ├── Media: 5 images (product, label close-up, lifestyle, packaging, certification)
  ├── Translations: TR ✅, EN ✅, DE ✅, FR ✅
  ├── Channels: Own Website ✅, Trendyol ✅, Retail Chain ✅
  ├── GS1 Packaging: Each (250g) → Case (12) → Pallet (480)
  └── Quality Score: 95/100
```

---

### 18.4 Archetype Comparison Matrix

| Dimension | Fashion Retailer | Industrial Supplier | Food Manufacturer |
|-----------|-----------------|--------------------|--------------------|
| **Catalog Size** | 2K–10K SKUs | 50K–200K SKUs | 500–5K SKUs |
| **Attribute Count** | 30+ | 80+ | 60+ |
| **Variant Complexity** | Size × Color (5–30 SKUs/product) | Multi-axis (50–200+ SKUs/product) | Weight × Flavor (3–10 SKUs/product) |
| **Product Families** | 4–8 | 12–20+ | 5–8 |
| **Channels** | 4–6 (B2C marketplaces) | 2–4 (B2B + marketplaces) | 3–5 (B2C + retail portals) |
| **Languages** | 2–3 | 4–5+ | 3–4 |
| **Primary Export Format** | JSON/API | BMEcat 2005 XML | GS1 XML / BMEcat |
| **Quality Score Threshold** | 75 | 85 | 90 |
| **AI Use Case** | Marketing copy, translations | Technical descriptions, translations | Marketing copy (NOT nutrition data) |
| **Compliance Burden** | Low (textile labeling) | Medium (CE, RoHS, SDS) | High (FDA, EU 1169, allergens) |
| **ERP Sync Direction** | PIM → ERP | Bidirectional | PIM → ERP |
| **MDM Needed?** | Rarely | Often (multiple sources) | Sometimes |
| **GS1 Complexity** | GTIN-13 only | Full hierarchy (4 levels) | Full hierarchy (3 levels) |
| **Media Focus** | Lifestyle photography | Technical drawings | Product + label photography |
| **Scoring Emphasis** | Media + Translation | Attribute + Translation | Attribute + Compliance |
| **Setup Time** | 1–2 weeks | 3–4 weeks | 2–3 weeks |

---

## Appendix B: Document Change Log

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | February 2026 | Implementation Team | Initial release — all 15 domains + 3 appendix sections |

---

## Appendix C: Glossary

| Term | Definition |
|------|-----------|
| **Bundle Pattern** | Drupal-inspired architecture where configuration entities (types) define the structure of content entities (records) |
| **EAV** | Entity-Attribute-Value — dynamic schema pattern where attributes are stored as rows rather than columns |
| **Product Family** | Core configuration entity that determines which attributes and variant axes apply to a set of products |
| **Product Master** | The parent product record containing shared data; generates Product Variants for individual SKUs |
| **Product Variant** | A specific SKU derived from a Product Master, differentiated by variant axis values (e.g., size + color) |
| **Channel** | A sales or distribution platform (e.g., Amazon, Shopify, Trendyol) where products are published |
| **Completeness Score** | Percentage indicating how many required fields for a given channel are populated |
| **Quality Score** | Multi-dimensional score (0–100) combining content, media, SEO, translation, attribute, and market readiness scores |
| **Golden Record** | The single authoritative record for a product created by merging data from multiple source systems (MDM) |
| **Survivorship Rule** | Field-level rules that determine which source system's value wins when merging conflicting data |
| **Data Steward** | A user assigned responsibility for product data quality within specific categories or product families |
| **Export Profile** | Configuration defining how products are exported: format, filters, field mapping, schedule |
| **NestedSet** | Frappe's tree structure implementation using left/right values for efficient hierarchy queries |
| **BMEcat** | European electronic product catalog standard (XML format) used in B2B procurement |
| **GS1** | Global Standards 1 — the organization managing GTIN barcodes, packaging hierarchy, and data standards |
| **GTIN** | Global Trade Item Number — the barcode number identifying products (GTIN-8, GTIN-13, GTIN-14) |
| **GDSN** | Global Data Synchronisation Network — GS1 standard for exchanging product data between trading partners |
