"""门可视化：单个门的酉矩阵实/虚双面板热力图。"""

import math

from ..gates import Gate, resolve
from ..ir import GateOperation
from ._mpl import _plt


def _gate_unitary(name, qubits, params):
    """用自研态矢量引擎逐列构造门的酉矩阵（列 = 基态经过门后的输出）。"""
    import numpy as np

    from ..simulators import StatevectorEngine

    n = max(qubits) + 1 if qubits else 1
    dim = 2 ** n
    u = np.zeros((dim, dim), dtype=complex)
    for col in range(dim):
        eng = StatevectorEngine(n)
        eng.state[col] = 1.0
        eng.apply(name, qubits, params)
        u[:, col] = eng.state
    return u


def _resolve_gate(gate):
    """把输入统一成 (name, qubits, params)。"""
    if isinstance(gate, GateOperation):
        return gate.name, list(gate.qubits), gate.params
    if isinstance(gate, Gate):
        name = gate.name
        qubits = list(range(max(1, gate.num_qubits)))
        return name, qubits, gate.params
    if isinstance(gate, str):
        g = resolve(gate)
        return g.name, list(range(max(1, g.num_qubits))), g.params
    raise TypeError("plot_gate_matrix 需要 Gate / GateOperation / 门名字符串")


def plot_gate_matrix(gate, ax=None, show=False, save=None, title=None):
    """画单个门的酉矩阵实部/虚部双面板热力图。

    参数：
        gate: Gate 对象 / GateOperation / 门名字符串（如 "cx"、"h"、"mcz"）。
        ax: 可选，长度为 2 的 Axes 序列（[实部, 虚部]）；不传则新建。
        show / save / title: 同 plot_circuit。

    返回：长度为 2 的 Axes 序列 [ax_real, ax_imag]。
    """
    import numpy as np

    plt = _plt()
    name, qubits, params = _resolve_gate(gate)
    if name == "measure":
        raise ValueError("测量门没有酉矩阵")

    u = _gate_unitary(name, qubits, params)
    n = int(round(math.log2(u.shape[0])))
    labels = [f"|{format(i, '0%db' % n)}>" for i in range(u.shape[0])]

    if ax is None:
        fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    else:
        axes = ax
        fig = axes[0].figure

    vmax = max(float(np.max(np.abs(u.real))), float(np.max(np.abs(u.imag))), 1e-12)

    im0 = axes[0].imshow(u.real, cmap="RdBu_r", vmin=-vmax, vmax=vmax)
    axes[0].set_title(f"Re({name})")
    im1 = axes[1].imshow(u.imag, cmap="RdBu_r", vmin=-vmax, vmax=vmax)
    axes[1].set_title(f"Im({name})")
    for a in axes:
        a.set_xticks(range(u.shape[0]))
        a.set_yticks(range(u.shape[0]))
        a.set_xticklabels(labels, rotation=90, fontsize=6)
        a.set_yticklabels(labels, fontsize=6)
    fig.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)
    fig.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)
    if title is not None:
        fig.suptitle(title)
    if save:
        fig.savefig(save, bbox_inches="tight", dpi=120)
    if show:
        plt.show()
    return axes
