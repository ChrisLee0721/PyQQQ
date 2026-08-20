# Hsp / General framework for Simon, Shor, and other HSP algorithms.

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

Hidden Subgroup Problem / 隐藏子群问题

General framework for Simon, Shor, and other HSP algorithms.

---

## 快速上手

```python
from quonic.algorithms import hsp_demo

result = hsp_demo()
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Hsp circuit](/images/hsp_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import hsp_demo

result = hsp_demo()
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Factoring (因式分解)
- - Discrete log (离散对数)
- - Graph isomorphism (图同构)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/hsp/hsp.py
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
"""Hidden Subgroup Problem / 隐藏子群问题

General framework for Simon, Shor, and other HSP algorithms.
Simon、Shor 和其他 HSP 算法的通用框架。

## Application / 应用场景
- Factoring (因式分解)
- Discrete log (离散对数)
- Graph isomorphism (图同构)

## Output / 输出
Subgroup generators.
子群生成元。"""

from quonic.algorithms import hsp_demo

result = hsp_demo()
print(result.counts)

```

### 运行方式

```bash
python examples/hsp/hsp.py
```

---

## 下载

- [hsp.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/hsp/hsp.py)
