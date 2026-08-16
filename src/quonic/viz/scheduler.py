"""调度器相关可视化：方法对比、决策树、选择热力图、降级链、特征雷达图。"""


from ..ir import Circuit
from ..scheduler import circuit_features, load_measured_decision, recommend_method
from ..scheduler.registry import load_performance
from ._mpl import _plt, finalize

# ---------------------------------------------------------------------------
# 4. 方法对比折线图
# ---------------------------------------------------------------------------

def plot_method_comparison(cls="clifford", ax=None, show=False, save=None, title=None):
    """画各模拟方法随量子比特数增长的耗时折线（对数 y 轴）。

    参数：
        cls: 决策类别 "clifford" 或 "low_tw"（对应基准里的电路族）。
        ax / show / save / title: 同 plot_circuit。

    返回：matplotlib Axes。
    """
    plt = _plt()
    perf = [p for p in load_performance() if p.get("class") == cls]
    if not perf:
        raise ValueError(f"没有 '{cls}' 类别的实测数据，请先运行基准校准")

    ns = sorted({p["n"] for p in perf})
    methods = sorted({m for p in perf for m in p["timings"]})

    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 4.5))
    else:
        fig = ax.figure

    for method in methods:
        xs, ys = [], []
        for n in ns:
            row = next((p for p in perf if p["n"] == n), None)
            if row is not None and method in row["timings"]:
                xs.append(n)
                ys.append(row["timings"][method])
        ax.plot(xs, ys, marker="o", label=method)

    ax.set_xlabel("量子比特数 n")
    ax.set_ylabel("耗时 (s)")
    ax.set_yscale("log")
    ax.legend()
    ax.set_title(f"决策类别：{cls}")
    return finalize(fig, ax, show, save, title)


# ---------------------------------------------------------------------------
# 5. 调度决策树
# ---------------------------------------------------------------------------

class _Node:
    __slots__ = ("label", "children", "x", "y")

    def __init__(self, label, children=None):
        self.label = label
        self.children = children or []  # list[(edge_label, _Node)]
        self.x = 0.0
        self.y = 0.0


_LAYER_SPACING = 1.6  # 相邻层之间的 y 间距（自上而下）
_LEAF_SPACING = 2.0   # 相邻叶子之间的 x 间距


def _assign(node, depth, next_leaf, max_depth):
    node.y = depth * _LAYER_SPACING
    max_depth[0] = max(max_depth[0], depth)
    if not node.children:
        node.x = next_leaf[0] * _LEAF_SPACING
        next_leaf[0] += 1
        return
    for _, child in node.children:
        _assign(child, depth + 1, next_leaf, max_depth)
    node.x = sum(c.x for _, c in node.children) / len(node.children)


def _build_decision_tree():
    decision = load_measured_decision() or {}
    cliff_n = decision.get("clifford", {}).get("above_n", 24)
    lowtw_n = decision.get("low_tw", {}).get("above_n", 24)

    root = _Node("电路")
    noise_yes = _Node("DM", [])
    classify = _Node("决策类别")

    general = _Node("SV", [])
    cliff = _Node(f"n ≥ {cliff_n}?")
    cliff.children = [
        ("是", _Node("Stab", [])),
        ("否", _Node("SV", [])),
    ]
    lowtw = _Node(f"n ≥ {lowtw_n}?")
    lowtw.children = [
        ("是", _Node("MPS", [])),
        ("否", _Node("SV", [])),
    ]

    classify.children = [
        ("general", general),
        ("clifford", cliff),
        ("low_tw", lowtw),
    ]
    root.children = [("有噪声", noise_yes), ("无噪声", classify)]
    return root


def plot_decision_tree(ax=None, show=False, save=None, title=None):
    """画调度决策树：噪声 → density_matrix，其余按类别与交叉点选方法。

    参数：
        ax / show / save / title: 同 plot_circuit。

    返回：matplotlib Axes。
    """
    from matplotlib.patches import FancyArrowPatch, Rectangle

    plt = _plt()
    root = _build_decision_tree()
    next_leaf = [0]
    max_depth = [0]
    _assign(root, 0, next_leaf, max_depth)

    depth = max_depth[0]
    n_leaves = next_leaf[0]
    xmax = (n_leaves - 1) * _LEAF_SPACING
    ymax = depth * _LAYER_SPACING

    if ax is None:
        fig, ax = plt.subplots(
            figsize=(max(7.0, xmax * 0.8 + 1.6), max(4.0, ymax * 0.8 + 1.2))
        )
    else:
        fig = ax.figure

    def draw(node):
        # 先画子边，再画自身，保证节点盖在边上
        for edge_label, child in node.children:
            ax.add_patch(
                FancyArrowPatch(
                    (node.x, node.y + 0.22),
                    (child.x, child.y - 0.22),
                    arrowstyle="-",
                    color="0.5",
                    lw=1.2,
                )
            )
            mx, my = (node.x + child.x) / 2, (node.y + child.y) / 2
            ax.text(
                mx,
                my,
                edge_label,
                ha="center",
                va="center",
                fontsize=8,
                color="0.25",
                bbox=dict(facecolor="white", edgecolor="none", pad=1.5),
                zorder=5,
            )
            draw(child)
        ax.add_patch(
            Rectangle(
                (node.x - 0.5, node.y - 0.22),
                1.0,
                0.44,
                facecolor="#4C72B0",
                edgecolor="black",
                zorder=2,
            )
        )
        ax.text(node.x, node.y, node.label, ha="center", va="center",
                fontsize=8, color="white", zorder=3)

    draw(root)
    ax.set_xlim(-1.2, xmax + 1.2)
    ax.set_ylim(-0.6, ymax + 0.6)
    ax.invert_yaxis()
    ax.axis("off")
    fig.subplots_adjust(bottom=0.12)
    fig.text(0.5, 0.02, _method_legend(), ha="center", va="bottom", fontsize=8, color="0.4")
    return finalize(fig, ax, show, save, title)


# ---------------------------------------------------------------------------
# 6. 方法选择热力图
# ---------------------------------------------------------------------------

_METHODS = ["statevector", "stabilizer", "matrix_product_state", "density_matrix"]
_METHOD_COLORS = {
    "statevector": 0,
    "stabilizer": 1,
    "matrix_product_state": 2,
    "density_matrix": 3,
}
_METHOD_ABBREV = {
    "statevector": "SV",
    "stabilizer": "Stab",
    "matrix_product_state": "MPS",
    "density_matrix": "DM",
}


def _method_legend():
    return "   ".join(f"{abbr} = {name}" for name, abbr in _METHOD_ABBREV.items())


def _features_for_class(cls, n):
    if cls == "clifford":
        return {"n": n, "gate_types": ["cx", "h"], "treewidth_ub": 1}
    if cls == "low_tw":
        return {"n": n, "gate_types": ["cx", "rz"], "treewidth_ub": 1}
    # general：高树宽非 Clifford
    return {"n": n, "gate_types": ["mcz"], "treewidth_ub": n - 1}


def plot_method_heatmap(ax=None, show=False, save=None, title=None):
    """画「决策类别 × 比特数 → 调度器所选方法」的热力图。

    参数：
        ax / show / save / title: 同 plot_circuit。

    返回：matplotlib Axes。
    """
    plt = _plt()
    rows = ["clifford", "low_tw", "general", "noisy"]
    ns = [8, 12, 16, 20, 24, 28]

    grid = []
    for cls in rows:
        row = []
        for n in ns:
            if cls == "noisy":
                method = "density_matrix"
            else:
                method = recommend_method(_features_for_class(cls, n))
            row.append(method)
        grid.append(row)

    data = [[_METHOD_COLORS[m] for m in row] for row in grid]

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 4.5))
    else:
        fig = ax.figure

    ax.imshow(data, cmap="viridis", aspect="auto", vmin=0, vmax=len(_METHODS) - 1)
    for i in range(len(rows)):
        for j in range(len(ns)):
            ax.text(j, i, _METHOD_ABBREV[grid[i][j]], ha="center", va="center", fontsize=7)

    ax.set_xticks(range(len(ns)))
    ax.set_xticklabels(ns)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels(rows)
    ax.set_xlabel("量子比特数 n")
    ax.set_ylabel("决策类别")
    fig.subplots_adjust(bottom=0.18)
    fig.text(0.5, 0.02, _method_legend(), ha="center", va="bottom", fontsize=8, color="0.4")
    return finalize(fig, ax, show, save, title)


# ---------------------------------------------------------------------------
# 7. 降级链路径图
# ---------------------------------------------------------------------------

def plot_fallback_chain(ax=None, show=False, save=None, title=None):
    """画后端降级链：qiskit → cirq → pennylane → native（自研兜底）。

    参数：
        ax / show / save / title: 同 plot_circuit。

    返回：matplotlib Axes。
    """
    from matplotlib.patches import FancyArrowPatch, Rectangle

    plt = _plt()
    chain = [
        ("qiskit", "Aer"),
        ("cirq", "Google"),
        ("pennylane", "量子机器学习"),
        ("native", "自研引擎兜底"),
    ]
    n = len(chain)

    if ax is None:
        fig, ax = plt.subplots(figsize=(8.5, 2.6))
    else:
        fig = ax.figure

    for i, (name, desc) in enumerate(chain):
        ax.add_patch(
            Rectangle((i - 0.38, -0.22), 0.76, 0.44, facecolor="#4C72B0",
                      edgecolor="black", zorder=2)
        )
        ax.text(i, 0, name, ha="center", va="center", color="white", fontsize=9, zorder=3)
        ax.text(i, -0.42, desc, ha="center", va="center", fontsize=7, color="0.4")
        if i < n - 1:
            ax.add_patch(
                FancyArrowPatch((i + 0.42, 0), (i + 0.58, 0), arrowstyle="-|>",
                                mutation_scale=14, color="0.4", lw=1.2)
            )
            ax.text(i + 0.5, 0.16, "未安装\n/ 不支持", ha="center", va="bottom",
                    fontsize=6.5, color="0.4")

    ax.set_xlim(-0.7, n - 0.3)
    ax.set_ylim(-0.7, 0.5)
    ax.axis("off")
    return finalize(fig, ax, show, save, title)


# ---------------------------------------------------------------------------
# 9. 电路特征雷达图
# ---------------------------------------------------------------------------

def plot_feature_radar(circuit_or_features, ax=None, show=False, save=None, title=None):
    """画单个电路的多维特征雷达图（极坐标）。

    参数：
        circuit_or_features: Circuit 或 circuit_features(circuit) 的 dict。
        ax / show / save / title: 同 plot_circuit。

    返回：matplotlib Axes。
    """
    import numpy as np

    plt = _plt()
    if isinstance(circuit_or_features, Circuit):
        feats = circuit_features(circuit_or_features)
    else:
        feats = circuit_or_features

    dims = ["n", "depth", "gate_count", "treewidth_ub", "clifford"]
    labels = ["比特数", "深度", "门数", "树宽", "Clifford"]
    raw = [
        feats.get("n", 0) / 30.0,
        feats.get("depth", 0) / 100.0,
        feats.get("gate_count", 0) / 200.0,
        feats.get("treewidth_ub", 0) / 10.0,
        1.0 if feats.get("is_clifford") else 0.0,
    ]
    values = [min(max(v, 0.0), 1.0) for v in raw]

    if ax is None:
        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111, projection="polar")
    else:
        fig = ax.figure

    angles = np.linspace(0, 2 * np.pi, len(dims), endpoint=False).tolist()
    values_c = values + values[:1]
    angles_c = angles + angles[:1]

    ax.plot(angles_c, values_c, color="#4C72B0", lw=1.5)
    ax.fill(angles_c, values_c, color="#4C72B0", alpha=0.25)
    ax.set_xticks(angles)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["0.25", "0.5", "0.75", "1.0"], fontsize=7)
    if title is not None:
        ax.set_title(title)
    if save:
        fig.savefig(save, bbox_inches="tight", dpi=120)
    if show:
        plt.show()
    return ax
