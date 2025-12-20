from datetime import timedelta
from implementations.base.ulasim_araci import UlasimAraci
        
class Bisiklet(UlasimAraci):
    def __init__(self, arac_id,  kalkis, bitis,  durum, guzergah,elektrikli,batarya, km_ucreti,kapsam):
        self.arac_id=arac_id
        self.kalkis=kalkis
        self.bitis=bitis
        self.durum=durum
        self.batarya=batarya
        self.guzergah=guzergah
        self.elektrikli = elektrikli
        self.km_ucreti = km_ucreti
        self.kullanilan_dakika=0
        self.mesafe_km = 0

    def sefer_bilgisi(self):
        print("Bisiklet kullanımda")

    def hareket_et(self):
        print("Bisiklet hareket ediyor")

    def sefer_baslat(self):
        self.durum = "Kullanımda"

    def sefer_bitir(self):
        self.sifirla()
        self.kullanilan_dakika = 0

    def sure_ekle(self, dakika):
        self.kullanilan_dakika += dakika

    def ucret_hesapla(self):
        return self.kullanilan_dakika * (1.5 if self.elektrikli else 0.5)

    def tahmini_sure(self):
        return timedelta(minutes=30)

    def bilgi_ver(self):
        return {
            "tip": "Bisiklet",
            "arac_id": self.arac_id,
            "durum": self.durum,
            "ucret": self.ucret_hesapla()
        }