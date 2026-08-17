"""Classical measurement translator (measure a qubit into a named creg).

Single-bit cregs (bit 0) are supported on all three backends. Multi-bit cregs
(bit > 0) are only supported on qiskit (which builds a real ClassicalRegister);
cirq / pennylane raise a clear error for the multi-bit case.
"""

from __future__ import annotations

from typing import Any, Dict, List

from ..._i18n import tr
from .base import Translator


class CMeasureTranslator(Translator):
    name = "cmeasure"

    def to_qiskit(self, qc: Any, op: Any, cregs: Dict[str, Any]) -> None:
        cr = cregs.get(op.creg)
        if cr is not None and not isinstance(cr, int):
            # multi-bit register: measure into the named ClassicalRegister bit
            qc.measure(op.qubit, cr[op.bit])
        else:
            # single-bit alias: measure into the qubit's own flat classical bit
            qc.measure(op.qubit, op.qubit)
            cregs[op.creg] = op.qubit

    def to_cirq(
        self, cirq: Any, op: Any, qubits: List[Any], cregs: Dict[str, str]
    ) -> List[Any]:
        if op.bit > 0:
            raise NotImplementedError(tr("err.multi_creg_backend", backend="cirq"))
        key = f"m{op.qubit}"
        cregs[op.creg] = key
        return [cirq.measure(qubits[op.qubit], key=key)]

    def to_pennylane(self, qml: Any, op: Any, cregs: Dict[str, Any]) -> None:
        if op.bit > 0:
            raise NotImplementedError(tr("err.multi_creg_backend", backend="pennylane"))
        cregs[op.creg] = qml.measure(wires=op.qubit)
