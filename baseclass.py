from abc import ABC, abstractmethod
from datetime import datetime


class OdemeYontemi(ABC):
  def __init__(self, sahip, bakiye, para_birimi="TRY"):
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
  
class KrediKartiOdeme(OdemeYontemi):
  def __init__(self, sahip, limit, kart_numarasi):
    super().__init__(sahip, limit)
    self.kart_numarasi = kart_numarasi


def yetkilendir(self, tutar):
  return tutar <= self.bakiye

class NakitOdeme(OdemeYontemi):
  def yetkilendir(self, tutar):
    return tutar <= self.bakiye
  
class OnlineCuzdanOdeme(OdemeYontemi):
  def __init__(self, sahip, bakiye, cuzdan_adi, dogrulanmis=False):
    super().__init__(sahip, bakiye)
    self.cuzdan_adi = cuzdan_adi
    self.dogrulanmis = dogrulanmis


def yetkilendir(self, tutar):
  return self.dogrulanmis and tutar <= self.bakiye