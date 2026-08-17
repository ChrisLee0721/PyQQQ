"""Controlled gate translators (cx / cz / ccx)."""

from __future__ import annotations

from typing import Any, Dict, List

from .base import Translator


class CXTranslator(Translator):
    name = "cx"

    def to_qiskit(self, qc: Any, op: Any, cregs: Dict[str, int]) -> None:
        qc.cx(op.qubits[0], op.qubits[1])

    def to_cirq(
        self, cirq: Any, op: Any, qubits: List[Any], cregs: Dict[str, str]
    ) -> List[Any]:
        return [cirq.CNOT(qubits[op.qubits[0]], qubits[op.qubits[1]])]

    def to_pennylane(self, qml: Any, op: Any, cregs: Dict[str, Any]) -> None:
        qml.CNOT(wires=[op.qubits[0], op.qubits[1]])


class CZTranslator(Translator):
    name = "cz"

    def to_qiskit(self, qc: Any, op: Any, cregs: Dict[str, int]) -> None:
        qc.cz(op.qubits[0], op.qubits[1])

    def to_cirq(
        self, cirq: Any, op: Any, qubits: List[Any], cregs: Dict[str, str]
    ) -> List[Any]:
        return [cirq.CZ(qubits[op.qubits[0]], qubits[op.qubits[1]])]

    def to_pennylane(self, qml: Any, op: Any, cregs: Dict[str, Any]) -> None:
        qml.CZ(wires=[op.qubits[0], op.qubits[1]])


class CCXTranslator(Translator):
    name = "ccx"

    def to_qiskit(self, qc: Any, op: Any, cregs: Dict[str, int]) -> None:
        qc.ccx(op.qubits[0], op.qubits[1], op.qubits[2])

    def to_cirq(
        self, cirq: Any, op: Any, qubits: List[Any], cregs: Dict[str, str]
    ) -> List[Any]:
        return [cirq.CCNOT(qubits[op.qubits[0]], qubits[op.qubits[1]], qubits[op.qubits[2]])]

    def to_pennylane(self, qml: Any, op: Any, cregs: Dict[str, Any]) -> None:
        qml.Toffoli(wires=[op.qubits[0], op.qubits[1], op.qubits[2]])
