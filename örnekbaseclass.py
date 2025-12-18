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

class MenuServisi:
  def __init__(self):
   self.menu = {
      "Hamburger": 80,
      "Pizza": 120,
      "Kola": 30
    }

def menu_listele(self):
  return self.menu

class SiparisServisi:
  def toplam_tutar_hesapla(self, secilen_urunler, menu):
    return sum(menu[urun] for urun in secilen_urunler)(menu[item] for item in selected_items)
  
class OdemeRepository:
  def __init__(self):
    self.odemeler = []  


def kaydet(self, sahip, tutar, yontem):
  self.odemeler.append({
  "sahip": sahip,
  "tutar": tutar,
  "yontem": yontem,
  "tarih": datetime.now()
  })


def tumunu_listele(self):
  return self.odemeler


def sahibe_gore_filtrele(self, sahip):
  return [o for o in self.odemeler if o["sahip"] == sahip]

# === TEST / ÇALIŞTIRMA KODU ===

menu_servisi = MenuServisi()
siparis_servisi = SiparisServisi()
repo = OdemeRepository()

menu = menu_servisi.menu_listele()
secilen_urunler = ["Hamburger", "Kola"]

toplam_tutar = siparis_servisi.toplam_tutar_hesapla(secilen_urunler, menu)

odeme = KrediKartiOdeme("Beril", 200, "1234-5678")

if odeme.ode(toplam_tutar):
    repo.kaydet(odeme.sahip, toplam_tutar, "Kredi Kartı")
    print("Ödeme başarılı")
else:
    print("Yetersiz bakiye")
