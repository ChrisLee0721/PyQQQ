# Oracle / Oracle construction / 预言机构造

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

Oracle construction / 预言机构造

Oracle construction / 预言机构造

---

## 快速上手

```python
from quonic.algorithms import grover, oracle


@oracle(3)
def is_five(x):
    return x == 5


result = grover(is_five, 3, shots=1024)
print(result.counts)  # dominated by |101>
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Oracle circuit](/images/oracle_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import grover, oracle


@oracle(3)
def is_five(x):
    return x == 5


result = grover(is_five, 3, shots=1024)
print(result.counts)  # dominated by |101>
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
python examples/oracle/oracle.py
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
"""Oracle construction / 预言机构造

Oracle construction / 预言机构造

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

from quonic.algorithms import grover, oracle


@oracle(3)
def is_five(x):
    return x == 5


result = grover(is_five, 3, shots=1024)
print(result.counts)  # dominated by |101>

```

### 运行方式

```bash
python examples/oracle/oracle.py
```

---

## 下载

- [oracle.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/oracle/oracle.py)
