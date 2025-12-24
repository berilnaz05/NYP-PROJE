from abc import ABC, abstractmethod
from datetime import datetime
import uuid

class OdemeYontemi(ABC):
    GECERLI_PARA_BIRIMLERI = {"TL", "USD", "EUR"}

    def __init__(self, sahip, bakiye, para_birimi="TL"):
        if para_birimi not in self.GECERLI_PARA_BIRIMLERI:
            raise ValueError("Geçersiz para birimi")

        self.sahip = sahip
        self.bakiye = bakiye
        self.para_birimi = para_birimi

        self.islem_id = None
        self.islem_tarihi = None
        self.islem_durumu = None
        self.son_fis = None
        self.fis_gecmisi = []

    @abstractmethod
    def yetkilendir(self, tutar):
        pass

    def ode(self, tutar):
        if not self._gecerli_tutar_mi(tutar):
            self.islem_durumu = "BAŞARISIZ"
            return False

        if not self.yetkilendir(tutar):
            self.islem_durumu = "BAŞARISIZ"
            self._islem_basarisiz_mesaji()
            return False

        self._islem_baslat()
        komisyon = self.komisyon_hesapla(tutar)
        toplam_tutar = tutar + komisyon

        if self.bakiye < toplam_tutar:
            self.islem_durumu = "BAŞARISIZ"
            print("Komisyon dahil bakiye yetersiz.")
            return False

        self._bakiyeden_dus(toplam_tutar)
        self.islem_durumu = "BAŞARILI"

        self._fis_olustur(tutar, komisyon)
        self._fis_kaydet()
        self._islem_basarili_mesaji()

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
        return tutar * kurlar.get((self.para_birimi, hedef_para), 1)

    def iade_et(self, fis_id):
        for fis in self.fis_gecmisi:
            if fis["islem_id"] == fis_id:
                self.bakiye += fis["toplam_tutar"]
                print("İade işlemi başarılı.")
                return True
        print("Fiş bulunamadı.")
        return False

    def fis_goster(self):
        if self.son_fis:
            print(self.son_fis)
        else:
            print("Gösterilecek fiş yok.")

    def fis_gecmisini_goster(self):
        for fis in self.fis_gecmisi:
            print(fis)

    def _fis_olustur(self, tutar, komisyon):
        self.son_fis = f"""
        ---------- ÖDEME FİŞİ ----------
        İşlem ID     : {self.islem_id}
        Tarih        : {self.islem_tarihi}
        Kullanıcı    : {self.sahip}
        Ödeme Türü   : {self.__class__.__name__}
        Tutar        : {tutar}
        Komisyon     : {komisyon}
        Toplam       : {tutar + komisyon}
        Para Birimi  : {self.para_birimi}
        Durum        : {self.islem_durumu}
        --------------------------------
        """

        self.fis_gecmisi.append({
            "islem_id": self.islem_id,
            "tutar": tutar,
            "komisyon": komisyon,
            "toplam_tutar": tutar + komisyon,
            "tarih": self.islem_tarihi,
            "durum": self.islem_durumu
        })

    def _fis_kaydet(self):
        with open(f"fis_{self.islem_id}.txt", "w", encoding="utf-8") as f:
            f.write(self.son_fis)

    def _islem_baslat(self):
        self.islem_id = str(uuid.uuid4())
        self.islem_tarihi = datetime.now()

    def _gecerli_tutar_mi(self, tutar):
        if tutar <= 0:
            print("Tutar sıfırdan büyük olmalı.")
            return False
        return True

    def _bakiyeden_dus(self, tutar):
        self.bakiye -= tutar

    def _islem_basarili_mesaji(self):
        print("İşlem başarılı ✅ Fiş oluşturuldu.")

    def _islem_basarisiz_mesaji(self):
        print("İşlem başarısız ❌")
