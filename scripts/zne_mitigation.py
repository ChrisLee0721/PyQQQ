"""Zero-Noise Extrapolation (ZNE) 错误缓解示范。

方法：全局 unitary folding + 线性外推。
  1. 逻辑电路 L 折叠成 L (L† L)^k，噪声放大档 λ = 2k+1（1 / 3 / 5）；
  2. 每档 transpile（optimization_level=0 + 固定 initial_layout，避免
     opt=1 把 C†C 抵消，也避免 SWAP）后跑 Tuna-9；
  3. 成功率 p(λ) 线性外推到 λ=0，得缓解后的成功率 p(0)。

注意：Tuna-9 耦合图无 (1,2) 边，3-qubit 链 0-1-2 必须落在物理 0-1-3，
故 QI 返回的计数键宽为 4 bit；用 physical_qubits 把物理比特串映射回逻辑。

产出 zne_mitigation.json。

用法：
    .venv-qi/Scripts/python.exe scripts/zne_mitigation.py
"""

import json
import os

from qiskit import QuantumCircuit, transpile
from qiskit_quantuminspire.qi_provider import QIProvider

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = 4096
BACKEND_NAME = "Tuna-9"


def _fold(circuit, k):
    """全局折叠：C -> C (C† C)^k，逻辑等价但门数变为 (2k+1) 倍。"""
    result = circuit.copy()
    for _ in range(k):
        result = result.compose(circuit.inverse())
        result = result.compose(circuit)
    return result


def _counts_to_logical(raw_counts, physical_qubits):
    """QI 计数键（hex 或二进制，键宽 = 最高物理比特位 + 1）→ 逻辑比特串。

    物理比特串 MSB-first，bit 位置 = 物理 qubit 下标；按 physical_qubits
    （逻辑顺序对应的物理下标列表）抽出逻辑比特。
    """
    width = max(physical_qubits) + 1
    logical = {}
    for key, v in raw_counts.items():
        key = str(key)
        val = int(key, 16) if key.startswith("0x") else int(key, 2)
        bs = format(val, f"0{width}b")
        bits = "".join(bs[width - 1 - pq] for pq in physical_qubits)
        logical[bits] = logical.get(bits, 0) + v
    return logical


def _run(backend, logical_gates, n_qubits, physical_qubits, k, target):
    folded = _fold(logical_gates, k)
    qc = QuantumCircuit(n_qubits, n_qubits)
    qc = qc.compose(folded)
    qc.measure(range(n_qubits), range(n_qubits))
    compiled = transpile(qc, backend, optimization_level=0,
                         initial_layout=physical_qubits)
    job = backend.run(compiled, shots=SHOTS)
    result = job.result(timeout=1800)
    counts = _counts_to_logical(result.get_counts(), physical_qubits)
    total = sum(counts.values()) or 1
    success = sum(counts.get(s, 0) for s in target) / total
    return success, counts


def _linear_extrap(lam, p):
    """对 (λ, p(λ)) 做最小二乘线性拟合，返回 p(λ=0)。"""
    n = len(lam)
    xb = sum(lam) / n
    yb = sum(p) / n
    sxx = sum((x - xb) ** 2 for x in lam)
    sxy = sum((x - xb) * (y - yb) for x, y in zip(lam, p))
    b = sxy / sxx if sxx else 0.0
    return yb - b * xb


def _case(backend, name, n_qubits, build, physical_qubits, target):
    logical = build()
    print(f"\n### {name} — ZNE（{SHOTS} shots，物理比特 {physical_qubits}）")
    lam, probs, all_counts = [], [], {}
    for k in range(3):
        lamda = 2 * k + 1
        p, counts = _run(backend, logical, n_qubits, physical_qubits, k, target)
        lam.append(lamda)
        probs.append(p)
        all_counts[str(lamda)] = counts
        print(f"  λ={lamda}  success={p:.4f}")
    p0 = _linear_extrap(lam, probs)
    gain = p0 - probs[0]
    print(f"  外推 λ=0  success={p0:.4f}  相对 λ=1 拉升 {gain:+.4f} ({gain*100:+.1f}%)")
    return {
        "name": name, "n_qubits": n_qubits, "physical_qubits": physical_qubits,
        "target": sorted(target), "lambda": lam, "success": probs,
        "extrapolated_success": p0, "gain": gain, "counts": all_counts,
    }


def _ghz3():
    c = QuantumCircuit(3)
    c.h(0)
    c.cx(0, 1)
    c.cx(1, 2)
    return c


def _bell():
    c = QuantumCircuit(2)
    c.h(0)
    c.cx(0, 1)
    return c


def main():
    provider = QIProvider()
    backend = provider.get_backend(BACKEND_NAME)
    print(f"后端: {BACKEND_NAME}（{backend.num_qubits} qubits），方法: 全局折叠 + 线性外推")

    cases = [
        _case(backend, "ghz3", 3, _ghz3, [0, 1, 3], {"000", "111"}),
        _case(backend, "bell", 2, _bell, [0, 1], {"00", "11"}),
    ]

    report = {"backend": BACKEND_NAME, "shots": SHOTS,
              "method": "global unitary folding + linear extrapolation",
              "cases": cases}
    with open(os.path.join(HERE, "zne_mitigation.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    print("\n已写入 zne_mitigation.json")


if __name__ == "__main__":
    main()
