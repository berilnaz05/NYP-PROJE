from datetime import timedelta
from implementations.base.ulasim_araci import UlasimAraci
        
class Scooter(UlasimAraci):
    def __init__(self, arac_id, kalkis, bitis,  durum, guzergah,elektrikli,batarya, dakika_ucreti,kapsam):
        self.batarya=batarya
        self.arac_id=arac_id
        self.kalkis=kalkis
        self.kapsam=kapsam
        self.bitis=bitis
        self.durum=durum
        self.guzergah=guzergah
        self.elektrikli = elektrikli
        self.dakika_ucreti=dakika_ucreti
        self.kullanilan_dakika=0
        self.mesafe_km = 0

    def sefer_bilgisi(self):
        print("Scooter kullanımda")

    def hareket_et(self):
        print("Scooter hareket ediyor")

    def sefer_baslat(self):
        self.durum = "Kullanımda"
        self.sefer_arttir()

    def sefer_bitir(self):
        self.sifirla()
        self.kullanilan_dakika = 0

    def sure_ekle(self, dakika):
        self.kullanilan_dakika += dakika

    def ucret_hesapla(self):
        return self.kullanilan_dakika * self.dakika_ucreti

    def tahmini_sure(self):
        return timedelta(minutes=20)

    def bilgi_ver(self):
        return {
            "tip": "Scooter",
            "arac_id": self.arac_id,
            "durum": self.durum,
            "ucret": self.ucret_hesapla()
        }