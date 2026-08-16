"""性能基准回归：重跑调度基准，和随包基线比对，标记性能回退。

判断标准（不依赖绝对耗时，避免机器漂移误报）：
  1. 能力矩阵变化 —— 任何方法的能力（noise / 门集）收窄即回归；
  2. 决策表（交叉点）变化 —— 备选方法首次占优的 n 上移，或退回 statevector；
  3. 高树宽 statevector 天花板 + 噪声成本 —— 相对基线放大超过 --ratio 倍即回归。

用法：
    .venv/Scripts/python.exe scripts/benchmark_regression.py [--ratio 3.0] [--backend qiskit]

退出码：0 = 通过；1 = 检测到回归。
"""

import argparse
import json
import os
import sys

from quonic.scheduler import benchmark as bench

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASELINE_PATH = os.path.join(
    HERE, "src", "quonic", "scheduler", "data", "benchmarks.json"
)

# 与随包基线一致的网格（保证决策表可比）
GRID_N = (8, 12, 16, 20, 24)
NOISE_N = (2, 4, 6, 8, 10, 12)
GENERAL_N = (8, 12, 16)


def _load_baseline():
    with open(BASELINE_PATH, encoding="utf-8") as f:
        return json.load(f)


def compare_capabilities(base, cur):
    issues = []
    caps = base.get("capabilities", {})
    cur_caps = cur.get("capabilities", {})
    for m, b in caps.items():
        c = cur_caps.get(m)
        if c is None:
            issues.append(f"能力矩阵：方法 '{m}' 消失")
            continue
        if b.get("noise") and not c.get("noise"):
            issues.append(f"能力矩阵：方法 '{m}' 失去噪声支持")
        if b.get("gates") != c.get("gates"):
            issues.append(
                f"能力矩阵：方法 '{m}' 门集 {b.get('gates')} -> {c.get('gates')}"
            )
    return issues


def compare_decision(base, cur):
    issues = []
    base_d = base.get("decision", {})
    cur_d = cur.get("decision", {})
    for cls, b in base_d.items():
        c = cur_d.get(cls)
        if c is None:
            issues.append(
                f"决策表：{cls} 的备选方法 {b['method']} 不再占优（可能退回 statevector）"
            )
            continue
        if c["method"] != b["method"]:
            issues.append(f"决策表：{cls} 方法 {b['method']} -> {c['method']}")
            continue
        if c["above_n"] > b["above_n"]:
            issues.append(
                f"决策表：{cls} 交叉点 n 从 {b['above_n']} 上移到 {c['above_n']}"
                f"（{b['method']} 相对变慢）"
            )
    return issues


def compare_ratio(base, cur, ratio, key, keyfn):
    issues = []
    base_rows = {keyfn(r): r for r in base.get(key, [])}
    cur_rows = {keyfn(r): r for r in cur.get(key, [])}
    for k, b in base_rows.items():
        c = cur_rows.get(k)
        if c is None:
            continue
        bt, ct = b["time"], c["time"]
        if bt > 0 and ct > bt * ratio:
            issues.append(f"{key}：{k} 耗时 {bt:.4f}s -> {ct:.4f}s（>{ratio}x）")
    return issues


def compare_noise(base, cur, ratio):
    issues = []
    b = base.get("noise", {})
    c = cur.get("noise", {})
    if not b or not c:
        return issues
    b_inf, c_inf = b.get("infeasible_n"), c.get("infeasible_n")
    if b_inf and c_inf and c_inf < b_inf:
        issues.append(
            f"噪声成本：不可行阈值 n 从 {b_inf} 降到 {c_inf}（4^n 成本提前爆炸）"
        )
    base_perf = {r["n"]: r["time"] for r in b.get("performance", [])}
    cur_perf = {r["n"]: r["time"] for r in c.get("performance", [])}
    for n, bt in base_perf.items():
        ct = cur_perf.get(n)
        if ct and bt > 0 and ct > bt * ratio:
            issues.append(f"噪声成本：n={n} 耗时 {bt:.4f}s -> {ct:.4f}s（>{ratio}x）")
    return issues


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="性能基准回归：重跑调度基准并比对基线"
    )
    parser.add_argument("--ratio", type=float, default=3.0,
                        help="耗时放大倍数阈值（默认 3）")
    parser.add_argument("--backend", default="qiskit")
    parser.add_argument("--shots", type=int, default=256)
    args = parser.parse_args(argv)

    base = _load_baseline()
    print(f"基线：{base.get('meta', {}).get('generated_at', '?')} "
          f"（{base.get('meta', {}).get('backend', '?')}）")
    print("重跑基准（同机同网格）…")

    data = bench.build_benchmark_data(
        GRID_N, noise_n=NOISE_N, general_n=GENERAL_N,
        backend=args.backend, shots=args.shots,
    )

    issues = []
    issues += compare_capabilities(base, data)
    issues += compare_decision(base, data)
    issues += compare_ratio(base, data, args.ratio, "general",
                            lambda r: f"{r['circuit']}:{r['n']}")
    issues += compare_noise(base, data, args.ratio)

    print()
    if issues:
        print(f"检测到 {len(issues)} 处回退：")
        for i in issues:
            print(f"  ✗ {i}")
        print("\n结论：回归（可能由依赖升级 / 后端变化 / 系统负载引起，可重跑确认）")
        return 1
    print("未检测到性能回退。")
    print("结论：通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
