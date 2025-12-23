from typing import List, Dict
from base import OdemeYontemi
from datetime import datetime

class OdemeService:
    def __init__(self):
        self.islemler: List[Dict] = []

    def odeme_yap(self, odeme_yontemi: OdemeYontemi, tutar: float) -> bool:
        basarili = odeme_yontemi.ode(tutar)
        islem = {
            "islem_id": odeme_yontemi.islem_id or f"ISLEM-{len(self.islemler)+1}",
            "sahip": getattr(odeme_yontemi, "sahip", "Bilinmiyor"),
            "tutar": tutar,
            "para_birimi": getattr(odeme_yontemi, "para_birimi", "TL"),
            "durum": "BAŞARILI" if basarili else "BAŞARISIZ",
            "tarih": datetime.now()
        }
        self.islemler.append(islem)
        return basarili

    def odeme_gecmisini_goster(self, kullanici: str = None):
        for i in self.islemler:
            if kullanici and i["sahip"] != kullanici:
                continue
            print(f"İşlem ID: {i['islem_id']}, Sahip: {i['sahip']}, Tutar: {i['tutar']} {i['para_birimi']}, Durum: {i['durum']}, Tarih: {i['tarih']}")

    def odeme_sil(self, islem_id: str) -> bool:
        for i in self.islemler:
            if i["islem_id"] == islem_id:
                self.islemler.remove(i)
                return True
        return False

    def toplam_odeme(self, kullanici: str = None) -> float:
        toplam = 0
        for i in self.islemler:
            if kullanici and i["sahip"] != kullanici:
                continue
            if i["durum"] == "BAŞARILI":
                toplam += i["tutar"]
        return toplam

    def islemleri_kaydet(self, dosya_adi="odeme_gecmisi.txt"):
        with open(dosya_adi, "w", encoding="utf-8") as f:
            for i in self.islemler:
                f.write(f"{i['islem_id']} | {i['sahip']} | {i['tutar']} {i['para_birimi']} | {i['durum']} | {i['tarih']}\n")

    def islemleri_oku(self, dosya_adi="odeme_gecmisi.txt"):
        try:
            with open(dosya_adi, "r", encoding="utf-8") as f:
                self.islemler.clear()
                for line in f:
                    parts = line.strip().split(" | ")
                    if len(parts) == 5:
                        islem_id, sahip, tutar_str, durum, tarih_str = parts
                        tutar, para_birimi = tutar_str.split(" ")
                        self.islemler.append({
                            "islem_id": islem_id,
                            "sahip": sahip,
                            "tutar": float(tutar),
                            "para_birimi": para_birimi,
                            "durum": durum,
                            "tarih": datetime.strptime(tarih_str, "%Y-%m-%d %H:%M:%S.%f")
                        })
        except FileNotFoundError:
            pass

    def kullanici_bakiyesi(self, sahip: str) -> float:
        return sum([i["tutar"] for i in self.islemler if i["sahip"] == sahip and i["durum"] == "BAŞARILI"])

    def basarili_odeme_sayisi(self) -> int:
        return len([i for i in self.islemler if i["durum"] == "BAŞARILI"])

    def basarisiz_odeme_sayisi(self) -> int:
        return len([i for i in self.islemler if i["durum"] == "BAŞARISIZ"])

    def en_yuksek_odeme(self):
        if not self.islemler:
            return None
        return max(self.islemler, key=lambda x: x["tutar"])

    def en_dusuk_odeme(self):
        if not self.islemler:
            return None
        return min(self.islemler, key=lambda x: x["tutar"])

    def rastgele_odeme_uret(self, odeme_yontemi: OdemeYontemi):
        import random
        tutar = random.randint(1, 500)
        self.odeme_yap(odeme_yontemi, tutar)

    def odeme_istatistikleri(self):
        basarili = self.basarili_odeme_sayisi()
        basarisiz = self.basarisiz_odeme_sayisi()
        toplam = sum([i["tutar"] for i in self.islemler])
        print(f"Toplam Ödeme: {toplam}, Başarılı: {basarili}, Başarısız: {basarisiz}")

    def islemleri_listele_dosyaya(self, dosya_adi="odeme_rapor.txt"):
        with open(dosya_adi, "w", encoding="utf-8") as f:
            for i in self.islemler:
                f.write(f"{i['islem_id']} | {i['sahip']} | {i['tutar']} {i['para_birimi']} | {i['durum']} | {i['tarih']}\n")
