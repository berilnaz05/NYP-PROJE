from typing import List, Dict
from .menu_service import MenuService
from datetime import datetime

class SiparisService:
    def __init__(self, menu_service: MenuService):
        self.menu_service = menu_service
        self.siparisler: List[Dict] = []

    def siparis_olustur(self, kullanici: str, urun_isimleri: List[str]) -> Dict:
        siparis = {
            "kullanici": kullanici,
            "urunler": [],
            "toplam_tutar": 0,
            "tarih": datetime.now(),
            "siparis_id": None
        }

        toplam = 0
        for isim in urun_isimleri:
            urun = self.menu_service.urun_ara(isim)
            if urun:
                siparis["urunler"].append(urun)
                toplam += urun["fiyat"]
        siparis["toplam_tutar"] = toplam
        siparis["siparis_id"] = f"SIP-{len(self.siparisler)+1}"
        self.siparisler.append(siparis)
        return siparis

    def siparis_listele(self, kullanici: str = None) -> List[Dict]:
        if kullanici:
            return [s for s in self.siparisler if s["kullanici"] == kullanici]
        return self.siparisler

    def toplam_tutar_hesapla(self, siparis_id: str) -> float:
        for s in self.siparisler:
            if s["siparis_id"] == siparis_id:
                return s["toplam_tutar"]
        return 0

    def siparis_goster(self, siparis_id: str):
        for s in self.siparisler:
            if s["siparis_id"] == siparis_id:
                print(f"Sipariş ID: {s['siparis_id']}")
                print(f"Kullanıcı: {s['kullanici']}")
                print(f"Tarih: {s['tarih']}")
                print("Ürünler:")
                for u in s["urunler"]:
                    print(f"  {u['isim']} - {u['fiyat']} TL - {u['kategori']}")
                print(f"Toplam: {s['toplam_tutar']} TL")
                return
        print("Sipariş bulunamadı.")

    def siparis_sil(self, siparis_id: str) -> bool:
        for s in self.siparisler:
            if s["siparis_id"] == siparis_id:
                self.siparisler.remove(s)
                return True
        return False

    def siparisleri_kaydet(self, dosya_adi="siparisler.txt"):
        with open(dosya_adi, "w", encoding="utf-8") as f:
            for s in self.siparisler:
                urunler_str = ", ".join([u["isim"] for u in s["urunler"]])
                f.write(f"{s['siparis_id']} | {s['kullanici']} | {urunler_str} | {s['toplam_tutar']} TL | {s['tarih']}\n")

    def siparisleri_oku(self, dosya_adi="siparisler.txt"):
        try:
            with open(dosya_adi, "r", encoding="utf-8") as f:
                self.siparisler.clear()
                for line in f:
                    parts = line.strip().split(" | ")
                    if len(parts) == 5:
                        siparis_id, kullanici, urunler_str, toplam_tutar, tarih_str = parts
                        urunler = [{"isim": isim} for isim in urunler_str.split(", ")]
                        self.siparisler.append({
                            "siparis_id": siparis_id,
                            "kullanici": kullanici,
                            "urunler": urunler,
                            "toplam_tutar": float(toplam_tutar.replace(" TL","")),
                            "tarih": datetime.strptime(tarih_str, "%Y-%m-%d %H:%M:%S.%f")
                        })
        except FileNotFoundError:
            pass

    def rastgele_siparis_olustur(self, kullanici: str, adet: int = 3):
        import random
        if self.menu_service.menu_bos_mu():
            print("Menü boş. Sipariş oluşturulamıyor.")
            return None
        urunler = [self.menu_service.rastgele_urun_sec()["isim"] for _ in range(adet)]
        return self.siparis_olustur(kullanici, urunler)

    def toplam_siparis_sayisi(self) -> int:
        return len(self.siparisler)

    def kullanici_toplam_harcama(self, kullanici: str) -> float:
        return sum([s["toplam_tutar"] for s in self.siparisler if s["kullanici"] == kullanici])

    def en_yuksek_tutarli_siparis(self):
        if not self.siparisler:
            return None
        return max(self.siparisler, key=lambda x: x["toplam_tutar"])

    def en_dusuk_tutarli_siparis(self):
        if not self.siparisler:
            return None
        return min(self.siparisler, key=lambda x: x["toplam_tutar"])

    def siparisleri_listele_dosyaya(self, dosya_adi="siparis_rapor.txt"):
        with open(dosya_adi, "w", encoding="utf-8") as f:
            for s in self.siparisler:
                urunler_str = ", ".join([u["isim"] for u in s["urunler"]])
                f.write(f"{s['siparis_id']} | {s['kullanici']} | {urunler_str} | {s['toplam_tutar']} TL | {s['tarih']}\n")
