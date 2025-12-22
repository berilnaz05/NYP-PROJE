from abc import ABC, abstractmethod

class OdemeYontemi(ABC):
    def __init__(self, tutar, sahip, bakiye, para_birimi="TL"):
        self.tutar = tutar
        self.sahip = sahip
        self.bakiye = bakiye
        self.para_birimi = para_birimi

    @abstractmethod
    def yetkilendir(self, tutar):
        pass

    def ode(self, tutar):
        if self.yetkilendir(tutar):
            self.bakiye -= tutar
            return True
        return False
