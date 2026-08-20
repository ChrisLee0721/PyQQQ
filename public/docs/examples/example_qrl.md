# Qrl / Quantum agent learning in classical environment.

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

Quantum Reinforcement Learning / 量子强化学习

Quantum agent learning in classical environment.

---

## 快速上手

```python
from quonic.algorithms import qrl_demo

result = qrl_demo(n_episodes=10)
print(result.counts)
```

**预期输出**：

```
See code comments for output explanation.
```

---

## 原理详解

### 电路图

![Qrl circuit](/images/qrl_circuit.svg)

See code comments for explanation.

---

## 代码详解

```python
from quonic.algorithms import qrl_demo

result = qrl_demo(n_episodes=10)
print(result.counts)
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Game playing (游戏)
- - Robotics (机器人)
- - Optimization (优化)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/qrl/qrl.py
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
"""Quantum Reinforcement Learning / 量子强化学习

Quantum agent learning in classical environment.
经典环境中的量子智能体学习。

## Application / 应用场景
- Game playing (游戏)
- Robotics (机器人)
- Optimization (优化)

## Output / 输出
Learned policy.
学习到的策略。"""

from quonic.algorithms import qrl_demo

result = qrl_demo(n_episodes=10)
print(result.counts)

```

### 运行方式

```bash
python examples/qrl/qrl.py
```

---

## 下载

- [qrl.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qrl/qrl.py)
