# Quantum Monte Carlo / 量子蒙特卡洛

> **Algorithms** / 算法 | 难度：高级 | 预计时间：15 分钟

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

量子蒙特卡洛用于积分和采样。

**经典局限**：
- 经典蒙特卡洛：O(1/√ε) 复杂度
- 量子蒙特卡洛：O(1/ε) 复杂度

**量子优势**：
- 二次加速
- 是量子金融的基础

**实际应用**：
- 量子金融
- 积分问题
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import quantum_monte_carlo

# 量子蒙特卡洛
result = quantum_monte_carlo(function, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'00': 512, '11': 512}
```

---

## 原理详解

### 电路图

![Quantum Monte Carlo circuit](/images/quantum_monte_carlo_circuit.svg)

### 数学推导

**量子蒙特卡洛算法**

目标：估计积分值。

**算法步骤**：
1. 初始化：均匀叠加态
2. Oracle：标记函数值
3. 振幅估计：估计积分值
4. 测量：得到积分估计

**数学推导**：
I = ∫ f(x) dx
≈ (1/N) Σ f(xᵢ)
量子：O(1/ε) vs 经典：O(1/√ε)

### 几何解释

量子蒙特卡洛的几何解释：

1. 初始态：均匀叠加态
2. Oracle：标记函数值
3. 振幅估计：估计积分值
4. 测量：得到积分估计

这就像用量子干涉来估计积分。

---

## 代码详解

```python
from quonic.algorithms import quantum_monte_carlo  # 导入算法

# quantum_monte_carlo(function, shots)
# function: 被积函数
# shots: 测量次数
result = quantum_monte_carlo(function, shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `quantum_monte_carlo(function, shots)` | function: 被积函数, shots: 测量次数 | 执行量子蒙特卡洛 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同函数

```python
# 不同函数
result = quantum_monte_carlo(function1, shots=1024)
print(result.counts)

result = quantum_monte_carlo(function2, shots=1024)
print(result.counts)
```

### 场景 2：量子蒙特卡洛用于量子金融

```python
# 量子蒙特卡洛可以用于量子金融
# 估计期权价格
```

### 场景 3：量子蒙特卡洛用于积分问题

```python
# 量子蒙特卡洛可以用于积分问题
# 估计积分值
```

---

## 适用场景

### 场景 1：量子金融

量子蒙特卡洛可以用于量子金融，估计期权价格。

### 场景 2：积分问题

量子蒙特卡洛可以用于积分问题，估计积分值。

### 场景 3：量子算法教学

量子蒙特卡洛是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: 量子蒙特卡洛的加速比是多少？

二次加速。

### Q2: 量子蒙特卡洛需要多少量子比特？

取决于精度要求。

### Q3: 量子蒙特卡洛和经典蒙特卡洛有什么区别？

量子蒙特卡洛有二次加速。

### Q4: 量子蒙特卡洛在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 量子蒙特卡洛的精度如何？

精度取决于测量次数。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 振幅估计
- 蒙特卡洛方法

### 继续学习

- 量子金融
- 积分问题
- 量子算法

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本量子蒙特卡洛

```python
from quonic.algorithms import quantum_monte_carlo

result = quantum_monte_carlo(function, shots=1024)
print(result.counts)
```

### 示例 2：不同函数

```python
from quonic.algorithms import quantum_monte_carlo

result = quantum_monte_carlo(function1, shots=1024)
print(result.counts)

result = quantum_monte_carlo(function2, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/quantum_monte_carlo/quantum_monte_carlo.py
```

---

## 下载

- [quantum_monte_carlo.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/quantum_monte_carlo/quantum_monte_carlo.py)
