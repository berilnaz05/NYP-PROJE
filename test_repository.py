import unittest
from payment.repositories.odeme_repository import OdemeRepository
from payment.repositories.odeme_yontemi_repository import OdemeYontemiRepository
from payment.models.odeme_yontemi_model import OdemeYontemiModel


class TestRepositoryler(unittest.TestCase):

    def test_odeme_kaydetme(self):
        repo = OdemeRepository()

        odeme = repo.odeme_kaydet(
            kullanici="Beril",
            tutar=150,
            odeme_tipi="KrediKartiOdeme"
        )

        self.assertEqual(odeme.kullanici, "Beril")
        self.assertEqual(len(repo.tum_odemeleri_listele()), 1)

    def test_kullaniciya_gore_filtreleme(self):
        repo = OdemeRepository()

        repo.odeme_kaydet("Beril", 100, "NakitOdeme")
        repo.odeme_kaydet("Ahmet", 200, "KrediKartiOdeme")

        sonuc = repo.kullaniciya_gore_filtrele("Beril")

        self.assertEqual(len(sonuc), 1)
        self.assertEqual(sonuc[0].kullanici, "Beril")

    def test_odeme_yontemi_repository(self):
        repo = OdemeYontemiRepository()

        yontem = OdemeYontemiModel(
            yontem_id="1",
            kullanici="Beril",
            yontem_adi="Kredi Kartı"
        )

        repo.ekle(yontem)

        self.assertEqual(len(repo.tum_yontemleri_listele()), 1)
        self.assertEqual(len(repo.kullaniciya_ait_yontemler("Beril")), 1)

        repo.pasif_yap("1")
        self.assertEqual(len(repo.kullaniciya_ait_yontemler("Beril")), 0)


if __name__ == "__main__":
    unittest.main()
