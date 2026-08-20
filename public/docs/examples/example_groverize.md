# Groverize / Groverize cwhile / Grover 化 cwhile

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

Groverize cwhile / Grover 化 cwhile

Groverize cwhile / Grover 化 cwhile

---

## 快速上手

```python
import math

from quonic import creg, cwhile, qgate
from quonic.backends import get_backend
from quonic.gates import Ry

flag = creg("flag")
with cwhile(flag, until=0) as loop:
    qgate(Ry(2 * math.pi / 3), 0)   # 单次成功概率 p = 1/4
    flag.measure(0)

static = loop.groverize()   # 编译成静态 Grover 电路（success_prob 自动推断）

# 静态电路无中段反馈，任意后端都能跑；成功态 |00> 的概率从 1/4 放大到 1
print(get_backend("qiskit").run(static, shots=1024).counts)  # {'00': 1024}

# 真机（Quantum Inspire，需登录排队）同样能跑：
# print(get_backend("qi", device="tuna9").run(static, shots=1024).counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Groverize circuit](/images/groverize_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
import math

from quonic import creg, cwhile, qgate
from quonic.backends import get_backend
from quonic.gates import Ry

flag = creg("flag")
with cwhile(flag, until=0) as loop:
    qgate(Ry(2 * math.pi / 3), 0)   # 单次成功概率 p = 1/4
    flag.measure(0)

static = loop.groverize()   # 编译成静态 Grover 电路（success_prob 自动推断）

# 静态电路无中段反馈，任意后端都能跑；成功态 |00> 的概率从 1/4 放大到 1
print(get_backend("qiskit").run(static, shots=1024).counts)  # {'00': 1024}

# 真机（Quantum Inspire，需登录排队）同样能跑：
# print(get_backend("qi", device="tuna9").run(static, shots=1024).counts)
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
python examples/groverize/groverize.py
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
"""Groverize cwhile / Grover 化 cwhile

Groverize cwhile / Grover 化 cwhile

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

import math

from quonic import creg, cwhile, qgate
from quonic.backends import get_backend
from quonic.gates import Ry

flag = creg("flag")
with cwhile(flag, until=0) as loop:
    qgate(Ry(2 * math.pi / 3), 0)   # 单次成功概率 p = 1/4
    flag.measure(0)

static = loop.groverize()   # 编译成静态 Grover 电路（success_prob 自动推断）

# 静态电路无中段反馈，任意后端都能跑；成功态 |00> 的概率从 1/4 放大到 1
print(get_backend("qiskit").run(static, shots=1024).counts)  # {'00': 1024}

# 真机（Quantum Inspire，需登录排队）同样能跑：
# print(get_backend("qi", device="tuna9").run(static, shots=1024).counts)

```

### 运行方式

```bash
python examples/groverize/groverize.py
```

---

## 下载

- [groverize.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/groverize/groverize.py)
