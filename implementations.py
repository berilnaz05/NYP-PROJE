from datetime import timedelta
from base import UlasimAraci, IRepository, TransportRepository, Kapsam

#sistemdei tüm araçları yönetir
class UlasimYoneticisi:
    def __init__(self):
        self.araclar = []
        self.sefer_gecmisi = []

    def arac_ekle(self, arac):
        if not isinstance(arac, UlasimAraci):
            raise TypeError("Sadece UlasimAraci eklenebilir")
        self.araclar.append(arac)

    def arac_bul(self, arac_id):
        for arac in self.araclar:
            if arac.arac_id == arac_id:
                return arac
        raise ValueError("Araç bulunamadı")

    def sefer_baslat(self, arac_id):
        arac = self.arac_bul(arac_id)
        if arac.aktif_mi():
            raise ValueError("Araç zaten aktif")
        arac.sefer_baslat()
        arac.hareket_et()

    def sefer_bitir(self, arac_id):
        arac = self.arac_bul(arac_id)
        arac.sefer_bitir()
    
    def tum_araclari_listele(self):
        return [arac.bilgi_ver() for arac in self.araclar  ] 

    def toplam_gelir(self):
        return sum(k["ucret"] for k in self.sefer_gecmisi)
    
    def en_cok_kullanilan_tip(self):
        if not self.sefer_gecmisi:
            return "Henüz sefer yok"

        sayac = {}

        for kayit in self.sefer_gecmisi:
         tip = kayit["tip"]
         sayac[tip] = sayac.get(tip, 0) + 1

        return max(sayac, key=sayac.get)
    def arac_sayisi_raporu(self):
     rapor = {}

     for arac in self.araclar:
        tip = arac.bilgi_ver()["tip"]
        rapor[tip] = rapor.get(tip, 0) + 1

        return rapor
    def duruma_gore_listele(self, durum):
      return [
        arac.bilgi_ver()
        for arac in self.araclar
        if arac.durum == durum
    ]
     #scooter sınıfı 
class Scooter(UlasimAraci):
    def __init__(self, arac_id, kalkis, bitis, durum, guzergah,elektrikli, batarya, dakika_ucreti):

        super().__init__(arac_id=arac_id,kapasite=1,kalkis=kalkis,bitis=bitis,durum=durum,guzergah=guzergah,kapsam=Kapsam.kampus_ici)
        self.elektrikli = elektrikli
        self.batarya = batarya
        self.dakika_ucreti = dakika_ucreti
        self.kullanilan_dakika = 0

    def sefer_bilgisi(self):
        return "Scooter kullanımda"

    def hareket_et(self):
        print(f"Scooter {self.arac_id} hareket ediyor")

    def sefer_baslat(self):
        self.durum = "Kullanımda"

    def sefer_bitir(self):
        self.sifirla()
        self.kullanilan_dakika = 0

    def sure_ekle(self, dakika):
        self.kullanilan_dakika += dakika

    def ucret_hesapla(self):
        return self.kullanilan_dakika * self.dakika_ucreti

    def tahmini_sure(self):
        return timedelta(minutes=20)

    def bilgi_ver(self):
        return {
            "tip": "Scooter",
            "arac_id": self.arac_id,
            "durum": self.durum,
            "ucret": self.ucret_hesapla()
        }
# bisilet sınıfı

class Bisiklet(UlasimAraci):
    def __init__(self, arac_id, kalkis, bitis, durum, guzergah,elektrikli, batarya):

        super().__init__(arac_id=arac_id,kapasite=1,kalkis=kalkis,bitis=bitis,durum=durum,guzergah=guzergah,kapsam=Kapsam.kampus_ici
        )
        self.elektrikli = elektrikli
        self.batarya = batarya
        self.kullanilan_dakika = 0

    def sefer_bilgisi(self):
        return "Bisiklet kullanımda"

    def hareket_et(self):
        print(f"Bisiklet {self.arac_id} hareket ediyor")

    def sefer_baslat(self):
        self.durum = "Kullanımda"

    def sefer_bitir(self):
        self.sifirla()
        self.kullanilan_dakika = 0

    def sure_ekle(self, dakika):
        self.kullanilan_dakika += dakika

    def ucret_hesapla(self):
        return self.kullanilan_dakika * (1.5 if self.elektrikli else 0.5)

    def tahmini_sure(self):
        return timedelta(minutes=30)
#araç hakkında ilgi verir
    def bilgi_ver(self):
        return {
            "tip": "Bisiklet",
            "arac_id": self.arac_id,
            "durum": self.durum,
            "ucret": self.ucret_hesapla()
        }

# otobüs sınıfı

class Otobus(UlasimAraci):
    def __init__(self, arac_id, kapasite, kalkis, bitis,durum, guzergah, hat_no, kapsam):
        super().__init__(arac_id=arac_id,kapasite=kapasite,kalkis=kalkis,bitis=bitis,durum=durum,guzergah=guzergah,kapsam=kapsam)
        self.hat_no = hat_no
        self.ucret_kampus_ici = 10
        self.ucret_kampus_disi = 20

    def sefer_bilgisi(self):
        return f"Otobüs {self.hat_no} seferde"

    def hareket_et(self):
        print(f"Otobüs {self.arac_id} güzergah:")
        for durak in self.guzergah:
            print("-", durak)

    def sefer_baslat(self):
        self.durum = "Seferde"

    def sefer_bitir(self):
        self.sifirla()

    def ucret_hesapla(self):
        return (
            self.ucret_kampus_ici
            if self.kapsam == Kapsam.kampus_ici
            else self.ucret_kampus_disi
        )

    def tahmini_sure(self):
        return timedelta(minutes=len(self.guzergah) * 5)

# otobüs bilgisi verir
    def bilgi_ver(self):
        return {
            "tip": "Otobüs",
            "arac_id": self.arac_id,
            "durum": self.durum,
            "ucret": self.ucret_hesapla()
        }

class Shuttle(UlasimAraci):
    def __init__(self, arac_id, kapasite, kalkis, bitis, durum, guzergah, hat_no, kapsam):
        super().__init__(
            arac_id=arac_id,
            kapasite=kapasite,
            kalkis=kalkis,
            bitis=bitis,
            durum=durum,
            guzergah=guzergah,
            kapsam=kapsam
        )
        self.hat_no = hat_no
        self.rezervasyonlar = []  # Rezervasyonları tutmak için liste

    # Soyut metodları implement et
    def sefer_bilgisi(self):
        return f"Shuttle {self.hat_no} seferde"

    def hareket_et(self):
        print(f"Shuttle {self.arac_id} güzergah: {self.guzergah}")

    def sefer_baslat(self):
        self.durum = "Seferde"

    def sefer_bitir(self):
        self.sifirla()
        self.rezervasyonlar.clear()  # sefer bitince rezervasyonları temizle

    def ucret_hesapla(self):
        return 15  # sabit fiyat örneği

    def tahmini_sure(self):
        return timedelta(minutes=len(self.guzergah) * 5)

    def bilgi_ver(self):
        return {
            "tip": "Shuttle",
            "arac_id": self.arac_id,
            "durum": self.durum,
            "ucret": self.ucret_hesapla(),
            "rezervasyon_sayisi": len(self.rezervasyonlar)
        }

    #  Shuttle’a özel 
    def rezervasyon_yap(self, isim, kisi_sayisi=1):
        if self.bos_kapasite() >= kisi_sayisi:
            self.rezervasyonlar.append({"isim": isim, "kisi_sayisi": kisi_sayisi})
            self.aktif_yolcu += kisi_sayisi
            return True
        return False

    def rezervasyon_iptal(self, isim):
        for r in self.rezervasyonlar:
            if r["isim"] == isim:
                self.aktif_yolcu -= r["kisi_sayisi"]
                self.rezervasyonlar.remove(r)
                return True
        return False

# veriyi ramda tutar
class MemoryTransportRepository(IRepository):
    def __init__(self):
        self.data = {}

    def listele(self):
        return list(self.data.values())

    def id_ile_bul(self, item_id):
        return self.data.get(item_id)

    def filtrele(self, **kwargs):
        return [
            item for item in self.data.values()
            if all(getattr(item, k) == v for k, v in kwargs.items())
        ]

    def kaydet(self, item_id, item):
        self.data[item_id] = item

    def sil(self, item_id):
        self.data.pop(item_id, None)
        
#servis yapısı
class TransportService:
    def __init__(self, repo: TransportRepository, yonetici: UlasimYoneticisi):
        self.repo = repo
        self.yonetici = yonetici

    def sefer_baslat(self, sefer_id, arac_id):
        arac = self.repo.id_ile_bul(arac_id)
        if not arac:
            raise ValueError("Araç bulunamadı")

        arac.sefer_baslat()
        arac.hareket_et()

        self.yonetici.sefer_gecmisi.append({
            "sefer_id": sefer_id,
            "tip": arac.bilgi_ver()["tip"],
            "ucret": arac.ucret_hesapla()
        })