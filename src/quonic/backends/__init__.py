"""Backend registry."""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from .._i18n import tr
from .base import Backend
from .cirq import CirqBackend
from .cqlib import CqlibBackend
from .cudaq import CudaQBackend
from .engine import EngineBackend
from .mindquantum import MindQuantumBackend
from .native import NativeBackend
from .pennylane import PennyLaneBackend
from .qi import QuantumInspireBackend
from .qiskit import QiskitBackend
from .qpanda import QPandaBackend
from .qulacs import QulacsBackend
from .tensorcircuit import TensorCircuitBackend

# Engine registry: the backend argument only recognizes these five engine names
# (local simulators plus the qi cloud entry point). Specific real-hardware devices
# (Tuna-9 / Tuna-17 / QX emulator) are selected via the device argument, not
# registered here as independent backend names.
_REGISTRY: Dict[str, Backend] = {
    "qiskit": QiskitBackend(),
    "cirq": CirqBackend(),
    "pennylane": PennyLaneBackend(),
    "native": NativeBackend(),
    "qi": QuantumInspireBackend(),
    "qulacs": QulacsBackend(),
    "tensorcircuit": TensorCircuitBackend(),
    "cudaq": CudaQBackend(),
    "mindquantum": MindQuantumBackend(),
    "qpanda": QPandaBackend(),
    "cqlib": CqlibBackend(),
}

# Backward-compatible aliases for the legacy one-shot device shortcuts: backend="tuna9" is equivalent to backend="qi", device="tuna9".
_BACKEND_ALIASES: Dict[str, Tuple[str, str]] = {
    "tuna9": ("qi", "tuna9"),
    "tuna17": ("qi", "tuna17"),
    "qx": ("qi", "qx"),
}


def resolve_target(
    backend: str, device: Optional[str] = None
) -> Tuple[str, Optional[str]]:
    """Normalize (backend, device) into (engine name, device name).

    - If backend is a legacy device shortcut (tuna9/tuna17/qx), translate it into ("qi", device alias);
    - device is only meaningful when backend="qi"; passing device to any other engine raises a Chinese error;
    - when backend="auto", device must not be passed (auto only probes local simulators).
    """
    if backend in _BACKEND_ALIASES:
        alias_engine, alias_device = _BACKEND_ALIASES[backend]
        if device is not None and str(device).lower() != alias_device:
            raise ValueError(
                tr(
                    "err.device_alias_conflict",
                    backend=backend,
                    alias_device=alias_device,
                    device=device,
                )
            )
        return alias_engine, alias_device
    if device is not None and backend != "qi":
        raise ValueError(tr("err.device_only_qi", backend=backend))
    return backend, device


def _detect_available() -> str:
    """Probe installed backends in priority order (qiskit -> cirq -> pennylane -> native)."""
    import importlib.util

    candidates = (
        ("qiskit", ("qiskit", "qiskit_aer")),
        ("cirq", ("cirq",)),
        ("pennylane", ("pennylane",)),
    )
    for name, modules in candidates:
        if all(importlib.util.find_spec(m) is not None for m in modules):
            return name
    return "native"  # Fallback: the in-house engine, which only needs numpy


def get_backend(name: str, device: Optional[str] = None) -> Backend:
    """Get a backend by name. Supports legacy device-shortcut aliases (returns a qi instance carrying the device)."""
    name, device = resolve_target(name, device)
    if name == "auto":
        name = _detect_available()
    if name not in _REGISTRY:
        raise ValueError(
            tr("err.unknown_backend", name=name, engines=", ".join(sorted(_REGISTRY)))
        )
    if device is not None:
        # resolve_target already guarantees device is only valid for qi, so this is always qi
        return QuantumInspireBackend(device)
    return _REGISTRY[name]


def get_backend_for_method(
    name: str, method: str, device: Optional[str] = None
) -> Backend:
    """Resolve a backend by method: fall back to native (the in-house engine) when the target backend does not support the method.

    Users can use stabilizer / MPS and other methods on any backend — when the
    capabilities do not match, uniformly fall back to the QuoNic in-house engine
    rather than forcing statevector.
    """
    be = get_backend(name, device=device)
    if be.supports(method):
        return be
    native = _REGISTRY["native"]
    if native.supports(method):
        return native
    raise ValueError(tr("err.no_method_support", method=method))


def available_backends() -> List[str]:
    return sorted(_REGISTRY)


__all__ = [
    "Backend",
    "EngineBackend",
    "get_backend",
    "get_backend_for_method",
    "available_backends",
    "resolve_target",
]
