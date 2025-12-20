from implementations.otobus import Otobus
from implementations.bisiklet import Bisiklet
from implementations.scooter import Scooter

def menu():
    print("\nAKILLI KAMPÜS ULAŞIM SİSTEMİ")
    print("---------------------------------------------------------------------")
    print("1 - Otobüs oluştur")
    print("2 - Bisiklet oluştur")
    print("3 - Scooter oluştur")
    print("0 - Çıkış")

araclar = []

while True:
    menu()
    secim = input("Seçiminiz: ")

    if secim == "1":
        otobus1 = Otobus(
            arac_id=400,
            kapasite=75,
            kalkis="yurtlar",
            bitis="kutuphane",
            hat_no="Hat No:11A",
            guzergah=["yurtlar", "Hastane", "mühendislik","rektörlük","kütüphane","fen fakültesi"],
            durum="beklemede",
            kapsam="Kampüs içi"
        )

        otobus2 = Otobus(
            arac_id=404,
            kapasite=100,
            kalkis="yurtlar",
            bitis="rektörlük",
            hat_no="Hat No:12B",
            guzergah=["yurtlar","yemekhane","sağlık fakültesi","rektörlük","mühendislik","murat evler","anadolu","fatih","kadeş meydanı","anitta","hastane"],
            durum="Beklemede",
            kapsam="Kampus Dışı"
        )

        otobusler = [otobus1, otobus2]

        print("Otobüs seçenekleri:")
        for i, otobus in enumerate(otobusler, start=1):
            print(f"{i}. {otobus.hat_no}, Kapasite: {otobus.kapasite}")

        secim_otobus = int(input("Seçmek istediğiniz otobüsü yazınız: "))
        secili_otobus = otobusler[secim_otobus - 1]

        secili_otobus.sefer_bilgisi()
        tur = input("Ücret için tur seçin(kampus içi / kampus dışı): ").strip().lower()
        print("Seçilen tur ücreti:", secili_otobus.ucret_hesapla(tur))

        secili_otobus.sefer_baslat()
        araclar.extend([otobus1, otobus2])
        print("Otobüsler eklendi.")

    elif secim == "2":
        bisikletler = []

        bisiklet1 = Bisiklet(
            arac_id=1,
            kalkis="yurtlar",
            bitis="",
            durum="boşta",
            guzergah=["yurtlar", "Hastane", "mühendislik","rektörlük","kütüphane","fen fakültesi"],
            kapsam="kampus içi",
            elektrikli="elektrikli",
            batarya="%100",
            km_ucreti=0.8
        )

        bisiklet2 = Bisiklet(
            arac_id=2,
            kalkis="yurtlar",
            bitis="",
            durum="Boşta",
            guzergah=["yurtlar","yemekhane","sağlık fakültesi","rektörlük","mühendislik","murat evler","anadolu","fatih","kadeş meydanı","anitta","hastane"],
            kapsam="kampüsdışı",
            elektrikli="elektrikli",
            batarya="%100",
            km_ucreti=2
        )

        bisikletler.extend([bisiklet1, bisiklet2])

        print("Bisiklet seçenekleri:")
        for i, bisiklet in enumerate(bisikletler, start=1):
            print(f"{i}. Bisiklet {bisiklet.arac_id}")

        secim_bisiklet =int(input("Seçmek istediğiniz bisikleti giriniz: "))
        secili_bisiklet = bisikletler[secim_bisiklet - 1]

        dakika = int(input("Kullanım süresi (dk): "))
        secili_bisiklet.sefer_baslat()
        secili_bisiklet.sure_ekle(dakika)
        araclar.append(secili_bisiklet)
        print("Bisiklet seçildi.")

    elif secim == "3":
        scooterler=[]
        
        scooter1 = Scooter(
            arac_id=1,
            kalkis="yurtlar",
            bitis="",
            durum="Boşta",
            guzergah=["yurtlar", "Hastane", "mühendislik","rektörlük","kütüphane","fen fakültesi"],
            elektrikli="evet",
            batarya="%100",
            dakika_ucreti=5,
            kapsam="kampüs içi"
        )

        scooter2 = Scooter(
            arac_id=2,
            kalkis="yurtlar",
            bitis="",
            durum="Boşta",
            guzergah=["yurtlar", "Hastane", "mühendislik","rektörlük","kütüphane","fen fakültesi"],
            elektrikli="evet",
            batarya="%100",
            dakika_ucreti=5,
            kapsam="kampüs içi"
        )

        scooterler.extend([scooter1, scooter2])

        print("Scooter seçenekleri:")
        for s, scooter in enumerate(scooterler, start=1):
            print(f"{s}. Scooter {scooter.arac_id}")

        secim_scooter = int(input("Seçmek istediğiniz scooter'ı giriniz: "))
        secili_scooter = scooterler[secim_scooter - 1]

        dakika = int(input("Kullanım süresi (dk): "))
        secili_scooter.sefer_baslat()
        secili_scooter.sure_ekle(dakika)
        araclar.append(secili_scooter)
        print("Scooter seçildi.")

    elif secim == "0":
        print("Çıkış yapıldı")
        break

    else:
        print("Geçersiz seçim")


