"""Tests for ZX-calculus optimization."""

from __future__ import annotations

import numpy as np

from quonic.compiler import optimize, optimize_zx_circuit
from quonic.ir import Circuit, GateOperation
from quonic.zx import ZXGraph, circuit_to_zx, optimize_zx
from quonic.zx.graph import SpiderType


def test_zx_graph_basic():
    """ZXGraph should support basic operations."""
    g = ZXGraph()
    s1 = g.add_spider(SpiderType.Z, 0.0)
    s2 = g.add_spider(SpiderType.X, np.pi)
    g.add_edge(s1, s2)
    assert len(g.spiders) == 2
    assert len(g.edges) == 1
    assert g.neighbors(s1) == [s2]


def test_zx_spider_fusion():
    """Adjacent same-type spiders should fuse."""
    g = ZXGraph()
    s1 = g.add_spider(SpiderType.Z, 0.5)
    s2 = g.add_spider(SpiderType.Z, 0.3)
    g.add_edge(s1, s2)

    simplified = optimize_zx(g)
    # After fusion, should have fewer spiders
    z_spiders = [s for s in simplified.spiders.values() if s.stype == SpiderType.Z]
    assert len(z_spiders) == 1
    assert abs(z_spiders[0].phase - 0.8) < 1e-10


def test_zx_identity_removal():
    """0-phase spider with 2 neighbors should be removed."""
    g = ZXGraph()
    s1 = g.add_spider(SpiderType.Z, 0.5)
    s2 = g.add_spider(SpiderType.Z, 0.0)  # identity
    s3 = g.add_spider(SpiderType.Z, 0.3)
    g.add_edge(s1, s2)
    g.add_edge(s2, s3)

    simplified = optimize_zx(g)
    # s2 should be removed, s1 and s3 connected
    z_spiders = [s for s in simplified.spiders.values() if s.stype == SpiderType.Z]
    assert len(z_spiders) <= 2


def test_circuit_to_zx():
    """Circuit-to-ZX conversion should produce a valid graph."""
    c = Circuit()
    c.allocate(2)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("cx", (0, 1)))

    g = circuit_to_zx(c)
    assert len(g.spiders) > 0
    assert len(g.inputs) == 2
    assert len(g.outputs) == 2


def test_circuit_to_zx_single_qubit():
    """Single-qubit circuit should produce boundary + gate spiders."""
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("rz", (0,), (0.5,)))

    g = circuit_to_zx(c)
    # Should have: input boundary + rz spider + output boundary
    assert len(g.inputs) == 1
    assert len(g.outputs) == 1
    z_spiders = [s for s in g.spiders.values() if s.stype == SpiderType.Z]
    assert len(z_spiders) >= 1


def test_zx_optimize_circuit():
    """ZX optimization should simplify redundant gates."""
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("h", (0,)))  # H·H = I

    optimized = optimize_zx_circuit(c)
    ops = [op for op in optimized.ops if op.name != "measure"]
    assert len(ops) == 0  # H·H should cancel


def test_zx_optimize_rz_cancel():
    """ZX optimization should cancel Rz(θ) · Rz(-θ)."""
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("rz", (0,), (0.5,)))
    c.add(GateOperation("rz", (0,), (-0.5,)))

    optimized = optimize_zx_circuit(c)
    ops = [op for op in optimized.ops if op.name != "measure"]
    assert len(ops) == 0


def test_zx_optimize_rz_combine():
    """ZX optimization should combine Rz(a) · Rz(b) = Rz(a+b)."""
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("rz", (0,), (0.3,)))
    c.add(GateOperation("rz", (0,), (0.7,)))

    optimized = optimize_zx_circuit(c)
    ops = [op for op in optimized.ops if op.name != "measure"]
    assert len(ops) == 1
    assert abs(ops[0].params[0] - 1.0) < 1e-10


def test_zx_in_optimize_pipeline():
    """ZX pass should work in the optimize() pipeline."""
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("h", (0,)))

    optimized = optimize(c, passes=("zx",))
    ops = [op for op in optimized.ops if op.name != "measure"]
    assert len(ops) == 0
