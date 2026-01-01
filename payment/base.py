from abc import ABC, abstractmethod
from datetime import datetime
import uuid

class OdemeYontemi(ABC):
    GECERLI_PARA_BIRIMLERI = {"TL", "USD", "EUR"}

    toplam_odeme_sayisi = 0
    toplam_komisyon = 0.0

    def __init__(self, sahip, bakiye, para_birimi="TL"):
        if para_birimi not in self.GECERLI_PARA_BIRIMLERI:
            raise ValueError("Geçersiz para birimi")

        self.__sahip = sahip
        self.__bakiye = bakiye
        self.__para_birimi = para_birimi

        self.__islem_id = None
        self.__islem_tarihi = None
        self.__islem_durumu = None
        self.__son_fis = None
        self.__fis_gecmisi = []

    @abstractmethod
    def yetkilendir(self, tutar):
        pass

    @abstractmethod
    def ode(self, tutar):
        if not self._gecerli_tutar_mi(tutar):
            self.__islem_durumu = "BAŞARISIZ"
            return False

        if not self.yetkilendir(tutar):
            self.__islem_durumu = "BAŞARISIZ"
            self._islem_basarisiz_mesaji()
            return False

        self._islem_baslat()
        komisyon = self.komisyon_hesapla(tutar)
        toplam_tutar = tutar + komisyon

        if self.__bakiye < toplam_tutar:
            self.__islem_durumu = "BAŞARISIZ"
            print("Komisyon dahil bakiye yetersiz.")
            return False

        self._bakiyeden_dus(toplam_tutar)
        self.__islem_durumu = "BAŞARILI"

        self._fis_olustur(tutar, komisyon)
        self._fis_kaydet()
        self._islem_basarili_mesaji()

        OdemeYontemi.toplam_odeme_sayisi += 1
        OdemeYontemi.toplam_komisyon += komisyon

        return True

    def komisyon_hesapla(self, tutar):
        return 0.0

    def kur_donustur(self, tutar, hedef_para):
        kurlar = {
            ("TL", "USD"): 0.033,
            ("USD", "TL"): 30,
            ("TL", "EUR"): 0.030,
            ("EUR", "TL"): 33,
        }
        return tutar * kurlar.get((self.__para_birimi, hedef_para), 1)

    @classmethod
    def toplam_odeme_bilgisi(cls):
        print(f"Toplam ödeme sayısı: {cls.toplam_odeme_sayisi}")
        print(f"Toplam komisyon: {cls.toplam_komisyon:.2f} TL")

    @staticmethod
    def para_birimi_kontrol(para):
        if para not in OdemeYontemi.GECERLI_PARA_BIRIMLERI:
            raise ValueError("Geçersiz para birimi")

    def _fis_olustur(self, tutar, komisyon):
        self.__son_fis = f"""
        ---------- ÖDEME FİŞİ ----------
        İşlem ID     : {self.__islem_id}
        Tarih        : {self.__islem_tarihi}
        Kullanıcı    : {self.__sahip}
        Ödeme Türü   : {self.__class__.__name__}
        Tutar        : {tutar}
        Komisyon     : {komisyon}
        Toplam       : {tutar + komisyon}
        Para Birimi  : {self.__para_birimi}
        Durum        : {self.__islem_durumu}
        --------------------------------
        """
        self.__fis_gecmisi.append({
            "islem_id": self.__islem_id,
            "tutar": tutar,
            "komisyon": komisyon,
            "toplam_tutar": tutar + komisyon,
            "tarih": self.__islem_tarihi,
            "durum": self.__islem_durumu
        })

    def _fis_kaydet(self):
        with open(f"fis_{self.__islem_id}.txt", "w", encoding="utf-8") as f:
            f.write(self.__son_fis)

    def _islem_baslat(self):
        self.__islem_id = str(uuid.uuid4())
        self.__islem_tarihi = datetime.now()

    def _gecerli_tutar_mi(self, tutar):
        if tutar <= 0:
            print("Tutar sıfırdan büyük olmalı.")
            return False
        return True

    def _bakiyeden_dus(self, tutar):
        self.__bakiye -= tutar

    def _islem_basarili_mesaji(self):
        print("İşlem başarılı ✅ Fiş oluşturuldu.")

    def _islem_basarisiz_mesaji(self):
        print("İşlem başarısız ❌")

    # Getter / Setter 
    
    @property
    def bakiye(self):
        return self._bakiye

    @bakiye.setter
    def bakiye(self, value):
        if value < 0:
            raise ValueError("Bakiye negatif olamaz")
        self._bakiye = value

    @property
    def sahip(self):
        return self.__sahip

    @property
    def para_birimi(self):
        return self.__para_birimi

    @property
    def fis_gecmisi(self):
        return self.__fis_gecmisi
    