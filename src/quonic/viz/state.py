"""量子态可视化：布洛赫球、密度矩阵热力图、纠缠谱、逐门态演化。"""

import math

from ..ir import Circuit
from ._mpl import _plt, finalize
from .circuit import _to_statevector


def _bloch_vector(state):
    """把单比特态（或布洛赫向量三元组）转成 (x, y, z)。"""
    import numpy as np

    if isinstance(state, (list, tuple)) and len(state) == 3:
        x, y, z = (float(v) for v in state)
        if x * x + y * y + z * z > 1.0 + 1e-9:
            raise ValueError("布洛赫向量模长需 ≤ 1")
        return x, y, z

    sv = np.asarray(_to_statevector(state), dtype=complex)
    if sv.size != 2:
        raise ValueError("布洛赫球只接受单比特态（2 个复振幅）或 3 维布洛赫向量")
    sv = sv / np.linalg.norm(sv)
    a, b = sv[0], sv[1]
    x = 2 * (a.conjugate() * b).real
    y = 2 * (a.conjugate() * b).imag
    z = abs(a) ** 2 - abs(b) ** 2
    return float(x), float(y), float(z)


def _rho_bloch_vector(rho):
    """从 2×2 密度矩阵求布洛赫向量（混合态也适用）。"""
    import numpy as np

    rho = np.asarray(rho, dtype=complex)
    x = 2 * rho[0, 1].real
    y = 2 * rho[1, 0].imag  # = -2 Im(rho01)
    z = (rho[0, 0] - rho[1, 1]).real
    return float(x), float(y), float(z)


def _draw_bloch_sphere(ax, x, y, z, label=None):
    """在给定 3D Axes 上画一个布洛赫球（球线框 + 坐标轴 + 态向量箭头）。"""
    import numpy as np

    u = np.linspace(0, 2 * np.pi, 48)
    v = np.linspace(0, np.pi, 24)
    sx = np.outer(np.cos(u), np.sin(v))
    sy = np.outer(np.sin(u), np.sin(v))
    sz = np.outer(np.ones_like(u), np.cos(v))
    ax.plot_wireframe(sx, sy, sz, color="0.85", linewidth=0.4, alpha=0.6)

    for (dx, dy, dz), t in (((1, 0, 0), "x"), ((0, 1, 0), "y"), ((0, 0, 1), "|0>")):
        ax.plot([-dx, dx], [-dy, dy], [-dz, dz], color="0.5", lw=0.8)
        ax.text(dx * 1.15, dy * 1.15, dz * 1.15, t, fontsize=9, color="0.3")
    ax.text(0, 0, -1.18, "|1>", fontsize=9, color="0.3")

    r = math.sqrt(x * x + y * y + z * z)
    color = "#4C72B0" if r > 0.99 else "#C44E52"  # 纯态蓝 / 混合态橙红
    ax.plot([0, x], [0, y], [0, z], color=color, lw=3)
    ax.scatter([x], [y], [z], color=color, s=80, zorder=5,
               edgecolor="white", linewidth=0.5)
    ax.scatter([0], [0], [0], color="0.4", s=12, zorder=4)  # 球心参考点
    if label is not None:
        ax.text2D(0.03, 0.97, label, transform=ax.transAxes, fontsize=10,
                  color="0.2", va="top", ha="left")

    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    ax.set_box_aspect((1, 1, 1))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])


def plot_bloch_sphere(state, ax=None, show=False, save=None, title=None):
    """画单比特态的布洛赫球（3D，单位球面上的一个点 + 原点指向它的箭头）。

    参数：
        state: 2 复振幅数组 / StatevectorEngine(1) / 单比特 Circuit / 3 维布洛赫向量。
        ax: 可选，需为 3D projection；不传则新建。
        show / save / title: 同 plot_circuit。

    返回：matplotlib Axes（3D）。
    """
    plt = _plt()
    x, y, z = _bloch_vector(state)

    if ax is None:
        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111, projection="3d")
    else:
        fig = ax.figure

    _draw_bloch_sphere(ax, x, y, z)
    if title is not None:
        ax.set_title(title)
    if save:
        fig.savefig(save, bbox_inches="tight", dpi=120)
    if show:
        plt.show()
    return ax


def plot_bloch_multivector(state, cols=None, annotate=False, show=False, save=None, title=None):
    """画多比特态每个量子比特的布洛赫球（网格布局）。

    对每个比特 q 求其约化单比特密度矩阵 ρ_q（对其它比特做部分迹），画成一张
    布洛赫球网格。纠缠态里各比特会「缩」进球内（混合态），直积态仍在球面。

    参数：
        state: n 比特态（1D 态矢量 / 2D 密度矩阵 / StatevectorEngine / Circuit）。
        cols: 每行球数；None 则取 min(n, 5)。
        annotate: True 时在每个球下方标注精确布洛赫矢量 (x, y, z)；默认 False
            保持图清爽（箭头方向 + |r| 标签已编码同等信息）。
        show / save / title: 同 plot_circuit。

    返回：3D Axes 列表（每个量子比特一个）。
    """
    import math

    plt = _plt()
    rho = _to_density(state)
    n = int(round(math.log2(rho.shape[0])))

    cols = cols or min(n, 5)
    rows = math.ceil(n / cols)
    fig = plt.figure(figsize=(cols * 2.8, rows * 2.8))

    axes = []
    for q in range(n):
        rho_q = _partial_trace(rho, [q], n)
        x, y, z = _rho_bloch_vector(rho_q)
        r = math.sqrt(x * x + y * y + z * z)
        ax = fig.add_subplot(rows, cols, q + 1, projection="3d")
        _draw_bloch_sphere(ax, x, y, z, label=f"q{q}  |r|={r:.2f}")
        if annotate:
            ax.text2D(0.5, 0.02, f"({x:+.3f}, {y:+.3f}, {z:+.3f})",
                      transform=ax.transAxes, fontsize=8, color="0.3",
                      va="bottom", ha="center")
        axes.append(ax)

    if title is not None:
        fig.suptitle(title)
    if save:
        fig.savefig(save, bbox_inches="tight", dpi=120)
    if show:
        plt.show()
    return axes


# ---------------------------------------------------------------------------
# 密度矩阵热力图
# ---------------------------------------------------------------------------

def _to_density(state):
    """把输入统一成 2^n × 2^n 复密度矩阵（numpy 数组）。"""
    import numpy as np

    from ..simulators import DensityMatrixEngine, StatevectorEngine

    if isinstance(state, DensityMatrixEngine):
        return np.asarray(state.rho)
    if isinstance(state, StatevectorEngine):
        sv = np.asarray(state.state)
        return np.outer(sv, sv.conjugate())
    if isinstance(state, Circuit):
        eng = DensityMatrixEngine(state.num_qubits)
        for op in state.ops:
            eng.apply(op.name, list(op.qubits), op.params)
        return np.asarray(eng.rho)
    arr = np.asarray(state, dtype=complex)
    if arr.ndim == 1:
        return np.outer(arr, arr.conjugate())
    if arr.ndim == 2:
        return arr
    raise TypeError("无法识别的量子态输入（需 1D 态矢量 / 2D 密度矩阵 / 引擎 / Circuit）")


def plot_density_matrix(state, ax=None, show=False, save=None, title=None):
    """画密度矩阵的实部/虚部双面板热力图。

    参数：
        state: DensityMatrixEngine / StatevectorEngine / Circuit / 复数组。
        ax: 可选，长度为 2 的 Axes 序列（[实部, 虚部]）；不传则新建双子图。
        show / save / title: 同 plot_circuit。

    返回：长度为 2 的 Axes 序列 [ax_real, ax_imag]。
    """
    import numpy as np

    plt = _plt()
    rho = _to_density(state)
    n = int(round(math.log2(rho.shape[0])))

    if ax is None:
        fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
    else:
        axes = ax
        fig = axes[0].figure

    vmax = max(float(np.max(np.abs(rho.real))), float(np.max(np.abs(rho.imag))), 1e-12)

    labels = [f"|{format(i, '0%db' % n)}>" for i in range(2 ** n)]

    im0 = axes[0].imshow(rho.real, cmap="RdBu_r", vmin=-vmax, vmax=vmax)
    axes[0].set_title("Re(ρ)")
    im1 = axes[1].imshow(rho.imag, cmap="RdBu_r", vmin=-vmax, vmax=vmax)
    axes[1].set_title("Im(ρ)")
    for a in axes:
        a.set_xticks(range(2 ** n))
        a.set_yticks(range(2 ** n))
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


# ---------------------------------------------------------------------------
# 纠缠可视化
# ---------------------------------------------------------------------------

def _partial_trace(rho, keep, n):
    """对 n 比特密度矩阵求子系 A（keep 中的比特）的约化密度矩阵。

    被 trace 掉的比特，其行/列指标共享同一 einsum 字母（对角求和 = 部分迹）。
    """
    import numpy as np

    rho = np.asarray(rho, dtype=complex).reshape([2] * (2 * n))
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    row_axis = {q: n - 1 - q for q in range(n)}
    col_axis = {q: n + (n - 1 - q) for q in range(n)}

    keep = set(keep)
    sub = [None] * (2 * n)
    row_out, col_out = [], []
    idx = 0
    for q in sorted(keep):
        r, c = letters[idx], letters[idx + 1]
        idx += 2
        sub[row_axis[q]] = r
        sub[col_axis[q]] = c
        row_out.append(r)
        col_out.append(c)
    for q in range(n):
        if q in keep:
            continue
        s = letters[idx]
        idx += 1
        sub[row_axis[q]] = s
        sub[col_axis[q]] = s

    in_sub = "".join(sub)
    out_sub = "".join(row_out + col_out)
    result = np.einsum(in_sub + "->" + out_sub, rho)
    k = len(keep)
    return result.reshape(2 ** k, 2 ** k)


def _von_neumann_entropy(eigenvalues):
    """从约化密度矩阵特征值求冯诺依曼熵（比特）。"""
    import numpy as np

    lam = np.clip(np.real(eigenvalues), 0.0, None)
    lam = lam[lam > 1e-12]
    return float(-np.sum(lam * np.log2(lam)))


def _concurrence(rho):
    """Wootters 并发度，适用于任意 2 比特态（纯或混合）。

    纯态退化为 sqrt(2(1 - Tr(ρ_A²)))；混合态（如测量坍缩后的经典关联态）
    正确返回 0——纯态公式对混合态会误判成非零。
    """
    import numpy as np

    rho = np.asarray(rho, dtype=complex)
    if rho.shape != (4, 4):
        raise ValueError("并发度只对 2 比特态定义（需 4×4 密度矩阵）")
    sy = np.array([[0.0, -1j], [1j, 0.0]], dtype=complex)
    m = np.kron(sy, sy)  # σ_y ⊗ σ_y
    rho_tilde = m @ rho.conj() @ m
    r = rho @ rho_tilde
    eig = np.linalg.eigvals(r)
    lam = np.sort(np.sqrt(np.clip(np.real(eig), 0.0, None)))[::-1]
    return float(max(0.0, lam[0] - lam[1] - lam[2] - lam[3]))


def plot_entanglement(state, partition=None, ax=None, show=False, save=None, title=None):
    """画量子态的纠缠谱（约化密度矩阵特征值）+ 冯诺依曼熵。

    把态按 partition（子系 A 的比特下标，默认取前一半）切开，对 B 做部分迹得到
    ρ_A，画出其特征值（施密特系数平方）降序柱状图，并标注纠缠熵。2 比特态额外
    标注并发度（concurrence，Wootters 公式，对纯态和混合态都成立）。

    参数：
        state: 1D 态矢量 / 2D 密度矩阵 / StatevectorEngine / Circuit。
        partition: 子系 A 的比特下标列表；None 表示前 floor(n/2) 个比特。
        ax / show / save / title: 同 plot_circuit。

    返回：matplotlib Axes。
    """
    import numpy as np

    plt = _plt()
    rho = _to_density(state)
    n = int(round(math.log2(rho.shape[0])))

    if partition is None:
        partition = list(range(n // 2))
    partition = sorted(set(partition))
    if not partition or any(not 0 <= q < n for q in partition):
        raise ValueError(f"partition 需为 [0, {n}) 的非空比特下标子集，收到 {partition}")

    rho_a = _partial_trace(rho, partition, n)
    eigvals = np.linalg.eigvalsh(rho_a)
    eigvals = np.sort(np.real(eigvals))[::-1]
    entropy = _von_neumann_entropy(eigvals)

    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 4))
    else:
        fig = ax.figure

    ax.bar(range(len(eigvals)), eigvals, color="#4C72B0")
    ax.set_xticks(range(len(eigvals)))
    ax.set_xticklabels([f"λ{i + 1}" for i in range(len(eigvals))])
    ax.set_ylabel("约化密度矩阵特征值")
    ax.set_xlabel("施密特系数（降序）")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

    label = f"纠缠熵 S(ρ_A) = {entropy:.3f} bit"
    if n == 2 and len(partition) == 1:
        concurrence = _concurrence(rho)
        label += f"   并发度 C = {concurrence:.3f}"
    ax.set_title(label)

    if title is not None:
        ax.set_title(f"{title}\n{label}")
    if save:
        fig.savefig(save, bbox_inches="tight", dpi=120)
    if show:
        plt.show()
    return ax


def plot_entanglement_profile(state, ax=None, show=False, save=None, title=None):
    """画所有相邻二分切口（0..k vs k+1..n-1）的纠缠熵谱。

    对每个切口 k 求约化密度矩阵 ρ_{0..k} 的冯诺依曼熵，画成柱状图。GHZ 态
    处处为 1、直积态处处为 0、低纠缠链式态呈单调分布。

    参数：
        state: 1D 态矢量 / 2D 密度矩阵 / StatevectorEngine / Circuit。
        ax / show / save / title: 同 plot_circuit。

    返回：matplotlib Axes。
    """
    import numpy as np

    plt = _plt()
    rho = _to_density(state)
    n = int(round(math.log2(rho.shape[0])))

    entropies = []
    for k in range(n - 1):
        rho_a = _partial_trace(rho, list(range(k + 1)), n)
        eigvals = np.linalg.eigvalsh(rho_a)
        entropies.append(_von_neumann_entropy(eigvals))

    if ax is None:
        fig, ax = plt.subplots(figsize=(max(5.0, n * 0.8), 4.0))
    else:
        fig = ax.figure

    cuts = list(range(n - 1))
    ax.bar(cuts, entropies, color="#4C72B0")
    ax.set_xticks(cuts)
    ax.set_xticklabels([f"k={k}" for k in cuts])
    ax.set_xlabel("二分切口（0..k | k+1..n-1）")
    ax.set_ylabel("纠缠熵 S (bit)")
    ax.set_ylim(0, max(1.0, (max(entropies) if entropies else 0) * 1.15))
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    return finalize(fig, ax, show, save, title)


# ---------------------------------------------------------------------------
# 逐门态演化
# ---------------------------------------------------------------------------

def plot_state_evolution(circuit, ax=None, show=False, save=None, title=None, top_k=16):
    """画态矢量随电路逐门演化的概率热力图。

    横轴为门序列（0 表示初态），纵轴为基态，色块为 |振幅|²。基态过多时只保留
    概率峰值最大的前 top_k 个（按索引排序）。

    参数：
        circuit: Circuit 对象。
        ax / show / save / title: 同 plot_circuit。
        top_k: 保留的基态数（按全程最大概率取前 k 个）；None 表示全部。

    返回：matplotlib Axes。
    """
    import numpy as np

    from ..simulators import StatevectorEngine

    plt = _plt()
    n = circuit.num_qubits
    eng = StatevectorEngine(n)
    probs = [np.abs(eng.state) ** 2]
    for op in circuit.ops:
        if op.name == "measure":
            continue
        eng.apply(op.name, list(op.qubits), op.params)
        probs.append(np.abs(eng.state) ** 2)
    grid = np.array(probs).T  # shape (2^n, 步数)

    shown = np.arange(2 ** n)
    if top_k is not None and grid.shape[0] > top_k:
        peak = grid.max(axis=1)
        shown = np.sort(np.argsort(peak)[::-1][:top_k])
        grid = grid[shown]

    if ax is None:
        fig, ax = plt.subplots(figsize=(max(6.0, grid.shape[1] * 0.4), max(3.0, grid.shape[0] * 0.3)))
    else:
        fig = ax.figure

    im = ax.imshow(grid, aspect="auto", cmap="Blues", interpolation="nearest", vmin=0, vmax=1)
    ax.set_yticks(range(grid.shape[0]))
    ax.set_yticklabels([f"|{format(i, '0%db' % n)}>" for i in shown], fontsize=7)
    ax.set_xlabel("门序列（0 = 初态）")
    ax.set_ylabel("基态")
    fig.colorbar(im, ax=ax, label="|振幅|²")
    if title is None and grid.shape[0] != 2 ** n:
        title = f"态演化（概率峰值最大的前 {top_k} 个基态，共 {2 ** n} 个）"
    return finalize(fig, ax, show, save, title)
