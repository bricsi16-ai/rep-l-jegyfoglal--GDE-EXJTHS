# -*- coding: utf-8 -*-
"""Repülőjegy Foglalási Rendszer.

Egyszerű konzolos vizsgafeladat Pythonban:
- járatok listázása,
- jegy foglalása,
- foglalás lemondása,
- aktuális foglalások listázása.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class AdatValidaciosHiba(ValueError):
    """Hibás vagy hiányzó felhasználói adat."""


class FoglalasiHiba(Exception):
    """Foglalással kapcsolatos üzleti hiba."""


class Jarat(ABC):
    """Absztrakt járat osztály: járatszám, célállomás, jegyár."""

    def __init__(
        self,
        jaratszam: str,
        celallomas: str,
        jegyar: int,
        indulasi_ido: datetime,
        ferohelyek: int,
        utazasi_ido_perc: int,
    ) -> None:
        self._jaratszam = self._ervenyes_szoveg(jaratszam, "A járatszám")
        self._celallomas = self._ervenyes_szoveg(celallomas, "A célállomás")
        self.jegyar = jegyar
        self.indulasi_ido = indulasi_ido
        self.ferohelyek = ferohelyek
        self.utazasi_ido_perc = utazasi_ido_perc

    @staticmethod
    def _ervenyes_szoveg(ertek: str, mezo_nev: str) -> str:
        if not isinstance(ertek, str) or not ertek.strip():
            raise AdatValidaciosHiba(f"{mezo_nev} nem lehet üres.")
        return ertek.strip()

    @property
    def jaratszam(self) -> str:
        return self._jaratszam

    @property
    def celallomas(self) -> str:
        return self._celallomas

    @celallomas.setter
    def celallomas(self, uj_celallomas: str) -> None:
        self._celallomas = self._ervenyes_szoveg(uj_celallomas, "A célállomás")

    @property
    def jegyar(self) -> int:
        return self._jegyar

    @jegyar.setter
    def jegyar(self, uj_jegyar: int) -> None:
        if not isinstance(uj_jegyar, int) or uj_jegyar <= 0:
            raise AdatValidaciosHiba("A jegyár csak pozitív egész szám lehet.")
        self._jegyar = uj_jegyar

    @property
    def indulasi_ido(self) -> datetime:
        return self._indulasi_ido

    @indulasi_ido.setter
    def indulasi_ido(self, uj_indulasi_ido: datetime) -> None:
        if not isinstance(uj_indulasi_ido, datetime):
            raise AdatValidaciosHiba("Az indulási időnek datetime típusúnak kell lennie.")
        self._indulasi_ido = uj_indulasi_ido

    @property
    def ferohelyek(self) -> int:
        return self._ferohelyek

    @ferohelyek.setter
    def ferohelyek(self, uj_ferohelyek: int) -> None:
        if not isinstance(uj_ferohelyek, int) or uj_ferohelyek <= 0:
            raise AdatValidaciosHiba("A férőhelyek száma csak pozitív egész szám lehet.")
        self._ferohelyek = uj_ferohelyek

    @property
    def utazasi_ido_perc(self) -> int:
        return self._utazasi_ido_perc

    @utazasi_ido_perc.setter
    def utazasi_ido_perc(self, uj_utazasi_ido_perc: int) -> None:
        if not isinstance(uj_utazasi_ido_perc, int) or uj_utazasi_ido_perc <= 0:
            raise AdatValidaciosHiba("Az utazási idő csak pozitív egész szám lehet.")
        self._utazasi_ido_perc = uj_utazasi_ido_perc

    @property
    def erkezesi_ido(self) -> datetime:
        return self._indulasi_ido + timedelta(minutes=self._utazasi_ido_perc)

    @abstractmethod
    def jarat_tipus(self) -> str:
        """Visszaadja, hogy belföldi vagy nemzetközi járatról van szó."""

    def foglalhato(self) -> bool:
        return self._indulasi_ido > datetime.now()


class BelfoldiJarat(Jarat):
    """Belföldi járat: rövidebb útvonal, kedvezőbb jegyár."""

    def jarat_tipus(self) -> str:
        return "Belföldi"


class NemzetkoziJarat(Jarat):
    """Nemzetközi járat: hosszabb útvonal, magasabb jegyár."""

    def jarat_tipus(self) -> str:
        return "Nemzetközi"


class LegiTarsasag:
    """Légitársaság, amely saját járatokat tart nyilván."""

    def __init__(self, nev: str) -> None:
        self.nev = nev
        self._jaratok: dict[str, Jarat] = {}

    @property
    def nev(self) -> str:
        return self._nev

    @nev.setter
    def nev(self, uj_nev: str) -> None:
        if not isinstance(uj_nev, str) or not uj_nev.strip():
            raise AdatValidaciosHiba("A légitársaság neve nem lehet üres.")
        self._nev = uj_nev.strip()

    @property
    def jaratok(self) -> tuple[Jarat, ...]:
        return tuple(self._jaratok.values())

    def jarat_hozzaadasa(self, jarat: Jarat) -> None:
        if not isinstance(jarat, Jarat):
            raise AdatValidaciosHiba("Csak Jarat típusú objektum adható hozzá.")
        if jarat.jaratszam in self._jaratok:
            raise AdatValidaciosHiba(f"Már létezik ilyen járatszám: {jarat.jaratszam}")
        self._jaratok[jarat.jaratszam] = jarat

    def jarat_keresese(self, jaratszam: str) -> Jarat:
        jarat = self._jaratok.get(jaratszam.strip().upper())
        if jarat is None:
            raise FoglalasiHiba("Nincs ilyen járatszám a rendszerben.")
        return jarat


class JegyFoglalas:
    """Egy utas egy konkrét járatra szóló foglalását tárolja."""

    def __init__(self, foglalasi_azonosito: str, utas_nev: str, jarat: Jarat) -> None:
        self._foglalasi_azonosito = self._ervenyes_azonosito(foglalasi_azonosito)
        self.utas_nev = utas_nev
        self._jarat = jarat
        self._foglalas_ideje = datetime.now()

    @staticmethod
    def _ervenyes_azonosito(ertek: str) -> str:
        if not isinstance(ertek, str) or not ertek.strip():
            raise AdatValidaciosHiba("A foglalási azonosító nem lehet üres.")
        return ertek.strip().upper()

    @property
    def foglalasi_azonosito(self) -> str:
        return self._foglalasi_azonosito

    @property
    def utas_nev(self) -> str:
        return self._utas_nev

    @utas_nev.setter
    def utas_nev(self, uj_utas_nev: str) -> None:
        if not isinstance(uj_utas_nev, str) or len(uj_utas_nev.strip()) < 2:
            raise AdatValidaciosHiba("Az utas neve legalább 2 karakter legyen.")
        self._utas_nev = uj_utas_nev.strip()

    @property
    def jarat(self) -> Jarat:
        return self._jarat

    @property
    def foglalas_ideje(self) -> datetime:
        return self._foglalas_ideje

    @property
    def ar(self) -> int:
        return self._jarat.jegyar


class FoglalasiRendszer:
    """A jegyfoglalási műveleteket összefogó szolgáltatás osztály."""

    def __init__(self, legitarsasag: LegiTarsasag) -> None:
        self._legitarsasag = legitarsasag
        self._foglalasok: dict[str, JegyFoglalas] = {}
        self._kovetkezo_sorszam = 1

    @property
    def legitarsasag(self) -> LegiTarsasag:
        return self._legitarsasag

    @property
    def foglalasok(self) -> tuple[JegyFoglalas, ...]:
        return tuple(self._foglalasok.values())

    def jegy_foglalasa(self, utas_nev: str, jaratszam: str) -> JegyFoglalas:
        jarat = self._legitarsasag.jarat_keresese(jaratszam)
        if not jarat.foglalhato():
            raise FoglalasiHiba("Erre a járatra már nem lehet foglalni, mert elindult.")
        if self.szabad_helyek(jarat.jaratszam) <= 0:
            raise FoglalasiHiba("A kiválasztott járat betelt.")

        azonosito = self._uj_foglalasi_azonosito()
        foglalas = JegyFoglalas(azonosito, utas_nev, jarat)
        self._foglalasok[azonosito] = foglalas
        return foglalas

    def foglalas_lemondasa(self, foglalasi_azonosito: str) -> JegyFoglalas:
        azonosito = foglalasi_azonosito.strip().upper()
        if azonosito not in self._foglalasok:
            raise FoglalasiHiba("Csak létező foglalást lehet lemondani.")
        return self._foglalasok.pop(azonosito)

    def szabad_helyek(self, jaratszam: str) -> int:
        jarat = self._legitarsasag.jarat_keresese(jaratszam)
        foglalt_helyek = sum(
            1 for foglalas in self._foglalasok.values()
            if foglalas.jarat.jaratszam == jarat.jaratszam
        )
        return jarat.ferohelyek - foglalt_helyek

    def _uj_foglalasi_azonosito(self) -> str:
        while True:
            azonosito = f"F{self._kovetkezo_sorszam:04d}"
            self._kovetkezo_sorszam += 1
            if azonosito not in self._foglalasok:
                return azonosito


def penz_formazasa(osszeg: int) -> str:
    return f"{osszeg:,} Ft".replace(",", " ")


def datum_formazasa(datum: datetime) -> str:
    return datum.strftime("%Y.%m.%d. %H:%M")


def rendszer_feltoltese() -> FoglalasiRendszer:
    """Induló adatok: 1 légitársaság, 3 járat, 6 foglalás."""

    most = datetime.now().replace(second=0, microsecond=0)
    legitarsasag = LegiTarsasag("Duna Wings")

    indulasi_idok = [
        most + timedelta(days=7, hours=3),
        most + timedelta(days=12, hours=6),
        most + timedelta(days=20, hours=8),
    ]

    jaratok: list[Jarat] = [
        BelfoldiJarat("DW101", "Debrecen", 14900, indulasi_idok[0], 8, 45),
        BelfoldiJarat("DW202", "Pécs", 18900, indulasi_idok[1], 8, 55),
        NemzetkoziJarat("DW303", "London", 58900, indulasi_idok[2], 10, 150),
    ]

    for jarat in jaratok:
        legitarsasag.jarat_hozzaadasa(jarat)

    rendszer = FoglalasiRendszer(legitarsasag)
    indulasi_foglalasok = [
        ("Kovács Anna", "DW101"),
        ("Nagy Péter", "DW101"),
        ("Szabó Lilla", "DW202"),
        ("Tóth Márk", "DW202"),
        ("Varga Nóra", "DW303"),
        ("Balogh Dániel", "DW303"),
    ]

    for utas_nev, jaratszam in indulasi_foglalasok:
        rendszer.jegy_foglalasa(utas_nev, jaratszam)

    return rendszer


def jaratok_kiirasa(rendszer: FoglalasiRendszer) -> None:
    print("\nElérhető járatok")
    print("-" * 88)
    print(f"{'Járatszám':<10} {'Típus':<12} {'Célállomás':<16} {'Indulás':<18} {'Ár':<12} {'Szabad hely'}")
    print("-" * 88)
    for jarat in rendszer.legitarsasag.jaratok:
        print(
            f"{jarat.jaratszam:<10} "
            f"{jarat.jarat_tipus():<12} "
            f"{jarat.celallomas:<16} "
            f"{datum_formazasa(jarat.indulasi_ido):<18} "
            f"{penz_formazasa(jarat.jegyar):<12} "
            f"{rendszer.szabad_helyek(jarat.jaratszam)}"
        )


def foglalasok_kiirasa(rendszer: FoglalasiRendszer) -> None:
    print("\nAktuális foglalások")
    print("-" * 94)
    if not rendszer.foglalasok:
        print("Nincs aktuális foglalás.")
        return

    print(f"{'Azonosító':<12} {'Utas':<20} {'Járat':<10} {'Célállomás':<16} {'Indulás':<18} {'Ár'}")
    print("-" * 94)
    for foglalas in rendszer.foglalasok:
        jarat = foglalas.jarat
        print(
            f"{foglalas.foglalasi_azonosito:<12} "
            f"{foglalas.utas_nev:<20} "
            f"{jarat.jaratszam:<10} "
            f"{jarat.celallomas:<16} "
            f"{datum_formazasa(jarat.indulasi_ido):<18} "
            f"{penz_formazasa(foglalas.ar)}"
        )


def jegy_foglalasa_menu(rendszer: FoglalasiRendszer) -> None:
    jaratok_kiirasa(rendszer)
    utas_nev = input("\nUtas neve: ").strip()
    jaratszam = input("Járatszám: ").strip().upper()
    foglalas = rendszer.jegy_foglalasa(utas_nev, jaratszam)
    print(
        "\nSikeres foglalás!"
        f"\nFoglalási azonosító: {foglalas.foglalasi_azonosito}"
        f"\nFizetendő ár: {penz_formazasa(foglalas.ar)}"
    )


def foglalas_lemondasa_menu(rendszer: FoglalasiRendszer) -> None:
    foglalasok_kiirasa(rendszer)
    azonosito = input("\nLemondandó foglalás azonosítója: ").strip().upper()
    torolt_foglalas = rendszer.foglalas_lemondasa(azonosito)
    print(
        "\nA foglalás sikeresen lemondva:"
        f" {torolt_foglalas.foglalasi_azonosito} - {torolt_foglalas.utas_nev}"
    )


def menu_kiirasa(rendszer: FoglalasiRendszer) -> None:
    print("\n" + "=" * 52)
    print(f"Repülőjegy Foglalási Rendszer - {rendszer.legitarsasag.nev}")
    print("=" * 52)
    print("1. Járatok listázása")
    print("2. Jegy foglalása")
    print("3. Foglalás lemondása")
    print("4. Foglalások listázása")
    print("0. Kilépés")


def main() -> None:
    rendszer = rendszer_feltoltese()
    print("A rendszer betöltött 1 légitársaságot, 3 járatot és 6 foglalást.")

    while True:
        menu_kiirasa(rendszer)
        valasztas = input("\nVálassz egy menüpontot: ").strip()

        try:
            if valasztas == "1":
                jaratok_kiirasa(rendszer)
            elif valasztas == "2":
                jegy_foglalasa_menu(rendszer)
            elif valasztas == "3":
                foglalas_lemondasa_menu(rendszer)
            elif valasztas == "4":
                foglalasok_kiirasa(rendszer)
            elif valasztas == "0":
                print("\nViszlát!")
                break
            else:
                print("\nNincs ilyen menüpont. Kérlek, válassz újra.")
        except (AdatValidaciosHiba, FoglalasiHiba) as hiba:
            print(f"\nHiba: {hiba}")


if __name__ == "__main__":
    main()
