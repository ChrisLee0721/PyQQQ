"""把资源估算（resource_estimation.json）绘成报告用图。

产出 docs/figures/resource_explosion.png（原 IR → decompose → transpile 门数对比）。

用法：
    .venv/Scripts/python.exe scripts/plot_resource.py
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

with open(os.path.join(HERE, "resource_estimation.json"), encoding="utf-8") as f:
    report = json.load(f)

cases = report["cases"]
names = list(cases)
orig = [cases[n]["original_gates"] for n in names]
decomp = [cases[n]["decomposed_gates"] for n in names]
transp = [cases[n]["transpiled_gates"] for n in names]
twoq = [cases[n]["transpiled_2q_gates"] for n in names]

x = range(len(names))
w = 0.21

fig, ax = plt.subplots(figsize=(9, 4.5))
ax.bar([i - w for i in x], orig, w, label="原 IR", color="#4C72B0")
ax.bar(x, decomp, w, label="decompose()", color="#DD8452")
ax.bar([i + w for i in x], transp, w, label="transpile→Tuna-9", color="#C44E52")
ax.set_yscale("log")
ax.set_ylabel("门数（log 刻度）")
ax.set_xticks(list(x))
ax.set_xticklabels(names, fontsize=9)
ax.set_title("编译各阶段门数爆炸（Tuna-9）")
ax.legend()
for i in x:
    ax.text(i, transp[i] * 1.15, f"{transp[i]}", ha="center", fontsize=8, color="#8b1a1a")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
path = os.path.join(OUT, "resource_explosion.png")
fig.savefig(path, bbox_inches="tight", dpi=130)
plt.close(fig)

# 深度 + 两比特门（噪声相关指标）
fig, ax = plt.subplots(figsize=(9, 3.8))
ax.bar([i - w / 2 for i in x], [cases[n]["transpiled_depth"] for n in names],
       w, label="深度", color="#55A868")
ax.bar([i + w / 2 for i in x], twoq, w, label="两比特门", color="#8172B2")
ax.set_ylabel("数量")
ax.set_xticks(list(x))
ax.set_xticklabels(names, fontsize=9)
ax.set_title("transpile 后深度与两比特门（噪声主因）")
ax.legend()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
path2 = os.path.join(OUT, "resource_depth_2q.png")
fig.savefig(path2, bbox_inches="tight", dpi=130)
plt.close(fig)

print("已生成：")
print(" ", os.path.join("docs", "figures", "resource_explosion.png"))
print(" ", os.path.join("docs", "figures", "resource_depth_2q.png"))
