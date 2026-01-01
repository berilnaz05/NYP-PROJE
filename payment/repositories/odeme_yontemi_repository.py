
import json
from datetime import datetime
from glob import glob

class OdemeRepository:

    @staticmethod
    def kaydet(odeme_model: OdemeModel):
        data = {
            "odeme_id": odeme_model.odeme_id,
            "sahip": getattr(odeme_model.odeme_yontemi, "sahip", None),
            "tutar": odeme_model.tutar,
            "para_birimi": odeme_model.para_birimi,
            "tarih": odeme_model.tarih.isoformat(),
            "durum": odeme_model.durum,
            "tip": odeme_model.odeme_yontemi.__class__.__name__
        }
        with open(f"odeme_{odeme_model.odeme_id}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def listele():
        tum_dosyalar = glob("odeme_*.json")
        tum_veriler = []
        for dosya in tum_dosyalar:
            with open(dosya, "r", encoding="utf-8") as f:
                tum_veriler.append(json.load(f))
        return tum_veriler

    @staticmethod
    def bul(odeme_id: str):
        try:
            with open(f"odeme_{odeme_id}.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return None

    @staticmethod
    def guncelle(odeme_model: OdemeModel):
        OdemeRepository.kaydet(odeme_model)

    @staticmethod
    def basarili_odemeler():
        return [o for o in OdemeRepository.listele() if o.get("durum") == "BAŞARILI"]

    @staticmethod
    def basarisiz_odemeler():
        return [o for o in OdemeRepository.listele() if o.get("durum") == "BAŞARISIZ"]

    @staticmethod
    def toplam_tutar():
        return sum(o.get("tutar",0) for o in OdemeRepository.basarili_odemeler())

    @staticmethod
    def kullanici_toplam(sahip: str):
        return sum(o.get("tutar",0) for o in OdemeRepository.basarili_odemeler() if o.get("sahip") == sahip)

    @staticmethod
    def son_n_odeme(n=5):
        liste = sorted(OdemeRepository.listele(), key=lambda x: x["tarih"], reverse=True)
        return liste[:n]

    @staticmethod
    def aylik_odemeler(ay: int, yil: int):
        return [o for o in OdemeRepository.listele() if datetime.fromisoformat(o["tarih"]).month == ay and datetime.fromisoformat(o["tarih"]).year == yil]

    @staticmethod
    def kullanici_aylik_odemeler(sahip: str, ay: int, yil: int):
        return [o for o in OdemeRepository.aylik_odemeler(ay, yil) if o.get("sahip") == sahip]

    @staticmethod
    def en_yuksek_odeme():
        liste = OdemeRepository.listele()
        if not liste:
            return None
        return max(liste, key=lambda x: x.get("tutar",0))

    @staticmethod
    def en_dusuk_odeme():
        liste = OdemeRepository.listele()
        if not liste:
            return None
        return min(liste, key=lambda x: x.get("tutar",0))

    @staticmethod
    def dosyaya_yaz(dosya_adi="odemeler.json"):
        tum_veri = OdemeRepository.listele()
        with open(dosya_adi, "w", encoding="utf-8") as f:
            json.dump(tum_veri, f, indent=4)
