"""Tests for ZX phase teleportation."""

from __future__ import annotations

from quonic.ir import Circuit, GateOperation
from quonic.zx import ZXGraph, circuit_to_zx, optimize_zx
from quonic.zx.graph import SpiderType


def test_phase_teleportation_same_type():
    """Phase should teleport to same-type neighbor."""
    g = ZXGraph()
    b1 = g.add_spider(SpiderType.BOUNDARY)
    s1 = g.add_spider(SpiderType.Z, 0.5)
    s2 = g.add_spider(SpiderType.Z, 0.3)
    b2 = g.add_spider(SpiderType.BOUNDARY)
    g.add_edge(b1, s1)
    g.add_edge(s1, s2)
    g.add_edge(s2, b2)

    simplified = optimize_zx(g)
    # After teleportation + fusion, should have one Z spider with phase 0.8
    z_spiders = [s for s in simplified.spiders.values() if s.stype == SpiderType.Z]
    assert len(z_spiders) == 1
    assert abs(z_spiders[0].phase - 0.8) < 1e-10


def test_phase_teleportation_different_type():
    """Phase should teleport to different-type neighbor."""
    g = ZXGraph()
    b1 = g.add_spider(SpiderType.BOUNDARY)
    s1 = g.add_spider(SpiderType.Z, 0.5)
    s2 = g.add_spider(SpiderType.X, 0.0)
    b2 = g.add_spider(SpiderType.BOUNDARY)
    g.add_edge(b1, s1)
    g.add_edge(s1, s2)
    g.add_edge(s2, b2)

    simplified = optimize_zx(g)
    # After teleportation, s1 should have phase 0, s2 should have phase -0.5
    [s for s in simplified.spiders.values() if s.stype == SpiderType.Z]
    x_spiders = [s for s in simplified.spiders.values() if s.stype == SpiderType.X]
    # s1 (Z) should be removed (phase 0, 2 neighbors)
    # s2 (X) should remain with phase -0.5
    assert len(x_spiders) == 1
    assert abs(x_spiders[0].phase - (-0.5)) < 1e-10


def test_optimize_zx_with_teleportation():
    """Full optimization with teleportation should simplify circuits."""
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("rz", (0,), (0.3,)))
    c.add(GateOperation("rz", (0,), (0.5,)))

    g = circuit_to_zx(c)
    simplified = optimize_zx(g)
    non_boundary = [s for s in simplified.spiders.values() if s.stype != SpiderType.BOUNDARY]
    # Should fuse into one spider with phase 0.8
    assert len(non_boundary) == 1
    assert abs(non_boundary[0].phase - 0.8) < 1e-10
