"""Classical-if translator (measure-then-branch).

An int control measures that qubit first and branches on the result; a str control
reads a value already stored by a preceding ``cmeasure`` op. Only the qiskit backend
supports the str control (named classical bit) form today, because cmeasure is not
translated for cirq / pennylane yet.
"""

from __future__ import annotations

from typing import Any, Dict, List

from ..._i18n import tr
from ...ir import CRegCondition
from .base import Translator


class CifTranslator(Translator):
    name = "cif"

    def to_qiskit(self, qc: Any, op: Any, cregs: Dict[str, Any]) -> None:
        from . import TRANSLATORS  # deferred import to avoid a cycle

        if isinstance(op.control, int):
            qc.measure(op.control, op.control)
            clbit = qc.clbits[op.control]
            with qc.if_test((clbit, 1)):
                TRANSLATORS[op.then_op.name].to_qiskit(qc, op.then_op, cregs)
            with qc.if_test((clbit, 0)):
                TRANSLATORS[op.else_op.name].to_qiskit(qc, op.else_op, cregs)
            return

        if isinstance(op.control, CRegCondition):
            cond = op.control
            if cond.width > 1:
                cr = cregs[cond.creg]  # a qiskit ClassicalRegister
                with qc.if_test((cr, cond.value)) as else_:
                    TRANSLATORS[op.then_op.name].to_qiskit(qc, op.then_op, cregs)
                with else_:
                    TRANSLATORS[op.else_op.name].to_qiskit(qc, op.else_op, cregs)
                return
            # width == 1 register with an explicit value: alias to a single clbit
            clbit = qc.clbits[cregs.get(cond.creg, 0)]
            with qc.if_test((clbit, cond.value)):
                TRANSLATORS[op.then_op.name].to_qiskit(qc, op.then_op, cregs)
            with qc.if_test((clbit, 1 - cond.value)):
                TRANSLATORS[op.else_op.name].to_qiskit(qc, op.else_op, cregs)
            return

        # str control (single-bit creg alias): then on == 1, else on == 0
        clbit = qc.clbits[cregs.get(op.control, 0)]
        with qc.if_test((clbit, 1)):
            TRANSLATORS[op.then_op.name].to_qiskit(qc, op.then_op, cregs)
        with qc.if_test((clbit, 0)):
            TRANSLATORS[op.else_op.name].to_qiskit(qc, op.else_op, cregs)

    def to_cirq(
        self, cirq: Any, op: Any, qubits: List[Any], cregs: Dict[str, str]
    ) -> List[Any]:
        from . import TRANSLATORS  # deferred import to avoid a cycle

        if isinstance(op.control, CRegCondition):
            raise NotImplementedError(tr("err.multi_creg_backend", backend="cirq"))
        if not isinstance(op.control, int):
            raise NotImplementedError(tr("err.cirq_ctrl"))

        import sympy

        key = f"m{op.control}"
        ops = [cirq.measure(qubits[op.control], key=key)]
        then_ops = TRANSLATORS[op.then_op.name].to_cirq(cirq, op.then_op, qubits, cregs)
        else_ops = TRANSLATORS[op.else_op.name].to_cirq(cirq, op.else_op, qubits, cregs)
        for t in then_ops:
            ops.append(t.with_classical_controls(key))
        for e in else_ops:
            ops.append(e.with_classical_controls(sympy.Eq(sympy.Symbol(key), 0)))
        return ops

    def to_pennylane(self, qml: Any, op: Any, cregs: Dict[str, Any]) -> None:
        from . import TRANSLATORS  # deferred import to avoid a cycle

        if isinstance(op.control, CRegCondition):
            raise NotImplementedError(tr("err.multi_creg_backend", backend="pennylane"))
        if not isinstance(op.control, int):
            raise NotImplementedError(tr("err.pennylane_ctrl"))

        m = qml.measure(wires=op.control)

        def then_fn() -> None:
            TRANSLATORS[op.then_op.name].to_pennylane(qml, op.then_op, cregs)

        def else_fn() -> None:
            TRANSLATORS[op.else_op.name].to_pennylane(qml, op.else_op, cregs)

        qml.cond(m == 1, then_fn, else_fn)()
