"""后端注册表。"""

from .base import Backend
from .cirq import CirqBackend
from .pennylane import PennyLaneBackend
from .qiskit import QiskitBackend

_REGISTRY = {
    "qiskit": QiskitBackend(),
    "cirq": CirqBackend(),
    "pennylane": PennyLaneBackend(),
}


def get_backend(name):
    if name not in _REGISTRY:
        raise ValueError(
            f"未知的后端 '{name}'。当前可用：{', '.join(sorted(_REGISTRY))}"
        )
    return _REGISTRY[name]


def available_backends():
    return sorted(_REGISTRY)


__all__ = ["Backend", "get_backend", "available_backends"]
