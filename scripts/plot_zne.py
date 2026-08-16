"""把 ZNE 结果（zne_mitigation.json）绘成外推图。

产出 docs/figures/zne_extrapolation.png：x 轴为噪声档 λ，y 轴成功率，
散点 + 线性拟合线 + 外推到 λ=0 的缓解值。

用法：
    .venv/Scripts/python.exe scripts/plot_zne.py
"""

import json
import os

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "docs", "figures")
os.makedirs(OUT, exist_ok=True)

available = {f.name for f in font_manager.fontManager.ttflist}
for name in ("Microsoft YaHei", "SimHei", "PingFang SC", "Noto Sans CJK SC"):
    if name in available:
        matplotlib.rcParams["font.sans-serif"] = [name, "DejaVu Sans"]
        break
matplotlib.rcParams["axes.unicode_minus"] = False

with open(os.path.join(HERE, "zne_mitigation.json"), encoding="utf-8") as f:
    report = json.load(f)

fig, ax = plt.subplots(figsize=(7.5, 4.2))
colors = {"ghz3": "#C44E52", "bell": "#4C72B0"}
for c in report["cases"]:
    lam = c["lambda"]
    p = c["success"]
    col = colors.get(c["name"], "#555")
    ax.scatter(lam, p, color=col, label=f"{c['name']}（实测）", zorder=3)
    # 线性外推线（最小二乘）
    n = len(lam)
    xb, yb = sum(lam) / n, sum(p) / n
    sxx = sum((x - xb) ** 2 for x in lam)
    sxy = sum((x - xb) * (y - yb) for x, y in zip(lam, p))
    b = sxy / sxx if sxx else 0.0
    a = yb - b * xb
    xs = [0, max(lam) + 0.5]
    ys = [a + b * x for x in xs]
    ax.plot(xs, ys, "--", color=col, alpha=0.7, label=f"{c['name']}（线性外推）")
    ax.scatter([0], [a], color=col, marker="*", s=180, zorder=4,
               label=f"{c['name']} λ=0 缓解 {a:.3f}")
ax.axvline(0, color="gray", lw=0.8, alpha=0.5)
ax.set_xlabel("噪声放大倍数 λ（全局折叠）")
ax.set_ylabel("成功率")
ax.set_title("ZNE：成功率随 λ 外推到零噪声")
ax.legend(fontsize=8)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
path = os.path.join(OUT, "zne_extrapolation.png")
fig.savefig(path, bbox_inches="tight", dpi=130)
plt.close(fig)
print("已生成", os.path.join("docs", "figures", "zne_extrapolation.png"))
