from payment.credit_card import KrediKartiOdeme
from payment.repositories.odeme_repository import OdemeRepository
from payment.services.odeme_service import OdemeIslemServisi

kart = KrediKartiOdeme(
    tutar=40,
    sahip="Beril",
    bakiye=100,
    kart_numarasi="1234567812345678",
    son_kullanma_tarihi="12/30",
    cvv="123"
)

repo = OdemeRepository()
servis = OdemeIslemServisi(repo)

servis.odeme_yap("Beril", 40, kart)
