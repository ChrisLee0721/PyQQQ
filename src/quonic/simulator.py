"""态矢量模拟器 —— 用 numpy 精确计算期望值，供 VQE / QAOA 使用。

约定：qubit 0 是最低位（bitstring 最右侧），与三个采样后端一致。
"""

import numpy as np

_I = np.array([[1.0, 0.0], [0.0, 1.0]], dtype=complex)
_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
_Y = np.array([[0.0, -1j], [1j, 0.0]], dtype=complex)
_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
_H = np.array([[1.0, 1.0], [1.0, -1.0]], dtype=complex) / np.sqrt(2.0)

_PAULI = {"I": _I, "X": _X, "Y": _Y, "Z": _Z}


def _rotation(axis, theta):
    c = np.cos(theta / 2.0)
    s = np.sin(theta / 2.0)
    if axis == "x":
        return np.array([[c, -1j * s], [-1j * s, c]], dtype=complex)
    if axis == "y":
        return np.array([[c, -s], [s, c]], dtype=complex)
    if axis == "z":
        return np.array([[np.exp(-1j * theta / 2), 0], [0, np.exp(1j * theta / 2)]], dtype=complex)
    raise ValueError(f"未知旋转轴 '{axis}'")


class StatevectorSimulator:
    def __init__(self, num_qubits):
        self.n = num_qubits
        self.state = np.zeros(2 ** num_qubits, dtype=complex)
        self.state[0] = 1.0  # |0...0>

    def _apply_single(self, u, q):
        a = 2 ** q
        k = 2 ** (self.n - q - 1)
        s = self.state.reshape(a, 2, k)
        self.state = np.einsum("ij,ajk->aik", u, s).reshape(-1)

    def _apply_phase(self, qubits):
        # 对「这些 qubit 全为 |1>」的基态叠加 -1 相位（实现多控制 Z）
        idx = np.arange(2 ** self.n)
        mask = np.ones(2 ** self.n, dtype=bool)
        for q in qubits:
            mask &= ((idx >> q) & 1).astype(bool)
        self.state = np.where(mask, -self.state, self.state)

    def apply(self, name, qubits, params=()):
        name = name.lower()
        if name == "h":
            self._apply_single(_H, qubits[0])
        elif name in ("x", "y", "z"):
            self._apply_single(_PAULI[name.upper()], qubits[0])
        elif name in ("rx", "ry", "rz"):
            self._apply_single(_rotation(name[1], params[0]), qubits[0])
        elif name == "cx":
            self._apply_single(_H, qubits[1])
            self._apply_phase((qubits[0], qubits[1]))
            self._apply_single(_H, qubits[1])
        elif name == "cz":
            self._apply_phase((qubits[0], qubits[1]))
        elif name == "ccx":
            self._apply_single(_H, qubits[2])
            self._apply_phase(tuple(qubits))
            self._apply_single(_H, qubits[2])
        elif name == "mcz":
            self._apply_phase(tuple(qubits))
        else:
            raise ValueError(f"态矢量模拟器暂不支持门 '{name}'")

    def expectation(self, pauli_string):
        """计算 <ψ| O |ψ>，其中 O 是 pauli_string 描述的泡利积。

        pauli_string[i] 作用于 qubit i（例如 "ZZ" 表示 Z⊗Z）。
        """
        if len(pauli_string) != self.n:
            raise ValueError(
                f"泡利串长度 {len(pauli_string)} 与量子比特数 {self.n} 不一致"
            )
        other = StatevectorSimulator(self.n)
        other.state = self.state.copy()
        for q, p in enumerate(pauli_string):
            if p != "I":
                other._apply_single(_PAULI[p], q)
        return float(np.real(np.vdot(self.state, other.state)))
