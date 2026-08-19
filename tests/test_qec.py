"""Tests for the quantum error correction module."""

from __future__ import annotations

from quonic.ir import Circuit
from quonic.qec import (
    BitFlipCode,
    PhaseFlipCode,
    ShorCode,
    StabilizerCode,
    SteaneCode,
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
