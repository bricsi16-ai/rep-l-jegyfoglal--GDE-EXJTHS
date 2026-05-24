# -*- coding: utf-8 -*-
"""Grafikus felület a Repülőjegy Foglalási Rendszerhez."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from main import (
    AdatValidaciosHiba,
    FoglalasiHiba,
    FoglalasiRendszer,
    datum_formazasa,
    penz_formazasa,
    rendszer_feltoltese,
)


class RepulojegyApp(tk.Tk):
    """Tkinter alapú, könnyen kezelhető grafikus alkalmazás."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Repülőjegy Foglalási Rendszer")
        self.geometry("1120x720")
        self.minsize(980, 620)

        self.rendszer: FoglalasiRendszer = rendszer_feltoltese()
        self._aktiv_nezet = "jaratok"
        self._jarat_valaszto_ertekek: list[str] = []

        self._szinek = {
            "hatter": "#f4f7fb",
            "panel": "#ffffff",
            "sotet": "#1d2b3a",
            "szoveg": "#243447",
            "muted": "#687789",
            "kiemeles": "#0f766e",
            "kiemeles_sotet": "#115e59",
            "vonal": "#d8e1ec",
            "hiba": "#b42318",
        }

        self.configure(bg=self._szinek["hatter"])
        self._stilus_beallitasa()
        self._felulet_felepitese()
        self.frissites()

    def _stilus_beallitasa(self) -> None:
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self.style.configure(
            "Treeview",
            background=self._szinek["panel"],
            foreground=self._szinek["szoveg"],
            fieldbackground=self._szinek["panel"],
            rowheight=32,
            borderwidth=0,
            font=("Segoe UI", 10),
        )
        self.style.configure(
            "Treeview.Heading",
            background="#e8eef6",
            foreground=self._szinek["sotet"],
            font=("Segoe UI", 10, "bold"),
            padding=(8, 8),
        )
        self.style.map(
            "Treeview",
            background=[("selected", self._szinek["kiemeles"])],
            foreground=[("selected", "#ffffff")],
        )
        self.style.configure("TCombobox", padding=6, font=("Segoe UI", 10))

    def _felulet_felepitese(self) -> None:
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._oldalsav = tk.Frame(self, bg=self._szinek["sotet"], width=250)
        self._oldalsav.grid(row=0, column=0, sticky="ns")
        self._oldalsav.grid_propagate(False)

        self._tartalom = tk.Frame(self, bg=self._szinek["hatter"])
        self._tartalom.grid(row=0, column=1, sticky="nsew")
        self._tartalom.grid_columnconfigure(0, weight=1)
        self._tartalom.grid_rowconfigure(1, weight=1)

        self._fejlec_felepitese()
        self._oldalsav_felepitese()
        self._nezetek_felepitese()

    def _fejlec_felepitese(self) -> None:
        fejlec = tk.Frame(self._tartalom, bg=self._szinek["hatter"])
        fejlec.grid(row=0, column=0, sticky="ew", padx=28, pady=(24, 12))
        fejlec.grid_columnconfigure(0, weight=1)

        self.cim_label = tk.Label(
            fejlec,
            text="Járatok áttekintése",
            bg=self._szinek["hatter"],
            fg=self._szinek["sotet"],
            font=("Segoe UI", 22, "bold"),
        )
        self.cim_label.grid(row=0, column=0, sticky="w")

        self.alcim_label = tk.Label(
            fejlec,
            text="Válassz járatot, foglalj jegyet, vagy kezeld a meglévő foglalásokat.",
            bg=self._szinek["hatter"],
            fg=self._szinek["muted"],
            font=("Segoe UI", 10),
        )
        self.alcim_label.grid(row=1, column=0, sticky="w", pady=(4, 0))

        frissites_gomb = tk.Button(
            fejlec,
            text="Frissítés",
            command=self.frissites,
            bg=self._szinek["kiemeles"],
            fg="#ffffff",
            activebackground=self._szinek["kiemeles_sotet"],
            activeforeground="#ffffff",
            bd=0,
            padx=18,
            pady=10,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
        )
        frissites_gomb.grid(row=0, column=1, rowspan=2, sticky="e")

    def _oldalsav_felepitese(self) -> None:
        logo = tk.Label(
            self._oldalsav,
            text="Duna\nWings",
            bg=self._szinek["sotet"],
            fg="#ffffff",
            justify="left",
            font=("Segoe UI", 24, "bold"),
        )
        logo.pack(anchor="w", padx=24, pady=(28, 4))

        leiras = tk.Label(
            self._oldalsav,
            text="Repülőjegy Foglalási Rendszer",
            bg=self._szinek["sotet"],
            fg="#b9c7d8",
            justify="left",
            font=("Segoe UI", 10),
        )
        leiras.pack(anchor="w", padx=24, pady=(0, 28))

        self.menu_gombok: dict[str, tk.Button] = {}
        menupontok = [
            ("jaratok", "Járatok listázása"),
            ("foglalas", "Jegy foglalása"),
            ("lemondas", "Foglalás lemondása"),
            ("foglalasok", "Foglalások listázása"),
        ]

        for kulcs, felirat in menupontok:
            gomb = tk.Button(
                self._oldalsav,
                text=felirat,
                anchor="w",
                command=lambda nez=kulcs: self.nezet_valtas(nez),
                bg=self._szinek["sotet"],
                fg="#e7edf5",
                activebackground="#2b3d52",
                activeforeground="#ffffff",
                bd=0,
                padx=24,
                pady=13,
                cursor="hand2",
                font=("Segoe UI", 11, "bold"),
            )
            gomb.pack(fill="x", padx=12, pady=3)
            self.menu_gombok[kulcs] = gomb

        also_panel = tk.Frame(self._oldalsav, bg=self._szinek["sotet"])
        also_panel.pack(side="bottom", fill="x", padx=24, pady=24)

        self.statusz_label = tk.Label(
            also_panel,
            text="Kész",
            bg=self._szinek["sotet"],
            fg="#b9c7d8",
            wraplength=190,
            justify="left",
            font=("Segoe UI", 9),
        )
        self.statusz_label.pack(anchor="w")

    def _nezetek_felepitese(self) -> None:
        self.nezet_tarolo = tk.Frame(self._tartalom, bg=self._szinek["hatter"])
        self.nezet_tarolo.grid(row=1, column=0, sticky="nsew", padx=28, pady=(0, 24))
        self.nezet_tarolo.grid_columnconfigure(0, weight=1)
        self.nezet_tarolo.grid_rowconfigure(0, weight=1)

        self.nezetek: dict[str, tk.Frame] = {}
        self.nezetek["jaratok"] = self._jaratok_nezet()
        self.nezetek["foglalas"] = self._foglalas_nezet()
        self.nezetek["lemondas"] = self._lemondas_nezet()
        self.nezetek["foglalasok"] = self._foglalasok_nezet()

        for frame in self.nezetek.values():
            frame.grid(row=0, column=0, sticky="nsew")

    def _kartya(self, szulo: tk.Widget) -> tk.Frame:
        kartya = tk.Frame(
            szulo,
            bg=self._szinek["panel"],
            highlightbackground=self._szinek["vonal"],
            highlightthickness=1,
            bd=0,
        )
        return kartya

    def _jaratok_nezet(self) -> tk.Frame:
        frame = tk.Frame(self.nezet_tarolo, bg=self._szinek["hatter"])
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        stat_panel = tk.Frame(frame, bg=self._szinek["hatter"])
        stat_panel.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        for oszlop in range(3):
            stat_panel.grid_columnconfigure(oszlop, weight=1)

        self.jaratok_stat_label = self._stat_kartya(stat_panel, "Járatok", "0")
        self.foglalasok_stat_label = self._stat_kartya(stat_panel, "Foglalások", "0")
        self.helyek_stat_label = self._stat_kartya(stat_panel, "Szabad helyek", "0")

        tabla_kartya = self._kartya(frame)
        tabla_kartya.grid(row=1, column=0, sticky="nsew")
        tabla_kartya.grid_columnconfigure(0, weight=1)
        tabla_kartya.grid_rowconfigure(0, weight=1)

        self.jaratok_tabla = self._tabla(
            tabla_kartya,
            ("jaratszam", "tipus", "cel", "indulas", "erkezes", "ar", "szabad"),
            ("Járatszám", "Típus", "Célállomás", "Indulás", "Érkezés", "Ár", "Szabad hely"),
        )
        self.jaratok_tabla.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)
        self.jaratok_tabla.bind("<<TreeviewSelect>>", self._jarat_kivalasztva)

        return frame

    def _stat_kartya(self, szulo: tk.Widget, cim: str, ertek: str) -> tk.Label:
        kartya = self._kartya(szulo)
        oszlop = len(szulo.grid_slaves())
        kartya.grid(row=0, column=oszlop, sticky="ew", padx=(0 if oszlop == 0 else 12, 0))

        tk.Label(
            kartya,
            text=cim,
            bg=self._szinek["panel"],
            fg=self._szinek["muted"],
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", padx=16, pady=(14, 0))

        label = tk.Label(
            kartya,
            text=ertek,
            bg=self._szinek["panel"],
            fg=self._szinek["sotet"],
            font=("Segoe UI", 24, "bold"),
        )
        label.pack(anchor="w", padx=16, pady=(2, 14))
        return label

    def _foglalas_nezet(self) -> tk.Frame:
        frame = tk.Frame(self.nezet_tarolo, bg=self._szinek["hatter"])
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        urlap = self._kartya(frame)
        urlap.grid(row=0, column=0, sticky="nsew", padx=(0, 16))
        urlap.grid_columnconfigure(0, weight=1)

        tk.Label(
            urlap,
            text="Új jegyfoglalás",
            bg=self._szinek["panel"],
            fg=self._szinek["sotet"],
            font=("Segoe UI", 18, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=22, pady=(22, 4))

        tk.Label(
            urlap,
            text="Add meg az utas nevét, majd válassz egy elérhető járatot.",
            bg=self._szinek["panel"],
            fg=self._szinek["muted"],
            font=("Segoe UI", 10),
        ).grid(row=1, column=0, sticky="w", padx=22, pady=(0, 18))

        tk.Label(
            urlap,
            text="Utas neve",
            bg=self._szinek["panel"],
            fg=self._szinek["szoveg"],
            font=("Segoe UI", 10, "bold"),
        ).grid(row=2, column=0, sticky="w", padx=22, pady=(0, 6))

        self.utas_nev_entry = tk.Entry(
            urlap,
            bg="#f9fbfd",
            fg=self._szinek["szoveg"],
            bd=0,
            highlightthickness=1,
            highlightbackground=self._szinek["vonal"],
            highlightcolor=self._szinek["kiemeles"],
            font=("Segoe UI", 12),
        )
        self.utas_nev_entry.grid(row=3, column=0, sticky="ew", padx=22, ipady=9)

        tk.Label(
            urlap,
            text="Járat",
            bg=self._szinek["panel"],
            fg=self._szinek["szoveg"],
            font=("Segoe UI", 10, "bold"),
        ).grid(row=4, column=0, sticky="w", padx=22, pady=(18, 6))

        self.jarat_combobox = ttk.Combobox(urlap, state="readonly", font=("Segoe UI", 11))
        self.jarat_combobox.grid(row=5, column=0, sticky="ew", padx=22, ipady=4)
        self.jarat_combobox.bind("<<ComboboxSelected>>", lambda _event: self._foglalas_reszletek_frissitese())

        self.foglalas_reszletek_label = tk.Label(
            urlap,
            text="",
            bg=self._szinek["panel"],
            fg=self._szinek["muted"],
            justify="left",
            font=("Segoe UI", 10),
        )
        self.foglalas_reszletek_label.grid(row=6, column=0, sticky="w", padx=22, pady=(16, 0))

        foglalas_gomb = tk.Button(
            urlap,
            text="Jegy foglalása",
            command=self.jegy_foglalasa,
            bg=self._szinek["kiemeles"],
            fg="#ffffff",
            activebackground=self._szinek["kiemeles_sotet"],
            activeforeground="#ffffff",
            bd=0,
            padx=18,
            pady=13,
            cursor="hand2",
            font=("Segoe UI", 11, "bold"),
        )
        foglalas_gomb.grid(row=7, column=0, sticky="ew", padx=22, pady=(26, 22))

        jobb_oldal = self._kartya(frame)
        jobb_oldal.grid(row=0, column=1, sticky="nsew")
        jobb_oldal.grid_columnconfigure(0, weight=1)
        jobb_oldal.grid_rowconfigure(1, weight=1)

        tk.Label(
            jobb_oldal,
            text="Választható járatok",
            bg=self._szinek["panel"],
            fg=self._szinek["sotet"],
            font=("Segoe UI", 15, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=18, pady=(18, 0))

        self.foglalas_jaratok_tabla = self._tabla(
            jobb_oldal,
            ("jaratszam", "cel", "indulas", "ar", "szabad"),
            ("Járat", "Cél", "Indulás", "Ár", "Szabad"),
            magassag=12,
        )
        self.foglalas_jaratok_tabla.grid(row=1, column=0, sticky="nsew", padx=16, pady=16)
        self.foglalas_jaratok_tabla.bind("<<TreeviewSelect>>", self._foglalasi_tabla_kivalasztva)

        return frame

    def _lemondas_nezet(self) -> tk.Frame:
        frame = tk.Frame(self.nezet_tarolo, bg=self._szinek["hatter"])
        frame.grid_columnconfigure(0, minsize=360)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        panel = self._kartya(frame)
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 16))
        panel.grid_columnconfigure(0, weight=1)

        tk.Label(
            panel,
            text="Foglalás lemondása",
            bg=self._szinek["panel"],
            fg=self._szinek["sotet"],
            font=("Segoe UI", 18, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=22, pady=(22, 4))

        tk.Label(
            panel,
            text="Válaszd ki a listából, vagy írd be a foglalási azonosítót.",
            bg=self._szinek["panel"],
            fg=self._szinek["muted"],
            wraplength=300,
            justify="left",
            font=("Segoe UI", 10),
        ).grid(row=1, column=0, sticky="w", padx=22, pady=(0, 18))

        tk.Label(
            panel,
            text="Foglalási azonosító",
            bg=self._szinek["panel"],
            fg=self._szinek["szoveg"],
            font=("Segoe UI", 10, "bold"),
        ).grid(row=2, column=0, sticky="w", padx=22, pady=(0, 6))

        self.lemondas_entry = tk.Entry(
            panel,
            bg="#f9fbfd",
            fg=self._szinek["szoveg"],
            bd=0,
            highlightthickness=1,
            highlightbackground=self._szinek["vonal"],
            highlightcolor=self._szinek["kiemeles"],
            font=("Segoe UI", 12),
        )
        self.lemondas_entry.grid(row=3, column=0, sticky="ew", padx=22, ipady=9)

        lemondas_gomb = tk.Button(
            panel,
            text="Foglalás lemondása",
            command=self.foglalas_lemondasa,
            bg=self._szinek["hiba"],
            fg="#ffffff",
            activebackground="#8a1c13",
            activeforeground="#ffffff",
            bd=0,
            padx=18,
            pady=13,
            cursor="hand2",
            font=("Segoe UI", 11, "bold"),
        )
        lemondas_gomb.grid(row=4, column=0, sticky="ew", padx=22, pady=(24, 22))

        tabla_kartya = self._kartya(frame)
        tabla_kartya.grid(row=0, column=1, sticky="nsew")
        tabla_kartya.grid_columnconfigure(0, weight=1)
        tabla_kartya.grid_rowconfigure(0, weight=1)

        self.lemondas_tabla = self._foglalas_tabla(tabla_kartya)
        self.lemondas_tabla.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)
        self.lemondas_tabla.bind("<<TreeviewSelect>>", self._lemondas_kivalasztva)

        return frame

    def _foglalasok_nezet(self) -> tk.Frame:
        frame = tk.Frame(self.nezet_tarolo, bg=self._szinek["hatter"])
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        tabla_kartya = self._kartya(frame)
        tabla_kartya.grid(row=0, column=0, sticky="nsew")
        tabla_kartya.grid_columnconfigure(0, weight=1)
        tabla_kartya.grid_rowconfigure(0, weight=1)

        self.foglalasok_tabla = self._foglalas_tabla(tabla_kartya)
        self.foglalasok_tabla.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)

        return frame

    def _tabla(
        self,
        szulo: tk.Widget,
        oszlopok: tuple[str, ...],
        fejlecek: tuple[str, ...],
        magassag: int = 14,
    ) -> ttk.Treeview:
        tarolo = tk.Frame(szulo, bg=self._szinek["panel"])
        tarolo.grid_columnconfigure(0, weight=1)
        tarolo.grid_rowconfigure(0, weight=1)

        tabla = ttk.Treeview(tarolo, columns=oszlopok, show="headings", height=magassag)
        gorgeto = ttk.Scrollbar(tarolo, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=gorgeto.set)

        for azonosito, fejlec in zip(oszlopok, fejlecek):
            tabla.heading(azonosito, text=fejlec)
            tabla.column(azonosito, width=120, anchor="w", stretch=True)

        tabla.grid(row=0, column=0, sticky="nsew")
        gorgeto.grid(row=0, column=1, sticky="ns")
        return tarolo

    def _foglalas_tabla(self, szulo: tk.Widget) -> tk.Frame:
        tabla_tarolo = self._tabla(
            szulo,
            ("azonosito", "utas", "jarat", "cel", "indulas", "ar"),
            ("Azonosító", "Utas", "Járat", "Célállomás", "Indulás", "Ár"),
            magassag=15,
        )
        return tabla_tarolo

    def _treeview(self, tarolo: tk.Frame) -> ttk.Treeview:
        return next(
            gyerek for gyerek in tarolo.winfo_children()
            if isinstance(gyerek, ttk.Treeview)
        )

    def nezet_valtas(self, nezet: str) -> None:
        self._aktiv_nezet = nezet
        self.nezetek[nezet].tkraise()

        cimek = {
            "jaratok": "Járatok áttekintése",
            "foglalas": "Jegy foglalása",
            "lemondas": "Foglalás lemondása",
            "foglalasok": "Foglalások listázása",
        }
        alcimek = {
            "jaratok": "Az összes járat, ár, indulási idő és szabad hely egy helyen.",
            "foglalas": "Új jegy létrehozása név és járatszám alapján.",
            "lemondas": "Meglévő foglalás törlése foglalási azonosítóval.",
            "foglalasok": "Az aktuálisan élő foglalások teljes listája.",
        }
        self.cim_label.config(text=cimek[nezet])
        self.alcim_label.config(text=alcimek[nezet])

        for kulcs, gomb in self.menu_gombok.items():
            if kulcs == nezet:
                gomb.config(bg=self._szinek["kiemeles"], fg="#ffffff")
            else:
                gomb.config(bg=self._szinek["sotet"], fg="#e7edf5")

        self.statusz_label.config(text=f"Aktív menüpont: {cimek[nezet]}")

    def frissites(self) -> None:
        self._jaratok_frissitese()
        self._foglalasok_frissitese()
        self._foglalas_valaszto_frissitese()
        self.nezet_valtas(self._aktiv_nezet)

    def _jaratok_frissitese(self) -> None:
        jarat_tabla = self._treeview(self.jaratok_tabla)
        foglalas_tabla = self._treeview(self.foglalas_jaratok_tabla)
        self._tabla_torlese(jarat_tabla)
        self._tabla_torlese(foglalas_tabla)

        szabad_helyek_osszesen = 0
        for jarat in self.rendszer.legitarsasag.jaratok:
            szabad_hely = self.rendszer.szabad_helyek(jarat.jaratszam)
            szabad_helyek_osszesen += szabad_hely
            jarat_tabla.insert(
                "",
                "end",
                iid=jarat.jaratszam,
                values=(
                    jarat.jaratszam,
                    jarat.jarat_tipus(),
                    jarat.celallomas,
                    datum_formazasa(jarat.indulasi_ido),
                    datum_formazasa(jarat.erkezesi_ido),
                    penz_formazasa(jarat.jegyar),
                    szabad_hely,
                ),
            )
            foglalas_tabla.insert(
                "",
                "end",
                iid=jarat.jaratszam,
                values=(
                    jarat.jaratszam,
                    jarat.celallomas,
                    datum_formazasa(jarat.indulasi_ido),
                    penz_formazasa(jarat.jegyar),
                    szabad_hely,
                ),
            )

        self.jaratok_stat_label.config(text=str(len(self.rendszer.legitarsasag.jaratok)))
        self.foglalasok_stat_label.config(text=str(len(self.rendszer.foglalasok)))
        self.helyek_stat_label.config(text=str(szabad_helyek_osszesen))

    def _foglalasok_frissitese(self) -> None:
        for tabla_tarolo in (self.foglalasok_tabla, self.lemondas_tabla):
            tabla = self._treeview(tabla_tarolo)
            self._tabla_torlese(tabla)

            for foglalas in self.rendszer.foglalasok:
                jarat = foglalas.jarat
                tabla.insert(
                    "",
                    "end",
                    iid=foglalas.foglalasi_azonosito,
                    values=(
                        foglalas.foglalasi_azonosito,
                        foglalas.utas_nev,
                        jarat.jaratszam,
                        jarat.celallomas,
                        datum_formazasa(jarat.indulasi_ido),
                        penz_formazasa(foglalas.ar),
                    ),
                )

    def _foglalas_valaszto_frissitese(self) -> None:
        ertekek = []
        for jarat in self.rendszer.legitarsasag.jaratok:
            szabad_hely = self.rendszer.szabad_helyek(jarat.jaratszam)
            ertekek.append(
                f"{jarat.jaratszam} - {jarat.celallomas} - "
                f"{penz_formazasa(jarat.jegyar)} - {szabad_hely} szabad hely"
            )

        self._jarat_valaszto_ertekek = ertekek
        self.jarat_combobox["values"] = ertekek
        if ertekek and not self.jarat_combobox.get():
            self.jarat_combobox.current(0)
        self._foglalas_reszletek_frissitese()

    def _foglalas_reszletek_frissitese(self) -> None:
        jaratszam = self._kivalasztott_jaratszam()
        if not jaratszam:
            self.foglalas_reszletek_label.config(text="Nincs kiválasztott járat.")
            return

        try:
            jarat = self.rendszer.legitarsasag.jarat_keresese(jaratszam)
            self.foglalas_reszletek_label.config(
                text=(
                    f"Típus: {jarat.jarat_tipus()}\n"
                    f"Célállomás: {jarat.celallomas}\n"
                    f"Indulás: {datum_formazasa(jarat.indulasi_ido)}\n"
                    f"Ár: {penz_formazasa(jarat.jegyar)}\n"
                    f"Szabad hely: {self.rendszer.szabad_helyek(jarat.jaratszam)}"
                )
            )
        except FoglalasiHiba as hiba:
            self.foglalas_reszletek_label.config(text=str(hiba))

    def jegy_foglalasa(self) -> None:
        jaratszam = self._kivalasztott_jaratszam()
        utas_nev = self.utas_nev_entry.get().strip()

        try:
            foglalas = self.rendszer.jegy_foglalasa(utas_nev, jaratszam)
        except (AdatValidaciosHiba, FoglalasiHiba) as hiba:
            messagebox.showerror("Sikertelen foglalás", str(hiba))
            return

        self.utas_nev_entry.delete(0, tk.END)
        self.frissites()
        messagebox.showinfo(
            "Sikeres foglalás",
            (
                f"Foglalási azonosító: {foglalas.foglalasi_azonosito}\n"
                f"Utas: {foglalas.utas_nev}\n"
                f"Fizetendő ár: {penz_formazasa(foglalas.ar)}"
            ),
        )
        self.nezet_valtas("foglalasok")

    def foglalas_lemondasa(self) -> None:
        azonosito = self.lemondas_entry.get().strip().upper()
        if not azonosito:
            messagebox.showwarning("Hiányzó azonosító", "Add meg a foglalási azonosítót.")
            return

        if not messagebox.askyesno(
            "Megerősítés",
            f"Biztosan lemondod ezt a foglalást?\n\n{azonosito}",
        ):
            return

        try:
            torolt = self.rendszer.foglalas_lemondasa(azonosito)
        except FoglalasiHiba as hiba:
            messagebox.showerror("Sikertelen lemondás", str(hiba))
            return

        self.lemondas_entry.delete(0, tk.END)
        self.frissites()
        messagebox.showinfo(
            "Foglalás lemondva",
            f"A foglalás sikeresen lemondva:\n{torolt.foglalasi_azonosito} - {torolt.utas_nev}",
        )

    def _jarat_kivalasztva(self, _event: tk.Event) -> None:
        tabla = self._treeview(self.jaratok_tabla)
        kivalasztott = tabla.selection()
        if not kivalasztott:
            return
        jaratszam = kivalasztott[0]
        self._combobox_jarat_beallitasa(jaratszam)

    def _foglalasi_tabla_kivalasztva(self, _event: tk.Event) -> None:
        tabla = self._treeview(self.foglalas_jaratok_tabla)
        kivalasztott = tabla.selection()
        if not kivalasztott:
            return
        self._combobox_jarat_beallitasa(kivalasztott[0])

    def _lemondas_kivalasztva(self, _event: tk.Event) -> None:
        tabla = self._treeview(self.lemondas_tabla)
        kivalasztott = tabla.selection()
        if not kivalasztott:
            return
        self.lemondas_entry.delete(0, tk.END)
        self.lemondas_entry.insert(0, kivalasztott[0])

    def _combobox_jarat_beallitasa(self, jaratszam: str) -> None:
        for index, ertek in enumerate(self._jarat_valaszto_ertekek):
            if ertek.startswith(jaratszam):
                self.jarat_combobox.current(index)
                self._foglalas_reszletek_frissitese()
                return

    def _kivalasztott_jaratszam(self) -> str:
        ertek = self.jarat_combobox.get().strip()
        if not ertek:
            return ""
        return ertek.split(" - ", 1)[0].upper()

    @staticmethod
    def _tabla_torlese(tabla: ttk.Treeview) -> None:
        for elem in tabla.get_children():
            tabla.delete(elem)


def main() -> None:
    app = RepulojegyApp()
    app.mainloop()


if __name__ == "__main__":
    main()
