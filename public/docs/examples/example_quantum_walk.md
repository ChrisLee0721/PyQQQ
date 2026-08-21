# Quantum Walk / 量子行走

> **Algorithms** / 算法 | 难度：中级 | 预计时间：10 分钟

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

量子行走是经典随机行走的量子版本。

**经典局限**：
- 经典随机行走：扩散速度 O(√t)
- 量子行走：扩散速度 O(t)

**量子优势**：
- 二次加速
- 是许多量子算法的基础

**实际应用**：
- 图算法
- 搜索问题
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import quantum_walk

# 量子行走
result = quantum_walk(n_steps=10, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'00': 256, '01': 256, '10': 256, '11': 256}
```

---

## 原理详解

### 电路图

![Quantum Walk circuit](/images/quantum_walk_circuit.svg)

### 数学推导

**量子行走算法**

目标：模拟量子行走。

**算法步骤**：
1. 初始化：|0⟩|0⟩
2. 硬币：Hadamard 门
3. 移动：根据硬币结果移动
4. 重复：多次迭代

**数学推导**：
|ψ₀⟩ = |0⟩|0⟩
|ψ₁⟩ = H|0⟩ ⊗ |0⟩ = (|0⟩+|1⟩)/√2 ⊗ |0⟩
|ψ₂⟩ = 移动后的态
...
|ψₙ⟩ = 行走后的态

### 几何解释

量子行走的几何解释：

1. 初始态：在原点
2. 硬币：决定方向
3. 移动：根据硬币结果移动
4. 重复：多次迭代
5. 结果：量子行走的分布

这就像在直线上随机行走，但有量子干涉。

---

## 代码详解

```python
from quonic.algorithms import quantum_walk  # 导入算法

# quantum_walk(n_steps, shots)
# n_steps: 行走步数
# shots: 测量次数
result = quantum_walk(n_steps=10, shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `quantum_walk(n_steps, shots)` | n_steps: 行走步数, shots: 测量次数 | 执行量子行走 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同步数

```python
# 不同步数
result = quantum_walk(n_steps=5, shots=1024)
print(result.counts)

result = quantum_walk(n_steps=10, shots=1024)
print(result.counts)

result = quantum_walk(n_steps=20, shots=1024)
print(result.counts)
```

### 场景 2：量子行走用于图算法

```python
# 量子行走可以用于图算法
# 例如：图搜索
```

### 场景 3：量子行走用于搜索问题

```python
# 量子行走可以用于搜索问题
# 例如：无序搜索
```

---

## 适用场景

### 场景 1：图算法

量子行走可以用于图算法，例如图搜索。

### 场景 2：搜索问题

量子行走可以用于搜索问题，例如无序搜索。

### 场景 3：量子算法教学

量子行走是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: 量子行走的加速比是多少？

二次加速。

### Q2: 量子行走需要多少量子比特？

取决于行走的空间大小。

### Q3: 量子行走和经典随机行走有什么区别？

量子行走有量子干涉，经典随机行走没有。

### Q4: 量子行走在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 量子行走的复杂度如何？

复杂度取决于行走步数。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- Hadamard 门
- 随机行走

### 继续学习

- 图算法
- 搜索问题
- 量子算法

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本量子行走

```python
from quonic.algorithms import quantum_walk

result = quantum_walk(n_steps=10, shots=1024)
print(result.counts)
```

### 示例 2：不同步数

```python
from quonic.algorithms import quantum_walk

result = quantum_walk(n_steps=5, shots=1024)
print(result.counts)

result = quantum_walk(n_steps=10, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/quantum_walk/quantum_walk.py
```

---

## 下载

- [quantum_walk.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/quantum_walk/quantum_walk.py)
