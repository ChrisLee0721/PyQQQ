"""Tests for the quantum control / pulse module."""

from __future__ import annotations

import numpy as np

from quonic.pulse import (
    CrossResonancePulse,
    DragPulse,
    GaussianPulse,
    cpmg_sequence,
    rabi_calibration,
    t1_calibration,
    t2_calibration,
    xy4_sequence,
)

# ---------------------------------------------------------------------------
# 1. Pulse waveforms
# ---------------------------------------------------------------------------


def test_gaussian_pulse():
    p = GaussianPulse(duration=20, sigma=5, amplitude=0.5)
    w = p.waveform()
    assert len(w) == 20
    assert abs(w[10] - 0.5) < 0.01  # peak at center
    assert abs(w[0]) < abs(w[10])  # lower at edges than at center


def test_drag_pulse():
    p = DragPulse(duration=20, sigma=5, amplitude=0.5, beta=0.1)
    w = p.waveform()
    assert len(w) == 20
    assert np.iscomplexobj(w)  # DRAG has imaginary component


def test_cross_resonance_pulse():
    p = CrossResonancePulse(duration=20, amplitude=0.5, detuning=0.1)
    w = p.waveform()
    assert len(w) == 20
    assert np.iscomplexobj(w)


# ---------------------------------------------------------------------------
# 2. Calibration routines
# ---------------------------------------------------------------------------


def test_rabi_calibration():
    result = rabi_calibration(qubit=0, amplitudes=[0.1, 0.2, 0.3, 0.4, 0.5])
    assert len(result.amplitudes) == 5
    assert len(result.populations) == 5
    assert 0 <= result.pi_amplitude <= 1


def test_t1_calibration():
    result = t1_calibration(qubit=0, delays=[10, 20, 50, 100])
    assert len(result.delays) == 4
    assert len(result.populations) == 4
    assert result.t1 > 0


def test_t2_calibration():
    result = t2_calibration(qubit=0, delays=[10, 20, 50, 100])
    assert len(result.delays) == 4
    assert len(result.populations) == 4
    assert result.t2 > 0


# ---------------------------------------------------------------------------
# 3. Decoupling sequences
# ---------------------------------------------------------------------------


def test_cpmg_sequence():
    times = cpmg_sequence(n_pulses=4, delay=100)
    assert len(times) == 4
    assert all(t > 0 for t in times)


def test_xy4_sequence():
    times = xy4_sequence(delay=100)
    assert len(times) == 4
    assert all(t > 0 for t in times)
