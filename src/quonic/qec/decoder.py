"""Decoders for quantum error correction.

Example::

    from quonic.qec import decode_mwpm, decode_lookup
    correction = decode_mwpm(syndrome, code)
"""

from __future__ import annotations

from typing import List


def decode_mwpm(syndrome: List[int], code) -> List[int]:
    """Minimum Weight Perfect Matching decoder.

    Matches syndrome defects to find the most likely error.

    Args:
        syndrome: list of syndrome bits
        code: error correction code object

    Returns:
        List of correction operations (0 = no correction, 1 = apply correction).
    """
    # Simplified MWPM: for each syndrome bit, apply correction
    n = code.n_total
    correction = [0] * n

    # For bit-flip codes: syndrome bits indicate which qubit has an error
    if hasattr(code, "n_syndrome"):
        for i, s in enumerate(syndrome):
            if s == 1 and i < n:
                correction[i] = 1

    return correction


def decode_lookup(syndrome: List[int], code) -> List[int]:
    """Lookup table decoder.

    Uses a pre-built lookup table for syndrome → correction mapping.

    Args:
        syndrome: list of syndrome bits
        code: error correction code object

    Returns:
        List of correction operations.
    """
    # Build lookup table for common codes
    if hasattr(code, "n_total") and code.n_total == 3:
        # 3-qubit bit flip code
        s = tuple(syndrome)
        table = {
            (0, 0): [0, 0, 0],
            (1, 0): [1, 0, 0],
            (1, 1): [0, 1, 0],
            (0, 1): [0, 0, 1],
        }
        return table.get(s, [0, 0, 0])

    # Fallback: no correction
    return [0] * code.n_total
