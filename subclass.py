# SUB CLASS 1 - Kredi Kartı Ödeme

from baseclass import OdemeYontemi
from datetime import datetime

class KrediKartiOdeme(OdemeYontemi):
    def __init__(self, kart_numarasi, son_kullanma_tarihi, cvv, sahip, bakiye, para_birimi="TL"):
        super().__init__(kart_numarasi, son_kullanma_tarihi, cvv, 0, sahip, bakiye, para_birimi)

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

        if para_birimi != "TL":
            raise ValueError("Kredi kartı ödemeleri sadece TL cinsindendir.")

    def yetkilendir(self, tutar):
        return self.bakiye >= tutar

    def ode(self, tutar):
        if self.yetkilendir(tutar):
            self.bakiye -= tutar
            print(f"Sayın {self.sahip}; {tutar} {self.para_birimi} tutarındaki ödemeniz başarıyla gerçekleştirildi.")
        else:
            print(f"Sayın {self.sahip}; yeterli bakiye yok!")


# SUB CLASS 2 - Nakit Ödeme
class NakitOdeme(OdemeYontemi):
    def __init__(self, kart_numarasi, son_kullanma_tarihi, cvv, sahip, bakiye, para_birimi="TL"):
        super().__init__(kart_numarasi, son_kullanma_tarihi, cvv, 0, sahip, bakiye, para_birimi)

    def yetkilendir(self, tutar):
        return self.bakiye >= tutar

    def ode(self, tutar):
        if self.yetkilendir(tutar):
            self.bakiye -= tutar
            print(f"{tutar} {self.para_birimi} nakit ödendi.")
        else:
            print("Yetersiz nakit!")


# SUB CLASS 3 - Dijital Cüzdan Ödeme
class DijitalCuzdanOdeme(OdemeYontemi):
    def __init__(self, tutar, sahip, bakiye, para_birimi="TL", cuzdan_adi=None, dogrulanmis=False):
        super().__init__(None, None, None, tutar, sahip, bakiye, para_birimi, cuzdan_adi, dogrulanmis)

    def yetkilendir(self, tutar):
        return self.bakiye >= tutar and self.dogrulanmis

    def ode(self, tutar):
        if not self.dogrulanmis:
            print(f"{self.cuzdan_adi} adlı dijital cüzdan doğrulanmadı. Ödeme yapılamıyor.")
            return

        if self.bakiye >= tutar:
            self.bakiye -= tutar
            print(f"{tutar} {self.para_birimi} tutarındaki ödeme {self.cuzdan_adi} adlı dijital cüzdandan başarıyla gerçekleştirildi.")
        else:
            print("Yetersiz bakiye!")