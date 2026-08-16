"""密度矩阵引擎：2^n × 2^n 密度矩阵，支持去极化噪声。

约定：qubit 0 是最低位。噪声在每个逻辑门之后施加（去极化信道）。
"""

import numpy as np

from ..noise import resolve_noise
from ._gates import _H, single

_I = np.eye(2, dtype=complex)
_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
_Y = np.array([[0.0, -1j], [1j, 0.0]], dtype=complex)
_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
_PAULIS = (_I, _X, _Y, _Z)


class DensityMatrixEngine:
    def __init__(self, num_qubits, noise=None):
        self.n = num_qubits
        self.noise = resolve_noise(noise)
        self.rho = np.zeros((2 ** num_qubits, 2 ** num_qubits), dtype=complex)
        self.rho[0, 0] = 1.0

    @staticmethod
    def _apply_single_to(rho, u, q, n):
        hi = 2 ** (n - q - 1)
        lo = 2 ** q
        r = rho.reshape(hi, 2, lo, hi, 2, lo)
        uc = u.conj().T
        return np.einsum("AQBCRD,qQ,Rr->AqBCrD", r, u, uc).reshape(2 ** n, 2 ** n)

    def _apply_single(self, u, q):
        self.rho = self._apply_single_to(self.rho, u, q, self.n)

    def _apply_phase(self, qubits, angle):
        idx = np.arange(2 ** self.n)
        mask = np.ones(2 ** self.n, dtype=bool)
        for q in qubits:
            mask &= ((idx >> q) & 1).astype(bool)
        phase = np.zeros(2 ** self.n)
        phase[mask] = angle
        self.rho *= np.exp(1j * (phase[:, None] - phase[None, :]))

    def _swap(self, a, b):
        if a == b:
            return
        idx = np.arange(2 ** self.n)
        ia = (idx >> a) & 1
        ib = (idx >> b) & 1
        mask = ~((1 << a) | (1 << b))
        perm = (idx & mask) | (ia << b) | (ib << a)
        self.rho = self.rho[perm][:, perm]

    def _depolarize_single(self, q, p):
        rho = self.rho
        result = (1.0 - p) * rho
        for pauli in (_X, _Y, _Z):
            result += (p / 3.0) * self._apply_single_to(rho, pauli, q, self.n)
        self.rho = result

    def _depolarize_double(self, q0, q1, p):
        rho = self.rho
        result = (1.0 - p) * rho
        for pa in _PAULIS:
            for pb in _PAULIS:
                if pa is _I and pb is _I:
                    continue
                tmp = rho
                if pa is not _I:
                    tmp = self._apply_single_to(tmp, pa, q0, self.n)
                if pb is not _I:
                    tmp = self._apply_single_to(tmp, pb, q1, self.n)
                result += (p / 15.0) * tmp
        self.rho = result

    def _noise_after(self, qubits):
        if not self.noise.enabled:
            return
        nq = len(qubits)
        if nq == 1 and self.noise.single > 0.0:
            self._depolarize_single(qubits[0], self.noise.single)
        elif nq == 2 and self.noise.double > 0.0:
            self._depolarize_double(qubits[0], qubits[1], self.noise.double)

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
            raise ValueError(f"密度矩阵引擎暂不支持门 '{name}'")
        self._noise_after(qubits)

    def sample(self, shots):
        probs = np.real(np.diag(self.rho))
        probs = np.clip(probs, 0.0, None)
        probs = probs / probs.sum()
        idx = np.random.choice(2 ** self.n, size=shots, p=probs)
        counts = {}
        fmt = f"0{self.n}b"
        for i in idx:
            bs = format(int(i), fmt)
            counts[bs] = counts.get(bs, 0) + 1
        return counts

    def measure_qubit(self, q):
        """中途测量 qubit q：按对角概率坍缩密度矩阵，返回测量结果 0/1。

        用投影 P_outcome·ρ·P_outcome 实现（保留 2^n 维度，把 qubit q != outcome
        的行列清零），再按迹归一化。
        """
        idx = np.arange(2 ** self.n)
        bit = (idx >> q) & 1
        diag = np.real(np.diag(self.rho))
        p0 = float(np.sum(diag[bit == 0]))
        outcome = 0 if np.random.random() < p0 else 1
        keep = bit == outcome
        self.rho[~keep, :] = 0.0
        self.rho[:, ~keep] = 0.0
        tr = np.real(np.trace(self.rho))
        if tr > 0.0:
            self.rho /= tr
        return outcome
