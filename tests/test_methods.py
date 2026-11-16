"""Testi pravilnosti za ILP in SAT metodo (naloga 1).
Zagon iz korena repozitorija v conda okolju sage:
    python tests/test_methods.py
Testi:
  1) znane vrednosti χ'_r (K1, K2, P3, K4, H0, Petersen, nepovezan graf),
  2) K4 nima bogatega 4-barvanja."""

import os
import sys
import time
# da deluje "from src. ...", dodamo koren repozitorija v sys.path.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sage.all import Graph, graphs
from src.ilp import rich_coloring_ilp, rich_chromatic_index_ilp
from src.sat import rich_coloring_sat, rich_chromatic_index_sat


def test_known_values():
    H0 = graphs.CompleteGraph(4)
    H0.subdivide_edge(0, 1, 1)
    known = [
        ("K1", Graph(1), 0),
        ("K2", graphs.CompleteGraph(2), 1),
        ("P3", graphs.PathGraph(3), 2),
        ("K4", graphs.CompleteGraph(4), 5),
        ("H0", H0, 6),
        ("Petersen", graphs.PetersenGraph(), 5),
        ("K2 + K2 + K1", Graph({0: [1], 2: [3], 4: []}), 1),  # nepovezan z izoliranim vozliščem
    ]
    for name, G, expected in known:
        k_ilp = rich_chromatic_index_ilp(G)[0]
        k_sat = rich_chromatic_index_sat(G)[0]
        assert k_ilp == expected, f"{name}: ILP {k_ilp}, pričakovano {expected}"
        assert k_sat == expected, f"{name}: SAT {k_sat}, pričakovano {expected}"
        print(f"  {name}: χ'_r = {expected}  OK")


def test_K4_no_4_coloring():
    K4 = graphs.CompleteGraph(4)
    assert rich_coloring_ilp(K4, 4) is None
    assert rich_coloring_sat(K4, 4) is None
    print("  K4 s 4 barvami: ILP in SAT vrneta None  OK")


if __name__ == "__main__":
    start = time.time()
    print("Znane vrednosti:")
    test_known_values()
    print("K4 brez 4-barvanja:")
    test_K4_no_4_coloring()
    print(f"\nVSI TESTI USPEŠNI ({time.time() - start:.1f} s)")
