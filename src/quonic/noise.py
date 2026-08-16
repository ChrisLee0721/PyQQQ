"""去极化（depolarizing）噪声模型。

用法：
    from quonic import qshow, depolarizing, NoiseModel

    qshow(backend="qiskit", shots=1024, noise=0.05)          # 每个门 5% 去极化
    qshow(noise=depolarizing(0.05))                          # 等价
    qshow(noise=NoiseModel(single=0.01, double=0.05))        # 单/双比特门分开
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class NoiseModel:
    """去极化噪声模型。

    参数：
        single: 每个单比特门之后施加的去极化概率 p。
        double: 每个两比特门之后施加的去极化概率 p。
    """

    single: float = 0.0
    double: float = 0.0

    def __post_init__(self):
        for name in ("single", "double"):
            p = getattr(self, name)
            if not 0.0 <= p <= 1.0:
                raise ValueError(f"去极化概率 {name} 需在 [0, 1] 内，收到 {p}")

    @property
    def enabled(self):
        return self.single > 0.0 or self.double > 0.0


def depolarizing(p):
    """构造单/双比特去极化概率均为 p 的噪声模型。"""
    return NoiseModel(single=float(p), double=float(p))


def resolve_noise(noise):
    """把 noise 参数统一成 NoiseModel（None 表示无噪声）。"""
    if noise is None:
        return NoiseModel()
    if isinstance(noise, NoiseModel):
        return noise
    if isinstance(noise, (int, float)):
        return depolarizing(noise)
    raise TypeError(
        "noise 参数必须是 NoiseModel、一个 [0,1] 内的概率数值，或 None"
    )
