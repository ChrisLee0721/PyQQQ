# Bell / Bell state is the simplest quantum entanglement. Two qubits become correlated: measuring one instantly determines the other.

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

Create a maximally entangled state / 创建最大纠缠态

Bell state is the simplest quantum entanglement. Two qubits become correlated: measuring one instantly determines the other.

---

## 快速上手

```python
from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)
qshow()
```

**预期输出**：

```
Roughly 50% |00⟩ and 50% |11⟩. No |01⟩ or |10⟩ (proves entanglement).
约 50% |00⟩ 和 50% |11⟩。没有 |01⟩ 或 |10⟩（证明纠缠）。
```

---

## 原理详解

### 电路图

![Bell circuit](/images/bell_circuit.svg)

H gate creates superposition, CX gate creates entanglement.
H 门创建叠加态，CX 门创建纠缠。

---

## 代码详解

```python
from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)
qshow()
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

- - Quantum teleportation (隐形传态)
- - Superdense coding (超密编码)
- - Quantum key distribution (量子密钥分发)
- - Testing quantum hardware (测试量子硬件)

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/bell/bell.py
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
"""Create a maximally entangled state / 创建最大纠缠态

Bell state is the simplest quantum entanglement. Two qubits become correlated: measuring one instantly determines the other.
Bell 态是最简单的量子纠缠。两个量子比特关联：测量一个立即确定另一个。

## Application / 应用场景
- Quantum teleportation (隐形传态)
- Superdense coding (超密编码)
- Quantum key distribution (量子密钥分发)
- Testing quantum hardware (测试量子硬件)

## How it works / 原理
H gate creates superposition, CX gate creates entanglement.
H 门创建叠加态，CX 门创建纠缠。

## Output / 输出说明
Roughly 50% |00⟩ and 50% |11⟩. No |01⟩ or |10⟩ (proves entanglement).
约 50% |00⟩ 和 50% |11⟩。没有 |01⟩ 或 |10⟩（证明纠缠）。

## Classical vs Quantum / 经典 vs 量子
Classical: can't create this correlation. Quantum: instant correlation regardless of distance.
经典：无法创建这种关联。量子：无论距离多远都是即时关联。
"""


from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)
qshow()

```

### 运行方式

```bash
python examples/bell/bell.py
```

---

## 下载

- [bell.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/bell/bell.py)
