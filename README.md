# Repülőjegy Foglalási Rendszer

Egyszerű Python konzolos alkalmazás a vizsgafeladathoz. A program induláskor betölt:

- 1 légitársaságot,
- 3 járatot,
- 6 előre elkészített foglalást.

## Fő funkciók

- jegy foglalása járatszám alapján,
- foglalás lemondása foglalási azonosító alapján,
- aktuális foglalások listázása,
- járatok listázása szabad helyekkel.
- grafikus felület bal oldali menüvel, táblázatokkal és űrlapokkal.

## Fő osztályok

- `Jarat` absztrakt osztály
- `BelfoldiJarat`
- `NemzetkoziJarat`
- `LegiTarsasag`
- `JegyFoglalas`
- `FoglalasiRendszer`

Az osztályok non-public attribútumokat használnak, ahol szükséges getter/setter propertykkel. A program tartalmaz adatvalidációt és hibakezelést.

## Telepítés és futtatás

Python 3.9 vagy újabb verzió szükséges hozzá. Külső csomag jelenleg nem kell, de a projekt tartalmaz `requirements.txt` fájlt, ezért később is ugyanígy telepíthető marad.

Windows gépen dupla kattintással a grafikus alkalmazáshoz:

```bat
inditas.bat
```

Windows gépen parancssorból:

```bash
telepites.bat
inditas.bat
```

A régi konzolos verzió is megmaradt tartalékként:

```bat
konzol.bat
```

macOS vagy Linux gépen:

```bash
bash install.sh
bash run.sh
```

PyCharmban nyisd meg ezt a mappát, majd futtasd a `gui.py` fájlt. Ha a konzolos verziót szeretnéd ellenőrizni, a `main.py` is külön futtatható.

## Grafikus menüpontok

- `Járatok listázása`: járatszám, típus, célállomás, indulás, érkezés, ár és szabad hely.
- `Jegy foglalása`: utasnév megadása és járat kiválasztása.
- `Foglalás lemondása`: foglalás kiválasztása vagy azonosító beírása.
- `Foglalások listázása`: minden aktuális foglalás táblázatos megjelenítése.

## GitHub beadás előtt

1. Hozz létre egy public GitHub repositoryt.
2. Töltsd fel a projekt mappáját.
3. Incognito böngészőben ellenőrizd, hogy a repository nyilvánosan látszik.
4. Clone-old vissza PyCharmban, és ellenőrizd, hogy indul-e a `main.py`.
5. A Neptunba feltöltendő `NEPTUNKOD.docx` fájlba másold be a GitHub repository linkjét.
