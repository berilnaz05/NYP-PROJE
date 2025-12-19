from repository import BellekUlasimRepository
from implementations import Otobus, Bisiklet, Scooter


print("\n========== TEST BASLIYOR ==========\n")


repo = BellekUlasimRepository()
print("Repository oluşturuldu")

otobus1 = Otobus(
    arac_id=1,
    kapasite=40,
    kalkis="A Kapısı",
    bitis="B Kapısı",
    mevcut_konum="Garaj",
    durum="Boşta",
    guzergah=["yurtlar", "rektrlük", "yemekhane"],
    hat_no="K1",
    km_ucreti=2.5
)
otobus1.mesafe_ayarla(12)

otobus2 = Otobus(
    arac_id=2,
    kapasite=30,
    kalkis="Yurtlar",
    bitis="Merkez",
    mevcut_konum="Garaj",
    durum="Seferde",
    guzergah=["Yurtlar", "Merkez","kütüphane"],
    hat_no="K2",
    km_ucreti=3
)
otobus2.mesafe_ayarla(8)


bisiklet1 = Bisiklet(
    arac_id=4,
    kapasite=1,
    kalkis="",
    bitis="",
    mevcut_konum="İstasyon 1",
    durum="Boşta",
    guzergah=[],
    elektrikli=True,
    batarya=100
)

scooter1 = Scooter(
    arac_id=5,
    kapasite=1,
    kalkis="",
    bitis="",
    mevcut_konum="İstasyon 2",
    durum="Boşta",
    guzergah=[],
    hiz=25,
    dakika_ucreti=1.8
)

print("Araçlar oluşturuldu")


repo.ekle(otobus1)
repo.ekle(otobus2)
repo.ekle(bisiklet1)
repo.ekle(scooter1)

print("Araçlar repository'e eklendi")


print("\n--- Tüm Araçlar ---")
for arac in repo.tumunu_getir():
    print(arac.bilgi_ver())
    
print("\n--- Seferde Olan Araçlar ---")
for arac in repo.seferde_olanlar():
    print(arac.bilgi_ver())


print("\n--- Sadece Otobüsler ---")
for arac in repo.tipe_gore_getir(Otobus):
    print(arac.bilgi_ver())


print("\n--- Kapasitesi 20 ve üzeri olanlar ---")
for arac in repo.kapasiteye_gore_getir(20):
    print(arac.bilgi_ver())

print("\n--- Bisiklet Kullanımı ---")
bisiklet1.sefer_baslat()
bisiklet1.sure_ekle(20)
print(bisiklet1.bilgi_ver())

print("\n--- Scooter Kullanımı ---")
scooter1.sefer_baslat()
scooter1.sure_ekle(15)
print(scooter1.bilgi_ver())

print("\n--- Raporlar ---")
print("Toplam araç sayısı:", repo.arac_sayisi())
print("Tip özeti:", repo.tip_ozeti())
print("Durum özeti:", repo.durum_ozeti())

print("\n--- Araç Silme ---")
repo.sil(5)
print("Scooter silindi")

print("Kalan araçlar:")
for arac in repo.tumunu_getir():
    print(arac.bilgi_ver())

print("\n========== TEST BITTI ==========\n")