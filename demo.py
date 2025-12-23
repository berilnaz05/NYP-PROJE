#örnek kullanıcı girdisinin alındığı kısım 
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
import time

print("------------- Ulaşım Sistemi Başlatılıyor -------------\n")

# Yönetici ve repository oluşturuluyor

yonetici = UlasimYoneticisi()
repo = MemoryTransportRepository()
service = TransportService(repo, yonetici)

print("Yönetici ve Repository oluşturuldu.\n")

# ------------------- Araç Oluşturma -------------------

scooter1 = Scooter(1, "A Kapısı", "B Kapısı", "Boşta", ["A","B"], True, 80, 2)
scooter2 = Scooter(2, "Yurtlar", "Kütüphane", "Boşta", ["Yurt","Merkez","Kütüphane"], True, 40, 2)

bisiklet1 = Bisiklet(3, "Spor Salonu", "Mühendislik", "Boşta", ["Spor","Yemekhane","Mühendislik"], False, 0)
bisiklet2 = Bisiklet(4, "Fen Fakültesi", "Merkez", "Boşta", ["Fen","Merkez"], True, 60)

otobus1 = Otobus(5, 40, "Ana Giriş", "Kampüs İçi", "Boşta", ["Giriş","Merkez","Yurtlar"], "K1", Kapsam.kampus_ici)
otobus2 = Otobus(6, 50, "Kampüs", "Şehir Merkezi", "Boşta", ["Kampüs","AVM","Merkez"], "D2", Kapsam.kampus_disi)

shuttle1 = Shuttle(7, 20, "Kampüs", "Şehir Merkezi", "Boşta", ["Kampüs","AVM","Merkez"], "S1", Kapsam.kampus_disi)

# Araçları hem repo hem yöneticiye ekleme
for arac in [scooter1, scooter2, bisiklet1, bisiklet2, otobus1, otobus2, shuttle1]:
    yonetici.arac_ekle(arac)
    repo.kaydet(arac.arac_id, arac)

print("Mevcut araçlar sisteme eklendi.\n\n")

# Araç Listeleme

print("---------------------------------- Tüm Araçlar ------------------------------------")
for arac in yonetici.tum_araclari_listele():
    print(arac)
print("-" * 50)

# Kullanıcıdan ıd seçimi

while True:
    try:
        secim_id = int(input("Durumunu görmek istediğiniz aracın ID'sini girin: "))
        secilen_arac = yonetici.arac_bul(secim_id)
        if secilen_arac is None:
            print("Girilen ID sistemde yok. Tekrar deneyin.")
            continue
        break
    except ValueError:
        print("Hatalı ID, tekrar deneyin.")

print(f"\n\nSeçilen Araç Bilgisi: {secilen_arac.bilgi_ver()}")

# Seilen her aracca göre davranış

if isinstance(secilen_arac, (Scooter, Bisiklet)):
    while True:
        try:
            sure = int(input(f"{secilen_arac.bilgi_ver()['tip']} kullanım süresi (dakika) girin: "))
            break
        except ValueError:
            print("Lütfen geçerli bir sayı girin!")
    secilen_arac.sure_ekle(sure)
    service.sefer_baslat(sefer_id=100+secilen_arac.arac_id, arac_id=secilen_arac.arac_id)
    print(f"{secilen_arac.bilgi_ver()['tip']} ücreti: {secilen_arac.ucret_hesapla()}")
    yonetici.sefer_bitir(secilen_arac.arac_id)

elif isinstance(secilen_arac, Otobus):
    service.sefer_baslat(sefer_id=200+secilen_arac.arac_id, arac_id=secilen_arac.arac_id)
    print("Otobüs hareket ediyor...")
    while True:
        try:
            yolcu_sayisi = int(input("Otobüse binecek yolcu sayısını girin: "))
            break
        except ValueError:
            print("Lütfen geçerli bir sayı girin!")
    if secilen_arac.yolcu_ekle(yolcu_sayisi):
        print("Yolcular eklendi.")
    else:
        print("Kapasite yetersiz!")
    print("Güncel durumu:", secilen_arac.genel_durum())
    yonetici.sefer_bitir(secilen_arac.arac_id)

elif isinstance(secilen_arac, Shuttle):
    isim = input("Rezervasyon yapacak kişinin adı: ")
    while True:
        try:
            kisi_sayisi = int(input("Kaç kişi rezervasyon yapacak? "))
            break
        except ValueError:
            print("Lütfen geçerli bir sayı girin!")
    if secilen_arac.rezervasyon_yap(isim, kisi_sayisi):
        print("Rezervasyon başarılı!")
    else:
        print("Yeterli kapasite yok.")
    print("Rezervasyon sonrası durumu:", secilen_arac.bilgi_ver())
    iptal = input("Rezervasyonu iptal etmek ister misiniz? (E/H) ")
    if iptal.upper() == "E":
        if secilen_arac.rezervasyon_iptal(isim):
            print("Rezervasyon iptal edildi.")
        else:
            print("Rezervasyon bulunamadı.")

# Aracın kapasite ve durum bilgisini verir

print("\n-------------------------- Araç Kapasite ve Durum Bilgisi -------------------------------")
for arac in yonetici.araclar:
    bilgi = arac.bilgi_ver()
    print(f"ID: {arac.arac_id} | Tip: {bilgi['tip']} | Durum: {bilgi['durum']} | "
          f"Aktif Yolcu: {bilgi.get('aktif_yolcu', 0)} | Boş Kapasite: {bilgi.get('bos_kapasite', arac.kapasite)} | "
          f"Rezervasyonlar: {bilgi.get('rezervasyonlar', {})} | "
          f"Müsait mi?: {'Evet' if arac.musait_mi() else 'Hayır'} | "
          f"Konum: {arac.mevcut_konum} | "
          f"Zaman Bilgisi: {arac.zaman_bilgisi()}")

print("\n----------------------------- Sefer Geçmişi ----------------------------------")
for kayit in yonetici.sefer_gecmisi:
    print(kayit)

# boşta olan araç bilgisini verir
print("\n---------------------------- Boşta Olan Araçlar -------------------------------")
for bilgi in yonetici.duruma_gore_listele("Boşta"):
    print(bilgi)

print("\n \nSistem işlemleri tamamlandı.")
