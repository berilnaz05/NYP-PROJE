from typing import List, Dict
from datetime import datetime
from odeme_service import OdemeService

class RaporlamaService:
    def __init__(self, odeme_service: OdemeService):
        self.odeme_service = odeme_service

    def tum_islemleri_goster(self):
        for islem in self.odeme_service.islemler:
            print(f"İşlem ID: {islem['islem_id']}, Sahip: {islem['sahip']}, "
                  f"Tutar: {islem['tutar']} {islem['para_birimi']}, "
                  f"Durum: {islem['durum']}, Tarih: {islem['tarih']}")

    def basarili_islemleri_goster(self):
        for islem in self.odeme_service.islemler:
            if islem["durum"] == "BAŞARILI":
                print(f"{islem['islem_id']} | {islem['sahip']} | {islem['tutar']} {islem['para_birimi']} | {islem['tarih']}")

    def basarisiz_islemleri_goster(self):
        for islem in self.odeme_service.islemler:
            if islem["durum"] == "BAŞARISIZ":
                print(f"{islem['islem_id']} | {islem['sahip']} | {islem['tutar']} {islem['para_birimi']} | {islem['tarih']}")

    def toplam_tutar(self):
        toplam = sum([i["tutar"] for i in self.odeme_service.islemler if i["durum"] == "BAŞARILI"])
        print(f"Tüm başarılı işlemlerin toplam tutarı: {toplam}")

    def kullanici_toplam_tutar(self, kullanici: str):
        toplam = sum([i["tutar"] for i in self.odeme_service.islemler 
                      if i["durum"] == "BAŞARILI" and i["sahip"] == kullanici])
        print(f"{kullanici} adlı kullanıcının başarılı ödemeler toplamı: {toplam}")

    def en_yuksek_odeme(self):
        if not self.odeme_service.islemler:
            print("Hiç işlem yok.")
            return
        max_odeme = max(self.odeme_service.islemler, key=lambda x: x["tutar"])
        print(f"En yüksek ödeme: {max_odeme['tutar']} {max_odeme['para_birimi']} - {max_odeme['sahip']}")

    def en_dusuk_odeme(self):
        if not self.odeme_service.islemler:
            print("Hiç işlem yok.")
            return
        min_odeme = min(self.odeme_service.islemler, key=lambda x: x["tutar"])
        print(f"En düşük ödeme: {min_odeme['tutar']} {min_odeme['para_birimi']} - {min_odeme['sahip']}")

    def odeme_istatistikleri(self):
        basarili = len([i for i in self.odeme_service.islemler if i["durum"] == "BAŞARILI"])
        basarisiz = len([i for i in self.odeme_service.islemler if i["durum"] == "BAŞARISIZ"])
        toplam = sum([i["tutar"] for i in self.odeme_service.islemler])
        print(f"Toplam ödeme: {toplam}, Başarılı işlemler: {basarili}, Başarısız işlemler: {basarisiz}")

    def kullanici_istatistikleri(self, kullanici: str):
        islemler = [i for i in self.odeme_service.islemler if i["sahip"] == kullanici]
        toplam = sum([i["tutar"] for i in islemler if i["durum"] == "BAŞARILI"])
        basarili = len([i for i in islemler if i["durum"] == "BAŞARILI"])
        basarisiz = len([i for i in islemler if i["durum"] == "BAŞARISIZ"])
        print(f"{kullanici} - Toplam: {toplam}, Başarılı: {basarili}, Başarısız: {basarisiz}")

    def raporu_dosyaya_yaz(self, dosya_adi="rapor.txt"):
        with open(dosya_adi, "w", encoding="utf-8") as f:
            for islem in self.odeme_service.islemler:
                f.write(f"{islem['islem_id']} | {islem['sahip']} | {islem['tutar']} {islem['para_birimi']} | "
                        f"{islem['durum']} | {islem['tarih']}\n")

    def aylik_rapor(self, ay: int, yil: int):
        toplam = sum([i["tutar"] for i in self.odeme_service.islemler 
                      if i["tarih"].month == ay and i["tarih"].year == yil and i["durum"] == "BAŞARILI"])
        print(f"{yil}-{ay} ayındaki toplam başarılı ödeme tutarı: {toplam}")

    def kullanici_aylik_rapor(self, kullanici: str, ay: int, yil: int):
        toplam = sum([i["tutar"] for i in self.odeme_service.islemler 
                      if i["tarih"].month == ay and i["tarih"].year == yil 
                      and i["sahip"] == kullanici and i["durum"] == "BAŞARILI"])
        print(f"{kullanici} için {yil}-{ay} ayındaki toplam başarılı ödeme: {toplam}")

    def son_n_islemler(self, n: int = 5):
        son_islemler = sorted(self.odeme_service.islemler, key=lambda x: x["tarih"], reverse=True)[:n]
        for i in son_islemler:
            print(f"{i['islem_id']} | {i['sahip']} | {i['tutar']} {i['para_birimi']} | {i['durum']} | {i['tarih']}")

    def kullanici_son_n_islemler(self, kullanici: str, n: int = 5):
        son_islemler = sorted([i for i in self.odeme_service.islemler if i["sahip"] == kullanici], 
                               key=lambda x: x["tarih"], reverse=True)[:n]
        for i in son_islemler:
            print(f"{i['islem_id']} | {i['sahip']} | {i['tutar']} {i['para_birimi']} | {i['durum']} | {i['tarih']}")

