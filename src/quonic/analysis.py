"""Circuit analysis — resource estimation and gate counting.

Example::

    from quonic.analysis import analyze
    report = analyze(circuit)
    print(f"Depth: {report.depth}, CNOTs: {report.cx_count}")
"""

from __future__ import annotations

from dataclasses import dataclass

from .ir import Circuit, GateOperation

_MEASURE_NAMES = ("measure", "cmeasure")

# Gate categories for counting
_SINGLE_QUBIT = {"h", "x", "y", "z", "rx", "ry", "rz", "p", "i"}
_TWO_QUBIT = {"cx", "cz", "cp", "swap"}
_MULTI_QUBIT = {"ccx", "mcz", "cswap"}


@dataclass
class CircuitReport:
    """Resource estimation report for a circuit."""

    n_qubits: int
    depth: int
    gate_count: int
    single_qubit_count: int
    two_qubit_count: int
    multi_qubit_count: int
    cx_count: int
    measure_count: int
    fidelity_estimate: float

    def __repr__(self) -> str:
        return (
            f"CircuitReport(n={self.n_qubits}, depth={self.depth}, "
            f"gates={self.gate_count}, cx={self.cx_count}, "
            f"fidelity≈{self.fidelity_estimate:.4f})"
        )


def analyze(circuit: Circuit, gate_error: float = 0.001) -> CircuitReport:
    """Analyze a circuit and return resource estimates.

    Args:
        circuit: the circuit to analyze
        gate_error: assumed per-gate error rate for fidelity estimation

    Returns:
        CircuitReport with gate counts, depth, and fidelity estimate
    """
    n = circuit.num_qubits
    depth = circuit.depth()

    single = 0
    two = 0
    multi = 0
    cx = 0
    measure = 0

    for op in circuit.ops:
        if not isinstance(op, GateOperation):
            continue
        name = op.name
        if name in _MEASURE_NAMES:
            measure += 1
        elif name in _SINGLE_QUBIT:
            single += 1
        elif name in _TWO_QUBIT:
            two += 1
            if name == "cx":
                cx += 1
        elif name in _MULTI_QUBIT:
            multi += 1
        else:
            # Unknown gate — count as single-qubit by default
            single += 1

    total_gates = single + two + multi
    # Rough fidelity estimate: F ≈ (1 - error)^gate_count
    fidelity = (1 - gate_error) ** total_gates if total_gates > 0 else 1.0

    return CircuitReport(
        n_qubits=n,
        depth=depth,
        gate_count=total_gates,
        single_qubit_count=single,
        two_qubit_count=two,
        multi_qubit_count=multi,
        cx_count=cx,
        measure_count=measure,
        fidelity_estimate=fidelity,
    )
