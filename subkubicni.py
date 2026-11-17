from sage.all import graphs, Graph



# PRIZME

def prizma(n): # n bo število vozlišč, ki ga bo imel vsak od dveh ciklov (torej skupno 2n vozlišč)
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