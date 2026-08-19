"""Tests for ZX circuit extraction and advanced rules."""

from __future__ import annotations

from quonic.ir import Circuit, GateOperation
from quonic.zx import ZXGraph, circuit_to_zx, extract_circuit, optimize_zx
from quonic.zx.graph import SpiderType


def test_circuit_to_zx_and_back():
    """Round-trip: circuit → ZX → circuit should preserve qubit count."""
    c = Circuit()
    c.allocate(2)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("cx", (0, 1)))

    g = circuit_to_zx(c)
    c2 = extract_circuit(g)
    assert c2.num_qubits == 2


def test_extract_single_qubit():
    """Single qubit circuit should extract correctly."""
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("rz", (0,), (0.5,)))

    g = circuit_to_zx(c)
    c2 = extract_circuit(g)
    ops = [op for op in c2.ops if op.name != "measure"]
    assert len(ops) >= 1
    assert ops[0].name == "rz"


def test_h_edge_elimination():
    """H-edge between same-type spiders with 0-phase should be eliminated."""
    g = ZXGraph()
    s1 = g.add_spider(SpiderType.Z, 0.0)
    s2 = g.add_spider(SpiderType.Z, 0.5)
    g.add_edge(s1, s2, hadamard=True)

    simplified = optimize_zx(g)
    # After H-edge elimination, the edge should no longer be H
    h_edges = [e for e in simplified.edges if e.hadamard and e.src != -1]
    assert len(h_edges) == 0


def test_optimize_zx_removes_h_h():
    """ZX optimization should cancel H·H = I."""
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("h", (0,)))

    g = circuit_to_zx(c)
    simplified = optimize_zx(g)
    # After optimization, H·H should be removed
    non_boundary = [s for s in simplified.spiders.values() if s.stype != SpiderType.BOUNDARY]
    assert len(non_boundary) == 0


def test_optimize_zx_fuses_rz():
    """ZX optimization should fuse adjacent Rz gates."""
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("rz", (0,), (0.3,)))
    c.add(GateOperation("rz", (0,), (0.7,)))

    g = circuit_to_zx(c)
    simplified = optimize_zx(g)
    non_boundary = [s for s in simplified.spiders.values() if s.stype != SpiderType.BOUNDARY]
    # Should fuse into one spider with phase 1.0
    assert len(non_boundary) == 1
    assert abs(non_boundary[0].phase - 1.0) < 1e-10


def test_extract_circuit_from_simplified():
    """Extracting from a simplified graph should produce a valid circuit."""
    c = Circuit()
    c.allocate(2)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("rz", (0,), (0.5,)))
    c.add(GateOperation("cx", (0, 1)))

    g = circuit_to_zx(c)
    simplified = optimize_zx(g)
    c2 = extract_circuit(simplified)
    assert c2.num_qubits == 2
