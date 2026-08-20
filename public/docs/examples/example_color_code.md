# Color Code / Topological error correction code with transversal gates.

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

Color code error correction / 颜色码纠错

Topological error correction code with transversal gates.

---

## 快速上手

```python
from quonic.algorithms import color_code_demo

result = color_code_demo(shots=100)
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Color Code circuit](/images/color_code_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import color_code_demo

result = color_code_demo(shots=100)
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Fault-tolerant quantum computing (容错量子计算)
- - Topological codes (拓扑码)
- - Quantum memory (量子存储)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/color_code/color_code.py
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
"""Color code error correction / 颜色码纠错

Topological error correction code with transversal gates.
具有横向门的拓扑纠错码。

## Application / 应用场景
- Fault-tolerant quantum computing (容错量子计算)
- Topological codes (拓扑码)
- Quantum memory (量子存储)

## Output / 输出
Encoded logical qubit with error protection.
具有错误保护的编码逻辑比特。"""

from quonic.algorithms import color_code_demo

result = color_code_demo(shots=100)
print(result.counts)

```

### 运行方式

```bash
python examples/color_code/color_code.py
```

---

## 下载

- [color_code.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/color_code/color_code.py)
