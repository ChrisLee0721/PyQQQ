"""Cirq 后端适配器。"""

from .base import Backend


class CirqBackend(Backend):
    name = "cirq"

    def run(self, circuit, shots=1024):
        try:
            import cirq
        except ImportError as e:
            raise ImportError(
                "使用 cirq 后端需要安装 cirq：\n"
                "    pip install 'pyqqq[cirq]'\n"
                "或： pip install cirq"
            ) from e

        n = circuit.num_qubits
        qubits = [cirq.LineQubit(i) for i in range(n)]
        ops = []
        for op in circuit.ops:
            ops.extend(self._to_ops(cirq, op, qubits))

        for q in circuit.unmeasured_qubits():
            ops.append(cirq.measure(qubits[q], key=f"m{q}"))

        simulator = cirq.Simulator()
        result = simulator.run(cirq.Circuit(ops), repetitions=shots)

        counts = {}
        for r in range(shots):
            bits = [result.measurements[f"m{q}"][r][0] for q in range(n)]
            bitstring = "".join(str(int(b)) for b in reversed(bits))
            counts[bitstring] = counts.get(bitstring, 0) + 1
        return {"counts": counts, "shots": shots}

    @staticmethod
    def _to_ops(cirq, op, qubits):
        name, q = op.name, op.qubits
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
        if name == "measure":
            return [cirq.measure(qubits[q[0]], key=f"m{q[0]}")]
        raise ValueError(f"Cirq 后端暂不支持门 '{name}'")
