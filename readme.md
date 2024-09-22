# Opetussovellus
Sovelluksen avulla voidaan järjestää verkkokursseja, joissa on tekstimateriaalia ja automaattisesti tarkastettavia tehtäviä. Jokainen käyttäjä on opettaja tai opiskelija.

## Sovelluksen ominaisuuksia

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Opiskelija näkee listan kursseista ja voi liittyä kurssille.
- Opiskelija voi lukea kurssin tekstimateriaalia sekä ratkoa kurssin tehtäviä.
- Opiskelija pystyy näkemään tilaston, mitkä kurssin tehtävät hän on ratkonut.
- Opettaja pystyy luomaan uuden kurssin, muuttamaan olemassa olevaa kurssia ja poistamaan kurssin.
- Opettaja pystyy lisäämään kurssille tekstimateriaalia ja tehtäviä. Tehtävä voi olla ainakin monivalinta tai tekstikenttä, johon tulee kirjoittaa oikea vastaus.
- Opettaja pystyy näkemään kurssistaan tilaston, keitä opiskelijoita on kurssilla ja mitkä kurssin tehtävät kukin on ratkonut.

[Lähde](https://hy-tsoha.github.io/materiaali/aiheen_valinta/#opetussovellus)

## Kuinka saan toimimaan?

### Tietokanta
Sovelluksen käyttämät skeemat, taulut ja funktiot löytyvät projektin juuresta tiedostosta `schema.sql`. Niiden tuonti onnistuu esimerkiksi näin:

```
$ psql < schema.sql
```

Mikäli haluat esimerkkidataa, se löytyy projektin juuresta tiedostosta `sample.sql`. Sen tuonti onnistuu samalla tavalla.

### Ympäristömuuttujat

Projektin juuressa on oltava .env -tiedosto, jossa on seuraavat tiedot:
- `DB_URL`, PostgreSQL-tietokantaan yhdistämiseen käyvä merkkijono / osoite
- `SESSION_SECRET`, vapaavalintainen vaikeasti arvattava merkkijono

### Python-riippuvuudet
TODO
