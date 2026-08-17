"""Classical-while translator (classical feedback loop).

Only the native backend can execute cwhile natively (per-shot Python loop); the
library backends have no while-loop primitive, so this translator raises a clear
error directing the user to native.
"""

from __future__ import annotations

from typing import Any, Dict, List

from ..._i18n import tr
from .base import Translator


class CwhileTranslator(Translator):
    name = "cwhile"

    def to_qiskit(self, qc: Any, op: Any, cregs: Dict[str, int]) -> None:
        raise NotImplementedError(tr("err.qiskit_cwhile"))

    def to_cirq(
        self, cirq: Any, op: Any, qubits: List[Any], cregs: Dict[str, str]
    ) -> List[Any]:
        raise NotImplementedError(tr("err.cirq_ctrl"))

    def to_pennylane(self, qml: Any, op: Any, cregs: Dict[str, Any]) -> None:
        raise NotImplementedError(tr("err.pennylane_ctrl"))
