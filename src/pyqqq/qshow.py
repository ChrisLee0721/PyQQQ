"""qshow —— 运行当前电路并在终端 / Jupyter 中显示结果。

运行后会自动清空当前电路（每次 qshow 都是一个完整程序），
如需手动清空可调用 reset()。
"""

import sys

from .backends import get_backend
from .stack import current_circuit, reset

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def qshow(backend="qiskit", shots=1024):
    circuit = current_circuit()
    if circuit.is_empty():
        print("（当前电路为空，请先用 qgate(...) 构建电路）")
        return None

    be = get_backend(backend)
    result = be.run(circuit, shots=shots)
    _print_result(be.name, shots, result)
    reset()
    return result


def _print_result(backend_name, shots, result):
    counts = result["counts"]
    total = sum(counts.values()) or 1
    print(f"后端: {backend_name} | shots: {shots}")
    print("结果:")
    for bitstring in sorted(counts):
        n = counts[bitstring]
        bar = "#" * int(round(40 * n / total))
        print(f"  |{bitstring}>  {n:>6d}  ({n / total:6.1%})  {bar}")
