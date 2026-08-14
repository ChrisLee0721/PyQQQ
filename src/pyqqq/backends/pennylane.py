"""PennyLane 后端适配器。"""

from .base import Backend


class PennyLaneBackend(Backend):
    name = "pennylane"

    def run(self, circuit, shots=1024):
        try:
            import pennylane as qml
        except ImportError as e:
            raise ImportError(
                "使用 pennylane 后端需要安装 pennylane：\n"
                "    pip install 'pyqqq[pennylane]'\n"
                "或： pip install pennylane"
            ) from e

        n = circuit.num_qubits
        dev = qml.device("default.qubit", wires=n)

        @qml.set_shots(shots=shots)
        @qml.qnode(dev)
        def qnode():
            for op in circuit.ops:
                self._apply(qml, op)
            return qml.counts()

        raw = qnode()
        # PennyLane 的比特串是 wire0 在最高位，反转为 Qiskit 约定（qubit0 在最低位）
        counts = {}
        for bitstring, count in raw.items():
            key = str(bitstring)[::-1]
            counts[key] = counts.get(key, 0) + count
        return {"counts": counts, "shots": shots}

    @staticmethod
    def _apply(qml, op):
        name, qubits = op.name, op.qubits
        if name == "h":
            qml.Hadamard(wires=qubits[0])
        elif name == "x":
            qml.PauliX(wires=qubits[0])
        elif name == "y":
            qml.PauliY(wires=qubits[0])
        elif name == "z":
            qml.PauliZ(wires=qubits[0])
        elif name == "cx":
            qml.CNOT(wires=[qubits[0], qubits[1]])
        elif name == "measure":
            return  # qml.counts() 会测量所有 wire，显式 measure 无需额外操作
        else:
            raise ValueError(f"PennyLane 后端暂不支持门 '{name}'")
