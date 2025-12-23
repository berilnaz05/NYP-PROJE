from typing import List

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
