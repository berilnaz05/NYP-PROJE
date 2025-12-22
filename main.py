from payment.subclass import (
    KrediKartiOdeme,
    NakitOdeme,
    DijitalCuzdanOdeme
)


def main():
    kredi_karti = KrediKartiOdeme(
        tutar=0,
        sahip="Beril",
        bakiye=500,
        kart_numarasi="1234567812345678",
        son_kullanma_tarihi="12/26",
        cvv="123"
    )

    sonuc = kredi_karti.ode(200)

    if sonuc:
        print("Ödeme başarılı 🎉")
    else:
        print("Ödeme başarısız ❌")

if __name__ == "__main__":
    main()
