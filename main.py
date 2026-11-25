# klicanje funkcij in dodajanje
from src.subkubicni import prizma, posplosen_petersonov, mobiusova_lestev, ravninski_kubicni, ravninski_subkubicni, fulereni
from src.funkcije import CSV_POT1, CSV_POT2, CSV_POT3, CSV_POT4, CSV_POT5, zapis_csv

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








##########################################################################################################################
# POSPLOŠENI PETERSONOVI GRAFI P(n,k)







##########################################################################################################################
# RAVNINSKI SUBKUBIČNI IN KUBIČNI GRAFI


# for n in range(4, 11):
# 
#     for i, G in enumerate(ravninski_subkubicni(n), start=1):
# 
#         for metoda in ("ILP", "SAT"):
# 
#             zapis_csv(
#                 G,
#                 druzina="ravninski_subkubicni",
#                 parametri=f"n={n}, graf={i}",
#                 metoda=metoda,
#                 pot_csv=CSV_POT4
#             )
#         print (f"Št. vozlišč:{n}")



# kubični graf mora imeti sodo število n, vsaj 4
# for n in range(4, 21, 2): # n bodo soda števila med 4 in 20
# 
#     for i, G in enumerate(ravninski_kubicni(n), start=1):
# 
#         for metoda in ("ILP", "SAT"):
# 
#             zapis_csv(
#                 G,
#                 druzina="ravninski_kubicni",
#                 parametri=f"n={n},graf={i}",
#                 metoda=metoda,
#                 pot_csv=CSV_POT4
#             )
#  
#     print(f"Število vozlišč: {n}")

# opravljeno testiranje za kubične ravninske grafe s 4, 6, 8, 10, 12, 14, 16, 18 in 20 vozlišči
# rezultati so shranjeni v "rezultati4.csv"





##########################################################################################################################
# FULERENI
# potrebno je instalirati paket "buckygen"






##########################################################################################################################
# SNARKI
# tbd


