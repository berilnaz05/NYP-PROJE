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

# Sefer ve Kullanım Testleri

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

print("\nDetaylı fonksiyon testleri...\n")
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

print("\ntestler tamamlandı")
