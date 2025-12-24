# sadece rapor verir kullanıcı girdisi yok 

from base import Kapsam
from implementations import (
    UlasimYoneticisi,
    Scooter,
    Bisiklet,
    Otobus,
    Shuttle,
    MemoryTransportRepository,
    TransportService
)
from datetime import timedelta

print("-------------------------- Araç Raporlama Sistemi --------------------------\n\n")

yonetici = UlasimYoneticisi()
repo = MemoryTransportRepository()
service = TransportService(repo, yonetici)

# Araç oluşturma
scooter1 = Scooter(1, "A Kapısı", "B Kapısı", "Boşta", ["A","B"], True, 80, 2)
scooter2 = Scooter(2, "Yurtlar", "Kütüphane", "Boşta", ["Yurt","Merkez","Kütüphane"], True, 40, 2)

bisiklet1 = Bisiklet(3, "Spor Salonu", "Mühendislik", "Boşta", ["Spor","Yemekhane","Mühendislik"], False, 0)
bisiklet2 = Bisiklet(4, "Fen Fakültesi", "Merkez", "Boşta", ["Fen","Merkez"], True, 60)

otobus1 = Otobus(5, 40, "Ana Giriş", "Kampüs İçi", "Boşta", ["Giriş","Merkez","Yurtlar"], "K1", Kapsam.kampus_ici)
otobus2 = Otobus(6, 50, "Kampüs", "Şehir Merkezi", "Boşta", ["Kampüs","AVM","Merkez"], "D2", Kapsam.kampus_disi)

shuttle1 = Shuttle(7, 20, "Kampüs", "Şehir Merkezi", "Boşta", ["Kampüs","AVM","Merkez"], "S1", Kapsam.kampus_disi)
shuttle2 = Shuttle(8, 15, "kampüs", "Hastane", "Boşta", ["kampüs","meydan","hastane"], "S2", Kapsam.kampus_disi)

# Araçları repo ve yöneticiye ekleme

for arac in [scooter1, scooter2, bisiklet1, bisiklet2, otobus1, otobus2, shuttle1, shuttle2]:
    yonetici.arac_ekle(arac)
    repo.kaydet(arac.arac_id, arac)

# Örnek Seferler ve Kullanım

scooter1.sure_ekle(25)
service.sefer_baslat(sefer_id=101, arac_id=scooter1.arac_id)
yonetici.sefer_bitir(scooter1.arac_id)

bisiklet1.sure_ekle(15)
service.sefer_baslat(sefer_id=102, arac_id=bisiklet1.arac_id)
yonetici.sefer_bitir(bisiklet1.arac_id)

bisiklet2.sure_ekle(45)
service.sefer_baslat(sefer_id=110, arac_id=bisiklet2.arac_id)
yonetici.sefer_bitir(bisiklet2.arac_id)

otobus1.yolcu_ekle(15)
service.sefer_baslat(sefer_id=103, arac_id=otobus1.arac_id)
yonetici.sefer_bitir(otobus1.arac_id)

otobus2.yolcu_ekle(20)
service.sefer_baslat(sefer_id=120, arac_id=otobus2.arac_id)
yonetici.sefer_bitir(otobus2.arac_id)

scooter2.sure_ekle(35)
service.sefer_baslat(sefer_id=56, arac_id=scooter2.arac_id)
yonetici.sefer_bitir(scooter2.arac_id)

shuttle2.rezervasyon_yap("Ali", 1)
shuttle2.rezervasyon_yap("Veli", 1)
service.sefer_baslat(sefer_id=130, arac_id=shuttle2.arac_id)
yonetici.sefer_bitir(shuttle2.arac_id)

shuttle1.rezervasyon_yap("Ahmet", 3)
shuttle1.rezervasyon_yap("Ayşe", 2)
service.sefer_baslat(sefer_id=104, arac_id=shuttle1.arac_id)
yonetici.sefer_bitir(shuttle1.arac_id)

print("--------------------------------- Araç Durum Raporu ------------------------\n\n")
for arac in yonetici.araclar:
    bilgi = arac.bilgi_ver()
    print(f"ID: {bilgi['arac_id']} | Tip: {bilgi['tip']} | Durum: {bilgi['durum']}")
    print(f"Kapasite: {arac.kapasite} | Aktif Yolcu: {arac.aktif_yolcu} | Boş Kapasite: {arac.bos_kapasite()}")
    print(f"Müsait mi?: {'Evet' if arac.musait_mi() else 'Hayır'} | Doluluk Oranı: {arac.doluluk_orani()*100:.1f}%")
    print(f"Konum: {arac.mevcut_konum} | Zaman Bilgisi: {arac.zaman_bilgisi()}")
    if isinstance(arac, Shuttle):
        print(f"Rezervasyon Sayısı: {len(arac.rezervasyonlar)}")


# Genel Rapor Bilgileri

print("\n----------------------------------------- Genel Rapor ------------------------")
print("Toplam Gelir:", yonetici.toplam_gelir())
print("En Çok Kullanılan Araç Tipi:", yonetici.en_cok_kullanilan_tip())
print("Araç Sayısı Raporu:", yonetici.arac_sayisi_raporu())
print("\nBoşta Olan Araçlar:")
for bilgi in yonetici.duruma_gore_listele("Boşta"):
    print(bilgi)

print("\n\n-------------------------Tüm Araçlar------------------------")
for bilgi in yonetici.tum_araclari_listele():
    print(bilgi)


#  Ortalama ücret raporu

ortalama_ucret = yonetici.toplam_gelir() / len(yonetici.sefer_gecmisi) if yonetici.sefer_gecmisi else 0
print("\nOrtalama Ücret:", round(ortalama_ucret, 2))

#  En çok kullanılan güzergah raporu
def guzergah_sayac(yonetici):
    guzergah_sayac = {}
    # Aracları geziyoruz
    for arac in yonetici.araclar:
        for durak in arac.guzergah:
            guzergah_sayac[durak] = guzergah_sayac.get(durak, 0) + 1
    # En popüler durak
    en_populer_durak = max(guzergah_sayac, key=guzergah_sayac.get)
    print("En Çok Geçilen Durak:", en_populer_durak)

#  Araç tipine göre toplam gelir

def gelir_tip(yonetici):
   gelir_tip = {}
   for kayit in yonetici.sefer_gecmisi:
       tip = kayit["tip"]
       gelir_tip[tip] = gelir_tip.get(tip, 0) + kayit.get("ucret", 0)
   print("\nAraç Tipine Göre Gelir Dağılımı:")
   for tip, gelir in gelir_tip.items():
      print(f"{tip}: {gelir} TL")

#  en çok kullanılan araç tipi
def sayac(yonetici):
   sayac = {}
   for kayit in yonetici.sefer_gecmisi:
      tip = kayit["tip"]
      sayac[tip] = sayac.get(tip, 0) + 1
   top3 = sorted(sayac.items(), key=lambda x: x[1], reverse=True)[:3]
   print("\nTop 3 En Çok Kullanılan Araç Tipi:")
   for tip, adet in top3:
      print(f"{tip}: {adet} sefer")

#  Kampüs içi vs kampüs dışı gelir raporu

kampus_ici_gelir = sum(arac.ucret_hesapla() for arac in yonetici.araclar if arac.kapsam == Kapsam.kampus_ici)
kampus_disi_gelir = sum(arac.ucret_hesapla() for arac in yonetici.araclar if arac.kapsam == Kapsam.kampus_disi)
print("\nKapsama Göre Gelir Raporu:")
print("Kampüs İçi:", kampus_ici_gelir, "TL")
print("Kampüs Dışı:", kampus_disi_gelir,"TL")


# test kısmı
from base import Kapsam
from implementations import (
    UlasimYoneticisi,
    Scooter,
    Bisiklet,
    Otobus,
    Shuttle,
    MemoryTransportRepository,
    TransportService
)
from datetime import timedelta

print("------------------------------------------- Test Ortamı Başlıyor ---------------------------------------\n")

# Yönetici ve repo oluşturuluyor

yonetici = UlasimYoneticisi()
repo = MemoryTransportRepository()
service = TransportService(repo, yonetici)

# Araçları oluşturma
scooter1 = Scooter(1, "A Kapısı", "B Kapısı", "Boşta", ["A","B"], True, 80, 2)
scooter2 = Scooter(2, "Yurtlar", "Kütüphane", "Boşta", ["Yurt","Merkez","Kütüphane"], True, 40, 2)

bisiklet1 = Bisiklet(3, "Spor Salonu", "Mühendislik", "Boşta", ["Spor","Yemekhane","Mühendislik"], False, 0)
bisiklet2 = Bisiklet(4, "Fen Fakültesi", "Merkez", "Boşta", ["Fen","Merkez"], True, 60)

otobus1 = Otobus(5, 40, "Ana Giriş", "Kampüs İçi", "Boşta", ["Giriş","Merkez","Yurtlar"], "K1", Kapsam.kampus_ici)
otobus2 = Otobus(6, 50, "Kampüs", "Şehir Merkezi", "Boşta", ["Kampüs","AVM","Merkez"], "D2", Kapsam.kampus_disi)

shuttle1 = Shuttle(7, 20, "Kampüs", "Şehir Merkezi", "Boşta", ["Kampüs","AVM","Merkez"], "S1", Kapsam.kampus_disi)
shuttle2 =Shuttle(5,15,"kampüs","Hastane","Boşta",["kampüs","meydan","hastane"],"S2",Kapsam.kampus_disi)

# Araçları repo ve yöneticiye ekleme

for arac in [scooter1, bisiklet1, otobus1, shuttle1]:
    yonetici.arac_ekle(arac)
    repo.kaydet(arac.arac_id, arac)


print("-----------------------------------Sefer ve kullanım testleri yapılıyor--------------------------------")

# Scooter testi

try:
    service.sefer_baslat(sefer_id=101, arac_id=1)
    scooter1.sure_ekle(20)
    print(f"Scooter ücreti (20 dk): {scooter1.ucret_hesapla()}")
    yonetici.sefer_bitir(1)
except ValueError as e:
    print("Hata:", e)

# Bisiklet testi

try:
    service.sefer_baslat(sefer_id=102, arac_id=2)
    bisiklet1.sure_ekle(15)
    print(f"Bisiklet ücreti (15 dk): {bisiklet1.ucret_hesapla()}")
    yonetici.sefer_bitir(2)
except ValueError as e:
    print("Hata:", e)

# Otobüs testi

try:
    service.sefer_baslat(sefer_id=103, arac_id=3)
    otobus1.yolcu_ekle(25)
    print(f"Otobüs aktif yolcu: {otobus1.aktif_yolcu}, boş kapasite: {otobus1.bos_kapasite()}")
    yonetici.sefer_bitir(3)
except ValueError as e:
    print("Hata:", e)

# Shuttle testi ve rezervasyon

try:
    service.sefer_baslat(sefer_id=104, arac_id=4)
    shuttle1.rezervasyon_yap("Ahmet", 5)
    shuttle1.rezervasyon_yap("Ayşe", 3)
    print(f"Shuttle rezervasyon sayısı: {len(shuttle1.rezervasyonlar)}")
    yonetici.sefer_bitir(4)
except ValueError as e:
    print("Hata:", e)

# Hata Kontrolü

print("\nHata kontrolü: ID yanlış girildiğinde tekrar seçiliyor\n")
invalid_id = 999
while True:
    try:
        secilen = yonetici.arac_bul(invalid_id)
        break
    except ValueError:
        print(f"ID {invalid_id} bulunamadı, lütfen tekrar seçin.")
        invalid_id = 1  # Test için geçerli ID'yi seçiyoruz
print(f"Seçilen araç: {secilen.bilgi_ver()}")

# Repository Testleri

print("\nRepository testleri...\n")
# Listele

print("Repo listele:", repo.listele())

# ID ile bul

print("ID 1 ile bul:", repo.id_ile_bul(1))

# Filtrele

filtre = repo.filtrele(durum="Boşta")
print("Durumu Boşta olan araçlar:", filtre)

# Kaydet ve sil

yeni_bisiklet = Bisiklet(5, "Yeni Başlangıç", "Yeni Hedef", "Boşta", ["A","B"], False, 0)
repo.kaydet(5, yeni_bisiklet)
print("Yeni bisiklet eklendi:", repo.id_ile_bul(5))
repo.sil(5)
print("Silindikten sonra:", repo.id_ile_bul(5))

# Rapor Testleri

print("\nSefer geçmişi testleri...")
yonetici.sefer_gecmisi.extend([
    {"tip": "Scooter", "ucret": scooter1.ucret_hesapla()},
    {"tip": "Bisiklet", "ucret": bisiklet1.ucret_hesapla()},
    {"tip": "Otobüs", "ucret": otobus1.ucret_hesapla()},
    {"tip": "Shuttle", "ucret": shuttle1.ucret_hesapla()}
])

print("Toplam gelir:", yonetici.toplam_gelir())
print("En çok kullanılan araç tipi:", yonetici.en_cok_kullanilan_tip())
print("Araç sayısı raporu:", yonetici.arac_sayisi_raporu())
print("Boşta olan araçlar:", yonetici.duruma_gore_listele("Boşta"))
print("Tüm araçlar:", yonetici.tum_araclari_listele())

# Detaylı Testler

for arac in yonetici.araclar:

    print(f"Araç ID: {arac.arac_id}, Tip: {arac.bilgi_ver()['tip']}")
    print(f"Doluluk oranı: {arac.doluluk_orani()*100:.1f}%")
    print(f"Müsait mi?: {'Evet' if arac.musait_mi() else 'Hayır'}")
    print(f"Konum: {arac.mevcut_konum}")
    print(f"Zaman Bilgisi: {arac.zaman_bilgisi()}")
    print(f"Sıfırlama öncesi durum: {arac.durum}")

    arac.sifirla()
    print(f"Sıfırlama sonrası durum: {arac.durum}")
    print("-"*60)


