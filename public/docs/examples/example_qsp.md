# Qsp / Core subroutine for quantum singular value transformation.

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

Quantum Signal Processing / 量子信号处理

Core subroutine for quantum singular value transformation.

---

## 快速上手

```python
from quonic.algorithms import qsp_demo

result = qsp_demo(angle=0.785)
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Qsp circuit](/images/qsp_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import qsp_demo

result = qsp_demo(angle=0.785)
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Quantum algorithms (量子算法)
- - Hamiltonian simulation (哈密顿量模拟)
- - Eigenvalue problems (特征值问题)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/qsp/qsp.py
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
"""Quantum Signal Processing / 量子信号处理

Core subroutine for quantum singular value transformation.
量子奇异值变换的核心子程序。

## Application / 应用场景
- Quantum algorithms (量子算法)
- Hamiltonian simulation (哈密顿量模拟)
- Eigenvalue problems (特征值问题)

## Output / 输出
Transformed signal.
变换后的信号。"""

from quonic.algorithms import qsp_demo

result = qsp_demo(angle=0.785)
print(result.counts)

```

### 运行方式

```bash
python examples/qsp/qsp.py
```

---

## 下载

- [qsp.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qsp/qsp.py)
