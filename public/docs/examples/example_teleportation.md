# Teleportation / Quantum teleportation / 量子隐形传态

> **Example** / 示例

---

## 目录

- [为什么需要？](#为什么需要)
- [快速上手](#快速上手)
- [原理详解](#原理详解)
- [代码详解](#代码详解)
- [进阶用法](#进阶用法)
- [适用场景](#适用场景)
- [常见问题](#常见问题)
- [学习路径](#学习路径)
- [完整示例代码](#完整示例代码)

---

## 为什么需要？

Quantum teleportation / 量子隐形传态

Quantum teleportation / 量子隐形传态

---

## 快速上手

```python
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
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Teleportation circuit](/images/teleportation_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
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
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Quantum computing (量子计算)
- - Algorithm demonstration (算法演示)
- - Educational (教学)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/teleportation/teleportation.py
```

### Q2: What backend is used?

The example uses the default backend. You can specify a different one:

```python
qshow(backend='qiskit')
```

---

## 学习路径

### 前置知识

- Basic quantum computing concepts
- QuoNic API basics

### 继续学习

- Other examples in this documentation
- QuoNic API reference

---

## 完整示例代码

```python
"""Quantum teleportation / 量子隐形传态

Quantum teleportation / 量子隐形传态

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

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

```

### 运行方式

```bash
python examples/teleportation/teleportation.py
```

---

## 下载

- [teleportation.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/teleportation/teleportation.py)
