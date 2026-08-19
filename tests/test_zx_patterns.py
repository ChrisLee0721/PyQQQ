"""Tests for ZX pattern matching rules."""

from __future__ import annotations

import numpy as np

from quonic.ir import Circuit, GateOperation
from quonic.zx import ZXGraph, circuit_to_zx, extract_circuit, optimize_zx
from quonic.zx.graph import SpiderType


def test_h_conjugation_z_to_x():
    """HZH = X: Z-spider with phase π via H-edge should become X (then removed)."""
    g = ZXGraph()
    b1 = g.add_spider(SpiderType.BOUNDARY)
    z = g.add_spider(SpiderType.Z, np.pi)
    b2 = g.add_spider(SpiderType.BOUNDARY)
    g.add_edge(b1, z, hadamard=True)
    g.add_edge(z, b2)

    simplified = optimize_zx(g)
    non_boundary = [s for s in simplified.spiders.values() if s.stype != SpiderType.BOUNDARY]
    # Z(π) → X(0) → removed by identity elimination
    assert len(non_boundary) == 0


def test_h_conjugation_x_to_z():
    """HXH = Z: X-spider with phase π via H-edge should become Z (then removed)."""
    g = ZXGraph()
    b1 = g.add_spider(SpiderType.BOUNDARY)
    x = g.add_spider(SpiderType.X, np.pi)
    b2 = g.add_spider(SpiderType.BOUNDARY)
    g.add_edge(b1, x, hadamard=True)
    g.add_edge(x, b2)

    simplified = optimize_zx(g)
    non_boundary = [s for s in simplified.spiders.values() if s.stype != SpiderType.BOUNDARY]
    assert len(non_boundary) == 0


def test_optimize_h_z_h():
    """H·Z·H circuit should simplify to X."""
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("rz", (0,), (np.pi,)))
    c.add(GateOperation("h", (0,)))

    g = circuit_to_zx(c)
    simplified = optimize_zx(g)
    non_boundary = [s for s in simplified.spiders.values() if s.stype != SpiderType.BOUNDARY]
    # Should simplify significantly
    assert len(non_boundary) <= 1


def test_pattern_matching_preserves_circuit():
    """Pattern matching should not break the circuit structure."""
    c = Circuit()
    c.allocate(2)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("rz", (0,), (0.5,)))
    c.add(GateOperation("cx", (0, 1)))

    g = circuit_to_zx(c)
    simplified = optimize_zx(g)
    c2 = extract_circuit(simplified)
    assert c2.num_qubits == 2
