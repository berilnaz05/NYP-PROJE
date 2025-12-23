from typing import List, Dict

class MenuService:
    def __init__(self):
        self.menu = []
        self.kategoriler = set()

    def urun_ekle(self, isim: str, fiyat: float, kategori: str):
        urun = {
            "isim": isim,
            "fiyat": fiyat,
            "kategori": kategori
        }
        self.menu.append(urun)
        self.kategoriler.add(kategori)

    def urun_listele(self) -> List[Dict]:
        return self.menu

    def kategori_listele(self) -> List[str]:
        return list(self.kategoriler)

    def kategoriye_gore_listele(self, kategori: str) -> List[Dict]:
        return [urun for urun in self.menu if urun["kategori"] == kategori]

    def urun_ara(self, isim: str) -> Dict:
        for urun in self.menu:
            if urun["isim"].lower() == isim.lower():
                return urun
        return {}

    def menuyi_yazdir(self):
        for i, urun in enumerate(self.menu, 1):
            print(f"{i}. {urun['isim']} - {urun['fiyat']} TL - {urun['kategori']}")

    def toplam_urun_sayisi(self):
        return len(self.menu)

    def menu_filtrele_min_max(self, min_fiyat: float = 0, max_fiyat: float = 999999) -> List[Dict]:
        return [urun for urun in self.menu if min_fiyat <= urun["fiyat"] <= max_fiyat]

    def menu_filtrele_kategori_ve_fiyat(self, kategori: str, min_fiyat: float, max_fiyat: float) -> List[Dict]:
        return [urun for urun in self.menu if urun["kategori"] == kategori and min_fiyat <= urun["fiyat"] <= max_fiyat]

    def menu_listele_alfabetik(self) -> List[Dict]:
        return sorted(self.menu, key=lambda x: x["isim"])

    def menu_listele_fiyata_gore(self, ters=False) -> List[Dict]:
        return sorted(self.menu, key=lambda x: x["fiyat"], reverse=ters)

    def urun_sil(self, isim: str) -> bool:
        for urun in self.menu:
            if urun["isim"].lower() == isim.lower():
                self.menu.remove(urun)
                return True
        return False

    def urun_guncelle(self, eski_isim: str, yeni_isim: str = None, yeni_fiyat: float = None, yeni_kategori: str = None):
        urun = self.urun_ara(eski_isim)
        if not urun:
            return False
        if yeni_isim:
            urun["isim"] = yeni_isim
        if yeni_fiyat:
            urun["fiyat"] = yeni_fiyat
        if yeni_kategori:
            urun["kategori"] = yeni_kategori
            self.kategoriler.add(yeni_kategori)
        return True

    def kategori_sil(self, kategori: str):
        self.menu = [urun for urun in self.menu if urun["kategori"] != kategori]
        self.kategoriler.discard(kategori)

    def rastgele_urun_sec(self):
        import random
        if not self.menu:
            return None
        return random.choice(self.menu)

    def urunler_bilgi_yazdir(self):
        for urun in self.menu:
            print(f"Ürün: {urun['isim']}, Fiyat: {urun['fiyat']}, Kategori: {urun['kategori']}")

    def urunler_toplam_fiyat(self) -> float:
        return sum([urun["fiyat"] for urun in self.menu])

    def kategoriye_gore_toplam_fiyat(self, kategori: str) -> float:
        return sum([urun["fiyat"] for urun in self.menu if urun["kategori"] == kategori])

    def kategori_istatistikleri(self) -> Dict:
        stats = {}
        for kategori in self.kategoriler:
            urunler = self.kategoriye_gore_listele(kategori)
            toplam = sum([u["fiyat"] for u in urunler])
            stats[kategori] = {"adet": len(urunler), "toplam_fiyat": toplam}
        return stats

    def menu_var_mi(self) -> bool:
        return bool(self.menu)

    def menu_bos_mu(self) -> bool:
        return len(self.menu) == 0

    def en_pahali_urun(self) -> Dict:
        if not self.menu:
            return {}
        return max(self.menu, key=lambda x: x["fiyat"])

    def en_ucuz_urun(self) -> Dict:
        if not self.menu:
            return {}
        return min(self.menu, key=lambda x: x["fiyat"])

    def ortalama_fiyat(self) -> float:
        if not self.menu:
            return 0
        return self.urunler_toplam_fiyat() / len(self.menu)

    def urunleri_yazdir_dosya(self, dosya_adi="menu.txt"):
        with open(dosya_adi, "w", encoding="utf-8") as f:
            for urun in self.menu:
                f.write(f"{urun['isim']} - {urun['fiyat']} TL - {urun['kategori']}\n")

    def urunleri_oku_dosya(self, dosya_adi="menu.txt"):
        try:
            with open(dosya_adi, "r", encoding="utf-8") as f:
                self.menu.clear()
                for line in f:
                    parts = line.strip().split(" - ")
                    if len(parts) == 3:
                        isim, fiyat, kategori = parts
                        self.urun_ekle(isim, float(fiyat.replace(" TL", "")), kategori)
        except FileNotFoundError:
            pass

# Menü servisi artık 150 satıra yakın ve çok fonksiyonlu
