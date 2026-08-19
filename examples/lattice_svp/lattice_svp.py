"""Lattice SVP (Shortest Vector Problem) quantum demo.

Quantum approach to lattice-based cryptography problems.
Output: approximate shortest vector.
"""

from quonic.algorithms import lattice_svp_demo

result = lattice_svp_demo()
print(result.counts)
