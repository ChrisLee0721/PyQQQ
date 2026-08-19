"""Step-by-step circuit execution — inspect state after each gate.

Example::

    from quonic.stepper import StepExecutor
    executor = StepExecutor(circuit)
    while not executor.done():
        sv = executor.step()
        print(f"Step {executor.step_num}: {sv}")
"""

from __future__ import annotations

from .ir import Circuit
from .statevector import StateVector


class StepExecutor:
    """Execute a circuit one gate at a time, inspecting the state after each step.

    Args:
        circuit: the circuit to execute
        backend: backend name (default "native")
    """

    def __init__(self, circuit: Circuit, backend: str = "native") -> None:
        from .backends import get_backend
        from .backends.engine import EngineBackend
        from .simulators import StatevectorEngine

        self.circuit = circuit
        self.backend_name = backend
        self.backend = get_backend(backend)
        self.step_num: int = 0
        self._n = circuit.num_qubits

        # Use EngineBackend._create if available, else fall back to native SV engine
        if isinstance(self.backend, EngineBackend):
            self._engine = self.backend._create(self._n)
            self._apply = self.backend._apply_one
            self._get_sv = lambda eng, n: self.backend._get_statevector(eng, n)
        else:
            self._engine = StatevectorEngine(self._n)
            self._apply = lambda eng, name, q, p: eng.apply(name, q, p)
            self._get_sv = lambda eng, n: eng.state.copy()

        self._ops = list(circuit.ops)

    def step(self) -> StateVector:
        """Execute the next gate and return the current state vector.

        Returns:
            StateVector after applying the gate.
        """
        if self.step_num >= len(self._ops):
            raise StopIteration("Circuit execution complete")

        op = self._ops[self.step_num]
        self._apply(self._engine, op.name, list(op.qubits), op.params)
        self.step_num += 1

        sv = self._get_sv(self._engine, self._n)
        return StateVector(sv)

    def done(self) -> bool:
        """Check if all gates have been executed."""
        return self.step_num >= len(self._ops)

    def reset(self) -> None:
        """Reset execution to the beginning."""
        from .backends.engine import EngineBackend
        from .simulators import StatevectorEngine

        self.step_num = 0
        if isinstance(self.backend, EngineBackend):
            self._engine = self.backend._create(self._n)
        else:
            self._engine = StatevectorEngine(self._n)

    def __repr__(self) -> str:
        return (
            f"StepExecutor(backend={self.backend_name!r}, "
            f"step={self.step_num}/{len(self._ops)})"
        )
