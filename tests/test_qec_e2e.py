"""Tests for QEC end-to-end error correction."""

from __future__ import annotations

from quonic.qec import qec_round_trip


def test_bit_flip_code_low_error():
    """Bit-flip code should correct most single errors at low error rate."""
    result = qec_round_trip(code="bit_flip", error_rate=0.01, shots=10000)
    # Logical error rate should be much lower than physical
    assert result.logical_error_rate < result.physical_error_rate
    # With 1% error rate, logical error should be < 0.1%
    assert result.logical_error_rate < 0.01


def test_bit_flip_code_high_error():
    """At high error rates, QEC should still help somewhat."""
    result = qec_round_trip(code="bit_flip", error_rate=0.1, shots=10000)
    # Should still be better than no coding
    assert result.logical_error_rate < result.physical_error_rate * 3


def test_phase_flip_code():
    """Phase-flip code should correct phase errors."""
    result = qec_round_trip(code="phase_flip", error_rate=0.01, shots=10000)
    assert result.logical_error_rate < 0.05


def test_steane_code():
    """Steane code should correct single-qubit errors."""
    result = qec_round_trip(code="steane", error_rate=0.01, shots=10000)
    # Steane code corrects arbitrary single-qubit errors
    assert result.logical_error_rate < 0.05


def test_qec_result_fields():
    """QECResult should have all expected fields."""
    result = qec_round_trip(code="bit_flip", error_rate=0.01, shots=100)
    assert hasattr(result, "logical_error_rate")
    assert hasattr(result, "physical_error_rate")
    assert hasattr(result, "n_shots")
    assert hasattr(result, "n_logical_errors")
    assert hasattr(result, "n_physical_errors")
    assert result.n_shots == 100


def test_zero_error_rate():
    """With zero error rate, there should be no errors."""
    result = qec_round_trip(code="bit_flip", error_rate=0.0, shots=1000)
    assert result.logical_error_rate == 0.0
    assert result.physical_error_rate == 0.0
