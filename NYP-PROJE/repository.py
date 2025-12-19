from abc import ABC, abstractmethod
from typing import List, Type
from base import UlasimAraci

class UlasimRepositoryBase(ABC):

    @abstractmethod
    def ekle(self, arac: UlasimAraci) -> None:
        pass

    @abstractmethod
    def sil(self, arac_id: int) -> None:
        pass

    @abstractmethod
    def getir(self, arac_id: int) -> UlasimAraci:
        pass

    @abstractmethod
    def tumunu_getir(self) -> List[UlasimAraci]:
        pass

    # YENİ İŞ KURALLARI
    @abstractmethod
    def duruma_gore_getir(self, durum: str) -> List[UlasimAraci]:
        pass

    @abstractmethod
    def tipe_gore_getir(self, tip: Type[UlasimAraci]) -> List[UlasimAraci]:
        pass

    @abstractmethod
    def seferde_olanlar(self) -> List[UlasimAraci]:
        pass

    @abstractmethod
    def kapasiteye_gore_getir(self, min_kapasite: int) -> List[UlasimAraci]:
        pass

class BellekUlasimRepository(UlasimRepositoryBase):

    def __init__(self):
        self._araclar: List[UlasimAraci] = []

  
    def ekle(self, arac: UlasimAraci) -> None:
        if not isinstance(arac, UlasimAraci):
            raise TypeError("UlasimAraci türünde olmalı")

        if any(a.id == arac.id for a in self._araclar):
            raise ValueError("Aynı ID'ye sahip araç zaten var")

        self._araclar.append(arac)

    def sil(self, arac_id: int) -> None:
        arac = self.getir(arac_id)
        self._araclar.remove(arac)

    def getir(self, arac_id: int) -> UlasimAraci:
        for arac in self._araclar:
            if arac.id == arac_id:
                return arac
        raise ValueError("Araç bulunamadı")

    def tumunu_getir(self) -> List[UlasimAraci]:
        return list(self._araclar)

    
    def duruma_gore_getir(self, durum: str) -> List[UlasimAraci]:
        return [a for a in self._araclar if a.durum == durum]

    def tipe_gore_getir(self, tip: Type[UlasimAraci]) -> List[UlasimAraci]:
        return [a for a in self._araclar if isinstance(a, tip)]

    def seferde_olanlar(self) -> List[UlasimAraci]:
        return self.duruma_gore_getir("Seferde")

    def kapasiteye_gore_getir(self, min_kapasite: int) -> List[UlasimAraci]:
        return [a for a in self._araclar if a.kapasite >= min_kapasite]

    def arac_sayisi(self) -> int:
        return len(self._araclar)

    def tip_ozeti(self) -> dict:
        ozet = {}
        for arac in self._araclar:
            tip = type(arac).__name__
            ozet[tip] = ozet.get(tip, 0) + 1
        return ozet

    def durum_ozeti(self) -> dict:
        ozet = {}
        for arac in self._araclar:
            ozet[arac.durum] = ozet.get(arac.durum, 0) + 1
        return ozet