
---

# Frappe PIM (Product Information Management) - Full System Prompt

## Proje Özeti

Frappe Framework üzerinde çalışan, ERPNext ile çift yönlü tam entegre, kurumsal düzeyde Product Information Management (PIM) uygulaması geliştir. Sistem ürün bilgilerini merkezi olarak yönetir, çoklu kanal/marketplace desteği sunar ve attribute-based variant yönetimi sağlar.

---

## 1. Core Entity Hiyerarşisi

### 1.1 Product Type
```
Doctype: PIM Product Type
Fields:
- title (Data, required)
- code (Data, unique, required) 
- description (Text Editor, translatable)
- default_attribute_template (Link → PIM Attribute Template)
- status (Select: Active/Inactive)
- icon (Attach Image)
```

### 1.2 Product Family
```
Doctype: PIM Product Family
Fields:
- title (Data, required)
- code (Data, unique, required)
- product_type (Link → PIM Product Type, required)
- description (Text Editor, translatable)
- default_attribute_template (Link → PIM Attribute Template)
- status (Select: Active/Inactive)
- icon (Attach Image)
```

### 1.3 Product Master (Template)
```
Doctype: PIM Product Master
Fields:
== Tab 1: Genel Bilgiler ==
- title (Data, required, translatable)
- code/sku (Data, unique, required)
- product_type (Link → PIM Product Type, required)
- product_family (Link → PIM Product Family, required, filtered by product_type)
- short_description (Small Text, translatable)
- description (Text Editor, translatable)
- status (Select: Draft/Active/Discontinued/Archived)
- is_template (Check) - varyant üretecekse true
- erpnext_item (Link → Item, read-only after sync)

== Tab 2: Kategoriler ==
- categories (Table MultiSelect → PIM Category)

== Tab 3: Attributes ==
- attribute_values (Child Table → PIM Product Attribute Value)

== Tab 4: Media ==
- media (Child Table → PIM Product Media)

== Tab 5: Fiyatlandırma ==
- pricing_entries (Virtual/Link list - Item Price'lardan çekilir)
- pricing_rules (Virtual/Link list)

== Tab 6: İlişkiler ==
- variants (Virtual list - bu master'a bağlı variant'lar)
- bundles (Link list - bu ürünün dahil olduğu bundle'lar)
- related_products (Table MultiSelect → PIM Product Master)
- package_types (Child Table → PIM Product Package)

== Tab 7: Sorumlular ==
- responsible_persons (Child Table → PIM Product Responsible)

== Tab 8: SEO & Çeviri ==
- seo_title (Data, translatable)
- seo_description (Small Text, translatable)
- seo_keywords (Data, translatable)
- url_slug (Data, translatable)
```

### 1.4 Product Variant
```
Doctype: PIM Product Variant
Fields:
- master (Link → PIM Product Master, required)
- sku (Data, unique, required)
- barcode (Data)
- status (Select: Active/Inactive/Out of Stock)
- source (Select: Generated/Manual)
- is_non_standard (Check) - kombinasyona uymayan manuel variant
- axis_values (Child Table → PIM Variant Axis Value)
- attribute_overrides (Child Table → PIM Product Attribute Value) - master'dan farklı değerler
- media_overrides (Child Table → PIM Product Media)
- erpnext_item (Link → Item, read-only after sync)
- price_overrides (sadece variant'a özel fiyat varsa)
```

---

## 2. Category / Taxonomy Sistemi

```
Doctype: PIM Category
Fields:
- title (Data, required, translatable)
- code (Data, unique, required)
- parent_category (Link → PIM Category) - sınırsız nested
- description (Text Editor, translatable)
- image (Attach Image)
- placeholder_image (Attach Image) - bu kategorideki ürünler için default
- sort_order (Int)
- status (Select: Active/Inactive)
- required_attributes (Child Table → PIM Category Required Attribute)
- is_leaf_only (Check) - sadece en alt seviyede ürün atanabilir mi

Child Table: PIM Category Required Attribute
- attribute (Link → PIM Attribute)
- is_required (Check)
- default_value (Data)
```

### RBAC/ABAC + RACI Framework
```
Doctype: PIM Category Permission
Fields:
- category (Link → PIM Category)
- role (Link → Role)
- permission_type (Select: View/Edit/Assign Products/Manage Attributes)
- raci_type (Select: Responsible/Accountable/Consulted/Informed)
- restrict_to_leaf (Check) - bu rol sadece leaf category'ye ürün atayabilir
```

---

## 3. Attribute Sistemi

### 3.1 Attribute Type
```
Doctype: PIM Attribute Type
Fields:
- name (Data, unique) - text, number, select, multiselect, color, boolean, date, measurement, reference
- storage_kind (Select: scalar/option_ref/option_multi_ref/json)
- base_data_type (Select: string/int/decimal/bool/date/json)
- supports_options (Check)
- supports_unit (Check)
- default_widget (Data) - color_picker, textbox, dropdown, checkbox, datepicker, number_input
- default_formatter (Data) - swatch, plain, range, badge
- validation_schema (JSON) - min, max, regex, precision vb.
```

### 3.2 Attribute Group
```
Doctype: PIM Attribute Group
Fields:
- title (Data, required, translatable)
- code (Data, unique)
- sort_order (Int)
- parent_group (Link → PIM Attribute Group) - nested grup için
- scope_categories (Table MultiSelect → PIM Category) - hangi kategorilerde görünür
```

### 3.3 Attribute
```
Doctype: PIM Attribute
Fields:
- label (Data, required, translatable)
- code (Data, unique, required)
- attribute_type (Link → PIM Attribute Type, required)
- attribute_group (Link → PIM Attribute Group)
- is_required (Check)
- is_variant_axis (Check) - varyant oluşturur mu
- is_translatable (Check)
- cardinality (Select: Single/Multiple)
- unit_group (Link → PIM Unit Group) - ml/gr/kg için
- default_value (Data)
- help_text (Small Text, translatable)
- widget_override (Data) - default widget'ı override et
- status (Select: Active/Deprecated)
- sort_order (Int)
- scope_rules (JSON) - kategori/kanal filtreleri
```

### 3.4 Attribute Option (Dictionary Values)
```
Doctype: PIM Attribute Option
Fields:
- attribute (Link → PIM Attribute, required)
- value_key (Data, required) - machine name: red, green
- label (Data, required, translatable)
- sort_order (Int)
- meta (JSON) - color için: {"hex": "#FF0000"}, measurement için: {"amount": 500, "unit": "ml"}
- status (Select: Active/Inactive)
```

### 3.5 Product Attribute Value
```
Doctype: PIM Product Attribute Value (Child Table)
Fields:
- attribute (Link → PIM Attribute, required)
- value_kind (Select: scalar/option/options)
- value_string (Data)
- value_number (Float)
- value_bool (Check)
- value_date (Date)
- option (Link → PIM Attribute Option) - select için
- options (JSON - array of option links) - multiselect için
- raw_json (JSON) - complex tipler
- source (Select: Manual/Import/Integration/Inherited)
- locale (Link → Language) - translatable ise
```

### 3.6 Variant Axis Value
```
Doctype: PIM Variant Axis Value (Child Table)
Fields:
- attribute (Link → PIM Attribute, required) - is_variant_axis=true olmalı
- option (Link → PIM Attribute Option, required)
```

### 3.7 Attribute Template
```
Doctype: PIM Attribute Template
Fields:
- title (Data, required)
- code (Data, unique)
- description (Text)
- template_attributes (Child Table → PIM Template Attribute Item)

Child Table: PIM Template Attribute Item
- attribute (Link → PIM Attribute)
- is_required (Check)
- default_value (Data)
- sort_order (Int)
```

**Template → Attribute Converter:** 
- Template seçildiğinde "Generate Attributes" butonu ile Attribute + Options otomatik oluşur
- Template export (JSON/Excel) yapılabilir, düzenlenip import edilebilir

---

## 4. Media Sistemi

### 4.1 Product Media
```
Doctype: PIM Product Media (Child Table)
Fields:
- file (Attach, required)
- media_type (Select: Image/Video/Document/3D Model)
- is_primary (Check)
- alt_text (Data, translatable)
- sort_order (Int)
- usage_context (Select: Thumbnail/Gallery/Zoom/Lifestyle/Technical/Certificate)
- title (Data, translatable)
```

### 4.2 Media Asset Library
```
Doctype: PIM Media Asset
Fields:
- file (Attach, required)
- title (Data, required)
- media_type (Select: Image/Video/Document/3D Model/Logo/Certificate)
- tags (Table MultiSelect → PIM Media Tag)
- usage_rights (Text)
- expiry_date (Date)
- auto_optimize (Check, default: true)
- optimization_settings (JSON) - thumbnail size, compression level vb.
```

**Otomatik Optimizasyon:**
- Upload sırasında thumbnail, medium, large versiyonlar oluştur
- WebP formatına dönüştür (opsiyonel)
- Options panel ile boyut/kalite ayarlanabilir

---

## 5. Package Types

```
Doctype: PIM Package Type
Fields:
- title (Data, required)
- code (Data, unique)
- package_type (Select: Box/Bag/Pallet/Carton/Envelope/Tube/Other)
- dimensions_length (Float)
- dimensions_width (Float)
- dimensions_height (Float)
- dimension_unit (Select: cm/mm/m/inch)
- weight_gross (Float)
- weight_net (Float)
- weight_unit (Select: g/kg/lb/oz)
- barcode (Data) - GTIN-14 vb.
- barcode_type (Select: GTIN-14/SSCC/Custom)
- units_per_package (Int) - 1 koli = 12 adet
- is_default (Check)
```

```
Doctype: PIM Product Package (Child Table)
Fields:
- package_type (Link → PIM Package Type, required)
- units_count (Int) - bu pakette kaç adet var
- custom_barcode (Data) - ürüne özel barkod override
- custom_dimensions (JSON) - override dimensions
```

---

## 6. Product Responsible

```
Doctype: PIM Product Responsible (Child Table)
Fields:
- user (Link → User, required)
- role_type (Select: Category Manager/Content Editor/Pricing Admin/QC Reviewer/Product Owner/Translator)
- department (Link → Department)
- notify_on_change (Check)
- notification_types (MultiSelect: Create/Update/Price Change/Stock Change/Status Change)
```

---

## 7. Bundle Sistemi

### 7.1 Bundle Master
```
Doctype: PIM Bundle
Fields:
- title (Data, required, translatable)
- code (Data, unique, required)
- bundle_type (Select: Static/Configurable/Dynamic/Build Your Own)
- description (Text Editor, translatable)
- status (Select: Draft/Active/Scheduled/Expired/Inactive)
- image (Attach Image)

== Kompozisyon ==
- slots (Child Table → PIM Bundle Slot)
- dependency_rules (Child Table → PIM Bundle Dependency Rule)
- max_total_items (Int) - Build Your Own için

== Fiyatlandırma ==
- pricing_model (Select: Fixed Price/Percentage Discount/Per Item Discount/Tiered/Buy X Pay Y)
- fixed_price (Currency)
- discount_percentage (Percent)
- discount_amount (Currency)
- min_price_limit (Currency)
- max_price_limit (Currency)
- tiered_pricing (Child Table → PIM Bundle Tier)

== Geçerlilik ==
- valid_from (Datetime)
- valid_to (Datetime)
- channels (Table MultiSelect → PIM Sales Channel)
- customer_segments (Table MultiSelect → PIM Customer Segment)

== Stok Kuralları ==
- stock_behavior (Select: Deactivate When Out/Show Warning/Offer Alternative)
- min_stock_threshold (Int)
- allow_partial_fulfillment (Check)
- reserve_stock (Check)

== ERPNext ==
- erpnext_item (Link → Item) - bundle item olarak
- create_as_bom (Check) - false, BOM ERPNext'te kalacak
```

### 7.2 Bundle Slot
```
Doctype: PIM Bundle Slot (Child Table)
Fields:
- title (Data, required)
- slot_type (Select: Fixed Product/Category Pool/Tag Pool/Manual List)
- is_required (Check)
- min_quantity (Int, default: 1)
- max_quantity (Int, default: 1)
- default_product (Link → PIM Product Master)
- category_filter (Link → PIM Category)
- tag_filter (Data)
- allowed_products (Table MultiSelect → PIM Product Master) - manual list için
- sort_order (Int)
- price_override (Currency) - bu slot için özel fiyat
- discount_override (Percent)
```

### 7.3 Bundle Dependency Rule
```
Doctype: PIM Bundle Dependency Rule (Child Table)
Fields:
- rule_type (Select: Requires/Excludes/Recommends)
- if_product (Link → PIM Product Master)
- then_product (Link → PIM Product Master)
- message (Data, translatable) - UI'da gösterilecek mesaj
```

### 7.4 Bundle Tier
```
Doctype: PIM Bundle Tier (Child Table)
Fields:
- min_items (Int)
- max_items (Int)
- discount_percentage (Percent)
- discount_amount (Currency)
```

---

## 8. Fiyatlandırma Sistemi

### 8.1 Sales Channel
```
Doctype: PIM Sales Channel
Fields:
- title (Data, required)
- code (Data, unique, required) - amazon_us, trendyol_tr, wholesale_tr
- channel_type (Select: E-commerce/Marketplace/Wholesale/Retail/B2B Portal)
- currency (Link → Currency, required)
- region (Data)
- tax_included (Check)
- rounding_policy (Select: None/Round to 0.99/Round to nearest 0.5)
- price_sync_enabled (Check)
- sync_direction (Select: Push/Pull/Bidirectional)
- api_config (JSON) - marketplace API bilgileri
```

### 8.2 Channel Price List Map
```
Doctype: PIM Channel Price List Map
Fields:
- sales_channel (Link → PIM Sales Channel, required)
- price_list (Link → Price List, required) - ERPNext Price List
- fallback_price_list (Link → Price List)
- priority (Int)
- is_primary (Check)
```

### 8.3 Customer Segment
```
Doctype: PIM Customer Segment
Fields:
- title (Data, required)
- code (Data, unique)
- tier (Select: Retail/Wholesale/Distributor/Reseller/VIP)
- default_discount_percentage (Percent)
- min_order_value (Currency)
- payment_terms_template (Link → Payment Terms Template)
- price_list (Link → Price List)
```

### 8.4 Contract Price
```
Doctype: PIM Contract Price
Fields:
- customer (Link → Customer)
- customer_group (Link → Customer Group)
- product (Link → PIM Product Master)
- variant (Link → PIM Product Variant)
- price (Currency)
- discount_percentage (Percent)
- min_quantity (Float)
- uom (Link → UOM)
- valid_from (Date, required)
- valid_to (Date, required)
- status (Select: Active/Expired/Pending Approval)
```

### 8.5 Marketplace Listing
```
Doctype: PIM Marketplace Listing
Fields:
- sales_channel (Link → PIM Sales Channel, required)
- product (Link → PIM Product Master)
- variant (Link → PIM Product Variant)
- listing_id (Data) - Amazon ASIN, eBay Item ID vb.
- listing_url (Data)
- min_price (Currency) - repricing guardrail
- max_price (Currency) - repricing guardrail
- status (Select: Active/Paused/Pending/Rejected)
- last_sync (Datetime)
- sync_errors (Text)
```

### 8.6 Price Resolution API
```python
def get_final_price(sku, channel, customer=None, qty=1, currency=None, date=None):
    """
    Fiyat çözümleme sırası:
    1. Contract/Account Price (müşteri özel)
    2. Channel Listing override (marketplace listing bazlı)
    3. Channel Primary Price List → Item Price (qty break + validity + uom)
    4. Fallback Price List
    5. Currency conversion + rounding policy
    6. Pricing Rule(lar) (segment + channel + coupon + qty)
    7. Guardrails (min/max, margin floor)
    
    Returns: {
        "final_unit_price": Decimal,
        "original_price": Decimal,
        "discount_amount": Decimal,
        "applied_rules": [...],
        "source_trace": [...],  # Debug için
        "currency": str
    }
    """
```

---

## 9. ERPNext Entegrasyonu

### 9.1 Sync Mekanizması
```
Doctype: PIM Sync Queue
Fields:
- doctype (Data) - PIM Product Master, PIM Product Variant vb.
- docname (Data)
- sync_direction (Select: PIM to ERPNext/ERPNext to PIM)
- sync_type (Select: Create/Update/Delete)
- status (Select: Pending/Processing/Completed/Failed/Retry)
- priority (Int)
- payload (JSON)
- error_message (Text)
- retry_count (Int)
- created_at (Datetime)
- processed_at (Datetime)
```

### 9.2 Sync Rules
- **Realtime tetikleme:** Her save/update'te queue'ya ekle
- **Queue işleme:** Background job ile 1-5 saniye içinde işle
- **Hata yönetimi:** 
  - Hata olursa retry (max 3)
  - 3 retry sonrası admin'e notification
  - Dead letter queue'ya taşı
  - Sistem çalışmaya devam etsin, hata vermesi

### 9.3 Field Mapping
```
PIM Product Master ↔ ERPNext Item
- title → item_name
- code/sku → item_code
- description → description
- product_family → item_group
- is_template → has_variants
- attribute_values → item attributes (via Item Variant Attribute)
- media[0] → image

PIM Product Variant ↔ ERPNext Item (Variant)
- sku → item_code
- master.erpnext_item → variant_of
- axis_values → attributes

PIM Bundle → ERPNext Item (is_stock_item=0, is_sales_item=1)
- slots → Product Bundle Item (ERPNext core doctype)
```

### 9.4 Conflict Resolution
```
Doctype: PIM Sync Conflict Rule
Fields:
- field_name (Data)
- master_source (Select: PIM/ERPNext/Last Modified)
- description (Text)

Default Rules:
- description, media, attributes → PIM master
- stock_qty, warehouse → ERPNext master  
- price → Last modified wins, log conflict
- Ortak olmayan alanlar → Her iki tarafta bağımsız kalır
```

---

## 10. Export Sistemi

### 10.1 Export Profile
```
Doctype: PIM Export Profile
Fields:
- title (Data, required)
- code (Data, unique)
- export_format (Select: CSV/Excel/JSON/XML)
- target_channel (Link → PIM Sales Channel) - Amazon Export, Trendyol Export vb.
- include_variants (Check)
- include_media_urls (Check)
- language (Link → Language)
- field_mappings (Child Table → PIM Export Field Mapping)
- filters (JSON) - category, status vb. filtreler
- created_by (Link → User)
```

### 10.2 Export Field Mapping
```
Doctype: PIM Export Field Mapping (Child Table)
Fields:
- source_field (Data) - PIM field path: title, attributes.color.value
- target_field (Data) - Export column name
- transform (Select: None/Uppercase/Lowercase/Truncate/Custom)
- transform_config (JSON)
- default_value (Data)
- is_required (Check)
- sort_order (Int)
```

---

## 11. Çeviri Sistemi

### 11.1 Kurallar
- **Çevrilebilir:** title, description, short_description, seo fields, alt_text, attribute labels (anlam taşıyan)
- **Çevrilemez:** sku, barcode, code alanları, standart kodları (IP67, AISI 304)
- **Özel isimler:** Marka adı çevrilmez, marka açıklaması çevrilir

### 11.2 Frappe Translation Entegrasyonu
- `translatable` flag'li alanlar için Frappe'nin mevcut Translation sistemi kullanılacak
- Attribute Option label'ları için ayrı translation entry
- Fallback: Çeviri yoksa default language'a düş

### 11.3 Translation Status Tracking
```
Doctype: PIM Translation Status
Fields:
- reference_doctype (Data)
- reference_name (Data)
- language (Link → Language)
- status (Select: Not Started/In Progress/Completed/Needs Review)
- completion_percentage (Percent)
- last_updated (Datetime)
- translator (Link → User)
```

---

## 12. UI/UX Gereksinimleri

### 12.1 Wizard (Step-by-Step Form)
Yeni ürün oluştururken:
```
Step 1: Temel Bilgiler
- Product Type seç
- Product Family seç (filtered by type)
- Title, SKU gir

Step 2: Kategori Seçimi
- Kategori ağacından seç (multi-select)
- Leaf-only kuralı varsa uygula

Step 3: Attribute Template / Attributes
- Template seç → Otomatik attribute'lar gelsin
- Değerleri gir
- "+" ile ek attribute ekle

Step 4: Media Upload
- Drag-drop upload
- Primary image seç
- Alt text gir

Step 5: Pricing (Opsiyonel)
- Temel fiyat gir
- İstenirse atla, sonra girilebilir

Step 6: Review & Save
- Özet göster
- Validation check
- Save & Create Variants / Save & Exit
```

### 12.2 Tab Yapısı (Edit Mode)
```
Tab 1: Genel Bilgiler - Temel alanlar, açıklamalar
Tab 2: Kategoriler - Kategori ataması
Tab 3: Attributes - Attribute değerleri, "+" ile ekleme
Tab 4: Media - Dosya yönetimi, sıralama
Tab 5: Fiyatlandırma - Price list entries, pricing rules
Tab 6: İlişkiler - Variants, Bundles, Related Products, Package Types
Tab 7: Sorumlular - Responsible persons
Tab 8: SEO & Çeviri - SEO alanları, çeviri durumu
```

### 12.3 Liste Görünümü
- Thumbnail göster (yoksa kategori placeholder)
- SKU, Title, Type, Family, Status kolonları
- Quick filters: Status, Category, Product Type
- Bulk actions: Status change, Category assign, Export

### 12.4 Connections (Alt Panel)
Product Master ekranının altında dinamik bağlantılar:
- Variants (bu master'ın variant'ları)
- Bundles (bu ürünün dahil olduğu)
- Price Entries (tüm channel'lardaki fiyatlar)
- Media Assets
- ERPNext Item (link)
- Marketplace Listings
- Related Products
- Sync History

### 12.5 Variant Oluşturma UI
```
1. Master'da "Create Variants" butonu
2. Axis Attribute seç (is_variant_axis=true olanlar)
3. Her axis için option'ları seç
4. Kombinasyon önizleme göster
5. SKU pattern belirle (MASTER-{color}-{size})
6. Generate butonu → Variants oluşsun
7. Manuel variant için "Add Manual Variant" butonu
```

### 12.6 Bundle Builder UI
```
Simple Mode:
- Ürün listesi + miktar + tek fiyat

Advanced Mode:
- Slot tanımla (drag-drop)
- Her slot için ürün havuzu belirle
- Dependency kuralları ekle
- Fiyatlandırma modeli seç
- Geçerlilik ayarları
- Preview & Test
```

---

## 13. Validations & Business Rules

### 13.1 Product Master
- SKU unique olmalı
- is_template=true ise en az 1 variant axis attribute olmalı
- Kategori zorunlu attribute'ları doldurulmalı
- Media'da en az 1 primary image olmalı (opsiyonel kural)

### 13.2 Variant
- Master ile aynı SKU olamaz
- Axis value kombinasyonu unique olmalı (aynı master altında)
- Generated variant'ın axis value'ları değiştirilemez

### 13.3 Bundle
- En az 1 slot olmalı
- Static bundle'da tüm slot'lar fixed product olmalı
- Circular dependency olamaz (A requires B, B requires A)
- Valid_to > valid_from olmalı

### 13.4 Category
- Circular parent reference olamaz
- is_leaf_only kategori, parent olamaz

---

## 14. Notifications & Alerts

```
Doctype: PIM Notification Rule
Fields:
- title (Data)
- trigger_doctype (Data)
- trigger_event (Select: Create/Update/Delete/Status Change/Price Change/Stock Low)
- condition (Code) - frappe condition
- recipients (Table MultiSelect → User)
- recipient_roles (Table MultiSelect → Role)
- channel (Select: Email/System Notification/Slack/Webhook)
- message_template (Text)
- is_active (Check)
```

Default Notifications:
- Sync hatası → Admin
- Stok kritik seviye → Product Owner
- Fiyat değişikliği → Pricing Admin
- Yeni ürün → Category Manager

---

## 15. Technical Requirements

### 15.1 Frappe Hooks
```python
# hooks.py
doc_events = {
    "PIM Product Master": {
        "after_insert": "pim.events.product.after_insert",
        "on_update": "pim.events.product.on_update",
        "on_trash": "pim.events.product.on_trash"
    },
    "Item": {
        "on_update": "pim.events.item.sync_from_erpnext"
    }
}

scheduler_events = {
    "cron": {
        "*/1 * * * *": ["pim.tasks.process_sync_queue"]  # Her dakika
    }
}
```

### 15.2 API Endpoints
```
/api/method/pim.api.get_product - Ürün detay
/api/method/pim.api.search_products - Arama
/api/method/pim.api.get_final_price - Fiyat hesaplama
/api/method/pim.api.export_products - Export
/api/method/pim.api.generate_variants - Variant üretimi
/api/method/pim.api.sync_status - Sync durumu
```

### 15.3 Permissions
```
Role: PIM Admin - Full access
Role: PIM Product Manager - CRUD on products, read on settings
Role: PIM Content Editor - Edit product content, no delete
Role: PIM Pricing Manager - Edit pricing, read on products
Role: PIM Viewer - Read only

Category-based permissions via PIM Category Permission doctype
```

---

## 16. Dosya Yapısı

```
frappe-bench/apps/pim/
├── pim/
│   ├── pim/
│   │   ├── doctype/
│   │   │   ├── pim_product_master/
│   │   │   ├── pim_product_variant/
│   │   │   ├── pim_product_type/
│   │   │   ├── pim_product_family/
│   │   │   ├── pim_category/
│   │   │   ├── pim_attribute_type/
│   │   │   ├── pim_attribute_group/
│   │   │   ├── pim_attribute/
│   │   │   ├── pim_attribute_option/
│   │   │   ├── pim_attribute_template/
│   │   │   ├── pim_bundle/
│   │   │   ├── pim_sales_channel/
│   │   │   ├── pim_customer_segment/
│   │   │   ├── pim_contract_price/
│   │   │   ├── pim_marketplace_listing/
│   │   │   ├── pim_export_profile/
│   │   │   ├── pim_package_type/
│   │   │   ├── pim_sync_queue/
│   │   │   └── ... (child tables)
│   │   ├── workspace/
│   │   │   └── pim.json
│   │   └── report/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── product.py
│   │   ├── pricing.py
│   │   └── sync.py
│   ├── events/
│   │   ├── product.py
│   │   └── item.py
│   ├── tasks/
│   │   ├── sync.py
│   │   └── export.py
│   ├── utils/
│   │   ├── price_resolver.py
│   │   ├── variant_generator.py
│   │   └── media_optimizer.py
│   ├── hooks.py
│   └── patches/
├── setup.py
└── requirements.txt
```

---
