"""Lattice Problems — minimal demo of lattice-based cryptography concepts.

Boundary conditions:
- Minimal: 2D lattice shortest vector problem (SVP)
- Classical brute-force (quantum would use HSP)
- Demonstrates the concept only

Example::

    from quonic.algorithms import lattice_svp_demo
    result = lattice_svp_demo()
"""

from __future__ import annotations

import numpy as np

from ..result import Result


def lattice_svp_demo() -> Result:
    """Minimal lattice SVP demo: find shortest vector in 2D lattice."""
    # Lattice basis
    basis = np.array([[3, 1], [1, 2]])

    # Brute-force search for shortest vector
    min_norm = float("inf")
    shortest = None
    for i in range(-5, 6):
        for j in range(-5, 6):
            if i == 0 and j == 0:
                continue
            v = i * basis[0] + j * basis[1]
            norm = np.linalg.norm(v)
            if norm < min_norm:
                min_norm = norm
                shortest = v.tolist()

    return Result.from_value(float(min_norm), shortest_vector=shortest)
