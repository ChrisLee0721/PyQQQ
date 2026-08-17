"""TensorCircuit backend adapter."""

from __future__ import annotations

from typing import Any, Dict, Tuple

from .._i18n import tr
from ..noise import NoiseModel
from .engine import EngineBackend

_tc_patched = False


def _patch_numpy_for_tensorcircuit() -> None:
    """Monkey-patch numpy so TensorCircuit 0.12 works with numpy 2.x.

    numpy 2.0 made several breaking changes:
    - ``newshape`` kwarg renamed to ``shape`` in np.reshape
    - ``np.ComplexWarning`` removed (now builtins.ComplexWarning)
    - Various other deprecations

    We patch once, before the first ``import tensorcircuit``.
    """
    global _tc_patched
    if _tc_patched:
        return
    import warnings

    import numpy as np

    # 1. Fix np.reshape newshape kwarg (only needed on numpy 2.x)
    if np.__version__ >= "2":
        _orig_reshape = np.reshape

        def _compat_reshape(a, *args, **kwargs):
            if "newshape" in kwargs and "shape" not in kwargs:
                kwargs["shape"] = kwargs.pop("newshape")
            return _orig_reshape(a, *args, **kwargs)

        np.reshape = _compat_reshape

    # 2. Restore np.ComplexWarning (moved to numpy.exceptions in numpy 2.0)
    if np.__version__ >= "2" and not hasattr(np, "ComplexWarning"):
        try:
            from numpy.exceptions import ComplexWarning

            np.ComplexWarning = ComplexWarning
        except ImportError:
            pass

    _tc_patched = True


class TensorCircuitBackend(EngineBackend):
    name = "tensorcircuit"
    _MISSING_ERR = "err.tensorcircuit_missing"
    _GATE_ERR = "err.tensorcircuit_gate"
    methods = frozenset({"statevector", "density_matrix"})

    # ------------------------------------------------------------------ #
    #  Statevector path (v1, unchanged)
    # ------------------------------------------------------------------ #

    def _create(self, n: int) -> Any:
        _patch_numpy_for_tensorcircuit()
        try:
            import tensorcircuit as tc
        except ImportError as e:
            raise ImportError(tr(self._MISSING_ERR)) from e
        return tc.Circuit(n)

    def _apply_one(
        self, engine: Any, name: str, qubits: list[int], params: Tuple[float, ...]
    ) -> None:
        if name in ("identity", "i"):
            pass  # no-op
        elif name == "h":
            engine.h(qubits[0])
        elif name == "x":
            engine.x(qubits[0])
        elif name == "y":
            engine.y(qubits[0])
        elif name == "z":
            engine.z(qubits[0])
        elif name == "cx":
            engine.cnot(qubits[0], qubits[1])
        elif name == "cz":
            engine.cz(qubits[0], qubits[1])
        elif name == "swap":
            engine.swap(qubits[0], qubits[1])
        elif name == "ccx":
            engine.toffoli(qubits[0], qubits[1], qubits[2])
        elif name == "rx":
            engine.rx(qubits[0], theta=params[0])
        elif name == "ry":
            engine.ry(qubits[0], theta=params[0])
        elif name == "rz":
            engine.rz(qubits[0], theta=params[0])
        elif name == "p":
            engine.phase(qubits[0], theta=params[0])
        elif name == "cp":
            engine.cphase(qubits[0], qubits[1], theta=params[0])
        elif name == "mcz":
            self._apply_mcz(engine, qubits)
        elif name == "measure":
            pass
        else:
            raise ValueError(tr(self._GATE_ERR, name=name))

    @staticmethod
    def _apply_mcz(engine: Any, qubits: list[int]) -> None:
        if len(qubits) == 2:
            engine.cz(qubits[0], qubits[1])
        else:
            target = qubits[-1]
            engine.h(target)
            for c in qubits[:-1]:
                engine.cnot(c, target)
            engine.h(target)

    def _sample(self, engine: Any, shots: int, n: int) -> Dict[str, int]:
        raw = engine.sample(shots)
        # TensorCircuit returns list of (bitstring_array, probability) tuples.
        # Convention: qubit 0 is the leftmost character (already LSB-first).
        counts: Dict[str, int] = {}
        for val in raw:
            if isinstance(val, tuple):
                bits = val[0]  # numpy array of 0.0/1.0
                bs = "".join(str(int(bits[i])) for i in range(n))
            elif isinstance(val, str):
                bs = val
            else:
                bs = "".join(str(int(val[i])) for i in range(n))
            counts[bs] = counts.get(bs, 0) + 1
        return counts

    # ------------------------------------------------------------------ #
    #  Density-matrix path (v2)
    # ------------------------------------------------------------------ #

    def _create_dm(self, n: int) -> Any:
        """DMCircuit is a drop-in replacement for Circuit — same API."""
        _patch_numpy_for_tensorcircuit()
        try:
            import tensorcircuit as tc
        except ImportError as e:
            raise ImportError(tr(self._MISSING_ERR)) from e
        return tc.DMCircuit(n)

    def _apply_noise_after_gate(
        self, engine: Any, qubits: list[int], nm: NoiseModel
    ) -> None:
        import tensorcircuit as tc

        p = nm.single if len(qubits) == 1 else nm.double
        if p > 0:
            # depolarizingchannel(px, py, pz) — symmetric: px=py=pz=p/3
            channel = tc.channels.depolarizingchannel(p / 3, p / 3, p / 3)
            for q in qubits:
                engine.apply_general_kraus(channel, [(q,)])

    def _measure_qubit(self, engine: Any, qubit: int) -> int:
        """Mid-circuit measurement via manual probability extraction from DM."""
        import numpy as np

        # Get the density matrix — may be 1D (flattened) or 2D
        dm = engine.state()
        dm_np = dm.numpy() if hasattr(dm, "numpy") else np.asarray(dm)
        if dm_np.ndim == 1:
            dim = int(np.sqrt(len(dm_np)))
            dm_np = dm_np.reshape(dim, dim)
        diag = np.real(np.diag(dm_np))
        n = int(np.log2(len(diag)))
        idx = np.arange(2**n)
        bit = (idx >> qubit) & 1
        p0 = float(np.sum(diag[bit == 0]))
        return 0 if np.random.random() < p0 else 1
