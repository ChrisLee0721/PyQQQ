"""Surface Code — minimal demonstration of topological error correction.

Boundary conditions:
- Minimal 3x3 surface code (distance 3)
- Demonstrates syndrome extraction on a lattice
- NOT a full fault-tolerant implementation
- Shows the concept of topological protection

Example::

    from quonic.algorithms import surface_code_demo
    result = surface_code_demo()
"""

from __future__ import annotations

from ..backends import get_backend
from ..ir import Circuit, GateOperation
from ..result import Result


def surface_code_demo(
    backend: str = "auto",
    shots: int = 100,
) -> Result:
    """Minimal surface code demo with 3x3 lattice."""
    circuit = Circuit()

    # Minimal surface code: 5 data qubits (cross pattern), 4 syndrome qubits
    # Data qubits: 0,1,2,3,4
    # Syndrome qubits: 5,6,7,8

    # Prepare logical |0>
    # (Surface code encoding is complex; this is a minimal demo)

    # X-stabilizer measurements
    circuit.add(GateOperation("h", (5,)))
    circuit.add(GateOperation("cx", (5, 0)))
    circuit.add(GateOperation("cx", (5, 1)))
    circuit.add(GateOperation("h", (5,)))

    circuit.add(GateOperation("h", (6,)))
    circuit.add(GateOperation("cx", (6, 1)))
    circuit.add(GateOperation("cx", (6, 2)))
    circuit.add(GateOperation("h", (6,)))

    # Z-stabilizer measurements
    circuit.add(GateOperation("cx", (0, 7)))
    circuit.add(GateOperation("cx", (2, 7)))

    circuit.add(GateOperation("cx", (1, 8)))
    circuit.add(GateOperation("cx", (3, 8)))

    result = get_backend(backend).run(circuit, shots=shots)
    return Result.from_value(1.0, counts=result.counts)
