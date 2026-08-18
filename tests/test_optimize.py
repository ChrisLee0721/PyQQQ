"""Tests for circuit optimization passes."""

from __future__ import annotations

from quonic import optimize, qgate, reset
from quonic.compiler import optimize_cancel, optimize_peephole
from quonic.gates import CX, H, X
from quonic.ir import Circuit, GateOperation
from quonic.stack import current_circuit

# ---------------------------------------------------------------------------
# 1. Gate cancellation
# ---------------------------------------------------------------------------


def test_cancel_xx():
    reset()
    qgate(X, 0)
    qgate(X, 0)
    c = optimize_cancel(current_circuit())
    # X·X = I, should be empty
    gate_ops = [op for op in c.ops if isinstance(op, GateOperation) and op.name != "measure"]
    assert len(gate_ops) == 0


def test_cancel_hh():
    reset()
    qgate(H, 0)
    qgate(H, 0)
    c = optimize_cancel(current_circuit())
    gate_ops = [op for op in c.ops if isinstance(op, GateOperation) and op.name != "measure"]
    assert len(gate_ops) == 0


def test_cancel_cx_cx():
    reset()
    qgate(CX, 0, 1)
    qgate(CX, 0, 1)
    c = optimize_cancel(current_circuit())
    gate_ops = [op for op in c.ops if isinstance(op, GateOperation) and op.name != "measure"]
    assert len(gate_ops) == 0


def test_cancel_no_pair():
    reset()
    qgate(X, 0)
    qgate(H, 0)
    c = optimize_cancel(current_circuit())
    gate_ops = [op for op in c.ops if isinstance(op, GateOperation) and op.name != "measure"]
    assert len(gate_ops) == 2  # no cancellation


# ---------------------------------------------------------------------------
# 2. Commutation reordering
# ---------------------------------------------------------------------------


def test_commute_brings_cancelable_together():
    # H(0) · X(1) · H(0) → X(1) · H(0) · H(0) → X(1) (after cancel)
    reset()
    qgate(H, 0)
    qgate(X, 1)
    qgate(H, 0)
    circ = current_circuit()
    optimized = optimize(circ, passes=("commute", "cancel"))
    gate_ops = [op for op in optimized.ops if isinstance(op, GateOperation) and op.name != "measure"]
    assert len(gate_ops) == 1
    assert gate_ops[0].name == "x"


# ---------------------------------------------------------------------------
# 3. Peephole optimization
# ---------------------------------------------------------------------------


def test_peephole_swap():
    # CX(0,1) · CX(1,0) · CX(0,1) = SWAP(0,1)
    reset()
    qgate(CX, 0, 1)
    qgate(CX, 1, 0)
    qgate(CX, 0, 1)
    circ = current_circuit()
    optimized = optimize_peephole(circ)
    gate_ops = [op for op in optimized.ops if isinstance(op, GateOperation) and op.name != "measure"]
    assert len(gate_ops) == 1
    assert gate_ops[0].name == "swap"
    assert gate_ops[0].qubits == (0, 1)


# ---------------------------------------------------------------------------
# 4. Unified optimize()
# ---------------------------------------------------------------------------


def test_optimize_all_passes():
    # H(0) · X(1) · H(0) · CX(0,1) · CX(1,0) · CX(0,1)
    # = X(1) · SWAP(0,1)  (after commute+cancel+peephole)
    reset()
    qgate(H, 0)
    qgate(X, 1)
    qgate(H, 0)
    qgate(CX, 0, 1)
    qgate(CX, 1, 0)
    qgate(CX, 0, 1)
    circ = current_circuit()
    optimized = optimize(circ)
    gate_ops = [op for op in optimized.ops if isinstance(op, GateOperation) and op.name != "measure"]
    assert len(gate_ops) == 2
    assert gate_ops[0].name == "x"
    assert gate_ops[1].name == "swap"


def test_optimize_empty_circuit():
    c = Circuit()
    optimized = optimize(c)
    assert len(optimized.ops) == 0


def test_optimize_preserves_non_gate_ops():
    # Optimization should not touch non-GateOperation ops (e.g., cmeasure)
    reset()
    qgate(X, 0)
    qgate(X, 0)
    circ = current_circuit()
    optimized = optimize(circ)
    # Should be empty (X·X = I)
    gate_ops = [op for op in optimized.ops if isinstance(op, GateOperation) and op.name != "measure"]
    assert len(gate_ops) == 0
