"""Qiskit 后端适配器。"""

import math

from ..noise import resolve_noise
from ..result import Result
from .base import Backend


class QiskitBackend(Backend):
    name = "qiskit"
    methods = frozenset(
        {"statevector", "stabilizer", "matrix_product_state", "density_matrix"}
    )

    def run(self, circuit, shots=1024, noise=None, method="statevector"):
        try:
            from qiskit import QuantumCircuit
            from qiskit_aer import AerSimulator
        except ImportError as e:
            raise ImportError(
                "使用 qiskit 后端需要安装 qiskit 和 qiskit-aer：\n"
                "    pip install 'quonic[qiskit]'\n"
                "或： pip install qiskit qiskit-aer"
            ) from e

        nm = resolve_noise(noise)
        qc = QuantumCircuit(circuit.num_qubits, circuit.num_qubits)
        # 具名经典位是某个量子比特测量结果的别名：映射到该比特自己的经典位，
        # 因此 get_counts 输出与 native 后端一致的扁平比特串（无具名寄存器）。
        creg_map = {}

        for op in circuit.ops:
            if op.name == "cif":
                # 经典控制流：control 为 qubit 时先测量；为 creg 时直接读经典位
                if isinstance(op.control, int):
                    qc.measure(op.control, op.control)
                    clbit = qc.clbits[op.control]
                else:
                    clbit = qc.clbits[creg_map.get(op.control, 0)]
                with qc.if_test((clbit, 1)):
                    self._apply(qc, op.then_op)
                with qc.if_test((clbit, 0)):
                    self._apply(qc, op.else_op)
            elif op.name == "cmeasure":
                qc.measure(op.qubit, op.qubit)
                creg_map[op.creg] = op.qubit
            elif op.name == "cwhile":
                raise NotImplementedError(
                    "qiskit 后端暂不支持 cwhile（经典反馈循环）；请用 native 后端"
                )
            else:
                self._apply(qc, op)

        # 自动补全：任何没有显式 measure 的量子比特，在最后统一测量
        for q in circuit.unmeasured_qubits():
            qc.measure(q, q)

        # 噪声模拟需要密度矩阵方法；stabilizer / MPS 不支持通用噪声模型
        if nm.enabled:
            method = "density_matrix"

        simulator = AerSimulator(method=method)
        run_kwargs = {}
        if nm.enabled:
            from qiskit_aer.noise import NoiseModel as QiskitNoiseModel
            from qiskit_aer.noise import depolarizing_error

            qnm = QiskitNoiseModel()
            single_gates = ["h", "x", "y", "z", "rx", "ry", "rz"]
            double_gates = ["cx", "cz", "swap"]
            if nm.single > 0.0:
                qnm.add_all_qubit_quantum_error(
                    depolarizing_error(nm.single, 1), single_gates
                )
            if nm.double > 0.0:
                qnm.add_all_qubit_quantum_error(
                    depolarizing_error(nm.double, 2), double_gates
                )
            run_kwargs["noise_model"] = qnm

        result = simulator.run(qc, shots=shots, **run_kwargs).result()
        counts = result.get_counts()
        return Result.from_counts(counts, shots)

    @staticmethod
    def _apply(qc, op):
        name, qubits = op.name, op.qubits
        if name == "i":
            qc.id(qubits[0])
        elif name == "h":
            qc.h(qubits[0])
        elif name == "x":
            qc.x(qubits[0])
        elif name == "y":
            qc.y(qubits[0])
        elif name == "z":
            qc.z(qubits[0])
        elif name == "cx":
            qc.cx(qubits[0], qubits[1])
        elif name == "cz":
            qc.cz(qubits[0], qubits[1])
        elif name == "ccx":
            qc.ccx(qubits[0], qubits[1], qubits[2])
        elif name == "swap":
            qc.swap(qubits[0], qubits[1])
        elif name == "mcz":
            qc.mcp(math.pi, list(qubits[:-1]), qubits[-1])
        elif name == "rx":
            qc.rx(op.params[0], qubits[0])
        elif name == "ry":
            qc.ry(op.params[0], qubits[0])
        elif name == "rz":
            qc.rz(op.params[0], qubits[0])
        elif name == "cp":
            qc.cp(op.params[0], qubits[0], qubits[1])
        elif name == "p":
            qc.p(op.params[0], qubits[0])
        elif name == "measure":
            qc.measure(qubits[0], qubits[0])
        else:
            raise ValueError(f"Qiskit 后端暂不支持门 '{name}'")
