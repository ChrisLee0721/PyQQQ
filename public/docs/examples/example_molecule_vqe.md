# Molecule Vqe / Compute ground state energy of molecules.

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

Molecular ground state / 分子基态

Compute ground state energy of molecules.

---

## 快速上手

```python
from quonic.algorithms import molecule_vqe_demo

result = molecule_vqe_demo(maxiter=200)
print(f"Ground state energy: {result.value}")
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Molecule Vqe circuit](/images/molecule_vqe_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import molecule_vqe_demo

result = molecule_vqe_demo(maxiter=200)
print(f"Ground state energy: {result.value}")
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Drug discovery (药物发现)
- - Material design (材料设计)
- - Chemical reactions (化学反应)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/molecule_vqe/molecule_vqe.py
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
"""Molecular ground state / 分子基态

Compute ground state energy of molecules.
计算分子的基态能量。

## Application / 应用场景
- Drug discovery (药物发现)
- Material design (材料设计)
- Chemical reactions (化学反应)

## Output / 输出
Ground state energy of molecule.
分子的基态能量。"""

from quonic.algorithms import molecule_vqe_demo

result = molecule_vqe_demo(maxiter=200)
print(f"Ground state energy: {result.value}")

```

### 运行方式

```bash
python examples/molecule_vqe/molecule_vqe.py
```

---

## 下载

- [molecule_vqe.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/molecule_vqe/molecule_vqe.py)
