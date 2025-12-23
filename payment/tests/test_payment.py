import unittest
from payment.base import (
    KrediKartiOdeme,
    NakitOdeme,
    DijitalCuzdanOdeme
)


class TestOdemeYontemleri(unittest.TestCase):

    def test_kredi_karti_basarili_odeme(self):
        kk = KrediKartiOdeme(
            tutar=0,
            sahip="Beril",
            bakiye=500,
            kart_numarasi="1234567812345678",
            son_kullanma_tarihi="12/26",
            cvv="123"
        )

        sonuc = kk.ode(200)

        self.assertTrue(sonuc)
        self.assertEqual(kk.bakiye, 300)

    def test_kredi_karti_yetersiz_bakiye(self):
        kk = KrediKartiOdeme(
            tutar=0,
            sahip="Beril",
            bakiye=100,
            kart_numarasi="1234567812345678",
            son_kullanma_tarihi="12/26",
            cvv="123"
        )

        sonuc = kk.ode(200)

        self.assertFalse(sonuc)
        self.assertEqual(kk.bakiye, 100)

    def test_nakit_odeme(self):
        nakit = NakitOdeme(
            verilen_nakit=300,
            sahip="Beril",
            bakiye=300
        )

        sonuc = nakit.ode(150)

        self.assertTrue(sonuc)
        self.assertEqual(nakit.bakiye, 150)

    def test_dijital_cuzdan_dogrulanmamis(self):
        cuzdan = DijitalCuzdanOdeme(
            tutar=0,
            sahip="Beril",
            bakiye=300,
            cuzdan_adi="PayBeril",
            dogrulanmis=False
        )

        sonuc = cuzdan.ode(100)

        self.assertFalse(sonuc)
        self.assertEqual(cuzdan.bakiye, 300)

    def test_dijital_cuzdan_basarili(self):
        cuzdan = DijitalCuzdanOdeme(
            tutar=0,
            sahip="Beril",
            bakiye=300,
            cuzdan_adi="PayBeril",
            dogrulanmis=True
        )

        sonuc = cuzdan.ode(100)

        self.assertTrue(sonuc)
        self.assertEqual(cuzdan.bakiye, 200)


if __name__ == "__main__":
    unittest.main()
