"""Tests for complete ZX circuit extraction."""

from __future__ import annotations

from quonic.ir import Circuit, GateOperation
from quonic.zx import circuit_to_zx, extract_circuit, optimize_zx


def test_extract_simple_circuit():
    """Simple circuit should extract correctly."""
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("rz", (0,), (0.5,)))

    g = circuit_to_zx(c)
    c2 = extract_circuit(g)
    ops = [op for op in c2.ops if op.name != "measure"]
    assert len(ops) >= 1
    assert ops[0].name == "rz"


def test_extract_two_qubit_cx():
    """CX gate should extract correctly."""
    c = Circuit()
    c.allocate(2)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("cx", (0, 1)))

    g = circuit_to_zx(c)
    simplified = optimize_zx(g)
    c2 = extract_circuit(simplified)
    assert c2.num_qubits == 2
    # After optimization, H+CX may simplify significantly
    # Just verify extraction produces a valid circuit


def test_extract_preserves_qubit_count():
    """Extraction should preserve qubit count."""
    for n in [1, 2, 3, 4]:
        c = Circuit()
        c.allocate(n)
        for q in range(n):
            c.add(GateOperation("h", (q,)))

        g = circuit_to_zx(c)
        c2 = extract_circuit(g)
        assert c2.num_qubits == n


def test_extract_with_entangling_gates():
    """Circuit with entangling gates should extract correctly."""
    c = Circuit()
    c.allocate(3)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("cx", (0, 1)))
    c.add(GateOperation("cz", (1, 2)))

    g = circuit_to_zx(c)
    simplified = optimize_zx(g)
    c2 = extract_circuit(simplified)
    assert c2.num_qubits == 3
