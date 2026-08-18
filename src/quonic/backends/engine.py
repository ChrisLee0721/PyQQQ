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
