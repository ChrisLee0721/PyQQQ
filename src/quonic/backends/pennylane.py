"""PennyLane 后端适配器。"""

from ..noise import resolve_noise
from ..result import Result
from .base import Backend


def _two_qubit_depolarizing_kraus(p):
    """双比特去极化信道的 16 个 Kraus 算子（与 Qiskit 的 depolarizing_error(p, 2) 一致）。"""
    import numpy as np

    I2 = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.array([[1, 0], [0, -1]], dtype=complex)
    paulis = (I2, X, Y, Z)
    kraus = [np.sqrt(1 - 15 * p / 16) * np.kron(I2, I2)]
    s = np.sqrt(p / 16)
    for a in paulis:
        for b in paulis:
            if a is I2 and b is I2:
                continue
            kraus.append(s * np.kron(a, b))
    return kraus


class PennyLaneBackend(Backend):
    name = "pennylane"
    methods = frozenset({"statevector"})

    def run(self, circuit, shots=1024, noise=None, method="statevector"):
        try:
            import pennylane as qml
        except ImportError as e:
            raise ImportError(
                "使用 pennylane 后端需要安装 pennylane：\n"
                "    pip install 'quonic[pennylane]'\n"
                "或： pip install pennylane"
            ) from e

        nm = resolve_noise(noise)
        n = circuit.num_qubits
        device_name = "default.mixed" if nm.enabled else "default.qubit"
        dev = qml.device(device_name, wires=n)

        two_qubit_kraus = None
        if nm.enabled and nm.double > 0.0:
            two_qubit_kraus = _two_qubit_depolarizing_kraus(nm.double)

        @qml.qnode(dev)
        def qnode():
            for op in circuit.ops:
                self._apply(qml, op)
                if nm.enabled and op.name != "measure":
                    if len(op.qubits) == 1 and nm.single > 0.0:
                        qml.DepolarizingChannel(nm.single, wires=op.qubits[0])
                    elif len(op.qubits) == 2 and two_qubit_kraus is not None:
                        qml.QubitChannel(two_qubit_kraus, wires=list(op.qubits))
            return qml.counts()

        qnode = qml.set_shots(qnode, shots=shots)

        raw = qnode()
        # PennyLane 的比特串是 wire0 在最高位，反转为 Qiskit 约定（qubit0 在最低位）
        counts = {}
        for bitstring, count in raw.items():
            key = str(bitstring)[::-1]
            counts[key] = counts.get(key, 0) + count
        return Result.from_counts(counts, shots)

    @staticmethod
    def _apply(qml, op):
        name, qubits = op.name, op.qubits
        if name == "i":
            qml.Identity(wires=qubits[0])
        elif name == "h":
            qml.Hadamard(wires=qubits[0])
        elif name == "x":
            qml.PauliX(wires=qubits[0])
        elif name == "y":
            qml.PauliY(wires=qubits[0])
        elif name == "z":
            qml.PauliZ(wires=qubits[0])
        elif name == "cx":
            qml.CNOT(wires=[qubits[0], qubits[1]])
        elif name == "cz":
            qml.CZ(wires=[qubits[0], qubits[1]])
        elif name == "ccx":
            qml.Toffoli(wires=[qubits[0], qubits[1], qubits[2]])
        elif name == "swap":
            qml.SWAP(wires=[qubits[0], qubits[1]])
        elif name == "mcz":
            target = qubits[-1]
            qml.Hadamard(wires=target)
            qml.MultiControlledX(wires=list(qubits))
            qml.Hadamard(wires=target)
        elif name == "rx":
            qml.RX(op.params[0], wires=qubits[0])
        elif name == "ry":
            qml.RY(op.params[0], wires=qubits[0])
        elif name == "rz":
            qml.RZ(op.params[0], wires=qubits[0])
        elif name == "cp":
            qml.ControlledPhaseShift(op.params[0], wires=[qubits[0], qubits[1]])
        elif name == "p":
            qml.PhaseShift(op.params[0], wires=qubits[0])
        elif name == "measure":
            return  # qml.counts() 会测量所有 wire，显式 measure 无需额外操作
        elif name in ("cif", "cmeasure", "cwhile"):
            raise NotImplementedError(
                "pennylane 后端暂不支持经典控制流（cif/cmeasure/cwhile）；"
                "请改用 qiskit 或 native 后端"
            )
        else:
            raise ValueError(f"PennyLane 后端暂不支持门 '{name}'")
