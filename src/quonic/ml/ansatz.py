"""Variational ansatz library — parameterized quantum circuits for QML.

Provides pre-built ansatz structures for variational quantum algorithms.

Example::

    from quonic.ml import Ansatz
    ansatz = Ansatz.hardware_efficient(n_qubits=4, layers=3)
    circuit = ansatz.build(params)
"""

from __future__ import annotations

from typing import List

from ..ir import Circuit, GateOperation


class Ansatz:
    """Variational ansatz builder."""

    @staticmethod
    def hardware_efficient(
        n_qubits: int,
        layers: int = 1,
        entanglement: str = "linear",
    ) -> "AnsatzBuilder":
        """Hardware-efficient ansatz: Ry rotations + entangling CX ladder.

        Args:
            n_qubits: number of qubits
            layers: number of rotation + entanglement layers
            entanglement: "linear" (nearest-neighbor CX) or "full" (all-pairs CX)

        Returns:
            AnsatzBuilder with build(params) method.
        """
        return _HardwareEfficient(n_qubits, layers, entanglement)

    @staticmethod
    def qaoa(n_qubits: int, p: int = 1) -> "AnsatzBuilder":
        """QAOA ansatz: alternating mixer and problem unitaries.

        Args:
            n_qubits: number of qubits
            p: number of QAOA layers

        Returns:
            AnsatzBuilder with build(params) method.
        """
        return _QAOA(n_qubits, p)

    @staticmethod
    def uccsd(n_qubits: int) -> "AnsatzBuilder":
        """UCCSD ansatz (simplified): singles + doubles excitations.

        Args:
            n_qubits: number of qubits

        Returns:
            AnsatzBuilder with build(params) method.
        """
        return _UCCSD(n_qubits)


class AnsatzBuilder:
    """Base class for ansatz builders."""

    n_params: int

    def build(self, params: List[float]) -> Circuit:
        """Build a circuit from parameters."""
        raise NotImplementedError


class _HardwareEfficient(AnsatzBuilder):
    """Hardware-efficient ansatz: Ry rotations + CX ladder."""

    def __init__(self, n_qubits: int, layers: int, entanglement: str):
        self.n_qubits = n_qubits
        self.layers = layers
        self.entanglement = entanglement
        # Each layer: n Ry rotations + (n-1) CX gates
        self.n_params = n_qubits * layers

    def build(self, params: List[float]) -> Circuit:
        c = Circuit()
        c.allocate(self.n_qubits)
        idx = 0
        for layer in range(self.layers):
            # Rotation layer
            for q in range(self.n_qubits):
                c.add(GateOperation("ry", (q,), (params[idx],)))
                idx += 1
            # Entanglement layer
            if self.entanglement == "linear":
                for q in range(self.n_qubits - 1):
                    c.add(GateOperation("cx", (q, q + 1)))
            elif self.entanglement == "full":
                for i in range(self.n_qubits):
                    for j in range(i + 1, self.n_qubits):
                        c.add(GateOperation("cx", (i, j)))
        return c


class _QAOA(AnsatzBuilder):
    """QAOA ansatz: alternating mixer and problem unitaries."""

    def __init__(self, n_qubits: int, p: int):
        self.n_qubits = n_qubits
        self.p = p
        # Each layer: n Rx rotations (mixer) + n CX + n Rz (problem)
        self.n_params = 2 * n_qubits * p

    def build(self, params: List[float]) -> Circuit:
        c = Circuit()
        c.allocate(self.n_qubits)
        # Initial superposition
        for q in range(self.n_qubits):
            c.add(GateOperation("h", (q,)))
        idx = 0
        for layer in range(self.p):
            # Problem unitary: ZZ interactions
            for q in range(self.n_qubits - 1):
                c.add(GateOperation("cx", (q, q + 1)))
                c.add(GateOperation("rz", (q + 1,), (params[idx],)))
                idx += 1
                c.add(GateOperation("cx", (q, q + 1)))
            # Mixer unitary: Rx rotations
            for q in range(self.n_qubits):
                c.add(GateOperation("rx", (q,), (params[idx],)))
                idx += 1
        return c


class _UCCSD(AnsatzBuilder):
    """Simplified UCCSD ansatz: singles + doubles excitations."""

    def __init__(self, n_qubits: int):
        self.n_qubits = n_qubits
        # Singles: n_qubits, Doubles: n_qubits*(n_qubits-1)/2
        self.n_params = n_qubits + n_qubits * (n_qubits - 1) // 2

    def build(self, params: List[float]) -> Circuit:
        c = Circuit()
        c.allocate(self.n_qubits)
        idx = 0
        # Singles excitations
        for q in range(self.n_qubits):
            c.add(GateOperation("ry", (q,), (params[idx],)))
            idx += 1
        # Doubles excitations
        for i in range(self.n_qubits):
            for j in range(i + 1, self.n_qubits):
                c.add(GateOperation("cx", (i, j)))
                c.add(GateOperation("ry", (j,), (params[idx],)))
                idx += 1
                c.add(GateOperation("cx", (i, j)))
        return c
