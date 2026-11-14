"""Preverjanje bogatih barvanj povezav.
S to funkcijo preverimo vsako barvanje, ki ga vrneta ILP ali SAT.

Uporaba:
    from src.rich import is_rich_coloring
    G = graphs.CompleteGraph(4)
    is_rich_coloring(G, col)   # col: slovar {(u, v): barva}"""

from sage.all import Graph


def color(col, u, v):
    """Vrne barvo povezave uv.
    col...slovar {(u, v): barva}, ključ je lahko (u, v) ali (v, u)."""
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
