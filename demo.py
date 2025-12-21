from implementations import UlasimYoneticisi
from implementations import (
    Scooter,
    Bisiklet,
    Shuttle,
    Otobus,
    UlasimYoneticisi,
    MemoryTransportRepository,
    TransportService
)
from base import Kapsam
from datetime import timedelta
import time

print("-----------------sistem başlatılıyor------------")

#yönetici oluşturuldu

yonetici = UlasimYoneticisi()
repo = MemoryTransportRepository()
service = TransportService(repo, yonetici)
print("Yönetici ve Repository oluşturuldu\n")

print("-------------araçlar oluşturuldu-----------")

# Aaç nesneleri oluşturulur

scooter1 = Scooter(
    arac_id=1,
    kalkis="A Kapısı",
    bitis="B Kapısı",
    durum="Boşta",
    guzergah=["A", "B"],
    elektrikli=True,
    batarya=80,
    dakika_ucreti=2
)

scooter2 = Scooter(
    arac_id=2,
    kalkis="Yurtlar",
    bitis="Kütüphane",
    durum="Boşta",
    guzergah=["Yurt", "Merkez", "Kütüphane"],
    elektrikli=True,
    batarya=40,
    dakika_ucreti=2
)

bisiklet1 = Bisiklet(
    arac_id=3,
    kalkis="Spor Salonu",
    bitis="Mühendislik",
    durum="Boşta",
    guzergah=["Spor", "Yemekhane", "Mühendislik"],
    elektrikli=False,
    batarya=0,
)

bisiklet2 = Bisiklet(
    arac_id=4,
    kalkis="Fen Fakültesi",
    bitis="Merkez",
    durum="Boşta",
    guzergah=["Fen", "Merkez"],
    elektrikli=True,
    batarya=60,
)
otobus1 = Otobus(
    arac_id=5,
    kapasite=40,
    kalkis="Ana Giriş",
    bitis="Kampüs İçi",
    durum="Boşta",
    guzergah=["Giriş", "Merkez", "Yurtlar"],
    hat_no="K1",
    kapsam=Kapsam.kampus_ici
)

otobus2 = Otobus(
    arac_id=6,
    kapasite=50,
    kalkis="Kampüs",
    bitis="Şehir Merkezi",
    durum="Boşta",
    guzergah=["Kampüs", "AVM", "Merkez"],
    hat_no="D2",
    kapsam=Kapsam.kampus_disi
)
shuttle1 = Shuttle(
    arac_id=7,
    kapasite=20,
    kalkis="Kampüs",
    bitis="Şehir Merkezi",
    durum="Boşta",
    guzergah=["Kampüs", "AVM", "Merkez"],
    hat_no="S1",
    kapsam=Kapsam.kampus_disi
)

print("\n----------------- mevcut araçlar ------------------------------------")
for arac in [scooter1, scooter2, bisiklet1, bisiklet2, otobus1, otobus2,shuttle1]:
    #araçlar repo ve yöneticide saklanıyor
    repo.data[arac.arac_id] = arac
    #yöneticiye ekler
    yonetici.araclar.append(arac)
    repo.data[shuttle1.arac_id] = shuttle1
    yonetici.araclar.append(shuttle1)

    # araç bilgilerini listeleme ve  ve seçim
        
    for arac in yonetici.araclar:
      if isinstance(arac, Otobus):
        print("Otobüs ID:", arac.arac_id)
        print("Durum:", arac.durum)
        print("Toplam kapasite:", arac.kapasite)
        print("Aktif yolcu:", arac.aktif_yolcu)
        print("Boş kapasite:", arac.bos_kapasite())
        print("-" * 30)
        
    for arac in yonetici.araclar:
     if isinstance(arac, Bisiklet):
        print("Bisiklet ID:", arac.arac_id)
        print("Durum:", arac.durum)
        print("Elektrikli mi:", arac.elektrikli)
        print("Kullanılan süre (dk):", arac.kullanilan_dakika)
        print("Ücret:", arac.ucret_hesapla())
        print("-" * 30)

    for arac in yonetici.araclar:
        if isinstance(arac,Scooter):
            print("scooter ID:",arac.arac_id)
            print("Durum:",arac.durum)
            print("kullanıln Süre(dk):",arac.kullanilan_dakika)
            print("ücret:",arac.ucret_hesapla())
            print("-"*20)
    for arac in yonetici.araclar:
        if isinstance(arac,Shuttle):
            print("Shuttle  ID:",arac.arac_id)
            print("Durum:",arac.durum)
            print("ücret:",arac.ucret_hesapla)
            print("Boş Kapasite:",arac.bos_kapasite)
            print("Aktif Yolcu:",arac.aktif_yolcu)
            
    
for arac in yonetici.araclar:
    bilgi = arac.bilgi_ver()
    print(
        f"ID: {bilgi['arac_id']} | "
        f"Tip: {bilgi['tip']} | "
        f"Durum: {bilgi['durum']}"
    )
    secim_id = int(input("\nSeçmek istediğiniz aracın ID'sini girin: "))
    secilen_arac=yonetici.arac_bul(secim_id)
    print("seçilen araç:",secilen_arac.bilgi_ver())
    
    #araç tiplerine göre detaylar

            
print("Shuttle rezervasyonu yapmak için:")
isim = input("Adınızı girin: ")
kisi_sayisi = int(input("Kaç kişi?: "))

if shuttle1.rezervasyon_yap(isim, kisi_sayisi):
    print("Rezervasyon başarılı!")
else:
    print("Yeterli kapasite yok!")

# Rezervasyon iptali örneği
iptal = input("Rezervasyon iptal etmek ister misiniz? (E/H) ")
if iptal.upper() == "E":
    if shuttle1.rezervasyon_iptal(isim):
        print("Rezervasyon iptal edildi.")
    else:
        print("Rezervasyon bulunamadı.")
            
print("\n--- Araç Kapasite ve Müsaitlik Durumu ---")

for arac in yonetici.araclar:
    print(f"""
Araç Tipi     : {arac.bilgi_ver()['tip']}
Araç ID       : {arac.arac_id}
Durum         : {arac.durum}
Kapasite      : {arac.kapasite}
Aktif Yolcu   : {arac.aktif_yolcu}
Boş Kapasite  : {arac.bos_kapasite()}
Müsait mi?    : {"Evet" if arac.musait_mi() else "Hayır"}
""")

print("Araç nesneleri oluşturuldu\n")

#repo ya kaydetme

print("araclar repository e kaydedildi")

for arac in [scooter1, scooter2, bisiklet1, bisiklet2, otobus1, otobus2]:
    repo.data[arac.arac_id] = arac
    yonetici.araclar.append(arac)
    print(f"Araç eklendi  ID: {arac.arac_id}, Tip: {arac.bilgi_ver()['tip']}")

print("\nToplam araç sayısı:", len(repo.listele()))
print("\nBoşta olan araçlar:")
for bilgi in yonetici.duruma_gore_listele("Boşta"):
    print(bilgi)

print("--------tüm araçlar------------")
for bilgi in yonetici.tum_araclari_listele():
    print(bilgi)

#scoter seferi
print("----------------scooter seferi-------------")
sure = int(input("Scooter için kullanım süresi (dakika): "))
scooter1.sure_ekle(sure)

service.sefer_baslat(sefer_id=1, arac_id=1)
sure = int(input("Scooter için kullanım süresi (dakika): "))
scooter1.sure_ekle(sure)

print("Scooter ücreti:", scooter1.ucret_hesapla())

# ücret hesaplama
for dakika in range(5, 1000):
    scooter1.sure_ekle(5)
    print(f"{dakika}. dakika - Ücret:", scooter1.ucret_hesapla())
    time.sleep(0.1)

yonetici.sefer_bitir(1)
print("Scooter seferi tamamlandı\n")

#bisiklet bilgileri

print("----------------bisiklet seferi--------------")

service.sefer_baslat(sefer_id=2, arac_id=3)
sure = int(input("Bisiklet için kullanım süresi (dakika): "))
bisiklet1.sure_ekle(sure)
print("Bisiklet ücreti:", bisiklet1.ucret_hesapla())

for dakika in range(10, 61, 10):
    bisiklet1.sure_ekle(10)
    print(f"{dakika}. dakika - Ücret:", bisiklet1.ucret_hesapla())
    time.sleep(0.1)

yonetici.sefer_bitir(3)
print("Bisiklet seferi tamamlandı\n")

#otobüs  bilgileri

print("----------------otobüs sefer detayları-----------")

yonetici.sefer_baslat(5)
otobus1.hareket_et()

service.sefer_baslat(sefer_id=3, arac_id=5)

#raporlama
print("\nOtobüs kapasite bilgisi:")
print("Toplam kapasite:", otobus1.kapasite)
print("Boş kapasite:", otobus1.bos_kapasite())

yolcu_sayisi = int(input("Otobüse binecek yolcu sayısı: "))


if otobus1.yolcu_ekle(yolcu_sayisi):
    print("Yolcular eklendi.")
else:
    print("Kapasite yetersiz! Yolcu eklenemedi.")

print("Güncel aktif yolcu:", otobus1.aktif_yolcu)
print("Kalan boş kapasite:", otobus1.bos_kapasite())
for yolcu in range(5, 31, 5):
    otobus1.yolcu_ekle(5)
    print(f"Aktif yolcu: {otobus1.aktif_yolcu} / {otobus1.kapasite}")
    time.sleep(0.1)

yonetici.sefer_bitir(5)
print("Otobüs seferi tamamlandı\n")

#sefer geçiişi oluşturulu
print("------------sefer geçmişi kaydı--------------")

yonetici.sefer_gecmisi.extend([
    {"tip": "Scooter", "ucret": 60},
    {"tip": "Bisiklet", "ucret": 30},
    {"tip": "Otobüs", "ucret": 10},
    {"tip": "Otobüs", "ucret": 20},
])

for kayit in yonetici.sefer_gecmisi:
    print(kayit)
    
#Rapor oluşturuldu
print("-----------Raporlr---------------")
print("Toplam gelir:", yonetici.toplam_gelir())
print("En çok kullanılan araç tipi:", yonetici.en_cok_kullanilan_tip())
print("Araç sayısı raporu:", yonetici.arac_sayisi_raporu())

print("BOŞTA OLAN ARAÇLAR")

for bilgi in yonetici.duruma_gore_listele("Boşta"):
    print(bilgi)
    
for bilgi in yonetici.tum_araclari_listele():
    print(bilgi)
    
print("En çok kullanılan araç tipi:", yonetici.en_cok_kullanilan_tip())
print("Araç sayısı raporu:", yonetici.arac_sayisi_raporu())


