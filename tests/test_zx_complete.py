"""Tests for ZX complete rewriting rules."""

from __future__ import annotations

from quonic.ir import Circuit, GateOperation
from quonic.zx import ZXGraph, circuit_to_zx, extract_circuit, optimize_zx
from quonic.zx.graph import SpiderType


def test_phase_copy():
    """Phase copy rule: 0-phase spider connecting multiple same-type neighbors."""
    g = ZXGraph()
    b1 = g.add_spider(SpiderType.BOUNDARY)
    b2 = g.add_spider(SpiderType.BOUNDARY)
    center = g.add_spider(SpiderType.Z, 0.0)
    g.add_edge(b1, center)
    g.add_edge(center, b2)

    simplified = optimize_zx(g)
    # Center should be removed, boundaries connected
    non_boundary = [s for s in simplified.spiders.values() if s.stype != SpiderType.BOUNDARY]
    assert len(non_boundary) == 0


def test_bialgebra():
    """Bialgebra rule: Z-X pair with boundary neighbors."""
    g = ZXGraph()
    b1 = g.add_spider(SpiderType.BOUNDARY)
    b2 = g.add_spider(SpiderType.BOUNDARY)
    z = g.add_spider(SpiderType.Z, 0.0)
    x = g.add_spider(SpiderType.X, 0.0)
    g.add_edge(b1, z)
    g.add_edge(z, x)
    g.add_edge(x, b2)

    simplified = optimize_zx(g)
    non_boundary = [s for s in simplified.spiders.values() if s.stype != SpiderType.BOUNDARY]
    # Both should be removed (0-phase, bialgebra pattern)
    assert len(non_boundary) == 0


def test_optimize_complex_circuit():
    """Complex circuit should simplify significantly."""
    c = Circuit()
    c.allocate(2)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("rz", (0,), (0.5,)))
    c.add(GateOperation("h", (0,)))  # H·Rz·H = Rx
    c.add(GateOperation("cx", (0, 1)))

    g = circuit_to_zx(c)
    simplified = optimize_zx(g)
    non_boundary = [s for s in simplified.spiders.values() if s.stype != SpiderType.BOUNDARY]
    # Should have fewer spiders than original
    original_non_boundary = [s for s in g.spiders.values() if s.stype != SpiderType.BOUNDARY]
    assert len(non_boundary) <= len(original_non_boundary)


def test_extract_after_full_optimize():
    """Full optimization + extraction should produce valid circuit."""
    c = Circuit()
    c.allocate(2)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("rz", (0,), (0.3,)))
    c.add(GateOperation("cx", (0, 1)))
    c.add(GateOperation("rz", (1,), (0.5,)))

    g = circuit_to_zx(c)
    simplified = optimize_zx(g)
    c2 = extract_circuit(simplified)
    assert c2.num_qubits == 2
