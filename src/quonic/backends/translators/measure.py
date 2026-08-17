"""Measurement gate translator."""

from __future__ import annotations

from typing import Any, Dict, List

from .base import Translator


class MeasureTranslator(Translator):
    name = "measure"

    def to_qiskit(self, qc: Any, op: Any, cregs: Dict[str, int]) -> None:
        qc.measure(op.qubits[0], op.qubits[0])

    def to_cirq(
        self, cirq: Any, op: Any, qubits: List[Any], cregs: Dict[str, str]
    ) -> List[Any]:
        return [cirq.measure(qubits[op.qubits[0]], key=f"m{op.qubits[0]}")]

    def to_pennylane(self, qml: Any, op: Any, cregs: Dict[str, Any]) -> None:
        # qml.counts() measures all wires, so an explicit measure needs no extra op
        return
