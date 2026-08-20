# Jordan Wigner / Map fermionic Hamiltonian to qubit Hamiltonian.

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

Jordan-Wigner transform / Jordan-Wigner 变换

Map fermionic Hamiltonian to qubit Hamiltonian.

---

## 快速上手

```python
from quonic.algorithms import jordan_wigner_2site

result = jordan_wigner_2site(t=1.0, U=2.0)
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Jordan Wigner circuit](/images/jordan_wigner_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import jordan_wigner_2site

result = jordan_wigner_2site(t=1.0, U=2.0)
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Quantum chemistry (量子化学)
- - Fermionic systems (费米子系统)
- - Hubbard model (Hubbard 模型)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/jordan_wigner/jordan_wigner.py
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
"""Jordan-Wigner transform / Jordan-Wigner 变换

Map fermionic Hamiltonian to qubit Hamiltonian.
将费米子哈密顿量映射到量子比特哈密顿量。

## Application / 应用场景
- Quantum chemistry (量子化学)
- Fermionic systems (费米子系统)
- Hubbard model (Hubbard 模型)

## Output / 输出
Qubit Hamiltonian for simulation.
用于模拟的量子比特哈密顿量。"""

from quonic.algorithms import jordan_wigner_2site

result = jordan_wigner_2site(t=1.0, U=2.0)
print(result.counts)

```

### 运行方式

```bash
python examples/jordan_wigner/jordan_wigner.py
```

---

## 下载

- [jordan_wigner.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/jordan_wigner/jordan_wigner.py)
