"""Hadamard gate translator."""

from __future__ import annotations

from typing import Any, Dict, List

from .base import Translator


class HadamardTranslator(Translator):
    name = "h"

    def to_qiskit(self, qc: Any, op: Any, cregs: Dict[str, int]) -> None:
        qc.h(op.qubits[0])

    def to_cirq(
        self, cirq: Any, op: Any, qubits: List[Any], cregs: Dict[str, str]
    ) -> List[Any]:
        return [cirq.H(qubits[op.qubits[0]])]

    def to_pennylane(self, qml: Any, op: Any, cregs: Dict[str, Any]) -> None:
        qml.Hadamard(wires=op.qubits[0])
