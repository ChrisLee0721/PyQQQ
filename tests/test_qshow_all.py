"""Tests for qshow_all — parallel multi-backend execution."""

from __future__ import annotations

from quonic import gates, qgate, qshow_all, reset

BACKENDS = ["qiskit", "cirq"]


def test_qshow_all_basic():
    """qshow_all returns results for each backend."""
    reset()
    qgate(gates.H, 0)
    qgate(gates.CX, 0, 1)
    results = qshow_all(BACKENDS, shots=256, print_results=False)
    assert set(results.keys()) == set(BACKENDS)
    for name, r in results.items():
        assert r.kind == "counts"
        p00 = r.counts.get("00", 0) / 256
        p11 = r.counts.get("11", 0) / 256
        assert p00 + p11 > 0.8, f"{name}: expected Bell state, got {r.counts}"


def test_qshow_all_empty_circuit():
    """qshow_all on empty circuit returns empty dict."""
    reset()
    results = qshow_all(BACKENDS, print_results=False)
    assert results == {}


def test_qshow_all_single_backend():
    """qshow_all with single backend works without process pool."""
    reset()
    qgate(gates.X, 0)
    results = qshow_all(["qiskit"], shots=100, print_results=False)
    assert "qiskit" in results
    assert results["qiskit"].counts.get("1", 0) == 100


def test_qshow_all_print(capsys):
    """qshow_all with print_results=True outputs results."""
    reset()
    qgate(gates.X, 0)
    qshow_all(["qiskit"], shots=100, print_results=True)
    captured = capsys.readouterr()
    assert "qiskit" in captured.out or "100" in captured.out
