# Rejection Sampling / 量子拒绝采样

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

量子拒绝采样用于采样。

**经典局限**：
- 经典拒绝采样：经典计算
- 量子拒绝采样：量子计算

**量子优势**：
- 可以高效采样
- 是量子算法的基础

**实际应用**：
- 采样问题
- 量子算法
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import rejection_sampling

# 量子拒绝采样
result = rejection_sampling(distribution, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'00': 512, '11': 512}
```

---

## 原理详解

### 电路图

![Rejection Sampling circuit](/images/rejection_sampling_circuit.svg)

### 数学推导

**量子拒绝采样算法**

目标：从分布中采样。

**算法步骤**：
1. 初始化：分布编码
2. 采样：从分布中采样
3. 接受/拒绝：根据概率接受或拒绝

**数学推导**：
P(accept) = f(x) / (M g(x))
使用量子态表示分布

### 几何解释

量子拒绝采样的几何解释：

1. 分布：在概率空间中的分布
2. 采样：从分布中采样
3. 接受/拒绝：根据概率接受或拒绝

这就像在概率空间中采样。

---

## 代码详解

```python
from quonic.algorithms import rejection_sampling  # 导入算法

# rejection_sampling(distribution, shots)
# distribution: 分布
# shots: 测量次数
result = rejection_sampling(distribution, shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `rejection_sampling(distribution, shots)` | distribution: 分布, shots: 测量次数 | 执行量子拒绝采样 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同分布

```python
# 不同分布
result = rejection_sampling(distribution1, shots=1024)
print(result.counts)

result = rejection_sampling(distribution2, shots=1024)
print(result.counts)
```

### 场景 2：量子拒绝采样用于采样

```python
# 量子拒绝采样可以用于采样
# 从分布中采样
```

### 场景 3：量子拒绝采样用于量子算法

```python
# 量子拒绝采样可以用于量子算法
# 例如：振幅估计
```

---

## 适用场景

### 场景 1：采样问题

量子拒绝采样可以用于采样问题。

### 场景 2：量子算法

量子拒绝采样可以用于量子算法。

### 场景 3：量子算法教学

量子拒绝采样是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: 量子拒绝采样的精度如何？

精度取决于分布复杂度和采样次数。

### Q2: 量子拒绝采样需要多少量子比特？

取决于分布维度。

### Q3: 量子拒绝采样和经典拒绝采样有什么区别？

量子拒绝采样可以高效采样。

### Q4: 量子拒绝采样在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 量子拒绝采样的复杂度如何？

复杂度取决于分布复杂度和采样次数。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 采样问题
- 量子算法基础

### 继续学习

- 量子算法
- 采样问题
- 量子算法教学

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本量子拒绝采样

```python
from quonic.algorithms import rejection_sampling

result = rejection_sampling(distribution, shots=1024)
print(result.counts)
```

### 示例 2：不同分布

```python
from quonic.algorithms import rejection_sampling

result = rejection_sampling(distribution1, shots=1024)
print(result.counts)

result = rejection_sampling(distribution2, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/rejection_sampling/rejection_sampling.py
```

---

## 下载

- [rejection_sampling.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/rejection_sampling/rejection_sampling.py)
