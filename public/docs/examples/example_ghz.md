# GHZ State / GHZ 态

> **Foundational** / 基础 | 难度：初级 | 预计时间：5 分钟

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

GHZ 态是多量子比特纠缠的经典例子，展示了量子力学的非局域性。

**经典局限**：
- 经典物理无法创建三体以上的纠缠
- 经典关联最多只能有两体关联

**量子优势**：
- GHZ 态是三体纠缠的最基本形式
- 违反 Mermin 不等式，证明量子力学的非局域性更强
- 是量子纠错、量子密钥分发的基础

**实际应用**：
- 量子纠错（GHZ 码）
- 量子密钥分发（多方量子密钥）
- 量子传感（增强测量精度）

---

## 快速上手

```python
from quonic import qgate, qshow
from quonic.gates import CX, H

# 创建 GHZ 态
qgate(H, 0)      # Hadamard 门：创建叠加态
qgate(CX, 0, 1)  # CNOT 门：纠缠 q₀ 和 q₁
qgate(CX, 1, 2)  # CNOT 门：纠缠 q₁ 和 q₂
qshow()           # 测量并显示结果
```

**预期输出**：

```
backend: native | shots: 1024
Result:
  |000>    512  ( 50.0%)  ####################
  |111>    512  ( 50.0%)  ####################
```

---

## 原理详解

### 电路图

![GHZ State circuit](/images/ghz_circuit.svg)

### 数学推导

**Step 1: 初始状态**

三个量子比特都从 |0⟩ 开始：
|ψ₀⟩ = |000⟩

**Step 2: Hadamard 门**

对 q₀ 施加 H 门：
H|0⟩ = (|0⟩ + |1⟩)/√2

所以状态变为：
|ψ₁⟩ = (|0⟩ + |1⟩)/√2 ⊗ |00⟩ = (|000⟩ + |100⟩)/√2

**Step 3: 第一个 CNOT 门**

CNOT(q₀, q₁)：如果 q₀ 是 |1⟩，就翻转 q₁
|ψ₂⟩ = (|000⟩ + |110⟩)/√2

**Step 4: 第二个 CNOT 门**

CNOT(q₁, q₂)：如果 q₁ 是 |1⟩，就翻转 q₂
|ψ₃⟩ = (|000⟩ + |111⟩)/√2

**Step 5: 测量概率**

测量时：
- P(|000⟩) = |1/√2|² = 0.5
- P(|111⟩) = |1/√2|² = 0.5
- 其他状态概率 = 0

### 几何解释

GHZ 态是 Bell 态的推广：
- Bell 态：2 量子比特纠缠 (|00⟩+|11⟩)/√2
- GHZ 态：3+ 量子比特纠缠 (|000⟩+|111⟩)/√2

在 Bloch 球上，GHZ 态不能用单个球描述——
它是多体纠缠，需要更高维度的几何表示。

---

## 代码详解

```python
from quonic import qgate, qshow  # 导入核心 API
from quonic.gates import CX, H   # 导入门定义

# Step 1: 创建叠加态
qgate(H, 0)      # 对 q₀ 施加 H 门
                  # 效果：q₀ → (|0⟩+|1⟩)/√2

# Step 2: 纠缠 q₀ 和 q₁
qgate(CX, 0, 1)  # CNOT 门：控制=q₀，目标=q₁
                  # 效果：(|00⟩+|11⟩)/√2 ⊗ |0⟩

# Step 3: 纠缠 q₁ 和 q₂
qgate(CX, 1, 2)  # CNOT 门：控制=q₁，目标=q₂
                  # 效果：(|000⟩+|111⟩)/√2

# Step 4: 测量
qshow()           # 运行电路并显示结果
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `qgate(H, 0)` | H: Hadamard 门, 0: 量子比特索引 | 对 q₀ 施加 H 门 |
| `qgate(CX, 0, 1)` | CX: CNOT 门, 0: 控制比特, 1: 目标比特 | 纠缠 q₀ 和 q₁ |
| `qgate(CX, 1, 2)` | CX: CNOT 门, 1: 控制比特, 2: 目标比特 | 纠缠 q₁ 和 q₂ |
| `qshow()` | 无参数 | 运行电路并显示结果 |

---

## 进阶用法

### 场景 1：N 量子比特 GHZ 态

```python
# 5 量子比特 GHZ 态
n = 5
qgate(H, 0)
for i in range(n - 1):
    qgate(CX, i, i + 1)
qshow()
```

### 场景 2：噪声下的 GHZ 态

```python
# 无噪声
qshow(noise=0)

# 5% 噪声
qshow(noise=0.05)

# 20% 噪声
qshow(noise=0.20)
```

### 场景 3：GHZ 态用于量子纠错

```python
# GHZ 态可以用于检测错误
# 如果测量结果不是全 0 或全 1，说明有错误
qgate(H, 0)
qgate(CX, 0, 1)
qgate(CX, 1, 2)
# 添加错误
qgate(X, 1)  # 人为错误
qshow()  # 结果会显示非 GHZ 态
```

---

## 适用场景

### 场景 1：量子纠错

GHZ 态用于检测量子比特的错误。如果测量结果不是全 0 或全 1，说明有错误发生。

### 场景 2：量子密钥分发

多方量子密钥分发使用 GHZ 态，让多个参与方共享密钥。

### 场景 3：量子传感

GHZ 态可以增强测量精度，用于量子传感和量子计量。

---

## 常见问题

### Q1: GHZ 态和 Bell 态有什么区别？

Bell 态是 2 量子比特纠缠，GHZ 态是 3+ 量子比特纠缠。GHZ 态是 Bell 态的推广。

### Q2: 如何验证 GHZ 态？

测量结果应该只有 |000⟩ 和 |111⟩，没有其他状态。如果看到其他状态，说明有噪声或错误。

### Q3: GHZ 态有多少个量子比特？

GHZ 态可以有任意数量的量子比特。常见的有 3、5、7、10 个等。

### Q4: GHZ 态在量子纠错中怎么用？

GHZ 态用于检测错误。如果测量结果不是全 0 或全 1，说明有错误发生，可以进行纠错。

### Q5: GHZ 态的数学表达式是什么？

N 量子比特 GHZ 态：(|00...0⟩ + |11...1⟩)/√2。例如 3 量子比特：(|000⟩ + |111⟩)/√2。

---

## 学习路径

### 前置知识

- 量子比特的基本概念
- Bell 态（2 量子比特纠缠）
- CNOT 门的作用

### 继续学习

- 量子纠错（使用 GHZ 态检测错误）
- 量子密钥分发（多方量子密钥）
- 量子传感（增强测量精度）

### 难度等级

- 当前：初级
- 下一步：中级

---

## 完整示例代码

### 示例 1：基本 GHZ 态

```python
from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)
qgate(CX, 1, 2)
qshow()
```

### 示例 2：5 量子比特 GHZ 态

```python
from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
for i in range(4):
    qgate(CX, i, i + 1)
qshow()
```

### 运行方式

```bash
python examples/ghz/ghz.py
```

---

## 下载

- [ghz.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/ghz/ghz.py)
