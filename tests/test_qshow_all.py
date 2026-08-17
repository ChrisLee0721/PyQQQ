"""Tests for qshow_all — parallel multi-backend execution."""

from __future__ import annotations

import os

import pytest

from quonic import gates, qgate, qshow_all, reset


@pytest.mark.skipif(os.environ.get("CI") == "true", reason="ProcessPoolExecutor hangs on Linux CI spawn")
def test_qshow_all_basic():
    """qshow_all returns results for each backend."""
    reset()
    qgate(gates.H, 0)
    qgate(gates.CX, 0, 1)
    results = qshow_all(["native"], shots=128, print_results=False)
    assert "native" in results
    r = results["native"]
    assert r.kind == "counts"
    p00 = r.counts.get("00", 0) / 128
    p11 = r.counts.get("11", 0) / 128
    assert p00 + p11 > 0.7


def test_qshow_all_empty_circuit():
    """qshow_all on empty circuit returns empty dict."""
    reset()
    results = qshow_all(["native"], print_results=False)
    assert results == {}


def test_qshow_all_single_backend():
    """qshow_all with single backend works without process pool."""
    reset()
    qgate(gates.X, 0)
    results = qshow_all(["native"], shots=100, print_results=False)
    assert "native" in results
    assert results["native"].counts.get("1", 0) == 100


def test_qshow_all_print(capsys):
    """qshow_all with print_results=True outputs results."""
    reset()
    qgate(gates.X, 0)
    qshow_all(["native"], shots=100, print_results=True)
    captured = capsys.readouterr()
    assert "native" in captured.out or "100" in captured.out
