"""门的 numpy 矩阵构造（供自研引擎复用）。

约定：
- qubit 0 是最低位（bitstring 最右侧），与三个采样后端一致。
- 单比特矩阵 matrix[out, in]。
- 多比特门（cx/ccx/cz/cp/mcz）在各引擎里用「对角相位 + H」技巧实现，
  因此这里只提供单比特矩阵，避免多比特矩阵的指标顺序歧义。
"""

import numpy as np

_SQRT_HALF = 1.0 / np.sqrt(2.0)

_I = np.eye(2, dtype=complex)
_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
_Y = np.array([[0.0, -1j], [1j, 0.0]], dtype=complex)
_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
_H = np.array([[1.0, 1.0], [1.0, -1.0]], dtype=complex) * _SQRT_HALF


def rotation(axis, theta):
    c = np.cos(theta / 2.0)
    s = np.sin(theta / 2.0)
    if axis == "x":
        return np.array([[c, -1j * s], [-1j * s, c]], dtype=complex)
    if axis == "y":
        return np.array([[c, -s], [s, c]], dtype=complex)
    if axis == "z":
        return np.array(
            [[np.exp(-1j * theta / 2.0), 0.0], [0.0, np.exp(1j * theta / 2.0)]],
            dtype=complex,
        )
    raise ValueError(f"未知旋转轴 '{axis}'")


def phase_shift(theta):
    """相位门 P(θ) = diag(1, e^{iθ})。"""
    return np.array([[1.0, 0.0], [0.0, np.exp(1j * theta)]], dtype=complex)


def single(name, params=()):
    """返回单比特门矩阵；name 为小写门名。"""
    name = name.lower()
    if name == "i":
        return _I
    if name == "h":
        return _H
    if name == "x":
        return _X
    if name == "y":
        return _Y
    if name == "z":
        return _Z
    if name == "rx":
        return rotation("x", params[0])
    if name == "ry":
        return rotation("y", params[0])
    if name == "rz":
        return rotation("z", params[0])
    if name == "p":
        return phase_shift(params[0])
    raise ValueError(f"自研引擎暂不支持单比特门 '{name}'")


# 单比特 Clifford 门集（stabilizer 可用）
SINGLE_GATES = {"i", "h", "x", "y", "z", "rx", "ry", "rz", "p"}
