"""Qiskit 后端适配器。"""

from .base import Backend


class QiskitBackend(Backend):
    name = "qiskit"

    def run(self, circuit, shots=1024):
        try:
            from qiskit import QuantumCircuit
            from qiskit_aer import AerSimulator
        except ImportError as e:
            raise ImportError(
                "使用 qiskit 后端需要安装 qiskit 和 qiskit-aer：\n"
                "    pip install 'pyqqq[qiskit]'\n"
                "或： pip install qiskit qiskit-aer"
            ) from e

        qc = QuantumCircuit(circuit.num_qubits, circuit.num_qubits)
        for op in circuit.ops:
            self._apply(qc, op)

        # 自动补全：任何没有显式 measure 的量子比特，在最后统一测量
        for q in circuit.unmeasured_qubits():
            qc.measure(q, q)

        simulator = AerSimulator()
        result = simulator.run(qc, shots=shots).result()
        counts = result.get_counts()
        return {"counts": counts, "shots": shots}

    @staticmethod
    def _apply(qc, op):
        name, qubits = op.name, op.qubits
        if name == "h":
            qc.h(qubits[0])
        elif name == "x":
            qc.x(qubits[0])
        elif name == "y":
            qc.y(qubits[0])
        elif name == "z":
            qc.z(qubits[0])
        elif name == "cx":
            qc.cx(qubits[0], qubits[1])
        elif name == "measure":
            qc.measure(qubits[0], qubits[0])
        else:
            raise ValueError(f"Qiskit 后端暂不支持门 '{name}'")
