# klicanje funkcij in dodajanje
from src.subkubicni import prizma, posplosen_petersonov, mobiusova_lestev, ravninski_kubicni, ravninski_subkubicni, fulereni
from src.funkcije import CSV_POT1, CSV_POT2, CSV_POT3, CSV_POT4, CSV_POT5, zapis_csv

##########################################################################################################################
# PRIZME







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
for n in range(4, 21, 2): # n bodo soda števila med 4 in 20

    for i, G in enumerate(ravninski_kubicni(n), start=1):

        for metoda in ("ILP", "SAT"):

            zapis_csv(
                G,
                druzina="ravninski_kubicni",
                parametri=f"n={n}, graf={i}",
                metoda=metoda,
                pot_csv=CSV_POT4
            )

    print(f"Število vozlišč: {n}")






##########################################################################################################################
# FULERENI
# potrebno je instalirati paket "buckygen"






##########################################################################################################################
# SNARKI
# tbd


