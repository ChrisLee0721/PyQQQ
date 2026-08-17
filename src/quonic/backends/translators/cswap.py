"""Controlled-SWAP (Fredkin) gate translator."""

from __future__ import annotations

from typing import Any, Dict, List

from .base import Translator


class CswapTranslator(Translator):
    name = "cswap"

    def to_qiskit(self, qc: Any, op: Any, cregs: Dict[str, int]) -> None:
        qc.cswap(op.qubits[0], op.qubits[1], op.qubits[2])

    def to_cirq(
        self, cirq: Any, op: Any, qubits: List[Any], cregs: Dict[str, str]
    ) -> List[Any]:
        return [
            cirq.CSWAP(
                qubits[op.qubits[0]], qubits[op.qubits[1]], qubits[op.qubits[2]]
            )
        ]

    def to_pennylane(self, qml: Any, op: Any, cregs: Dict[str, Any]) -> None:
        qml.CSWAP(wires=[op.qubits[0], op.qubits[1], op.qubits[2]])
