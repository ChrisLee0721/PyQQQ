"""Cirq 后端适配器。"""

import math

from ..noise import resolve_noise
from ..result import Result
from .base import Backend


class CirqBackend(Backend):
    name = "cirq"
    methods = frozenset({"statevector"})

    def run(self, circuit, shots=1024, noise=None, method="statevector"):
        try:
            import cirq
        except ImportError as e:
            raise ImportError(
                "使用 cirq 后端需要安装 cirq：\n"
                "    pip install 'quonic[cirq]'\n"
                "或： pip install cirq"
            ) from e

        nm = resolve_noise(noise)
        n = circuit.num_qubits
        qubits = [cirq.LineQubit(i) for i in range(n)]
        ops = []
        for op in circuit.ops:
            ops.extend(self._to_ops(cirq, op, qubits))
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

    @staticmethod
    def _to_ops(cirq, op, qubits):
        name, q = op.name, op.qubits
        if name == "i":
            return [cirq.I(qubits[q[0]])]
        if name == "h":
            return [cirq.H(qubits[q[0]])]
        if name == "x":
            return [cirq.X(qubits[q[0]])]
        if name == "y":
            return [cirq.Y(qubits[q[0]])]
        if name == "z":
            return [cirq.Z(qubits[q[0]])]
        if name == "cx":
            return [cirq.CNOT(qubits[q[0]], qubits[q[1]])]
        if name == "cz":
            return [cirq.CZ(qubits[q[0]], qubits[q[1]])]
        if name == "ccx":
            return [cirq.CCNOT(qubits[q[0]], qubits[q[1]], qubits[q[2]])]
        if name == "swap":
            return [cirq.SWAP(qubits[q[0]], qubits[q[1]])]
        if name == "mcz":
            return [
                cirq.ControlledGate(cirq.Z, num_controls=len(q) - 1).on(
                    *(qubits[i] for i in q)
                )
            ]
        if name == "rx":
            return [cirq.rx(op.params[0])(qubits[q[0]])]
        if name == "ry":
            return [cirq.ry(op.params[0])(qubits[q[0]])]
        if name == "rz":
            return [cirq.rz(op.params[0])(qubits[q[0]])]
        if name == "cp":
            return [
                cirq.CZPowGate(exponent=op.params[0] / math.pi).on(
                    qubits[q[0]], qubits[q[1]]
                )
            ]
        if name == "p":
            return [cirq.ZPowGate(exponent=op.params[0] / math.pi).on(qubits[q[0]])]
        if name == "measure":
            return [cirq.measure(qubits[q[0]], key=f"m{q[0]}")]
        if name in ("cif", "cmeasure", "cwhile"):
            raise NotImplementedError(
                "cirq 后端暂不支持经典控制流（cif/cmeasure/cwhile）；"
                "请改用 qiskit 或 native 后端"
            )
        raise ValueError(f"Cirq 后端暂不支持门 '{name}'")
