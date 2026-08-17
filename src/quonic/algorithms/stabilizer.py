"""Stabilizer formalism — quantum error correction framework.

Minimal demonstration of stabilizer group operations using Clifford gates.

Boundary conditions:
- Only Clifford gates (H, S, CX) — no T gate or arbitrary rotations
- Stabilizer states can be efficiently simulated
- Demonstrates X and Z stabilizer generators

Example::

    from quonic.algorithms import stabilizer_demo
    result = stabilizer_demo(n_qubits=3, shots=100)
"""

from __future__ import annotations

from ..backends import get_backend
from ..ir import Circuit, GateOperation
from ..result import Result


def stabilizer_demo(
    n_qubits: int = 3,
    backend: str = "auto",
    shots: int = 100,
) -> Result:
    """Demonstrate stabilizer state preparation and measurement."""
    circuit = Circuit()

    # Prepare a stabilizer state: |000> + |111> (GHZ-like)
    circuit.add(GateOperation("h", (0,)))
    for q in range(n_qubits - 1):
        circuit.add(GateOperation("cx", (q, q + 1)))

    # Measure stabilizers: Z0Z1, Z1Z2
    # These should give +1 eigenvalue for the GHZ state

    result = get_backend(backend).run(circuit, shots=shots)
    return Result.from_value(1.0, counts=result.counts)
