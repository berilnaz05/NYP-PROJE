# main.py

from payment.subclass import KrediKartiOdeme
from payment.services.menu_service import MenuService

def main():
    print("=== KAMPÜS ÖDEME SİSTEMİ ===\n")

    # 1️⃣ Menü oluştur
    menu = MenuService()
    menu.urun_ekle("Hamburger", 85, "Yemek")
    menu.urun_ekle("Pizza", 110, "Yemek")
    menu.urun_ekle("Kola", 20, "İçecek")

    print("📋 MENÜ")
    menu.menuyi_yazdir()
    print()

    # 2️⃣ Ürün seçimi
    secilen_urun = menu.urun_ara("Hamburger")
    if not secilen_urun:
        print("Ürün bulunamadı.")
        return

    tutar = secilen_urun["fiyat"]
    print(f"Seçilen ürün: {secilen_urun['isim']} - {tutar} TL\n")

    # 3️⃣ Ödeme yöntemi
    odeme = KrediKartiOdeme(
        sahip="Beril",
        bakiye=500,
        kart_numarasi="1234567812345678",
        son_kullanma_tarihi="12/26",
        cvv="123"
    )

    # 4️⃣ Ödeme işlemi
    sonuc = odeme.ode(tutar)

    # 5️⃣ Fiş göster
    if sonuc:
        print("\n🧾 FİŞ")
        odeme.fis_goster()

    print("\n=== İŞLEM TAMAMLANDI ===")

if __name__ == "__main__":
    main()
