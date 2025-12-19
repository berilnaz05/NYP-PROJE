# BASE CLASS
from abc import ABC, abstractmethod
from datetime import datetime
import uuid

# Ödeme Yöntemi
class OdemeYontemi(ABC):
    def __init__(
        self,
        kart_numarasi,
        son_kullanma_tarihi,
        cvv,
        tutar,
        sahip,
        bakiye,
        para_birimi="TL",
        cuzdan_adi=None,
        dogrulanmis=False   
    ):
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


# SUB CLASS 1 - Kredi Kartı Ödeme
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


# Sipariş ve Menü Servisleri
from datetime import datetime
from typing import List, Dict
import uuid

class YemekhaneMenuServisi:
    def __init__(self, menu_goster={}):
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

        self.ana_yemekler = {
            "Kuru Fasulye": 25,
            "Tavuk Sote": 30,
            "Izgara Köfte": 35,
            "Sebzeli Makarna": 20,
            "Balık Izgara": 40,
            "Et Sote": 45,
        }

        self.salatalar = {
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

    def menu_yazdir(self):
        for kategori in [
            self.baslangic,
            self.ara_sıcaklar,
            self.ana_yemekler,
            self.salatalar,
            self.tatlilar
        ]:
            for urun, fiyat in kategori.items():
                print(f"{urun}: {fiyat} TL")


class Siparis:
    def __init__(self, secilen_urunler):
        self.secilen_urunler = secilen_urunler

    def toplam_tutar_hesapla(self, menu):
        toplam = 0
        for urun in self.secilen_urunler:
            if urun in menu:
                toplam += menu[urun]
        return toplam

# ÜRÜN SINIFI
class Urun:
    def __init__(self, ad: str, fiyat: float, kategori: str):
        self.ad = ad
        self.fiyat = fiyat
        self.kategori = kategori

    def __str__(self):
        return f"{self.ad} ({self.kategori}) - {self.fiyat} TL"

# MENÜ SERVİSİ
class MenuServisi:
    def __init__(self):
        self.urunler: List[Urun] = []

    def urun_ekle(self, urun: Urun):
        self.urunler.append(urun)

    def menu_listele(self):
        print("\n--- YEMEKHANE MENÜSÜ ---")
        for urun in self.urunler:
            print(urun)

    def kategoriye_gore_listele(self, kategori: str):
        print(f"\n--- {kategori.upper()} ---")
        for urun in self.urunler:
            if urun.kategori == kategori:
                print(urun)

    def urun_bul(self, ad: str):
        for urun in self.urunler:
            if urun.ad == ad:
                return urun
        return None

# SİPARİŞ SERVİSİ
class SiparisServisi:
    def __init__(self):
        self.aktif_siparisler = []

    def siparis_olustur(self, kullanici: str):
        siparis = {
            "kullanici": kullanici,
            "urunler": [],
            "tarih": datetime.now()
        }
        self.aktif_siparisler.append(siparis)
        return siparis

    def urun_ekle(self, siparis: dict, urun: Urun, adet: int):
        siparis["urunler"].append({
            "urun": urun,
            "adet": adet,
            "ara_toplam": urun.fiyat * adet
        })

    def toplam_tutar_hesapla(self, siparis: dict):
        toplam = 0
        for kalem in siparis["urunler"]:
            toplam += kalem["ara_toplam"]
        return toplam

    def siparis_ozeti(self, siparis: dict):
        print("\n--- SİPARİŞ ÖZETİ ---")
        for kalem in siparis["urunler"]:
            print(
                f"{kalem['urun'].ad} x{kalem['adet']} = {kalem['ara_toplam']} TL"
            )
        print(f"Toplam: {self.toplam_tutar_hesapla(siparis)} TL")

# ÖDEME YÖNTEMİ SEÇME SERVİSİ
class OdemeYontemiSecici:
    def __init__(self, odeme_yontemleri: list):
        self.odeme_yontemleri = odeme_yontemleri

    def uygun_yontemleri_listele(self, tutar: float):
        uygunlar = []
        for yontem in self.odeme_yontemleri:
            if yontem.yetkilendir(tutar):
                uygunlar.append(yontem)
        return uygunlar

    def otomatik_sec(self, tutar: float):
        for yontem in self.odeme_yontemleri:
            if yontem.yetkilendir(tutar):
                return yontem
        return None

# ÖDEME GERÇEKLEŞTİRME SERVİSİ
class OdemeIslemServisi:
    def __init__(self):
        self.islem_gecmisi = []

    def odeme_yap(self, kullanici: str, siparis: dict, odeme_yontemi):
        tutar = 0
        for kalem in siparis["urunler"]:
            tutar += kalem["ara_toplam"]

        print(f"\n➡️ {kullanici} için ödeme başlatılıyor...")

        sonuc = odeme_yontemi.ode(tutar)

        if sonuc:
            islem = {
                "kullanici": kullanici,
                "tutar": tutar,
                "odeme_tipi": type(odeme_yontemi).__name__,
                "tarih": datetime.now(),
                "urun_sayisi": len(siparis["urunler"])
            }
            self.islem_gecmisi.append(islem)
            print("✅ Ödeme başarıyla tamamlandı.")
            return True
        else:
            print("❌ Ödeme başarısız.")
            return False

# RAPORLAMA SERVİSİ
class RaporlamaServisi:
    def __init__(self, islem_gecmisi: List[Dict]):
        self.islem_gecmisi = islem_gecmisi

    def tum_islemleri_listele(self):
        print("\n--- TÜM İŞLEMLER ---")
        for islem in self.islem_gecmisi:
            self._yazdir(islem)

    def kullaniciya_gore(self, kullanici: str):
        print(f"\n--- {kullanici} İŞLEMLERİ ---")
        for islem in self.islem_gecmisi:
            if islem["kullanici"] == kullanici:
                self._yazdir(islem)

    def tarih_araligina_gore(self, baslangic: datetime, bitis: datetime):
        print("\n--- TARİH ARALIĞI RAPORU ---")
        for islem in self.islem_gecmisi:
            if baslangic <= islem["tarih"] <= bitis:
                self._yazdir(islem)

    def toplam_ciro(self):
        toplam = 0
        for islem in self.islem_gecmisi:
            toplam += islem["tutar"]
        print(f"\n💰 Toplam Ciro: {toplam} TL")
        return toplam

    def _yazdir(self, islem: dict):
        print(
            f"{islem['kullanici']} | "
            f"{islem['tutar']} TL | "
            f"{islem['odeme_tipi']} | "
            f"{islem['tarih'].strftime('%d.%m.%Y %H:%M')}"
        )

from datetime import datetime
from typing import List, Optional

# MODEL
class OdemeModel:
    def __init__(
        self,
        odeme_id: str,
        kullanici: str,
        tutar: float,
        odeme_tipi: str,
        tarih: datetime
    ):
        self.odeme_id = odeme_id
        self.kullanici = kullanici
        self.tutar = tutar
        self.odeme_tipi = odeme_tipi
        self.tarih = tarih

    def __repr__(self):
        return (
            f"OdemeModel("
            f"id={self.odeme_id}, "
            f"kullanici={self.kullanici}, "
            f"tutar={self.tutar}, "
            f"tip={self.odeme_tipi}, "
            f"tarih={self.tarih})"
        )

# ÖDEME YÖNTEMİ MODELİ
class OdemeYontemiModel:
    def __init__(
        self,
        yontem_id: str,
        kullanici: str,
        yontem_adi: str,
        aktif: bool = True
    ):
        self.yontem_id = yontem_id
        self.kullanici = kullanici
        self.yontem_adi = yontem_adi
        self.aktif = aktif

    def __repr__(self):
        return (
            f"OdemeYontemiModel("
            f"id={self.yontem_id}, "
            f"kullanici={self.kullanici}, "
            f"yontem={self.yontem_adi}, "
            f"aktif={self.aktif})"
        )

# ÖDEME YÖNTEMİ REPOSITORY
class OdemeYontemiRepository:
    def __init__(self):
        self._yontemler: List[OdemeYontemiModel] = []

    def ekle(self, yontem: OdemeYontemiModel):
        self._yontemler.append(yontem)

    def tum_yontemleri_listele(self) -> List[OdemeYontemiModel]:
        return self._yontemler

    def kullaniciya_ait_yontemler(self, kullanici: str) -> List[OdemeYontemiModel]:
        return [
            y for y in self._yontemler
            if y.kullanici == kullanici and y.aktif
        ]

    def yontem_bul(self, yontem_id: str) -> Optional[OdemeYontemiModel]:
        for y in self._yontemler:
            if y.yontem_id == yontem_id:
                return y
        return None

    def pasif_yap(self, yontem_id: str) -> bool:
        yontem = self.yontem_bul(yontem_id)
        if yontem:
            yontem.aktif = False
            return True
        return False

# ÖDEME REPOSITORY
class OdemeRepository:
    def __init__(self):
        self._odemeler: List[OdemeModel] = []

    def odeme_kaydet(
        self,
        kullanici: str,
        tutar: float,
        odeme_tipi: str
    ) -> OdemeModel:
        odeme = OdemeModel(
            odeme_id=str(uuid.uuid4()),
            kullanici=kullanici,
            tutar=tutar,
            odeme_tipi=odeme_tipi,
            tarih=datetime.now()
        )
        self._odemeler.append(odeme)
        return odeme

    def tum_odemeleri_listele(self) -> List[OdemeModel]:
        return self._odemeler

    def odeme_bul_id_ile(self, odeme_id: str) -> Optional[OdemeModel]:
        for odeme in self._odemeler:
            if odeme.odeme_id == odeme_id:
                return odeme
        return None

    def kullaniciya_gore_filtrele(self, kullanici: str) -> List[OdemeModel]:
        return [
            o for o in self._odemeler
            if o.kullanici == kullanici
        ]

    def tarih_araligina_gore_filtrele(
        self,
        baslangic: datetime,
        bitis: datetime
    ) -> List[OdemeModel]:
        return [
            o for o in self._odemeler
            if baslangic <= o.tarih <= bitis
        ]

    def toplam_tutar(self) -> float:
        toplam = 0
        for o in self._odemeler:
            toplam += o.tutar
        return toplam

    def kullanici_bazli_toplam(self, kullanici: str) -> float:
        toplam = 0
        for o in self._odemeler:
            if o.kullanici == kullanici:
                toplam += o.tutar
        return toplam

# RAPOR SERVİSİ
class OdemeRaporServisi:
    def __init__(self, odeme_repo: OdemeRepository):
        self.odeme_repo = odeme_repo

    def tum_odeme_raporu(self) -> List[OdemeModel]:
        return self.odeme_repo.tum_odemeleri_listele()

    def kullanici_raporu(self, kullanici: str) -> List[OdemeModel]:
        return self.odeme_repo.kullaniciya_gore_filtrele(kullanici)

    def tarih_raporu(
        self,
        baslangic: datetime,
        bitis: datetime
    ) -> List[OdemeModel]:
        return self.odeme_repo.tarih_araligina_gore_filtrele(
            baslangic,
            bitis
        )

    def genel_ciro(self) -> float:
        return self.odeme_repo.toplam_tutar()
