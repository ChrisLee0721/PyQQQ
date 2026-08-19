"""Teleport quantum state / 隐形传态量子态

Transfer quantum state from one location to another using entanglement.
使用纠缠将量子态从一个位置传送到另一个位置。

## Application / 应用场景
- Quantum communication (量子通信)
- Quantum networks (量子网络)
- Distributed quantum computing (分布式量子计算)

## How it works / 原理
Bell pair + Bell measurement + classical communication + correction.
Bell 对 + Bell 测量 + 经典通信 + 纠正。

## Output / 输出说明
Target qubit receives the original state (with classical corrections).
目标量子比特接收原始态（需要经典纠正）。

## Classical vs Quantum / 经典 vs 量子
Classical: can't transmit unknown quantum state. Quantum: instant transfer.
经典：无法传输未知量子态。量子：即时传输。
"""


import math

from quonic import qgate, qshow, reset
from quonic.gates import CX, CZ, H, Ry
from quonic.stack import current_circuit


def teleport():
    """Run quantum teleportation protocol."""
    # Prepare state to teleport: Ry(π/3)|0> on qubit 0
    qgate(Ry(math.pi / 3), 0)

    # Create Bell pair between q1 and q2
    qgate(H, 1)
    qgate(CX, 1, 2)

    # Alice's operations: CNOT(q0, q1) then H(q0)
    qgate(CX, 0, 1)
    qgate(H, 0)

    # Measure q0 and q1 (classical communication)
    # Bob applies corrections based on measurement results
    # For simplicity, we show the full circuit without mid-circuit measurement

    # Corrections (would be conditional in real implementation):
    # if q1 == 1: X(q2)
    # if q0 == 1: Z(q2)

    # For demo, apply both corrections (one will be identity)
    qgate(CX, 1, 2)
    qgate(CX, 0, 2)
    qgate(CZ, 0, 2)

    return current_circuit()


def main():
    reset()
    circuit = teleport()
    print("Quantum Teleportation:")
    print(f"  Circuit: {circuit.gate_count()} gates, {circuit.num_qubits} qubits")
    result = qshow()
    print(f"  Result: {result.counts}")


if __name__ == "__main__":
    main()
