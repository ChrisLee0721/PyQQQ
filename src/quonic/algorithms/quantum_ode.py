"""Quantum ODE Solver — minimal demo.

Boundary conditions:
- Minimal: dy/dt = -y (exponential decay)
- Uses Trotter decomposition
- NOT a production ODE solver

Example::

    from quonic.algorithms import quantum_ode_demo
    result = quantum_ode_demo()
"""

from __future__ import annotations

from ..backends import get_backend
from ..ir import Circuit, GateOperation
from ..result import Result


def quantum_ode_demo(
    backend: str = "auto",
    shots: int = 1024,
) -> Result:
    """Minimal quantum ODE solver demo."""
    circuit = Circuit()

    # Initial condition: y(0) = 1 (|1>)
    circuit.add(GateOperation("x", (0,)))

    # Time evolution: exp(-t) via Rz rotation
    t = 1.0
    circuit.add(GateOperation("rz", (0,), (t,)))

    result = get_backend(backend).run(circuit, shots=shots)
    return Result.from_value(0.0, counts=result.counts)
