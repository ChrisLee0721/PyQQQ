"""MindQuantum backend adapter."""

from __future__ import annotations

from typing import Any, Dict, Tuple

from .._i18n import tr
from ..noise import NoiseModel
from .engine import EngineBackend


class MindQuantumBackend(EngineBackend):
    name = "mindquantum"
    _MISSING_ERR = "err.mindquantum_missing"
    _GATE_ERR = "err.mindquantum_gate"
    methods = frozenset({"statevector", "density_matrix"})

    # ------------------------------------------------------------------ #
    #  Statevector path (v1, unchanged)
    # ------------------------------------------------------------------ #

    def _create(self, n: int) -> Any:
        try:
            from mindquantum import Circuit
        except ImportError as e:
            raise ImportError(tr(self._MISSING_ERR)) from e
        self._n = n
        return Circuit()

    def _apply_one(
        self, engine: Any, name: str, qubits: list[int], params: Tuple[float, ...]
    ) -> None:
        from mindquantum import gates as G

        if name == "identity":
            engine += G.I.on(qubits[0])
        elif name == "h":
            engine += G.H.on(qubits[0])
        elif name == "x":
            engine += G.X.on(qubits[0])
        elif name == "y":
            engine += G.Y.on(qubits[0])
        elif name == "z":
            engine += G.Z.on(qubits[0])
        elif name == "cx":
            engine += G.X.on(qubits[1], qubits[0])  # CNOT: target, control
        elif name == "cz":
            engine += G.Z.on(qubits[1], qubits[0])
        elif name == "swap":
            engine += G.SWAP.on(qubits[0], qubits[1])
        elif name == "ccx":
            engine += G.X.on(qubits[2], [qubits[0], qubits[1]])
        elif name == "rx":
            engine += G.RX(params[0]).on(qubits[0])
        elif name == "ry":
            engine += G.RY(params[0]).on(qubits[0])
        elif name == "rz":
            engine += G.RZ(params[0]).on(qubits[0])
        elif name == "p":
            engine += G.PhaseShift(params[0]).on(qubits[0])
        elif name == "cp":
            engine += G.PhaseShift(params[0]).on(qubits[1], qubits[0])
        elif name == "mcz":
            self._apply_mcz(engine, qubits)
        elif name == "measure":
            pass
        else:
            raise ValueError(tr(self._GATE_ERR, name=name))

    @staticmethod
    def _apply_mcz(engine: Any, qubits: list[int]) -> None:
        from mindquantum import gates as G

        if len(qubits) == 2:
            engine += G.Z.on(qubits[1], qubits[0])
        else:
            target = qubits[-1]
            engine += G.H.on(target)
            for c in qubits[:-1]:
                engine += G.X.on(target, c)
            engine += G.H.on(target)

    def _sample(self, engine: Any, shots: int, n: int) -> Dict[str, int]:
        from mindquantum import Simulator

        sim = Simulator("cpu", n)
        sim.apply_circuit(engine)
        raw = sim.sampling(shots)
        counts: Dict[str, int] = {}
        for sample in raw.samples:
            bs = "".join(str(int(sample[i])) for i in range(n))[::-1]
            counts[bs] = counts.get(bs, 0) + 1
        return counts

    # ------------------------------------------------------------------ #
    #  Density-matrix path (v2)
    # ------------------------------------------------------------------ #

    def _run_noisy(
        self, circuit: Any, shots: int, nm: NoiseModel, method: str
    ) -> Any:
        """MindQuantum supports noise natively via Simulator with noise gates."""
        from mindquantum import Circuit, Simulator
        from mindquantum import gates as G
        from mindquantum.noise import Depolarizing

        from ..result import Result

        circ = Circuit()
        for op in circuit.ops:
            if op.name == "measure":
                continue
            # Apply gate using the same dispatch
            self._apply_one(circ, op.name, list(op.qubits), op.params)
            # Apply noise gate after
            nq = len(op.qubits)
            if nq == 1 and nm.single > 0:
                circ += G.NoiseGate(Depolarizing(nm.single)).on(op.qubits[0])
            elif nq == 2 and nm.double > 0:
                circ += G.NoiseGate(Depolarizing(nm.double)).on(
                    list(op.qubits)
                )

        sim = Simulator("density_matrix", circuit.num_qubits)
        sim.apply_circuit(circ)
        raw = sim.sampling(shots)
        counts: Dict[str, int] = {}
        for sample in raw.samples:
            bs = "".join(str(int(sample[i])) for i in range(circuit.num_qubits))[::-1]
            counts[bs] = counts.get(bs, 0) + 1

        if nm.readout > 0:
            counts = self._apply_readout_noise(
                counts, circuit.num_qubits, nm.readout
            )
        return Result.from_counts(counts, shots)

    def _measure_qubit(self, engine: Any, qubit: int) -> int:
        """Mid-circuit measurement via manual probability extraction."""
        import numpy as np

        from mindquantum import Simulator

        sim = Simulator("cpu", self._n)
        sim.apply_circuit(engine)
        # Get state vector and compute P(1)
        sv = sim.get_qs()
        n = self._n
        idx = np.arange(2**n)
        bit = (idx >> qubit) & 1
        p0 = float(np.sum(np.abs(sv[bit == 0]) ** 2))
        outcome = 0 if np.random.random() < p0 else 1
        return outcome
