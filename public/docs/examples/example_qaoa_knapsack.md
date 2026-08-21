# QAOA Knapsack / QAOA 背包问题

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

QAOA Knapsack 用于解决背包问题。

**经典局限**：
- 经典算法：NP-hard
- 量子算法：近似解

**量子优势**：
- 可以找到近似最优解
- 是量子优化的基础

**实际应用**：
- 组合优化
- 资源分配
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import qaoa_knapsack

# QAOA Knapsack
weights = [2, 3, 4]
values = [3, 4, 5]
capacity = 5
result = qaoa_knapsack(weights, values, capacity, init_params=[0.3, 0.3], maxiter=200)
print(result.value)  # ≈ 7
```

**预期输出**：

```
7
```

---

## 原理详解

### 电路图

![QAOA Knapsack circuit](/images/qaoa_knapsack_circuit.svg)

### 数学推导

**QAOA Knapsack 算法**

目标：解决背包问题。

**算法步骤**：
1. 定义：定义物品和容量
2. 构建：构建 QAOA 电路
3. 优化：优化参数
4. 输出：输出最大价值

**数学推导**：
max Σᵢ vᵢ xᵢ
s.t. Σᵢ wᵢ xᵢ ≤ C
使用 QAOA 近似求解

### 几何解释

QAOA Knapsack 的几何解释：

1. 物品：重量和价值
2. 背包：容量限制
3. 最大价值：在容量限制内最大化价值

这就像在背包中装最有价值的物品。

---

## 代码详解

```python
from quonic.algorithms import qaoa_knapsack  # 导入算法

# 定义问题
weights = [2, 3, 4]
values = [3, 4, 5]
capacity = 5

# qaoa_knapsack(weights, values, capacity, init_params, maxiter)
# weights: 物品重量
# values: 物品价值
# capacity: 背包容量
# init_params: 初始参数
# maxiter: 最大迭代次数
result = qaoa_knapsack(weights, values, capacity, init_params=[0.3, 0.3], maxiter=200)

# result.value: 最大价值
print(result.value)  # ≈ 7
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `qaoa_knapsack(weights, values, capacity, init_params, maxiter)` | weights: 物品重量, values: 物品价值, capacity: 背包容量, init_params: 初始参数, maxiter: 最大迭代次数 | 执行 QAOA Knapsack |
| `result.value` | 无参数 | 最大价值 |

---

## 进阶用法

### 场景 1：不同问题

```python
# 不同问题
weights1 = [2, 3, 4]
values1 = [3, 4, 5]
capacity1 = 5
result1 = qaoa_knapsack(weights1, values1, capacity1, init_params=[0.3, 0.3], maxiter=200)
print(result1.value)

weights2 = [1, 2, 3]
values2 = [2, 3, 4]
capacity2 = 4
result2 = qaoa_knapsack(weights2, values2, capacity2, init_params=[0.3, 0.3], maxiter=200)
print(result2.value)
```

### 场景 2：QAOA Knapsack 用于组合优化

```python
# QAOA Knapsack 可以用于组合优化
# 解决背包问题
```

### 场景 3：QAOA Knapsack 用于资源分配

```python
# QAOA Knapsack 可以用于资源分配
# 分配资源
```

---

## 适用场景

### 场景 1：组合优化

QAOA Knapsack 可以用于组合优化。

### 场景 2：资源分配

QAOA Knapsack 可以用于资源分配。

### 场景 3：量子算法教学

QAOA Knapsack 是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: QAOA Knapsack 的精度如何？

精度取决于参数优化。

### Q2: QAOA Knapsack 需要多少量子比特？

取决于物品数量。

### Q3: QAOA Knapsack 和经典算法有什么区别？

QAOA Knapsack 可以找到近似最优解。

### Q4: QAOA Knapsack 在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: QAOA Knapsack 的复杂度如何？

复杂度取决于物品数量。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- QAOA 算法
- 组合优化

### 继续学习

- 组合优化
- 资源分配
- 量子算法教学

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本 QAOA Knapsack

```python
from quonic.algorithms import qaoa_knapsack

weights = [2, 3, 4]
values = [3, 4, 5]
capacity = 5
result = qaoa_knapsack(weights, values, capacity, init_params=[0.3, 0.3], maxiter=200)
print(result.value)
```

### 示例 2：不同问题

```python
from quonic.algorithms import qaoa_knapsack

weights1 = [2, 3, 4]
values1 = [3, 4, 5]
capacity1 = 5
result1 = qaoa_knapsack(weights1, values1, capacity1, init_params=[0.3, 0.3], maxiter=200)
print(result1.value)

weights2 = [1, 2, 3]
values2 = [2, 3, 4]
capacity2 = 4
result2 = qaoa_knapsack(weights2, values2, capacity2, init_params=[0.3, 0.3], maxiter=200)
print(result2.value)
```

### 运行方式

```bash
python examples/qaoa_knapsack/qaoa_knapsack.py
```

---

## 下载

- [qaoa_knapsack.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qaoa_knapsack/qaoa_knapsack.py)
