# Simon / Find hidden period of 2-to-1 function. Precursor to Shor.

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

Simon's Algorithm / Simon 算法

Find hidden period of 2-to-1 function. Precursor to Shor.

---

## 快速上手

```python
from quonic import qgate
from quonic.algorithms import simon
from quonic.gates import CX

# Hidden period s = "101" (decimal 5)
S = 5
N = 3

def simon_oracle(circuit, n):
    """Oracle for f(x) = f(x XOR s)."""
    for i in range(n):
        qgate(CX, i, i + n)
    for i in range(n):
        if (S >> i) & 1:
            qgate(CX, 0, i + n)

result = simon(N, simon_oracle, shots=200)
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Simon circuit](/images/simon_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic import qgate
from quonic.algorithms import simon
from quonic.gates import CX

# Hidden period s = "101" (decimal 5)
S = 5
N = 3

def simon_oracle(circuit, n):
    """Oracle for f(x) = f(x XOR s)."""
    for i in range(n):
        qgate(CX, i, i + n)
    for i in range(n):
        if (S >> i) & 1:
            qgate(CX, 0, i + n)

result = simon(N, simon_oracle, shots=200)
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Cryptography (密码学)
- - Period finding (周期查找)
- - Quantum advantage (量子优势)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/simon/simon.py
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
"""Simon's Algorithm / Simon 算法

Find hidden period of 2-to-1 function. Precursor to Shor.
找到 2-to-1 函数的隐藏周期。Shor 的前身。

## Application / 应用场景
- Cryptography (密码学)
- Period finding (周期查找)
- Quantum advantage (量子优势)

## Output / 输出
Hidden period string.
隐藏周期串。"""

from quonic import qgate
from quonic.algorithms import simon
from quonic.gates import CX

# Hidden period s = "101" (decimal 5)
S = 5
N = 3

def simon_oracle(circuit, n):
    """Oracle for f(x) = f(x XOR s)."""
    for i in range(n):
        qgate(CX, i, i + n)
    for i in range(n):
        if (S >> i) & 1:
            qgate(CX, 0, i + n)

result = simon(N, simon_oracle, shots=200)
print(result.counts)

```

### 运行方式

```bash
python examples/simon/simon.py
```

---

## 下载

- [simon.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/simon/simon.py)
