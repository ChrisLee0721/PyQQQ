"""统一的结果对象。

qshow() 与所有算法模板都返回 Result，把两类输出收敛到同一个结构：

- 采样结果（kind="counts"）：运行电路 / Grover 搜索，含 counts 直方图
- 标量结果（kind="value"）：VQE 能量 / QAOA 割大小，含 value + metadata

用法：
    Result.from_counts({"00": 512, "11": 512}, shots=1024)
    Result.from_value(-2.236, params=[0.1, 0.2, ...])
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class Result:
    kind: str
    counts: Optional[Dict[str, int]] = None
    shots: int = 0
    value: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_counts(cls, counts, shots):
        """从采样直方图构造 Result。"""
        return cls(
            kind="counts",
            counts={str(k): int(v) for k, v in counts.items()},
            shots=int(shots),
        )

    @classmethod
    def from_value(cls, value, **metadata):
        """从标量结果构造 Result，附加信息放进 metadata。"""
        return cls(kind="value", value=float(value), metadata=dict(metadata))
