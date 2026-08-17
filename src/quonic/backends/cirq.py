"""Cirq backend adapter."""

from __future__ import annotations

from typing import Optional, Union

from .._i18n import tr
from ..ir import Circuit
from ..noise import NoiseModel, resolve_noise
from ..result import Result
from .base import Backend
from .translators import TRANSLATORS


class CirqBackend(Backend):
    name = "cirq"
    methods = frozenset({"statevector"})

    def run(
        self,
        circuit: Circuit,
        shots: int = 1024,
        noise: Optional[Union[NoiseModel, float, int]] = None,
        method: str = "statevector",
    ) -> Result:
        try:
            import cirq
        except ImportError as e:
            raise ImportError(tr("err.cirq_missing")) from e

        nm = resolve_noise(noise)
        n = circuit.num_qubits
        qubits = [cirq.LineQubit(i) for i in range(n)]
        ops = []
        cregs = {}
        for op in circuit.ops:
            ops.extend(TRANSLATORS[op.name].to_cirq(cirq, op, qubits, cregs))
            if nm.enabled and op.name != "measure":
                nq = len(op.qubits)
                if nq == 1 and nm.single > 0.0:
                    ops.append(cirq.depolarize(nm.single).on(qubits[op.qubits[0]]))
                elif nq == 2 and nm.double > 0.0:
                    ops.append(
                        cirq.depolarize(nm.double, n_qubits=2).on(
                            *[qubits[i] for i in op.qubits]
                        )
                    )

        for q in circuit.unmeasured_qubits():
            ops.append(cirq.measure(qubits[q], key=f"m{q}"))

        simulator = cirq.Simulator()
        result = simulator.run(cirq.Circuit(ops), repetitions=shots)

        counts = {}
        for r in range(shots):
            bits = [result.measurements[f"m{q}"][r][0] for q in range(n)]
            bitstring = "".join(str(int(b)) for b in reversed(bits))
            counts[bitstring] = counts.get(bitstring, 0) + 1
        return Result.from_counts(counts, shots)
