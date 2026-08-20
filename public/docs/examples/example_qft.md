# Qft / Quantum version of DFT. Foundation for many quantum algorithms.

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

Quantum Fourier Transform / 量子傅里叶变换

Quantum version of DFT. Foundation for many quantum algorithms.

---

## 快速上手

```python
from quonic.algorithms import qft

result = qft(n_qubits=3, shots=1024)
print(result.counts)
```

**预期输出**：

```
Transforms computational basis to Fourier basis.
将计算基变换到傅里叶基。
```

---

## 原理详解

### 电路图

![Qft circuit](/images/qft_circuit.svg)

H gates + controlled rotations create frequency-domain representation.
H 门 + 受控旋转创建频域表示。

---

## 代码详解

```python
from quonic.algorithms import qft

result = qft(n_qubits=3, shots=1024)
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Shor's algorithm (Shor 算法)
- - Quantum phase estimation (量子相位估计)
- - Quantum counting (量子计数)
- - Signal processing (信号处理)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/qft/qft.py
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
"""Quantum Fourier Transform / 量子傅里叶变换

Quantum version of DFT. Foundation for many quantum algorithms.
量子版 DFT。许多量子算法的基础。

## Application / 应用场景
- Shor's algorithm (Shor 算法)
- Quantum phase estimation (量子相位估计)
- Quantum counting (量子计数)
- Signal processing (信号处理)

## How it works / 原理
H gates + controlled rotations create frequency-domain representation.
H 门 + 受控旋转创建频域表示。

## Output / 输出说明
Transforms computational basis to Fourier basis.
将计算基变换到傅里叶基。

## Classical vs Quantum / 经典 vs 量子
Classical FFT: O(N log N). Quantum QFT: O(log²N) — exponential speedup.
经典 FFT：O(N log N)。量子 QFT：O(log²N) — 指数加速。
"""


from quonic.algorithms import qft

result = qft(n_qubits=3, shots=1024)
print(result.counts)

```

### 运行方式

```bash
python examples/qft/qft.py
```

---

## 下载

- [qft.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qft/qft.py)
