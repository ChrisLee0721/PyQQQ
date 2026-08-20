# Swap Test / Estimate overlap between two quantum states.

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

SWAP Test / SWAP 测试

Estimate overlap between two quantum states.

---

## 快速上手

```python
from quonic import qgate
from quonic.algorithms import swap_test
from quonic.gates import X


# prepare(circuit, qubit_index, n_qubits)
def prep_a(circuit, q, n):
    pass  # |0>

def prep_b(circuit, q, n):
    qgate(X, q)  # |1> — orthogonal to |0>

result = swap_test(1, prep_a, prep_b, shots=10000)
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Swap Test circuit](/images/swap_test_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic import qgate
from quonic.algorithms import swap_test
from quonic.gates import X


# prepare(circuit, qubit_index, n_qubits)
def prep_a(circuit, q, n):
    pass  # |0>

def prep_b(circuit, q, n):
    qgate(X, q)  # |1> — orthogonal to |0>

result = swap_test(1, prep_a, prep_b, shots=10000)
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - State comparison (态比较)
- - Kernel estimation (核估计)
- - Fidelity measurement (保真度测量)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/swap_test/swap_test.py
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
"""SWAP Test / SWAP 测试

Estimate overlap between two quantum states.
估计两个量子态之间的重叠。

## Application / 应用场景
- State comparison (态比较)
- Kernel estimation (核估计)
- Fidelity measurement (保真度测量)

## Output / 输出
P(|0⟩) = (1 + |⟨a|b⟩|²) / 2."""

from quonic import qgate
from quonic.algorithms import swap_test
from quonic.gates import X


# prepare(circuit, qubit_index, n_qubits)
def prep_a(circuit, q, n):
    pass  # |0>

def prep_b(circuit, q, n):
    qgate(X, q)  # |1> — orthogonal to |0>

result = swap_test(1, prep_a, prep_b, shots=10000)
print(result.counts)

```

### 运行方式

```bash
python examples/swap_test/swap_test.py
```

---

## 下载

- [swap_test.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/swap_test/swap_test.py)
