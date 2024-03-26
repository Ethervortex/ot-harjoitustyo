# Ohjelmistotekniikka, harjoitustyö

Sovellus on toteutettu Helsingin yliopiston kurssilla: Aineopintojen harjoitustyö: Ohjelmistotekniikka 

Sovellus on **funktiolaskin**, jolla voi laskea peruslaskutoimitusten (+, -, * ja /) lisäksi myös mm. trigonometriset funktiot, logaritmit, potenssilaskut ja juuret. Peruslaskutoimitukset voi syöttää hiiren lisäksi myös näppäimistöllä. Laskuhistoria kerätään omaan näyttöönsä ja sen voi tarvittaessa tallentaa tietokantaan sekä ladata sieltä.

## Python-versio

Laskin on toteutettu ja testattu Python-versiolla `3.10`.

## Linkki *laskarit*-hakemistoon:

- [Laskarit](./laskarit)

## Dokumentaatio
- [Vaatimusmäärittely](./dokumentaatio/vaatimusmaarittely.md)
- [Työaikakirjanpito](./dokumentaatio/tuntikirjanpito.md)
- [Changelog](./dokumentaatio/changelog.md)

## Asentaminen

Asenna riippuvuudet komennolla:

```bash
poetry install
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
