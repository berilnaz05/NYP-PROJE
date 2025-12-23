from datetime import datetime

class OdemeModel:
    def __init__(
        self,
        odeme_id: str,
        kullanici: str,
        tutar: float,
        odeme_tipi: str,
        tarih: datetime
    ):
        self.odeme_id = odeme_id
        self.kullanici = kullanici
        self.tutar = tutar
        self.odeme_tipi = odeme_tipi
        self.tarih = tarih

    def __repr__(self):
        return (
            f"OdemeModel("
            f"id={self.odeme_id}, "
            f"kullanici={self.kullanici}, "
            f"tutar={self.tutar}, "
            f"tip={self.odeme_tipi}, "
            f"tarih={self.tarih})"
        )
