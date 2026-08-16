"""qshow —— 运行当前电路并在终端 / Jupyter 中显示结果。

两种用法：
    qshow(shots=1024)                     # 运行当前电路并显示
    qshow(result)                          # 直接可视化一个 Result（算法输出等）

运行当前电路后会自动清空电路（每次 qshow 都是一个完整程序），
如需手动清空可调用 reset()。

传入 cache=LocalCacheRegistry(...) 时启用本地调度缓存：第一次跑会记录
「电路特征 -> 后端」，之后微调电路再跑时直接命中缓存，免去重复决策。
"""

import sys
import time

from .backends import get_backend, get_backend_for_method
from .compiler import decompose, route_swaps
from .noise import resolve_noise
from .result import Result
from .scheduler import circuit_features, load_noise_cost, recommend_method, schedule
from .stack import current_circuit, reset

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def qshow(result=None, backend="auto", shots=1024, noise=None, report=False, cache=None,
          coupling_map=None):
    if result is not None:
        if not isinstance(result, Result):
            raise TypeError(
                "qshow 的第一个参数必须是 Result 对象（可用 Result.from_counts / "
                "Result.from_value 构造），或留空以运行当前电路"
            )
        _print_result(result, backend_name=None)
        return result

    circuit = current_circuit()
    if circuit.is_empty():
        print("（当前电路为空，请先用 qgate(...) 构建电路）")
        return None

    # 目标拓扑：先门分解（高阶门 → 基础门），再 SWAP 路由落到耦合图上
    if coupling_map is not None:
        circuit = route_swaps(decompose(circuit), coupling_map)

    if report:
        _print_circuit_report(circuit)

    # 调度：解析电路选 method；传了 cache 且未显式指定 backend 时，后端也查表
    noise_enabled = resolve_noise(noise).enabled
    if noise_enabled:
        _warn_noise_cost(circuit.num_qubits)
    if cache is not None and backend == "auto":
        rec = schedule(circuit, cache=cache, noise=noise_enabled)
        be_name = rec.backend
        method = rec.method
    else:
        be_name = backend
        method = recommend_method(circuit_features(circuit), noise=noise_enabled)

    # 噪声由各后端自行处理（qiskit/native 走 density_matrix，cirq/pennylane
    # 用信道），不做 method 降级；无噪声才按方法能力匹配降级到 native。
    if noise_enabled:
        be = get_backend(be_name)
    else:
        be = get_backend_for_method(be_name, method)
    t0 = time.time()
    result = be.run(circuit, shots=shots, noise=noise, method=method)
    elapsed = time.time() - t0

    if cache is not None:
        cache.report_result(circuit_features(circuit), f"{be.name}:{method}", elapsed, None)

    _print_result(result, backend_name=be.name)
    reset()
    return result


def _warn_noise_cost(n):
    """有噪声时按实测数据提示 density_matrix 的 4^n 成本（无实测数据则静默）。"""
    cost = load_noise_cost()
    infeasible = cost.get("infeasible_n")
    if infeasible is not None and n >= infeasible:
        print(
            f"提示：去极化噪声走 density_matrix（4^n 资源），"
            f"参考机实测 n>={infeasible} 时已超预算。当前 n={n}，可能很慢或内存不足。"
        )


def _print_circuit_report(circuit):
    print("电路资源:")
    print(f"  门数: {circuit.gate_count()}")
    print(f"  深度: {circuit.depth()}")
    print(f"  量子比特: {circuit.num_qubits}")


def _print_result(result, backend_name=None):
    if result.kind == "counts":
        _print_counts(result, backend_name)
    elif result.kind == "value":
        _print_value(result)
    else:
        raise ValueError(f"未知的 Result 类型 '{result.kind}'")


def _print_counts(result, backend_name):
    header = f"后端: {backend_name} | " if backend_name else ""
    print(f"{header}shots: {result.shots}")
    print("结果:")
    counts = result.counts or {}
    total = sum(counts.values()) or 1
    for bitstring in sorted(counts):
        n = counts[bitstring]
        bar = "#" * int(round(40 * n / total))
        print(f"  |{bitstring}>  {n:>6d}  ({n / total:6.1%})  {bar}")


def _print_value(result):
    print("结果:")
    print(f"  {result.value}")
    for key, val in result.metadata.items():
        print(f"  {key} = {val}")
