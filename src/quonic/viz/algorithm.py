"""算法相关可视化：VQE/QAOA 能量收敛图、Grover 迭代振幅图。"""

import math

from ..result import Result
from ._mpl import _plt, finalize

# ---------------------------------------------------------------------------
# 10. 能量收敛图
# ---------------------------------------------------------------------------

def _as_energies(data):
    if isinstance(data, Result):
        history = data.metadata.get("history")
        if history is None:
            raise ValueError(
                "Result 里没有收敛轨迹。请用 vqe(..., record_history=True) 或 "
                "qaoa_maxcut(..., record_history=True) 运行，或直接传入能量列表。"
            )
        return list(history)
    return list(data)


def plot_energy_convergence(energies, ax=None, show=False, save=None, title=None):
    """画变分算法（VQE/QAOA）的能量随优化迭代次数的收敛曲线。

    参数：
        energies: 能量列表，或带 metadata["history"] 的 Result。
        ax / show / save / title: 同 plot_circuit。

    返回：matplotlib Axes。
    """
    plt = _plt()
    ys = _as_energies(energies)

    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 4))
    else:
        fig = ax.figure

    ax.plot(range(len(ys)), ys, marker="o", markersize=3, color="#4C72B0")
    ax.set_xlabel("优化迭代")
    ax.set_ylabel("能量")
    ax.grid(True, alpha=0.3)
    return finalize(fig, ax, show, save, title)


# ---------------------------------------------------------------------------
# 11. Grover 迭代振幅图
# ---------------------------------------------------------------------------

def _apply_oracle(eng, marked):
    n = eng.n
    for q in range(n):
        if marked[n - 1 - q] == "0":
            eng.apply("x", (q,))
    eng.apply("mcz", tuple(range(n)))
    for q in range(n):
        if marked[n - 1 - q] == "0":
            eng.apply("x", (q,))


def _apply_diffusion(eng):
    n = eng.n
    for q in range(n):
        eng.apply("h", (q,))
    for q in range(n):
        eng.apply("x", (q,))
    eng.apply("mcz", tuple(range(n)))
    for q in range(n):
        eng.apply("x", (q,))
    for q in range(n):
        eng.apply("h", (q,))


def _target_prob(eng, marked):
    idx = int(marked, 2)
    return float(abs(eng.state[idx]) ** 2)


def plot_grover_amplitudes(n_qubits, marked, iterations=None, ax=None,
                           show=False, save=None, title=None):
    """画 Grover 搜索中目标态概率随迭代次数的变化（自研引擎模拟，无后端依赖）。

    参数：
        n_qubits: 量子比特数。
        marked: 要标记的目标比特串（如 "11"）。
        iterations: 迭代次数，默认 floor(π/4 · √(2^n))。
        ax / show / save / title: 同 plot_circuit。

    返回：matplotlib Axes。
    """
    from ..simulators import StatevectorEngine

    plt = _plt()
    marked = str(marked)
    if len(marked) != n_qubits or any(ch not in "01" for ch in marked):
        raise ValueError(f"marked 需为长度 {n_qubits} 的 0/1 比特串，收到 {marked!r}")
    if iterations is None:
        iterations = int(math.pi / 4 * math.sqrt(2 ** n_qubits))

    eng = StatevectorEngine(n_qubits)
    for q in range(n_qubits):
        eng.apply("h", (q,))
    probs = [_target_prob(eng, marked)]
    for _ in range(iterations):
        _apply_oracle(eng, marked)
        _apply_diffusion(eng)
        probs.append(_target_prob(eng, marked))

    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 4))
    else:
        fig = ax.figure

    ax.plot(range(len(probs)), probs, marker="o", color="#4C72B0")
    ax.set_xlabel("迭代次数")
    ax.set_ylabel(f"目标态 |{marked}> 概率")
    ax.set_ylim(0, 1.02)
    ax.grid(True, alpha=0.3)
    return finalize(fig, ax, show, save, title)


# ---------------------------------------------------------------------------
# 问题图（QAOA MaxCut）
# ---------------------------------------------------------------------------

def plot_problem_graph(edges, n_qubits=None, partition=None, ax=None, show=False,
                       save=None, title=None):
    """画优化问题图（如 MaxCut 的顶点与边），可选按割着色。

    参数：
        edges: 边列表 [(i, j), ...]。
        n_qubits: 顶点数；None 则取边的最大顶点 + 1。
        partition: 可选，每个顶点的割归属——dict {顶点: 0/1} 或长度 n 的 0/1 序列。
            给定后跨割的边与两侧顶点用不同颜色标出。
        ax / show / save / title: 同 plot_circuit。

    返回：matplotlib Axes。
    """
    from matplotlib.patches import Circle

    plt = _plt()
    edges = [(int(u), int(v)) for u, v in edges]
    if n_qubits is None:
        n_qubits = max((max(u, v) for u, v in edges), default=-1) + 1

    side = None
    if partition is not None:
        if isinstance(partition, dict):
            side = {int(k): int(v) for k, v in partition.items()}
        else:
            side = {q: int(partition[q]) for q in range(n_qubits)}

    pos = {}
    for q in range(n_qubits):
        ang = 2 * math.pi * q / n_qubits - math.pi / 2
        pos[q] = (math.cos(ang), math.sin(ang))

    if ax is None:
        fig, ax = plt.subplots(figsize=(5, 5))
    else:
        fig = ax.figure

    for u, v in edges:
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        is_cut = side is not None and side.get(u) != side.get(v)
        ax.plot([x1, x2], [y1, y2], color="#DD8452" if is_cut else "#4C72B0",
                lw=2.5 if is_cut else 1.5, zorder=1)

    for q in range(n_qubits):
        x, y = pos[q]
        color = "#4C72B0"
        if side is not None:
            color = "#4C72B0" if side[q] == 0 else "#DD8452"
        ax.add_patch(Circle((x, y), 0.08, facecolor=color, edgecolor="black", zorder=2))
        ax.text(x, y + 0.14, str(q), ha="center", va="bottom", fontsize=9)

    pad = 0.25
    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    ax.set_xlim(min(xs) - pad, max(xs) + pad)
    ax.set_ylim(min(ys) - pad, max(ys) + pad)
    ax.set_aspect("equal")
    ax.axis("off")
    return finalize(fig, ax, show, save, title)


# ---------------------------------------------------------------------------
# 哈密顿量可视化
# ---------------------------------------------------------------------------

_OP_COLORS = {"I": "#EEEEEE", "X": "#4C72B0", "Y": "#55A868", "Z": "#C44E52"}


def plot_hamiltonian(hamiltonian, n_qubits=None, ax=None, show=False, save=None, title=None):
    """画泡利项哈密顿量：左 = 各项系数柱状图，右 = 算符结构热力图。

    参数：
        hamiltonian: 列表 [(系数, 泡利串), ...]，泡利串长度 = n_qubits。
        n_qubits: 量子比特数；None 则取第一个泡利串的长度。
        ax: 可选，长度为 2 的 Axes 序列（[系数, 算符结构]）；不传则新建。
        show / save / title: 同 plot_circuit。

    返回：长度为 2 的 Axes 序列 [ax_coeff, ax_ops]。
    """
    import numpy as np
    from matplotlib.colors import ListedColormap

    plt = _plt()
    coeffs = [float(c) for c, _ in hamiltonian]
    paulis = [p for _, p in hamiltonian]
    if n_qubits is None:
        n_qubits = len(paulis[0]) if paulis else 0
    paulis = [p.ljust(n_qubits, "I") for p in paulis]

    op_map = {"I": 0, "X": 1, "Y": 2, "Z": 3}
    grid = np.zeros((len(paulis), n_qubits), dtype=int)
    for i, p in enumerate(paulis):
        for j, ch in enumerate(p):
            grid[i, j] = op_map.get(ch, 0)

    if ax is None:
        fig, axes = plt.subplots(1, 2, figsize=(10, 4),
                                 gridspec_kw={"width_ratios": [1, 1.5]})
    else:
        axes = ax
        fig = axes[0].figure

    xs = list(range(len(coeffs)))
    colors = ["#4C72B0" if c >= 0 else "#C44E52" for c in coeffs]
    axes[0].bar(xs, coeffs, color=colors)
    axes[0].set_xticks(xs)
    axes[0].set_xticklabels(paulis)
    axes[0].axhline(0, color="0.5", lw=0.8)
    axes[0].set_xlabel("泡利项")
    axes[0].set_ylabel("系数")
    axes[0].set_title("系数")
    for s in ("top", "right"):
        axes[0].spines[s].set_visible(False)

    cmap = ListedColormap([_OP_COLORS[k] for k in ("I", "X", "Y", "Z")])
    im = axes[1].imshow(grid, cmap=cmap, aspect="auto", vmin=0, vmax=3)
    axes[1].set_xticks(range(n_qubits))
    axes[1].set_xticklabels([f"q{q}" for q in range(n_qubits)])
    axes[1].set_yticks(range(len(paulis)))
    axes[1].set_yticklabels(paulis)
    axes[1].set_xlabel("量子比特")
    axes[1].set_title("算符结构")
    for i in range(len(paulis)):
        for j in range(n_qubits):
            axes[1].text(j, i, paulis[i][j], ha="center", va="center",
                         fontsize=8, color="0.15")
    cbar = fig.colorbar(im, ax=axes[1], ticks=[0, 1, 2, 3], fraction=0.046, pad=0.04)
    cbar.ax.set_yticklabels(["I", "X", "Y", "Z"])

    if title is not None:
        fig.suptitle(title)
    if save:
        fig.savefig(save, bbox_inches="tight", dpi=120)
    if show:
        plt.show()
    return axes
