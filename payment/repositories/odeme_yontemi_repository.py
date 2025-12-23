from typing import List, Optional
from payment.models.odeme_yontemi_model import OdemeYontemiModel

class OdemeYontemiRepository:
    def __init__(self):
        self._yontemler: List[OdemeYontemiModel] = []

    def ekle(self, yontem: OdemeYontemiModel):
        self._yontemler.append(yontem)

    def tum_yontemleri_listele(self) -> List[OdemeYontemiModel]:
        return self._yontemler

    def kullaniciya_ait_yontemler(self, kullanici: str) -> List[OdemeYontemiModel]:
        return [
            y for y in self._yontemler
            if y.kullanici == kullanici and y.aktif
        ]

    def yontem_bul(self, yontem_id: str) -> Optional[OdemeYontemiModel]:
        for y in self._yontemler:
            if y.yontem_id == yontem_id:
                return y
        return None

    def pasif_yap(self, yontem_id: str) -> bool:
        yontem = self.yontem_bul(yontem_id)
        if yontem:
            yontem.aktif = False
            return True
        return False
