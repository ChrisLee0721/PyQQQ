# QAOA TSP / QAOA 旅行商问题

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

QAOA TSP 用于解决旅行商问题。

**经典局限**：
- 经典算法：NP-hard
- 量子算法：近似解

**量子优势**：
- 可以找到近似最优解
- 是量子优化的基础

**实际应用**：
- 组合优化
- 路径规划
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import qaoa_tsp

# QAOA TSP
distances = [[0, 1, 2], [1, 0, 3], [2, 3, 0]]
result = qaoa_tsp(distances, init_params=[0.3, 0.3], maxiter=200)
print(result.value)  # ≈ 6
```

**预期输出**：

```
6
```

---

## 原理详解

### 电路图

![QAOA TSP circuit](/images/qaoa_tsp_circuit.svg)

### 数学推导

**QAOA TSP 算法**

目标：解决旅行商问题。

**算法步骤**：
1. 定义：定义距离矩阵
2. 构建：构建 QAOA 电路
3. 优化：优化参数
4. 输出：输出最短路径

**数学推导**：
min Σᵢⱼ dᵢⱼ xᵢⱼ
s.t. 每个城市访问一次
使用 QAOA 近似求解

### 几何解释

QAOA TSP 的几何解释：

1. 城市：节点
2. 距离：边权重
3. 最短路径：访问所有城市的最短路径

这就像在图上找最短路径。

---

## 代码详解

```python
from quonic.algorithms import qaoa_tsp  # 导入算法

# 定义距离矩阵
distances = [[0, 1, 2], [1, 0, 3], [2, 3, 0]]

# qaoa_tsp(distances, init_params, maxiter)
# distances: 距离矩阵
# init_params: 初始参数
# maxiter: 最大迭代次数
result = qaoa_tsp(distances, init_params=[0.3, 0.3], maxiter=200)

# result.value: 最短路径长度
print(result.value)  # ≈ 6
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `qaoa_tsp(distances, init_params, maxiter)` | distances: 距离矩阵, init_params: 初始参数, maxiter: 最大迭代次数 | 执行 QAOA TSP |
| `result.value` | 无参数 | 最短路径长度 |

---

## 进阶用法

### 场景 1：不同问题

```python
# 不同问题
distances1 = [[0, 1, 2], [1, 0, 3], [2, 3, 0]]
result1 = qaoa_tsp(distances1, init_params=[0.3, 0.3], maxiter=200)
print(result1.value)

distances2 = [[0, 2, 3, 4], [2, 0, 1, 5], [3, 1, 0, 6], [4, 5, 6, 0]]
result2 = qaoa_tsp(distances2, init_params=[0.3, 0.3], maxiter=200)
print(result2.value)
```

### 场景 2：QAOA TSP 用于组合优化

```python
# QAOA TSP 可以用于组合优化
# 解决旅行商问题
```

### 场景 3：QAOA TSP 用于路径规划

```python
# QAOA TSP 可以用于路径规划
# 规划路径
```

---

## 适用场景

### 场景 1：组合优化

QAOA TSP 可以用于组合优化。

### 场景 2：路径规划

QAOA TSP 可以用于路径规划。

### 场景 3：量子算法教学

QAOA TSP 是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: QAOA TSP 的精度如何？

精度取决于参数优化。

### Q2: QAOA TSP 需要多少量子比特？

取决于城市数量。

### Q3: QAOA TSP 和经典算法有什么区别？

QAOA TSP 可以找到近似最优解。

### Q4: QAOA TSP 在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: QAOA TSP 的复杂度如何？

复杂度取决于城市数量。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- QAOA 算法
- 组合优化

### 继续学习

- 组合优化
- 路径规划
- 量子算法教学

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本 QAOA TSP

```python
from quonic.algorithms import qaoa_tsp

distances = [[0, 1, 2], [1, 0, 3], [2, 3, 0]]
result = qaoa_tsp(distances, init_params=[0.3, 0.3], maxiter=200)
print(result.value)
```

### 示例 2：不同问题

```python
from quonic.algorithms import qaoa_tsp

distances1 = [[0, 1, 2], [1, 0, 3], [2, 3, 0]]
result1 = qaoa_tsp(distances1, init_params=[0.3, 0.3], maxiter=200)
print(result1.value)

distances2 = [[0, 2, 3, 4], [2, 0, 1, 5], [3, 1, 0, 6], [4, 5, 6, 0]]
result2 = qaoa_tsp(distances2, init_params=[0.3, 0.3], maxiter=200)
print(result2.value)
```

### 运行方式

```bash
python examples/qaoa_tsp/qaoa_tsp.py
```

---

## 下载

- [qaoa_tsp.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qaoa_tsp/qaoa_tsp.py)
