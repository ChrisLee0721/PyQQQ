"""Pauli gate translators (x / y / z)."""

from __future__ import annotations

from typing import Any, Dict, List

from .base import Translator


class XTranslator(Translator):
    name = "x"

    def to_qiskit(self, qc: Any, op: Any, cregs: Dict[str, int]) -> None:
        qc.x(op.qubits[0])

    def to_cirq(
        self, cirq: Any, op: Any, qubits: List[Any], cregs: Dict[str, str]
    ) -> List[Any]:
        return [cirq.X(qubits[op.qubits[0]])]

    def to_pennylane(self, qml: Any, op: Any, cregs: Dict[str, Any]) -> None:
        qml.PauliX(wires=op.qubits[0])


class YTranslator(Translator):
    name = "y"

    def to_qiskit(self, qc: Any, op: Any, cregs: Dict[str, int]) -> None:
        qc.y(op.qubits[0])

    def to_cirq(
        self, cirq: Any, op: Any, qubits: List[Any], cregs: Dict[str, str]
    ) -> List[Any]:
        return [cirq.Y(qubits[op.qubits[0]])]

    def to_pennylane(self, qml: Any, op: Any, cregs: Dict[str, Any]) -> None:
        qml.PauliY(wires=op.qubits[0])


class ZTranslator(Translator):
    name = "z"

    def to_qiskit(self, qc: Any, op: Any, cregs: Dict[str, int]) -> None:
        qc.z(op.qubits[0])

    def to_cirq(
        self, cirq: Any, op: Any, qubits: List[Any], cregs: Dict[str, str]
    ) -> List[Any]:
        return [cirq.Z(qubits[op.qubits[0]])]

    def to_pennylane(self, qml: Any, op: Any, cregs: Dict[str, Any]) -> None:
        qml.PauliZ(wires=op.qubits[0])
