# ÖDEME YÖNTEMİ REPOSITORY
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

# ÖDEME REPOSITORY
class OdemeRepository:
    def __init__(self):
        self._odemeler: List[OdemeModel] = []

    def odeme_kaydet(
        self,
        kullanici: str,
        tutar: float,
        odeme_tipi: str
    ) -> OdemeModel:
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
        return [
            o for o in self._odemeler
            if o.kullanici == kullanici
        ]

    def tarih_araligina_gore_filtrele(
        self,
        baslangic: datetime,
        bitis: datetime
    ) -> List[OdemeModel]:
        return [
            o for o in self._odemeler
            if baslangic <= o.tarih <= bitis
        ]

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

# RAPOR SERVİSİ
class OdemeRaporServisi:
    def __init__(self, odeme_repo: OdemeRepository):
        self.odeme_repo = odeme_repo

    def tum_odeme_raporu(self) -> List[OdemeModel]:
        return self.odeme_repo.tum_odemeleri_listele()

    def kullanici_raporu(self, kullanici: str) -> List[OdemeModel]:
        return self.odeme_repo.kullaniciya_gore_filtrele(kullanici)

    def tarih_raporu(
        self,
        baslangic: datetime,
        bitis: datetime
    ) -> List[OdemeModel]:
        return self.odeme_repo.tarih_araligina_gore_filtrele(
            baslangic,
            bitis
        )

    def genel_ciro(self) -> float:
        return self.odeme_repo.toplam_tutar()
