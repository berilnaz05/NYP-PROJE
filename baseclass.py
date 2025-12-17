#BASE CLASS
from abc import ABC, abstractmethod
from datetime import datetime

#Ödeme Yöntemi 
class OdemeYontemi(ABC):
    def __init__(self, kart_numarasi, son_kullanma_tarihi, cvv, tutar, sahip, bakiye, para_birimi="TL"):
        self.sahip = sahip
        self.bakiye = bakiye
        self.para_birimi = para_birimi
        self.kart_numarasi = kart_numarasi
        self.son_kullanma_tarihi = son_kullanma_tarihi  
        self.cvv = cvv
        self.tutar = tutar

    @abstractmethod
    def yetkilendir(self, tutar):
        pass

    def ode(self, tutar):
        if self.yetkilendir(tutar):
            return True
        return False
    
    def bilgi(self, tutar):
        if self.bakiye >= tutar:
            print(f"{self.sahip} adlı kullanıcının bakiyesi yeterlidir.")
        else:
            print(f"{self.sahip} adlı kullanıcının bakiyesi yetersizdir.")
        return 

#SUB CLASS 1 - Kredi Kartı Ödeme
class KrediKartiOdeme(OdemeYontemi):
    def __init__(self, kart_numarasi, son_kullanma_tarihi, cvv, sahip, bakiye, para_birimi="TL"):
        super().__init__(kart_numarasi, son_kullanma_tarihi, cvv, 0, sahip, bakiye, para_birimi)

        # Kart bilgilerini doğrulama
        if len(kart_numarasi) != 16:
            raise ValueError("Kart numarası 16 haneli olmalıdır.")
        else:
            print("Lütfen son kullanma tarihini 'AA/YY' formatında giriniz.")

        try:
            kart_tarih = datetime.strptime(son_kullanma_tarihi, "%m/%y")
            if kart_tarih < datetime.now():
                raise ValueError("Kartın son kullanma tarihi geçmiş.")
            else:
                print("Lütfen CVV kodunu giriniz.")
        except:
            raise ValueError("Son kullanma tarihi formatı yanlış. 'AA/YY' şeklinde olmalı.")

        if len(cvv) != 3:
            raise ValueError("CVV kodu 3 haneli olmalıdır.")
        else:
            print(f"Sayın {sahip}; Kredi kartı bilgileriniz doğrulandı.")

        if para_birimi != "TL":
            raise ValueError("Kredi kartı ödemeleri sadece TL cinsindendir.")

    def yetkilendir(self, tutar):
        return self.bakiye >= tutar
    
    def ode(self, tutar):
        if self.yetkilendir(tutar):
            self.bakiye -= tutar
            print(f"Sayın {self.sahip}; {tutar} {self.para_birimi} tutarındaki ödemeniz başarıyla gerçekleştirilmiştir.")
        else:
            print(f"Sayın {self.sahip}; yeterli bakiye yok!")

#SUB CLASS 2 - Nakit Ödeme
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
            
