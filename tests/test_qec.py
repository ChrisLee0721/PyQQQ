"""Tests for the quantum error correction module."""

from __future__ import annotations

from quonic.ir import Circuit
from quonic.qec import (
    BitFlipCode,
    PhaseFlipCode,
    ShorCode,
    StabilizerCode,
    SteaneCode,
    UnionFindDecoder,
    decode_lookup,
    decode_mwpm,
)

# ---------------------------------------------------------------------------
# 1. Error correction codes
# ---------------------------------------------------------------------------


def test_bit_flip_code():
    code = BitFlipCode()
    assert code.n_data == 1
    assert code.n_syndrome == 2
    assert code.n_total == 3
    c = code.encode(Circuit())
    assert c.num_qubits == 3


def test_phase_flip_code():
    code = PhaseFlipCode()
    assert code.n_data == 1
    assert code.n_syndrome == 2
    assert code.n_total == 3
    c = code.encode(Circuit())
    assert c.num_qubits == 3


def test_shor_code():
    code = ShorCode()
    assert code.n_data == 1
    assert code.n_syndrome == 8
    assert code.n_total == 9
    c = code.encode(Circuit())
    assert c.num_qubits == 9


def test_steane_code():
    code = SteaneCode()
    assert code.n_data == 1
    assert code.n_syndrome == 6
    assert code.n_total == 7
    c = code.encode(Circuit())
    assert c.num_qubits == 7


# ---------------------------------------------------------------------------
# 2. Stabilizer code
# ---------------------------------------------------------------------------


def test_stabilizer_code():
    code = StabilizerCode(["ZZII", "IIZZ", "XIII", "IIXI"])
    assert code.n_qubits == 4
    assert code.n_stabilizers == 4
    assert not code.is_valid([1, 0, 0, 0])
    assert code.is_valid([0, 0, 0, 0])


# ---------------------------------------------------------------------------
# 3. Decoders
# ---------------------------------------------------------------------------


def test_decode_lookup():
    code = BitFlipCode()
    # syndrome (1, 0) → error on qubit 0
    correction = decode_lookup([1, 0], code)
    assert correction == [1, 0, 0]

    # syndrome (0, 0) → no error
    correction = decode_lookup([0, 0], code)
    assert correction == [0, 0, 0]


def test_decode_mwpm():
    code = BitFlipCode()
    correction = decode_mwpm([1, 0], code)
    assert len(correction) == 3
    assert correction[0] == 1


# ---------------------------------------------------------------------------
# 4. Stabilizer syndrome computation
# ---------------------------------------------------------------------------


def test_stabilizer_syndrome_no_error():
    """Syndrome of |0000> against ZZZZ stabilizers should be all zeros."""
    import numpy as np

    code = StabilizerCode(["ZZII", "IIZZ"])
    # |0000> is a +1 eigenstate of all Z-type stabilizers
    state = np.zeros(16, dtype=complex)
    state[0] = 1.0
    syndrome = code.syndrome_vector(state)
    assert syndrome == [0, 0], f"Expected [0,0] but got {syndrome}"


def test_stabilizer_syndrome_with_error():
    """Syndrome detects bit-flip errors."""
    import numpy as np

    code = StabilizerCode(["ZZII", "IIZZ"])
    # Apply X on qubit 0 (rightmost bit): |0000> → |0001>
    # IIZZ covers qubits 1,0 → anti-commutes with X_0 → syndrome[1] = 1
    # ZZII covers qubits 3,2 → commutes with X_0 → syndrome[0] = 0
    state = np.zeros(16, dtype=complex)
    state[1] = 1.0  # |0001>
    syndrome = code.syndrome_vector(state)
    assert syndrome[1] == 1, f"IIZZ should detect X on qubit 0, got {syndrome}"
    assert syndrome[0] == 0, f"ZZII should not detect X on qubit 0, got {syndrome}"


def test_stabilizer_detect_error():
    """detect_error should identify single-qubit errors."""
    code = StabilizerCode(["ZZII", "IIZZ"])
    # Syndrome for X on qubit 0
    error = code.detect_error([1, 0])
    assert error is not None
    assert error[0] == "X"  # X on qubit 0


def test_stabilizer_logical_operator():
    """Logical operators should be defined."""
    code = StabilizerCode(
        ["ZZII", "IIZZ"],
        logical_ops={"X": ["XXXX"], "Z": ["ZZII"]},
    )
    lx = code.logical_operator("X")
    assert lx is not None
    assert lx.shape == (16, 16)


# ---------------------------------------------------------------------------
# 5. Union-Find decoder
# ---------------------------------------------------------------------------


def test_union_find_decoder_no_error():
    """No syndrome defects → no correction."""
    code = BitFlipCode()
    decoder = UnionFindDecoder(code)
    correction = decoder.decode([0, 0])
    assert all(c == 0 for c in correction)


def test_union_find_decoder_single_error():
    """Single defect → correction applied."""
    code = BitFlipCode()
    decoder = UnionFindDecoder(code)
    correction = decoder.decode([1, 0])
    assert len(correction) == 3
    # At least one qubit should be corrected
    assert any(c == 1 for c in correction)
