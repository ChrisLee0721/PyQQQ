# Vqe / Variational Quantum Eigensolver finds the lowest energy of a quantum system.

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

Find ground state energy / 寻找基态能量

Variational Quantum Eigensolver finds the lowest energy of a quantum system.

---

## 快速上手

```python
from quonic.algorithms import vqe

hamiltonian = [(1.0, "ZZ"), (1.0, "XI"), (1.0, "IX")]
result = vqe(hamiltonian, 2, init_params=[0.1] * 4, maxiter=200)
print(result.value)  # ≈ -2.236
```

**预期输出**：

```
Energy value converges to exact ground state energy.
能量值收敛到精确基态能量。
```

---

## 原理详解

### 电路图

![Vqe circuit](/images/vqe_circuit.svg)

Parameterized circuit + classical optimizer minimize energy expectation.
参数化电路 + 经典优化器最小化能量期望值。

---

## 代码详解

```python
from quonic.algorithms import vqe

hamiltonian = [(1.0, "ZZ"), (1.0, "XI"), (1.0, "IX")]
result = vqe(hamiltonian, 2, init_params=[0.1] * 4, maxiter=200)
print(result.value)  # ≈ -2.236
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Quantum chemistry: molecular ground states (量子化学：分子基态)
- - Materials science: new materials (材料科学：新材料)
- - Drug discovery: molecular properties (药物发现：分子性质)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/vqe/vqe.py
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
"""Find ground state energy / 寻找基态能量

Variational Quantum Eigensolver finds the lowest energy of a quantum system.
变分量子本征求解器找到量子系统的最低能量。

## Application / 应用场景
- Quantum chemistry: molecular ground states (量子化学：分子基态)
- Materials science: new materials (材料科学：新材料)
- Drug discovery: molecular properties (药物发现：分子性质)

## How it works / 原理
Parameterized circuit + classical optimizer minimize energy expectation.
参数化电路 + 经典优化器最小化能量期望值。

## Output / 输出说明
Energy value converges to exact ground state energy.
能量值收敛到精确基态能量。

## Classical vs Quantum / 经典 vs 量子
Classical: exponential scaling with system size. Quantum: polynomial.
经典：随系统规模指数增长。量子：多项式。
"""


from quonic.algorithms import vqe

hamiltonian = [(1.0, "ZZ"), (1.0, "XI"), (1.0, "IX")]
result = vqe(hamiltonian, 2, init_params=[0.1] * 4, maxiter=200)
print(result.value)  # ≈ -2.236

```

### 运行方式

```bash
python examples/vqe/vqe.py
```

---

## 下载

- [vqe.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/vqe/vqe.py)
