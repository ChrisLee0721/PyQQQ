# Qpe / Quantum Phase Estimation / 量子相位估计

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

Quantum Phase Estimation / 量子相位估计

Quantum Phase Estimation / 量子相位估计

---

## 快速上手

```python
import math

from quonic.algorithms import qpe

result = qpe(math.pi, n_precision=3, shots=1024)
print(result.counts)  # dominated by "...010" (rightmost 3 bits -> j = 2)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Qpe circuit](/images/qpe_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
import math

from quonic.algorithms import qpe

result = qpe(math.pi, n_precision=3, shots=1024)
print(result.counts)  # dominated by "...010" (rightmost 3 bits -> j = 2)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Quantum computing (量子计算)
- - Algorithm demonstration (算法演示)
- - Educational (教学)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/qpe/qpe.py
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
"""Quantum Phase Estimation / 量子相位估计

Quantum Phase Estimation / 量子相位估计

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

import math

from quonic.algorithms import qpe

result = qpe(math.pi, n_precision=3, shots=1024)
print(result.counts)  # dominated by "...010" (rightmost 3 bits -> j = 2)

```

### 运行方式

```bash
python examples/qpe/qpe.py
```

---

## 下载

- [qpe.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qpe/qpe.py)
