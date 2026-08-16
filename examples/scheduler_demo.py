"""调度器收益演示：自动选最优方法 vs 手动选错/默认。

跑三个典型电路，对比「调度器自动选择」与「手动选错或默认」的差异：

一、选对方法（性能）：调度器 vs 手动默认 statevector
    GHZ(24)   —— 纯 Clifford，调度器路由到 stabilizer（默认 statevector 撞 2^n）
    QAOA(24)  —— 低树宽非 Clifford，调度器路由到 matrix_product_state

二、能力矩阵（正确性）：Grover(10) 高树宽非 Clifford
    调度器正确地留在 statevector；手动选错 stabilizer / MPS / density_matrix
    都会因 Aer 不支持 mcz->mcphase 而崩溃。

用法：
    python examples/scheduler_demo.py
"""

import time

from quonic.backends import get_backend, get_backend_for_method
from quonic.ir import Circuit, GateOperation
from quonic.scheduler import schedule


def _ghz(n):
    c = Circuit()
    c.add(GateOperation("h", (0,)))
    for i in range(n - 1):
        c.add(GateOperation("cx", (i, i + 1)))
    return c


def _qaoa(n):
    c = Circuit()
    for q in range(n):
        c.add(GateOperation("ry", (q,), (0.5,)))
    for i in range(n - 1):
        c.add(GateOperation("cx", (i, i + 1)))
    for q in range(n):
        c.add(GateOperation("rz", (q,), (0.4,)))
    return c


def _grover(n):
    c = Circuit()
    for q in range(n):
        c.add(GateOperation("h", (q,)))
    c.add(GateOperation("x", (0,)))
    c.add(GateOperation("ccx", (0, 1, n - 1)))
    c.add(GateOperation("x", (0,)))
    for q in range(n):
        c.add(GateOperation("h", (q,)))
        c.add(GateOperation("x", (q,)))
    c.add(GateOperation("mcz", tuple(range(n))))
    for q in range(n):
        c.add(GateOperation("x", (q,)))
        c.add(GateOperation("h", (q,)))
    return c


def _time(backend, circuit, method, shots=256):
    t0 = time.perf_counter()
    backend.run(circuit, shots=shots, method=method)
    return time.perf_counter() - t0


def _run_auto(circuit, shots=256):
    rec = schedule(circuit)
    be = get_backend_for_method(rec.backend, rec.method)
    return be.name, rec.method, _time(be, circuit, rec.method, shots)


def _run_forced(circuit, method, shots=256):
    be = get_backend("qiskit")
    return "qiskit", method, _time(be, circuit, method, shots)


def main():
    # 预热：触发后端导入/编译，避免首个调用计入耗时
    _run_forced(_ghz(4), "statevector")

    timing = [
        ("GHZ(24)", _ghz(24), "statevector"),
        ("QAOA(24)", _qaoa(24), "statevector"),
    ]

    print("一、选对方法：调度器 vs 手动默认 statevector")
    print(f"{'电路':10s} | {'调度器自动':30s} | {'手动/默认':30s} | 加速")
    print("-" * 92)
    for name, circuit, wrong_method in timing:
        auto_be, auto_m, auto_t = _run_auto(circuit)
        forced_be, forced_m, forced_t = _run_forced(circuit, wrong_method)
        speedup = forced_t / auto_t if auto_t > 0 else float("inf")
        print(
            f"{name:10s} | {auto_be + ':' + auto_m:30s} | "
            f"{forced_be + ':' + forced_m:30s} | {speedup:5.1f}x"
        )
        print(
            f"{'':10s} | {auto_t * 1000:10.1f} ms          | "
            f"{forced_t * 1000:10.1f} ms          |"
        )

    print()
    print("二、能力矩阵：Grover(10) 高树宽非 Clifford，调度器留在 statevector")
    circuit = _grover(10)
    rec = schedule(circuit)
    be = get_backend_for_method(rec.backend, rec.method)
    t = _time(be, circuit, rec.method)
    print(f"  调度器选择：{be.name}:{rec.method}  运行成功 {t * 1000:.1f} ms")
    print()
    print("  手动选错（Aer 不支持 mcz->mcphase，全部崩溃）：")
    for wrong in ("stabilizer", "matrix_product_state", "density_matrix"):
        try:
            _run_forced(circuit, wrong)
            print(f"    {wrong:22s} 成功")
        except Exception as e:  # noqa: BLE001 —— 演示脚本，展示崩溃原因
            print(f"    {wrong:22s} ✗ {type(e).__name__}")


if __name__ == "__main__":
    main()
