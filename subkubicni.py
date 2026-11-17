from sage.all import graphs, Graph

from src.rich import is_rich_coloring
from src.ilp import rich_coloring_ilp
from src.sat import rich_coloring_sat



# PRIZME

def prizma(n): # n bo število vozlišč, ki ga bo imel vsak od dveh ciklov (torej skupno 2n vozlišč)
    """Generira prizmatični graf z 2n vozlišči."""
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



# MÖBIUSOVE LESTVE(CIRKULANTI C_(2n)(1,n))

def mobiusova_lestev(n):
    """Generira Mobiusovo lestev z 2n vozlišči."""
    return graphs.CirculantGraph(2*n, [1, n])



# POSPLOŠENI PETERSONOVI GRAFI P(n,k)

def posplosen_petersonov(n, k):
    """Generira posplošeni Petersenov graf P(n,k)."""
    return graphs.GeneralizedPetersenGraph(n, k)



# RAVNINSKI KUBIČNI GRAFI

def ravninski_kubicni(n):
    """Generira povezane ravninske kubične grafe z n vozlišči."""
    # st. vozlisc mora biti sodo:
    if n < 4 or n % 2 != 0:
        raise ValueError("n mora biti sodo število >= 4.")
    # vsi povezani kubični:
    generator = graphs.nauty_geng(f"{n} -c -d3 -D3") 
    # izberemo samo ravninske:
    for G in generator:
        if G.is_planar():
            yield G



# FULERENI
# potrebno je instalirati paket "buckygen"

def fulereni(n):
    """Generira vse fulerenske grafe z n vozlišči."""
    return graphs.fullerenes(n)



