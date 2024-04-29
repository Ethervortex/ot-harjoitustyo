# Ohjelmistotekniikka, harjoitustyö

Sovellus on toteutettu Helsingin yliopiston kurssilla: Aineopintojen harjoitustyö: Ohjelmistotekniikka 

Sovellus on **funktiolaskin**, jolla voi laskea peruslaskutoimitusten (+, -, * ja /) lisäksi myös mm. trigonometriset funktiot, logaritmit, potenssilaskut ja juuret. Käyttäjä voi valita lasketaanko trigonometriset funktiot radiaaneina vai asteina. Peruslaskutoimitukset voi syöttää hiiren lisäksi myös näppäimistöllä. Laskuhistoria kerätään omaan näyttöönsä ja sen voi tarvittaessa tallentaa tietokantaan sekä ladata sieltä.

## Python-versio

Laskin on toteutettu ja testattu Python-versiolla `3.10`.

## Dokumentaatio
- [Käyttöohje](./dokumentaatio/kayttoohje.md)
- [Vaatimusmäärittely](./dokumentaatio/vaatimusmaarittely.md)
- [Arkkitehtuurikuvaus](./dokumentaatio/arkkitehtuuri.md)
- [Testausdokumentti](./dokumentaatio/testaus.md)
- [Työaikakirjanpito](./dokumentaatio/tuntikirjanpito.md)
- [Changelog](./dokumentaatio/changelog.md)

## Release
- [Viikko 5](https://github.com/Ethervortex/ot-harjoitustyo/releases/tag/viikko5)
- [Viikko 6](https://github.com/Ethervortex/ot-harjoitustyo/releases/tag/viikko6)

## Asentaminen

Asenna riippuvuudet komennolla:

```bash
poetry install
```

Sen jälkeen alusta tietokanta komennolla:

```bash
poetry run invoke build
```

## Ohjelman suorittaminen

Käynnistä sovellus komennolla:

```bash
poetry run invoke start
```

## Testaus

Ohjelman testit suoritetaan komennolla:

```bash
poetry run invoke test
```

## Testikattavuus

Testikattavuusraportin voi luoda komennolla:

```bash
poetry run invoke coverage-report
```

## Pylint

Koodin laatutarkistukset suoritetaan komennolla:

```bash
poetry run invoke lint
```
