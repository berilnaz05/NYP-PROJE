from dataclasses import dataclass,field
from typing import List,Optional,callable
from enum import Enum
class Cinsiyet(Enum):
    ERKEK="Erkek"
    KADIN="Kadın"
    DIGER="Diğer"
class Durum(Enum):
    AKTIF="Aktif"
    TABURCU="Taburcu"
    BEKLEMEDE="Beklemede"
    ACIL="Acil"
    @dataclass
    class Patient:
        #temel hasta sınıfı (base class)
        tc=int
        ad=str
        yas=int
        cinsiyet=Cinsiyet
        durum:Durum=Durum.AKTIF
        notlar:List[str]=field(default_factory= List)
        def ek_not(self,metin:str) -> None:
            #hasta kaydına açıklama /yorum ekler. 
            self.notlar.append(metin)
        def durum_guncelle(self,yeni_durum:Durum) -> None:
            #hastanın durumunu günceller
            self.durum=yeni_durum
        def ozet(self)-> str:
            #hasta kısa özetini döndürür
            return f"[{self.tc}] {self.ad}| {self.yas}| {self.cinsiyet.value} |Durum:{self.durum.value}"