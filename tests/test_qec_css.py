"""Tests for CSS code encoding and logical gates."""

from __future__ import annotations

import numpy as np

from quonic.ir import Circuit
from quonic.qec import CSSCode, SteaneCode


def test_steane_logical_x():
    """Steane logical X should flip all 7 qubits (transversal)."""
    code = SteaneCode()
    c = Circuit()
    c.allocate(7)
    lx = code.logical_x(c)
    ops = [op for op in lx.ops if op.name != "measure"]
    assert len(ops) == 7
    assert all(op.name == "x" for op in ops)


def test_steane_logical_z():
    """Steane logical Z should apply Z to all 7 qubits."""
    code = SteaneCode()
    c = Circuit()
    c.allocate(7)
    lz = code.logical_z(c)
    ops = [op for op in lz.ops if op.name != "measure"]
    assert len(ops) == 7
    assert all(op.name == "z" for op in ops)


def test_steane_logical_h():
    """Steane logical H should apply H to all 7 qubits."""
    code = SteaneCode()
    c = Circuit()
    c.allocate(7)
    lh = code.logical_h(c)
    ops = [op for op in lh.ops if op.name != "measure"]
    assert len(ops) == 7
    assert all(op.name == "h" for op in ops)


def test_css_code_encode():
    """CSS code encoding should add CX and CZ gates for syndrome extraction."""
    hx = np.array([[1, 1, 0, 0], [0, 1, 1, 0]])
    hz = np.array([[1, 0, 1, 0], [0, 1, 0, 1]])
    code = CSSCode(hx, hz)
    assert code.n_data == 4
    assert code.n_x_checks == 2
    assert code.n_z_checks == 2
    assert code.n_syndrome == 4

    c = Circuit()
    encoded = code.encode(c)
    ops = [op for op in encoded.ops if op.name != "measure"]
    # Should have CX for X-checks and CZ for Z-checks
    assert any(op.name == "cx" for op in ops)
    assert any(op.name == "cz" for op in ops)


def test_css_code_repr():
    """CSSCode should have a readable repr."""
    hx = np.array([[1, 1, 0]])
    hz = np.array([[0, 1, 1]])
    code = CSSCode(hx, hz)
    r = repr(code)
    assert "CSSCode" in r
    assert "n_data=3" in r
