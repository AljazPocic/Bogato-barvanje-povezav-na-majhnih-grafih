"""Osnovne funkcije za bogata barvanja povezav: preverjanje in spodnja meja.
Z is_rich_coloring preverimo vsako barvanje, ki ga vrneta ILP ali SAT.

Uporaba:
    from src.rich import is_rich_coloring, lower_bound
    G = graphs.CompleteGraph(4)
    is_rich_coloring(G, col)   # col: slovar {(u, v): barva}
    lower_bound(G)             # 5"""

from sage.all import Graph


def color(col, u, v):
    """Vrne barvo povezave uv.
    col...slovar {(u, v): barva}, ključ je lahko (u, v) ali (v, u).
    Če med u in v ni povezave, funkcija vrene Error."""
    return col[(u, v)] if (u, v) in col else col[(v, u)]


def is_rich(G, col, u, v):
    """Vrne True, če je povezava uv bogata."""
    sosednje = [color(col, u, w) for w in G.neighbors(u) if w != v] \
             + [color(col, v, w) for w in G.neighbors(v) if w != u]
    return len(sosednje) == len(set(sosednje))


def is_rich_coloring(G, col):
    """Vrne True, če je `col` bogato barvanje povezav grafa G, sicer False.
    G...Sage Graph
    col...slovar, ki vsaki povezavi (u, v) priredi barvo."""

    # Vsaka povezava ima barvo
    for u, v in G.edges(labels=False, sort=False):
        if (u, v) not in col and (v, u) not in col:
            return False

    # Povezave pri istem vozlišču imajo paroma različne barve
    for v in G:
        barve = [color(col, v, w) for w in G.neighbors(v)]
        if len(barve) != len(set(barve)):
            return False

    # Vsako neizolirano vozlišče mora imeti vsaj eno bogato povezavo
    for v in G:
        if G.degree(v) > 0 and not any(is_rich(G, col, v, w) for w in G.neighbors(v)):
            return False

    return True


def lower_bound(G):
    """Vrne spodnjo mejo za bogati kromatični indeks.
    Meja je max(Δ, max_v min_{u ∈ N(v)} (d(u) + d(v) - 1))."""

    # Pravilno barvanje potrebuje vsaj Δ barv
    meja = max(G.degree(), default=0)

    # Vozlišče v potrebuje bogato povezavo vu. Ta in njeni sosedje so paroma
    # različnih barv kar je d(u) + d(v) - 1 barv. Vozlišče v si izbere
    # najugodnejšega soseda (min), meja pa mora veljati za vsa v (max)
    for v in G:
        if G.degree(v) > 0:  # izloirane preskočimo
            najmanj = min(G.degree(u) + G.degree(v) - 1 for u in G.neighbors(v))
            meja = max(meja, najmanj)

    return meja
