"""Quantum Inspire 真实硬件后端。

通过 qiskit-quantuminspire 把 QuoNic 电路编译成 cQASM 3.0，提交到
Quantum Inspire 的超导真机（Tuna-9 / Tuna-17）或 QX emulator
（10 量子比特云端模拟器，用于提交前验证）。

与模拟器后端（qiskit/cirq/pennylane/native）不同：
  - 真实硬件没有「模拟 method」之分，run() 忽略 method；
  - 硬件固有噪声，无法注入去极化噪声，run() 拒绝 noise；
  - 不支持经典控制流（cif/cwhile）：超导真机无中段测量反馈。

前置条件（一次性）：
    1. 安装依赖：   pip install 'qiskit-quantuminspire'
       （注意：qiskit-quantuminspire 0.18.x 要求 qiskit<2.4.0，当前 pyproject
        允许 qiskit>=1.0；若已装 2.5.x 需临时降级 qiskit==2.3.1）
    2. 登录：       qi login   # OAuth 设备流，浏览器授权
       token 存于 ~/.quantuminspire/config.json，不要手写或贴出。

用法：
    from quonic.backends import get_backend
    get_backend("qi").run(circuit, shots=1024)          # 真机 Tuna-9
    # 一键设备捷径（qshow 也可用 backend= 直达）：
    get_backend("tuna9").run(circuit, shots=1024)       # Tuna-9
    get_backend("tuna17").run(circuit, shots=1024)      # Tuna-17
    get_backend("qx").run(circuit, shots=1024)          # QX emulator（提交前验证）
    # 或显式构造：
    from quonic.backends.qi import QuantumInspireBackend
    QuantumInspireBackend("QX emulator").run(circuit, shots=1024)
"""

from ..result import Result
from .base import Backend
from .qiskit import QiskitBackend

# 设备别名 → QI 正式设备名。让 qshow(backend="tuna9") / get_backend("qx")
# 一键直达，不必记住 Tuna-9 / QX emulator 的精确拼写。
DEVICE_ALIASES = {
    "tuna9": "Tuna-9",
    "tuna17": "Tuna-17",
    "qx": "QX emulator",
}


def resolve_device(device):
    """把设备别名（tuna9 / tuna17 / qx）映射到 QI 正式设备名；未知名原样透传。"""
    if device is None:
        return None
    return DEVICE_ALIASES.get(str(device).lower(), device)


class QuantumInspireBackend(Backend):
    name = "qi"
    # 真实硬件无「模拟方法」之分；列出全部方法名仅供工具/文档参考，
    # 能力匹配由 supports() 覆盖，避免 get_backend_for_method 降级到 native。
    methods = frozenset(
        {"statevector", "stabilizer", "matrix_product_state", "density_matrix"}
    )

    def __init__(self, device=None):
        # device=None 时用真机 Tuna-9；也可传别名 tuna9/tuna17/qx 或
        # 正式设备名 "Tuna-9"/"Tuna-17"/"QX emulator"
        self.device = resolve_device(device)

    def supports(self, method):
        # 硬件后端不参与 method 能力匹配：任何 method 都直接跑硬件
        return True

    def run(self, circuit, shots=1024, noise=None, method="statevector"):
        if noise is not None:
            raise ValueError(
                "qi 后端运行真实硬件，无法注入噪声 noise；"
                "请用 qiskit 后端（Aer density_matrix）模拟去极化噪声"
            )
        self._check_supported(circuit)

        # 延迟导入：保证 `import quonic` 零开销，且未装依赖时给出清晰提示
        try:
            from qiskit import QuantumCircuit, transpile
            from qiskit_quantuminspire.qi_provider import QIProvider
        except ImportError as e:
            raise ImportError(
                "使用 qi 后端需要安装 qiskit-quantuminspire 并登录：\n"
                "    pip install 'qiskit-quantuminspire'\n"
                "    qi login\n"
                "（注意：qiskit-quantuminspire 0.18.x 要求 qiskit<2.4.0，"
                "若已装 2.5.x 需临时降级）"
            ) from e

        qc = QuantumCircuit(circuit.num_qubits, circuit.num_qubits)
        for op in circuit.ops:
            if op.name == "cmeasure":
                # 具名经典位无反馈语义时等价于普通测量，映射到该比特自己的经典位
                qc.measure(op.qubit, op.qubit)
            else:
                QiskitBackend._apply(qc, op)

        # 自动补全：未显式测量的量子比特最后统一测量
        for q in circuit.unmeasured_qubits():
            qc.measure(q, q)

        provider = QIProvider()
        backend = provider.get_backend(self.device or "Tuna-9")
        qc_compiled = transpile(qc, backend)

        job = backend.run(qc_compiled, shots=shots)
        # 真机需排队，超时放宽到 30 分钟；QX emulator 通常几秒返回
        result = job.result(timeout=1800)
        counts_hex = result.get_counts()
        counts = {
            _hex_to_bitstring(k, circuit.num_qubits): v
            for k, v in counts_hex.items()
        }
        return Result.from_counts(counts, shots)

    @staticmethod
    def _check_supported(circuit):
        for op in circuit.ops:
            if op.name == "cwhile":
                raise NotImplementedError(
                    "qi 后端不支持 cwhile（经典反馈循环）；"
                    "真实硬件无法逐 shot 动态回读，请用 native 后端"
                )
            if op.name == "cif":
                raise NotImplementedError(
                    "qi 后端不支持 cif（中段测量 + 经典分支）；"
                    "超导真机无中段测量反馈，请用 qiskit 或 native 后端"
                )


def _hex_to_bitstring(key, n_qubits):
    """Quantum Inspire 返回 counts 键为 0x.. 形式，还原成 MSB-first 比特串。

    QI 的原始 cQASM 结果串以 qubit 0 为最右位（标准二进制），与 QuoNic
    native / qiskit 后端约定一致（qubit 0 = LSB = 最右字符）。
    """
    key = str(key)
    if key.startswith("0x"):
        val = int(key, 16)
    else:  # 兜底：若已是二进制串
        val = int(key, 2)
    return format(val, f"0{n_qubits}b")
