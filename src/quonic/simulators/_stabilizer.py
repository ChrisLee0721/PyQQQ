"""稳定子引擎：Aaronson–Gottesman 的 Clifford tableau（多项式级）。

仅支持基础 Clifford 门集 {h, x, y, z, cx, cz}；遇到非 Clifford 门（任意角
旋转 / ccx / cp 等）或 mcz 会抛错，由调度器降级到其它 method。

约定：qubit 0 是最低位。tableau 为 2n 行（前 n 行 destabilizer，后 n 行
stabilizer），列 = x[0..n-1] | z[0..n-1] | phase（mod 4：0=+1,1=i,2=-1,3=-i）。
"""

import numpy as np


class StabilizerEngine:
    def __init__(self, num_qubits):
        self.n = num_qubits
        # 行 0..n-1 是 destabilizer（X_i），行 n..2n-1 是 stabilizer（Z_i）
        self.x = np.zeros((2 * num_qubits, num_qubits), dtype=bool)
        self.z = np.zeros((2 * num_qubits, num_qubits), dtype=bool)
        self.phase = np.zeros(2 * num_qubits, dtype=int)
        for i in range(num_qubits):
            self.x[i, i] = True
            self.z[num_qubits + i, i] = True

    # ------------------------------------------------------------------
    # 门操作（作用于所有 2n 行）
    # ------------------------------------------------------------------
    def _h(self, q):
        mask = self.x[:, q] & self.z[:, q]
        self.x[:, q], self.z[:, q] = self.z[:, q].copy(), self.x[:, q].copy()
        self.phase = (self.phase + 2 * mask.astype(int)) % 4

    def _s(self, q):
        mask = self.x[:, q] & self.z[:, q]
        self.z[:, q] ^= self.x[:, q]
        self.phase = (self.phase + 2 * mask.astype(int)) % 4

    def _x(self, q):
        self.phase = (self.phase + 2 * self.z[:, q].astype(int)) % 4

    def _y(self, q):
        self.phase = (self.phase + 2 * (self.x[:, q] ^ self.z[:, q]).astype(int)) % 4

    def _z(self, q):
        self.phase = (self.phase + 2 * self.x[:, q].astype(int)) % 4

    def _cx(self, a, b):
        r = self.x[:, a] & self.z[:, b] & (self.x[:, b] ^ self.z[:, a] ^ True)
        self.phase = (self.phase + 2 * r.astype(int)) % 4
        self.x[:, b] ^= self.x[:, a]
        self.z[:, a] ^= self.z[:, b]

    def apply(self, name, qubits, params=()):
        name = name.lower()
        if name == "measure":
            return
        if name == "h":
            self._h(qubits[0])
        elif name == "x":
            self._x(qubits[0])
        elif name == "y":
            self._y(qubits[0])
        elif name == "z":
            self._z(qubits[0])
        elif name == "cx":
            self._cx(qubits[0], qubits[1])
        elif name == "cz":
            self._h(qubits[1])
            self._cx(qubits[0], qubits[1])
            self._h(qubits[1])
        elif name == "swap":
            self._cx(qubits[0], qubits[1])
            self._cx(qubits[1], qubits[0])
            self._cx(qubits[0], qubits[1])
        else:
            raise ValueError(f"稳定子引擎暂不支持门 '{name}'")

    # ------------------------------------------------------------------
    # 测量 + 投影
    # ------------------------------------------------------------------
    def _rowsum(self, i, p):
        """row i = row i * row p（Pauli 乘法，带相位）。"""
        xi, zi = self.x[i], self.z[i]
        xp, zp = self.x[p], self.z[p]
        per_q = (
            (xi & zi).astype(int)
            + (xp & zp).astype(int)
            + 2 * (zi & xp).astype(int)
            - ((xi ^ xp) & (zi ^ zp)).astype(int)
        )
        inc = int(per_q.sum() % 4)
        self.phase[i] = (self.phase[i] + self.phase[p] + inc) % 4
        self.x[i] = xi ^ xp
        self.z[i] = zi ^ zp

    @staticmethod
    def _bit(g, c, n):
        """symplectic 向量 g=(x, z) 的第 c 位：c<n 为 x 区，c>=n 为 z 区。"""
        if c < n:
            return bool(g[0][c])
        return bool(g[1][c - n])

    @staticmethod
    def _mul(g, h):
        """Pauli 乘法 g·h，返回 (x^, z^, phase mod 4)。"""
        x1, z1, p1 = g
        x2, z2, p2 = h
        per_q = (
            (x1 & z1).astype(int)
            + (x2 & z2).astype(int)
            + 2 * (z1 & x2).astype(int)
            - ((x1 ^ x2) & (z1 ^ z2)).astype(int)
        )
        inc = int(per_q.sum() % 4)
        return x1 ^ x2, z1 ^ z2, (p1 + p2 + inc) % 4

    def _deterministic_outcome(self, q):
        """无稳定子行含 X_q 时，测量确定；用高斯消元求 Z_q 的符号。"""
        n = self.n
        gens = [
            [self.x[i].copy(), self.z[i].copy(), int(self.phase[i])]
            for i in range(n, 2 * n)
        ]
        pivot = [-1] * (2 * n)
        for i in range(n):
            first = next((c for c in range(2 * n) if self._bit(gens[i], c, n)), None)
            if first is None:
                continue
            pivot[first] = i
            for j in range(n):
                if j != i and self._bit(gens[j], first, n):
                    gens[j] = self._mul(gens[j], gens[i])
        target = [np.zeros(n, dtype=bool), np.zeros(n, dtype=bool), 0]
        target[1][q] = True
        for c in range(2 * n):
            if self._bit(target, c, n):
                i = pivot[c]
                if i < 0:
                    raise RuntimeError("确定性测量失败：Z_q 不在稳定子群内")
                target = self._mul(target, gens[i])
        return 0 if target[2] == 0 else 1

    def _measure(self, q):
        n = self.n
        p = None
        for i in range(n, 2 * n):
            if self.x[i, q]:
                p = i
                break
        if p is None:
            return self._deterministic_outcome(q)
        outcome = int(np.random.randint(2))
        for i in range(2 * n):
            if i != p and self.x[i, q]:
                self._rowsum(i, p)
        # destabilizer 行 (p-n) = 旧 stabilizer 行 p；stabilizer 行 p = ±Z_q
        self.x[p - n] = self.x[p]
        self.z[p - n] = self.z[p]
        self.phase[p - n] = self.phase[p]
        self.x[p] = False
        self.z[p] = False
        self.z[p, q] = True
        self.phase[p] = 2 * outcome
        return outcome

    def sample(self, shots):
        counts = {}
        for _ in range(shots):
            engine = self._copy()
            bits = [engine._measure(q) for q in range(self.n)]
            bs = "".join(str(b) for b in reversed(bits))
            counts[bs] = counts.get(bs, 0) + 1
        return counts

    def _copy(self):
        e = StabilizerEngine(self.n)
        e.x = self.x.copy()
        e.z = self.z.copy()
        e.phase = self.phase.copy()
        return e
