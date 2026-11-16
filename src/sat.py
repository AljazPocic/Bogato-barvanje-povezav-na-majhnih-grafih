"""Bogato barvanje povezav s SAT solverjem.
Potrebuje paket pycosat.
Uporaba (iz korena repozitorija):
    from src.sat import rich_coloring_sat, rich_chromatic_index_sat
    G = graphs.CompleteGraph(4)
    rich_coloring_sat(G, 4)          # None (s 4 barvami ne gre)
    rich_coloring_sat(G, 5)          # {(0, 1): 0, (0, 2): 1...}
    rich_chromatic_index_sat(G)      # (5, barvanje)"""

import itertools
from sage.sat.solvers.satsolver import SAT
from src.rich import is_rich_coloring, lower_bound


def rich_coloring_sat(G, k, solver="picosat"):
    """Vrne bogato barvanje povezav grafa G s k barvami (0, ..., k-1)
    kot slovar {(u, v): barva} ali None, če tako barvanje ne obstaja.
    Logične spremenljivke:
        x[e, c] povezava e ima barvo c
        r[e]    povezava e je bogata (zahtevamo, da je)"""

    E = G.edges(labels=False, sort=True)
    if not E:
        return {}  # graf brez povezav

    # Pri vozlišču stopnje Δ potrebujemo Δ različnih barv, zato za k < Δ ne gre.
    if k < max(G.degree()):
        return None

    # SAT solver pozna le spremenljivke 1, 2, 3... Negativno število je negacija.
    # Funkcija x() vsakemu ključu, npr. ('x', e, c) ali ('r', e), ob prvi
    # uporabi priredi novo številko in jo shrani v slovar var.
    var = {}
    def x(*key):  # fun sprejme poljub. št. argumentov
        if key not in var:
            var[key] = len(var) + 1
        return var[key]

    S = SAT(solver=solver)

    # Povezave, ki imajo krajišče v
    incident = {v: [e for e in E if v in e] for v in G}

    # 1. pogoj: vsaka povezava ima natanko eno barvo
    for e in E:
        # vsaj ena barva
        S.add_clause(tuple(x('x', e, c) for c in range(k)))
        # največ ena barva
        for c, d in itertools.combinations(range(k), 2):
            S.add_clause((-x('x', e, c), -x('x', e, d)))

    # 2. pogoj (pravilnost): povezavi z istim krajiščem nimata iste barve
    for v in G:
        for e, f in itertools.combinations(incident[v], 2):
            for c in range(k):
                S.add_clause((-x('x', e, c), -x('x', f, c)))

    # 3. pogoj: če je e bogata imata vsaki dve njej sosednji povezavi različni barvi
    for e in E:
        N = [f for f in E if f != e and set(f) & set(e)]
        for f, g in itertools.combinations(N, 2):
            for c in range(k):
                S.add_clause((-x('r', e), -x('x', f, c), -x('x', g, c)))

    # 4. pogoj: vsako neizolirano vozlišče ima vsaj eno bogato povezavo
    for v in G:
        if incident[v]:
            S.add_clause(tuple(x('r', e) for e in incident[v]))

    # Lomljenje simetrij: povezavam pri vozlišču največje stopnje vnaprej
    # določimo barve 0, 1, 2...
    v0 = max(G, key=G.degree)
    for c, e in enumerate(incident[v0]):
        S.add_clause((x('x', e, c),))

    # S() vrne False, če rešitve ni, sicer tuple vrednosti spremenljivk:
    # sol[i] je True/False za spremenljivko i. sol[0] je None
    sol = S()
    if sol is False:
        return None  # bogato k-barvanje ne obstaja

    return {e: c for e in E for c in range(k) if sol[x('x', e, c)]}


def rich_chromatic_index_sat(G, solver="picosat"):
    """Vrne par (χ'_r(G), bogato barvanje s χ'_r(G) barvami).
    Začne pri spodnji meji in povečuje k, dokler SAT ne najde barvanja"""

    k = lower_bound(G)
    while True:
        col = rich_coloring_sat(G, k, solver=solver)
        if col is not None:
            assert is_rich_coloring(G, col), "SAT je vrnil napačno barvanje."
            return k, col
        k += 1
