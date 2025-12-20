from typing import List
from base.ulasim_araci import UlasimAraci


class UlasimRepository:
    def __init__(self):
        self._araclar: List[UlasimAraci] = []

    def ekle(self, arac: UlasimAraci):
        if any(a.arac_id == arac.arac_id for a in self._araclar):
            raise ValueError("Bu ID ile araç zaten var")
        self._araclar.append(arac)

  
    def bul_id_ile(self, arac_id: int) -> UlasimAraci:
        for arac in self._araclar:
            if arac.arac_id == arac_id:
                return arac
        raise ValueError("Araç bulunamadı")

    def tumunu_getir(self) -> List[UlasimAraci]:
        return list(self._araclar)

    def duruma_gore(self, durum: str) -> List[UlasimAraci]:
        return [a for a in self._araclar if a.durum == durum]

    def bos_koltuk_en_az(self, min_bos: int) -> List[UlasimAraci]:
        return [
            a for a in self._araclar
            if (a.kapasite - a.aktif_yolcu) >= min_bos
        ]