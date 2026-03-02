# Auto-Claude Kullanım Rehberi - Frappe PIM
> Bu rehber, Auto-Claude ile PIM projesini düzeltmek için adım adım talimatlar içerir

---

## 📁 Auto-Claude'a Verilecek Dosyalar

### Spec Klasörüne Kopyalanacak .md Dosyaları

Auto-Claude projenizi açtıktan sonra, `specs/` klasörüne bu dosyaları koyun:

| Dosya | Amaç |
|-------|------|
| `PIM_FIX_SPEC.md` | Ana görev tanımı - 7 kritik sorunu çözecek talimatlar |
| `PIM_CONTEXT.md` | Proje bağlamı - mimari, standartlar, kurallar |
| `PIM_MERGER.md` | Worktree birleştirme talimatları |

### Proje Kök Dizinine Kopyalanacak Referans Dosyaları

Bu dosyalar Auto-Claude'un projeyi anlaması için gerekli:

```
frappe_pim/
├── CLAUDE.md          ← Mevcut (proje standartları)
├── 01_ARCHITECTURE.md ← Mevcut (mimari diyagramlar)
├── 02_CONFLICTS.md    ← Mevcut (bilinen sorunlar)
├── 03_DOCTYPES_SPEC.md ← Mevcut (DocType tanımları)
├── 04_CHILD_TABLES.md ← Mevcut (child table tanımları)
├── 05_ERPNEXT_SYNC.md ← Mevcut (sync kodu)
├── 06_IMPLEMENTATION.md ← Mevcut (uygulama adımları)
```

---

## 🚀 Auto-Claude Başlatma Adımları

### Adım 1: Projeyi Aç
```bash
# Auto-Claude'u başlat ve proje klasörünü seç:
/home/bora/Masaüstü/Frappe-V15/frappe-bench/apps/frappe_pim
```

### Adım 2: Spec Oluştur
Auto-Claude UI'da veya CLI'da:

```bash
cd apps/backend
python spec_runner.py --task "Fix all critical PIM issues" --complexity complex
```

Veya interaktif mod:
```bash
python spec_runner.py --interactive
```

**Görev açıklaması olarak şunu gir:**
```
Fix Frappe PIM application critical issues:
1. Fix pim_attribute_type.py imports and indentation
2. Create missing child table DocTypes (Family Attribute Template, Family Variant Attribute, Product Type Field)
3. Enhance PIM Product Type with custom fields capability
4. Create ERPNext custom fields fixture
5. Fix Product Master field mapping inconsistencies
6. Implement Product Variant controller
7. Verify ERPNext sync works bidirectionally

Reference: @PIM_FIX_SPEC.md for detailed acceptance criteria
Context: @PIM_CONTEXT.md for project standards
```

### Adım 3: Spec'i Çalıştır
```bash
python run.py --spec 001
```

### Adım 4: İlerlemeyi İzle
- Auto-Claude her session'da ilerleme kaydeder
- `specs/001-xxx/build-progress.txt` dosyasını kontrol et
- Sorun olursa `HUMAN_INPUT.md` dosyasına talimat yaz

### Adım 5: İnceleme ve Birleştirme
```bash
# Değişiklikleri incele
python run.py --spec 001 --review

# Değişiklikleri birleştir
python run.py --spec 001 --merge
```

---

## 🔧 Alternatif: Manuel Spec Dosyası Oluşturma

Auto-Claude UI kullanmak istemezseniz, manuel spec oluşturun:

### 1. Klasör Yapısı
```
frappe_pim/
└── .auto-claude/
    └── specs/
        └── 001-pim-critical-fixes/
            ├── spec.md          ← PIM_FIX_SPEC.md içeriği
            ├── context.json     ← Otomatik oluşur
            └── requirements.json ← Otomatik oluşur
```

### 2. spec.md İçeriği
`PIM_FIX_SPEC.md` dosyasının içeriğini kopyalayın.

### 3. Çalıştır
```bash
cd .auto-claude
python run.py --spec 001-pim-critical-fixes
```

---

## ⚠️ Önemli Notlar

### Session Sınırları
Auto-Claude her session'da belirli miktarda iş yapar. PIM fix için tahmini:
- **Session 1-2**: pim_attribute_type.py düzeltmeleri
- **Session 3-4**: Child table DocType'ları oluşturma
- **Session 5**: PIM Product Type geliştirme
- **Session 6**: Fixtures oluşturma
- **Session 7-8**: Product Master ve Variant düzeltmeleri
- **Session 9-10**: Test ve entegrasyon

### İnsan Müdahalesi Gerektiğinde
`HUMAN_INPUT.md` dosyası oluşturun:
```markdown
# Human Input Required

## Problem
[Auto-Claude'un takıldığı yeri açıkla]

## Guidance
[Ne yapması gerektiğini açıkla]

## Priority
[Önce neye odaklanmalı]
```

### Worktree Birleştirme
Her spec tamamlandığında:
1. `python run.py --spec 001 --review` ile incele
2. Test et: `bench --site frappe.local migrate`
3. `python run.py --spec 001 --merge` ile birleştir
4. `PIM_MERGER.md` talimatlarını takip et

---

## 📊 Beklenen Çıktılar

### Oluşturulacak Yeni Dosyalar
```
frappe_pim/pim/doctype/
├── family_attribute_template/
│   ├── __init__.py
│   ├── family_attribute_template.json
│   └── family_attribute_template.py
├── family_variant_attribute/
│   ├── __init__.py
│   ├── family_variant_attribute.json
│   └── family_variant_attribute.py
├── product_type_field/
│   ├── __init__.py
│   ├── product_type_field.json
│   └── product_type_field.py

frappe_pim/fixtures/
└── custom_field.json
```

### Değiştirilecek Mevcut Dosyalar
```
pim_attribute_type.py      ← Import + indentation fix
pim_product_type.json      ← Add type_fields, allowed_families
product_master.py          ← Consolidate field mappings
product_variant.py         ← Full implementation
hooks.py                   ← Verify fixtures
```

---

## 🧪 Doğrulama Komutları

Her aşamadan sonra çalıştır:

```bash
# 1. Python syntax kontrolü
find frappe_pim -name "*.py" -exec python -m py_compile {} \;

# 2. Migration testi
bench --site frappe.local migrate

# 3. Cache temizle
bench --site frappe.local clear-cache

# 4. Console'da test
bench --site frappe.local console
>>> frappe.new_doc("PIM Attribute Type")
>>> frappe.new_doc("Product Family")
>>> frappe.new_doc("Product Master")
```

---

## 🔄 Sorun Giderme

### "Module not found" Hatası
```bash
bench --site frappe.local clear-cache
bench restart
```

### "DocType not found" Hatası
```bash
bench --site frappe.local migrate
```

### Sync Loop (Sonsuz Döngü)
`product_variant.py` ve `product_master.py` dosyalarında `_from_pim_sync` flag kontrolü yapıldığından emin ol.

### Worktree Conflict
```bash
# Worktree'yi temizle
git worktree remove .worktrees/auto-claude/001-xxx --force
git worktree prune
```
