"""Translator protocol: each gate or classical-control operation declares its
translation for the three library backends (qiskit / cirq / pennylane).

The in-house native backend is not a translator target: it is data-driven
(``engine.apply(name, ...)``) and executes classical control shot-by-shot.
"""

from __future__ import annotations

from typing import Any, Dict, List


class Translator:
    name: str = ""

    def to_qiskit(self, qc: Any, op: Any, cregs: Dict[str, int]) -> None:
        """Emit this operation onto a Qiskit QuantumCircuit in place.

        ``cregs`` maps a named classical bit to its qubit index (maintained by
        the qiskit backend across ops).
        """
        raise NotImplementedError

    def to_cirq(
        self, cirq: Any, op: Any, qubits: List[Any], cregs: Dict[str, str]
    ) -> List[Any]:
        """Return the list of Cirq operations for this operation.

        ``cregs`` maps a named classical bit to its measurement key.
        """
        raise NotImplementedError

    def to_pennylane(self, qml: Any, op: Any, cregs: Dict[str, Any]) -> None:
        """Emit this operation inside a PennyLane qnode in place.

        ``cregs`` maps a named classical bit to its measured value.
        """
        raise NotImplementedError
