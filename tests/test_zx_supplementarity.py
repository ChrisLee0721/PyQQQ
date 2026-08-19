"""Tests for ZX supplementarity rule and complete extraction."""

from __future__ import annotations

from quonic.ir import Circuit, GateOperation
from quonic.zx import ZXGraph, circuit_to_zx, extract_circuit, optimize_zx
from quonic.zx.graph import SpiderType


def test_supplementarity_basic():
    """Z and X spiders with complementary phases sharing neighbors should simplify."""
    g = ZXGraph()
    # Create: Z(α) and X(-α) connected, both sharing the same neighbors
    # boundary1 -- Z(0.5) -- boundary2
    # boundary1 -- X(-0.5) -- boundary2
    b1 = g.add_spider(SpiderType.BOUNDARY)
    b2 = g.add_spider(SpiderType.BOUNDARY)
    z = g.add_spider(SpiderType.Z, 0.5)
    x = g.add_spider(SpiderType.X, -0.5)
    g.add_edge(b1, z)
    g.add_edge(z, b2)
    g.add_edge(b1, x)
    g.add_edge(x, b2)
    g.add_edge(z, x)  # connected to each other

    simplified = optimize_zx(g)
    non_boundary = [s for s in simplified.spiders.values() if s.stype != SpiderType.BOUNDARY]
    # Supplementarity should remove both spiders
    assert len(non_boundary) == 0


def test_supplementarity_different_phases():
    """Z and X spiders with non-complementary phases should NOT simplify."""
    g = ZXGraph()
    b1 = g.add_spider(SpiderType.BOUNDARY)
    b2 = g.add_spider(SpiderType.BOUNDARY)
    z = g.add_spider(SpiderType.Z, 0.5)
    x = g.add_spider(SpiderType.X, 0.3)
    g.add_edge(b1, z)
    g.add_edge(z, b2)
    g.add_edge(b1, x)
    g.add_edge(x, b2)
    g.add_edge(z, x)

    simplified = optimize_zx(g)
    non_boundary = [s for s in simplified.spiders.values() if s.stype != SpiderType.BOUNDARY]
    # Should NOT be removed (phases don't sum to 0)
    assert len(non_boundary) == 2


def test_extract_circuit_with_x_spiders():
    """Extraction should handle X-type spiders."""
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("rx", (0,), (0.5,)))

    g = circuit_to_zx(c)
    c2 = extract_circuit(g)
    ops = [op for op in c2.ops if op.name != "measure"]
    assert len(ops) >= 1


def test_extract_circuit_round_trip():
    """Round-trip should preserve qubit count for multi-gate circuit."""
    c = Circuit()
    c.allocate(3)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("rz", (1,), (0.5,)))
    c.add(GateOperation("cx", (0, 1)))
    c.add(GateOperation("cz", (1, 2)))

    g = circuit_to_zx(c)
    simplified = optimize_zx(g)
    c2 = extract_circuit(simplified)
    assert c2.num_qubits == 3
