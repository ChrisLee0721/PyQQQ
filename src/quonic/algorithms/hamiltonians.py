"""哈密顿量辅助：从外部量子化学库导入泡利哈密顿量。

QuoNic 不内置化学数据库；分子的电子结构哈密顿量需要用户用
Qiskit Nature / OpenFermion 等工具自行生成，再用本模块的适配器
转成 vqe() 所需的 [(系数, 泡利串), ...] 格式。
"""


def from_qiskit_nature(op):
    """把 Qiskit Nature（或 Qiskit）的 SparsePauliOp 转成 [(coeff, pauli), ...]。

    op 需具备 .coeffs 和 .paulis 属性（qiskit.quantum_info.SparsePauliOp 满足）。

    例（示意）：
        from qiskit_nature.second_q.drivers import PySCFDriver
        from qiskit_nature.second_q.mappers import JordanWignerMapper
        # ... 用 PySCFDriver 得到 ElectronicStructureProblem，做 JW 映射 ...
        qubit_op = problem.hamiltonian.second_q_op()  # 经 mapper 映射后是 SparsePauliOp
        terms = from_qiskit_nature(qubit_op)
        vqe(terms, n_qubits)

    说明：
        - 泡利串序已对齐 QuoNic 约定（左起第一个字符 = qubit 0），与 Qiskit 一致，无需反转。
        - 分子哈密顿量在 JW 映射下系数为实数；若出现不可忽略的虚部会报错。
    """
    terms = []
    for coeff, pauli in zip(op.coeffs, op.paulis):
        if abs(coeff.imag) > 1e-8:
            raise ValueError(
                f"哈密顿量系数 {coeff} 含不可忽略的虚部，当前 VQE 仅支持实系数"
            )
        label = pauli.to_label() if hasattr(pauli, "to_label") else str(pauli)
        terms.append((float(coeff.real), label))
    return terms
