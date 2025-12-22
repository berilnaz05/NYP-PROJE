# BASE CLASS
from abc import ABC, abstractmethod
from datetime import datetime
import uuid

# Ödeme Yöntemi
class OdemeYontemi(ABC):
    def __init__(
        self,
        tutar,
        sahip,
        bakiye,
        para_birimi="TL",
        dogrulanmis=False,
        kart_numarasi=None,
        son_kullanma_tarihi=None,
        cvv=None,
        verilen_nakit=None,
        cuzdan_adi=None,

    ):
        self.tutar = tutar
        self.sahip = sahip
        self.bakiye = bakiye
        self.para_birimi = para_birimi
        self.dogrulanmis = dogrulanmis
        self.kart_numarasi = kart_numarasi
        self.son_kullanma_tarihi = son_kullanma_tarihi
        self.cvv = cvv
        self.verilen_nakit = verilen_nakit
        self.cuzdan_adi = cuzdan_adi
       
    @abstractmethod
    def yetkilendir(self, tutar):
        pass

    def ode(self, tutar):
        if self.yetkilendir(tutar):
            return True
        return False

    def bilgi(self, tutar):
        if self.bakiye >= tutar:
            print(f"{self.sahip} adlı kullanıcının bakiyesi yeterlidir.")
        else:
            print(f"{self.sahip} adlı kullanıcının bakiyesi yetersizdir.")

