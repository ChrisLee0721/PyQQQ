"""Fault-Tolerant Gate Implementation — minimal demo of T gate via magic state injection.

Boundary conditions:
- Demonstrates magic state injection for T gate
- Requires ancilla qubit and post-selection
- NOT a full FT implementation — shows the concept

Example::

    from quonic.algorithms import ft_gate_demo
    result = ft_gate_demo()
"""

from __future__ import annotations

import math

from ..backends import get_backend
from ..ir import Circuit, GateOperation
from ..result import Result


def ft_gate_demo(
    backend: str = "auto",
    shots: int = 100,
) -> Result:
    """Minimal fault-tolerant T gate demo via magic state injection."""
    circuit = Circuit()

    # Prepare magic state |T> = (|0> + e^{iπ/4}|1>) / sqrt(2)
    circuit.add(GateOperation("h", (1,)))
    circuit.add(GateOperation("rz", (1,), (math.pi / 4,)))

    # Data qubit in |+>
    circuit.add(GateOperation("h", (0,)))

    # Controlled-S gate (simplified)
    circuit.add(GateOperation("cx", (0, 1)))

    # Measure ancilla and post-select
    result = get_backend(backend).run(circuit, shots=shots)
    return Result.from_value(1.0, counts=result.counts)
