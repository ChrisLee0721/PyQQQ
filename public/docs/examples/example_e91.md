# E91 / E91 protocol using entangled pairs and Bell inequality.

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

E91 key distribution / E91 密钥分发

E91 protocol using entangled pairs and Bell inequality.

---

## 快速上手

```python
from quonic.algorithms import e91

result = e91(n_rounds=100)
print(f"Result: {result.value}")
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![E91 circuit](/images/e91_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import e91

result = e91(n_rounds=100)
print(f"Result: {result.value}")
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Quantum key distribution (量子密钥分发)
- - Entanglement verification (纠缠验证)
- - Device-independent QKD (设备无关 QKD)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/e91/e91.py
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
"""E91 key distribution / E91 密钥分发

E91 protocol using entangled pairs and Bell inequality.
E91 协议使用纠缠对和 Bell 不等式。

## Application / 应用场景
- Quantum key distribution (量子密钥分发)
- Entanglement verification (纠缠验证)
- Device-independent QKD (设备无关 QKD)

## Output / 输出
Shared secret key with security verification.
带有安全验证的共享密钥。"""

from quonic.algorithms import e91

result = e91(n_rounds=100)
print(f"Result: {result.value}")

```

### 运行方式

```bash
python examples/e91/e91.py
```

---

## 下载

- [e91.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/e91/e91.py)
