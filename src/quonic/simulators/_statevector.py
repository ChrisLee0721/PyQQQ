"""态矢量引擎：2^n 复振幅向量，精确模拟（含非 Clifford 门）。

约定：qubit 0 是最低位（bitstring 最右侧）。多比特门用「对角相位 + H」
技巧实现，规避两比特矩阵的指标顺序歧义。
"""

import numpy as np

from ._gates import _H, single


class StatevectorEngine:
    def __init__(self, num_qubits):
        self.n = num_qubits
        self.state = np.zeros(2 ** num_qubits, dtype=complex)
        self.state[0] = 1.0  # |0...0>

    def _apply_single(self, u, q):
        hi = 2 ** (self.n - q - 1)
        lo = 2 ** q
        s = self.state.reshape(hi, 2, lo)
        self.state = np.einsum("ij,ajk->aik", u, s).reshape(-1)

    def _apply_phase(self, qubits, angle):
        """对「这些 qubit 全为 |1>」的基态叠加 e^{i·angle} 相位（对角门）。"""
        idx = np.arange(2 ** self.n)
        mask = np.ones(2 ** self.n, dtype=bool)
        for q in qubits:
            mask &= ((idx >> q) & 1).astype(bool)
        self.state[mask] *= np.exp(1j * angle)

    def _swap(self, a, b):
        if a == b:
            return
        idx = np.arange(2 ** self.n)
        ia = (idx >> a) & 1
        ib = (idx >> b) & 1
        mask = ~((1 << a) | (1 << b))
        perm = (idx & mask) | (ia << b) | (ib << a)
        self.state = self.state[perm]

    def apply(self, name, qubits, params=()):
        name = name.lower()
        if name == "measure":
            return
        if name in ("i", "h", "x", "y", "z", "rx", "ry", "rz", "p"):
            self._apply_single(single(name, params), qubits[0])
        elif name == "cx":
            self._apply_single(_H, qubits[1])
            self._apply_phase(qubits, np.pi)
            self._apply_single(_H, qubits[1])
        elif name == "cz":
            self._apply_phase(qubits, np.pi)
        elif name == "cp":
            self._apply_phase(qubits, params[0])
        elif name == "ccx":
            self._apply_single(_H, qubits[2])
            self._apply_phase(qubits, np.pi)
            self._apply_single(_H, qubits[2])
        elif name == "swap":
            self._swap(qubits[0], qubits[1])
        elif name == "mcz":
            self._apply_phase(qubits, np.pi)
        else:
            raise ValueError(f"态矢量引擎暂不支持门 '{name}'")

    def sample(self, shots):
        probs = np.abs(self.state) ** 2
        probs = probs / probs.sum()
        idx = np.random.choice(2 ** self.n, size=shots, p=probs)
        counts = {}
        fmt = f"0{self.n}b"
        for i in idx:
            bs = format(int(i), fmt)
            counts[bs] = counts.get(bs, 0) + 1
        return counts

    def measure_qubit(self, q):
        """中途测量 qubit q：按振幅概率坍缩，返回测量结果 0/1。"""
        idx = np.arange(2 ** self.n)
        bit = (idx >> q) & 1
        p0 = float(np.sum(np.abs(self.state[bit == 0]) ** 2))
        outcome = 0 if np.random.random() < p0 else 1
        self.state[bit != outcome] = 0.0
        norm = np.linalg.norm(self.state)
        if norm > 0.0:
            self.state /= norm
        return outcome
