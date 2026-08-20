# Qaoa Maxcut / Reproduce Farhi et al. (2014) MaxCut optimization.

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

QAOA for MaxCut / QAOA 求解 MaxCut

Reproduce Farhi et al. (2014) MaxCut optimization.

---

## 快速上手

```python
from quonic.algorithms import qaoa_maxcut

edges = [(0, 1), (1, 2), (0, 2)]
result = qaoa_maxcut(edges, 3, p=1, maxiter=100)
print(f"Max cut: {result.value}")
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Qaoa Maxcut circuit](/images/qaoa_maxcut_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import qaoa_maxcut

edges = [(0, 1), (1, 2), (0, 2)]
result = qaoa_maxcut(edges, 3, p=1, maxiter=100)
print(f"Max cut: {result.value}")
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Combinatorial optimization (组合优化)
- - Graph partitioning (图划分)
- - Benchmark (基准测试)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/qaoa_maxcut/qaoa_maxcut.py
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
"""QAOA for MaxCut / QAOA 求解 MaxCut

Reproduce Farhi et al. (2014) MaxCut optimization.
复现 Farhi et al. (2014) MaxCut 优化。

## Application / 应用场景
- Combinatorial optimization (组合优化)
- Graph partitioning (图划分)
- Benchmark (基准测试)

## Output / 输出
MaxCut value ≥ 1.8 on triangle.
三角图上 MaxCut ≥ 1.8。"""

from quonic.algorithms import qaoa_maxcut

edges = [(0, 1), (1, 2), (0, 2)]
result = qaoa_maxcut(edges, 3, p=1, maxiter=100)
print(f"Max cut: {result.value}")

```

### 运行方式

```bash
python examples/qaoa_maxcut/qaoa_maxcut.py
```

---

## 下载

- [qaoa_maxcut.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qaoa_maxcut/qaoa_maxcut.py)
