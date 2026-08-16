"""离线基准：在参考机上实测「门类型 × 比特数 × 方法」的交叉点，生成数据。

产出两份东西，供调度器运行时查询（护城河 = 别人抄代码、抄不到你积累的实测数据）：

- **能力矩阵**（capabilities，静态）—— 哪种方法能吃哪些门 / 是否支持噪声
- **性能数据**（performance + decision，动态）—— 各方法耗时 + 交叉点阈值

用法：
    python -m quonic.scheduler.benchmark -o scheduler/data/benchmarks.json

注意：耗时与 CPU / 内存 / BLAS / 后端版本强相关，跨机器会漂移。所以这份
脚本要能重跑校准；随包附带的是「参考机」上的固化表，冷启动兜底用。
"""

import argparse
import contextlib
import io
import json
import math
import time
from datetime import datetime, timezone

from ..backends import get_backend
from ..ir import Circuit, GateOperation
from ..noise import depolarizing
from .capabilities import METHOD_CAPABILITIES

# 每类电路对应的「挑战方法」（statevector 之外的备选）
_ALT_METHOD = {"clifford": "stabilizer", "low_tw": "matrix_product_state"}


def _timed_run(circuit, backend, method, shots=256, noise=None):
    """跑一次返回耗时；该 method 不支持此电路时返回 None。

    method 不支持该电路时 Aer 会向 stderr 打印报错，这里静默掉，只留耗时。
    noise 可为 NoiseModel 或概率数值，传给后端（用于 density_matrix 噪声基准）。
    """
    be = get_backend(backend)
    t0 = time.time()
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            be.run(circuit, shots=shots, method=method, noise=noise)
    except Exception:
        return None
    return time.time() - t0


# ---------------------------------------------------------------------------
# 电路族
# ---------------------------------------------------------------------------

def _ghz(n):
    """GHZ：纯基础 Clifford 链（H + CX），treewidth=1。"""
    c = Circuit()
    c.add(GateOperation("h", (0,)))
    for i in range(n - 1):
        c.add(GateOperation("cx", (i, i + 1)))
    return c


def _chain_rotation(n):
    """带旋转的低树宽链：非 Clifford（rz）+ CX 链，treewidth=1。"""
    c = Circuit()
    c.add(GateOperation("rz", (0,), (0.3,)))
    for i in range(n - 1):
        c.add(GateOperation("cx", (i, i + 1)))
    return c


def _qaoa(n, p=1):
    """QAOA 热身：一层 ry/rz 旋转 + CX 链，非 Clifford 低树宽。"""
    c = Circuit()
    for q in range(n):
        c.add(GateOperation("ry", (q,), (0.5,)))
    for i in range(n - 1):
        c.add(GateOperation("cx", (i, i + 1)))
    for q in range(n):
        c.add(GateOperation("rz", (q,), (0.4,)))
    return c


def _grover(n):
    """Grover 一次迭代：oracle + 扩散（ccx 非 Clifford，树宽较高）。"""
    c = Circuit()
    for q in range(n):
        c.add(GateOperation("h", (q,)))
    # oracle：翻转目标态 |1...1> 的相位（用 ccx 构造，非 Clifford）
    c.add(GateOperation("x", (0,)))
    c.add(GateOperation("ccx", (0, 1, n - 1)))
    c.add(GateOperation("x", (0,)))
    # 扩散算子：H 全层 + X 全层 + mcz + X 全层 + H 全层
    for q in range(n):
        c.add(GateOperation("h", (q,)))
        c.add(GateOperation("x", (q,)))
    c.add(GateOperation("mcz", tuple(range(n))))
    for q in range(n):
        c.add(GateOperation("x", (q,)))
        c.add(GateOperation("h", (q,)))
    return c


def _qft(n):
    """量子傅里叶变换：全连接受控相位（cp），非 Clifford 且树宽 n-1。

    标准 QFT 的 H + 受控旋转结构（省略末尾的比特序反转，不影响树宽/耗时特征）。
    """
    c = Circuit()
    for i in range(n):
        c.add(GateOperation("h", (i,)))
        for j in range(i + 1, n):
            angle = math.pi / (2 ** (j - i))
            c.add(GateOperation("cp", (j, i), (angle,)))
    return c


def representative_circuits():
    """演示/快速基准用的代表电路。"""
    return [
        ("ghz24", _ghz(24)),
        ("qaoa24", _qaoa(24)),
        ("grover8", _grover(8)),
    ]


# ---------------------------------------------------------------------------
# 网格基准
# ---------------------------------------------------------------------------

def benchmark_methods(circuit, methods, backend="qiskit", shots=256, repeats=3):
    """测各方法耗时，取 repeats 次的最小值（压掉单次计时抖动）。"""
    timings = {}
    for m in methods:
        samples = []
        for _ in range(repeats):
            t = _timed_run(circuit, backend, m, shots)
            if t is not None:
                samples.append(t)
        if samples:
            timings[m] = round(min(samples), 4)
    return timings


def benchmark_grid(n_values=(8, 12, 16, 20, 24), backend="qiskit", shots=256, repeats=3):
    """对 clifford / low_tw 两类，逐 n 测各方法耗时。"""
    _timed_run(_ghz(4), backend, "statevector", shots)  # 预热：触发后端导入/编译
    performance = []
    for n in n_values:
        c = _ghz(n)
        performance.append({
            "n": n,
            "class": "clifford",
            "timings": benchmark_methods(
                c, ("statevector", "stabilizer", "matrix_product_state"), backend, shots, repeats
            ),
        })
        c = _chain_rotation(n)
        performance.append({
            "n": n,
            "class": "low_tw",
            "timings": benchmark_methods(
                c, ("statevector", "matrix_product_state"), backend, shots, repeats
            ),
        })
    return performance


def benchmark_general(n_values=(8, 12, 16), backend="qiskit", shots=256, repeats=3):
    """实测高树宽非 Clifford 电路（QFT / Grover）在 statevector 下的耗时。

    这两类电路只有 statevector 能跑（含 mcz / 全连接 cp），本函数不是找交叉点，
    而是验证「general -> statevector」分类，并记录 statevector 随 n 的 2^n 天花板。
    """
    _timed_run(_ghz(4), backend, "statevector", shots)  # 预热
    performance = []
    for n in n_values:
        for name, fn in (("qft", _qft), ("grover", _grover)):
            samples = []
            for _ in range(repeats):
                t = _timed_run(fn(n), backend, "statevector", shots)
                if t is not None:
                    samples.append(t)
            if samples:
                performance.append({
                    "circuit": name,
                    "n": n,
                    "time": round(min(samples), 4),
                })
    return performance


def benchmark_noise(n_values=(2, 4, 6, 8, 10, 12), noise=0.01, backend="qiskit",
                    shots=256, repeats=3, budget=0.5):
    """实测有噪声时 density_matrix 的成本曲线（唯一支持噪声的方法，4^n 资源）。

    返回 {"method", "noise", "budget", "performance", "infeasible_n"}：
    infeasible_n 是首个耗时超过 budget 秒的比特数；网格内都跑得动则为 None。
    """
    _timed_run(_ghz(2), backend, "density_matrix", shots, noise=depolarizing(noise))  # 预热
    performance = []
    infeasible_n = None
    for n in n_values:
        samples = []
        for _ in range(repeats):
            t = _timed_run(_ghz(n), backend, "density_matrix", shots, noise=depolarizing(noise))
            if t is not None:
                samples.append(t)
        if not samples:
            continue
        tmin = round(min(samples), 4)
        performance.append({"n": n, "time": tmin})
        if infeasible_n is None and tmin > budget:
            infeasible_n = n
    return {
        "method": "density_matrix",
        "noise": noise,
        "budget": budget,
        "performance": performance,
        "infeasible_n": infeasible_n,
    }


def derive_decision(performance, margin=0.2):
    """从实测数据推导每类的交叉点。

    交叉点 = 备选方法首次「明显」快于 statevector 的最小 n。要求备选方法至少快
    margin（默认 20%），避免微秒级计时抖动在小 n 处把交叉点来回拨动——小 n 时
    两种方法都在毫秒量级，1% 的差异是噪声，不能据此改路由。
    """
    decision = {}
    for cls, alt in _ALT_METHOD.items():
        rows = [r for r in performance if r["class"] == cls]
        above = None
        for r in sorted(rows, key=lambda x: x["n"]):
            sv = r["timings"].get("statevector")
            at = r["timings"].get(alt)
            if sv is not None and at is not None and at < sv * (1 - margin):
                above = r["n"]
                break
        if above is not None:
            decision[cls] = {"method": alt, "above_n": above}
    return decision


def _meta(backend, shots):
    info = {}
    try:
        import platform

        info["machine"] = platform.platform()
    except Exception:
        pass
    try:
        import numpy

        info["numpy"] = numpy.__version__
    except Exception:
        pass
    try:
        import qiskit_aer

        info["qiskit_aer"] = qiskit_aer.__version__
    except Exception:
        pass
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "backend": backend,
        "shots": shots,
        **info,
    }


def build_benchmark_data(n_values=(8, 12, 16, 20, 24), noise_n=(2, 4, 6, 8, 10, 12),
                         general_n=(8, 12, 16), backend="qiskit", shots=256, repeats=3):
    """跑完整基准，返回结构化数据。

    产出：
        meta          —— 机器/版本信息
        capabilities  —— 静态能力矩阵
        performance   —— clifford/low_tw 交叉点网格
        general       —— QFT/Grover 的 statevector 验证点（记录 2^n 天花板）
        noise         —— density_matrix + 噪声的成本曲线（记录 4^n 成本）
        decision      —— 从 performance 推导的交叉点阈值
    """
    performance = benchmark_grid(n_values, backend=backend, shots=shots, repeats=repeats)
    return {
        "meta": _meta(backend, shots),
        "capabilities": METHOD_CAPABILITIES,
        "performance": performance,
        "general": benchmark_general(general_n, backend=backend, shots=shots, repeats=repeats),
        "noise": benchmark_noise(noise_n, backend=backend, shots=shots, repeats=repeats),
        "decision": derive_decision(performance),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="离线基准：生成调度数据（能力矩阵 + 性能）")
    parser.add_argument("-o", "--output", default="scheduler/data/benchmarks.json")
    parser.add_argument("--backend", default="qiskit")
    parser.add_argument("--shots", type=int, default=256)
    parser.add_argument("--n", default="8,12,16,20,24", help="逗号分隔的比特数网格")
    parser.add_argument("--noise-n", default="2,4,6,8,10,12",
                        help="噪声基准的比特数网格（density_matrix，4^n 成本）")
    parser.add_argument("--general-n", default="8,12,16",
                        help="QFT/Grover 验证点的比特数网格")
    args = parser.parse_args(argv)

    n_values = [int(x) for x in args.n.split(",")]
    noise_n = [int(x) for x in args.noise_n.split(",")]
    general_n = [int(x) for x in args.general_n.split(",")]
    data = build_benchmark_data(
        n_values, noise_n=noise_n, general_n=general_n,
        backend=args.backend, shots=args.shots,
    )

    print("能力矩阵：")
    for m, cap in data["capabilities"].items():
        print(f"  {m:24s} noise={str(cap['noise']):5s} gates={cap['gates']}")
    print("\n性能数据：")
    for r in data["performance"]:
        t = ", ".join(f"{m}={s}s" for m, s in r["timings"].items())
        print(f"  n={r['n']:>3d} {r['class']:8s} {t}")
    print("\n推导的决策表：")
    for cls, d in data["decision"].items():
        print(f"  {cls:8s} -> {d['method']} (n >= {d['above_n']})")

    print("\n高树宽非 Clifford（statevector 验证点）：")
    for r in data["general"]:
        print(f"  {r['circuit']:6s} n={r['n']:>3d}  statevector={r['time']}s")

    noise = data["noise"]
    print("\n噪声（density_matrix，4^n 成本）：")
    for r in noise["performance"]:
        print(f"  n={r['n']:>3d}  density_matrix={r['time']}s")
    print(f"  不可行阈值（>{noise['budget']}s）：{noise['infeasible_n']}")

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n已写入 {args.output}")


if __name__ == "__main__":
    main()
