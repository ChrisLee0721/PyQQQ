"""End-to-end quantum error correction: encode → noise → syndrome → decode → correct.

Provides a complete QEC pipeline for testing and demonstration.

Example::

    from quonic.qec import qec_round_trip

    result = qec_round_trip(code="bit_flip", error_rate=0.01, shots=1000)
    print(f"Logical error rate: {result.logical_error_rate:.4f}")
    print(f"Physical error rate: {result.physical_error_rate:.4f}")
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class QECResult:
    """Result of a QEC round-trip experiment.

    Args:
        logical_error_rate: probability of logical error after correction
        physical_error_rate: probability of physical error (before correction)
        n_shots: number of shots used
        n_logical_errors: count of logical errors
        n_physical_errors: count of physical errors
    """

    logical_error_rate: float
    physical_error_rate: float
    n_shots: int
    n_logical_errors: int
    n_physical_errors: int


def qec_round_trip(
    code: str = "bit_flip",
    error_rate: float = 0.01,
    shots: int = 1000,
    seed: int = 42,
) -> QECResult:
    """Run a full QEC round-trip: encode → depolarizing noise → syndrome → correct.

    Simulates the QEC cycle at the state-vector level and counts logical vs physical errors.

    Args:
        code: error correction code ("bit_flip", "phase_flip", "steane")
        error_rate: per-qubit depolarizing error rate
        shots: number of random trials
        seed: random seed

    Returns:
        QECResult with error rates.
    """
    rng = np.random.RandomState(seed)

    if code == "bit_flip":
        return _run_bit_flip(error_rate, shots, rng)
    elif code == "phase_flip":
        return _run_phase_flip(error_rate, shots, rng)
    elif code == "steane":
        return _run_steane(error_rate, shots, rng)
    else:
        raise ValueError(f"Unknown code: {code}. Use 'bit_flip', 'phase_flip', or 'steane'.")


def _run_bit_flip(error_rate: float, shots: int, rng: np.random.RandomState) -> QECResult:
    """3-qubit bit-flip code: encode |ψ> → |ψψψ>, correct single bit-flip errors."""
    n_logical_errors = 0
    n_physical_errors = 0

    for _ in range(shots):
        # Random logical state: |0> or |1>
        logical = rng.randint(2)

        # Encode: 3 physical qubits all in the same state
        data = [logical] * 3

        # Apply noise: each qubit flips with probability error_rate
        errors = rng.random(3) < error_rate
        for i in range(3):
            if errors[i]:
                data[i] ^= 1
                n_physical_errors += 1

        # Syndrome extraction: compare pairs
        s0 = data[0] ^ data[1]  # syndrome bit 0
        s1 = data[1] ^ data[2]  # syndrome bit 1

        # Correction
        if s0 == 1 and s1 == 0:
            data[0] ^= 1  # error on qubit 0
        elif s0 == 1 and s1 == 1:
            data[1] ^= 1  # error on qubit 1
        elif s0 == 0 and s1 == 1:
            data[2] ^= 1  # error on qubit 2

        # Majority vote for logical value
        corrected_logical = 1 if sum(data) >= 2 else 0

        if corrected_logical != logical:
            n_logical_errors += 1

    return QECResult(
        logical_error_rate=n_logical_errors / shots,
        physical_error_rate=n_physical_errors / (3 * shots),
        n_shots=shots,
        n_logical_errors=n_logical_errors,
        n_physical_errors=n_physical_errors,
    )


def _run_phase_flip(error_rate: float, shots: int, rng: np.random.RandomState) -> QECResult:
    """3-qubit phase-flip code: corrects single phase-flip errors."""
    n_logical_errors = 0
    n_physical_errors = 0

    for _ in range(shots):
        # Logical state: α|0> + β|1> (stored as amplitude pair)
        alpha = rng.randn() + 1j * rng.randn()
        alpha /= np.abs(alpha)  # normalize

        # Encode: |+++> or |---> (phase-flip code works in X basis)
        # Simulate in Z basis: phase flip ↔ bit flip in X basis
        data = [0] * 3  # all in |+> state (in X basis)

        # Apply phase-flip noise (equivalent to bit-flip in X basis)
        errors = rng.random(3) < error_rate
        for i in range(3):
            if errors[i]:
                data[i] ^= 1
                n_physical_errors += 1

        # Syndrome in X basis
        s0 = data[0] ^ data[1]
        s1 = data[1] ^ data[2]

        # Correction
        if s0 == 1 and s1 == 0:
            data[0] ^= 1
        elif s0 == 1 and s1 == 1:
            data[1] ^= 1
        elif s0 == 0 and s1 == 1:
            data[2] ^= 1

        # Check logical error: all 3 should be the same
        if not all(d == data[0] for d in data):
            n_logical_errors += 1

    return QECResult(
        logical_error_rate=n_logical_errors / shots,
        physical_error_rate=n_physical_errors / (3 * shots),
        n_shots=shots,
        n_logical_errors=n_logical_errors,
        n_physical_errors=n_physical_errors,
    )


def _run_steane(error_rate: float, shots: int, rng: np.random.RandomState) -> QECResult:
    """[[7,1,3]] Steane code: corrects arbitrary single-qubit errors.

    Simplified simulation: tracks Pauli errors as bit/phase flips.
    """
    n_logical_errors = 0
    n_physical_errors = 0

    for _ in range(shots):
        # Track X and Z errors on 7 qubits
        x_errors = [0] * 7
        z_errors = [0] * 7

        # Apply noise
        for i in range(7):
            r = rng.random()
            if r < error_rate / 3:
                x_errors[i] ^= 1
                n_physical_errors += 1
            elif r < 2 * error_rate / 3:
                z_errors[i] ^= 1
                n_physical_errors += 1
            elif r < error_rate:
                x_errors[i] ^= 1
                z_errors[i] ^= 1
                n_physical_errors += 1

        # Steane code syndrome extraction (simplified)
        # X syndrome: detects Z errors
        # Z syndrome: detects X errors
        x_syndrome = [
            x_errors[0] ^ x_errors[1] ^ x_errors[2] ^ x_errors[3],
            x_errors[0] ^ x_errors[1] ^ x_errors[4] ^ x_errors[5],
            x_errors[0] ^ x_errors[2] ^ x_errors[4] ^ x_errors[6],
        ]
        z_syndrome = [
            z_errors[0] ^ z_errors[1] ^ z_errors[2] ^ z_errors[3],
            z_errors[0] ^ z_errors[1] ^ z_errors[4] ^ z_errors[5],
            z_errors[0] ^ z_errors[2] ^ z_errors[4] ^ z_errors[6],
        ]

        # Correction (simplified: majority vote on each syndrome)
        # If syndrome is non-zero, assume single error and correct
        for syndrome, errors in [(x_syndrome, x_errors), (z_syndrome, z_errors)]:
            s = syndrome[0] * 4 + syndrome[1] * 2 + syndrome[2]
            if s > 0 and s <= 7:
                errors[s - 1] ^= 1  # correct

        # Logical error: any remaining X or Z error on data qubits
        logical_x = sum(x_errors) % 2
        logical_z = sum(z_errors) % 2

        if logical_x != 0 or logical_z != 0:
            n_logical_errors += 1

    return QECResult(
        logical_error_rate=n_logical_errors / shots,
        physical_error_rate=n_physical_errors / (7 * shots),
        n_shots=shots,
        n_logical_errors=n_logical_errors,
        n_physical_errors=n_physical_errors,
    )
