"""真机 Tuna-9 / Tuna-17 精选浅电路 + 噪声基准。

对每个电路，用「同一条逻辑电路」分别跑：
  - QX emulator（云端模拟器，无噪 → 理想参考）
  - Tuna-9（真机 → 有噪）

以「成功概率 / 分布距离」量化硬件噪声，并与理想值对比。

产出：
  - stdout：人类可读对照
  - qi_hardware.json：结构化结果，供报告书引用

用法：
    .venv-qi/Scripts/python.exe scripts/qi_hardware.py
"""

import json

from quonic import QInt, qeq, qgate, reset
from quonic.backends.qi import QuantumInspireBackend
from quonic.gates import CX, H
from quonic.stack import current_circuit

QX = "QX emulator"
SHOTS = 4096


def _counts(device):
    return QuantumInspireBackend(device).run(current_circuit(), shots=SHOTS)


def _normalize(counts):
    total = sum(counts.values()) or 1
    return {k: v / total for k, v in counts.items()}


def _success(counts, expected):
    """目标态命中率（MSB-first bitstring）。"""
    total = sum(counts.values()) or 1
    return sum(counts.get(s, 0) for s in expected) / total


def _tvd(counts, n_states):
    """与均匀分布的总变差距离 TVD = 1/2 Σ |p_i - 1/N|。"""
    p = _normalize(counts)
    nq = (n_states - 1).bit_length()
    acc = 0.0
    for i in range(n_states):
        key = format(i, f"0{nq}b")
        acc += abs(p.get(key, 0.0) - 1.0 / n_states)
    return acc / 2.0


def _bell():
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)


def _ghz3():
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    qgate(CX, 1, 2)


def _grover2():
    reset()
    from quonic.algorithms import diffusion, mark_state
    for q in range(2):
        qgate(H, q)
    mark_state("11")(current_circuit())
    diffusion(2)


def _qeq():
    reset()
    x = QInt(3, value=5)
    qeq(x, 5)


def _qft3_uniform():
    reset()
    from quonic.qft import add_qft
    add_qft(current_circuit(), (0, 1, 2))


# (name, desc, build_fn, n_qubits, kind, expected 或 n_states)
CASES = [
    ("bell", "Bell state H+CX (2q)", _bell, 2, "success", {"00", "11"}),
    ("ghz3", "3-qubit GHZ (CX chain)", _ghz3, 3, "success", {"000", "111"}),
    ("grover2", "Grover search |11> (2q)", _grover2, 2, "success", {"11"}),
    ("qeq", "Comparator x==5 (mcz, 4q)", _qeq, 4, "success", {"1101"}),
    ("qft3", "QFT(|000>) -> uniform (3q)", _qft3_uniform, 3, "uniform", 8),
]


def _run_case(name, desc, build, n_qubits, kind, target):
    print(f"\n### {name} — {desc}  ({n_qubits} qubits, {SHOTS} shots)")
    ideal = None
    real = None
    try:
        build()
        r = _counts(QX)
        ideal = r.counts
    except Exception as e:  # noqa: BLE001
        print(f"  QX   ERR  {type(e).__name__}: {e}")
        return {"name": name, "desc": desc, "qx_error": f"{type(e).__name__}: {e}"}

    try:
        build()
        r = _counts("Tuna-9")
        real = r.counts
    except Exception as e:  # noqa: BLE001
        print(f"  Tuna9 ERR  {type(e).__name__}: {e}")
        return {"name": name, "desc": desc,
                "qx_error": None, "tuna9_error": f"{type(e).__name__}: {e}",
                "ideal": ideal}

    if kind == "success":
        si = _success(ideal, target)
        sr = _success(real, target)
        print(f"  QX     success={si:.4f}")
        print(f"  Tuna-9 success={sr:.4f}   noise={si - sr:.4f}")
        top = sorted(real.items(), key=lambda kv: -kv[1])[:4]
        print(f"         top={[(k, round(v / sum(real.values()), 4)) for k, v in top]}")
        return {"name": name, "desc": desc, "kind": kind, "n_qubits": n_qubits,
                "target": sorted(target),
                "ideal_success": si, "real_success": sr,
                "noise": si - sr,
                "ideal_counts": ideal, "real_counts": real}
    else:
        di = _tvd(ideal, target)
        dr = _tvd(real, target)
        print(f"  QX     TVD(uniform)={di:.4f}")
        print(f"  Tuna-9 TVD(uniform)={dr:.4f}   ΔTVD={dr - di:.4f}")
        top = sorted(real.items(), key=lambda kv: -kv[1])[:4]
        print(f"         top={[(k, round(v / sum(real.values()), 4)) for k, v in top]}")
        return {"name": name, "desc": desc, "kind": kind, "n_qubits": n_qubits,
                "ideal_tvd": di, "real_tvd": dr, "delta_tvd": dr - di,
                "ideal_counts": ideal, "real_counts": real}


def _tuna17_bell():
    print("\n### bell17 — Bell state on Tuna-17 (跨设备对照)")
    try:
        _bell()
        r = _counts("Tuna-17")
        real = r.counts
        s = _success(real, {"00", "11"})
        print(f"  Tuna-17 success={s:.4f}")
        top = sorted(real.items(), key=lambda kv: -kv[1])[:4]
        print(f"          top={[(k, round(v / sum(real.values()), 4)) for k, v in top]}")
        return {"name": "bell17", "desc": "Bell state on Tuna-17",
                "real_success": s, "real_counts": real}
    except Exception as e:  # noqa: BLE001
        print(f"  Tuna17 ERR  {type(e).__name__}: {e}")
        return {"name": "bell17", "desc": "Bell state on Tuna-17",
                "error": f"{type(e).__name__}: {e}"}


def main():
    report = {"backend_ideal": QX, "backend_real": "Tuna-9",
              "shots": SHOTS, "cases": []}
    print(f"理想参考: {QX}（无噪）   真机: Tuna-9    shots={SHOTS}")
    print("=" * 78)
    for name, desc, build, nq, kind, target in CASES:
        report["cases"].append(_run_case(name, desc, build, nq, kind, target))
    report["cases"].append(_tuna17_bell())

    with open("qi_hardware.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    print("\n已写入 qi_hardware.json")


if __name__ == "__main__":
    main()
