from sage.all import graphs, Graph




##########################################################################################################################
# PRIZME
# prizma je vrsta posplošenega petersonovega grafa -> P(n,1) 
# rabimo pazit da se nam tukaj grafi ne bodo ponavljali 


def prizma(n): # n bo število vozlišč, ki ga bo imel vsak od dveh ciklov (torej skupno 2n vozlišč)
    """Generira prizmatični graf z 2n vozlišči."""
    if n < 3:
        raise ValueError("n mora biti vsaj 3.")
    G = Graph() # ustvarimo prazen graf
    # dodamo vozlišča:
    for i in range(n): # zaporedna številka vozlišča
        for j in (0, 1): # kateremu ciklu bo pripadalo vozlišče
            G.add_vertex((i, j))
    # dobimo dva cikla, ki ju moramo povezati
    # dodamo povezave:
    for i in range(n):
        j = (i + 1) % n # trenutno vozlišče želimo povezati z naslednjim; zadnje vozlišče se poveže s prvim in sklene cikel
        G.add_edge((i, 0), (j, 0)) # povezave prvega cikla    
        G.add_edge((i, 1), (j, 1)) # povezave drugega cikla 
        G.add_edge((i, 0), (i, 1)) # Povezave med cikloma
    return G







##########################################################################################################################
# MÖBIUSOVE LESTVE(CIRKULANTI C_(2n)(1,n))


def mobiusova_lestev(n):
    """Generira Mobiusovo lestev z 2n vozlišči."""
    if n < 2:
        raise ValueError("n mora biti vsaj 2.")
    return graphs.CirculantGraph(2*n, [1, n])








##########################################################################################################################
# POSPLOŠENI PETERSONOVI GRAFI P(n,k)



def posplosen_petersonov(n, k):
    """Generira posplošeni Petersenov graf P(n,k)."""
    if n < 3 or k < 1 or 2*k >= n:
        raise ValueError("Potrebno je n >= 3 in 1 <= k < n/2.")
    return graphs.GeneralizedPetersenGraph(n, k)






##########################################################################################################################
# RAVNINSKI KUBIČNI GRAFI


# n mora biti vsaj 4 in sodo
def ravninski_kubicni(n):
    """Generira povezane ravninske kubične grafe z n vozlišči."""
    # st. vozlisc mora biti sodo:
    if n < 4 or n % 2 != 0:
        raise ValueError("n mora biti sodo število >= 4.")
    # vsi povezani kubični:
    generator = graphs.nauty_geng(f"{n} -c -d3 -D3") # -d3 nam pove najmanj 3 povezave, -D3 nam pove največ 3 povezave
    # izberemo samo ravninske:
    for G in generator:
        if G.is_planar():
            yield G



# RAVNINSKI SUBKUBIČNI IN KUBIČNI GRAFI

# kubični graf mora imeti sodo število n, vsaj 4
def ravninski_subkubicni(n):
    """Generira vse povezane ravninske subkubične grafe z n vozlišči."""
    # pogoj za število vozlišč
    if n < 1:
        raise ValueError("n mora biti pozitivno celo število.")
    # generiranje grafov
    generator = graphs.nauty_geng(f"{n} -c -D3") # -D3 nam pove največ 3 povezave
    # izberemo samo ravnisnke:
    for G in generator:
        if G.is_planar():
            yield G






##########################################################################################################################
# FULERENI
# potrebno je instalirati paket "buckygen"


# n mora biti sodo med 20 in 256(256 je buckygen omejitev) ampak ne 22
def fulereni(n):
    """Generira vse fulerenske grafe z n vozlišči."""
    if n < 20 or n > 254 or n % 2 != 0 or n == 22:
        raise ValueError("n mora biti 20 ali sodo število med 24 in 254.")
    return graphs.fullerenes(n)





##########################################################################################################################
# SNARKI
# tbd



