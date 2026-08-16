"""噪声成本可视化：去极化噪声下密度矩阵模拟的耗时热力图、噪声叠加电路图。"""

import time

from ._mpl import _plt, finalize
from .circuit import _draw_box, _draw_target, _gate_label


def _noisy_ghz_time(n, p, repeats):
    """在密度矩阵引擎上跑 n 比特 GHZ（H + CX 链）并施加去极化噪声，返回最短耗时。"""
    from ..noise import depolarizing
    from ..simulators import DensityMatrixEngine

    best = None
    for _ in range(repeats):
        eng = DensityMatrixEngine(n, noise=depolarizing(p))
        t0 = time.perf_counter()
        eng.apply("h", (0,))
        for i in range(n - 1):
            eng.apply("cx", (i, i + 1))
        dt = time.perf_counter() - t0
        if best is None or dt < best:
            best = dt
    return best


def plot_noise_heatmap(n_values=(2, 4, 6, 8, 10), noise_rates=(0.0, 0.01, 0.05, 0.1, 0.5),
                       budget=1.0, repeats=1, ax=None, show=False, save=None, title=None):
    """画去极化噪声下密度矩阵模拟的耗时热力图。

    横轴为比特数 n，纵轴为去极化概率 p，色块为 log10(耗时/秒)。耗时主要随 n
    按 4^n 增长（密度矩阵的内存/时间墙）；p 本身几乎不影响耗时——去极化信道对
    任意 p>0 都做同样多的矩阵运算，只有 p=0（关闭噪声）才跳过噪声层。

    超过 budget 秒的格子会被红框标出，表示该 (p, n) 组合在此预算内不可行。

    参数：
        n_values: 比特数序列（密度矩阵为 4^n 成本，建议 ≤ 10）。
        noise_rates: 去极化概率序列（0.0 表示无噪声，仍用密度矩阵引擎跑）。
        budget: 耗时预算（秒），超过的格子标记为不可行。
        repeats: 每个格子重复次数，取最小值（压计时抖动）。
        ax / show / save / title: 同 plot_circuit。

    返回：matplotlib Axes。
    """
    import numpy as np

    plt = _plt()
    grid = []
    for p in noise_rates:
        row = [_noisy_ghz_time(n, p, repeats) for n in n_values]
        grid.append(row)

    times = np.array(grid)
    data = np.log10(times)
    infeasible = times > budget

    if ax is None:
        fig, ax = plt.subplots(
            figsize=(max(6.0, len(n_values) * 0.9 + 1.2),
                     max(3.0, len(noise_rates) * 0.7 + 1.0))
        )
    else:
        fig = ax.figure

    vmin = float(np.min(data))
    vmax = float(np.max(data))
    if vmax - vmin < 1e-12:
        vmax = vmin + 1.0

    im = ax.imshow(data, cmap="viridis", aspect="auto", vmin=vmin, vmax=vmax)

    from matplotlib.patches import Rectangle

    for i in range(len(noise_rates)):
        for j in range(len(n_values)):
            t = times[i][j]
            label = f"{t:.3g}"
            if infeasible[i][j]:
                ax.add_patch(
                    Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False,
                              edgecolor="red", lw=2, zorder=3)
                )
                ax.text(j, i, label, ha="center", va="center", fontsize=8,
                        color="red", fontweight="bold", zorder=4)
            else:
                lum = (data[i][j] - vmin) / (vmax - vmin)
                color = "white" if lum > 0.5 else "black"
                ax.text(j, i, label, ha="center", va="center", fontsize=8,
                        color=color, zorder=4)

    ax.set_xticks(range(len(n_values)))
    ax.set_xticklabels(n_values)
    ax.set_yticks(range(len(noise_rates)))
    ax.set_yticklabels(noise_rates)
    ax.set_xlabel("量子比特数 n")
    ax.set_ylabel("去极化概率 p")
    fig.colorbar(im, ax=ax, label="log10(耗时/s)")
    fig.subplots_adjust(bottom=0.18)
    fig.text(
        0.5, 0.02,
        f"红框 = 超过预算 {budget}s；耗时主要由 n 决定（4^n 墙），p 几乎不影响",
        ha="center", va="bottom", fontsize=8, color="0.4",
    )
    return finalize(fig, ax, show, save, title)


def plot_noisy_circuit(circuit, noise=None, ax=None, show=False, save=None, title=None):
    """在电路图上叠加噪声强度：每个门的背景色 = 它承受的去极化概率。

    单比特门用 noise.single、两比特及以上门用 noise.double 着色（YlOrRd
    色标），测量门不着色。白色门盒/目标符号画在色带之上，保证可读。

    参数：
        circuit: Circuit 对象。
        noise: NoiseModel / 概率数值 / None（None 表示无噪声，全部零强度）。
        ax / show / save / title: 同 plot_circuit。

    返回：matplotlib Axes。
    """
    from matplotlib.colors import Normalize
    from matplotlib.patches import Rectangle

    from ..noise import resolve_noise

    plt = _plt()
    noise = resolve_noise(noise)
    n = circuit.num_qubits
    m = len(circuit.ops)
    cmap = plt.cm.YlOrRd
    vmax = max(noise.single, noise.double, 1e-6)
    norm = Normalize(vmin=0, vmax=vmax)

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
        if op.name == "measure":
            _draw_box(ax, col, qs[0], _gate_label(op))
            continue
        rate = noise.single if len(qs) == 1 else noise.double
        if len(qs) == 1:
            y = qs[0]
            ax.add_patch(
                Rectangle((col - 0.5, y - 0.42), 1.0, 0.84,
                          facecolor=cmap(norm(rate)), edgecolor="none",
                          alpha=0.55, zorder=1.5)
            )
            _draw_box(ax, col, y, _gate_label(op))
            continue
        ymin, ymax = min(qs), max(qs)
        ax.add_patch(
            Rectangle((col - 0.5, ymin - 0.42), 1.0, (ymax - ymin) + 0.84,
                      facecolor=cmap(norm(rate)), edgecolor="none",
                      alpha=0.55, zorder=1.5)
        )
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

    sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, label="去极化噪声率")
    cbar.set_ticks([0, vmax])
    cbar.set_ticklabels(["0", f"{vmax:.3g}"])
    if title is None:
        title = f"噪声叠加（single={noise.single}, double={noise.double}）"
    return finalize(fig, ax, show, save, title)
