from abc import ABC, abstractmethod
from datetime import datetime,timedelta
from enum import Enum 
class Kapsam(Enum):
    kampus_ici="kampus içi"
    kampus_disi="kampüs dışı"

class UlasimAraci(ABC):
    def __init__(self,arac_id,kapasite,kalkis,bitis,durum,guzergah,kapsam):
        self.arac_id = arac_id
        self.kapsam=kapsam
        self.kapasite = kapasite
        self.kalkis = kalkis
        self.bitis = bitis
        self.durum = durum
        self.guzergah = guzergah
        self.kullanim_alani="kampüs içi"

        self.olusturma_tarihi = datetime.now()
        self.guncelleme_tarihi = datetime.now()

        self.aktif_yolcu = 0
               
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