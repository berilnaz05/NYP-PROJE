import unittest
from datetime import datetime
from payment.base import OdemeYontemi
from payment.credit_card import KrediKartiOdeme
from payment.cash import NakitOdeme
from payment.wallet import DijitalCuzdanOdeme
from payment.services.odeme_service import OdemeService
from payment.repositories.odeme_repository import OdemeRepository
from payment.repositories.odeme_yontemi_repository import OdemeYontemiRepository

class TestOdemeYontemi(unittest.TestCase):

    def setUp(self):
        self.kart = KrediKartiOdeme("Ali", 1000, "1234567812345678", "12/30", "123")
        self.nakit = NakitOdeme("Veli", "TL", 500)
        self.cuzdan = DijitalCuzdanOdeme("Ayşe", 300, "TL", "Hesap1", True)

    def test_kredi_karti_odeme_basari(self):
        sonuc = self.kart.ode(200)
        self.assertTrue(sonuc)
        self.assertEqual(self.kart.bakiye, 800)

    def test_kredi_karti_odeme_yetersiz_bakiye(self):
        sonuc = self.kart.ode(1200)
        self.assertFalse(sonuc)
        self.assertEqual(self.kart.bakiye, 1000)

    def test_nakit_odeme_basari(self):
        sonuc = self.nakit.ode(300)
        self.assertTrue(sonuc)
        self.assertEqual(self.nakit.bakiye, 200)

    def test_nakit_odeme_yetersiz(self):
        sonuc = self.nakit.ode(600)
        self.assertFalse(sonuc)
        self.assertEqual(self.nakit.bakiye, 500)

    def test_cuzdan_odeme_dogrulanmamis(self):
        self.cuzdan.dogrulanmis = False
        sonuc = self.cuzdan.ode(100)
        self.assertFalse(sonuc)
        self.assertEqual(self.cuzdan.bakiye, 300)

    def test_cuzdan_odeme_basari(self):
        sonuc = self.cuzdan.ode(150)
        self.assertTrue(sonuc)
        self.assertEqual(self.cuzdan.bakiye, 150)

    def test_yetkilendir_fonksiyonlari(self):
        self.assertTrue(self.kart.yetkilendir(500))
        self.assertFalse(self.kart.yetkilendir(2000))
        self.assertTrue(self.nakit.yetkilendir(200))
        self.assertFalse(self.nakit.yetkilendir(800))
        self.assertTrue(self.cuzdan.yetkilendir(100))
        self.cuzdan.dogrulanmis = False
        self.assertFalse(self.cuzdan.yetkilendir(100))


class TestOdemeRepository(unittest.TestCase):

    def setUp(self):
        self.kart = KrediKartiOdeme("Ali", 1000, "1234567812345678", "12/30", "123")
        self.odeme_model = OdemeService.odeme_olustur(self.kart, 200)
        OdemeRepository.temizle()

    def test_odeme_kaydet_ve_listele(self):
        OdemeRepository.kaydet(self.odeme_model)
        tum_odemeler = OdemeRepository.listele()
        self.assertTrue(any(o["odeme_id"] == self.odeme_model.odeme_id for o in tum_odemeler))

    def test_odeme_basarili_filtresi(self):
        OdemeRepository.kaydet(self.odeme_model)
        basarili = OdemeRepository.basarili_odemeler()
        self.assertTrue(any(o["odeme_id"] == self.odeme_model.odeme_id for o in basarili))

    def test_odeme_toplam_tutar(self):
        OdemeRepository.kaydet(self.odeme_model)
        toplam = OdemeRepository.toplam_tutar()
        self.assertGreaterEqual(toplam, 200)

    def test_odeme_son_n(self):
        OdemeRepository.kaydet(self.odeme_model)
        son_odemeler = OdemeRepository.son_n_odeme(1)
        self.assertEqual(len(son_odemeler), 1)


class TestOdemeYontemiRepository(unittest.TestCase):

    def setUp(self):
        OdemeYontemiRepository.temizle()
        self.kart = KrediKartiOdeme("Mehmet", 1000, "8765432187654321", "11/29", "321")
        OdemeYontemiRepository.kaydet(self.kart)

    def test_odeme_yontemi_listele(self):
        liste = OdemeYontemiRepository.listele()
        self.assertTrue(len(liste) > 0)

    def test_odeme_yontemi_bul_ve_pasif_yap(self):
        id_bulunan = OdemeYontemiRepository.listele()[0]["id"]
        found = OdemeYontemiRepository.bul(id_bulunan)
        self.assertIsNotNone(found)
        pasif = OdemeYontemiRepository.pasif_yap(id_bulunan)
        self.assertTrue(pasif)
        updated = OdemeYontemiRepository.bul(id_bulunan)
        self.assertEqual(updated["durum"], "PASIF")

    def test_odeme_yontemi_toplam_bakiye(self):
        toplam = OdemeYontemiRepository.toplam_bakiye()
        self.assertGreaterEqual(toplam, 0)

    def test_odeme_yontemi_sahip_ile_listele(self):
        liste = OdemeYontemiRepository.sahip_ile_listele("Mehmet")
        self.assertTrue(all(o["sahip"] == "Mehmet" for o in liste))

    def test_odeme_yontemi_bakiyeye_gore(self):
        sorted_list = OdemeYontemiRepository.bakiyeye_gore_sirala()
        self.assertTrue(sorted_list[0]["bakiye"] <= sorted_list[-1]["bakiye"])

if __name__ == "__main__":
    unittest.main()
