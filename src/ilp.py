"""Bogato barvanje povezav s celoštevilskim linearnim programom.
Uporaba (iz korena repozitorija):
    from src.ilp import rich_coloring_ilp, rich_chromatic_index_ilp
    G = graphs.CompleteGraph(4)
    rich_coloring_ilp(G, 4)          # None (s 4 barvami ne gre)
    rich_coloring_ilp(G, 5)          # {(0, 1): 0, (0, 2): 1, ...}
    rich_chromatic_index_ilp(G)      # (5, barvanje)"""

from sage.all import MixedIntegerLinearProgram
from sage.numerical.mip import MIPSolverException
from src.rich import is_rich_coloring, lower_bound


def rich_coloring_ilp(G, k, solver=None):
    """Vrne bogato barvanje povezav grafa G s k barvami
    kot slovar {(u, v): barva} ali None, če tako barvanje ne obstaja.
    solver...None pomeni privzeti GLPK.
    Spremenljivke (binarne):
        x[e, c] = 1  natanko tedaj, ko ima povezava e barvo c,
        r[e] = 1  pomeni, da zahtevamo, da je e bogata."""

    E = G.edges(labels=False, sort=True)  # seznam povezav
    if not E:
        return {}  # graf brez povezav

    # Pri vozlišču stopnje Δ potrebujemo Δ različnih barv, zato za k < Δ ne gre
    if k < max(G.degree()):
        return None

    p = MixedIntegerLinearProgram(maximization=False, solver=solver)
    x = p.new_variable(binary=True)
    r = p.new_variable(binary=True)

    # Povezave, ki imajo krajišče v
    incident = {v: [e for e in E if v in e] for v in G}

    # 1. pogoj: vsaka povezava ima natanko eno barvo
    for e in E:
        p.add_constraint(sum(x[e, c] for c in range(k)) == 1)

    for v in G:
        Ev = incident[v]
        if not Ev:
            continue  # izolirano vozlišče preskočimo (zanj ni pogojev)
        # 2. pogoj (pravilnost): pri vozlišču v je vsaka barva uporabljena največ enkrat
        for c in range(k):
            p.add_constraint(sum(x[e, c] for e in Ev) <= 1)
        # 4. pogoj: vozlišče v ima vsaj eno bogato povezavo
        p.add_constraint(sum(r[e] for e in Ev) >= 1)

    # 3. pogoj: če je r[e] = 1 so sosedje povezave e paroma različnih barv:
    # vsaka barva c se med njimi pojavi največ enkrat.
    # Če je r[e] = 0, je desna stran 1 + |N(e)| in pogoj nič ne omejuje
    for e in E:
        N = [f for f in E if f != e and set(f) & set(e)]  # N so sosedne povezave e
        for c in range(k):
            p.add_constraint(sum(x[f, c] for f in N) <= 1 + len(N) * (1 - r[e]))

    # Lomljenje simetrij: imena barv niso pomembna, zato povezavam pri
    # vozlišču največje stopnje vnaprej določimo barve 0, 1, 2...
    v0 = max(G, key=G.degree)
    for c, e in enumerate(incident[v0]):
        p.add_constraint(x[e, c] == 1)
    try:
        p.solve()
    except MIPSolverException:
        return None  # bogato k-barvanje ne obstaja

    # Iz vrednosti x[e, c] preberemo barvanje (> 0.5 zaradi zaokrožitvenih napak)
    X = p.get_values(x)
    return {e: c for e in E for c in range(k) if X[e, c] > 0.5}


def rich_chromatic_index_ilp(G, solver=None):
    """Vrne par (χ'_r(G), bogato barvanje s χ'_r(G) barvami).
    Začne pri spodnji meji in povečuje k dokler ILP ne najde barvanja"""
    k = lower_bound(G)
    while True:
        col = rich_coloring_ilp(G, k, solver=solver)
        if col is not None:
            # Rezultat solverja vedno preverimo z neodvisno funkcijo.
            assert is_rich_coloring(G, col), "ILP je vrnil napačno barvanje!"
            return k, col
        k += 1
