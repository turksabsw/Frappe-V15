# frappe_pim – Product Master, Attribute Engine ve Akıllı Formlar Mimarisi

## Amaç

Frappe PIM üzerinde:

- Doğru Product Family / Product / Product Type ayrımı
- Attribute şablon motoru
- Akıllı formlar ile veri üretimi
- Şablon → Attribute converter
- Master ekranını Item benzeri bağlantı merkezine dönüştürme
- Stok → Item → Variant zinciri
- SDS, ECHA, sektör bileşenleri, BOM, Price Rules entegrasyonu

---

## Kavramsal Model

### Ürün Hiyerarşisi

| Kavram | Açıklama |
|-------|----------|
| Product Family | Ürün ailesi (örn: Mouse) |
| Product Type | Ürün tipi (örn: Gaming Mouse, Office Mouse) |
| Product | Satılabilir ürün |
| Variant | Renk, kapasite, gramaj vb varyasyon |
| Item | ERP stok nesnesi |
| Package Type | Ambalaj tipi (entity) |

❌ [Klavye + Mouse] = Product Family değildir  
✅ Mouse = Product Family  

---

## Attribute Mimarisi

### Attribute Group
- Mantıksal gruplama
- UI-only
- Input içermez

### Attribute
- Gerçek veri alanı
- Input tipini belirler
- Color picker burada olur
- Unit destekler

### Attribute Type YOK
Sistem doğrudan Attribute + Input Type mantığı ile çalışır.

---

## Attribute Alan Tipleri

- Text
- Number
- Select
- Color Picker
- File
- Rich Text
- Unit Field

---

## Unit Sistemi

Her attribute birim destekler.


ÇIKTI:

---

## Attribute Template Engine (Şablon Motoru)

Amaç:
Besin değerleri, SDS, sektör bileşenleri gibi attribute setlerini şablonla üretmek.

### Attribute Template
- Template Name
- Sector
- Attribute List

### Template → Attribute Converter
- Şablondaki alanları gerçek Attribute’a dönüştürür
- Product Master’a otomatik bağlar

---

## Akıllı Form Motoru

Şablon bazlı dinamik formlar:

- Gıda formu
- Kozmetik formu
- Kimya (SDS) formu
- Vitamin formu

Akış:

Form → Attribute Values → Product Master


---

## Product Master Ekranı

Item ekranı mantığında tasarlanacak.

Alt bağlantılar:

- Attributes
- Variants
- Package Types
- BOM
- Price Rules
- SDS
- Content
- Contributors
- Comments
- Stock Items

Ürüne bakınca o ürünle ilgili her şey görünmeli.

---

## Contributors Sistemi

Product Master içinde:

| Rol | Sıra |
|-----|------|
| Ürün Yöneticisi | 1 |
| AR-GE | 2 |
| Kalite | 3 |
| Satınalma | 4 |

Alanlar:
- User
- Role
- Order
- Description

---

## Stok Zinciri

Product Master
↓
Item
↓
Variant
↓
Stock Ledger


---

## BOM Entegrasyonu

- BOM PIM ile ilişkili olacak
- BOM → Product Master bağlanacak
- BOM yoksa PIM üzerinden üretilecek

---

## Package Type Entity

- Ambalaj tipi ayrı entity
- Product Master’dan çağrılır
- Variant bazlı bağlanabilir

---

## SDS Modülü (ECHA)

- SDS Doctype
- ECHA Piktogramları
- SDS Standartları
- Ürün bazlı bağlanır

---

## Sektörel Bileşenler

Örnek:
- Vitaminler
- Mineraller
- Kimyasal bileşenler

Attribute Template olarak çalışır.

---

## Content Engine

- İçerik kategorisi seçilir
- İçerik otomatik üretilir
- Ürüne bağlanır
- Web Builder (Page Designer) ile entegre çalışır

---

## Price Engine

Price List → Price Rules → Product Master


---

## Mock Data Engine

- Ürünler için otomatik test datası üretir
- Variant + Attribute + Price üretir

---

## Translation Engine

- PIM içi çeviri yönetimi
- Attribute label çevirileri
- Product description çevirileri

---

## Yorum Sistemi (Hepsiburada Modeli)

- Kullanıcı ürün özelliklerine yorum yapar
- Öne çıkan özellikler işaretlenir
- Attribute bazlı yorumlar tutulur

---

## Nutrition Facts

Şimdilik opsiyonel.  
Tamamen Attribute Template üzerinden çalışır.

---

## Yeni Doctypelar

- Product Family
- Product Master
- Attribute
- Attribute Group
- Attribute Template
- Template Converter
- Smart Form
- Package Type
- SDS
- Sector Component
- Contributor
- Product Content
- Mock Data Engine

---

## Connections

Tüm Doctype bağlantıları Product Master alt panelinde listelenir.

---

## Sonuç

Bu mimari ile:

- Ürün ailesi doğru modellenir 
- Attribute sistemi modüler olur 
- Besin/SDS gibi yapılar şablondan üretilir 
- Ürün her şeyiyle tek ekranda yönetilir 
- ERP, stok, BOM, fiyat, içerik, yorum entegre çalışır 

---

Bu doküman AutoClaude için referans mimari ve geliştirme planıdır.
