"""Quantum Inspire QX emulator 云端编译链路验证。

用 .venv-qi 环境（含 qiskit-quantuminspire）跑，覆盖：
  - 基础门（H/CX）
  - 多控制 Z（mcz，需 transpile 分解）
  - QFT 加法（controlled Rz）
  - 8-qubit GHZ（非相邻 qubit 的 SWAP 路由）

产出 matrix_qx.json，供报告书引用。

用法：
    .venv-qi/Scripts/python.exe scripts/qi_matrix.py
"""

import json

from quonic import QInt, mul, qeq, qgate, qif, qlt, reset
from quonic.backends.qi import QuantumInspireBackend
from quonic.gates import CX, H, X, Z
from quonic.stack import current_circuit

BACKEND = "QX emulator"


def _signature(result):
    counts = result.counts or {}
    total = sum(counts.values()) or 1
    top = sorted(counts.items(), key=lambda kv: -kv[1])[:3]
    return {"shots": result.shots,
            "top": [[k, round(v / total, 4)] for k, v in top]}


def _run():
    return QuantumInspireBackend(BACKEND).run(current_circuit(), shots=1024)


def _bell():
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    return _run()


def _ghz3():
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    qgate(CX, 1, 2)
    return _run()


def _ghz8():
    reset()
    qgate(H, 0)
    for q in range(1, 8):
        qgate(CX, 0, q)  # 星形连接，迫使 transpile 做 SWAP 路由
    return _run()


def _qft3():
    reset()
    from quonic.qft import add_qft
    qgate(H, 0)
    add_qft(current_circuit(), (0, 1, 2))
    return _run()


def _grover4():
    # 手动重建 grover("1111", 4)：3 次迭代，压测 mcz 分解
    reset()
    from quonic.algorithms import diffusion, mark_state
    for q in range(4):
        qgate(H, q)
    for _ in range(3):
        mark_state("1111")(current_circuit())
        diffusion(4)
    return _run()


def _qeq():
    reset()
    x = QInt(3, value=5)
    qeq(x, 5)
    return _run()


def _qlt():
    reset()
    x = QInt(3, value=2)
    qlt(x, 5)
    return _run()


def _mul():
    reset()
    x = QInt(3, value=5)
    mul(x, 3)
    return _run()


def _qif():
    reset()
    qgate(H, 0)
    qif(0).then(X, 1).else_(Z, 1)
    return _run()


CASES = [
    ("bell", "Bell state H+CX (2q)", _bell),
    ("ghz3", "3-qubit GHZ (CX chain)", _ghz3),
    ("ghz8", "8-qubit GHZ (star, SWAP routing)", _ghz8),
    ("qft3", "3-qubit QFT", _qft3),
    ("grover4", "Grover |1111> 4q (mcz decompose)", _grover4),
    ("qeq", "Comparator x==5 (mcz)", _qeq),
    ("qlt", "Comparator x<5 (QFT adder)", _qlt),
    ("mul", "Multiply 5*3 mod 8 (QFT adder)", _mul),
    ("qif", "Coherent if (cp/rz decompose)", _qif),
]


def main():
    report = {"backend": BACKEND, "cases": {}}
    print(f"后端: {BACKEND}（10 qubit 云端模拟器）")
    print("=" * 78)
    for name, desc, fn in CASES:
        print(f"\n### {name} — {desc}")
        try:
            r = fn()
            sig = _signature(r)
            tops = ", ".join(f"{k}:{p:.0%}" for k, p in sig["top"])
            print(f"  OK   {tops}")
            report["cases"][name] = {"desc": desc, "status": "ok", **sig}
        except Exception as e:  # noqa: BLE001
            print(f"  ERR  {type(e).__name__}: {e}")
            report["cases"][name] = {
                "desc": desc, "status": "error",
                "error": f"{type(e).__name__}: {e}",
            }
    with open("matrix_qx.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    print("\n已写入 matrix_qx.json")


if __name__ == "__main__":
    main()
