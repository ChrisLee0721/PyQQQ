# Grover / Find a specific item in an unsorted list. Classical: O(N) queries. Quantum: O(√N) queries.

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

Search an unsorted database / 搜索无序数据库

Find a specific item in an unsorted list. Classical: O(N) queries. Quantum: O(√N) queries.

---

## 快速上手

```python
from quonic.algorithms import grover

result = grover("11", 2, shots=1024)
print(result.counts)
```

**预期输出**：

```
Target state appears with ~99% probability after optimal iterations.
目标态在最优迭代后以 ~99% 概率出现。
```

---

## 原理详解

### 电路图

![Grover circuit](/images/grover_circuit.svg)

Oracle marks target state, diffusion amplifies its probability.
Oracle 标记目标态，diffusion 放大概率。

---

## 代码详解

```python
from quonic.algorithms import grover

result = grover("11", 2, shots=1024)
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Database search (数据库搜索)
- - Cryptography: searching key space (密码学：搜索密钥空间)
- - Optimization: finding optimal solution (优化：寻找最优解)
- - SAT solving (SAT 求解)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/grover/grover.py
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
"""Search an unsorted database / 搜索无序数据库

Find a specific item in an unsorted list. Classical: O(N) queries. Quantum: O(√N) queries.
在无序列表中找到特定项。经典：O(N) 次查询。量子：O(√N) 次查询。

## Application / 应用场景
- Database search (数据库搜索)
- Cryptography: searching key space (密码学：搜索密钥空间)
- Optimization: finding optimal solution (优化：寻找最优解)
- SAT solving (SAT 求解)

## How it works / 原理
Oracle marks target state, diffusion amplifies its probability.
Oracle 标记目标态，diffusion 放大概率。

## Output / 输出说明
Target state appears with ~99% probability after optimal iterations.
目标态在最优迭代后以 ~99% 概率出现。

## Classical vs Quantum / 经典 vs 量子
For N=4: classical needs 3 queries, quantum needs 1.
对于 N=4：经典需要 3 次查询，量子需要 1 次。
"""


from quonic.algorithms import grover

result = grover("11", 2, shots=1024)
print(result.counts)

```

### 运行方式

```bash
python examples/grover/grover.py
```

---

## 下载

- [grover.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/grover/grover.py)
