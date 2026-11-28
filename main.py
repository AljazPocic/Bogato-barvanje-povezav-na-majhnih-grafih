# klicanje funkcij in dodajanje
from src.subkubicni import prizma, posplosen_petersonov, mobiusova_lestev, ravninski_kubicni, ravninski_subkubicni, fulereni, snarks_4
from src.funkcije import CSV_POT1, CSV_POT2, CSV_POT3, CSV_POT4_k, CSV_POT4_s, CSV_POT5, CSV_POT6, zapis_csv

##########################################################################################################################
# PRIZME

# for n in range(3, 33):
#
#     G = prizma(n)
#
#     for metoda in ("ILP", "SAT"):
#
#         zapis_csv(
#             G,
#             druzina="prizma",
#             parametri=f"n={n}",
#             metoda=metoda,
#             pot_csv=CSV_POT1
#         )
#
#     print(f"Dolžina cikla n: {n}, število vozlišč: {2*n}", flush=True)

# opravljeno testiranje za prizme z n = 3, ..., 32 (6 do 64 vozlišč), z metodama ILP in SAT
# rezultati so shranjeni v "rezultati1.csv"


# Za večje prizme uporabljamo spodnjo funkcijo (samo SAT, ker je bistveno hitrejši od ILP).
# Uporaba je najboljša v terminalu

def testiraj_prizme(n_od, n_do, korak=1, pot_csv=CSV_POT1):
    """Testira Domnevo 2 na prizmah C_n □ K_2 z metodo SAT in rezultate zapiše v CSV.

    n_od, n_do : najmanjša in največja dolžina cikla n (OBE meji sta vključeni);
                 prizma z dolžino cikla n ima 2n vozlišč, n mora biti vsaj 3
    korak      : razmik med zaporednimi n (privzeto 1)
    pot_csv    : CSV datoteka, kamor se zapisujejo rezultati (privzeto rezultati1.csv)
    """
    for n in range(n_od, n_do + 1, korak):

        G = prizma(n)

        zapis_csv(
            G,
            druzina="prizma",
            parametri=f"n={n}",
            metoda="SAT",
            pot_csv=pot_csv
        )

        print(f"Dolžina cikla n: {n}, število vozlišč: {2*n}", flush=True)


##########################################################################################################################
# MÖBIUSOVE LESTVE(CIRKULANTI C_(2n)(1,n))

def testiraj_mobiusove_lestve(n_od, n_do, korak=1, pot_csv=CSV_POT2):
    """ Testira Möbiusove lestve C_(2n)(1,n)

    n_od, n_do : najmanjša in največja dolžina cikla n (OBE meji sta vključeni);
                 prizma z dolžino cikla n ima 2n vozlišč, n mora biti vsaj 3
    korak      : razmik med zaporednimi n (privzeto 1)
    pot_csv    : CSV datoteka, kamor se zapisujejo rezultati (privzeto rezultati1.csv)
    """
    for n in range(n_od, n_do + 1, korak):
        G = mobiusova_lestev(n)

        zapis_csv(
            G,
            druzina="mobiusova_lestev",
            parametri=f"n={n}",
            metoda="ILP",
            pot_csv=pot_csv
            )

        print(f"Möbiusova lestev n={n}, število vozlišč: {2*n}", flush=True)

# opravljeno testiranje za Möbiusove lestve z vozlišči od 3 do 33
# rezultati so shranjeni v "rezultati2.csv"


##########################################################################################################################
# POSPLOŠENI PETERSONOVI GRAFI P(n,k)
# pogoj: n >= 3 in 1 <= k < n/2 (sicer graf ni kubičen); graf ima 2n vozlišč in 3n povezav
# k = 1 izpustimo, ker je P(n,1) prizma C_n □ K_2 
#
# Pri istem n so lahko različni k izomorfni: P(n,k) ≅ P(n,l), če je k*l ≡ ±1 (mod n),
# npr. P(7,2) ≅ P(7,3). Da istega grafa ne testiramo dvakrat, si za vsak n zapomnimo
# kanonične oznake (graph6) že testiranih grafov in izomorfne duplikate preskočimo.
# (Grafi z različnim n imajo različno število vozlišč, zato med njimi duplikatov ni.)


def testiraj_petersen(n_od, n_do, korak=1, pot_csv=CSV_POT3):
    """Testira Domnevo 2 na posplošenih Petersenovih grafih P(n,k), k >= 2, z metodo SAT.

    Za vsak n testira vse k = 2, ..., floor((n-1)/2), pri čemer izomorfne duplikate
    (pri istem n) preskoči. Rezultate zapiše v CSV.

    n_od, n_do : najmanjši in največji n (OBE meji sta vključeni); P(n,k) ima 2n vozlišč.
                 Prvi graf s k >= 2 je pri n = 5 (Petersenov graf P(5,2)).
    korak      : razmik med zaporednimi n (privzeto 1)
    pot_csv    : CSV datoteka, kamor se zapisujejo rezultati (privzeto rezultati3.csv)
    """
    for n in range(n_od, n_do + 1, korak):

        testirani = set()  # kanonične oznake grafov, ki smo jih pri tem n že testirali
        st_testiranih = 0
        st_preskocenih = 0

        # k teče od 2 do največjega k, za katerega velja 2k < n
        for k in range(2, (n - 1) // 2 + 1):

            G = posplosen_petersonov(n, k)

            # kanonična oznaka: izomorfna grafa imata enak graph6 niz
            oznaka = G.canonical_label().graph6_string()
            if oznaka in testirani:
                st_preskocenih += 1  # izomorfen že testiranemu P(n,l) -> preskočimo
                continue
            testirani.add(oznaka)

            zapis_csv(
                G,
                druzina="posplosen_petersen",
                parametri=f"n={n},k={k}",
                metoda="SAT",
                pot_csv=pot_csv
            )
            st_testiranih += 1

        print(
            f"n = {n} ({2*n} vozlišč): testiranih {st_testiranih}, "
            f"preskočenih izomorfnih {st_preskocenih}",
            flush=True
        )



##########################################################################################################################
# RAVNINSKI KUBIČNI GRAFI


#kubični graf mora imeti sodo število n, vsaj 4
def testiraj_ravninske_kubicne(n_od, n_do, korak=2, pot_csv=CSV_POT4_k, metode=("ILP", "SAT")):
    for n in range(n_od, n_do + 1, korak):

        for i, G in enumerate(ravninski_kubicni(n), start=1):

            for metoda in metode:

                zapis_csv(
                    G,
                    druzina="ravninski_kubicni",
                    parametri=f"n={n},graf={i}",
                    metoda=metoda,
                    pot_csv=pot_csv
                )
    
        print(f"Število vozlišč: {n}")

# opravljeno testiranje za kubične ravninske grafe s 4, 6, 8, 10, 12, 14, 16, 18 in 20 vozlišči
# rezultati so shranjeni v "rezultati4_k.csv"

# z metodo SAT je bilo opravljeno testiranje za kubične ravninske grafe s 22 vozlišči(testiranje ročno prekinjeno po 129 620 grafih)


##########################################################################################################################
# RAVNINSKI SUBKUBIČNI GRAFI  

# za subkubične ravninske grafe bomo uporabili spodnjo funkcijo(samo SAT, ker je hitrejša)
# pri tem se bodo nekateri grafi ponovili s tistimi zgoraj, ker med subkubične spadajo tudi kubični

def testiraj_ravninske_subkubicne(n_od, n_do, korak=1, pot_csv=CSV_POT4_s):
    for n in range(n_od, n_do + 1, korak):

        for i, G in enumerate(ravninski_subkubicni(n), start=1):

            zapis_csv(
                G,
                druzina="ravninski_subkubicni",
                parametri=f"n={n},graf={i}",
                metoda="SAT",
                pot_csv=pot_csv
            )

        print(f"Število vozlišč: {n}")


# opravljeno testiranje za ravninske subkubične grafe z vozlišči od 4 do 12
# rezultati so shranjeni v "rezultati4_s.csv"





##########################################################################################################################
# FULERENI
# potrebno je instalirati paket "buckygen"

# Fulerenski grafi imajo:
#- sodo število vozlišč,
#- najmanj 20 vozlišč,
#- 22 vozlišč ni dovoljenih,
#- vsa vozlišča imajo stopnjo 3.

def testiraj_fulereni(n_od, n_do, korak=2, pot_csv=CSV_POT5):
    """Testira fulerenske grafe z metodama SAT in ILP."""

    for n in range(n_od, n_do + 1, korak):
        if n < 20 or n > 254 or n % 2 != 0 or n == 22:
            print(f"Preskočimo n={n}: neveljavna velikost za fuleren.")
            continue

        G_generirani = fulereni(n)

        st_testiranih = 0

        for i, G in enumerate(G_generirani, start=1):
            for metoda in ["ILP", "SAT"]:
                zapis_csv(
                    G,
                    druzina="fuleren",
                    parametri=f"n={n},graf={i}",
                    metoda=metoda,
                    pot_csv=pot_csv
                )

            st_testiranih += 1

        print(f"Fulereni n={n}: testiranih {st_testiranih} grafov", flush=True)


# opravljeno testiranje za fulerene z vozlišči od 2 do 42
# rezultati so shranjeni v "rezultati5.csv"

##########################################################################################################################
# SNARKI
# uporabimo SAT, saj je hitrejša od ILP

def testiraj_snarke(pot_csv=CSV_POT6, metode=("SAT",)):

    for n, grafi in snarks_4:

        for i, G in enumerate(grafi, start=1):

            for metoda in metode:

                zapis_csv(
                    G,
                    druzina="snark",
                    parametri=f"n={n},graf={i}",
                    metoda=metoda,
                    pot_csv=pot_csv
                )

        print(f"Število vozlišč: {n}")

# opravljeno je bilo testiranje za snarke z obsegom več ali enako 4, z 10, 18, 20, 22, 24, 26, 28 vozlišči
# rezultati so shranjeni v "rezultati6.csv"