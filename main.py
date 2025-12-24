# Ödeme türleri
from payment.subclass import KrediKartiOdeme, NakitOdeme, DijitalCuzdanOdeme

# Servisler
from payment.services.menu_service import MenuService
from payment.services.siparis_service import SiparisService
from payment.services.odeme_servise import OdemeService
from payment.services.raporlama_servise import RaporlamaService

# Modeller
from payment.models.odeme_model import OdemeModel
from payment.models.odeme_yontemi_model import OdemeYontemiModel


# 1️⃣ Menü ve ürünler
menu = MenuService()
menu.urun_ekle("Hamburger", 85, "Yemek")
menu.urun_ekle("Pizza", 110, "Yemek")
menu.urun_ekle("Kola", 20, "İçecek")
menu.urun_ekle("Su", 10, "İçecek")

print("📋 Menü:")
menu.menuyi_yazdir()
print("\n")

# 2️⃣ Sipariş oluştur
siparis_service = SiparisService(menu)
siparis1 = siparis_service.siparis_olustur("Ahmet", ["Hamburger", "Kola"])
siparis2 = siparis_service.siparis_olustur("Ayşe", ["Pizza", "Su"])

print("🛒 Siparişler oluşturuldu:")
siparis_service.siparis_goster(siparis1["siparis_id"])
siparis_service.siparis_goster(siparis2["siparis_id"])
print("\n")

# 3️⃣ Ödeme yöntemleri oluştur
kart = KrediKartiOdeme("Ahmet", 200, "1234567812345678", "12/30", "123")
nakit = NakitOdeme("Ayşe", 150, "TL")
cuzdan = DijitalCuzdanOdeme("Mehmet", 300, "TL", "PayWallet", dogrulanmis=True)

odeme1 = OdemeYontemiModel(kart)
odeme2 = OdemeYontemiModel(nakit)
odeme3 = OdemeYontemiModel(cuzdan)

# 4️⃣ Ödemeleri yap
odeme_service = OdemeService()
print("💳 Ödeme İşlemleri:")
odeme_service.odeme_yap(kart, siparis1["toplam_tutar"])
odeme_service.odeme_yap(nakit, siparis2["toplam_tutar"])
odeme_service.odeme_yap(cuzdan, 50)  # örnek küçük ödeme

# 5️⃣ Fiş ve geçmiş
print("\n📄 Son fişler:")
kart.fis_goster()
nakit.fis_goster()
cuzdan.fis_goster()

print("\n📂 Tüm ödeme işlemleri:")
odeme_service.odeme_gecmisini_goster()

# 6️⃣ Raporlama
raporlama = RaporlamaService(odeme_service)
print("\n📊 Genel Ödeme İstatistikleri:")
raporlama.odeme_istatistikleri()

print("\n👤 Kullanıcı Bazlı İstatistikler:")
raporlama.kullanici_istatistikleri("Ahmet")
raporlama.kullanici_istatistikleri("Ayşe")
raporlama.kullanici_istatistikleri("Mehmet")

# 7️⃣ OdemeModel örnekleri
print("\n💾 OdemeModel Detayları:")
odemem1 = OdemeModel(kart, 105)
odemem2 = OdemeModel(nakit, 120)
odemem1.odeme_yap()
odemem2.odeme_yap()
OdemeModel.tum_odemeleri_goster()

# 8️⃣ OdemeYontemiModel istatistikleri
print("\n📌 OdemeYontemiModel İstatistikleri:")
OdemeYontemiModel.istatistik()
OdemeYontemiModel.en_yuksek_bakiye()
OdemeYontemiModel.en_dusuk_bakiye()
OdemeYontemiModel.odeme_turlerine_gore()
OdemeYontemiModel.dogrulanmis_cuzdanlari_goster()

