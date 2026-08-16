"""后端注册表。"""

from .base import Backend
from .cirq import CirqBackend
from .native import NativeBackend
from .pennylane import PennyLaneBackend
from .qi import QuantumInspireBackend
from .qiskit import QiskitBackend

_REGISTRY = {
    "qiskit": QiskitBackend(),
    "cirq": CirqBackend(),
    "pennylane": PennyLaneBackend(),
    "native": NativeBackend(),
    "qi": QuantumInspireBackend(),
    # 真机 / 云端模拟器的一键设备捷径：qshow(backend="tuna9") 直达
    "tuna9": QuantumInspireBackend("tuna9"),
    "tuna17": QuantumInspireBackend("tuna17"),
    "qx": QuantumInspireBackend("qx"),
}


def _detect_available():
    """按优先级探测已安装的后端（qiskit -> cirq -> pennylane -> native）。"""
    import importlib.util

    candidates = (
        ("qiskit", ("qiskit", "qiskit_aer")),
        ("cirq", ("cirq",)),
        ("pennylane", ("pennylane",)),
    )
    for name, modules in candidates:
        if all(importlib.util.find_spec(m) is not None for m in modules):
            return name
    return "native"  # 兜底：自研引擎，仅需 numpy


def get_backend(name):
    if name == "auto":
        name = _detect_available()
    if name not in _REGISTRY:
        raise ValueError(
            f"未知的后端 '{name}'。当前可用：{', '.join(sorted(_REGISTRY))}"
        )
    return _REGISTRY[name]


def get_backend_for_method(name, method):
    """按方法解析后端：目标后端不支持该方法时降级到 native（自研引擎）。

    用户切到任何后端都能用到 stabilizer / MPS 等方法——能力匹配不上时
    统一回落到 QuoNic 自研引擎，而不是硬套 statevector。
    """
    be = get_backend(name)
    if be.supports(method):
        return be
    native = _REGISTRY["native"]
    if native.supports(method):
        return native
    raise ValueError(f"没有任何后端支持方法 '{method}'")


def available_backends():
    return sorted(_REGISTRY)


__all__ = [
    "Backend",
    "get_backend",
    "get_backend_for_method",
    "available_backends",
]
