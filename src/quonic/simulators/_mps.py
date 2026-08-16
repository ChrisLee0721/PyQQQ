"""矩阵乘积态（MPS）引擎：低纠缠电路突破 2^n 内存墙。

朴素版：单比特门本地更新，多比特门用「对角相位 + H」技巧 + SVD 截断，
不相邻 qubit 用 SWAP 链搬移。bond 维上限 chi_max 硬截断。

约定：qubit 0 是最低位；site 从左到右依次为 qubit 0..n-1。
"""

import numpy as np

from ._gates import _H, single


class MPSEngine:
    def __init__(self, num_qubits, chi_max=32):
        self.n = num_qubits
        self.chi_max = chi_max
        # M[i] 形状 [χ_{i-1}, 2, χ_i]，初始 |0...0>（所有 bond 维为 1）
        self.M = [np.zeros((1, 2, 1), dtype=complex) for _ in range(num_qubits)]
        for t in self.M:
            t[0, 0, 0] = 1.0

    # ------------------------------------------------------------------
    # 基本张量操作
    # ------------------------------------------------------------------
    def _apply_single(self, q, u):
        self.M[q] = np.einsum("asb,ts->atb", self.M[q], u)

    def _merge(self, qubits):
        theta = self.M[qubits[0]]
        for j in range(1, len(qubits)):
            theta = np.einsum("...a,abc->...bc", theta, self.M[qubits[j]])
        return theta

    def _restore_pair(self, theta, i):
        """把 [χL, 2, 2, χR] 恢复成 site i, i+1（一次 SVD）。"""
        chi_l = theta.shape[0]
        chi_r = theta.shape[-1]
        mat = theta.reshape(chi_l * 2, 2 * chi_r)
        a, s, b = np.linalg.svd(mat, full_matrices=False)
        chi = min(len(s), self.chi_max)
        a = a[:, :chi]
        s = s[:chi]
        b = b[:chi, :]
        self.M[i] = a.reshape(chi_l, 2, chi)
        self.M[i + 1] = (s[:, None] * b).reshape(chi, 2, chi_r)

    def _restore(self, theta, qubits):
        """把 [χL, 2, ..., 2, χR] 恢复成连续 k 个 site（逐步左 SVD）。"""
        k = len(qubits)
        chi_l = theta.shape[0]
        chi_r = theta.shape[-1]
        cur = theta
        for idx in range(k - 1):
            num_phys = k - idx
            mat = cur.reshape(chi_l * 2, 2 ** (num_phys - 1) * chi_r)
            a, s, b = np.linalg.svd(mat, full_matrices=False)
            chi = min(len(s), self.chi_max)
            a = a[:, :chi]
            s = s[:chi]
            b = b[:chi, :]
            self.M[qubits[idx]] = a.reshape(chi_l, 2, chi)
            cur = (s[:, None] * b).reshape(chi, *([2] * (num_phys - 1)), chi_r)
            chi_l = chi
        self.M[qubits[k - 1]] = cur.reshape(chi_l, 2, chi_r)

    def _swap_adjacent(self, i):
        theta = np.einsum("asr,rtb->astb", self.M[i], self.M[i + 1])
        theta = np.einsum("astb->atsb", theta)
        self._restore_pair(theta, i)

    # ------------------------------------------------------------------
    # 对角门（cz / cp / mcz）：合并 -> 对角缩放 -> SVD 恢复
    # ------------------------------------------------------------------
    def _apply_diag_contiguous(self, qubits, angle):
        theta = self._merge(qubits)
        k = len(qubits)
        index = (slice(None),) + (1,) * k + (slice(None),)
        theta[index] *= np.exp(1j * angle)
        if k == 2:
            self._restore_pair(theta, qubits[0])
        else:
            self._restore(theta, qubits)

    def _apply_diag(self, qubits, angle):
        q = sorted(qubits)
        swaps = []
        for j in range(1, len(q)):
            target = q[0] + j
            while q[j] > target:
                self._swap_adjacent(q[j] - 1)
                swaps.append(q[j] - 1)
                q[j] -= 1
        self._apply_diag_contiguous(q, angle)
        for i in reversed(swaps):
            self._swap_adjacent(i)

    # ------------------------------------------------------------------
    # 门分派
    # ------------------------------------------------------------------
    def apply(self, name, qubits, params=()):
        name = name.lower()
        if name == "measure":
            return
        if name in ("i", "h", "x", "y", "z", "rx", "ry", "rz", "p"):
            self._apply_single(qubits[0], single(name, params))
        elif name == "cx":
            self._apply_single(qubits[1], _H)
            self._apply_diag(qubits, np.pi)
            self._apply_single(qubits[1], _H)
        elif name == "cz":
            self._apply_diag(qubits, np.pi)
        elif name == "cp":
            self._apply_diag(qubits, params[0])
        elif name == "ccx":
            self._apply_single(qubits[2], _H)
            self._apply_diag(qubits, np.pi)
            self._apply_single(qubits[2], _H)
        elif name == "mcz":
            self._apply_diag(qubits, np.pi)
        elif name == "swap":
            a, b = qubits[0], qubits[1]
            if abs(a - b) != 1:
                raise NotImplementedError("MPS 引擎仅支持相邻量子比特的 swap 门")
            self._swap_adjacent(min(a, b))
        else:
            raise ValueError(f"MPS 引擎暂不支持门 '{name}'")

    # ------------------------------------------------------------------
    # 采样：右环境 + 逐 bit 条件概率
    # ------------------------------------------------------------------
    def _right_env(self):
        r = [None] * (self.n + 1)
        r[self.n] = np.array([[1.0 + 0j]])
        for i in range(self.n - 1, -1, -1):
            r[i] = np.einsum("asc,cd,bsd->ab", self.M[i], r[i + 1], self.M[i].conj())
        return r

    def _sample_once(self, r):
        left = np.array([[1.0 + 0j]])
        bits = []
        for i in range(self.n):
            probs = []
            for s in (0, 1):
                m = self.M[i][:, s, :]
                p = np.einsum("ab,ac,cd,bd->", left, m, r[i + 1], m.conj())
                probs.append(float(np.real(p)))
            probs = np.clip(probs, 0.0, None)
            total = probs.sum()
            probs = probs / total if total > 0 else [0.5, 0.5]
            s = int(np.random.choice([0, 1], p=probs))
            bits.append(s)
            m = self.M[i][:, s, :]
            left = np.einsum("ab,ac,bd->cd", left, m, m.conj())
        return bits

    def sample(self, shots):
        r = self._right_env()
        counts = {}
        for _ in range(shots):
            bits = self._sample_once(r)
            bs = "".join(str(b) for b in reversed(bits))
            counts[bs] = counts.get(bs, 0) + 1
        return counts
