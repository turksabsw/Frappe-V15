Frappe PIM için diğer uygulamalarla entegrasyon sağlayacak kapsamlı bir JSON yapısı oluşturuyorum:Frappe PIM entegrasyon prompt'unu JSON formatında oluşturdum.

**Kapsam:**

**Temel Entegrasyonlar:**
- ERPNext (Item, BOM, Stock, Pricing Rule senkronizasyonu)
- Frappe Insights (BI dashboardları)
- Frappe Builder (Web sunum katmanı)
- Print Designer (Etiket ve katalog)

**İletişim & CRM:**
- Frappe CRM (Müşteri-ürün ilişkisi)
- Raven (Takım bildirimleri)
- WhatsApp Integration (Müşteri alertleri)

**Veri & API:**
- Frappe GraphQL (API katmanı)
- Sheets Integration (Toplu import/export)
- Background Tasks Unleashed (Zamanlanmış görevler)

**AI & Depolama:**
- Frappe MCP (AI destekli içerik üretimi, çeviri, sentiment analizi)
- DFP External Storage (S3 medya depolama)

**Yapı:**
- `doctypes`: Tüm DocType tanımları
- `integrations`: Her app için hook'lar ve sync ayarları
- `api`: REST endpoint'leri ve webhook'lar
- `hooks`: doc_events ve scheduler_events
- `fixtures`: ECHA piktogramları, attribute grupları
- `permissions`: Rol bazlı yetkilendirme
- `workspace`: UI organizasyonu