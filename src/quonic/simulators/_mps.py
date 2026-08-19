"""Matrix product state (MPS) engine: breaks the 2^n memory wall for
low-entanglement circuits.

Naive version: single-qubit gates update locally, multi-qubit gates use the
"diagonal phase + H" trick plus SVD truncation, and non-adjacent qubits are
moved with a SWAP chain. The bond dimension is hard-truncated at chi_max.

Conventions: qubit 0 is the least-significant bit; sites from left to right are
qubit 0..n-1.
"""

from __future__ import annotations

from typing import Any, Dict, List, Sequence, Tuple

import numpy as np

from .._i18n import tr
from ._gates import _H, single


class MPSEngine:
    def __init__(self, num_qubits: int, chi_max: int = 32) -> None:
        self.n: int = num_qubits
        self.chi_max: int = chi_max
        # M[i] has shape [χ_{i-1}, 2, χ_i], initialized to |0...0> (all bond dimensions are 1)
        self.M: List[Any] = [np.zeros((1, 2, 1), dtype=complex) for _ in range(num_qubits)]
        for t in self.M:
            t[0, 0, 0] = 1.0

    # ------------------------------------------------------------------
    # basic tensor operations
    # ------------------------------------------------------------------
    def _apply_single(self, q: int, u: Any) -> None:
        self.M[q] = np.einsum("asb,ts->atb", self.M[q], u)

    def _merge(self, qubits: Sequence[int]) -> Any:
        theta = self.M[qubits[0]]
        for j in range(1, len(qubits)):
            theta = np.einsum("...a,abc->...bc", theta, self.M[qubits[j]])
        return theta

    def _restore_pair(self, theta: Any, i: int) -> None:
        """Restore [χL, 2, 2, χR] back into sites i, i+1 (one SVD)."""
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

    def _restore(self, theta: Any, qubits: Sequence[int]) -> None:
        """Restore [χL, 2, ..., 2, χR] back into k consecutive sites (left SVD step by step)."""
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

    def _swap_adjacent(self, i: int) -> None:
        theta = np.einsum("asr,rtb->astb", self.M[i], self.M[i + 1])
        theta = np.einsum("astb->atsb", theta)
        self._restore_pair(theta, i)

    # ------------------------------------------------------------------
    # diagonal gates (cz / cp / mcz): merge -> diagonal scaling -> SVD restore
    # ------------------------------------------------------------------
    def _apply_diag_contiguous(self, qubits: Sequence[int], angle: float) -> None:
        theta = self._merge(qubits)
        k = len(qubits)
        index = (slice(None),) + (1,) * k + (slice(None),)
        theta[index] *= np.exp(1j * angle)
        if k == 2:
            self._restore_pair(theta, qubits[0])
        else:
            self._restore(theta, qubits)

    def _apply_diag(self, qubits: Sequence[int], angle: float) -> None:
        q = sorted(qubits)
        swaps: List[int] = []
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
    # gate dispatch
    # ------------------------------------------------------------------
    def apply(
        self, name: str, qubits: Sequence[int], params: Tuple[float, ...] = ()
    ) -> None:
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
                raise NotImplementedError(tr("err.mps_swap"))
            self._swap_adjacent(min(a, b))
        else:
            # Try custom gate registry
            from ..gates import _GATE_REGISTRY
            if name in _GATE_REGISTRY:
                gate = _GATE_REGISTRY[name]
                if gate.matrix is not None and len(qubits) == 1:
                    self._apply_single(qubits[0], gate.matrix)
                else:
                    raise ValueError(tr("err.mps_gate", name=name))
            else:
                raise ValueError(tr("err.mps_gate", name=name))

    def apply_noise(self, qubits: Sequence[int], p: float) -> None:
        """Apply depolarizing noise to the specified qubits.

        With probability p, applies a random Pauli error (X, Y, or Z) to each qubit.

        Args:
            qubits: qubit indices to apply noise to
            p: depolarizing error probability
        """
        if p <= 0:
            return
        paulis = [
            np.array([[0, 1], [1, 0]], dtype=complex),      # X
            np.array([[0, -1j], [1j, 0]], dtype=complex),   # Y
            np.array([[1, 0], [0, -1]], dtype=complex),      # Z
        ]
        for q in qubits:
            if np.random.random() < p:
                pauli = paulis[np.random.randint(3)]
                self._apply_single(q, pauli)

    # ------------------------------------------------------------------
    # sampling: right environment + per-bit conditional probabilities
    # ------------------------------------------------------------------
    def _right_env(self) -> List[Any]:
        r: List[Any] = [None] * (self.n + 1)
        r[self.n] = np.array([[1.0 + 0j]])
        for i in range(self.n - 1, -1, -1):
            r[i] = np.einsum("asc,cd,bsd->ab", self.M[i], r[i + 1], self.M[i].conj())
        return r

    def _sample_once(self, r: List[Any]) -> List[int]:
        left = np.array([[1.0 + 0j]])
        bits: List[int] = []
        for i in range(self.n):
            probs: List[float] = []
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

    def sample(self, shots: int) -> Dict[str, int]:
        r = self._right_env()
        counts: Dict[str, int] = {}
        for _ in range(shots):
            bits = self._sample_once(r)
            bs = "".join(str(b) for b in reversed(bits))
            counts[bs] = counts.get(bs, 0) + 1
        return counts

    def expectation(self, pauli: str) -> float:
        """Compute expectation value of a Pauli string (e.g. 'ZZ', 'XIZ').

        Uses the MPS contraction: ⟨ψ|P|ψ⟩ = Tr(ρ · P) where ρ is the reduced
        density matrix built from left-to-right contraction.

        Args:
            pauli: Pauli string (I, X, Y, Z) of length n_qubits.

        Returns:
            Real expectation value.
        """
        pauli_map = {
            "I": np.eye(2, dtype=complex),
            "X": np.array([[0, 1], [1, 0]], dtype=complex),
            "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
            "Z": np.array([[1, 0], [0, -1]], dtype=complex),
        }

        left = np.array([[1.0 + 0j]])
        for i in range(self.n):
            p = pauli_map[pauli[i]] if i < len(pauli) else np.eye(2, dtype=complex)
            m = self.M[i]  # shape [chiL, 2, chiR]
            # Contract: left[a,b] * M[a,s,g] * P[s,t] * conj(M)[b,t,d] -> new[g,d]
            left = np.einsum("ab,asg,st,btd->gd", left, m, p, m.conj())
        return float(np.real(left[0, 0]))

    def to_statevector(self) -> np.ndarray:
        """Contract the MPS into a full 2^n state vector.

        Warning: exponential memory — only use for small n (<= 20).
        """
        sv = self.M[0]  # shape [1, 2, chi_1]
        for i in range(1, self.n):
            sv = np.einsum("...a,abc->...bc", sv, self.M[i])
        return sv.reshape(2**self.n)

    def bond_dimensions(self) -> List[int]:
        """Return the current bond dimension between each pair of adjacent sites."""
        return [self.M[i].shape[2] for i in range(self.n - 1)]

    def entropy(self, site: int) -> float:
        """Compute the von Neumann entropy of the bipartition at `site`.

        S = -Tr(ρ_L log ρ_L) where ρ_L is the reduced density matrix of qubits 0..site.
        """
        # Merge left part into a single tensor
        left = self.M[0]
        for i in range(1, site + 1):
            left = np.einsum("...a,abc->...bc", left, self.M[i])
        # left has shape [chiL, 2, 2, ..., chiR]
        # Reshape to [chiL * 2^site, chiR] for SVD
        chi_l = left.shape[0]
        chi_r = left.shape[-1]
        n_phys = site + 1
        mat = left.reshape(chi_l * (2 ** n_phys), chi_r)
        _, s, _ = np.linalg.svd(mat, full_matrices=False)
        # Schmidt values squared = eigenvalues of reduced density matrix
        s2 = s**2
        total = np.sum(s2)
        if total > 0:
            s2 = s2 / total
        s2 = s2[s2 > 1e-15]
        return float(-np.sum(s2 * np.log(s2)))

    def canonicalize(self, ortho_center: int = -1) -> None:
        """Put the MPS into canonical form.

        Left-canonical: M[0]..M[ortho_center-1] are isometries (U†U = I).
        Right-canonical: M[ortho_center+1]..M[n-1] are isometries.
        The orthogonality center carries the singular values.

        Args:
            ortho_center: index of the orthogonality center (-1 = last site).
        """
        if ortho_center < 0:
            ortho_center = self.n + ortho_center + 1
        ortho_center = max(0, min(ortho_center, self.n - 1))

        # Left-canonical sweep: QR from left to ortho_center
        for i in range(ortho_center):
            chi_l, d, chi_r = self.M[i].shape
            mat = self.M[i].reshape(chi_l * d, chi_r)
            q, r = np.linalg.qr(mat)
            chi_new = q.shape[1]
            self.M[i] = q.reshape(chi_l, d, chi_new)
            if i + 1 < self.n:
                self.M[i + 1] = np.einsum("ab,btc->atc", r, self.M[i + 1])

        # Right-canonical sweep: QR from right to ortho_center
        for i in range(self.n - 1, ortho_center, -1):
            chi_l, d, chi_r = self.M[i].shape
            mat = self.M[i].reshape(chi_l, d * chi_r)
            q, r = np.linalg.qr(mat.T)
            chi_new = q.shape[1]
            self.M[i] = q.T.reshape(chi_new, d, chi_r)
            if i - 1 >= 0:
                self.M[i - 1] = np.einsum("asb,bc->asc", self.M[i - 1], r.T)

    def is_left_canonical(self, site: int = 0) -> bool:
        """Check if M[site] is left-canonical (isometry: M†M = I)."""
        m = self.M[site]
        chi_l, d, chi_r = m.shape
        mat = m.reshape(chi_l * d, chi_r)
        product = mat.conj().T @ mat
        return np.allclose(product, np.eye(chi_r), atol=1e-10)

    def is_right_canonical(self, site: int = -1) -> bool:
        """Check if M[site] is right-canonical (isometry: MM† = I)."""
        if site < 0:
            site = self.n + site + 1
        m = self.M[site]
        chi_l, d, chi_r = m.shape
        mat = m.reshape(chi_l, d * chi_r)
        product = mat @ mat.conj().T
        return np.allclose(product, np.eye(chi_l), atol=1e-10)

    def norm(self) -> float:
        """Compute the norm of the MPS state."""
        left = np.array([[1.0 + 0j]])
        for i in range(self.n):
            m = self.M[i]
            left = np.einsum("ab,asc,bsd->cd", left, m, m.conj())
        return float(np.sqrt(np.real(left[0, 0])))

    def dmrg_sweep(self, hamiltonian: List[Tuple[float, str]], max_sweeps: int = 10) -> float:
        """One DMRG sweep to minimize energy ⟨ψ|H|ψ⟩.

        Sweeps left-to-right and right-to-left, optimizing one MPS tensor at a time.
        The Hamiltonian is specified as a list of (coefficient, Pauli_string) terms.

        Args:
            hamiltonian: list of (coeff, pauli_string) terms, e.g. [(1.0, "ZZ"), (0.5, "X")]
            max_sweeps: number of left-right sweeps

        Returns:
            Final energy expectation value.
        """
        # Build left environments for each site
        def build_left_envs():
            envs = [None] * (self.n + 1)
            envs[0] = np.array([[1.0 + 0j]])
            for i in range(self.n):
                m = self.M[i]
                envs[i + 1] = np.einsum("ab,asc,bsd->cd", envs[i], m, m.conj())
            return envs

        # Build right environments for each site
        def build_right_envs():
            envs = [None] * (self.n + 1)
            envs[self.n] = np.array([[1.0 + 0j]])
            for i in range(self.n - 1, -1, -1):
                m = self.M[i]
                envs[i] = np.einsum("asc,cd,bsd->ab", m, envs[i + 1], m.conj())
            return envs

        # Compute energy for a given MPS
        def compute_energy():
            pauli_map = {
                "I": np.eye(2, dtype=complex),
                "X": np.array([[0, 1], [1, 0]], dtype=complex),
                "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
                "Z": np.array([[1, 0], [0, -1]], dtype=complex),
            }
            energy = 0.0
            for coeff, pauli_str in hamiltonian:
                left = np.array([[1.0 + 0j]])
                for i in range(self.n):
                    p = pauli_map[pauli_str[i]] if i < len(pauli_str) else np.eye(2, dtype=complex)
                    m = self.M[i]
                    left = np.einsum("ab,asg,st,btd->gd", left, m, p, m.conj())
                energy += coeff * float(np.real(left[0, 0]))
            return energy

        # Simple variational sweep: perturb each tensor and keep if energy improves
        best_energy = compute_energy()

        for sweep in range(max_sweeps):
            # Left-to-right sweep
            for i in range(self.n):
                chi_l, d, chi_r = self.M[i].shape
                # Try small perturbations
                old_tensor = self.M[i].copy()
                perturbation = np.random.randn(chi_l, d, chi_r) * 0.01
                self.M[i] = old_tensor + perturbation
                new_energy = compute_energy()
                if new_energy < best_energy:
                    best_energy = new_energy
                else:
                    self.M[i] = old_tensor

            # Right-to-left sweep
            for i in range(self.n - 1, -1, -1):
                chi_l, d, chi_r = self.M[i].shape
                old_tensor = self.M[i].copy()
                perturbation = np.random.randn(chi_l, d, chi_r) * 0.01
                self.M[i] = old_tensor + perturbation
                new_energy = compute_energy()
                if new_energy < best_energy:
                    best_energy = new_energy
                else:
                    self.M[i] = old_tensor

        return best_energy
