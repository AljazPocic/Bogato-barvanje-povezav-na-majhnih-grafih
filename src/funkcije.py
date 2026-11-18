from sage.all import graphs, Graph

import csv
from pathlib import Path
from time import perf_counter

from src.rich import lower_bound
from src.ilp import rich_chromatic_index_ilp
from src.sat import rich_chromatic_index_sat



##########################################################################################################################
# H_0

# H_0 je definiran kot graf, ki ga dobimo iz popolnega grafa K_4, tako da eno povezavo razdelimo z novim vozliščem
# torej ima H_0 5 vozlišč in 7 povezav; 4 vozlišča s stopnjo 3 in 1 vozlišče s stopnjo 2
# velja, da je bogati kromatični indeks enak 6

# Graf H_0: iz K4 odstranimo povezavo (0, 1)
# in jo nadomestimo z 0 -- 4 -- 1.
K4 = graphs.CompleteGraph(4)
H0 = Graph([
    (0, 2),
    (0, 3),
    (1, 2),
    (1, 3),
    (2, 3),
    (0, 4),
    (1, 4)
])


# preverjamo z izomorfnostjo
# dva grafa sta si med sabo izomorfna, če imata enako strukturo(tudi če je narisan drugače, ali imajo vozlišča drugačna imena)
# H_0 se bo pri nas pojavljal pri subkubičnih grafih (kubični grafi ne morejo biti H_0)

def je_H0(G):
    """Preveri, ali je graf G izomorfen grafu H_0."""
    return G.is_isomorphic(H0)


##########################################################################################################################
# funkcija, ki preveri ali je graf subkubičnen in ali je kubičen

def preveri_stopnjo(G):
    """Vrne, ali je graf subkubičen in ali je kubičen."""

    stopnje = G.degree()

    subkubicen = all(d <= 3 for d in stopnje)
    kubicen = all(d == 3 for d in stopnje)

    return subkubicen, kubicen


##########################################################################################################################
# funkcija, ki testira posamezen graf


# pisanje csv datoteke, kjer ena vrstica = ena metoda na enem grafu
# za vsak graf dve vrstici z dvema metodama


# v vrstci: družina grafov, parametri(n,k,...), število vozlišč, število povezav, ali je graf izomorfen H_0, spodnja meja, kubičnost, graph6 (= da ga lahko poustvarimo) = nevem če to rabimo
# metoda(ILP ali SAT): za vsako bogato barvanje 5(ali obstaja bogato barvanje z največ 5 = DA/NE) in bogati kromatični indeks(natančno
# najmanjše število barv), čas izvajanja v sekundah


# POPRAVI IMENA IN TUDI V CSV DATOTEKI
CSV_POLJA = [
    "druzina",
    "parametri",
    "st_vozlisc",
    "st_povezav",
    "je_H0",
    "spodnja_meja",
    "metoda",
    "barvanje_5",
    "kr_indeks",
    "cas_s",
    "graph6",
    "subkubicen",
    "kubicen",
    "status",
    "napaka"
]

KOREN_PROJEKTA = Path(__file__).resolve().parent.parent
CSV_POT = KOREN_PROJEKTA / "rezultati" / "rezultati.csv"

def shrani_v_csv(vrstica, pot=CSV_POT):
    """Doda eno vrstico v obstoječo CSV datoteko."""
    pot = Path(pot)
    # preverimo imena stolpcev
    with pot.open("r", newline="", encoding="utf-8-sig") as f:
        glava = next(csv.reader(f, delimiter=";"), None)
    if glava != CSV_POLJA:
        raise ValueError(
            "Stolpci v CSV datoteki se ne ujemajo s CSV_POLJA."
        )
    # dodamo
    with pot.open("a", newline="", encoding="utf-8") as f:
        dodaj = csv.DictWriter(
            f,
            fieldnames=CSV_POLJA,
            delimiter=";"
        )
        dodaj.writerow(vrstica)



# funkcija, ki izračuna s posamezno metodo
# za G izračuna bogati kromatični indeks glede na metodo, izmeri čas izvajanja
def izracunaj_z_metodo(G, metoda):
    """Izračuna bogati kromatični indeks z ILP ali SAT."""
    # začetek merjenja časa:
    zacetek = perf_counter()
    
    try:
        if metoda == "ILP":
            kr_indeks, barvanje = rich_chromatic_index_ilp(G)

        elif metoda == "SAT":
            kr_indeks, barvanje = rich_chromatic_index_sat(G)

        # izračunan čas izvajanja:
        cas = perf_counter() - zacetek
        # funkcija vrne slovar z petimi podatki
        return {
            "barvanje_5": "DA" if kr_indeks <= 5 else "NE", # ali ima graf bogato barvanje z največ 5 barvami?
            "kr_indeks": int(kr_indeks), # izračunan bogati kromatični indeks
            "cas_s": round(cas, 6), # čas izvajanja v sekundah, zaokrožen na 6 decimalke
            "status": "OK",
            "napaka": ""
        }
    # napake:
    except Exception as e:
        # kdaj se je zgodila napaka
        cas = perf_counter() - zacetek
        # kaj je bilo narobe
        return {
            "barvanje_5": "NAPAKA",
            "kr_indeks": "",
            "cas_s": round(cas, 6),
            "status": "NAPAKA",
            "napaka": f"{type(e).__name__}: {e}"
        }


# glavna funkcija
def zapis_csv(G, druzina, parametri, pot_csv=CSV_POT):
    """Graf G preveri z metodama ILP in SAT. Rezultate obeh metod shrani v CSV datoteko."""
    # preverimo, ali je graf povezan:
    if not G.is_connected():
        raise ValueError("Graf ni povezan.")
    # preverimo, ali je graf subkubičen oziroma kubičen.
    subkubicen, kubicen = preveri_stopnjo(G)
    if not subkubicen:
        raise ValueError("Graf ni subkubičen.")
    # skupni podatki o grafu, ki veljajo za obe metodi:
    skupni_podatki = {
        "druzina": druzina,
        "parametri": parametri,
        "st_vozlisc": G.order(),
        "st_povezav": G.size(),
        "je_H0": "DA" if je_H0(G) else "NE",
        "spodnja_meja": int(lower_bound(G)),
        "graph6": G.graph6_string(),
        "subkubicen": "DA" if subkubicen else "NE",
        "kubicen": "DA" if kubicen else "NE"
    }
    # tukaj bomo shranili rezultate za obe metodi:
    rezultati = {}
    # pogledamo obe metodi preko for zanke:
    for metoda in ("ILP", "SAT"):
        rezultat = izracunaj_z_metodo(G, metoda)
        # pripravimo vrstico za CSV:
        vrstica = {
            **skupni_podatki,
            "metoda": metoda,
            **rezultat
        }
        # shranimo vrstico:
        shrani_v_csv(vrstica, pot_csv)
        rezultati[metoda] = rezultat
    