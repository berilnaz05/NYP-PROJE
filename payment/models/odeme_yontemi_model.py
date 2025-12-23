from datetime import datetime
import uuid
from base import OdemeYontemi
from base import subclass


class OdemeYontemiModel:
    tum_odeme_yontemleri = []

    def __init__(self, odeme_tipi: OdemeYontemi):
        self.odeme_tipi = odeme_tipi
        self.id = str(uuid.uuid4())
        self.olusturma_tarihi = datetime.now()
        self.guncelleme_tarihi = datetime.now()
        self.durum = "AKTIF"
        OdemeYontemiModel.tum_odeme_yontemleri.append(self)

    @classmethod
    def listele(cls):
        for o in cls.tum_odeme_yontemleri:
            print(f"ID: {o.id} | Tip: {o.odeme_tipi.__class__.__name__} | Sahip: {getattr(o.odeme_tipi, 'sahip', None)} | Bakiye: {getattr(o.odeme_tipi, 'bakiye', None)} | Durum: {o.durum}")

    @classmethod
    def bul_id(cls, id: str):
        for o in cls.tum_odeme_yontemleri:
            if o.id == id:
                return o
        return None

    @classmethod
    def aktifleri_getir(cls):
        return [o for o in cls.tum_odeme_yontemleri if o.durum == "AKTIF"]

    @classmethod
    def bakiyeye_gore_sirala(cls, ters=False):
        return sorted(cls.tum_odeme_yontemleri, key=lambda x: getattr(x.odeme_tipi, "bakiye", 0), reverse=ters)

    @classmethod
    def kullaniciya_gore_listele(cls, sahip: str):
        return [o for o in cls.tum_odeme_yontemleri if getattr(o.odeme_tipi, "sahip", "") == sahip]

    def bakiyeyi_guncelle(self, yeni_bakiye):
        if hasattr(self.odeme_tipi, "bakiye"):
            self.odeme_tipi.bakiye = yeni_bakiye
            self.guncelleme_tarihi = datetime.now()
            return True
        return False

    def odeme_yap(self, tutar):
        if self.odeme_tipi.ode(tutar):
            self.guncelleme_tarihi = datetime.now()
            return True
        return False

    @classmethod
    def toplam_bakiye(cls):
        return sum(getattr(o.odeme_tipi, "bakiye", 0) for o in cls.tum_odeme_yontemleri)

    @classmethod
    def istatistik(cls):
        toplam = len(cls.tum_odeme_yontemleri)
        aktif = len([o for o in cls.tum_odeme_yontemleri if o.durum == "AKTIF"])
        print(f"Toplam yöntem: {toplam} | Aktif: {aktif}")

    @classmethod
    def en_yuksek_bakiye(cls):
        liste = cls.bakiyeye_gore_sirala(ters=True)
        if liste:
            o = liste[0]
            print(f"En yüksek bakiye: {getattr(o.odeme_tipi, 'bakiye', 0)} - {getattr(o.odeme_tipi, 'sahip', '')}")

    @classmethod
    def en_dusuk_bakiye(cls):
        liste = cls.bakiyeye_gore_sirala()
        if liste:
            o = liste[0]
            print(f"En düşük bakiye: {getattr(o.odeme_tipi, 'bakiye', 0)} - {getattr(o.odeme_tipi, 'sahip', '')}")

    def pasif_yap(self):
        self.durum = "PASIF"
        self.guncelleme_tarihi = datetime.now()

    @classmethod
    def odeme_turlerine_gore(cls):
        tur_dict = {}
        for o in cls.tum_odeme_yontemleri:
            tur = o.odeme_tipi.__class__.__name__
            tur_dict[tur] = tur_dict.get(tur, 0) + 1
        for k, v in tur_dict.items():
            print(f"{k}: {v} adet")

    @classmethod
    def bakiyeleri_topla(cls):
        toplam = {}
        for o in cls.tum_odeme_yontemleri:
            tur = o.odeme_tipi.__class__.__name__
            toplam[tur] = toplam.get(tur, 0) + getattr(o.odeme_tipi, "bakiye", 0)
        for k, v in toplam.items():
            print(f"{k} toplam bakiye: {v}")

    @classmethod
    def tum_odeme_detaylari(cls):
        for o in cls.tum_odeme_yontemleri:
            od = o.odeme_tipi
            print(f"{o.id} | {getattr(od,'sahip', '')} | {getattr(od,'bakiye',0)} | {od.__class__.__name__} | Durum: {o.durum} | Oluşturma: {o.olusturma_tarihi} | Güncelleme: {o.guncelleme_tarihi}")

    @classmethod
    def dogrulanmis_cuzdanlar(cls):
        return [o for o in cls.tum_odeme_yontemleri if isinstance(o.odeme_tipi, DijitalCuzdanOdeme) and o.odeme_tipi.dogrulanmis]

    @classmethod
    def dogrulanmis_cuzdanlari_goster(cls):
        for o in cls.dogrulanmis_cuzdanlar():
            print(f"{getattr(o.odeme_tipi,'cuzdan_adi','')} | Sahip: {getattr(o.odeme_tipi,'sahip','')} | Bakiye: {getattr(o.odeme_tipi,'bakiye',0)}")
