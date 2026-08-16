"""Shor 算法测试：经典连分数/阶提取 + 端到端分解。"""


from quonic.algorithms import shor
from quonic.algorithms.shor import (
    _factor_from_period,
    _modinv,
    _perfect_power_factor,
    _period_from_phase,
)

# ---------------------------------------------------------------------------
# 经典辅助函数（纯函数，快速）
# ---------------------------------------------------------------------------

def test_modinv():
    assert _modinv(7, 15) == 13   # 7·13 = 91 ≡ 1 (mod 15)
    assert _modinv(2, 5) == 3     # 2·3 = 6 ≡ 1 (mod 5)
    assert _modinv(3, 7) == 5     # 3·5 = 15 ≡ 1 (mod 7)
    assert _modinv(3, 6) is None  # 不互素，无逆元


def test_period_from_phase():
    # a=7 mod 15 的阶为 4；相位 1/4 -> j=16（t=6 位）
    assert _period_from_phase(16, 6, 7, 15) == 4
    # 相位 0 无法反解
    assert _period_from_phase(0, 6, 7, 15) is None


def test_factor_from_period():
    # 7 的阶为 4（偶数），7^{4/2}=7^2=49≡4 (mod 15)，gcd(4±1,15) 给出 3 或 5
    assert _factor_from_period(7, 4, 15) == 3
    # 奇数阶无法提取
    assert _factor_from_period(2, 3, 15) is None


def test_perfect_power_factor():
    assert _perfect_power_factor(9) == 3
    assert _perfect_power_factor(27) == 3
    assert _perfect_power_factor(15) is None


# ---------------------------------------------------------------------------
# 端到端分解
# ---------------------------------------------------------------------------

def test_shor_even():
    # 偶数直接返回 2
    assert shor(12).value == 2


def test_shor_perfect_power():
    # 完全幂直接返回底数
    assert shor(9).value == 3


def test_shor_15():
    # 经典例子：N=15，固定基 a=7（阶 4）。用小精度 t 加速（~3s）。
    result = shor(15, a=7, t=6, shots=256)
    assert result.value in (3, 5), f"分解结果 {result.value}"
    assert result.metadata["period"] == 4
