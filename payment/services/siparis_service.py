from datetime import datetime
from payment.services.menu_service import Urun

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
