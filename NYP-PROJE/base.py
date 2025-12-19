from abc import ABC, abstractmethod
from datetime import datetime,timedelta
from base import UlasimAraci


class UlasimAraci(ABC):
    def __init__(self,arac_id,kapasite,kalkis,bitis,mevcut_konum,durum,guzergah):
        self.arac_id = arac_id
        self.kapasite = kapasite
        self.kalkis = kalkis
        self.bitis = bitis
        self.mevcut_konum = mevcut_konum
        self.durum = durum
        self.guzergah = guzergah

        self.olusturma_tarihi = datetime.now()
        self.guncelleme_tarihi = datetime.now()

        self.aktif_yolcu = 0
        self.sefer_sayisi = 0
      
class Otobus(UlasimAraci):

    def __init__(self, arac_id, kapasite, kalkis, bitis, mevcut_konum,durum, guzergah, hat_no, km_ucreti):
        super().__init__(arac_id, kapasite, kalkis, bitis, mevcut_konum, durum, guzergah)
        self.hat_no = hat_no
        self.km_ucreti = km_ucreti
        self.mesafe_km = 0

    def mesafe_ayarla(self, km):
        self.mesafe_km = km

    def sefer_bilgisi(self):
        print("Otobüs güzergahı:", " -> ".join(self.guzergah))

    def hareket_et(self):
        print("Otobüs hareket ediyor")

    def sefer_baslat(self):
        self.durum = "Seferde"
        self.sefer_arttir()

    def sefer_bitir(self):
        self.durum = "Boşta"
        self.sifirla()

    def ucret_hesapla(self):
        return self.km_ucreti * self.mesafe_km

    def tahmini_sure(self):
        return timedelta(minutes=self.mesafe_km * 2)

    def bilgi_ver(self):
        return {
            "tip": "Otobüs",
            "arac id": self.arac_id,
            "hat": self.hat_no,
            "durum": self.durum,
            "ucret": self.ucret_hesapla()
        }

class Bisiklet(UlasimAraci):

    def __init__(self, arac_id, mevcut_konum, elektrikli, batarya=100):
        super().__init__(arac_id, 1, "", "", mevcut_konum, "Boşta", [])
        self.elektrikli = elektrikli
        self.batarya = batarya
        self.kullanilan_dakika = 0

    def sefer_bilgisi(self):
        print("Bisiklet kullanımda")

    def hareket_et(self):
        print("Bisiklet hareket ediyor")

    def sefer_baslat(self):
        self.durum = "Kullanımda"
        self.sefer_arttir()

    def sefer_bitir(self):
        self.durum = "Boşta"
        self.kullanilan_dakika = 0

    def sure_ekle(self, dakika):
        self.kullanilan_dakika += dakika
        if self.elektrikli:
            self.batarya = max(0, self.batarya - dakika * 0.5)

    def ucret_hesapla(self):
        return self.kullanilan_dakika * (1.5 if self.elektrikli else 0.5)

    def tahmini_sure(self):
        return timedelta(minutes=30)

    def bilgi_ver(self):
        return {
            "tip": "Bisiklet",
            "arac id": self.id,
            "durum": self.durum,
            "batarya": self.batarya,
            "ucret": self.ucret_hesapla()
        }

class Scooter(UlasimAraci):

    def __init__(self, arac_id, mevcut_konum, hiz, dakika_ucreti):
        super().__init__(arac_id, 1, "", "", mevcut_konum, "Boşta", [])
        self.hiz = hiz
        self.dakika_ucreti = dakika_ucreti
        self.kullanilan_dakika = 0

    def sefer_bilgisi(self):
        print("Scooter kullanımda")

    def hareket_et(self):
        print("Scooter hareket ediyor")

    def sefer_baslat(self):
        self.durum = "Kullanımda"
        self.sefer_arttir()

    def sefer_bitir(self):
        self.durum = "Boşta"
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
            "id": self.id,
            "durum": self.durum,
            "ucret": self.ucret_hesapla()
        }
#soyut  metodlar
    @abstractmethod
    def sefer_bilgisi(self):
        pass

    @abstractmethod
    def hareket_et(self):
        pass

    @abstractmethod
    def sefer_baslat(self):
        pass

    @abstractmethod
    def sefer_bitir(self):
        pass

    @abstractmethod
    def bilgi_ver(self):
        pass

    @abstractmethod
    def ucret_hesapla(self):
        pass

    @abstractmethod
    def tahmini_sure(self):
        pass

   #ortak kullanılacak alan

    def konum_guncelle(self, yeni_konum):
        self.mevcut_konum = yeni_konum
        self.guncelleme_tarihi = datetime.now()

    def durum_guncelle(self, yeni_durum):
        self.durum = yeni_durum
        self.guncelleme_tarihi = datetime.now()
        
    def bos_kapasite(self):
        return self.kapasite - self.aktif_yolcu

    def yolcu_ekle(self, adet=1):
        if self.aktif_yolcu + adet <= self.kapasite:
            self.aktif_yolcu += adet
            return True
        return False

    def yolcu_cikar(self, adet=1):
        if self.aktif_yolcu - adet >= 0:
            self.aktif_yolcu -= adet
            return True
        return False

    def sefer_arttir(self):
        self.sefer_sayisi += 1

    def doluluk_orani(self):
        if self.kapasite == 0:
            return 0
        return self.aktif_yolcu / self.kapasite

    def aktif_mi(self):
        return self.durum in ["Seferde", "Aktif"]

    def musait_mi(self):
        return self.durum in ["Müsait", "Beklemede", "Boşta"]

    def zaman_bilgisi(self):
        return {
            "olusturma": self.olusturma_tarihi,
            "guncelleme": self.guncelleme_tarihi
        }

    def ozet_bilgi(self):
        return {
            "araç id": self.arac_id,
            "kapasite": self.kapasite,
            "aktif_yolcu": self.aktif_yolcu,
            "durum": self.durum,
            "konum": self.mevcut_konum
        }

    def ayni_konum_mu(self, diger):
        return self.mevcut_konum == diger.mevcut_konum

    def sifirla(self):
        self.aktif_yolcu = 0
        self.durum = "Müsait"

    def durum_metni(self):
        return f"{self.id} - {self.durum}"

    def kapasite_doldu_mu(self):
        return self.aktif_yolcu >= self.kapasite

    def kapasite_bos_mu(self):
        return self.aktif_yolcu == 0

    def genel_durum(self):
        return {
            "durum": self.durum,
            "doluluk": self.doluluk_orani()
        }
class Sefer:
    def __init__(self, saat):
        self.saat = saat

    def sefer_durumu(self):
        if self.saat < datetime.now():
            return "Sefer tamamlandı"
        else:
            return "Sefer bekleniyor"
