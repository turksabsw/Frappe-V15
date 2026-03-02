# Frappe PIM - Paradigma ve Yaklaşım Rehberi

## Temel Felsefe

### "Ürün Merkezi Evren" Yaklaşımı

PIM'de ürün bir güneş gibidir. Tüm diğer kavramlar (attribute, paket, içerik, yorum, katkıda bulunanlar) bu güneşin etrafında dönen gezegenlerdir. Kullanıcı ürüne baktığında, o ürünle ilgili evreni tek bir noktadan görmelidir.

**Mevcut Sorun:** Bilgi dağınık. Kullanıcı farklı ekranlara gidip gelerek ürün hakkında fikir edinmeye çalışıyor.

**Olması Gereken:** Product Master bir "kontrol merkezi" gibi çalışmalı. Alt kısımdaki connections paneli ile ilişkili her şey tek bakışta erişilebilir olmalı.

---

## Kavramsal Ayrımlar

### Product Family Paradoksu

**Yanlış düşünce:** "Klavye + Mouse birlikte satılıyor, o zaman bir aile."

**Doğru düşünce:** Aile, ortak DNA taşıyan bireylerden oluşur. Mouse ailesi, mouse DNA'sı taşır. Klavye ailesi, klavye DNA'sı taşır. İkisini bir kutuya koymak onları akraba yapmaz - sadece komşu yapar.

Paket/Bundle kavramı ayrı bir şeydir. Product Family soy ağacıdır, Bundle ise alışveriş sepetidir.

### Attribute vs Entity Yanılgısı

**Yanlış düşünce:** "Vitaminler önemli, ayrı bir DocType olsun."

**Doğru düşünce:** Vitamin bir attribute'tur. Renk nasıl attribute ise, vitamin de öyle. Sektörel önem, kavramsal kategoriyi değiştirmez.

Bir şeyin "önemli" olması onu ayrı bir entity yapmaz. Önemli olan şeyler, iyi tasarlanmış attribute sistemleri içinde de önemli kalır.

---

## Şablon Düşüncesi

### "Kalıp ve Döküm" Metaforu

Attribute Template bir kalıptır. Bu kalıba malzeme (değerler) döküldüğünde, ürün attribute'ları ortaya çıkar.

**Akış:**
1. Kalıp tasarla (Besin Değerleri Şablonu)
2. Kalıbı seç
3. Malzemeyi dök (değerleri gir)
4. Ürün çıksın

Şablon, tekrar eden yapıların standartlaştırılmasıdır. Her seferinde sıfırdan attribute tanımlamak yerine, sektörel kalıplar kullanılır.

### Şablon Export/Import Döngüsü

Şablonlar taşınabilir olmalı. Bir şablon:
- Export edilebilmeli (başka sistemlere)
- Import edilebilmeli (başka sistemlerden)
- Versiyon kontrolü yapılabilmeli

Bu, bilgi kaybını önler ve standartlaşmayı sağlar.

---

## Attribute Tasarım Felsefesi

### Gruplama vs Tanımlama Ayrımı

**Attribute Group:** Sadece organizasyon amaçlı. "Bu attribute'lar birlikte anlamlı" der. Görsel özellik taşımaz.

**Attribute:** Gerçek değer taşıyıcı. Renk seçici, birim, değer - hepsi burada yaşar.

Gruplama, kütüphanedeki raf sistemidir. Kitabın kendisi attribute'tur. Rafın rengi önemli değil, kitabın içeriği önemli.

### Birim Esnekliği

Değerler bağlamsızdır. "500" tek başına anlamsız. "500ml", "$500", "%500" - bunlar anlamlı.

Birim sistemi iki yönlü düşünülmeli:
- Önde gelen birimler: $, €, ₺
- Sonda gelen birimler: kg, ml, %, °C

Bu esneklik, global ürün yönetiminde kritik.

---

## İlişki Düşüncesi

### Connections Yaklaşımı

Frappe'nin güçlü yanı link sistemleri. Bu sistem "ben sana bağlıyım" yerine "biz birbirimize bağlıyız" demeyi sağlar.

Product Master'ın altında görünmesi gerekenler:
- Paket tipleri (bu ürün hangi ambalajlarda?)
- Katkıda bulunanlar (kim ne yaptı?)
- İçerikler (hangi açıklamalar var?)
- Yorumlar (müşteriler ne diyor?)
- Varyantlar (hangi versiyonları var?)
- Fiyat kuralları (nasıl fiyatlandırılıyor?)
- BOM (nelerden oluşuyor?)
- SDS dokümanları (güvenlik bilgileri nerede?)

Bu bağlantılar "lazy loading" mantığıyla çalışmalı - her zaman yüklü değil, ama her zaman erişilebilir.

### BOM Entegrasyonu Düşüncesi

BOM (Bill of Materials) üretim tarafının konusu. PIM pazarlama/satış tarafının konusu. Ama ikisi aynı ürünü konuşuyor.

Bu iki dünya birbirine "köprü" ile bağlanmalı, "birleşme" ile değil. Her biri kendi bütünlüğünü korumalı ama diğerinden haberdar olmalı.

---

## Yorum Sistemi Düşüncesi

### Hepsiburada Modeli

Klasik yorum: "Ürün güzeldi, beğendim." - Enformasyon değeri düşük.

Attribute bazlı yorum: "Pil ömrü: 4/5, Ergonomi: 5/5, Fiyat/Performans: 3/5" - Enformasyon değeri yüksek.

Bu yaklaşım, yorumları yapısal dataya dönüştürür. Yapısal data analiz edilebilir, karşılaştırılabilir, raporlanabilir.

---

## Çeviri Düşüncesi

### Merkezi vs Dağıtık Çeviri

**Dağıtık:** Her DocType'ta ayrı çeviri alanları. Karmaşık, tutarsız.

**Merkezi:** Tek bir çeviri havuzu. Her şey oraya işaret eder. Tutarlı, yönetilebilir.

Çeviri, içeriğin gölgesidir. Gölge ayrı yaşamaz, ama ayrı yönetilir.

---

## Mock Data Düşüncesi

### Test Verisi Felsefesi

Boş sistem değerlendirilemez. Dolu sistem yavaş doldurulur. Mock data bu açığı kapatır.

Mock data "sahte" değil, "örnek" olarak düşünülmeli. Sistemin kapasitesini gösterir, edge case'leri ortaya çıkarır.

---

## İçerik Yönetimi Düşüncesi

### Kategori Odaklı İçerik

İçerik kategorisi bir şablondur. "Pazarlama açıklaması şöyle yazılır", "Teknik özellikler şöyle listelenir" der.

Kullanıcı kategori seçer, sistem o kategorinin şablonunu sunar, kullanıcı doldurur, içerik ürüne bağlanır.

Bu, içerik tutarlılığını sağlar. Herkes kendi kafasına göre yazmak yerine, standart yapılara uyar.

---

## Web Builder Düşüncesi

### PIM + Sunum Katmanı

PIM veriyi yönetir. Web Builder veriyi sunar. İkisi farklı sorumluluklar.

Ama ikisi arasında "besleme" ilişkisi olmalı. PIM'deki veri, otomatik olarak web sayfalarına akmalı.

Bu entegrasyon Phase 2 konusu. Önce veri yönetimi sağlam olmalı, sonra sunum katmanı eklenmeli.

---

## SDS ve Uyumluluk Düşüncesi

### Regülasyon Odaklı Tasarım

SDS (Safety Data Sheet) yasal zorunluluk. ECHA piktogramları standart.

Bu tür regülasyon gereksinimleri "olsa iyi olur" değil, "olmak zorunda" kategorisinde. Sistem bu zorunlulukları birinci sınıf vatandaş olarak ele almalı.

Piktogramlar görsel attribute gibi düşünülebilir - ama yasal bağlayıcılığı olan attribute.

---

## Önceliklendirme Düşüncesi

### Temel Önce, Süsleme Sonra

1. **Önce:** Attribute sistemi doğru çalışsın
2. **Sonra:** Şablon motoru eklensin
3. **Daha sonra:** Yorum, içerik, web builder

Sağlam temel olmadan üst katlar çöker. Attribute sistemi PIM'in temeli. Burası sağlam olmalı.

---

## Mevcut Yapıda Gözlemler

Workspace'indeki mevcut gruplamalar mantıklı. Ama bazı kavramsal düzeltmeler gerekli:

**Nutrition Facts:** Ayrı entity olarak durması tartışmalı. Attribute Template yaklaşımıyla absorbe edilebilir. Ama "şimdilik kalsın" kararı pragmatik - önce kritik düzeltmeler yapılmalı.

**Price Rule:** Doğru yerde. Ama Price List ile bağlantısı güçlendirilmeli.

**Chemical Usage Instruction:** SDS sistemiyle entegre düşünülmeli.

**Package Variant vs GS1 Packaging Hierarchy:** İkisi farklı şeyler. Package Variant ürün varyantı, GS1 standart hiyerarşi. Karıştırılmamalı.

---

## Sonuç: Üç Temel Prensip

1. **Merkezilik:** Ürün merkezde, her şey ona bağlı ve ondan erişilebilir

2. **Genelleştirme:** Sektörel kavramlar (vitamin, mineral, vb.) genel attribute sistemine dönüştürülmeli

3. **Bağlantısallık:** DocType'lar izole değil, connections ile birbirine bağlı bir ağ oluşturmalı

Bu üç prensip, tüm kararların filtresi olmalı. Her yeni özellik, her değişiklik bu prensiplere uygunluk açısından değerlendirilmeli.