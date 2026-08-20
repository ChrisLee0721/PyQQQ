# Amplitude Amplification / Like Grover but with custom state preparation. Boosts success probability.

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

Amplify probability of target state / 放大目标态概率

Like Grover but with custom state preparation. Boosts success probability.

---

## 快速上手

```python
from quonic.algorithms import amplitude_amplification, mark_state

oracle_fn = mark_state("11")
result = amplitude_amplification(2, oracle_fn, shots=1024)
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Amplitude Amplification circuit](/images/amplitude_amplification_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import amplitude_amplification, mark_state

oracle_fn = mark_state("11")
result = amplitude_amplification(2, oracle_fn, shots=1024)
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Quantum algorithms (量子算法)
- - State preparation (态制备)
- - Error mitigation (错误缓解)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/amplitude_amplification/amplitude_amplification.py
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
"""Amplify probability of target state / 放大目标态概率

Like Grover but with custom state preparation. Boosts success probability.
类似 Grover 但支持自定义态制备。提升成功概率。

## Application / 应用场景
- Quantum algorithms (量子算法)
- State preparation (态制备)
- Error mitigation (错误缓解)

## Output / 输出
Target state probability amplified from p to ~1.
目标态概率从 p 放大到 ~1。"""

from quonic.algorithms import amplitude_amplification, mark_state

oracle_fn = mark_state("11")
result = amplitude_amplification(2, oracle_fn, shots=1024)
print(result.counts)

```

### 运行方式

```bash
python examples/amplitude_amplification/amplitude_amplification.py
```

---

## 下载

- [amplitude_amplification.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/amplitude_amplification/amplitude_amplification.py)
