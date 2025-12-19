from abc import ABC, abstractmethod
from datetime import datetime


class UlasimAraci(ABC):
    def __init__(self, id, kapasite, mevcut_konum,durum):
        self.id = id
        self.kapasite = kapasite
        self.mevcut_konum = mevcut_konum
        self.durum = durum
        self.olusturma_tarihi = datetime.now()
        self.guncelleme_tarihi = datetime.now()
        self.aktif_yolcu = 0
        self.sefer_sayisi = 0
        self.rezervasyon_acik = False

    def konum_guncelle(self, yeni_konum):
        self.mevcut_konum = yeni_konum
        self.guncelleme_tarihi = datetime.now()

    def durum_guncelle(self, yeni_durum):
        self.durum = yeni_durum
        self.guncelleme_tarihi = datetime.now()

    def rezervasyon_ac(self):
        self.rezervasyon_acik = True

    def rezervasyon_kapat(self):
        self.rezervasyon_acik = False

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
        return self.durum in ["Seferde", "Aktif", "Arızalı"]

    def musait_mi(self):
        return self.durum in ["Müsait", "Beklemede", "Boşta"]

    def zaman_bilgisi(self):
        return {
            "olusturma": self.olusturma_tarihi,
            "guncelleme": self.guncelleme_tarihi
        }

    def ozet_bilgi(self):
        return {
            "id": self.id,
            "kapasite": self.kapasite,
            "aktif_yolcu": self.aktif_yolcu,
            "durum": self.durum,
            "lokasyon": self.mevcut_lokasyon
        }

    def ayni_konum_mu(self, diger):
        return self.mevcut_konum== diger.mevcut_konum

    def sifirla(self):
        self.aktif_yolcu = 0
        self.durum = "Müsait"
        self.rezervasyon_acik = False

    def durum_metni(self):
        return f"{self.id} - {self.durum}"

    def kapasite_doldu_mu(self):
        return self.aktif_yolcu >= self.kapasite

    def kapasite_bos_mu(self):
        return self.aktif_yolcu == 0

    def rezervasyon_durumu(self):
        return "Açık" if self.rezervasyon_acik else "Kapalı"

    def genel_durum(self):
        return {
            "durum": self.durum,
            "rezervasyon": self.rezervasyon_durumu(),
            "doluluk": self.doluluk_orani()
        }

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