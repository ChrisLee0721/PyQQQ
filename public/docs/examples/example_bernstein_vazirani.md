# Bernstein Vazirani / Find secret s in f(x) = s·x mod 2. One query suffices.

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

Find hidden bitstring / 找到隐藏比特串

Find secret s in f(x) = s·x mod 2. One query suffices.

---

## 快速上手

```python
from quonic import qgate
from quonic.algorithms import bernstein_vazirani
from quonic.gates import CZ

# Hidden string s = "1010" (decimal 10)
S = 10
N = 4

def bv_oracle(circuit, n):
    """Phase oracle for f(x) = s·x mod 2."""
    for i in range(n):
        if (S >> i) & 1:
            qgate(CZ, i, n)

result = bernstein_vazirani(N, bv_oracle, shots=1024)
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Bernstein Vazirani circuit](/images/bernstein_vazirani_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic import qgate
from quonic.algorithms import bernstein_vazirani
from quonic.gates import CZ

# Hidden string s = "1010" (decimal 10)
S = 10
N = 4

def bv_oracle(circuit, n):
    """Phase oracle for f(x) = s·x mod 2."""
    for i in range(n):
        if (S >> i) & 1:
            qgate(CZ, i, n)

result = bernstein_vazirani(N, bv_oracle, shots=1024)
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Oracle problems (预言机问题)
- - Cryptography (密码学)
- - Learning parity (学习奇偶性)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/bernstein_vazirani/bernstein_vazirani.py
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
"""Find hidden bitstring / 找到隐藏比特串

Find secret s in f(x) = s·x mod 2. One query suffices.
在 f(x) = s·x mod 2 中找到秘密 s。一次查询即可。

## Application / 应用场景
- Oracle problems (预言机问题)
- Cryptography (密码学)
- Learning parity (学习奇偶性)

## Output / 输出
All shots give the hidden string s.
所有测量结果给出隐藏串 s。"""

from quonic import qgate
from quonic.algorithms import bernstein_vazirani
from quonic.gates import CZ

# Hidden string s = "1010" (decimal 10)
S = 10
N = 4

def bv_oracle(circuit, n):
    """Phase oracle for f(x) = s·x mod 2."""
    for i in range(n):
        if (S >> i) & 1:
            qgate(CZ, i, n)

result = bernstein_vazirani(N, bv_oracle, shots=1024)
print(result.counts)

```

### 运行方式

```bash
python examples/bernstein_vazirani/bernstein_vazirani.py
```

---

## 下载

- [bernstein_vazirani.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/bernstein_vazirani/bernstein_vazirani.py)
