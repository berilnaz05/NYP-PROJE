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

# Yönetici ve repository oluşturuluyor

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
shuttle2 =Shuttle(5,15,"kampüs","Hastane","Boşta",["kampüs","meydan","hastane"],"S2",Kapsam.kampus_disi)

# Araçları repo ve yöneticiye ekleme

for arac in [scooter1, scooter2, bisiklet1, bisiklet2, otobus1, otobus2, shuttle1,shuttle2]:
    yonetici.arac_ekle(arac)
    repo.kaydet(arac.arac_id, arac)

#Örnek Seferler ve Kullanım 

scooter1.sure_ekle(25)
service.sefer_baslat(sefer_id=101, arac_id=scooter1.arac_id)
yonetici.sefer_bitir(scooter1.arac_id)

bisiklet1.sure_ekle(15)
service.sefer_baslat(sefer_id=102, arac_id=bisiklet1.arac_id)
yonetici.sefer_bitir(bisiklet1.arac_id)


bisiklet2.sure_ekle(45)
service.sefer_baslat(sefer_id=10, arac_id=bisiklet2.arac_id)
yonetici.sefer_bitir(bisiklet2.arac_id)

otobus1.yolcu_ekle(15)
service.sefer_baslat(sefer_id=103, arac_id=otobus1.arac_id)
yonetici.sefer_bitir(otobus1.arac_id)

otobus2.yolcu_ekle(20)
service.sefer_baslat(sefer_id=10,arac_id=otobus2.arac_id)
yonetici.sefer_bitir(otobus2.arac_id)

scooter2.sure_ekle(35)
service.sefer_baslat(sefer_id=56,arac_id=scooter2.arac_id)
yonetici.sefer_bitir(scooter2.arac_id)

shuttle2.rezervasyon_yap("Ali",1)
shuttle2.rezervasyon_yap("veli",1)
service.sefer_baslat(sefer_id=5,arac_id=shuttle2.arac_id)
yonetici.sefer_bitir(shuttle2.arac_id)

shuttle1.rezervasyon_yap("Ahmet", 3)
shuttle1.rezervasyon_yap("Ayşe", 2)
service.sefer_baslat(sefer_id=104, arac_id=shuttle1.arac_id)
yonetici.sefer_bitir(shuttle1.arac_id)

# Sefer geçmişi ekleme 

yonetici.sefer_gecmisi.extend([
    {"tip": "Scooter", "ucret": scooter1.ucret_hesapla()},
    {"tip": "Bisiklet", "ucret": bisiklet2.ucret_hesapla()},
    {"tip": "Otobüs", "ucret": otobus1.ucret_hesapla()},
    {"tip": "Shuttle", "ucret": shuttle1.ucret_hesapla()},
    {"tip": "Otobus", "ucret": otobus2.ucret_hesapla()},
    {"tip": "Bisiklet","ucret":bisiklet1.ucret_hesapla()},
    {"tip": "Scooter","ucret":scooter2.ucret_hesapla()},
    {"tip": "Shuttle", "ucret":shuttle2.ucret_hesapla()}

])

# Araç Raporları

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

print("\n\n------------------------------------Raporlama işlemi tamamlandı.---------------------------------------")
