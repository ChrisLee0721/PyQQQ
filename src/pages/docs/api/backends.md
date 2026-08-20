# Backends

QuoNic supports 12 backends. Use `get_backend()` to get a backend instance, then call `run()` to execute a circuit.

::: quonic.backends.Backend
    options:
      show_source: true
      members: [name, methods, supports, run]

::: quonic.backends.get_backend
    options:
      show_source: true

::: quonic.backends.get_backend_for_method
    options:
      show_source: true

::: quonic.backends.available_backends
    options:
      show_source: true

## Engine Backend

The `EngineBackend` base class provides a generic framework for simulator backends. Subclasses implement `_create`, `_apply_one`, and `_sample`.

::: quonic.backends.engine.EngineBackend
    options:
      show_source: true
      members: [run, _create, _apply_one, _sample]

## Available Backends

| Backend | SDK | GPU | Noise | Classical Control |
|---------|-----|-----|-------|-------------------|
| `native` | numpy | ✗ | ✓ | ✓ |
| `qiskit` | Qiskit + Aer | ✓ | ✓ | ✓ |
| `cirq` | Cirq | ✗ | ✓ | ✓ |
| `pennylane` | PennyLane | ✗ | ✗ | ✗ |
| `qulacs` | Qulacs | ✓ | ✓ | ✓ |
| `tensorcircuit` | TensorCircuit | ✓ | ✓ | ✓ |
| `cudaq` | CUDA-Q | ✓ | ✓ | ✓ |
| `mindquantum` | MindQuantum | ✓ | ✓ | ✓ |
| `qpanda` | QPanda3 | ✓ | ✓ | ✓ |
| `cqlib` | CqLib | ✗ | ✗ | ✗ |
| `cupy` | CuPy | ✓ | ✓ | ✓ |
| `qi` | Quantum Inspire | ✗ | ✗ | ✗ |
