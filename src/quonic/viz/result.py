"""结果可视化：测量直方图。"""

from ..result import Result
from ._mpl import _plt, finalize


def plot_counts(result, ax=None, show=False, save=None, title=None, top_k=20):
    """画测量直方图：x 轴为比特串，y 轴为采样次数。

    参数：
        result: Result（kind="counts"）或 dict 直方图。
        ax / show / save / title: 同 plot_circuit。
        top_k: 只显示次数最多的前 top_k 个比特串（按比特串排序）；None 表示
            全部显示。采样直方图条目很多时默认只画前 20 个，避免柱状图挤爆。

    返回：matplotlib Axes。
    """
    plt = _plt()
    if isinstance(result, Result):
        counts = result.counts or {}
    elif isinstance(result, dict):
        counts = result
    else:
        raise TypeError("plot_counts 需要 Result（counts）或 dict 直方图")

    truncated = top_k is not None and len(counts) > top_k
    if truncated:
        items = sorted(counts.items(), key=lambda kv: -kv[1])[:top_k]
        items.sort()
        labels = [k for k, _ in items]
    else:
        labels = sorted(counts)
    values = [counts[k] for k in labels]

    if ax is None:
        fig, ax = plt.subplots(figsize=(max(5.0, len(labels) * 0.8), 4.0))
    else:
        fig = ax.figure

    ax.bar(range(len(labels)), values, color="#4C72B0")
    ax.set_xticks(range(len(labels)))
    tick_labels = [f"|{k}>" for k in labels]
    max_len = max((len(t) for t in tick_labels), default=0)
    rotation = 90 if (len(labels) > 8 or max_len > 6) else 0
    fontsize = 9 if max_len <= 6 else (7 if max_len <= 10 else 6)
    ax.set_xticklabels(tick_labels, rotation=rotation, fontsize=fontsize)
    ax.set_ylabel("次数")
    ax.set_xlabel("比特串")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    if title is None and truncated:
        title = f"直方图（次数最多的前 {top_k} 个比特串，共 {len(counts)} 个）"
    return finalize(fig, ax, show, save, title)
