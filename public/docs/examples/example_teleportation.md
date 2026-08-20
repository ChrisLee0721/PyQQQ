# Quantum Teleportation / 量子隐形传态

> **Communication** / 通信 | 难度：中级 | 预计时间：10 分钟

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

量子隐形传态可以在不直接传输量子比特的情况下传输量子态。

**经典局限**：
- 经典通信无法传输量子态（不可克隆定理）
- 直接传输量子比特容易受噪声影响

**量子优势**：
- 使用纠缠和经典通信传输量子态
- 不违反不可克隆定理（原始态被销毁）
- 是量子网络的基础

**实际应用**：
- 量子网络（量子互联网）
- 量子计算（分布式量子计算）
- 量子密钥分发

---

## 快速上手

```python
import math
from quonic import qgate, qshow, reset
from quonic.gates import CX, CZ, H, Ry
from quonic.stack import current_circuit

# 准备要传输的态
qgate(Ry(math.pi / 3), 0)

# 创建 Bell 对
qgate(H, 1)
qgate(CX, 1, 2)

# Alice 的操作
qgate(CX, 0, 1)
qgate(H, 0)

# Bob 的校正
qgate(CX, 1, 2)
qgate(CX, 0, 2)
qgate(CZ, 0, 2)

qshow()
```

**预期输出**：

```
backend: native | shots: 1024
Result:
  |000>    256  ( 25.0%)  ##########
  |010>    256  ( 25.0%)  ##########
  |100>    256  ( 25.0%)  ##########
  |110>    256  ( 25.0%)  ##########
```

---

## 原理详解

### 电路图

![Quantum Teleportation circuit](/images/teleportation_circuit.svg)

### 数学推导

**Step 1: 准备态**

Alice 有 q₀ 处于态 |ψ⟩ = cos(π/6)|0⟩ + sin(π/6)|1⟩

**Step 2: 创建 Bell 对**

Alice 和 Bob 共享 Bell 对：
|Φ⁺⟩ = (|00⟩ + |11⟩)/√2

**Step 3: Alice 的操作**

Alice 对 q₀ 和 q₁ 执行 CNOT 和 H 门。

**Step 4: 测量**

Alice 测量 q₀ 和 q₁，得到 2 个经典比特。

**Step 5: Bob 的校正**

Bob 根据 Alice 的测量结果校正 q₂。

**Step 6: 结果**

q₂ 现在处于态 |ψ⟩，完成了量子态的传输。

### 几何解释

量子隐形传态的几何解释：

1. Alice 有 |ψ⟩，想传给 Bob
2. Alice 和 Bob 共享 Bell 对
3. Alice 执行 Bell 测量
4. Bob 根据结果校正
5. Bob 得到 |ψ⟩

这就像用纠缠作为量子信道，传输量子态。

---

## 代码详解

```python
import math
from quonic import qgate, qshow, reset
from quonic.gates import CX, CZ, H, Ry
from quonic.stack import current_circuit

# Step 1: 准备要传输的态
qgate(Ry(math.pi / 3), 0)  # q₀ = cos(π/6)|0⟩ + sin(π/6)|1⟩

# Step 2: 创建 Bell 对
qgate(H, 1)      # q₁ → (|0⟩+|1⟩)/√2
qgate(CX, 1, 2)  # q₁,q₂ → (|00⟩+|11⟩)/√2

# Step 3: Alice 的操作
qgate(CX, 0, 1)  # CNOT(q₀, q₁)
qgate(H, 0)       # H(q₀)

# Step 4: Bob 的校正
qgate(CX, 1, 2)  # CNOT(q₁, q₂)
qgate(CX, 0, 2)  # CNOT(q₀, q₂)
qgate(CZ, 0, 2)  # CZ(q₀, q₂)

# Step 5: 测量
qshow()
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `qgate(Ry(π/3), 0)` | Ry: Y 旋转门, π/3: 旋转角度, 0: 量子比特索引 | 准备要传输的态 |
| `qgate(H, 1)` | H: Hadamard 门, 1: 量子比特索引 | 创建叠加态 |
| `qgate(CX, 1, 2)` | CX: CNOT 门, 1: 控制比特, 2: 目标比特 | 创建纠缠 |
| `qshow()` | 无参数 | 运行电路并显示结果 |

---

## 进阶用法

### 场景 1：传输不同态

```python
# 传输 |0⟩
qgate(Ry(0), 0)  # |0⟩
# ... 隐形传态协议 ...

# 传输 |1⟩
qgate(Ry(math.pi), 0)  # |1⟩
# ... 隐形传态协议 ...

# 传输 |+⟩
qgate(H, 0)  # |+⟩
# ... 隐形传态协议 ...
```

### 场景 2：噪声下的隐形传态

```python
# 无噪声
qshow(noise=0)

# 5% 噪声
qshow(noise=0.05)

# 20% 噪声
qshow(noise=0.20)
```

### 场景 3：多跳隐形传态

```python
# 量子中继：多跳隐形传态
# Alice → 中继 → Bob
# 使用纠缠交换
```

---

## 适用场景

### 场景 1：量子网络

量子隐形传态是量子网络的基础，可以在节点之间传输量子态。

### 场景 2：分布式量子计算

在分布式量子计算中，隐形传态用于在不同量子处理器之间传输量子态。

### 场景 3：量子密钥分发

隐形传态可以用于量子密钥分发，实现安全的密钥传输。

---

## 常见问题

### Q1: 隐形传态能超光速通信吗？

不能。隐形传态需要经典通信来传输测量结果，经典通信受光速限制。

### Q2: 隐形传态会违反不可克隆定理吗？

不会。隐形传态会销毁原始态，所以不违反不可克隆定理。

### Q3: 隐形传态需要多少量子比特？

需要 3 个量子比特：1 个要传输的态 + 2 个 Bell 对。

### Q4: 隐形传态的保真度如何？

理想情况下保真度为 1。实际中受噪声影响，保真度会降低。

### Q5: 隐形传态和量子中继有什么关系？

量子中继使用隐形传态和纠缠交换来实现长距离的量子通信。

---

## 学习路径

### 前置知识

- Bell 态（2 量子比特纠缠）
- CNOT 门和 Hadamard 门
- 量子测量

### 继续学习

- 超密编码（用 1 个量子比特传输 2 个经典比特）
- 量子中继（长距离量子通信）
- 量子网络（量子互联网）

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本隐形传态

```python
import math
from quonic import qgate, qshow
from quonic.gates import CX, CZ, H, Ry

qgate(Ry(math.pi / 3), 0)
qgate(H, 1)
qgate(CX, 1, 2)
qgate(CX, 0, 1)
qgate(H, 0)
qgate(CX, 1, 2)
qgate(CX, 0, 2)
qgate(CZ, 0, 2)
qshow()
```

### 示例 2：带噪声的隐形传态

```python
import math
from quonic import qgate, qshow
from quonic.gates import CX, CZ, H, Ry

qgate(Ry(math.pi / 3), 0)
qgate(H, 1)
qgate(CX, 1, 2)
qgate(CX, 0, 1)
qgate(H, 0)
qgate(CX, 1, 2)
qgate(CX, 0, 2)
qgate(CZ, 0, 2)
qshow(noise=0.05)
```

### 运行方式

```bash
python examples/teleportation/teleportation.py
```

---

## 下载

- [teleportation.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/teleportation/teleportation.py)
