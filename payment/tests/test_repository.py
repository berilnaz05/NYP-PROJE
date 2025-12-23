import unittest
from datetime import datetime
from payment.base import OdemeYontemi
from payment.credit_card import KrediKartiOdeme
from payment.cash import NakitOdeme
from payment.wallet import DijitalCuzdanOdeme
from payment.repositories.odeme_repository import OdemeRepository
from payment.repositories.odeme_yontemi_repository import OdemeYontemiRepository
from payment.services.odeme_service import OdemeService

class TestOdemeRepository(unittest.TestCase):

    def setUp(self):
        OdemeRepository.temizle()
        self.kart = KrediKartiOdeme("Ali", 1000, "1234567812345678", "12/30", "123")
        self.nakit = NakitOdeme("Veli", "TL", 500)
        self.cuzdan = DijitalCuzdanOdeme("Ayşe", 300, "TL", "Cuzdan1", True)
        self.odeme1 = OdemeService.odeme_olustur(self.kart, 200)
        self.odeme2 = OdemeService.odeme_olustur(self.nakit, 100)
        self.odeme3 = OdemeService.odeme_olustur(self.cuzdan, 50)
        OdemeRepository.kaydet(self.odeme1)
        OdemeRepository.kaydet(self.odeme2)
        OdemeRepository.kaydet(self.odeme3)

    def test_listele(self):
        liste = OdemeRepository.listele()
        self.assertEqual(len(liste), 3)

    def test_basarili_odemeler(self):
        basarili = OdemeRepository.basarili_odemeler()
        self.assertTrue(all(o["durum"] == "BAŞARILI" for o in basarili))

    def test_toplam_tutar(self):
        toplam = OdemeRepository.toplam_tutar()
        self.assertGreaterEqual(toplam, 350)

    def test_son_n_odeme(self):
        son2 = OdemeRepository.son_n_odeme(2)
        self.assertEqual(len(son2), 2)
        self.assertEqual(son2[-1]["odeme_id"], self.odeme3.odeme_id)

    def test_fis_id_ile_iade(self):
        fis_id = self.odeme1.odeme_id
        result = OdemeRepository.iade(fis_id)
        self.assertTrue(result)
        odeme = next(o for o in OdemeRepository.listele() if o["odeme_id"] == fis_id)
        self.assertEqual(odeme["durum"], "Iade Edildi")


class TestOdemeYontemiRepository(unittest.TestCase):

    def setUp(self):
        OdemeYontemiRepository.temizle()
        self.kart = KrediKartiOdeme("Mehmet", 1000, "8765432187654321", "11/29", "321")
        self.nakit = NakitOdeme("Fatma", "TL", 500)
        self.cuzdan = DijitalCuzdanOdeme("Ahmet", 300, "TL", "Cuzdan2", True)
        OdemeYontemiRepository.kaydet(self.kart)
        OdemeYontemiRepository.kaydet(self.nakit)
        OdemeYontemiRepository.kaydet(self.cuzdan)

    def test_listele(self):
        liste = OdemeYontemiRepository.listele()
        self.assertEqual(len(liste), 3)

    def test_bul_ve_pasif_yap(self):
        id_bulunan = OdemeYontemiRepository.listele()[0]["id"]
        yontem = OdemeYontemiRepository.bul(id_bulunan)
        self.assertIsNotNone(yontem)
        OdemeYontemiRepository.pasif_yap(id_bulunan)
        updated = OdemeYontemiRepository.bul(id_bulunan)
        self.assertEqual(updated["durum"], "PASIF")

    def test_toplam_bakiye(self):
        toplam = OdemeYontemiRepository.toplam_bakiye()
        self.assertGreaterEqual(toplam, 0)

    def test_sahip_ile_listele(self):
        liste = OdemeYontemiRepository.sahip_ile_listele("Mehmet")
        self.assertTrue(all(o["sahip"] == "Mehmet" for o in liste))

    def test_bakiyeye_gore_sirala(self):
        sorted_list = OdemeYontemiRepository.bakiyeye_gore_sirala()
        self.assertTrue(sorted_list[0]["bakiye"] <= sorted_list[-1]["bakiye"])

if __name__ == "__main__":
    unittest.main()
