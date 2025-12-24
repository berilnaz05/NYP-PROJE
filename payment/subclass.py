# SUB CLASS 1 - Kredi Kartı Ödeme
from .base import OdemeYontemi
from datetime import datetime

class KrediKartiOdeme(OdemeYontemi):
    def __init__(self, sahip, bakiye, kart_numarasi, son_kullanma_tarihi, cvv):
        super().__init__(sahip, bakiye)
        self.__kart_numarasi = kart_numarasi
        self.__son_kullanma_tarihi = son_kullanma_tarihi
        self.__cvv = cvv

        if not kart_numarasi.isdigit() or len(kart_numarasi) != 16:
            raise ValueError("Kart numarası 16 haneli ve rakamlardan oluşmalıdır.")
        if not cvv.isdigit() or len(cvv) != 3:
            raise ValueError("CVV 3 haneli olmalıdır.")
        try:
            kart_tarih = datetime.strptime(son_kullanma_tarihi, "%m/%y")
            if kart_tarih < datetime.now():
                raise ValueError("Kartın son kullanma tarihi geçmiş.")
        except:
            raise ValueError("Son kullanma tarihi formatı yanlış. 'AA/YY' şeklinde olmalı.")

    def yetkilendir(self, tutar):
        return self.bakiye >= tutar

    def komisyon_hesapla(self, tutar):
        return tutar * 0.02

class NakitOdeme(OdemeYontemi):
    def __init__(self, sahip, bakiye, para_birimi, fis_talep=True):
        super().__init__(sahip, bakiye, para_birimi)
        self.__fis_talep = fis_talep

    def yetkilendir(self, tutar):
        return self.bakiye >= tutar

    def ode(self, tutar):
        success = super().ode(tutar)
        if success and self.__fis_talep:
            print("Nakit ödeme fişi verildi 🧾")
        return success

    @property
    def fis_talep(self):
        return self.__fis_talep

    @fis_talep.setter
    def fis_talep(self, value):
        self.__fis_talep = value

class DijitalCuzdanOdeme(OdemeYontemi):
    def __init__(self, sahip, bakiye, para_birimi="TL", cuzdan_adi="", dogrulanmis=False):
        super().__init__(sahip, bakiye, para_birimi)
        self.__cuzdan_adi = cuzdan_adi
        self.__dogrulanmis = dogrulanmis

    def yetkilendir(self, tutar):
        if not self.__dogrulanmis:
            print(f"{self.__cuzdan_adi} adlı dijital cüzdan doğrulanmadı.")
            return False
        return self.bakiye >= tutar

    @property
    def dogrulanmis(self):
        return self.__dogrulanmis

    @dogrulanmis.setter
    def dogrulanmis(self, value):
        self.__dogrulanmis = value

    @property
    def cuzdan_adi(self):
        return self.__cuzdan_adi
