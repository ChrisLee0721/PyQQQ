"""EngineBackend — generic simulator backend base class.

Subclasses only need to implement three methods:
  _create(n)          — create the SDK circuit/engine for n qubits
  _apply_one(engine, name, qubits, params) — apply a single gate
  _sample(engine, shots, n) — sample and return counts (qubit 0 = LSB)

The shared ``run()`` loop handles the iteration, auto-measurement, and
result conversion.

v2 adds optional hooks for noise injection and classical control flow:
  _create_dm(n)       — create a density-matrix engine (for noise)
  _apply_one_dm(...)  — gate dispatch for DM engine (defaults to _apply_one)
  _sample_dm(...)     — sampling from DM engine (defaults to _sample)
  _apply_noise_after_gate(engine, qubits, nm) — inject noise after a gate
  _measure_qubit(engine, qubit) — mid-circuit measurement (returns 0/1)
"""

from __future__ import annotations

from abc import abstractmethod
from typing import Any, Dict, FrozenSet, Iterable, Optional, Tuple, Union

from .._i18n import tr
from ..ir import Circuit, CRegCondition
from ..noise import NoiseModel, resolve_noise
from ..result import Result
from .base import Backend


class EngineBackend(Backend):
    """Generic simulator backend.  Subclasses fill _create / _apply_one / _sample.

    v2: Supports noise injection and classical control flow via optional hooks.
    """

    # Subclasses set these:
    _MISSING_ERR: str = ""  # e.g. "err.qulacs_missing"
    _GATE_ERR: str = ""     # e.g. "err.qulacs_gate"

    methods: FrozenSet[str] = frozenset({"statevector"})

    # ------------------------------------------------------------------ #
    #  run() — three-way dispatch
    # ------------------------------------------------------------------ #

    def run(
        self,
        circuit: Circuit,
        shots: int = 1024,
        noise: Optional[Union[NoiseModel, float, int]] = None,
        method: str = "statevector",
    ) -> Result:
        nm = resolve_noise(noise)
        has_ctrl = any(op.name in ("cif", "cmeasure", "cwhile") for op in circuit.ops)

        if has_ctrl:
            return self._run_dynamic(circuit, shots, nm, method)
        if nm.enabled:
            return self._run_noisy(circuit, shots, nm, method)

        # Clean statevector path (v1 behavior, unchanged)
        engine = self._create(circuit.num_qubits)
        for op in circuit.ops:
            self._apply_one(engine, op.name, list(op.qubits), op.params)
        counts = self._sample(engine, shots, circuit.num_qubits)
        return Result.from_counts(counts, shots)

    # ------------------------------------------------------------------ #
    #  _run_noisy — density-matrix + native noise channels
    # ------------------------------------------------------------------ #

    def _run_noisy(
        self, circuit: Circuit, shots: int, nm: NoiseModel, method: str
    ) -> Result:
        """Run with noise injection using density-matrix simulation.

        Subclasses may override for framework-specific noise models (e.g. CUDA-Q's
        global NoiseModel).  The default implementation uses _create_dm +
        _apply_noise_after_gate.
        """
        engine = self._create_dm(circuit.num_qubits)
        for op in circuit.ops:
            if op.name == "measure":
                continue
            self._apply_one_dm(engine, op.name, list(op.qubits), op.params)
            nq = len(op.qubits)
            if nq == 1 and nm.single > 0:
                self._apply_noise_after_gate(engine, list(op.qubits), nm)
            elif nq == 2 and nm.double > 0:
                self._apply_noise_after_gate(engine, list(op.qubits), nm)
        counts = self._sample_dm(engine, shots, circuit.num_qubits)
        if nm.readout > 0:
            counts = self._apply_readout_noise(counts, circuit.num_qubits, nm.readout)
        return Result.from_counts(counts, shots)

    # ------------------------------------------------------------------ #
    #  _run_dynamic — per-shot loop for classical control flow
    # ------------------------------------------------------------------ #

    def _run_dynamic(
        self, circuit: Circuit, shots: int, nm: NoiseModel, method: str
    ) -> Result:
        """Per-shot simulation for classical control flow (cif/cmeasure/cwhile).

        Each shot creates a fresh engine, executes ops sequentially with Python-level
        classical register tracking.  Modeled after NativeBackend._run_dynamic.
        """
        use_dm = nm.enabled
        counts: Dict[str, int] = {}
        for _ in range(shots):
            if use_dm:
                engine = self._create_dm(circuit.num_qubits)
            else:
                engine = self._create(circuit.num_qubits)
            cregs: Dict[str, int] = {}
            self._execute_shot(engine, circuit.ops, cregs, use_dm, nm)
            shot_counts = (self._sample_dm if use_dm else self._sample)(
                engine, 1, circuit.num_qubits
            )
            for bs, c in shot_counts.items():
                counts[bs] = counts.get(bs, 0) + c
        if nm.readout > 0:
            counts = self._apply_readout_noise(counts, circuit.num_qubits, nm.readout)
        return Result.from_counts(counts, shots)

    def _execute_shot(
        self,
        engine: Any,
        ops: Iterable[Any],
        cregs: Dict[str, int],
        use_dm: bool,
        nm: NoiseModel,
    ) -> None:
        """Execute a block of ops for a single shot, maintaining classical registers."""
        for op in ops:
            name = op.name
            if name == "cmeasure":
                outcome = self._measure_qubit(engine, op.qubit)
                v = cregs.get(op.creg, 0)
                cregs[op.creg] = (v & ~(1 << op.bit)) | (outcome << op.bit)
            elif name == "cif":
                if isinstance(op.control, int):
                    outcome = self._measure_qubit(engine, op.control)
                    hit = outcome == 1
                elif isinstance(op.control, CRegCondition):
                    hit = cregs.get(op.control.creg, 0) == op.control.value
                else:
                    hit = cregs.get(op.control, 0) == 1
                branch = op.then_op if hit else op.else_op
                apply_fn = self._apply_one_dm if use_dm else self._apply_one
                apply_fn(engine, branch.name, list(branch.qubits), branch.params)
            elif name == "cwhile":
                iters = 0
                while cregs.get(op.creg, 0) != op.until:
                    self._execute_shot(engine, op.body, cregs, use_dm, nm)
                    iters += 1
                    if iters > 100000:
                        raise RuntimeError(tr("err.cwhile_limit", creg=op.creg))
            elif name == "measure":
                pass  # handled by auto-measurement in _sample
            else:
                apply_fn = self._apply_one_dm if use_dm else self._apply_one
                apply_fn(engine, name, list(op.qubits), op.params)
                if use_dm and nm.enabled:
                    self._apply_noise_after_gate(engine, list(op.qubits), nm)

    # ------------------------------------------------------------------ #
    #  Abstract methods (unchanged from v1)
    # ------------------------------------------------------------------ #

    @abstractmethod
    def _create(self, n: int) -> Any:
        """Create and return an SDK circuit/engine for *n* qubits."""

    @abstractmethod
    def _apply_one(
        self, engine: Any, name: str, qubits: list[int], params: Tuple[float, ...]
    ) -> None:
        """Apply a single gate by QuoNic gate name.  Raise ValueError for unknown gates."""

    @abstractmethod
    def _sample(self, engine: Any, shots: int, n: int) -> Dict[str, int]:
        """Sample *shots* bitstrings, return {bitstring: count} with qubit 0 = LSB."""

    # ------------------------------------------------------------------ #
    #  Optional hooks (safe defaults)
    # ------------------------------------------------------------------ #

    def _create_dm(self, n: int) -> Any:
        """Create a density-matrix engine for *n* qubits.  Override in subclasses."""
        raise NotImplementedError(tr("err.engine_no_dm", name=self.name))

    def _apply_one_dm(
        self, engine: Any, name: str, qubits: list[int], params: Tuple[float, ...]
    ) -> None:
        """Apply a gate to the DM engine.  Default: delegates to _apply_one."""
        self._apply_one(engine, name, qubits, params)

    def _sample_dm(self, engine: Any, shots: int, n: int) -> Dict[str, int]:
        """Sample from the DM engine.  Default: delegates to _sample."""
        return self._sample(engine, shots, n)

    def _apply_noise_after_gate(
        self, engine: Any, qubits: list[int], nm: NoiseModel
    ) -> None:
        """Inject a noise channel after a gate application.  Default: no-op."""

    def _measure_qubit(self, engine: Any, qubit: int) -> int:
        """Mid-circuit measurement: collapse state and return 0 or 1.

        Override in subclasses that support mid-circuit measurement.
        """
        raise NotImplementedError(tr("err.engine_no_measure", name=self.name))

    # ------------------------------------------------------------------ #
    #  Numpy state-vector helpers for dynamic path
    # ------------------------------------------------------------------ #

    def _run_dynamic_sv(self, circuit, shots, nm):
        """Generic dynamic-path implementation using numpy state vectors.

        Backends that don't have a stateful SDK engine can use this as their
        _run_dynamic: it builds the state vector in pure numpy, supports
        mid-circuit measurement with collapse, and samples at the end.
        """
        import numpy as np

        n = circuit.num_qubits
        counts: Dict[str, int] = {}

        for _ in range(shots):
            sv = np.zeros(2**n, dtype=complex)
            sv[0] = 1.0
            cregs: Dict[str, int] = {}
            sv = self._sv_execute(sv, circuit.ops, cregs, n)
            probs = np.abs(sv) ** 2
            probs = probs / probs.sum()
            idx = np.random.choice(2**n, p=probs)
            bs = format(idx, f"0{n}b")[::-1]
            counts[bs] = counts.get(bs, 0) + 1

        if nm.readout > 0:
            counts = self._apply_readout_noise(counts, n, nm.readout)
        return Result.from_counts(counts, shots)

    def _sv_execute(self, sv, ops, cregs, n):
        """Execute ops on a numpy state vector, collapsing on measurement."""

        for op in ops:
            name = op.name
            if name == "cmeasure":
                outcome = self._sv_measure(sv, op.qubit, n)
                sv = self._sv_collapse(sv, op.qubit, n, outcome)
                v = cregs.get(op.creg, 0)
                cregs[op.creg] = (v & ~(1 << op.bit)) | (outcome << op.bit)
            elif name == "cif":
                if isinstance(op.control, int):
                    outcome = self._sv_measure(sv, op.control, n)
                    sv = self._sv_collapse(sv, op.control, n, outcome)
                    hit = outcome == 1
                elif isinstance(op.control, CRegCondition):
                    hit = cregs.get(op.control.creg, 0) == op.control.value
                else:
                    hit = cregs.get(op.control, 0) == 1
                branch = op.then_op if hit else op.else_op
                sv = self._sv_apply_gate(sv, branch.name, list(branch.qubits), branch.params, n)
            elif name == "cwhile":
                iters = 0
                while cregs.get(op.creg, 0) != op.until:
                    sv = self._sv_execute(sv, op.body, cregs, n)
                    iters += 1
                    if iters > 100000:
                        raise RuntimeError(tr("err.cwhile_limit", creg=op.creg))
            elif name == "measure":
                pass
            else:
                sv = self._sv_apply_gate(sv, name, list(op.qubits), op.params, n)
        return sv

    def _sv_apply_gate(self, sv, name, qubits, params, n):
        """Apply a gate to a numpy state vector."""

        if name in ("measure", "identity", "i"):
            return sv

        u = self._sv_gate_matrix(name, params)
        if u is not None and len(qubits) == 1:
            return self._sv_apply_single(sv, u, qubits[0], n)

        if name == "cx" and len(qubits) == 2:
            return self._sv_apply_cx(sv, qubits[0], qubits[1], n)
        if name == "cz" and len(qubits) == 2:
            return self._sv_apply_cz(sv, qubits[0], qubits[1], n)
        if name == "cp" and len(qubits) == 2:
            return self._sv_apply_cp(sv, qubits[0], qubits[1], params[0], n)
        if name == "ccx" and len(qubits) == 3:
            return self._sv_apply_ccx(sv, qubits[0], qubits[1], qubits[2], n)
        if name == "swap" and len(qubits) == 2:
            return self._sv_apply_swap(sv, qubits[0], qubits[1], n)
        if name == "mcz":
            return self._sv_apply_mcz(sv, qubits, n)
        return sv

    @staticmethod
    def _sv_gate_matrix(name, params):
        """Return 2x2 unitary matrix for a single-qubit gate."""
        import numpy as np

        if name == "h":
            return np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
        if name == "x":
            return np.array([[0, 1], [1, 0]], dtype=complex)
        if name == "y":
            return np.array([[0, -1j], [1j, 0]], dtype=complex)
        if name == "z":
            return np.array([[1, 0], [0, -1]], dtype=complex)
        if name == "rx":
            t = params[0]
            return np.array(
                [[np.cos(t / 2), -1j * np.sin(t / 2)], [-1j * np.sin(t / 2), np.cos(t / 2)]],
                dtype=complex,
            )
        if name == "ry":
            t = params[0]
            return np.array(
                [[np.cos(t / 2), -np.sin(t / 2)], [np.sin(t / 2), np.cos(t / 2)]],
                dtype=complex,
            )
        if name == "rz":
            t = params[0]
            return np.array(
                [[np.exp(-1j * t / 2), 0], [0, np.exp(1j * t / 2)]], dtype=complex
            )
        if name == "p":
            t = params[0]
            return np.array([[1, 0], [0, np.exp(1j * t)]], dtype=complex)
        return None

    @staticmethod
    def _sv_apply_single(sv, u, qubit, n):
        """Apply a single-qubit gate to a state vector."""

        new_sv = sv.copy()
        for i in range(2**n):
            if (i >> qubit) & 1 == 0:
                j = i | (1 << qubit)
                a, b = sv[i], sv[j]
                new_sv[i] = u[0, 0] * a + u[0, 1] * b
                new_sv[j] = u[1, 0] * a + u[1, 1] * b
        return new_sv

    @staticmethod
    def _sv_apply_cx(sv, control, target, n):
        """Apply CX (CNOT) gate."""
        new_sv = sv.copy()
        for i in range(2**n):
            if (i >> control) & 1 == 1:
                j = i ^ (1 << target)
                new_sv[i] = sv[j]
                new_sv[j] = sv[i]
        return new_sv

    @staticmethod
    def _sv_apply_cz(sv, q0, q1, n):
        """Apply CZ gate."""
        new_sv = sv.copy()
        for i in range(2**n):
            if (i >> q0) & 1 == 1 and (i >> q1) & 1 == 1:
                new_sv[i] = -sv[i]
        return new_sv

    @staticmethod
    def _sv_apply_cp(sv, q0, q1, theta, n):
        """Apply controlled-phase gate."""
        import numpy as np

        new_sv = sv.copy()
        for i in range(2**n):
            if (i >> q0) & 1 == 1 and (i >> q1) & 1 == 1:
                new_sv[i] = np.exp(1j * theta) * sv[i]
        return new_sv

    @staticmethod
    def _sv_apply_ccx(sv, c0, c1, target, n):
        """Apply Toffoli (CCX) gate."""
        new_sv = sv.copy()
        for i in range(2**n):
            if (i >> c0) & 1 == 1 and (i >> c1) & 1 == 1:
                j = i ^ (1 << target)
                new_sv[i] = sv[j]
                new_sv[j] = sv[i]
        return new_sv

    @staticmethod
    def _sv_apply_swap(sv, q0, q1, n):
        """Apply SWAP gate."""
        new_sv = sv.copy()
        for i in range(2**n):
            b0 = (i >> q0) & 1
            b1 = (i >> q1) & 1
            if b0 != b1:
                j = i ^ (1 << q0) ^ (1 << q1)
                new_sv[i] = sv[j]
                new_sv[j] = sv[i]
        return new_sv

    @staticmethod
    def _sv_apply_mcz(sv, qubits, n):
        """Apply multi-controlled Z gate."""
        new_sv = sv.copy()
        for i in range(2**n):
            if all((i >> q) & 1 == 1 for q in qubits):
                new_sv[i] = -sv[i]
        return new_sv

    @staticmethod
    def _sv_measure(sv, qubit, n):
        """Measure a qubit from a state vector, return 0 or 1."""
        import numpy as np

        idx = np.arange(2**n)
        bit = (idx >> qubit) & 1
        p0 = float(np.sum(np.abs(sv[bit == 0]) ** 2))
        return 0 if np.random.random() < p0 else 1

    @staticmethod
    def _sv_collapse(sv, qubit, n, outcome):
        """Collapse state vector after measurement."""
        import numpy as np

        idx = np.arange(2**n)
        bit = (idx >> qubit) & 1
        new_sv = sv.copy()
        new_sv[bit != outcome] = 0.0
        norm = np.linalg.norm(new_sv)
        if norm > 0:
            new_sv /= norm
        return new_sv

    # ------------------------------------------------------------------ #
    #  Shared helpers
    # ------------------------------------------------------------------ #

    @staticmethod
    def _apply_readout_noise(
        counts: Dict[str, int], n: int, readout_prob: float
    ) -> Dict[str, int]:
        """Apply bit-flip readout noise to a counts dict.

        For each unique bitstring, compute the probability of each possible
        output bitstring using the tensor product of per-qubit confusion
        matrices, then distribute counts accordingly.  O(unique_states × 2^n).
        """
        import numpy as np

        if not counts or readout_prob <= 0:
            return dict(counts)

        p = readout_prob
        # Per-qubit confusion matrix: [[1-p, p], [p, 1-p]]
        # Tensor product over n qubits gives 2^n × 2^n transition matrix
        single = np.array([[1 - p, p], [p, 1 - p]])
        mat = single
        for _ in range(n - 1):
            mat = np.kron(mat, single)

        noisy: Dict[str, int] = {}
        fmt = f"0{n}b"
        for bs, c in counts.items():
            # Input index
            in_idx = int(bs, 2)
            # Output probabilities for this input
            probs = mat[:, in_idx]
            # Distribute counts
            for out_idx in range(2**n):
                expected = probs[out_idx] * c
                if expected > 0.5:  # round to nearest integer
                    out_bs = format(out_idx, fmt)
                    noisy[out_bs] = noisy.get(out_bs, 0) + round(expected)
                elif expected > 0.001:  # keep small but non-negligible
                    out_bs = format(out_idx, fmt)
                    noisy[out_bs] = noisy.get(out_bs, 0) + max(1, round(expected))

        return noisy
