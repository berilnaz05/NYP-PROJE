from datetime import timedelta
from implementations.base.ulasim_araci import UlasimAraci


class Otobus(UlasimAraci):
    def __init__(self, arac_id, kapasite, kalkis, bitis,  durum, guzergah, hat_no,kapsam):
        super().__init__(arac_id, kapasite, kalkis, bitis, durum, guzergah,kapsam)
        self.hat_no = hat_no
        self.ucret_kampus_ici=10
        self.ucret_kampus_disi=20

    def sefer_bilgisi(self):
        print("Otobüs güzergahı:".join(self.guzergah))

    def hareket_et(self):
        print("Otobüs hareket ediyor")

    def sefer_baslat(self):
        self.durum = "Seferde"
        self.sefer_arttir()

    def sefer_bitir(self):
        self.sifirla()
        
    def ucret_hesapla(self,tur):
        if tur == "kampüs içi":
            return self.ucret_kampus_ici
        elif tur == "kampüs dışı":
            return self.ucret_kampus_disi
        else:
            return 0

    def bilgi_ver(self):
        return {
            "tip": "Otobüs",
            "arac_id": self.arac_id,
            "durum": self.durum,
            "ucret": self.ucret_hesapla()
        }