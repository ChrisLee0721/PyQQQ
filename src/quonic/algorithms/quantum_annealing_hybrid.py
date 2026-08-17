"""Quantum Annealing Hybrid — classical + quantum annealing simulation.

Boundary conditions:
- Combines classical optimization with quantum tunneling effect
- Minimal: simulated annealing with quantum-inspired tunneling
- NOT actual D-Wave hardware

Example::

    from quonic.algorithms import quantum_annealing_hybrid_demo
    result = quantum_annealing_hybrid_demo()
"""

from __future__ import annotations

import math
import random

from ..result import Result


def quantum_annealing_hybrid_demo(
    n_spins: int = 4,
    n_steps: int = 100,
    temperature: float = 1.0,
) -> Result:
    """Minimal quantum annealing hybrid demo.

    Ising model: H = -sum J_ij * s_i * s_j
    """
    # Random coupling
    J = {(i, j): random.uniform(-1, 1) for i in range(n_spins) for j in range(i + 1, n_spins)}

    # Initialize random spins
    spins = [random.choice([-1, 1]) for _ in range(n_spins)]
    best_energy = sum(-J[(i, j)] * spins[i] * spins[j] for i, j in J)
    best_spins = list(spins)

    for step in range(n_steps):
        # Classical: flip random spin
        i = random.randint(0, n_spins - 1)
        spins[i] *= -1
        energy = sum(-J[(a, b)] * spins[a] * spins[b] for a, b in J)

        # Accept or reject (Metropolis with quantum tunneling)
        delta = energy - best_energy
        if delta < 0 or random.random() < math.exp(-delta / temperature):
            best_energy = energy
            best_spins = list(spins)
        else:
            spins[i] *= -1  # revert

    return Result.from_value(best_energy, best_spins=best_spins)
