# Compare / Compare backends / 比较后端

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

Compare backends / 比较后端

Compare backends / 比较后端

---

## 快速上手

```python
from quonic import QInt, qlt, qshow

x = QInt(3)
x.h()            # uniform superposition |0>..|7>
flag = qlt(x, 4) # flag = 1 iff x < 4

qshow()
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Compare circuit](/images/compare_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic import QInt, qlt, qshow

x = QInt(3)
x.h()            # uniform superposition |0>..|7>
flag = qlt(x, 4) # flag = 1 iff x < 4

qshow()
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
python examples/compare/compare.py
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
"""Compare backends / 比较后端

Compare backends / 比较后端

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

from quonic import QInt, qlt, qshow

x = QInt(3)
x.h()            # uniform superposition |0>..|7>
flag = qlt(x, 4) # flag = 1 iff x < 4

qshow()

```

### 运行方式

```bash
python examples/compare/compare.py
```

---

## 下载

- [compare.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/compare/compare.py)
