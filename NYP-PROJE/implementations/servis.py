from base.ulasim_araci import UlasimAraci
from ..repository import UlasimRepository


class Servis(UlasimAraci):
    def __init__(self, repo):
         self.repo=repo
        
    def yeni_arac_ekle(self, arac):
        self.repo.ekle(arac)

  
    def sefer_baslat(self, arac_id):
        arac = self.repo.bul_id_ile(arac_id)
        if arac.durum != "Boşta":
            raise ValueError("Araç zaten seferde veya kullanımda")
        arac.sefer_baslat()
        arac.hareket_et()

    def sefer_bitir(self, arac_id):
        arac = self.repo.bul_id_ile(arac_id)
        arac.sefer_bitir()

   
    def kapasite_kontrol(self, arac_id, yolcu_sayisi):
        arac = self.repo.bul_id_ile(arac_id)
        if arac.aktif_yolcu + yolcu_sayisi > arac.kapasite:
            raise ValueError("Kapasite aşıldı")

  
    def bilet_rezervasyonu(self, arac_id, adet = 1):
        arac = self.repo.bul_id_ile(arac_id)
        if not arac.yolcu_ekle(adet):
            raise ValueError("Yeterli boş koltuk yok")

   
    def arac_durumu(self, arac_id) :
        arac = self.repo.bul_id_ile(arac_id)
        return {
            "arac_id": arac.arac_id,
            "durum": arac.durum,
            "kapasite": arac.kapasite,
            "aktif_yolcu": arac.aktif_yolcu,
            "bos_koltuk": arac.kapasite - arac.aktif_yolcu
        }