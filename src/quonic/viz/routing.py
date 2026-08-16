"""路由可视化：耦合图上的 SWAP 插入电路图。"""

from ..compiler import route_swaps
from ._mpl import _plt, finalize
from .circuit import _draw_box, _draw_target, _gate_label


def _draw_swap(ax, x, y0, y1):
    """在两个相邻量子比特线之间画 SWAP 叉号（橙色）。"""
    ax.plot([x, x], [y0, y1], color="0.35", lw=1.0, zorder=2)
    ax.plot([x - 0.28, x + 0.28], [y0, y1], color="#E07B00", lw=1.8, zorder=3)
    ax.plot([x - 0.28, x + 0.28], [y1, y0], color="#E07B00", lw=1.8, zorder=3)


def plot_routing(circuit, coupling_map, ax=None, show=False, save=None, title=None):
    """画贪心 SWAP 路由后的电路图，插入的 SWAP 用橙色叉号标出。

    横轴为门序列（原始门 + 插入的 SWAP），每行一个物理比特。单比特门会随映射
    移动到其物理位置，直观展示逻辑比特如何在耦合图上「走动」。

    参数：
        circuit: 源 Circuit。
        coupling_map: CouplingMap（连通性约束）。
        ax / show / save / title: 同 plot_circuit。

    返回：matplotlib Axes。
    """
    plt = _plt()
    routed = route_swaps(circuit, coupling_map)
    n = routed.num_qubits
    m = len(routed.ops)
    n_swaps = sum(1 for op in routed.ops if op.name == "swap")

    if ax is None:
        fig, ax = plt.subplots(
            figsize=(max(6.0, m * 0.55 + 1.0), max(1.8, n * 0.55))
        )
    else:
        fig = ax.figure

    for q in range(n):
        ax.plot([-0.5, m - 0.5], [q, q], color="0.35", lw=1.0, zorder=1)

    for col, op in enumerate(routed.ops):
        qs = list(op.qubits)
        if op.name == "swap":
            _draw_swap(ax, col, qs[0], qs[1])
            continue
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
    ax.set_ylabel("物理比特")
    for s in ("top", "right", "bottom"):
        ax.spines[s].set_visible(False)
    if title is None:
        title = f"SWAP 路由（插入 {n_swaps} 个 SWAP）"
    return finalize(fig, ax, show, save, title)
