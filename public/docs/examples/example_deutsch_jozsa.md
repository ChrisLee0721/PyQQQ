# Deutsch Jozsa / Determine if f is constant or balanced in one query.

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

Constant or balanced function? / 常数还是平衡函数？

Determine if f is constant or balanced in one query.

---

## 快速上手

```python
from quonic import qgate
from quonic.algorithms import deutsch_jozsa
from quonic.gates import CX

N = 3

def balanced_oracle(circuit, n):
    """Balanced oracle: flip last qubit if first qubit is |1>."""
    qgate(CX, 0, n)

result = deutsch_jozsa(N, balanced_oracle, shots=100)
print(f"Counts: {result.counts}")
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Deutsch Jozsa circuit](/images/deutsch_jozsa_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic import qgate
from quonic.algorithms import deutsch_jozsa
from quonic.gates import CX

N = 3

def balanced_oracle(circuit, n):
    """Balanced oracle: flip last qubit if first qubit is |1>."""
    qgate(CX, 0, n)

result = deutsch_jozsa(N, balanced_oracle, shots=100)
print(f"Counts: {result.counts}")
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Oracle complexity (预言机复杂度)
- - Quantum advantage (量子优势)
- - Function analysis (函数分析)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/deutsch_jozsa/deutsch_jozsa.py
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
"""Constant or balanced function? / 常数还是平衡函数？

Determine if f is constant or balanced in one query.
一次查询确定 f 是常数还是平衡函数。

## Application / 应用场景
- Oracle complexity (预言机复杂度)
- Quantum advantage (量子优势)
- Function analysis (函数分析)

## Output / 输出
All zeros = constant, anything else = balanced.
全零 = 常数，其他 = 平衡。"""

from quonic import qgate
from quonic.algorithms import deutsch_jozsa
from quonic.gates import CX

N = 3

def balanced_oracle(circuit, n):
    """Balanced oracle: flip last qubit if first qubit is |1>."""
    qgate(CX, 0, n)

result = deutsch_jozsa(N, balanced_oracle, shots=100)
print(f"Counts: {result.counts}")

```

### 运行方式

```bash
python examples/deutsch_jozsa/deutsch_jozsa.py
```

---

## 下载

- [deutsch_jozsa.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/deutsch_jozsa/deutsch_jozsa.py)
