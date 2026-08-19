"""Tests for gate fusion optimization pass."""

from __future__ import annotations

from quonic.compiler import optimize_fuse
from quonic.ir import Circuit, GateOperation


def test_fuse_consecutive_same_qubit():
    """Consecutive single-qubit gates on the same qubit should be fused."""
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("x", (0,)))
    c.add(GateOperation("h", (0,)))

    fused = optimize_fuse(c)
    # Should have 1 fused gate instead of 3
    ops = [op for op in fused.ops if op.name != "measure"]
    assert len(ops) == 1
    assert "fused" in ops[0].name


def test_fuse_different_qubits():
    """Gates on different qubits should not be fused."""
    c = Circuit()
    c.allocate(2)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("h", (1,)))

    fused = optimize_fuse(c)
    ops = [op for op in fused.ops if op.name != "measure"]
    assert len(ops) == 2


def test_fuse_preserves_circuit():
    """Fusion should not modify the original circuit."""
    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("x", (0,)))

    optimize_fuse(c)
    # Original should still have 2 ops
    ops_orig = [op for op in c.ops if op.name != "measure"]
    assert len(ops_orig) == 2


def test_fuse_with_two_qubit_gate():
    """Two-qubit gates should break the fusion chain."""
    c = Circuit()
    c.allocate(2)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("x", (0,)))
    c.add(GateOperation("cx", (0, 1)))  # breaks fusion
    c.add(GateOperation("h", (1,)))

    fused = optimize_fuse(c)
    ops = [op for op in fused.ops if op.name != "measure"]
    # Should have: fused(0), cx, h(1) = 3 ops
    assert len(ops) == 3


def test_fuse_in_optimize():
    """Gate fusion should work as part of the optimize pipeline."""
    from quonic.compiler import optimize

    c = Circuit()
    c.allocate(1)
    c.add(GateOperation("h", (0,)))
    c.add(GateOperation("x", (0,)))
    c.add(GateOperation("h", (0,)))

    optimized = optimize(c, passes=("fuse",))
    ops = [op for op in optimized.ops if op.name != "measure"]
    assert len(ops) == 1
