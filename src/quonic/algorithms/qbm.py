"""Quantum Boltzmann Machine — minimal demo of quantum thermal state sampling.

Boundary conditions:
- Minimal: 2-qubit thermal state
- Uses quantum simulation for Boltzmann distribution
- NOT a production QBM — demonstrates the concept

Example::

    from quonic.algorithms import qbm_demo
    result = qbm_demo()
"""

from __future__ import annotations

import math

from ..result import Result


def qbm_demo(
    temperature: float = 1.0,
) -> Result:
    """Minimal QBM demo: sample from thermal distribution."""
    import numpy as np

    # Energy function: E(x) = -J * x1 * x2 (Ising model)
    J = 1.0
    beta = 1.0 / temperature

    # Compute Boltzmann weights
    states = [(0, 0), (0, 1), (1, 0), (1, 1)]
    energies = {-J * s1 * s2: (s1, s2) for s1, s2 in states}
    weights = [math.exp(-beta * e) for e in energies.keys()]
    Z = sum(weights)
    probs = [w / Z for w in weights]

    # Sample
    samples = np.random.choice(len(states), size=100, p=probs)
    counts = {str(states[s]): int(np.sum(samples == s)) for s in range(len(states))}

    return Result.from_value(float(-J), counts=counts, partition_function=Z)
