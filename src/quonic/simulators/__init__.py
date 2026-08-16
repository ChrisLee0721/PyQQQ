"""自研模拟引擎（朴素版）：不绑定任何后端，仅需 numpy。

四个引擎对应四种模拟方法，供 native 后端与调度降级使用：

- StatevectorEngine   —— 2^n 复振幅，精确（含非 Clifford 门）
- StabilizerEngine    —— Clifford tableau，多项式级（仅基础 Clifford 门集）
- MPSEngine           —— 矩阵乘积态，低纠缠电路突破 2^n 内存墙
- DensityMatrixEngine —— 密度矩阵，支持去极化噪声
"""

from ._density import DensityMatrixEngine
from ._mps import MPSEngine
from ._stabilizer import StabilizerEngine
from ._statevector import StatevectorEngine

__all__ = [
    "StatevectorEngine",
    "StabilizerEngine",
    "MPSEngine",
    "DensityMatrixEngine",
]
