"""Tests for run_circuits — parallel multi-circuit execution."""

from __future__ import annotations

import os

import pytest

from quonic import gates, qgate, run_circuits


@pytest.mark.skipif(os.environ.get("CI") == "true", reason="ProcessPoolExecutor hangs on Linux CI spawn")
def test_run_circuits_basic():
    """run_circuits runs different circuits in parallel."""
    def bell():
        qgate(gates.H, 0)
        qgate(gates.CX, 0, 1)

    def flip():
        qgate(gates.X, 0)

    results = run_circuits([bell, flip], backend="native", shots=128, print_results=False)
    assert len(results) == 2
    bell_counts = results[0].counts
    assert bell_counts.get("00", 0) + bell_counts.get("11", 0) > 100
    assert results[1].counts.get("1", 0) == 128


def test_run_circuits_empty():
    """run_circuits with empty list returns empty dict."""
    results = run_circuits([], backend="native", print_results=False)
    assert results == {}


def test_run_circuits_single():
    """run_circuits with single builder works without process pool."""
    def flip():
        qgate(gates.X, 0)

    results = run_circuits([flip], backend="native", shots=100, print_results=False)
    assert len(results) == 1
    assert results[0].counts.get("1", 0) == 100


@pytest.mark.skipif(os.environ.get("CI") == "true", reason="ProcessPoolExecutor hangs on Linux CI spawn")
def test_run_circuits_resets():
    """run_circuits resets global state before each builder."""
    def first():
        qgate(gates.X, 0)

    def second():
        qgate(gates.H, 0)

    results = run_circuits([first, second], backend="native", shots=256, print_results=False)
    assert results[0].counts.get("1", 0) == 256
    p0 = results[1].counts.get("0", 0) / 256
    assert 0.3 < p0 < 0.7


def test_run_circuits_print(capsys):
    """run_circuits with print_results=True outputs results."""
    def flip():
        qgate(gates.X, 0)

    run_circuits([flip], backend="native", shots=100, print_results=True)
    captured = capsys.readouterr()
    assert "100" in captured.out
