from datetime import datetime

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
