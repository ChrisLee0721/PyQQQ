"""Hamiltonian Simulation — simulate time evolution of a quantum system.

Boundary conditions:
- Uses Trotter-Suzuki decomposition
- Wraps trotter() with simpler interface
- Minimal: 2-qubit Heisenberg model

Example::

    from quonic.algorithms import hamiltonian_simulation_demo
    result = hamiltonian_simulation_demo()
"""

from __future__ import annotations

from ..result import Result
from .trotter import trotter


def hamiltonian_simulation_demo() -> Result:
    """Minimal Hamiltonian simulation demo: 2-qubit Heisenberg model."""
    # H = J(Z0Z1 + X0X1 + Y0Y1)
    J = 1.0
    hamiltonian = [
        (J, "ZZ"),
        (J, "XX"),
        (J, "YY"),
    ]
    return trotter(hamiltonian, time=1.0, steps=10, n_qubits=2, shots=1024)
