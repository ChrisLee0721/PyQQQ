"""把硬件噪声基准（qi_hardware.json）绘成报告用图，嵌入 docs/test-report.md。

用 QuoNic 自带的 viz.plot_counts 画直方图（理想 vs 真机并排），
再用 matplotlib 画噪声汇总条形图。

产出：docs/figures/*.png

用法：
    .venv/Scripts/python.exe scripts/plot_report.py
"""

import json
import os

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager

from quonic.viz import plot_counts

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "docs", "figures")
os.makedirs(OUT, exist_ok=True)

# 中文字体（与 viz._mpl 相同策略）
available = {f.name for f in font_manager.fontManager.ttflist}
for name in ("Microsoft YaHei", "SimHei", "PingFang SC", "Noto Sans CJK SC"):
    if name in available:
        matplotlib.rcParams["font.sans-serif"] = [name, "DejaVu Sans"]
        break
matplotlib.rcParams["axes.unicode_minus"] = False

with open(os.path.join(HERE, "qi_hardware.json"), encoding="utf-8") as f:
    report = json.load(f)

cases = report["cases"]


def _side_by_side(name, title, ideal, real, xlabel="比特串"):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4), sharey=False)
    plot_counts(ideal, ax=ax1, title="QX emulator（理想）", top_k=None)
    plot_counts(real, ax=ax2, title="Tuna-9（真机）", top_k=None)
    ax1.set_ylabel("次数")
    ax2.set_ylabel("次数")
    fig.suptitle(title, fontsize=12)
    fig.tight_layout()
    path = os.path.join(OUT, f"{name}.png")
    fig.savefig(path, bbox_inches="tight", dpi=130)
    plt.close(fig)
    return path


def _success_targets(c):
    return set(c["target"])


# 1) 成功类用例：理想 vs 真机并排直方图
for c in cases:
    if c.get("kind") != "success":
        continue
    name = c["name"]
    desc = c["desc"]
    _side_by_side(
        name, f"{name} — {desc}",
        c["ideal_counts"], c["real_counts"],
    )

# 2) qft3（uniform）：理想 vs 真机
for c in cases:
    if c.get("kind") == "uniform":
        _side_by_side(
            c["name"], f"{c['name']} — {c['desc']}",
            c["ideal_counts"], c["real_counts"],
        )

# 3) 噪声汇总条形图（噪声 = 1 - 真机成功率）
labels = []
noise = []
for c in cases:
    if c.get("kind") != "success":
        continue
    labels.append(c["name"])
    noise.append(round((1 - c["real_success"]) * 100, 1))

fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(labels, noise, color="#C44E52")
ax.set_ylabel("噪声（%）")
ax.set_xlabel("电路")
ax.set_title("真机噪声（Tuna-9，噪声 = 1 − 成功率）")
for b, v in zip(bars, noise):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.5, f"{v:.1f}%",
            ha="center", va="bottom", fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
summary_path = os.path.join(OUT, "noise_summary.png")
fig.savefig(summary_path, bbox_inches="tight", dpi=130)
plt.close(fig)

# 4) Bell 跨设备对照（Tuna-9 vs Tuna-17）
bell = {c["name"]: c for c in cases}.get("bell")
bell17 = {c["name"]: c for c in cases}.get("bell17")
if bell and bell17:
    fig, ax = plt.subplots(figsize=(5, 3.5))
    devs = ["Tuna-9", "Tuna-17"]
    succ = [round(bell["real_success"] * 100, 2), round(bell17["real_success"] * 100, 2)]
    bars = ax.bar(devs, succ, color="#4C72B0")
    ax.set_ylim(90, 100)
    ax.set_ylabel("Bell 态成功率（%）")
    ax.set_title("Bell state 跨设备对照")
    for b, v in zip(bars, succ):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.1, f"{v:.2f}%",
                ha="center", va="bottom", fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    cross_path = os.path.join(OUT, "bell_cross_device.png")
    fig.savefig(cross_path, bbox_inches="tight", dpi=130)
    plt.close(fig)

print("已生成：")
for fn in sorted(os.listdir(OUT)):
    print(" ", os.path.join("docs", "figures", fn))
