# Trotter / Trotterization / Trotter 分解

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

Trotterization / Trotter 分解

Trotterization / Trotter 分解

---

## 快速上手

```python
from quonic import qgate, reset
from quonic.backends import get_backend
from quonic.gates import CX, Rz
from quonic.stack import current_circuit


def trotter_step(n_qubits, J, h, dt):
    """Apply one Trotter step for the transverse-field Ising model.

    Args:
        n_qubits: number of qubits
        J: ZZ coupling strength
        h: transverse field strength
        dt: time step
    """
    # ZZ interaction layer
    for i in range(n_qubits - 1):
        # ZZ rotation: CX - Rz(2J*dt) - CX
        qgate(CX, i, i + 1)
        qgate(Rz(2 * J * dt), i + 1)
        qgate(CX, i, i + 1)

    # X field layer
    for i in range(n_qubits):
        qgate(Rx(2 * h * dt), i)


def Rx(theta):
    """Rx gate."""
    from quonic.gates import Rx as _Rx
    return _Rx(theta)


def main():
    n = 3
    J = 1.0
    h = 0.5
    dt = 0.1
    n_steps = 5

    print("Trotter-Suzuki Hamiltonian Simulation")
    print(f"  Model: Transverse-field Ising (n={n}, J={J}, h={h})")
    print(f"  Trotter steps: {n_steps}, dt={dt}")

    reset()

    # Initial state: all |0>
    # Apply Trotter steps
    for _ in range(n_steps):
        trotter_step(n, J, h, dt)

    # Measure
    result = get_backend("native").run(current_circuit(), shots=1000)
    print(f"  Result: {result.counts}")
    print()
    print("The distribution shows the time-evolved state under H.")


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

![Trotter circuit](/images/trotter_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic import qgate, reset
from quonic.backends import get_backend
from quonic.gates import CX, Rz
from quonic.stack import current_circuit


def trotter_step(n_qubits, J, h, dt):
    """Apply one Trotter step for the transverse-field Ising model.

    Args:
        n_qubits: number of qubits
        J: ZZ coupling strength
        h: transverse field strength
        dt: time step
    """
    # ZZ interaction layer
    for i in range(n_qubits - 1):
        # ZZ rotation: CX - Rz(2J*dt) - CX
        qgate(CX, i, i + 1)
        qgate(Rz(2 * J * dt), i + 1)
        qgate(CX, i, i + 1)

    # X field layer
    for i in range(n_qubits):
        qgate(Rx(2 * h * dt), i)


def Rx(theta):
    """Rx gate."""
    from quonic.gates import Rx as _Rx
    return _Rx(theta)


def main():
    n = 3
    J = 1.0
    h = 0.5
    dt = 0.1
    n_steps = 5

    print("Trotter-Suzuki Hamiltonian Simulation")
    print(f"  Model: Transverse-field Ising (n={n}, J={J}, h={h})")
    print(f"  Trotter steps: {n_steps}, dt={dt}")

    reset()

    # Initial state: all |0>
    # Apply Trotter steps
    for _ in range(n_steps):
        trotter_step(n, J, h, dt)

    # Measure
    result = get_backend("native").run(current_circuit(), shots=1000)
    print(f"  Result: {result.counts}")
    print()
    print("The distribution shows the time-evolved state under H.")


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
python examples/trotter/trotter.py
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
"""Trotterization / Trotter 分解

Trotterization / Trotter 分解

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

from quonic import qgate, reset
from quonic.backends import get_backend
from quonic.gates import CX, Rz
from quonic.stack import current_circuit


def trotter_step(n_qubits, J, h, dt):
    """Apply one Trotter step for the transverse-field Ising model.

    Args:
        n_qubits: number of qubits
        J: ZZ coupling strength
        h: transverse field strength
        dt: time step
    """
    # ZZ interaction layer
    for i in range(n_qubits - 1):
        # ZZ rotation: CX - Rz(2J*dt) - CX
        qgate(CX, i, i + 1)
        qgate(Rz(2 * J * dt), i + 1)
        qgate(CX, i, i + 1)

    # X field layer
    for i in range(n_qubits):
        qgate(Rx(2 * h * dt), i)


def Rx(theta):
    """Rx gate."""
    from quonic.gates import Rx as _Rx
    return _Rx(theta)


def main():
    n = 3
    J = 1.0
    h = 0.5
    dt = 0.1
    n_steps = 5

    print("Trotter-Suzuki Hamiltonian Simulation")
    print(f"  Model: Transverse-field Ising (n={n}, J={J}, h={h})")
    print(f"  Trotter steps: {n_steps}, dt={dt}")

    reset()

    # Initial state: all |0>
    # Apply Trotter steps
    for _ in range(n_steps):
        trotter_step(n, J, h, dt)

    # Measure
    result = get_backend("native").run(current_circuit(), shots=1000)
    print(f"  Result: {result.counts}")
    print()
    print("The distribution shows the time-evolved state under H.")


if __name__ == "__main__":
    main()

```

### 运行方式

```bash
python examples/trotter/trotter.py
```

---

## 下载

- [trotter.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/trotter/trotter.py)
