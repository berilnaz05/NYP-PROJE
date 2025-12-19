#BASE CLASS
from abc import ABC, abstractmethod
from datetime import datetime

#Ödeme Yöntemi 
class OdemeYontemi(ABC):
    def __init__(self, kart_numarasi, son_kullanma_tarihi, cvv, tutar, sahip, bakiye, para_birimi="TL",cuzdan_adi=None, dogrulanmis=False):
        self.sahip = sahip
        self.bakiye = bakiye
        self.para_birimi = para_birimi
        self.kart_numarasi = kart_numarasi
        self.son_kullanma_tarihi = son_kullanma_tarihi  
        self.cvv = cvv
        self.tutar = tutar
        self.cuzdan_adi = cuzdan_adi
        self.dogrulanmis = dogrulanmis

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

#SUN CLASS3 - Dijital Cüzdan Ödeme
class DijitalCuzdanOdeme(OdemeYontemi):
    def __init__(self,  tutar, sahip, bakiye, para_birimi="TL",cuzdan_adi=None, dogrulanmis=False):
        super().__init__(tutar, sahip, bakiye, para_birimi, cuzdan_adi, dogrulanmis)
    
    def yetkilendir(self, tutar):
        return self.bakiye >= tutar and self.dogrulanmis
    
    def ode(self, tutar, bakiye, dogrulanmis, cuzdan_adi):
        super().__init__(self, tutar, bakiye, dogrulanmis, cuzdan_adi)
        if dogrulanmis== True:
            print(f"{cuzdan_adi} adlı dijital cüzdan doğrulandı.")
        else:
            print(f"{cuzdan_adi} adlı dijital cüzdan doğrulanmadı. Ödeme yapılamıyor.")

        if bakiye>= tutar:
            self.bakiye -= tutar
            print(f"{tutar} {self.para_birimi} tutarındaki ödeme {cuzdan_adi} adlı dijital cüzdandan başarıyla gerçekleştirildi.")
        else:
            print("Yetersiz bakiye!")

#Sipariş ve Menü Servisleri
class YemekhaneMenuServisi:
    def __init__(self,menu_goster={}):
        self.menu_goster = menu_goster
        self.baslangic = {
            "Mercimek Çorbası": 15,
            "Ezogelin Çorbası": 12,
            "Tarhana Çorbası": 10,
            "Domates Çorbası": 14,
            "Sebze Çorbası": 13,
        }

        self.ara_sıcaklar = {
            "Sigara Böreği": 20,
            "Patates Kızartması": 18,
            "Kalamar": 30,
            "Mücver": 22,
            "Paçanga Böreği": 25,
            "Fırınlanmış Midye": 28,
        }

        self.ana_yemekler,self.salatalar = {
            "Kuru Fasulye": 25,
            "Tavuk Sote": 30,
            "Izgara Köfte": 35,
            "Sebzeli Makarna": 20,
            "Balık Izgara": 40,
            "Et Sote": 45,
        }, {
            "Çoban Salata": 15,
            "Mevsim Salata": 12,
            "Akdeniz Salata": 18
        }

        self.tatlilar = {
            "Sütlaç": 10,
            "Kazandibi": 12,
            "Baklava": 20,
            "Künefe": 25,
            "Aşure": 15
        }

        def menu_goster(self):
            print("\n--- MENÜ ---")
            for urun, fiyat in self.menu.items():
                print(f"{urun}: {fiyat} TL")

class Siparis:
    def __init__(self, secilen_urunler):
        self.secilen_urunler = secilen_urunler
    def toplam_tutar_hesapla(self, menu):
        return sum(menu[urun] for urun in self.secilen_urunler)
    