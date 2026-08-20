# Hadamard Test / Primitive for inner product estimation.

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

Estimate Re(<ψ|U|ψ>) / 估计 Re(<ψ|U|ψ>)

Primitive for inner product estimation.

---

## 快速上手

```python
from quonic import qgate
from quonic.algorithms import hadamard_test
from quonic.gates import X


# prepare_psi(circuit, qubit_index, n_qubits)
def prep_psi(circuit, q, n):
    qgate(X, q)  # |1>

# apply_u(circuit, qubit_index)
def apply_u(circuit, q):
    pass  # Identity

result = hadamard_test(1, prep_psi, apply_u, shots=10000)
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Hadamard Test circuit](/images/hadamard_test_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic import qgate
from quonic.algorithms import hadamard_test
from quonic.gates import X


# prepare_psi(circuit, qubit_index, n_qubits)
def prep_psi(circuit, q, n):
    qgate(X, q)  # |1>

# apply_u(circuit, qubit_index)
def apply_u(circuit, q):
    pass  # Identity

result = hadamard_test(1, prep_psi, apply_u, shots=10000)
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Quantum algorithms (量子算法)
- - State overlap (态重叠)
- - Expectation values (期望值)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/hadamard_test/hadamard_test.py
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
"""Estimate Re(<ψ|U|ψ>) / 估计 Re(<ψ|U|ψ>)

Primitive for inner product estimation.
内积估计的基本操作。

## Application / 应用场景
- Quantum algorithms (量子算法)
- State overlap (态重叠)
- Expectation values (期望值)

## Output / 输出
Probability of |0⟩ encodes the real part.
|0⟩ 的概率编码实部。"""

from quonic import qgate
from quonic.algorithms import hadamard_test
from quonic.gates import X


# prepare_psi(circuit, qubit_index, n_qubits)
def prep_psi(circuit, q, n):
    qgate(X, q)  # |1>

# apply_u(circuit, qubit_index)
def apply_u(circuit, q):
    pass  # Identity

result = hadamard_test(1, prep_psi, apply_u, shots=10000)
print(result.counts)

```

### 运行方式

```bash
python examples/hadamard_test/hadamard_test.py
```

---

## 下载

- [hadamard_test.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/hadamard_test/hadamard_test.py)
