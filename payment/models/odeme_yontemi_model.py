class OdemeYontemiModel:
    def __init__(
        self,
        yontem_id: str,
        kullanici: str,
        yontem_adi: str,
        aktif: bool = True
    ):
        self.yontem_id = yontem_id
        self.kullanici = kullanici
        self.yontem_adi = yontem_adi
        self.aktif = aktif

    def __repr__(self):
        return (
            f"OdemeYontemiModel("
            f"id={self.yontem_id}, "
            f"kullanici={self.kullanici}, "
            f"yontem={self.yontem_adi}, "
            f"aktif={self.aktif})"
        )
