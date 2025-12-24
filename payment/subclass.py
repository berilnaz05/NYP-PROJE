# SUB CLASS 1 - Kredi Kartı Ödeme
from base import OdemeYontemi
from datetime import datetime

class KrediKartiOdeme(OdemeYontemi):
    def __init__(self, sahip, bakiye, kart_numarasi, son_kullanma_tarihi, cvv):
        super().__init__(sahip, bakiye, para_birimi="TL")
        self.kart_numarasi = kart_numarasi
        self.son_kullanma_tarihi = son_kullanma_tarihi
        self.cvv = cvv

        if not kart_numarasi.isdigit():
            raise ValueError("Kart numarası sadece rakamlardan oluşmalıdır.")

        if not cvv.isdigit():
            raise ValueError("CVV sadece rakam olmalıdır.")

        if len(kart_numarasi) != 16:
            raise ValueError("Kart numarası 16 haneli olmalıdır.")

        try:
            kart_tarih = datetime.strptime(son_kullanma_tarihi, "%m/%y")
            if kart_tarih < datetime.now():
                raise ValueError("Kartın son kullanma tarihi geçmiş.")
        except:
            raise ValueError("Son kullanma tarihi formatı yanlış. 'AA/YY' şeklinde olmalı.")

        if len(cvv) != 3:
            raise ValueError("CVV kodu 3 haneli olmalıdır.")


    def yetkilendir(self, tutar):
        return self.bakiye >= tutar


    def komisyon_hesapla(self, tutar):
        return tutar * 0.02

# SUB CLASS 2 - Nakit Ödeme
class NakitOdeme(OdemeYontemi):
    def __init__(self,sahip,bakiye,para_birimi):
        super().__init__(sahip ,bakiye, para_birimi)

    def yetkilendir(self, tutar):
        return self.bakiye >= tutar

# SUB CLASS 3 - Dijital Cüzdan Ödeme
class DijitalCuzdanOdeme(OdemeYontemi):
    def __init__(self, sahip, bakiye, para_birimi="TL", cuzdan_adi="", dogrulanmis=False):
        super().__init__(sahip, bakiye, para_birimi)
        self.cuzdan_adi = cuzdan_adi
        self.dogrulanmis = dogrulanmis

    def yetkilendir(self, tutar):
        if not self.dogrulanmis:
            print(f"{self.cuzdan_adi} adlı dijital cüzdan doğrulanmadı.")
            return False
        return self.bakiye >= tutar
