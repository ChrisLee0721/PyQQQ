"""资源估算：门数 / 深度在编译各阶段的爆炸对比。

对每个电路测量三阶段：
  1. 原 QuoNic IR（高阶门，如 mcz / cp）
  2. QuoNic decompose()（展开到基础门集，引入 ancilla）
  3. qiskit transpile → Tuna-9（原生门集 + SWAP 路由）

产出 resource_estimation.json + docs/figures/resource_explosion.png。

用法：
    .venv-qi/Scripts/python.exe scripts/resource_estimation.py
"""

import json
import os

from quonic import QInt, mul, qeq, qgate, qlt, reset
from quonic.compiler import decompose
from quonic.gates import CX, H
from quonic.stack import current_circuit

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_JSON = os.path.join(HERE, "resource_estimation.json")


def _bell():
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)


def _ghz3():
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    qgate(CX, 1, 2)


def _ghz8():
    reset()
    qgate(H, 0)
    for q in range(1, 8):
        qgate(CX, 0, q)


def _qeq():
    reset()
    x = QInt(3, value=5)
    qeq(x, 5)


def _qlt():
    reset()
    x = QInt(3, value=2)
    qlt(x, 5)


def _mul():
    reset()
    x = QInt(3, value=5)
    mul(x, 3)


def _grover4():
    reset()
    from quonic.algorithms import diffusion, mark_state
    for q in range(4):
        qgate(H, q)
    for _ in range(3):
        mark_state("1111")(current_circuit())
        diffusion(4)


def _transpile_stats(circuit, backend):
    """把 QuoNic 电路转成 qiskit，transpile 到目标后端，返回 (门数, 深度, count_ops)。"""
    from qiskit import QuantumCircuit, transpile

    from quonic.backends.qiskit import QiskitBackend

    qc = QuantumCircuit(circuit.num_qubits, circuit.num_qubits)
    for op in circuit.ops:
        if op.name == "cmeasure":
            qc.measure(op.qubit, op.qubit)
        else:
            QiskitBackend._apply(qc, op)
    qc_compiled = transpile(qc, backend, optimization_level=3)
    ops = qc_compiled.count_ops()
    twoq = sum(v for k, v in ops.items() if k in ("cx", "cz", "swap"))
    return sum(ops.values()), qc_compiled.depth(), ops, twoq


CASES = [
    ("bell", "Bell (2q)", _bell),
    ("ghz3", "GHZ (3q)", _ghz3),
    ("ghz8", "GHZ 星形 (8q)", _ghz8),
    ("qeq", "比较器 x==5 (mcz)", _qeq),
    ("qlt", "比较器 x<5 (QFT)", _qlt),
    ("mul", "乘法 5×3 (QFT)", _mul),
    ("grover4", "Grover |1111> (4q, mcz)", _grover4),
]


def main():
    from qiskit_quantuminspire.qi_provider import QIProvider
    provider = QIProvider()
    backend = provider.get_backend("Tuna-9")

    report = {"backend": "Tuna-9", "cases": {}}
    print(f"后端: Tuna-9（{backend.num_qubits} qubits）")
    print("=" * 88)
    print(f"{'电路':<22}{'原门数':>6}{'分解门数':>8}{'transpile门数':>14}{'2q门':>6}{'深度':>6}")

    for name, desc, build in CASES:
        build()
        orig = current_circuit()
        dec = decompose(orig)
        tg, td, ops, twoq = _transpile_stats(dec, backend)

        report["cases"][name] = {
            "desc": desc,
            "original_gates": orig.gate_count(),
            "original_depth": orig.depth(),
            "original_qubits": orig.num_qubits,
            "decomposed_gates": dec.gate_count(),
            "decomposed_depth": dec.depth(),
            "decomposed_qubits": dec.num_qubits,
            "transpiled_gates": tg,
            "transpiled_depth": td,
            "transpiled_2q_gates": twoq,
            "transpiled_ops": {k: v for k, v in sorted(ops.items())},
        }
        print(
            f"{name:<22}{orig.gate_count():>6}{dec.gate_count():>8}"
            f"{tg:>14}{twoq:>6}{td:>6}"
        )

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    print("\n已写入", OUT_JSON)


if __name__ == "__main__":
    main()
