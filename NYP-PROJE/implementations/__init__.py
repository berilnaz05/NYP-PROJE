from .base.ulasim_araci import UlasimAraci

class UlasimYoneticisi:

    def __init__(self):
        self.araclar: list[UlasimAraci] = []

    def arac_ekle(self, arac):
        if not isinstance(arac, UlasimAraci):
            raise TypeError("Sadece UlasimAraci türünden nesneler eklenebilir")

        self.araclar.append(arac)

    def arac_sil(self, arac_id):
        for arac in self.araclar:
            if arac.id == arac_id:
                self.araclar.remove(arac)
                return
        raise ValueError("Araç bulunamadı")

    def tum_araclari_listele(self):
        return [arac.bilgi_ver() for arac in self.araclar]

    def sefer_baslat(self, arac_id):
        arac = self._arac_bul(arac_id)
        arac.sefer_baslat()
        arac.hareket_et()

    def sefer_bitir(self, arac_id):
        arac = self._arac_bul(arac_id)
        arac.sefer_bitir()
        
    def toplam_ucret_hesapla(self) :
        return sum(arac.ucret_hesapla() for arac in self.araclar)

    def duruma_gore_listele(self, durum):
        return [
            arac.bilgi_ver()
            for arac in self.araclar
            if arac.durum == durum
        ]

    def tipe_gore_listele(self, tip):
        return [
            arac.bilgi_ver()
            for arac in self.araclar
            if arac.bilgi_ver().get("tip") == tip
        ]

    def arac_sayisi_raporu(self):
        rapor = {}
        for arac in self.araclar:
            tip = arac.bilgi_ver()["tip"]
            rapor[tip] = rapor.get(tip, 0) + 1
        return rapor

    def _arac_bul(self, arac_id) :
        for arac in self.araclar:
            if arac.id == arac_id:
                return arac
        raise ValueError("Araç bulunamadı")
    
    def kapasite_kontrol(self,arac_id,yolcu_sayisi):
        arac =self._arac_bul(arac_id)
        if yolcu_sayisi > arac.kapasite:
            raise ValueError("kapasite aşıldı")
        
    def sefer_baslat(self,arac_id ):
        arac=self._arac_bul(arac_id)
        if arac.durum in ("seferde","kullanımda"):
            raise ValueError("araç zaten çalışıyor")
        arac.sefer_baslat()
        arac.hareket_et()
        
    def sefer_bitir(self,arac_id):
        arac=self._arac_bul(arac_id)
        if arac.durum=="boşta":
            raise ValueError("araç zaten boşta")
        arac.sefer_bitir()
        
    def batarya_kontrol(self,arac_id):
        arac = self._arac_bul(arac_id)
        if hasattr(arac, "bataarya") and arac.batarya <= 5:
            raise ValueError("batarya yetersiz, kullnım engellendi")
        
    def max_ücret_kontrol(self,max_ucret):
        for arac in self.araclar:
            if arac.ucret_hesapla() > max_ucret:
                raise ValueError(f"{arac.bilgi_ver() ['tip']} için ücret sınırı aşıldı")
class UlasimYoneticisi:
    def __init__(self):
        self.araclar=[]
        self.sefer_gecmisi=[]
        
    def toplam_gelir(self):
         return sum(kayit["ucret"] for kayit in self.sefer_gecmisi)

    def en_cok_kullanilan_tip(self):
         sayac = {}
         for kayit in self.sefer_gecmisi:
            tip = kayit["tip"]
            sayac[tip] = sayac.get(tip, 0) + 1
            return max(sayac, key=sayac.get) if sayac else None
    def arac_ekle(self, arac):
         if any(a.id == arac.arac_id for a in self.araclar):
            raise ValueError("Bu ID ile araç zaten var")
            self.araclar.append(arac)