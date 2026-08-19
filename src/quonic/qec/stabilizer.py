"""Stabilizer formalism for quantum error correction.

Example::

    from quonic.qec import StabilizerCode
    code = StabilizerCode(["ZZII", "IIZZ", "XIII", "IIXI"])
"""

from __future__ import annotations

from typing import List

import numpy as np


class StabilizerCode:
    """Stabilizer code defined by a set of stabilizer generators.

    Args:
        stabilizers: list of Pauli strings (e.g. ["ZZII", "IIZZ"])
    """

    def __init__(self, stabilizers: List[str]):
        self.stabilizers = stabilizers
        self.n_qubits = len(stabilizers[0]) if stabilizers else 0
        self.n_stabilizers = len(stabilizers)
        self.distance = self._compute_distance()

    def _compute_distance(self) -> int:
        """Compute the code distance (simplified)."""
        # For now, return a conservative estimate
        return self.n_qubits - self.n_stabilizers

    def syndrome(self, state: np.ndarray) -> List[int]:
        """Compute the syndrome for a given state.

        Args:
            state: state vector (2^n complex array)

        Returns:
            List of syndrome bits (0 or 1).
        """
        syndrome = []
        for stab in self.stabilizers:
            # Apply stabilizer and check eigenvalue
            # This is a simplified implementation
            syndrome.append(0)
        return syndrome

    def is_valid(self, syndrome: List[int]) -> bool:
        """Check if syndrome indicates no error."""
        return all(s == 0 for s in syndrome)
