# PIM Özelleştirme Kılavuzu

## Kapsamlı Müşteri Bazlı Kurulum ve Yapılandırma Referansı

**Versiyon:** 1.0
**Son Güncelleme:** Şubat 2026
**Hedef Kitle:** Uygulama Ekipleri, Çözüm Mimarları, Müşteri Başarı Mühendisleri
**Kapsam:** Frappe PIM v15+ — 101 DocType, 24 Yardımcı Modül, 15 API Uç Noktası, 5 Servis Katmanı

---

## Yönetici Özeti

Frappe PIM, Frappe v15+ üzerine inşa edilmiş, derin ERPNext entegrasyonu olan kurumsal düzeyde bir Ürün Bilgi Yönetimi sistemidir. Yapılandırma varlıklarının (Ürün Tipleri, Öznitelik Tipleri, Ürün Aileleri) içerik varlıkları (Ürün Ana Kaydı, Ürün Varyantı, PIM Özniteliği) için alan yapısını ve davranışı tanımladığı **Drupal tarzı tip/paket deseni** izler.

Bu belge, müşteri kurulumu sırasında mevcut olan **her özelleştirme yüzeyini** 15 alan altında organize ederek kataloglar. Her özelleştirme noktası şunları içerir:

- **Ne olduğu** — DocType, alan veya yapılandırma seçeneği
- **Ne zaman yapılandırılacağı** — hangi kurulum aşamasında ayarlanması gerektiği
- **Kim yapılandıracak** — sorumlu rol (System Manager, PIM Manager, PIM User)
- **İş etkisi** — yapılandırmanın hangi iş sonucunu yönlendirdiği

### Bu Kılavuz Nasıl Kullanılır

1. **Yeni Dağıtımlar (Sıfırdan Kurulum):** Önerilen Kurulum Sıralamasını (Bölüm 16) baştan sona takip edin
2. **Göçler:** Göçe özel rehberlik için Uç Durumlar bölümünü (Bölüm 17) kullanın, ardından ilgili alan bölümlerini seçici olarak takip edin
3. **Mevcut Kurulumu Genişletme:** İlgili özelleştirme alanı bölümüne doğrudan atlayın

---

## İçindekiler

### Özelleştirme Alanları (Bölüm 1–15)

1. [Tip Sistemi (Drupal Tarzı Paket Deseni)](#1-tip-sistemi-drupal-tarzı-paket-deseni)
2. [Öznitelik Sistemi (EAV Deseni)](#2-öznitelik-sistemi-eav-deseni)
3. [Genel Ayarlar (PIM Ayarları)](#3-genel-ayarlar-pim-ayarları)
4. [Kanal Yapılandırması](#4-kanal-yapılandırması)
5. [İş Akışı ve Yaşam Döngüsü](#5-iş-akışı-ve-yaşam-döngüsü)
6. [Puanlama ve Kalite](#6-puanlama-ve-kalite)
7. [ERPNext Entegrasyonu](#7-erpnext-entegrasyonu)
8. [Roller ve İzinler](#8-roller-ve-izinler)
9. [Taksonomi ve Navigasyon](#9-taksonomi-ve-navigasyon)
10. [Yapay Zeka ve Zenginleştirme](#10-yapay-zeka-ve-zenginleştirme)
11. [Medya ve Dijital Varlıklar](#11-medya-ve-dijital-varlıklar)
12. [Dışa Aktarım ve Entegrasyon](#12-dışa-aktarım-ve-entegrasyon)
13. [Uluslararasılaştırma](#13-uluslararasılaştırma)
14. [Paketleme ve Ambalajlama](#14-paketleme-ve-ambalajlama)
15. [MDM (Ana Veri Yönetimi)](#15-mdm-ana-veri-yönetimi)

### Uygulama ve Kurulum (Bölüm 16–18)

16. [Önerilen Kurulum Yapılandırma Sıralaması](#16-önerilen-kurulum-yapılandırma-sıralaması)
    - Faz 0: Genel Yapılandırma (PIM Ayarları)
    - Faz 1: Temel Şema (Öznitelik Tipleri, Gruplar, Öznitelikler, Aileler)
    - Faz 2: İçerik Altyapısı (Ürün Tipleri, Kategoriler, Markalar)
    - Faz 3: Kalite ve Yönetişim (Roller, İzinler, Kalite Politikaları)
    - Faz 4: Kanal ve Dışa Aktarım Kurulumu (Kanallar, Dışa Aktarım Profilleri)
    - Faz 5: Gelişmiş Özellikler (Yapay Zeka, GS1, Paketleme, MDM)
    - Faz 6: İçerik Oluşturma (Ürünler, Varyantlar, Medya)
    - Faz 7: Canlıya Geçiş (İş Akışı, Yayınlama, Senkronizasyon Aktivasyonu)
17. [Uç Durumlar ve Dağıtım Senaryoları](#17-uç-durumlar-ve-dağıtım-senaryoları)
    - 17.1 Sıfırdan Kurulum vs. Göç
    - 17.2 Tek Şirket vs. Çoklu Şirket
    - 17.3 ERPNext İle vs. ERPNext Olmadan
    - 17.4 Minimal vs. Tam Kurulum
    - 17.5 Yaygın Dağıtım Desenleri
18. [Müşteri Arketip Detaylı İncelemeleri](#18-müşteri-arketip-detaylı-incelemeleri)
    - 18.1 Moda Perakendecisi (tam yapılandırma profili)
    - 18.2 Endüstriyel Tedarikçi (tam yapılandırma profili)
    - 18.3 Gıda Üreticisi (tam yapılandırma profili)
    - 18.4 Arketip Karşılaştırma Matrisi

### Ekler

- [Ek A: Ek Yapılandırılabilir Varlıklar](#ek-a-ek-yapılandırılabilir-varlıklar)
- [Ek B: Belge Değişiklik Günlüğü](#ek-b-belge-değişiklik-günlüğü)
- [Ek C: Sözlük](#ek-c-sözlük)

---

## 1. Tip Sistemi (Drupal Tarzı Paket Deseni)

### Genel Bakış

PIM, *yapılandırma varlıklarını* (yapıyı tanımlayan) *içerik varlıklarından* (ürün verilerini tutan) ayıran bir **Drupal tarzı tip/paket deseni** uygular. Bu desen, her müşterinin kod değişikliği olmadan kendi ürün veri modelini tanımlamasını sağlar.

**Mimari:**

```
┌─────────────────────┐     ┌──────────────────────┐     ┌────────────────────┐
│  PIM Product Type    │────▶│   Product Family      │────▶│   Product Master    │
│  (Paket Tanımı)      │     │   (Öznitelik Şablonu) │     │   (İçerik Varlığı)  │
└─────────────────────┘     └──────────────────────┘     └────────────────────┘
         │                           │                           │
         │                           │                           ▼
         │                           │                   ┌────────────────────┐
         │                           │                   │   Product Variant   │
         │                           │                   │   (SKU düzeyi)      │
         │                           ▼                   └────────────────────┘
         │                  ┌──────────────────────┐
         │                  │ Family Attribute      │
         │                  │ Template (alt tablo)  │
         │                  └──────────────────────┘
         ▼
┌─────────────────────┐
│  PIM Attribute Type  │
│  (Veri Tipi Tanımı)  │
└─────────────────────┘
```

### 1.1 PIM Product Type

**DocType:** `PIM Product Type`
**Amaç:** Ortak yapısal özelliklere sahip bir ürün kategorisi tanımlar — Drupal terminolojisindeki "paket".

> **Not:** Bu DocType, ürünlerin üst düzey sınıflandırmasını tanımlar. JSON tanımı tüm kurulumlarda mevcut olmayabilir (Frappe'nin DocType oluşturucu aracılığıyla oluşturulabilir), ancak kavramsal rolü tip sistemi için merkezidir.

**Özelleştirme Noktaları:**

| Alan | Tip | Amaç | Özelleştirme Etkisi |
|------|-----|------|---------------------|
| `type_name` | Data | Ürün tipinin görünen adı | Müşteriye özel ürün taksonomisi |
| `type_code` | Data | Benzersiz kısa tanımlayıcı | Dahili referans, API çağrılarını etkiler |
| `product_family` | Link → Product Family | Bu tip için varsayılan aile | Ürünlerde hangi özniteliklerin görüneceğini belirler |
| `fields` | Table → Product Type Field | Bu tip için özel alanlar | Tipe göre temel ürün formunu genişletir |
| `has_variants` | Check | Bu tipteki ürünlerin SKU varyantlarını destekleyip desteklemediği | İş modeli kararı |
| `description` | Text | Tip açıklaması | İçerik ekipleri için dokümantasyon |

**Ne Zaman Yapılandırılır:** Kurulumun 1. Fazı — PIM Ayarlarından hemen sonra
**Kim Yapılandırır:** PIM Manager veya Çözüm Mimarı
**İş Etkisi:** Tüm dağıtım için temel ürün veri modelini belirler

#### Müşteri Arketip Örnekleri — Ürün Tipleri

**Moda Perakendecisi:**
```
Ürün Tipleri:
  ├── Giyim           → has_variants: ✓  (Beden, Renk)
  ├── Ayakkabı        → has_variants: ✓  (Beden, Genişlik, Renk)
  ├── Aksesuar        → has_variants: ✓  (Renk, Malzeme)
  └── Hediye Kartları → has_variants: ✗
```

**Endüstriyel Tedarikçi:**
```
Ürün Tipleri:
  ├── Hammadde         → has_variants: ✗
  ├── Bileşen          → has_variants: ✓  (Derece, Tolerans)
  ├── Montaj           → has_variants: ✓  (Yapılandırma)
  ├── Takım            → has_variants: ✗
  └── Güvenlik Ekipmanı → has_variants: ✓  (Beden)
```

**Gıda Üreticisi:**
```
Ürün Tipleri:
  ├── Taze Ürün     → has_variants: ✓  (Ağırlık, Paket Boyutu)
  ├── Paketli Gıda  → has_variants: ✓  (Paket Boyutu, Lezzet)
  ├── İçecek        → has_variants: ✓  (Hacim, Lezzet)
  └── Hammadde      → has_variants: ✓  (Derece, Ağırlık)
```

### 1.2 PIM Attribute Type

**DocType:** `PIM Attribute Type`
**Amaç:** Ürün öznitelikleri için mevcut veri tiplerini tanımlar. Bu, hangi tür değerlerin saklanabileceğini kontrol eden üst veri katmanıdır.

**Özelleştirme Noktaları:**

| Alan | Tip | Amaç | Özelleştirme Etkisi |
|------|-----|------|---------------------|
| `type_name` | Data | Görünen ad | Arayüz etiketlemesi |
| `type_code` | Data | Benzersiz tanımlayıcı kısa ad | PIM Attribute `data_type` tarafından referans alınır |
| `base_type` | Select | Temel depolama tipi | Doğrulama davranışını belirler |
| `validation_rules` | JSON/Text | Tipe özel doğrulama | Veri kalitesi uygulaması |

**Desteklenen Veri Tipleri (toplam 12):**

| Veri Tipi | Depolama Alanı | Kullanım Örneği |
|-----------|----------------|-----------------|
| `Text` | `value_text` | Ürün adı, kısa açıklama |
| `Long Text` | `value_long_text` | Tam ürün açıklaması, bakım talimatları |
| `Integer` | `value_int` | Paket miktarı, minimum sipariş miktarı |
| `Float` | `value_float` | Ağırlık, boyutlar, yüzde değerleri |
| `Select` | `value_text` | Malzeme tipi, hedef cinsiyet, sezon |
| `Multi Select` | `value_text` | Geçerli sertifikalar, özellik listesi |
| `Boolean` | `value_boolean` | Organik mi, geri dönüştürülebilir mi, alerjen içerir mi |
| `Date` | `value_date` | Üretim tarihi, son kullanma tarihi |
| `Datetime` | `value_datetime` | Son kalite kontrol zaman damgası |
| `Link` | `value_link` | Başka bir DocType kaydına referans |
| `Image` | `value_text` | Teknik çizim, sertifika görseli |
| `File` | `value_text` | Güvenlik veri sayfası, kullanım kılavuzu PDF |

**Ne Zaman Yapılandırılır:** Faz 1 — PIM Öznitelikleri oluşturmadan önce
**Kim Yapılandırır:** System Manager (genellikle tek seferlik kurulum)
**İş Etkisi:** Ürünler hakkında yakalanabilecek veri türlerini kısıtlar; yanlış tip seçimi veri kalitesi sorunlarına yol açar

### 1.3 Product Family

**DocType:** `Product Family`
**Modül:** PIM
**Adlandırma Kuralı:** `field:family_code` (`family_code` alanına göre adlandırılır)
**Ağaç Yapısı:** Evet (`is_tree: true`, `nsm_parent_field: parent_family`) — Frappe'nin NestedSet deseni kullanılarak hiyerarşik aile yapılarını destekler.

Product Family, tip sistemini öznitelik sistemiyle birleştiren **merkezi yapılandırma varlığıdır**. Her Product Master tam olarak bir Product Family'ye ait olmalıdır ve bu aile şunları belirler:

1. Ürün formunda hangi özniteliklerin görüneceği (`Family Attribute Template` aracılığıyla)
2. Hangi özniteliklerin varyantları tanımladığı (`Family Variant Attribute` aracılığıyla)
3. SKU ön ek adlandırma kuralları
4. Medya gereksinimleri
5. Tamlık eşikleri
6. ERP Item Group eşlemesi

#### Yapılandırılabilir Alanlar

| Alan | Tip | Varsayılan | Amaç | Müşteri Bazlı Etki |
|------|-----|-----------|------|---------------------|
| `family_name` | Data (zorunlu, çevrilebilir) | — | Görünen ad | Müşteri diline göre yerelleştirilir |
| `family_code` | Data (zorunlu, benzersiz) | — | Benzersiz kısa tanımlayıcı | API çağrılarında, SKU oluşturmada kullanılır |
| `parent_family` | Link → Product Family | — | Hiyerarşideki üst eleman | Öznitelik kalıtımını etkinleştirir |
| `naming_series_prefix` | Data | — | SKU ön eki (ör. `TSH-`, `ELK-`) | Otomatik oluşturulan ürün kodlarını yönlendirir |
| `is_active` | Check | `1` | Aileyi etkinleştir/devre dışı bırak | Ürün oluşturma uygunluğunu kontrol eder |
| `allow_variants` | Check | `1` | Ürünlerin SKU varyantları olabilir | Temel iş modeli kararı |
| `inherit_parent_attributes` | Check | `1` | Üst aile özniteliklerini otomatik dahil et | Yapılandırma tekrarını azaltır |
| `erp_item_group` | Link → Item Group | — | ERPNext Item Group eşlemesi | ERP senkronizasyonu için gerekli; PIM ailesini ERP hiyerarşisine eşler |
| `attributes` | Table → Family Attribute Template | — | Bu aile için öznitelik atamaları | **Temel özelleştirme yüzeyi** — ürün veri modelini tanımlar |
| `variant_attributes` | Table MultiSelect → Family Variant Attribute | — | Varyantları tanımlayan öznitelikler | SKU oluşturma eksenlerini belirler |
| `required_media_types` | Small Text | — | Virgülle ayrılmış medya tipleri (ör. `Ana Görsel, Galeri, Video`) | Kanala özel medya gereksinimleri |
| `min_images` | Int | `1` | Ürün başına gereken minimum görsel sayısı | Yayınlama için kalite kapısı |
| `completeness_threshold` | Percent | `80` | "Tamamlanmış" sayılması için gereken minimum tamlık puanı | Kalite kapısı eşiği |
| `description` | Text Editor | — | Aile açıklaması | Dahili dokümantasyon |

#### Alt Tablo: Family Attribute Template

**DocType:** `Family Attribute Template` (alt tablo, `istable: 1`)

Bu alt tablo, PIM Özniteliklerini bir Product Family'ye bağlayarak, bu aileye ait ürünlerde hangi özniteliklerin görüneceğini ve nasıl davranacağını tanımlar.

| Alan | Tip | Amaç |
|------|-----|------|
| `attribute` | Link → PIM Attribute (zorunlu) | Hangi özniteliğin dahil edileceği |
| `is_required_in_family` | Check (varsayılan: 0) | Bu özniteliğin bu ailedeki ürünler için zorunlu olup olmadığı |
| `default_value` | Small Text | Yeni ürünler için önceden doldurulmuş değer |
| `sort_order` | Int (varsayılan: 0) | Ürün formundaki görüntüleme sırası |

#### Alt Tablo: Family Variant Attribute

**DocType:** `Family Variant Attribute` (alt tablo, `istable: 1`)

Ürün varyantlarını (SKU) oluşturmak için hangi özniteliklerin kullanıldığını belirtir. Örneğin, bir Tişört ailesi varyant tanımlayıcı öznitelikler olarak "Beden" ve "Renk" kullanabilir.

| Alan | Tip | Amaç |
|------|-----|------|
| `attribute` | Link → PIM Attribute (zorunlu) | Varyant tanımlayıcı öznitelik |
| `sort_order` | Int (varsayılan: 0) | Varyant eksenlerinin sırası |

#### İzinler

| Rol | Okuma | Yazma | Oluşturma | Silme | Dışa Aktarım | İçe Aktarım |
|-----|-------|-------|-----------|-------|---------------|-------------|
| System Manager | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PIM Manager | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PIM User | ✓ | — | — | — | — | — |

#### Müşteri Arketip Örnekleri — Ürün Aileleri

**Moda Perakendecisi:**
```
Ürün Aileleri (Hiyerarşik):
  ├── Giyim
  │   ├── Üst Giyim         → ön ek: TOP-, varyantlar: [Beden, Renk]
  │   │   ├── Tişörtler      → ön ek: TSH-, Üst Giyim özniteliklerini miras alır
  │   │   ├── Gömlekler      → ön ek: SHR-, miras alır + Yaka Tipi ekler
  │   │   └── Kazaklar       → ön ek: SWT-, miras alır + Örgü Tipi ekler
  │   ├── Alt Giyim          → ön ek: BTM-, varyantlar: [Beden, Renk]
  │   │   ├── Kotlar         → ön ek: JNS-, miras alır + Kalıp, Yıkama ekler
  │   │   └── Etekler        → ön ek: SKR-, miras alır + Uzunluk ekler
  │   └── Dış Giyim          → ön ek: OUT-, varyantlar: [Beden, Renk]
  ├── Ayakkabı
  │   ├── Spor Ayakkabı      → ön ek: SNK-, varyantlar: [Beden, Renk, Genişlik]
  │   └── Botlar             → ön ek: BTS-, varyantlar: [Beden, Renk]
  └── Aksesuarlar
      ├── Çantalar           → ön ek: BAG-, varyantlar: [Renk]
      └── Takılar            → ön ek: JWL-, varyantlar: [Malzeme, Beden]

Temel ayarlar:
  - inherit_parent_attributes: ✓ (12+ alt ailede kurulum süresinden tasarruf sağlar)
  - min_images: 4 (moda birden fazla açı gerektirir)
  - completeness_threshold: %90 (marka odaklı perakendeciler için yüksek çıta)
  - required_media_types: "Ana Görsel, Ön, Arka, Detay, Yaşam Tarzı"
```

**Endüstriyel Tedarikçi:**
```
Ürün Aileleri (Düz veya 2 seviyeli):
  ├── Bağlantı Elemanları    → ön ek: FST-, varyantlar: [Beden, Derece]
  ├── Rulmanlar              → ön ek: BRG-, varyantlar: [Beden, Tip]
  ├── Hidrolik Bileşenler    → ön ek: HYD-, varyant yok
  ├── Elektrik Bileşenleri   → ön ek: ELC-, varyantlar: [Değerlendirme, Konnektör]
  └── Güvenlik Ekipmanları   → ön ek: SAF-, varyantlar: [Beden]

Temel ayarlar:
  - inherit_parent_attributes: ✗ (düz yapı, her aile ayrıdır)
  - min_images: 1 (teknik ürünler daha az vitrin fotoğrafı gerektirir)
  - completeness_threshold: %95 (güvenlik açısından kritik veriler eksiksiz olmalıdır)
  - required_media_types: "Ana Görsel, Teknik Çizim"
  - erp_item_group mevcut ERP yapısına eşlenmiş
```

**Gıda Üreticisi:**
```
Ürün Aileleri (Düzenlenmiş hiyerarşi):
  ├── Süt Ürünleri
  │   ├── Süt              → ön ek: MLK-, varyantlar: [Yağ%, Paket Boyutu]
  │   ├── Peynir           → ön ek: CHS-, varyantlar: [Tip, Ağırlık]
  │   └── Yoğurt           → ön ek: YGT-, varyantlar: [Lezzet, Paket Boyutu]
  ├── Unlu Mamuller
  │   ├── Ekmek            → ön ek: BRD-, varyantlar: [Tip, Boyut]
  │   └── Hamur İşleri     → ön ek: PST-, varyantlar: [Lezzet, Paket Boyutu]
  └── İçecekler
      ├── Meyve Suları     → ön ek: JCE-, varyantlar: [Lezzet, Hacim]
      └── Su               → ön ek: WTR-, varyantlar: [Hacim, Tip]

Temel ayarlar:
  - inherit_parent_attributes: ✓ (beslenme bilgileri kategoriler arasında paylaşılır)
  - min_images: 2 (ön etiket + beslenme paneli)
  - completeness_threshold: %98 (mevzuat uyumu neredeyse eksiksiz veri gerektirir)
  - required_media_types: "Ana Görsel, Beslenme Etiketi, İçindekiler Listesi"
  - Özel öznitelikler: alerjenler, beslenme_bilgileri, raf_ömrü_gün, depolama_sıcaklığı
```

### 1.4 Tip Sisteminin Ürün Verileriyle Bağlantısı

Product Master DocType'ı, gerçek ürün verilerini saklayan **içerik varlığıdır**. Tip sistemiyle ilişkisi:

**DocType:** `Product Master`
**Temel Tip Sistemi Alanları:**

| Alan | Tip | Amaç |
|------|-----|------|
| `product_name` | Data (zorunlu, çevrilebilir) | Ürün görünen adı |
| `product_code` | Data (zorunlu, benzersiz) | Otomatik oluşturulan veya manuel ürün kodu |
| `product_family` | Link → Product Family (zorunlu) | **Öznitelik yapısını belirler** |
| `status` | Select | Yaşam döngüsü durumu: `Draft`, `In Review`, `Approved`, `Published`, `End of Life`, `Archived` |
| `brand` | Link → Brand | Ürün marka referansı |
| `manufacturer` | Link → Manufacturer | Ürün üretici referansı |
| `attribute_values` | Table → Product Attribute Value | **EAV öznitelik değerleri** (dinamik) |
| `media` | Table → Product Media | Ürün görselleri ve medya dosyaları |
| `channels` | Table MultiSelect → Product Channel | Kanal atamaları |
| `erp_item` | Link → Item | Bağlı ERPNext Ürünü |
| `auto_sync_to_erp` | Check (varsayılan: 1) | ERPNext'e otomatik senkronizasyonu etkinleştir |

**Product Attribute Value** (alt tablo, `istable: 1`) EAV deseni kullanarak gerçek öznitelik verilerini saklar:

| Alan | Tip | Amaç |
|------|-----|------|
| `attribute` | Link → PIM Attribute | Bu değerin hangi öznitelik için olduğu |
| `locale` | Link → Language (varsayılan: `tr`) | Bu değer için dil/yerel ayar |
| `value_text` | Small Text | Metin değeri depolama |
| `value_long_text` | Text | Uzun metin değeri depolama |
| `value_int` | Int | Tam sayı değeri depolama |
| `value_float` | Float (hassasiyet: 6) | Ondalık değer depolama |
| `value_boolean` | Check | Mantıksal değer depolama |
| `value_date` | Date | Tarih değeri depolama |
| `value_datetime` | Datetime | Tarih-saat değeri depolama |
| `value_link` | Dynamic Link | Bağlantı değeri depolama (`attribute.linked_doctype`'a referans verir) |
| `is_inherited` | Check (salt okunur) | Değerin üst üründen miras alınıp alınmadığı |
| `inherited_from` | Data (salt okunur, gizli) | Miras alınan değerin kaynağı |

### 1.5 Product Variant Yapılandırması

**DocType:** `Product Variant`
**Amaç:** Product Master'dan miras alan ve varyant tanımlayıcı özniteliklerle farklılaşan SKU düzeyinde kayıtlar.

**Temel Varyant Yapılandırılabilir Alanları:**

| Alan | Tip | Amaç | Müşteri Bazlı Etki |
|------|-----|------|---------------------|
| `variant_name` | Data (çevrilebilir) | SKU görünen adı | Adlandırma kuralları sektöre göre değişir |
| `variant_code` | Data (benzersiz, no_copy) | SKU kodu | Aile ön eki + varyant seçeneklerinden otomatik oluşturulur |
| `product_master` | Link → Product Master | Üst ürün | Kalıtım zincirini kurar |
| `product_family` | Link → Product Family (fetch_from master) | Aile (miras alınan) | Salt okunur, ana kayıttan kademelenir |
| `status` | Select | `Draft`, `Active`, `Inactive`, `Archived` | Varyant düzeyinde yaşam döngüsü |
| `option_1_attribute` ile `option_4_attribute` | Link → PIM Attribute | En fazla 4 varyant tanımlayıcı öznitelik | Eksen sayısı ürün tipine göre değişir |
| `option_1_value` ile `option_4_value` | Data | Her varyant seçeneği için değerler | Gerçek farklılaştırıcı değerler |
| `barcode` | Data | EAN/UPC barkod | Perakende için zorunlu, B2B için isteğe bağlı |
| `price` / `cost_price` | Currency | Varyant düzeyinde fiyatlandırma | Varyant bazlı fiyatlandırma modeli |
| `weight` | Float (hassasiyet: 3) | Kg cinsinden ağırlık | Lojistik gereksinimleri |
| `length` / `width` / `height` | Float (hassasiyet: 2) | Cm cinsinden boyutlar | Kargo hesaplamaları |
| `attribute_values` | Table → Product Attribute Value | Varyanta özel EAV öznitelikleri | Ana kayıt özniteliklerini geçersiz kılar veya tamamlar |
| `sync_to_erp` | Check (varsayılan: 1) | Varyant başına ERP senkronizasyon kontrolü | Seçici senkronizasyon |

### 1.6 Tip Sistemi için Kurulum Bağlamı

| Yön | Detaylar |
|-----|----------|
| **Ne Zaman Yapılandırılır** | Faz 1 — bu **ilk** özelleştirme alanıdır. Herhangi bir ürün veri girişinden önce tamamlanmalıdır. |
| **Kim Yapılandırır** | Çözüm Mimarı modeli tanımlar; PIM Manager sistemde uygular. |
| **Bağımlılıklar** | PIM Ayarları önce yapılandırılmalıdır (ERP senkronizasyon yönü için). PIM Öznitelikleri ve PIM Öznitelik Grupları, Product Family'lerin onlara referans verebilmesi için mevcut olmalıdır. |
| **Tipik Süre** | Katalog karmaşıklığına bağlı olarak başlangıç aile yapısı için 2–5 gün. |
| **İş Etkisi** | **Kritik** — tip sistemi tüm ürün veri modelinin temelidir. Ürünler oluşturulduktan sonra değiştirmek veri göçü gerektirir. |
| **Geri Dönüşülebilirlik** | Düşük — ürün oluşturulduktan sonra aileleri veya varyant eksenlerini değiştirmek kesintiye neden olur. Dikkatli planlayın. |

#### Yapılandırma Bağımlılıkları

```
PIM Ayarları (Genel)
    └── PIM Öznitelik Grupları (Genel, Boyutlar, SEO, Teknik)
        └── PIM Öznitelikleri (renk, beden, malzeme, ...)
            └── Ürün Aileleri (Giyim, Elektronik, ...)
                ├── Aile Öznitelik Şablonları (aile başına hangi öznitelikler)
                ├── Aile Varyant Öznitelikleri (hangi öznitelikler SKU tanımlar)
                └── Ürün Tipleri (isteğe bağlı üst düzey sınıflandırma)
                    └── Product Master (gerçek ürün kayıtları)
                        └── Product Variant (SKU düzeyinde kayıtlar)
```

---

## 2. Öznitelik Sistemi (EAV Deseni)

### Genel Bakış

PIM öznitelik sistemi, her müşterinin şema değişiklikleri olmadan sınırsız sayıda ürün özniteliği tanımlamasına olanak tanıyan bir **Varlık-Öznitelik-Değer (EAV) deseni** uygular. Olası her ürün özelliği için veritabanı sütunları eklemek yerine, EAV deseni öznitelik tanımlarını merkezi olarak saklar (`PIM Attribute`) ve değerleri tipli depolama sütunlarına sahip genel bir alt tabloda (`Product Attribute Value`) kalıcı kılar.

**Neden EAV?** Geleneksel ilişkisel şemalar tablo başına sabit bir sütun seti gerektirir. Bir moda perakendecisi "kol_uzunluğu" ve "kumaş_tipi" ihtiyaç duyarken, bir endüstriyel tedarikçi "tork_değeri" ve "ip_koruma_sınıfı" ihtiyaç duyar. EAV deseni, her dağıtımın kendi öznitelik sözlüğünü yapılandırma zamanında tanımlamasına olanak tanır ve PIM'i kod değişikliği olmadan sonsuz genişletilebilir kılar.

**Mimari:**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ÖZNİTELİK TANIMLAMA KATMANI                         │
│                                                                            │
│  ┌─────────────────┐     ┌─────────────────────┐                          │
│  │ PIM Attribute    │────▶│ PIM Attribute Group  │  (organizasyonel grup)   │
│  │ Group            │     │ Genel, Boyutlar,     │                          │
│  │ (fa-cog, #3498db)│     │ SEO, Teknik          │                          │
│  └─────────────────┘     └─────────────────────┘                          │
│           │                                                                │
│           ▼                                                                │
│  ┌─────────────────┐                                                      │
│  │ PIM Attribute    │  attribute_code: "color"                             │
│  │ data_type: Select│  options: "Kırmızı, Mavi, Yeşil"                    │
│  │ is_required: ✓   │  is_localizable: ✗                                  │
│  │ is_filterable: ✓ │  weight_in_completeness: 3                          │
│  └─────────────────┘                                                      │
└─────────────────────────────────────────────────────────────────────────────┘
           │
           │  Family Attribute Template (alt tablo) aracılığıyla bağlanır
           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AİLE BAĞLAMA KATMANI                                │
│                                                                            │
│  ┌────────────────────────┐                                               │
│  │ Product Family          │                                               │
│  │ └── attributes (Tablo)  │─── Family Attribute Template ───┐             │
│  │     ├── renk (zorunlu)  │     attribute: PIM Attribute     │             │
│  │     ├── beden (zorunlu) │     is_required_in_family: ✓/✗   │             │
│  │     ├── malzeme         │     default_value: "Pamuk"        │             │
│  │     └── bakım_tal       │     sort_order: 10, 20, 30...   │             │
│  │                         │                                  │             │
│  │ └── variant_attributes  │─── Family Variant Attribute ────┘             │
│  │     ├── renk            │     (hangi öznitelikler SKU tanımlar)         │
│  │     └── beden           │                                               │
│  └────────────────────────┘                                               │
└─────────────────────────────────────────────────────────────────────────────┘
           │
           │  Product Master, Product Family'ye bağlanır
           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DEĞER DEPOLAMA KATMANI                              │
│                                                                            │
│  ┌─────────────────────────────────┐                                      │
│  │ Product Attribute Value          │  (Product Master'ın alt tablosu)     │
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
**Modül:** PIM
**Adlandırma Kuralı:** `field:attribute_code` (`attribute_code` alanına göre adlandırılır)
**Amaç:** Tek bir ürün özniteliğini tanımlar — adı, veri tipi, doğrulama kısıtlamaları, görüntüleme davranışı ve tamlık ağırlığı. Bu, tüm ürün veri modelinin temel yapı taşıdır.

#### Yapılandırılabilir Alanlar

| Alan | Tip | Varsayılan | Amaç | Müşteri Bazlı Etki |
|------|-----|-----------|------|---------------------|
| `attribute_name` | Data (zorunlu, çevrilebilir) | — | Ürün formlarında gösterilen görünen ad | Müşteri diline göre yerelleştirilir |
| `attribute_code` | Data (zorunlu, benzersiz) | Addan otomatik oluşturulur | URL güvenli kısa tanımlayıcı | API'lerde, dışa aktarımlarda, içe aktarım eşlemelerinde referans alınır |
| `attribute_group` | Link → PIM Attribute Group | — | Organizasyonel grup | Öznitelikleri ürün formunda görsel olarak gruplar |
| `data_type` | Select (zorunlu) | `Text` | Veri tipi — 12 tipten biri | Depolama sütununu, doğrulamayı ve arayüz bileşenini belirler |
| `options` | Small Text | — | Select/Multi Select için virgülle ayrılmış değerler | İzin verilen değerleri kısıtlar; yalnızca `data_type` ∈ {Select, Multi Select} olduğunda görünür |
| `linked_doctype` | Link → DocType | — | Link veri tipi için hedef DocType | `data_type` = Link olduğunda gerekli; ERPNext kayıtlarına referans vermeyi sağlar |
| `is_required` | Check | `0` | Değerin genel olarak zorunlu olup olmadığı | Bu özniteliği kullanan tüm aileler genelinde genel gereklilik |
| `is_unique` | Check | `0` | Değerin ürün başına benzersiz olması gerekip gerekmediği | Tekrarlanan öznitelik değerlerini engeller (ör. benzersiz SKU tanımlayıcı) |
| `min_value` | Float | — | Minimum sayısal değer | Integer/Float için görünür; taban kısıtlamasını uygular |
| `max_value` | Float | — | Maksimum sayısal değer | Integer/Float için görünür; tavan kısıtlamasını uygular |
| `max_length` | Int | — | Maksimum karakter uzunluğu | Text/Long Text için görünür; aşırı uzun girişleri engeller |
| `is_filterable` | Check | `0` | Filtre/yüzey panelinde göster | Ürün listesi kullanıcı deneyimini ve kanal dışa aktarımını etkiler |
| `is_searchable` | Check | `0` | Tam metin aramaya dahil et | Performans etkisi — yalnızca gerçekten aranabilir alanlar için etkinleştirin |
| `show_in_grid` | Check | `1` | Liste/ızgara görünümlerinde göster | Ürün listesi sütun görünürlüğünü kontrol eder |
| `sort_order` | Int | `0` | Grup içindeki görüntüleme sırası | Düşük sayı = önce görünür |
| `weight_in_completeness` | Int | `1` | Tamlık puanı ağırlığı | `0` = puandan hariç; yüksek = ürün hazırlığı üzerinde daha fazla etki |
| `is_localizable` | Check | `0` | Yerel ayar bazlı değerleri destekle | Etkinleştirildiğinde, ürün dil başına farklı değerler saklayabilir |
| `is_standard` | Check (salt okunur) | `0` | Sistem özniteliği bayrağı | Standart öznitelikler silinemez; kurulum hook'ları tarafından ayarlanır |
| `description` | Small Text | — | Dahili dokümantasyon | İçerik ekiplerinin özniteliğin amacını anlamasına yardımcı olur |

#### Öznitelik Kodu Doğrulama

Öznitelik kodları, PIM genelinde tutarlılığı sağlamak için belirli kalıpları izlemelidir:

- Küçük harfle başlamalıdır
- Küçük harfler, rakamlar ve alt çizgiler içerebilir
- Desen: `^[a-z][a-z0-9_]*$`
- Sağlanmazsa, `attribute_name` üzerinden `frappe.scrub()` ile otomatik oluşturulur

**Örnekler:** `color`, `weight_kg`, `is_organic`, `care_instructions`, `ip_rating`, `shelf_life_days`

#### Doğrulama API'si

**Uç Nokta:** `frappe_pim.pim.api.attribute.validate_attribute_value`
**Parametreler:** `attribute` (PIM Attribute adı), `value` (doğrulanacak dize)

**Gerçekleştirilen doğrulama kontrolleri:**
1. **Zorunluluk kontrolü** — `is_required` ise ve değer boşsa → hata
2. **Select doğrulama** — değer tanımlı seçenekler listesinde olmalıdır
3. **Multi Select doğrulama** — her virgülle ayrılmış değer seçenekler listesinde olmalıdır
4. **Integer doğrulama** — tam sayı olarak ayrıştırılabilmeli; `min_value`/`max_value` aralığında olmalıdır
5. **Float doğrulama** — ondalık sayı olarak ayrıştırılabilmeli; `min_value`/`max_value` aralığında olmalıdır
6. **Metin uzunluğu doğrulama** — dize uzunluğu `max_length` değerini aşmamalıdır

**Dönüş:** `{"valid": true/false, "errors": [...]}`

#### İzinler

| Rol | Okuma | Yazma | Oluşturma | Silme | Dışa Aktarım | İçe Aktarım |
|-----|-------|-------|-----------|-------|---------------|-------------|
| System Manager | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PIM Manager | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| PIM User | ✓ | — | — | — | — | — |

### 2.2 PIM Attribute Group

**DocType:** `PIM Attribute Group`
**Modül:** PIM
**Adlandırma Kuralı:** `field:group_code` (`group_code` alanına göre adlandırılır)
**Sıralama:** `sort_order ASC` sırasına göre (düşük sayı = arayüzde ilk)
**Amaç:** PIM Özniteliklerini ürün formundaki mantıksal görsel bölümlere organize eder. Her öznitelik en fazla bir gruba ait olabilir. Gruplandırılmamış öznitelikler, en altta varsayılan "Gruplandırılmamış" bölümünde gösterilir.

#### Varsayılan Gruplar (Kurulumda Oluşturulur)

Kurulum hook'u (`setup/install.py`) dört standart öznitelik grubu oluşturur:

| Grup Adı | Grup Kodu | Amaç | Örnek Öznitelikler |
|----------|-----------|------|-------------------|
| **Genel** | `general` | Temel ürün bilgileri | product_name, brand, description, category |
| **Boyutlar** | `dimensions` | Fiziksel ölçümler | weight, height, width, length, volume |
| **SEO** | `seo` | Arama motoru optimizasyonu | meta_title, meta_description, url_slug, keywords |
| **Teknik** | `technical` | Teknik özellikler | voltage, wattage, ip_rating, torque, pressure |

Bu standart gruplar `is_standard: 1` değerine sahiptir ve **silinemez**. Ancak görüntüleme özellikleri (ikon, renk, sort_order, daraltılabilirlik) tamamen özelleştirilebilir.

#### Yapılandırılabilir Alanlar

| Alan | Tip | Varsayılan | Amaç | Müşteri Bazlı Etki |
|------|-----|-----------|------|---------------------|
| `group_name` | Data (zorunlu, çevrilebilir) | — | Görünen ad | Müşteri diline göre yerelleştirilir |
| `group_code` | Data (zorunlu, benzersiz) | Otomatik oluşturulur | URL güvenli kısa ad | API çağrılarında ve içe aktarım şablonlarında referans alınır |
| `sort_order` | Int | `0` (kaydetme sırasında denetleyici tarafından otomatik olarak 10'un sonraki katına ayarlanır) | Görüntüleme sırası | Ürün formundaki bölüm sırasını kontrol eder |
| `is_standard` | Check (salt okunur) | `0` | Sistem grubu bayrağı | Standart gruplar silinemez |
| `icon` | Data | — | FontAwesome ikon sınıfı | Grup başlıklarında görsel gösterge (ör. `fa-cog`, `fa-ruler`, `fa-search`) |
| `color` | Color | — | Hex renk kodu | Grup bölümleri için görsel markalama |
| `is_collapsible` | Check | `0` | Grup bölümü daraltılabilir | Yoğun formlar için görsel karmaşıklığı azaltır |
| `is_collapsed_default` | Check | `0` | Ürün görüntülenirken daraltılmış başla | Yalnızca `is_collapsible` etkinleştirildiğinde aktif |
| `description` | Small Text | — | Grup açıklaması | Uygulama ekipleri için dahili dokümantasyon |

#### Grup Kodu Doğrulama

PIM Attribute ile aynı desen: `^[a-z][a-z0-9_]*$`, sağlanmazsa `group_name` üzerinden otomatik oluşturulur.

#### Sıralama Otomatik Ataması

Yeni bir grup açık bir `sort_order` olmadan oluşturulduğunda, denetleyici mevcut maksimum sort_order'ı 10 artırarak bir sonraki uygun yeri otomatik atar. Bu, mevcut olanlar arasına grup eklemeye olanak tanıyan doğal bir aralık (10, 20, 30, ...) oluşturur.

#### API Uç Noktaları

| Uç Nokta | Amaç | Dönüş |
|----------|------|-------|
| `get_attribute_groups()` | sort_order sırasına göre tüm grupları listele | `[{name, group_name, group_code, icon, color, sort_order}]` |
| `get_attributes_by_group(group)` | Belirli bir gruptaki öznitelikleri listele | `[{name, attribute_name, attribute_code, data_type, is_required, sort_order}]` |
| `get_grouped_attributes()` | Gruba göre organize edilmiş tüm öznitelikler | `[{group: {...}, attributes: [...]}]` — "Gruplandırılmamış" sözde grubunu içerir |
| `reorder_groups(order)` | Grup adlarının JSON listesini sağlayarak grupları yeniden sırala | `{"success": true}` |

#### Müşteri Arketip Örnekleri — Öznitelik Grupları

**Moda Perakendecisi:**
```
Öznitelik Grupları:
  ├── Genel         (sıra: 10, ikon: fa-tshirt, renk: #3498db)
  │   └── marka, koleksiyon, sezon, cinsiyet, stil, durum
  ├── Beden         (sıra: 20, ikon: fa-ruler, renk: #e74c3c)  ← özel grup
  │   └── beden, kalıp, beden_tablosu_url, model_boyu, model_bedeni
  ├── Malzemeler    (sıra: 30, ikon: fa-layer-group, renk: #2ecc71)  ← özel grup
  │   └── kumaş_tipi, kumaş_bileşimi, bakım_talimatları, menşe_ülke
  ├── SEO           (sıra: 40, ikon: fa-search, renk: #9b59b6, daraltılabilir: ✓)
  │   └── meta_title, meta_description, url_slug
  └── Uyumluluk     (sıra: 50, ikon: fa-certificate, renk: #f39c12)  ← özel grup
      └── reach_uyumlu, oeko_tex, grs_sertifikalı
```

**Endüstriyel Tedarikçi:**
```
Öznitelik Grupları:
  ├── Genel         (sıra: 10, ikon: fa-cog)
  │   └── parça_numarası, üretici, seri, kategori
  ├── Teknik        (sıra: 20, ikon: fa-microchip, renk: #e67e22)
  │   └── voltaj, akım, güç_değerlendirmesi, çalışma_sıcaklığı, ip_sınıfı
  ├── Boyutlar      (sıra: 30, ikon: fa-ruler-combined, renk: #3498db)
  │   └── ağırlık, yükseklik, genişlik, derinlik, diş_boyutu
  ├── Sertifikalar  (sıra: 40, ikon: fa-shield-alt, renk: #27ae60)  ← özel grup
  │   └── ul_listeli, ce_işaretli, rohs_uyumlu, atex_sınıflı
  └── Lojistik      (sıra: 50, ikon: fa-truck, daraltılabilir: ✓, daraltılmış: ✓)  ← özel grup
      └── teslim_süresi_gün, minimum_sipariş, ambalaj_tipi, menşe_ülke
```

**Gıda Üreticisi:**
```
Öznitelik Grupları:
  ├── Genel         (sıra: 10, ikon: fa-apple-alt, renk: #27ae60)
  │   └── marka, ürün_hattı, lezzet, varyant
  ├── Beslenme      (sıra: 20, ikon: fa-heartbeat, renk: #e74c3c)  ← özel grup
  │   └── kalori, protein_g, yağ_g, karbonhidrat_g, lif_g, sodyum_mg
  ├── Alerjenler    (sıra: 30, ikon: fa-exclamation-triangle, renk: #f39c12)  ← özel grup
  │   └── gluten_içerir, süt_içerir, fındık_içerir, soya_içerir
  ├── Mevzuat       (sıra: 40, ikon: fa-gavel, renk: #8e44ad)  ← özel grup
  │   └── organik_sertifikalı, helal, koşer, gdo_içermez, raf_ömrü_gün
  ├── Depolama      (sıra: 50, ikon: fa-thermometer-half, renk: #2980b9)  ← özel grup
  │   └── depolama_sıcaklık_min, depolama_sıcaklık_max, soğutma_gerekli
  └── SEO           (sıra: 60, ikon: fa-search, daraltılabilir: ✓, daraltılmış: ✓)
      └── meta_title, meta_description, url_slug
```

---

## 3. Genel Ayarlar (PIM Ayarları)

### Genel Bakış

**DocType:** `PIM Settings`
**Modül:** PIM
**Tip:** Single (tekil — site başına yalnızca bir örnek mevcuttur, `issingle: 1`)
**Değişiklikleri İzle:** Evet (`track_changes: 1`)

> **Uygulama Durumu:** `PIM Settings` DocType JSON tanımı (`pim_settings.json`) henüz kod tabanında taahhüt edilmiş bir dosya olarak mevcut değildir. Aşağıda açıklanan alanlar, API'ler ve davranışlar, DocType'ın kod tabanı genelinde referans verilme şekline dayanan **planlanan mimariyi** temsil eder. Şu anda, `erp_sync.py` `enable_erp_sync`, `auto_create_variant_from_item` ve `auto_create_item_from_variant` değerlerini DocType'ın yokluğunu zarif bir şekilde ele alan `frappe.db.get_single_value()` çağrıları aracılığıyla defansif olarak okur (senkronizasyon etkin için varsayılan `True`). PIM Settings DocType'ını Frappe'nin DocType oluşturucusu aracılığıyla oluşturmak, bu bölümde açıklanan işlevselliğin çoğunu etkinleştirmek için bir ön koşuldur.

PIM Ayarları, tüm PIM sistemi için **genel yapılandırma merkezidir**. Neredeyse her diğer modül çalışma zamanında değerlerini okuduğundan, kurulum sırasında yapılandırılması gereken ilk DocType'tır. Ayarlar, ERP entegrasyonu, kanal varsayılanları, yapay zeka zenginleştirme, veri kalitesi, GS1/GDSN standartları ve medya yönetimini kapsayan **7 fonksiyonel grup** halinde organize edilmiştir.

**Ne Zaman Yapılandırılır:** Faz 0 — herhangi bir PIM kurulumunun en ilk adımı
**Kim Yapılandırır:** System Manager (başlangıç kurulumu), PIM Manager (devam eden ayarlama)
**İş Etkisi:** Tüm PIM için operasyonel çerçeveyi belirler — hangi özelliklerin aktif olduğu, ürünlerin ERP'ye nasıl aktığı ve hangi kalite kapılarının uygulandığı

#### Erişim İzinleri

| Rol | Okuma | Yazma | Oluşturma |
|-----|-------|-------|-----------|
| System Manager | ✓ | ✓ | ✓ |
| PIM Manager | ✓ | ✓ | — |
| PIM User | ✓ (salt okunur) | — | — |

> **Not:** PIM Kullanıcıları mevcut ayarları görüntüleyebilir (belirli özelliklerin neden etkin/devre dışı olduğunu anlamak için faydalıdır) ancak değiştiremez. Yalnızca System Manager ve PIM Manager rolleri PIM Ayarlarını değiştirebilir.

### 3.1 ERP Entegrasyon Ayarları

PIM ve ERPNext Item DocType'ı arasındaki çift yönlü senkronizasyonu kontrol eder. Bu en sonuç odaklı ayar grubudur — PIM'in kayıt sistemi olarak mı, ERP verilerinin aşağı akış tüketicisi olarak mı yoksa çift yönlü eş olarak mı çalışacağını belirler.

| Alan | Tip | Varsayılan | Seçenekler | Açıklama | Müşteri Bazlı Etki |
|------|-----|-----------|-----------|----------|---------------------|
| `enable_erp_sync` | Check | `1` (etkin) | — | ERP senkronizasyonu için ana anahtar | Devre dışı bırakmak PIM'i ERPNext'ten tamamen ayırır; bağımsız PIM dağıtımları için kullanın |
| `sync_direction` | Select | `Bidirectional` | `PIM to ERP`, `ERP to PIM`, `Bidirectional` | Sistemler arası veri akış yönü | Ürün verileri için hangi sistemin doğruluk kaynağı olduğunu belirler |
| `sync_on_save` | Check | `1` (etkin) | — | Ürün kaydedildiğinde otomatik senkronize et | Devre dışı bırakıldığında, senkronizasyon manuel olarak veya zamanlanmış görev aracılığıyla tetiklenmelidir |
| `auto_create_variant_from_item` | Check | `0` (devre dışı) | — | ERPNext Item varyantları oluşturulduğunda otomatik olarak PIM Product Variant oluştur | Varyantların ERPNext'te oluştuğu ERP öncelikli iş akışları için etkinleştirin |
| `auto_create_item_from_variant` | Check | `0` (devre dışı) | — | PIM Product Variant'ları ERP'ye senkronize edildiğinde otomatik olarak ERPNext Item oluştur | Ürünlerin PIM'de oluştuğu PIM öncelikli iş akışları için etkinleştirin |

**Görünürlük Bağımlılıkları:**
- `sync_direction` ve `sync_on_save` yalnızca `enable_erp_sync` etkinleştirildiğinde görünür
- `auto_create_variant_from_item` her zaman görünür (bağımsız anahtar)

#### Senkronizasyon Yönü Karar Kılavuzu

| Yön | Doğruluk Kaynağı | Kullanım Durumu | Ödünleşimler |
|-----|-----------------|-----------------|-------------|
| **PIM → ERP** | PIM ana kaynak | Pazarlama ekibinin ürünleri ERP görmeden önce zenginleştirdiği içerik öncelikli iş akışları | Paylaşılan alanlardaki ERP değişiklikleri bir sonraki senkronizasyonda üzerine yazılır |
| **ERP → PIM** | ERP ana kaynak | Satın almanın ERP'de ürün oluşturup PIM'in zenginleştirdiği operasyon öncelikli iş akışları | PIM zenginleştirmesi ERP kaynaklı alanları değiştiremez |
| **Çift Yönlü** | Her iki sistem katkıda bulunur | İşbirlikçi iş akışları — ERP lojistik alanlarına, PIM pazarlama alanlarına sahip | Net alan sahipliği kuralları gerektirir; senkronizasyon çatışma riski |

#### Müşteri Arketip Önerileri — ERP Entegrasyonu

```
Moda Perakendecisi (içerik öncelikli):
  enable_erp_sync: ✓
  sync_direction: "PIM to ERP"
  sync_on_save: ✓
  auto_create_variant_from_item: ✗
  Gerekçe: Pazarlama/içerik ekibi PIM'de ürünleri oluşturur ve zenginleştirir.
  ERP, envanter ve yerine getirme için tamamlanmış ürün verilerini alır.

Endüstriyel Tedarikçi (operasyon öncelikli):
  enable_erp_sync: ✓
  sync_direction: "Bidirectional"
  sync_on_save: ✗ (manuel senkronizasyon — mühendislik incelemesi gerekli)
  auto_create_variant_from_item: ✓
  Gerekçe: Satın alma ERP'de Ürünler oluşturur, mühendislik PIM'de teknik özellikler ekler.
  Her iki sistem de veri katkısında bulunur. Erken yayınlamayı önlemek için manuel senkronizasyon.

Gıda Üreticisi (uyumluluk odaklı):
  enable_erp_sync: ✓
  sync_direction: "PIM to ERP"
  sync_on_save: ✓
  auto_create_variant_from_item: ✗
  Gerekçe: Mevzuat verileri ERP'ye akmadan önce PIM'de doğrulanmalıdır.
  PIM, uyumluluk kontrollü doğruluk kaynağıdır.

Bağımsız PIM (ERPNext olmadan):
  enable_erp_sync: ✗
  sync_direction: (ilgisiz)
  sync_on_save: (ilgisiz)
  auto_create_variant_from_item: ✗
  Gerekçe: PIM bağımsız çalışır, verileri kanallar/dışa aktarımlar aracılığıyla dışa aktarır.
```

### 3.2 Kanal Ayarları

Ürün dağıtım kanalları ve dışa aktarım işlemleri için varsayılan davranışı kontrol eder.

| Alan | Tip | Varsayılan | Seçenekler | Açıklama | Müşteri Bazlı Etki |
|------|-----|-----------|-----------|----------|---------------------|
| `default_channel` | Link → Channel | — (yok) | Yapılandırılmış herhangi bir `Channel` kaydı | Yeni ürünler için varsayılan dağıtım kanalı | Yeni ürünlere varsayılan olarak hangi kanal gereksinimlerinin uygulanacağını belirler |
| `auto_publish_to_default` | Check | `0` (devre dışı) | — | Hazır olarak işaretlendiğinde ürünleri otomatik olarak varsayılan kanala yayınla | Etkinleştirildiğinde, "Onaylandı" durumuna ulaşan ürünler otomatik yayınlanır; dikkatli kullanın |
| `default_export_format` | Select | `JSON` | `JSON`, `XML`, `CSV`, `XLSX`, `BMEcat` | Ürün veri dışa aktarımları için varsayılan format | Tek tıkla dışa aktarım davranışını yönlendirir; farklı kanallar bunu geçersiz kılabilir |

#### Dışa Aktarım Format Kılavuzu

| Format | En İyi Kullanım | Tipik Kanallar |
|--------|-----------------|----------------|
| **JSON** | API entegrasyonları, geliştirici araçları | Özel entegrasyonlar, headless ticaret |
| **XML** | Yapılandırılmış B2B veri alışverişi | BMEcat, cXML, EDIFACT, GS1 XML |
| **CSV** | Toplu içe/dışa aktarımlar, elektronik tablo araçları | Google Merchant, temel pazar yeri yüklemeleri |
| **XLSX** | İnsan tarafından okunabilir dışa aktarımlar, müşteri incelemesi | Dahili inceleme, müşteri onay iş akışları |
| **BMEcat** | Avrupa B2B ürün katalogları | Tedarik platformları, B2B pazar yerleri |

### 3.3 Yapay Zeka Zenginleştirme Ayarları

Ürün açıklamaları, öznitelik çıkarma, kategorizasyon ve çeviri dahil olmak üzere yapay zeka destekli içerik oluşturmayı kontrol eder. Bu, harici API kimlik bilgileri gerektiren premium bir özelliktir.

| Alan | Tip | Varsayılan | Seçenekler | Açıklama | Müşteri Bazlı Etki |
|------|-----|-----------|-----------|----------|---------------------|
| `enable_ai_enrichment` | Check | `0` (devre dışı) | — | Tüm yapay zeka özellikleri için ana anahtar | Devre dışı bırakıldığında, yapay zeka zenginleştirme görevleri, otomatik kategorizasyon ve yapay zeka çevirisi kullanılamaz |
| `ai_provider` | Select | — (yok) | `OpenAI`, `Anthropic`, `Google Gemini`, `Azure OpenAI` | Yapay zeka servis sağlayıcısı | Her sağlayıcının farklı yetenekleri, fiyatlandırması ve veri ikamet etkileri vardır |
| `ai_api_key` | Password | — (yok) | — | Seçilen sağlayıcı için API anahtarı (veritabanında şifreli saklanır) | **Güvenlik açısından hassas** — Frappe'nin şifre şifreleme kullanılarak saklanır; API yanıtlarında asla açığa çıkmaz |
| `ai_model` | Data | — (yok) | Serbest metin (ör. `gpt-4`, `claude-3-opus`, `gemini-pro`) | Kullanılacak belirli model | Kalite/maliyet/hız dengesini kontrol eder; yeni modeller tüm bölgelerde mevcut olmayabilir |
| `ai_require_approval` | Check | `1` (etkin) | — | Yapay zeka tarafından oluşturulan içeriği uygulamadan önce insan onayı gerektir | **Şiddetle tavsiye edilir** — devre dışı bırakmak yapay zekanın inceleme olmadan içeriği otomatik uygulamasına izin verir |

### 3.4 Veri Kalitesi Ayarları

Ürünleri yapılandırılabilir tamlık ve kalite eşiklerine göre değerlendiren otomatik veri kalitesi puanlama motorunu kontrol eder.

| Alan | Tip | Varsayılan | Seçenekler | Açıklama | Müşteri Bazlı Etki |
|------|-----|-----------|-----------|----------|---------------------|
| `enable_quality_scoring` | Check | `1` (etkin) | — | Kalite puanı hesaplaması için ana anahtar | Devre dışı bırakmak ürün görünümlerinden kalite puanlarını kaldırır ve yayın kapılarını kaldırır |
| `minimum_quality_score` | Percent | `60` | 0–100 | Yayınlama için gereken minimum kalite puanı | Daha yüksek eşik = daha sıkı yayın kapısı; daha düşük = daha hızlı pazara çıkış |
| `block_publish_below_minimum` | Check | `0` (devre dışı) | — | Minimum kalite puanının altındaki ürünlerin yayınlanmasını kesinlikle engelle | Etkinleştirildiğinde, ürünler eşiğin altında herhangi bir kanala yayınlanamaz |
| `auto_scan_on_save` | Check | `1` (etkin) | — | Ürün kaydedildiğinde veri kalitesi sorunlarını otomatik tara | Gerçek zamanlı kalite geri bildirimi sağlar; toplu içe aktarım performansı için devre dışı bırakın |

---

## 4. Kanal Yapılandırması

### Genel Bakış

PIM kanal sistemi, dağıtım kanallarının (Amazon, Shopify, Trendyol, WooCommerce vb.) sabit kodlanmış pazar yeri modülleri yerine `Channel` DocType'ında veri kayıtları olarak tanımlandığı **yapılandırma odaklı bir mimari** uygular. Bu, herhangi bir pazar yerinin kod değişikliği olmadan kurulum zamanında yapılandırılabileceği anlamına gelir — sistem yeni kanallara sonsuz genişletilebilir.

**Temel Mimari Kararlar:**

1. **Genel Channel DocType** — Her pazar yeri/mağaza, bağlantı ayarları, dışa aktarım tercihleri ve senkronizasyon yapılandırmasına sahip bir `Channel` kaydıdır
2. **Product Channel alt tablosu** — Ürünleri kanal bazlı yayın durumu, senkronizasyon takibi ve harici kimliklerle kanallara bağlar
3. **Export Profile bağlama** — Her kanal, formatı, filtrelemeyi, zamanlamayı ve çıktıyı kontrol eden bir veya daha fazla Dışa Aktarım Profiline sahip olabilir
4. **Tamlık kapılama** — Ürünler herhangi bir kanala yayınlanmadan önce kalite/tamlık eşiklerini (PIM Ayarları ve Product Family'de tanımlanan) karşılamalıdır

### 4.1 Channel DocType

**DocType:** `Channel`
**Modül:** PIM
**Adlandırma Kuralı:** `field:channel_code` (`channel_code` alanına göre adlandırılır)
**Sıralama:** `sort_order ASC` (düşük sayı = listelerde ilk)
**Değişiklikleri İzle:** Evet (`track_changes: 1`)
**Amaç:** Bir dağıtım kanalı tanımlar — ürün verilerinin yayınlandığı bir pazar yeri, e-ticaret platformu, sosyal ticaret platformu veya herhangi bir satış noktası.

#### Yapılandırılabilir Alanlar

**Temel Ayarlar:**

| Alan | Tip | Varsayılan | Amaç | Müşteri Bazlı Etki |
|------|-----|-----------|------|---------------------|
| `channel_name` | Data (zorunlu, çevrilebilir) | — | Görünen ad (ör. "Amazon Türkiye", "Shopify ABD Mağazası") | Her kanal örneği için müşteriye özel adlandırma |
| `channel_code` | Data (zorunlu, benzersiz) | Otomatik oluşturulur | URL güvenli kısa ad (ör. `amazon_tr`, `shopify_us`) | API çağrılarında, dışa aktarım dosya adlarında, webhook URL'lerinde kullanılır |
| `channel_type` | Select (zorunlu) | `E-Commerce` | Kanal sınıflandırması | Organizasyonel; davranışı etkilemez |
| `enabled` | Check | `1` | Kanalı etkinleştir/devre dışı bırak | Devre dışı kanallar ürün yayını ve senkronizasyondan hariç tutulur |
| `sort_order` | Int | `0` (kaydetme sırasında denetleyicideki `get_next_sort_order()` ile 10'un sonraki katına otomatik ayarlanır) | Görüntüleme sırası | Ürün formlarında ve yönetici listelerindeki kanal sırasını kontrol eder |

**Kanal Tipi Seçenekleri:**

| Tip | Açıklama | Tipik Kanallar |
|-----|----------|----------------|
| `E-Commerce` | Kendi barındırdığınız çevrimiçi mağazalar | Shopify, WooCommerce, Magento, özel web mağazaları |
| `Marketplace` | Üçüncü taraf pazar yeri platformları | Amazon, Trendyol, Hepsiburada, N11, eBay, Etsy, Walmart |
| `Social Commerce` | Sosyal medya alışverişi | Meta Commerce (Facebook/Instagram Shops), TikTok Shop |
| `Retail` | Fiziksel perakende / POS | Mağaza içi gösterimler, POS sistemleri, kiosk |
| `Wholesale` | B2B toptan satış | Toptan satış portalları, distribütör katalogları |
| `B2B Portal` | İşletmeden işletmeye | BMEcat katalogları, tedarik platformları |
| `Mobile App` | Mobil uygulamalar | Native uygulamalar, PWA'lar |
| `Other` | Özel veya niş kanallar | Basılı kataloglar, veri havuzları, dahili sistemler |

---

## 5. İş Akışı ve Yaşam Döngüsü

### Genel Bakış

PIM, ürün verilerinin oluşturulmasından yayınlanmasına ve nihayetinde arşivlenmesine kadar olan yaşam döngüsünü yönetmek için çok katmanlı bir iş akışı sistemi uygular.

**Product Master Yaşam Döngüsü Durumları (6 durum):**

| Durum | Açıklama | İzin Verilen Geçişler |
|-------|----------|----------------------|
| `Draft` | İlk oluşturma, veri girişi | → In Review |
| `In Review` | İçerik inceleme aşamasında | → Approved, → Draft (ret) |
| `Approved` | İçerik onaylandı, yayına hazır | → Published |
| `Published` | Kanallarda canlı | → End of Life |
| `End of Life` | Aşamalı kaldırma döneminde | → Archived |
| `Archived` | Artık aktif değil | — |

**Product Variant Yaşam Döngüsü Durumları (4 durum):**

| Durum | Açıklama |
|-------|----------|
| `Draft` | İlk oluşturma |
| `Active` | Satışa hazır varyant |
| `Inactive` | Geçici olarak devre dışı (mevsimsel, stok yok) |
| `Archived` | Kalıcı olarak kaldırılmış |

---

## 6. Puanlama ve Kalite

### Genel Bakış

Frappe PIM, ürün veri kalitesini birden fazla boyutta ölçen **ağırlıklı tamlık puanlama sistemi** uygular. Puanlama motoru, doldurulmuş zorunlu alanların, özniteliklerin, medyanın ve açıklamaların oranına dayalı olarak bir yüzde puanı (%0–100) hesaplar. Bu puan, iş akışı geçişlerini ve kanal yayınını kontrol eden **kalite kapılarını** yönlendirir.

### 6.1 Puanlama Boyutları

Product Master tamlık puanı, birlikte ağırlıklı bir bileşik puan oluşturan **6 puanlama boyutundan** hesaplanır.

| # | Boyut | Ağırlık Kategorisi | Kaynak | Varsayılan Ağırlık | Özelleştirilebilir mi? |
|---|-------|-------------------|--------|--------------------|-----------------------|
| 1 | **İçerik** (Açıklamalar) | Sabit | `short_description` (5 puan) + `long_description` (5 puan) | 10 puan (~%20) | DocType özelleştirmesi ile |
| 2 | **Medya** (Görseller ve Dosyalar) | Sabit | `main_image` (10 puan) + ≥3 medya öğesi (10 puan) | 20 puan (~%15) | DocType özelleştirmesi ile |
| 3 | **SEO** (Arama Optimizasyonu) | Öznitelikler Aracılığıyla | `weight_in_completeness` ile SEO grubu öznitelikleri | Öznitelik başına yapılandırılabilir | ✓ Öznitelik başına ağırlık |
| 4 | **Çeviri** (Yerelleştirme) | Öznitelikler Aracılığıyla | Yerelleştirilebilir özniteliklerin (`is_localizable: 1`) tamlığı | Öznitelik başına yapılandırılabilir | ✓ Öznitelik başına ağırlık |
| 5 | **Öznitelikler** (Ürün Verileri) | Dinamik | Aile Öznitelik Şablonu zorunlu öznitelikleri | Öznitelik başına yapılandırılabilir (varsayılan: 1) | ✓ Öznitelik başına ağırlık |
| 6 | **Pazar** (Kanal Hazırlığı) | Kanal Kuralları Aracılığıyla | Kanala özel zorunlu öznitelikler ve alanlar | Kanal başına yapılandırılabilir | ✓ Kanal başına yapılandırma |

---

## 7. ERPNext Entegrasyonu

### Genel Bakış

Frappe PIM, ERPNext ile çift yönlü senkronizasyon sağlayarak ürün verilerinin her iki sistem arasında tutarlı kalmasını sağlar. Senkronizasyon yönü, `PIM Settings.sync_direction` ayarı ile kontrol edilir.

---

## 8. Roller ve İzinler

### Genel Bakış

PIM sistemi, erişim kontrolü için Frappe'nin yerleşik rol tabanlı izin sistemi üzerine inşa edilmiş iki temel rol sağlar:

| Rol | Amaç | Tipik Kullanıcılar |
|-----|------|-------------------|
| **PIM Manager** | Tam yönetici erişimi — tüm PIM DocType'ları üzerinde oluşturma, okuma, yazma, silme, içe/dışa aktarım | Katalog yöneticileri, ürün müdürleri, teknik yazarlar |
| **PIM User** | İçerik katılımcısı erişimi — çoğu DocType'ta okuma + yazma, ancak yapılandırma varlıklarını oluşturma/silme kısıtlı | İçerik editörleri, metin yazarları, fotoğrafçılar, veri giriş personeli |

---

## 9. Taksonomi ve Navigasyon

### Genel Bakış

Frappe PIM, müşterilerin ürünleri hiyerarşik sınıflandırma yapılarına organize etmesine olanak tanıyan **çok katmanlı taksonomi sistemi** sağlar. Taksonomi katmanı, Product Family hiyerarşisinden (Bölüm 1.3) bağımsız çalışır ve birden fazla eşzamanlı sınıflandırma şemasını destekler — örneğin bir perakende taksonomisi, bir mevzuat taksonomisi ve kanala özel bir taksonomi.

**Temel Tasarım İlkeleri:**
1. **Product Family = Yapısal Hiyerarşi** — bir ürünün hangi özniteliklere sahip olduğunu belirler (veri modeli)
2. **Taksonomi = Navigasyonel Hiyerarşi** — ürünlerin tarama, arama ve kanal yayını için nasıl organize edildiğini belirler (kullanıcıya dönük)
3. **Kategori = Ürün Sınıflandırması** — bir ürünün bir taksonomi içinde yerleştirildiği gerçek düğüm
4. **Ürün Başına Birden Fazla Taksonomi** — tek bir ürün aynı anda birkaç taksonomide sınıflandırılabilir

---

## 10. Yapay Zeka ve Zenginleştirme

### Genel Bakış

PIM, ürün açıklamaları oluşturma, öznitelik değerlerini çıkarma, ürünleri otomatik kategorize etme ve içeriği birden fazla dile çevirme dahil olmak üzere yapay zeka destekli içerik zenginleştirme sağlar.

---

## 11. Medya ve Dijital Varlıklar

### Genel Bakış

PIM medya sistemi, ürün görselleri, teknik çizimler, videolar ve belgeleri yöneten kapsamlı bir dijital varlık yönetimi (DAM) katmanı sağlar.

---

## 12. Dışa Aktarım ve Entegrasyon

### Genel Bakış

PIM dışa aktarım sistemi, ürün verilerini birden fazla formatta dış sistemlere aktarmak için kapsamlı bir altyapı sağlar. JSON, CSV, XML ve BMEcat formatlarını destekler.

#### Desteklenen Dışa Aktarım Formatları

| Format | Açıklama | Tipik Kullanım |
|--------|----------|----------------|
| **JSON** | JavaScript Nesne Gösterimi | API entegrasyonları, headless ticaret |
| **CSV** | Virgülle Ayrılmış Değerler | Toplu işlemler, elektronik tablo araçları |
| **XML** | Genişletilebilir İşaretleme Dili | B2B veri alışverişi, GS1 uyumu |
| **BMEcat** | Avrupa B2B standart formatı | Tedarik platformları, endüstriyel kataloglar |

### 12.2 BMEcat Dışa Aktarımı

**Kaynak:** `frappe_pim.pim.services.bmecat`
**Amaç:** BMEcat 2005 (varsayılan) ve BMEcat 1.2 (eski uyumluluk) formatlarında XML kataloğu oluşturmak.

**ISO 639-2 Dil Eşlemesi (BMEcat):**

| Frappe Kodu | ISO 639-2 | Dil |
|-------------|-----------|-----|
| `en` | `eng` | İngilizce |
| `de` | `deu` | Almanca |
| `fr` | `fra` | Fransızca |
| `es` | `spa` | İspanyolca |
| `it` | `ita` | İtalyanca |
| `nl` | `nld` | Felemenkçe |
| `pl` | `pol` | Lehçe |
| `tr` | `tur` | Türkçe |
| `ru` | `rus` | Rusça |
| `zh` | `zho` | Çince |
| `ja` | `jpn` | Japonca |
| `ko` | `kor` | Korece |

---

## 13. Uluslararasılaştırma

### Genel Bakış

PIM, ürün verilerinin birden fazla dilde yönetilmesini sağlayan kapsamlı çok dilli destek sunar. `is_localizable` bayrağı taşıyan öznitelikler, ürün başına birden fazla dilde değer saklayabilir.

---

## 14. Paketleme ve Ambalajlama

### Genel Bakış

PIM, ürün paketlerini ve paketleme yapılarını yönetmek için DocType'lar sağlar. Bu, birden fazla ürünü bir arada satan perakendeciler ve GS1 ambalaj hiyerarşisi gerektiren üreticiler için kritik öneme sahiptir.

---

## 15. MDM (Ana Veri Yönetimi)

### Genel Bakış

MDM modülü, birden fazla kaynak sistemden gelen ürün verilerini tek bir yetkili "altın kayıt"ta birleştirmek için araçlar sağlar. Bu, birden fazla ERP, e-ticaret platformu veya tedarikçi veri beslemesi kullanan kuruluşlar için kritik öneme sahiptir.

### 15.1 Golden Record

**DocType:** `Golden Record`
**Amaç:** Birden fazla kaynak sistemden gelen verilerin birleştirilmesiyle oluşturulan tek yetkili ürün kaydı.

### 15.4 Survivorship Rule

**DocType:** `Survivorship Rule`
**Amaç:** Birden fazla kaynaktan gelen kayıtları birleştirirken "kazanan" değeri seçme stratejisini tanımlar. Hayatta kalma kuralları, MDM çatışma çözümünün çekirdeğidir.

**Kural Tipleri:**

| Kural Tipi | Açıklama |
|-----------|----------|
| **Kaynak Önceliği** | Kaynak sisteme göre öncelik sıralaması |
| **En Güncel** | En son güncellenen değer kazanır |
| **En Yüksek Güven** | En yüksek güven puanına sahip değer kazanır |
| **Yetkili Kaynak** | Belirli bir kaynağın değeri her zaman kazanır |
| **En Eksiksiz** | En fazla doldurulan değer kazanır |
| **Özel** | Özel Python yöntemi ile belirlenir |

---

## 16. Önerilen Kurulum Yapılandırma Sıralaması

### Genel Bakış

Bu bölüm, yeni bir müşteri için Frappe PIM dağıtımı için **bağımlılık sıralı yapılandırma zincirini** tanımlar. Her faz bir öncekinin üzerine inşa edilir ve sıralama, bağımlı varlıkların (ör. Product Master) ön koşullarından (ör. Product Family, PIM Attribute) önce asla yapılandırılmamasını sağlar.

### Bağımlılık Grafiği

```
Faz 0: PIM Ayarları (Genel)
  │
  ├──▶ Faz 1: Temel Şema
  │      ├── PIM Attribute Type
  │      ├── PIM Attribute Group
  │      ├── PIM Attribute + PIM Attribute Option
  │      └── Product Family + Family Attribute Template + Family Variant Attribute
  │              │
  │              ├──▶ Faz 2: İçerik Altyapısı
  │              │      ├── PIM Product Type
  │              │      ├── Category (NestedSet)
  │              │      ├── Taxonomy + Taxonomy Node
  │              │      ├── Brand
  │              │      └── Manufacturer
  │              │              │
  │              │              ├──▶ Faz 3: Kalite ve Yönetişim
  │              │              │      ├── Data Quality Policy
  │              │              │      ├── Puanlama Ağırlıkları (PIM Ayarları)
  │              │              │      ├── Roller ve İzinler
  │              │              │      ├── PIM Category Permission
  │              │              │      └── Data Steward
  │              │              │              │
  │              │              │              ├──▶ Faz 4: Kanal ve Dışa Aktarım Kurulumu
  │              │              │              │      ├── Channel (Satış Kanalları)
  │              │              │              │      ├── Export Profile
  │              │              │              │      ├── Channel Attribute Requirement
  │              │              │              │      └── Channel Locale
  │              │              │              │              │
  │              │              │              │              ├──▶ Faz 5: Gelişmiş Özellikler
  │              │              │              │              │      ├── Yapay Zeka Yapılandırması
  │              │              │              │              │      ├── GS1 Ambalaj Hiyerarşisi
  │              │              │              │              │      ├── PIM Bundle
  │              │              │              │              │      ├── Price Rule
  │              │              │              │              │      └── MDM (Kaynak Sistemler, Hayatta Kalma Kuralları)
  │              │              │              │              │
  │              │              │              │              └──▶ Faz 6: İçerik Oluşturma
  │              │              │              │                     ├── Product Master
  │              │              │              │                     ├── Product Variant
  │              │              │              │                     ├── Product Attribute Value
  │              │              │              │                     ├── Product Media
  │              │              │              │                     └── Product Channel Ataması
  │              │              │              │                            │
  │              │              │              │                            └──▶ Faz 7: Canlıya Geçiş
  │              │              │              │                                   ├── İş Akışı Aktivasyonu
  │              │              │              │                                   ├── Kanal Yayınlama
  │              │              │              │                                   ├── Dışa Aktarım Besleme Zamanlaması
  │              │              │              │                                   └── ERPNext Senkronizasyon Aktivasyonu
```

### Faz 0: Genel Yapılandırma (PIM Ayarları)

**Süre:** 30 dakika – 1 saat
**Rol:** System Manager
**Bağımlılık:** Yok — bu tüm yapılandırmanın köküdür

| Adım | Ayar | DocType / Alan | Açıklama |
|------|------|----------------|----------|
| 0.1 | ERP Senkronizasyonunu Etkinleştir | `PIM Settings.enable_erp_sync` | ERPNext entegrasyonunun aktif olup olmadığına karar verin |
| 0.2 | Senkronizasyon Yönü | `PIM Settings.sync_direction` | `PIM to ERP`, `ERP to PIM` veya `Bidirectional` |
| 0.3 | Varsayılan Şirket | `PIM Settings.default_company` | ERPNext Ürün oluşturma için |
| 0.4 | Kaydetmede Otomatik Senkronizasyon | `PIM Settings.auto_sync_on_save` | Otomatik senkronizasyon tetikleyicisini etkinleştir/devre dışı bırak |
| 0.5 | Yapay Zeka Zenginleştirme | `PIM Settings.enable_ai_enrichment` | Yapay zeka destekli içerik oluşturmayı etkinleştir |
| 0.6 | Yapay Zeka Sağlayıcı | `PIM Settings.ai_provider` | `OpenAI`, `Anthropic`, `Google Gemini`, vb. |
| 0.7 | Yapay Zeka API Anahtarı | `PIM Settings.ai_api_key` | Sağlayıcı API anahtarı (şifre alanı) |
| 0.8 | Yapay Zeka Modeli | `PIM Settings.ai_model` | Model tanımlayıcı (ör. `gpt-4o`, `claude-3-sonnet`) |
| 0.9 | Kalite Puanlama | `PIM Settings.enable_quality_scoring` | Çok boyutlu puanlamayı etkinleştir |
| 0.10 | Min Kalite Puanı | `PIM Settings.minimum_quality_score` | Kanal yayınlama eşiği (0–100) |
| 0.11 | Medya Maks Boyutu | `PIM Settings.max_file_size_mb` | Maksimum yükleme boyutu (MB) |
| 0.12 | İzin Verilen Formatlar | `PIM Settings.allowed_image_formats` | Virgülle ayrılmış liste (ör. `jpg,png,webp`) |

---

## 17. Uç Durumlar ve Dağıtım Senaryoları

### 17.1 Sıfırdan Kurulum vs. Göç

#### Sıfırdan Kurulum (Greenfield)

**Tanım:** Mevcut ürün verisi olmadan tamamen yeni bir PIM dağıtımı.
**Yaklaşım:** Bölüm 16'daki standart Faz 0–7 sıralamasını takip edin.

#### Göç (Mevcut Sistemden)

**Tanım:** Mevcut bir sistemden (ERP, e-ticaret platformu, elektronik tablolar, eski PIM) ürün verilerinin taşınması.

**Değiştirilmiş Sıralama:**

```
Standart Faz 0–3   →   Göç Eşleme Fazı   →   Veri İçe Aktarımı   →   Faz 4–7
                                │
                                ├── Kaynak alanları PIM özniteliklerine eşle
                                ├── Kaynak kategorileri Ürün Ailelerine eşle
                                ├── Kaynak ürün tiplerini PIM Ürün Tiplerine eşle
                                ├── Veri temizleme kurallarını tanımla
                                ├── Öznitelik değer eşlemeleri oluştur (normalleştirme)
                                └── Duplikat tespit stratejisi tanımla
```

### 17.2 Tek Şirket vs. Çoklu Şirket

#### Tek Şirket
**Tanım:** Tek şirket varlığı ile standart dağıtım.
**Yaklaşım:** Standart Faz 0–7. `PIM Settings.default_company` bir kez ayarlayın ve tüm ERP senkronizasyon işlemleri bu şirketi kullanır.

#### Çoklu Şirket
**Tanım:** ERPNext birden fazla şirketle yapılandırılmıştır (ör. bölgesel yan kuruluşlar, holding şirket yapısı).

### 17.3 ERPNext İle vs. ERPNext Olmadan

#### ERPNext İle (Tam Entegrasyon)
**Tanım:** Frappe PIM, çift yönlü senkronizasyon etkinleştirilmiş olarak ERPNext ile birlikte dağıtılır.

#### ERPNext Olmadan (Bağımsız PIM)
**Tanım:** Frappe PIM, ERPNext olmadan bağımsız bir ürün bilgi sistemi olarak dağıtılır.

---

## 18. Müşteri Arketip Detaylı İncelemeleri

### 18.4 Arketip Karşılaştırma Matrisi

| Boyut | Moda Perakendecisi | Endüstriyel Tedarikçi | Gıda Üreticisi |
|-------|--------------------|-----------------------|----------------|
| **Katalog Boyutu** | 2K–10K SKU | 50K–200K SKU | 500–5K SKU |
| **Öznitelik Sayısı** | 30+ | 80+ | 60+ |
| **Varyant Karmaşıklığı** | Beden × Renk (ürün başına 5–30 SKU) | Çok eksenli (ürün başına 50–200+ SKU) | Ağırlık × Lezzet (ürün başına 3–10 SKU) |
| **Ürün Aileleri** | 4–8 | 12–20+ | 5–8 |
| **Kanallar** | 4–6 (B2C pazar yerleri) | 2–4 (B2B + pazar yerleri) | 3–5 (B2C + perakende portalları) |
| **Diller** | 2–3 | 4–5+ | 3–4 |
| **Birincil Dışa Aktarım Formatı** | JSON/API | BMEcat 2005 XML | GS1 XML / BMEcat |
| **Kalite Puan Eşiği** | 75 | 85 | 90 |
| **Yapay Zeka Kullanım Durumu** | Pazarlama metni, çeviriler | Teknik açıklamalar, çeviriler | Pazarlama metni (beslenme verileri DEĞİL) |
| **Uyumluluk Yükü** | Düşük (tekstil etiketleme) | Orta (CE, RoHS, SDS) | Yüksek (FDA, AB 1169, alerjenler) |
| **ERP Senkronizasyon Yönü** | PIM → ERP | Çift Yönlü | PIM → ERP |
| **MDM Gerekli mi?** | Nadiren | Sıklıkla (birden fazla kaynak) | Bazen |
| **GS1 Karmaşıklığı** | Yalnızca GTIN-13 | Tam hiyerarşi (4 seviye) | Tam hiyerarşi (3 seviye) |
| **Medya Odağı** | Yaşam tarzı fotoğrafçılığı | Teknik çizimler | Ürün + etiket fotoğrafçılığı |
| **Puanlama Vurgusu** | Medya + Çeviri | Öznitelik + Çeviri | Öznitelik + Uyumluluk |
| **Kurulum Süresi** | 1–2 hafta | 3–4 hafta | 2–3 hafta |

---

## Ek B: Belge Değişiklik Günlüğü

| Versiyon | Tarih | Yazar | Değişiklikler |
|----------|-------|-------|---------------|
| 1.0 | Şubat 2026 | Uygulama Ekibi | İlk sürüm — tüm 15 alan + 3 ek bölüm |

---

## Ek C: Sözlük

| Terim | Tanım |
|-------|-------|
| **Paket Deseni** | Yapılandırma varlıklarının (tipler) içerik varlıklarının (kayıtlar) yapısını tanımladığı Drupal'dan esinlenen mimari |
| **EAV** | Varlık-Öznitelik-Değer — özniteliklerin sütunlar yerine satırlar olarak saklandığı dinamik şema deseni |
| **Ürün Ailesi** | Bir dizi ürüne hangi özniteliklerin ve varyant eksenlerinin uygulanacağını belirleyen temel yapılandırma varlığı |
| **Product Master** | Paylaşılan verileri içeren üst ürün kaydı; bireysel SKU'lar için Product Variant'lar oluşturur |
| **Product Variant** | Product Master'dan türetilen, varyant eksen değerleriyle (ör. beden + renk) farklılaşan belirli bir SKU |
| **Kanal** | Ürünlerin yayınlandığı bir satış veya dağıtım platformu (ör. Amazon, Shopify, Trendyol) |
| **Tamlık Puanı** | Belirli bir kanal için gereken alanların ne kadarının doldurulduğunu gösteren yüzde |
| **Kalite Puanı** | İçerik, medya, SEO, çeviri, öznitelik ve pazar hazırlığı puanlarını birleştiren çok boyutlu puan (0–100) |
| **Altın Kayıt** | Birden fazla kaynak sistemden gelen verilerin birleştirilmesiyle oluşturulan tek yetkili ürün kaydı (MDM) |
| **Hayatta Kalma Kuralı** | Çelişen verileri birleştirirken hangi kaynak sistemin değerinin kazanacağını belirleyen alan düzeyinde kurallar |
| **Veri Sorumlusu** | Belirli kategoriler veya ürün aileleri içindeki ürün veri kalitesi sorumluluğu atanmış kullanıcı |
| **Dışa Aktarım Profili** | Ürünlerin nasıl dışa aktarılacağını tanımlayan yapılandırma: format, filtreler, alan eşlemesi, zamanlama |
| **NestedSet** | Frappe'nin verimli hiyerarşi sorguları için sol/sağ değerleri kullanan ağaç yapısı uygulaması |
| **BMEcat** | B2B tedarik alanında kullanılan Avrupa elektronik ürün kataloğu standardı (XML formatı) |
| **GS1** | Global Standards 1 — GTIN barkodlarını, ambalaj hiyerarşisini ve veri standartlarını yöneten kuruluş |
| **GTIN** | Global Ticari Ürün Numarası — ürünleri tanımlayan barkod numarası (GTIN-8, GTIN-13, GTIN-14) |
| **GDSN** | Global Veri Senkronizasyon Ağı — ticari ortaklar arasında ürün verisi alışverişi için GS1 standardı |
