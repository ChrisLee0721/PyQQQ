"""电路相关可视化：门序列图、耦合拓扑图、活跃度热力图、态向量图。"""

import math

from ..ir import Circuit
from ._mpl import _plt, finalize

# ---------------------------------------------------------------------------
# 1. 门序列电路图
# ---------------------------------------------------------------------------

def _gate_label(op):
    if op.name == "measure":
        return "M"
    if op.params:
        p = ", ".join(f"{x:.3g}" for x in op.params)
        return f"{op.name}({p})"
    return op.name


def _draw_box(ax, x, y, label):
    from matplotlib.patches import Rectangle

    ax.add_patch(
        Rectangle(
            (x - 0.4, y - 0.3),
            0.8,
            0.6,
            facecolor="white",
            edgecolor="black",
            zorder=3,
        )
    )
    ax.text(x, y, label, ha="center", va="center", fontsize=8, zorder=4)


def _draw_target(ax, x, y):
    """⊕ 目标符号（X 基目标端）。"""
    from matplotlib.patches import Circle

    ax.add_patch(
        Circle((x, y), 0.26, facecolor="white", edgecolor="black", zorder=3)
    )
    ax.plot([x - 0.16, x + 0.16], [y, y], color="black", lw=1.4, zorder=4)
    ax.plot([x, x], [y - 0.16, y + 0.16], color="black", lw=1.4, zorder=4)


def plot_circuit(circuit, ax=None, show=False, save=None, title=None):
    """画门序列电路图：每行一个量子比特，门按时间从左到右排布。

    参数：
        circuit: Circuit 对象。
        ax: 可选的 matplotlib Axes；不传则新建。
        show / save / title: 是否显示、保存路径、标题。

    返回：matplotlib Axes。
    """
    plt = _plt()
    n = circuit.num_qubits
    m = len(circuit.ops)

    if ax is None:
        fig, ax = plt.subplots(
            figsize=(max(6.0, m * 0.55 + 1.0), max(1.8, n * 0.55))
        )
    else:
        fig = ax.figure

    for q in range(n):
        ax.plot([-0.5, m - 0.5], [q, q], color="0.35", lw=1.0, zorder=1)

    for col, op in enumerate(circuit.ops):
        qs = list(op.qubits)
        if len(qs) == 1:
            _draw_box(ax, col, qs[0], _gate_label(op))
            continue
        ymin, ymax = min(qs), max(qs)
        ax.plot([col, col], [ymin, ymax], color="0.35", lw=1.0, zorder=2)
        target = qs[-1]
        for q in qs:
            if q == target:
                if op.name in ("cx", "ccx"):
                    _draw_target(ax, col, q)
                else:
                    _draw_box(ax, col, q, _gate_label(op))
            else:
                ax.plot(col, q, "ko", ms=5, zorder=3)

    ax.set_xlim(-0.8, m - 0.2)
    ax.set_ylim(-0.6, n - 0.4)
    ax.invert_yaxis()
    ax.set_yticks(range(n))
    ax.set_yticklabels([f"q{q}" for q in range(n)])
    ax.set_xticks([])
    ax.set_ylabel("量子比特")
    for s in ("top", "right", "bottom"):
        ax.spines[s].set_visible(False)
    return finalize(fig, ax, show, save, title)


# ---------------------------------------------------------------------------
# 3. 耦合拓扑图
# ---------------------------------------------------------------------------

def _layout_positions(coupling_map):
    """线型拓扑走直线布局，其余走环形布局（无 networkx 依赖）。"""
    n = coupling_map.n
    if coupling_map.edges() == [(i, i + 1) for i in range(n - 1)]:
        return {q: (q, 0.0) for q in range(n)}
    pos = {}
    for q in range(n):
        ang = 2 * math.pi * q / n - math.pi / 2
        pos[q] = (math.cos(ang), math.sin(ang))
    return pos


def plot_coupling_map(coupling_map, ax=None, show=False, save=None, title=None):
    """画耦合拓扑图：节点是量子比特，边是允许的两比特门连接。

    参数：
        coupling_map: CouplingMap 对象。
        ax / show / save / title: 同 plot_circuit。

    返回：matplotlib Axes。
    """
    from matplotlib.patches import Circle

    plt = _plt()
    n = coupling_map.n
    pos = _layout_positions(coupling_map)

    if ax is None:
        fig, ax = plt.subplots(figsize=(5, 5))
    else:
        fig = ax.figure

    for u, v in coupling_map.edges():
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        ax.plot([x1, x2], [y1, y2], color="0.6", lw=1.5, zorder=1)

    for q in range(n):
        x, y = pos[q]
        ax.add_patch(
            Circle((x, y), 0.07, facecolor="#4C72B0", edgecolor="black", zorder=2)
        )
        ax.text(x, y + 0.1, str(q), ha="center", va="bottom", fontsize=9)

    pad = 0.25
    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    ax.set_xlim(min(xs) - pad, max(xs) + pad)
    ax.set_ylim(min(ys) - pad, max(ys) + pad)
    ax.set_aspect("equal")
    ax.axis("off")
    return finalize(fig, ax, show, save, title)


# ---------------------------------------------------------------------------
# 8. 量子比特活跃度热力图
# ---------------------------------------------------------------------------

def plot_qubit_activity(circuit, ax=None, show=False, save=None, title=None):
    """画量子比特活跃度热力图：行 = 量子比特，列 = 门序列，着色表示被触及。

    参数：
        circuit: Circuit 对象。
        ax / show / save / title: 同 plot_circuit。

    返回：matplotlib Axes。
    """
    import numpy as np

    plt = _plt()
    n = circuit.num_qubits
    ops = [op for op in circuit.ops if op.name != "measure"]
    grid = np.zeros((n, len(ops)))
    for col, op in enumerate(ops):
        for q in op.qubits:
            grid[q, col] = 1.0

    if ax is None:
        fig, ax = plt.subplots(figsize=(max(6.0, len(ops) * 0.3 + 1.0), max(2.0, n * 0.4)))
    else:
        fig = ax.figure

    im = ax.imshow(grid, aspect="auto", cmap="Blues", interpolation="nearest", vmin=0, vmax=1)
    ax.set_yticks(range(n))
    ax.set_yticklabels([f"q{q}" for q in range(n)])
    ax.set_xlabel("门序列（时间）")
    ax.set_ylabel("量子比特")
    fig.colorbar(im, ax=ax, label="活跃")
    return finalize(fig, ax, show, save, title)


# ---------------------------------------------------------------------------
# 12. 态向量可视化
# ---------------------------------------------------------------------------

def _to_statevector(state):
    import numpy as np

    from ..simulators import StatevectorEngine

    if isinstance(state, StatevectorEngine):
        return np.asarray(state.state)
    if isinstance(state, Circuit):
        eng = StatevectorEngine(state.num_qubits)
        for op in state.ops:
            eng.apply(op.name, list(op.qubits), op.params)
        return np.asarray(eng.state)
    return np.asarray(state)


def plot_statevector(state, ax=None, show=False, save=None, title=None, top_k=32):
    """画态向量的复振幅：上图幅值、下图相位（按基态索引）。

    参数：
        state: numpy 复数数组 / StatevectorEngine / Circuit。
        ax: None（新建双子图）或长度为 2 的 Axes 序列。
        show / save / title: 同 plot_circuit。
        top_k: 只显示振幅最大的前 top_k 个基态（按基态索引排序）；None 表示
            全部显示。大规模态向量（如 10+ 比特）默认只画前 32 个，避免
            1024+ 根柱状图挤爆。

    返回：长度为 2 的 Axes 序列 [ax_amp, ax_phase]。
    """
    import numpy as np

    plt = _plt()
    sv = _to_statevector(state)
    sv = np.asarray(sv, dtype=complex)
    size = len(sv)
    n = int(round(math.log2(size)))

    truncated = top_k is not None and size > top_k
    if truncated:
        idx = np.argsort(np.abs(sv))[::-1][:top_k]
        shown = np.sort(idx)
    else:
        shown = np.arange(size)

    labels = [f"|{format(i, '0%db' % n)}>" for i in shown]
    amps = np.abs(sv[shown])
    phases = np.angle(sv[shown])
    k = len(shown)

    if ax is None:
        fig, axes = plt.subplots(
            2, 1, figsize=(max(6.0, k * 0.3), 6.0), sharex=True
        )
    else:
        axes = ax
        fig = axes[0].figure

    axes[0].bar(range(k), amps, color="#4C72B0")
    axes[0].set_ylabel("|振幅|")
    axes[1].bar(range(k), phases, color="#DD8452")
    axes[1].set_ylabel("相位 (rad)")
    axes[1].set_xticks(range(k))
    axes[1].set_xticklabels(labels, rotation=90, fontsize=7)
    if title is not None:
        axes[0].set_title(title)
    elif truncated:
        axes[0].set_title(f"态向量（振幅最大的前 {top_k} 个基态，共 {size} 个）")
    if save:
        fig.savefig(save, bbox_inches="tight", dpi=120)
    if show:
        plt.show()
    return axes
