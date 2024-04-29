# Käyttöohje

Lataa laskimen viimeisimmän [releasen]((https://github.com/Ethervortex/ot-harjoitustyo/releases/tag/viikko6)) lähdekoodi

## Konfigurointi

Tietokannan tiedostonimeä voi tarvittaessa muuttaa käynnistyshakemistossa _.env_-tiedostossa. 
Tietokantatiedosto luodaan automaattisesti laskuhistoriaa tallennettaessa, jos tiedostoa ei vielä ole.
Tiedoston _.env_ muoto on seuraava: 

```
DATABASE_FILENAME=calculator.db
```

## Ohjelman käynnistäminen

Ennen ohjelman käynnistämistä, asenna riippuvuudet komennolla:

```bash
poetry install
```

Nyt laskin voidaan käynnistää komennolla:

```
poetry run invoke start
```

## Laskimen käyttö

Laskinta voi käyttää hiirellä painamalla käyttöliittymän nappeja. Laskut voi 
syöttää myös suoraan näppäimistöltä, mutta etenkin funktioiden osalta tällöin tulee olla 
tietoinen oikeasta syntaksista. Seuraavassa ohjeet laskimen käyttämiseen:

1. Laskujen suoritus
- Syötä laskutoimitus hiirellä tai näppäimistöllä
- Suorita lasku painamalla hiirellä `=`-nappia tai näppäimistöstä `Enter`
- Edellisen laskun voi pyyhkiä painamalla `C`
- Laskuhistoria kertyy omaan näyttöönsä laskimen yläosaan

2. Funktiot
- Monissa funktioissa esim. `sin`, `log`, `abs` numeroarvo tulee syöttää sulkujen sisään
- Jos käyttäjä unohtaa sulkea sulut, käyttöliittymä huomauttaa siitä
- Erityisen tarkkana sulkujen kanssa tulee olla tilanteessa, jossa kulmayksiköiksi on valittu asteet 
ja käytetään trigonometrisia funktioita.

3. Radiaanit ja asteet
- Laskin käynnistyy `radians`-tilassa
- Käyttäjä voi vaihtaa asteiksi painamalla `radians`-nappia, jolloin napin tilaksi vaihtuu `degrees`
- Painamalla `degrees`-nappia laskimen tila vaihtuu takaisin radiaaneiksi

4. Muisti
- Laskutuloksen voi tallentaa muistiin painamalla `MS`-nappia
- Jos muistissa on tulos, sen voi palauttaa `MR`-napilla

5. Murtoluvuksi muuttaminen
- Laskutuloksen voi muuntaa murtoluvuksi painamalla `a/b`-nappia
- `a/b` antaa tuloksen pyöristettynä eli esim. myös piin likiarvon saa muutettua murtoluvuksi
- `a/b`-nappi on käytössä vain jos lasku on suoritettu

6. Laskuhistorian selailu
- Aiempia laskutuloksia voi selata ja niihin voi palata 'Undo'- ja 'Redo'-painikkeilla (kaarevat nuolet)

7. Virheet
- Jos tapahtuu virhe, virheilmoitus näkyy laskentaruudussa
- Sulkemattomat sulut aiheuttavat huomautuksen
- Virheen sattuessa tarkista syöte ja yritä uudelleen

8. Tietokanta
- Laskuhistorian voi ladata ja tallentaa `Database`-valikosta
- Tallennettaessa valitaan `Save history` ja annetaan tallennettavalle historialle nimi
- Ladattaessa valitaan `Load history` ja valitaan haluttu historia listasta
- Tietokannan sisällön voi poistaa valitsemalla valikosta `Clear database`
