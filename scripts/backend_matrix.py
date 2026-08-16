"""多后端矩阵测试：遍历算法 × 本地后端，收集支持性与结果一致性。

产出：
  - stdout：人类可读矩阵
  - matrix_local.json：结构化结果，供报告书引用

用法：
    .venv/Scripts/python.exe scripts/backend_matrix.py
"""

import json

from quonic import QInt, cif, creg, cwhile, mul, qeq, qgate, qif, qlt, reset
from quonic.backends import get_backend
from quonic.gates import CX, H, X, Z
from quonic.stack import current_circuit

BACKENDS = ["qiskit", "cirq", "pennylane", "native"]


def _bit(bs, q):
    """bs 为 MSB 在前，q=0 为最低位。"""
    return int(bs[len(bs) - 1 - q])


def _reg(bs, qubits):
    return sum(_bit(bs, q) << i for i, q in enumerate(qubits))


def _signature(result):
    """把 Result 归一化成可跨后端比较的签名。"""
    if result.kind == "counts":
        counts = result.counts or {}
        total = sum(counts.values()) or 1
        top = sorted(counts.items(), key=lambda kv: -kv[1])[:3]
        return {"type": "counts", "shots": result.shots,
                "top": [[k, round(v / total, 4)] for k, v in top]}
    return {"type": "value", "value": result.value}


# ---------------------------------------------------------------------------
# 用例：每个 fn(backend) -> Result
# ---------------------------------------------------------------------------

def _bell(backend):
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    return get_backend(backend).run(current_circuit(), shots=1024)


def _ghz3(backend):
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    qgate(CX, 1, 2)
    return get_backend(backend).run(current_circuit(), shots=1024)


def _qft3(backend):
    reset()
    from quonic.qft import add_qft
    qgate(H, 0)  # 输入 |001>，QFT 后应是带相位的均匀叠加
    add_qft(current_circuit(), (0, 1, 2))
    return get_backend(backend).run(current_circuit(), shots=1024)


def _grover2(backend):
    from quonic.algorithms import grover
    return grover("11", 2, shots=1024, backend=backend)


def _grover4(backend):
    from quonic.algorithms import grover
    return grover("1111", 4, shots=1024, backend=backend)


def _qpe_pi(backend):
    from quonic.algorithms import qpe
    return qpe(3.141592653589793, 3, shots=1024, backend=backend)


def _counting(backend):
    from quonic.algorithms import oracle, quantum_counting

    @oracle(3)
    def f(x):
        return x & 1 == 0  # 偶数共 4 个

    return quantum_counting(f, 3, shots=2048, backend=backend)


def _shor15(backend):
    from quonic.algorithms import shor
    return shor(15, a=7, t=6, shots=256, backend=backend)


def _qeq(backend):
    reset()
    x = QInt(3, value=5)
    qeq(x, 5)
    return get_backend(backend).run(current_circuit(), shots=256)


def _qlt(backend):
    reset()
    x = QInt(3, value=2)
    qlt(x, 5)
    return get_backend(backend).run(current_circuit(), shots=256)


def _mul(backend):
    reset()
    x = QInt(3, value=5)
    mul(x, 3)  # 5*3 mod 8 = 7
    return get_backend(backend).run(current_circuit(), shots=256)


def _qif(backend):
    reset()
    qgate(H, 0)
    qif(0).then(X, 1).else_(Z, 1)
    return get_backend(backend).run(current_circuit(), shots=1024)


def _cif(backend):
    reset()
    qgate(X, 0)
    flag = creg("flag")
    flag.measure(0)
    cif(flag).then(X, 1).else_(X, 1)
    return get_backend(backend).run(current_circuit(), shots=256)


def _cwhile(backend):
    reset()
    flag = creg("flag")
    with cwhile(flag, until=1):
        qgate(X, 0)
        flag.measure(0)
    return get_backend(backend).run(current_circuit(), shots=256)


CASES = [
    ("bell", "Bell state H+CX", _bell),
    ("ghz3", "3-qubit GHZ", _ghz3),
    ("qft3", "3-qubit QFT", _qft3),
    ("grover2", "Grover search |11> (2q)", _grover2),
    ("grover4", "Grover search |1111> (4q, mcz)", _grover4),
    ("qpe_pi", "QPE phase π (3-bit)", _qpe_pi),
    ("counting", "Quantum counting (N=8, M=4)", _counting),
    ("shor15", "Shor factor 15", _shor15),
    ("qeq", "Comparator x==5", _qeq),
    ("qlt", "Comparator x<5", _qlt),
    ("mul", "Multiply 5*3 mod 8", _mul),
    ("qif", "Coherent if (superposition)", _qif),
    ("cif", "Classical if (measure-branch)", _cif),
    ("cwhile", "Classical while (RUS)", _cwhile),
]


def main():
    report = {"backends": BACKENDS, "cases": {}}
    print("=" * 78)
    print("多后端矩阵：算法 × 本地后端")
    print("=" * 78)
    for name, desc, fn in CASES:
        row = {}
        print(f"\n### {name} — {desc}")
        for b in BACKENDS:
            try:
                r = fn(b)
                row[b] = {"status": "ok", ** _signature(r)}
                sig = row[b]
                if sig["type"] == "counts":
                    tops = ", ".join(f"{k}:{p:.0%}" for k, p in sig["top"])
                    print(f"  {b:>10}  OK   {tops}")
                else:
                    print(f"  {b:>10}  OK   value={sig['value']}")
            except Exception as e:  # noqa: BLE001
                row[b] = {"status": "error",
                          "error": f"{type(e).__name__}: {e}"}
                print(f"  {b:>10}  ERR  {type(e).__name__}: {e}")
        report["cases"][name] = {"desc": desc, "backends": row}

    with open("matrix_local.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    print("\n已写入 matrix_local.json")


if __name__ == "__main__":
    main()
