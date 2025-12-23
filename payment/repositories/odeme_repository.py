from datetime import datetime
from typing import List, Optional
import uuid
from payment.models.odeme_model import OdemeModel

class OdemeRepository:
    def __init__(self):
        self._odemeler: List[OdemeModel] = []

    def odeme_kaydet(self, kullanici: str, tutar: float, odeme_tipi: str) -> OdemeModel:
        odeme = OdemeModel(
            odeme_id=str(uuid.uuid4()),
            kullanici=kullanici,
            tutar=tutar,
            odeme_tipi=odeme_tipi,
            tarih=datetime.now()
        )
        self._odemeler.append(odeme)
        return odeme

    def tum_odemeleri_listele(self) -> List[OdemeModel]:
        return self._odemeler

    def odeme_bul_id_ile(self, odeme_id: str) -> Optional[OdemeModel]:
        for odeme in self._odemeler:
            if odeme.odeme_id == odeme_id:
                return odeme
        return None

    def kullaniciya_gore_filtrele(self, kullanici: str) -> List[OdemeModel]:
        return [o for o in self._odemeler if o.kullanici == kullanici]

    def tarih_araligina_gore_filtrele(self, baslangic: datetime, bitis: datetime) -> List[OdemeModel]:
        return [o for o in self._odemeler if baslangic <= o.tarih <= bitis]

    def toplam_tutar(self) -> float:
        toplam = 0
        for o in self._odemeler:
            toplam += o.tutar
        return toplam

    def kullanici_bazli_toplam(self, kullanici: str) -> float:
        toplam = 0
        for o in self._odemeler:
            if o.kullanici == kullanici:
                toplam += o.tutar
        return toplam
