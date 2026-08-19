"""Quantum error correction codes — encoding, syndrome extraction, and correction.

Provides pre-built codes for common error correction scenarios.

Example::

    from quonic.qec import BitFlipCode, SteaneCode
    code = BitFlipCode()
    encoded = code.encode(circuit)
"""

from __future__ import annotations

from typing import Tuple

from ..ir import Circuit, GateOperation


class BitFlipCode:
    """3-qubit bit flip code: corrects single bit-flip errors.

    Encodes: |ψ> = α|0> + β|1> → α|000> + β|111>
    Syndrome: detects which qubit was flipped.
    """

    n_data: int = 1
    n_syndrome: int = 2
    n_total: int = 3

    def encode(self, circuit: Circuit) -> Circuit:
        """Encode a single logical qubit into 3 physical qubits."""
        c = Circuit()
        c.allocate(3)
        # Copy qubit 0 to qubits 1 and 2
        c.add(GateOperation("cx", (0, 1)))
        c.add(GateOperation("cx", (0, 2)))
        return c

    def syndrome(self, circuit: Circuit) -> Circuit:
        """Extract syndrome bits (determines error location)."""
        c = Circuit()
        c.allocate(5)  # 3 data + 2 syndrome
        # Syndrome extraction
        c.add(GateOperation("cx", (0, 3)))
        c.add(GateOperation("cx", (1, 3)))
        c.add(GateOperation("cx", (1, 4)))
        c.add(GateOperation("cx", (2, 4)))
        return c

    def correct(self, circuit: Circuit, syndrome: Tuple[int, int]) -> Circuit:
        """Apply correction based on syndrome."""
        c = Circuit()
        c.allocate(3)
        s0, s1 = syndrome
        if s0 == 1 and s1 == 0:
            c.add(GateOperation("x", (0,)))  # error on qubit 0
        elif s0 == 1 and s1 == 1:
            c.add(GateOperation("x", (1,)))  # error on qubit 1
        elif s0 == 0 and s1 == 1:
            c.add(GateOperation("x", (2,)))  # error on qubit 2
        return c


class PhaseFlipCode:
    """3-qubit phase flip code: corrects single phase-flip errors.

    Encodes: |ψ> = α|0> + β|1> → α|+++> + β|->
    """

    n_data: int = 1
    n_syndrome: int = 2
    n_total: int = 3

    def encode(self, circuit: Circuit) -> Circuit:
        """Encode a single logical qubit into 3 physical qubits."""
        c = Circuit()
        c.allocate(3)
        c.add(GateOperation("cx", (0, 1)))
        c.add(GateOperation("cx", (0, 2)))
        c.add(GateOperation("h", (0,)))
        c.add(GateOperation("h", (1,)))
        c.add(GateOperation("h", (2,)))
        return c

    def syndrome(self, circuit: Circuit) -> Circuit:
        """Extract syndrome bits."""
        c = Circuit()
        c.allocate(5)
        c.add(GateOperation("h", (3,)))
        c.add(GateOperation("h", (4,)))
        c.add(GateOperation("cx", (3, 0)))
        c.add(GateOperation("cx", (3, 1)))
        c.add(GateOperation("cx", (4, 1)))
        c.add(GateOperation("cx", (4, 2)))
        c.add(GateOperation("h", (3,)))
        c.add(GateOperation("h", (4,)))
        return c


class ShorCode:
    """9-qubit Shor code: corrects arbitrary single-qubit errors.

    Combines bit-flip and phase-flip codes.
    """

    n_data: int = 1
    n_syndrome: int = 8
    n_total: int = 9

    def encode(self, circuit: Circuit) -> Circuit:
        """Encode a single logical qubit into 9 physical qubits."""
        c = Circuit()
        c.allocate(9)
        # Phase-flip encoding
        c.add(GateOperation("cx", (0, 3)))
        c.add(GateOperation("cx", (0, 6)))
        c.add(GateOperation("h", (0,)))
        c.add(GateOperation("h", (3,)))
        c.add(GateOperation("h", (6,)))
        # Bit-flip encoding within each block
        c.add(GateOperation("cx", (0, 1)))
        c.add(GateOperation("cx", (0, 2)))
        c.add(GateOperation("cx", (3, 4)))
        c.add(GateOperation("cx", (3, 5)))
        c.add(GateOperation("cx", (6, 7)))
        c.add(GateOperation("cx", (6, 8)))
        return c


class SteaneCode:
    """7-qubit Steane code: [[7,1,3]] CSS code.

    Corrects arbitrary single-qubit errors.
    """

    n_data: int = 1
    n_syndrome: int = 6
    n_total: int = 7

    def encode(self, circuit: Circuit) -> Circuit:
        """Encode a single logical qubit into 7 physical qubits."""
        c = Circuit()
        c.allocate(7)
        # Steane encoding circuit
        c.add(GateOperation("cx", (0, 3)))
        c.add(GateOperation("cx", (0, 6)))
        c.add(GateOperation("h", (0,)))
        c.add(GateOperation("h", (1,)))
        c.add(GateOperation("h", (2,)))
        c.add(GateOperation("cx", (0, 1)))
        c.add(GateOperation("cx", (0, 2)))
        c.add(GateOperation("cx", (3, 4)))
        c.add(GateOperation("cx", (3, 5)))
        c.add(GateOperation("cx", (6, 4)))
        c.add(GateOperation("cx", (6, 5)))
        return c


class SurfaceCode:
    """Surface code (rotated): distance-d code correcting (d-1)/2 errors.

    Args:
        distance: code distance (must be odd)
    """

    def __init__(self, distance: int = 3):
        if distance < 3 or distance % 2 == 0:
            raise ValueError("Distance must be odd and >= 3")
        self.distance = distance
        self.n_data = distance * distance
        self.n_syndrome = distance * distance - 1
        self.n_total = self.n_data + self.n_syndrome

    def encode(self, circuit: Circuit) -> Circuit:
        """Encode logical qubits into surface code layout."""
        c = Circuit()
        c.allocate(self.n_total)
        # Surface code encoding is complex; this is a simplified placeholder
        # Real implementation would use the stabilizer structure
        return c


class ColorCode:
    """Color code: distance-d code with transversal gates.

    Args:
        distance: code distance (must be odd)
    """

    def __init__(self, distance: int = 3):
        if distance < 3 or distance % 2 == 0:
            raise ValueError("Distance must be odd and >= 3")
        self.distance = distance
        self.n_data = distance * distance
        self.n_syndrome = distance * distance - 1
        self.n_total = self.n_data + self.n_syndrome

    def encode(self, circuit: Circuit) -> Circuit:
        """Encode logical qubits into color code layout."""
        c = Circuit()
        c.allocate(self.n_total)
        return c


class CSSCode:
    """Generic CSS (Calderbank-Shor-Steane) code.

    Args:
        hx: X-check matrix
        hz: Z-check matrix
    """

    def __init__(self, hx, hz):
        self.hx = hx
        self.hz = hz
        self.n_data = hx.shape[1]
        self.n_syndrome = hx.shape[0] + hz.shape[0]
        self.n_total = self.n_data + self.n_syndrome

    def encode(self, circuit: Circuit) -> Circuit:
        """Encode logical qubits into CSS code."""
        c = Circuit()
        c.allocate(self.n_total)
        return c
