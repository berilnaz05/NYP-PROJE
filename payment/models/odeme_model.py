from datetime import datetime
from typing import List
import uuid
from ..base import OdemeYontemi

class OdemeModel:
    tum_odemeler: List[dict] = []

    def __init__(self, odeme_yontemi: OdemeYontemi, tutar: float, para_birimi: str = "TL"):
        self.odeme_id = str(uuid.uuid4())
        self.odeme_yontemi = odeme_yontemi
        self.tutar = tutar
        self.para_birimi = para_birimi
        self.tarih = datetime.now()
        self.durum = None
        OdemeModel.tum_odemeler.append(self)

    def odeme_yap(self):
        if self.odeme_yontemi.ode(self.tutar):
            self.durum = "BAŞARILI"
        else:
            self.durum = "BAŞARISIZ"
        return self.durum

    @classmethod
    def basarili_odemeler(cls):
        return [o for o in cls.tum_odemeler if o.durum == "BAŞARILI"]

    @classmethod
    def basarisiz_odemeler(cls):
        return [o for o in cls.tum_odemeler if o.durum == "BAŞARISIZ"]

    @classmethod
    def toplam_tutar(cls):
        return sum(o.tutar for o in cls.tum_odemeler if o.durum == "BAŞARILI")

    @classmethod
    def kullanici_toplam(cls, sahip: str):
        return sum(o.tutar for o in cls.tum_odemeler if getattr(o.odeme_yontemi, "sahip", "") == sahip and o.durum == "BAŞARILI")

    @classmethod
    def son_n_odeme(cls, n: int = 5):
        sirali = sorted(cls.tum_odemeler, key=lambda x: x.tarih, reverse=True)
        return sirali[:n]

    @classmethod
    def odeme_istatistik(cls):
        basarili = len(cls.basarili_odemeler())
        basarisiz = len(cls.basarisiz_odemeler())
        toplam = len(cls.tum_odemeler)
        print(f"Toplam ödemeler: {toplam} | Başarılı: {basarili} | Başarısız: {basarisiz}")

    @classmethod
    def tum_odemeleri_goster(cls):
        for o in cls.tum_odemeler:
            print(f"{o.odeme_id} | {getattr(o.odeme_yontemi,'sahip','')} | {o.tutar} {o.para_birimi} | {o.durum} | {o.tarih}")

    @classmethod
    def aylik_odemeler(cls, ay: int, yil: int):
        return [o for o in cls.tum_odemeler if o.tarih.month == ay and o.tarih.year == yil]

    @classmethod
    def kullanici_aylik_odemeler(cls, sahip: str, ay: int, yil: int):
        return [o for o in cls.aylik_odemeler(ay, yil) if getattr(o.odeme_yontemi, "sahip", "") == sahip]

    @classmethod
    def en_yuksek_odeme(cls):
        if not cls.tum_odemeler:
            return None
        return max(cls.tum_odemeler, key=lambda x: x.tutar)

    @classmethod
    def en_dusuk_odeme(cls):
        if not cls.tum_odemeler:
            return None
        return min(cls.tum_odemeler, key=lambda x: x.tutar)

    @classmethod
    def kullanici_istatistik(cls, sahip: str):
        odemeler = [o for o in cls.tum_odemeler if getattr(o.odeme_yontemi, "sahip", "") == sahip]
        basarili = len([o for o in odemeler if o.durum == "BAŞARILI"])
        basarisiz = len([o for o in odemeler if o.durum == "BAŞARISIZ"])
        toplam = sum(o.tutar for o in odemeler if o.durum == "BAŞARILI")
        print(f"{sahip} - Toplam: {toplam} | Başarılı: {basarili} | Başarısız: {basarisiz}")

    @classmethod
    def tum_odeme_detaylari(cls):
        for o in cls.tum_odemeler:
            print(f"{o.odeme_id} | {getattr(o.odeme_yontemi,'sahip','')} | {o.tutar} {o.para_birimi} | {o.durum} | {o.tarih}")

    @classmethod
    def kullanici_son_n_odeme(cls, sahip: str, n: int = 5):
        odemeler = [o for o in cls.tum_odemeler if getattr(o.odeme_yontemi, "sahip", "") == sahip]
        sirali = sorted(odemeler, key=lambda x: x.tarih, reverse=True)
        return sirali[:n]

    @classmethod
    def tum_odemeleri_dosyaya_yaz(cls, dosya_adi="odemeler.txt"):
        with open(dosya_adi, "w", encoding="utf-8") as f:
            for o in cls.tum_odemeler:
                f.write(f"{o.odeme_id} | {getattr(o.odeme_yontemi,'sahip','')} | {o.tutar} {o.para_birimi} | {o.durum} | {o.tarih}\n")
