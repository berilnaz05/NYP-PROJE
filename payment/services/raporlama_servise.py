from datetime import datetime
from typing import List, Dict

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
