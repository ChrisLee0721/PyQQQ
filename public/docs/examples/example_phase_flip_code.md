# Phase Flip Code / 3-qubit code corrects single phase-flip errors.

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

Correct phase-flip errors / 纠正相位翻转错误

3-qubit code corrects single phase-flip errors.

---

## 快速上手

```python
from quonic.algorithms import phase_flip_code

result = phase_flip_code(error_qubit=0, shots=100)
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Phase Flip Code circuit](/images/phase_flip_code_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import phase_flip_code

result = phase_flip_code(error_qubit=0, shots=100)
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Quantum error correction (量子纠错)
- - Phase protection (相位保护)
- - NISQ algorithms (NISQ 算法)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/phase_flip_code/phase_flip_code.py
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
"""Correct phase-flip errors / 纠正相位翻转错误

3-qubit code corrects single phase-flip errors.
3 比特码纠正单个相位翻转错误。

## Application / 应用场景
- Quantum error correction (量子纠错)
- Phase protection (相位保护)
- NISQ algorithms (NISQ 算法)

## Output / 输出
Corrected logical state despite phase errors.
尽管有相位错误，纠正后的逻辑态。"""

from quonic.algorithms import phase_flip_code

result = phase_flip_code(error_qubit=0, shots=100)
print(result.counts)

```

### 运行方式

```bash
python examples/phase_flip_code/phase_flip_code.py
```

---

## 下载

- [phase_flip_code.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/phase_flip_code/phase_flip_code.py)
