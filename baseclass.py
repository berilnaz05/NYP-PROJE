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
            
# SERVİSLER
class YemekhaneServisi:
    def __init__(self):
        # Menü: ürün adı -> fiyat
        self.menu = {
            "Hamburger": 25,
            "Pizza": 40,
            "Salata": 15,
            "Kahve": 10,
            "Çay": 5
        }
        # Sipariş listesi
        self.siparisler = []

    def menu_goster(self):
        print("---- Menü ----")
        for urun, fiyat in self.menu.items():
            print(f"{urun}: {fiyat} TL")
        print("--------------")

    def siparis_olustur(self, kullanici, secilen_urunler: dict):
        """
        secilen_urunler: {"Hamburger": 2, "Kahve":1} gibi
        """
        toplam_tutar = 0
        for urun, adet in secilen_urunler.items():
            if urun in self.menu:
                toplam_tutar += self.menu[urun] * adet
            else:
                print(f"{urun} menüde bulunamadı!")
        siparis = {
            "kullanici": kullanici,
            "urunler": secilen_urunler,
            "toplam_tutar": toplam_tutar,
            "tarih": datetime.now()
        }
        self.siparisler.append(siparis)
        print(f"{kullanici} için sipariş oluşturuldu. Toplam tutar: {toplam_tutar} TL")
        return toplam_tutar

# REPO / VERİ YÖNETİMİ
class OdemeRepository:
    def __init__(self):
        self.odemeler = []  # ödeme kayıtları
        self.odeme_yontemleri = []  # kullanıcıların ödeme yöntemleri

    def odeme_yontemi_ekle(self, odeme_yontemi: OdemeYontemi):
        self.odeme_yontemleri.append(odeme_yontemi)

    def kullanici_odeme_yontemlerini_getir(self, kullanici):
        return [yontem for yontem in self.odeme_yontemleri if yontem.sahip == kullanici]

    def odeme_kaydet(self, odeme: dict):
        self.odemeler.append(odeme)
        print(f"{odeme['kullanici']} adlı kullanıcının {odeme['toplam_tutar']} TL tutarındaki ödemesi kaydedildi.")

    def odeme_filtrele(self, kullanici=None, baslangic_tarihi=None, bitis_tarihi=None):
        sonuc = self.odemeler
        if kullanici:
            sonuc = [o for o in sonuc if o["kullanici"] == kullanici]
        if baslangic_tarihi:
            sonuc = [o for o in sonuc if o["tarih"] >= baslangic_tarihi]
        if bitis_tarihi:
            sonuc = [o for o in sonuc if o["tarih"] <= bitis_tarihi]
        return sonuc

# ÖDEME SERVİSİ

class OdemeServisi:
    def __init__(self, repo: OdemeRepository):
        self.repo = repo

    def odeme_yap(self, kullanici, odeme_yontemi: OdemeYontemi, tutar):
        if odeme_yontemi.yetkilendir(tutar):
            odeme_yontemi.ode(tutar)
            kayit = {
                "kullanici": kullanici,
                "toplam_tutar": tutar,
                "tarih": datetime.now(),
                "odeme_turu": type(odeme_yontemi).__name__
            }
            self.repo.odeme_kaydet(kayit)
            print(f"{kullanici} adlı kullanıcının ödemesi başarıyla gerçekleşti.")
            return True
        else:
            print(f"{kullanici} adlı kullanıcının ödemesi gerçekleştirilemedi. Yetersiz bakiye/limit!")
            return False

# TEST ÖRNEKLERİ

if __name__ == "__main__":
    # Repo ve servis
    repo = OdemeRepository()
    servis = OdemeServisi(repo)
    yemekhane = YemekhaneServisi()

    # Ödeme yöntemleri
    kredi = KrediKartiOdeme("1234567812345678", "12/30", "123", "Ali", 0, limit=500)
    nakit = NakitOdeme("", "", "", "Veli", 200)
    cuzdan = DijitalCuzdanOdeme("", "", "", 0, "Ayşe", 150)

    # Repo'ya ekle
    repo.odeme_yontemi_ekle(kredi)
    repo.odeme_yontemi_ekle(nakit)
    repo.odeme_yontemi_ekle(cuzdan)

    # Menü göster
    yemekhane.menu_goster()

    # Sipariş oluştur
    toplam = yemekhane.siparis_olustur("Ali", {"Hamburger": 2, "Kahve":1})

    # Ödeme denemesi
    servis.odeme_yap("Ali", kredi, toplam)
    servis.odeme_yap("Veli", nakit, toplam)
    servis.odeme_yap("Ayşe", cuzdan, toplam)

    # Raporlama
    print("\n--- Ödeme Geçmişi ---")
    for odeme in repo.odeme_filtrele():
        print(odeme)
