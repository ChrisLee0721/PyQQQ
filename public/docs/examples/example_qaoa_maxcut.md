# QAOA MaxCut / QAOA 最大割

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

QAOA MaxCut 用于解决最大割问题。

**经典局限**：
- 经典算法：NP-hard
- 量子算法：近似解

**量子优势**：
- 可以找到近似最优解
- 是量子优化的基础

**实际应用**：
- 组合优化
- 图分割
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import qaoa_maxcut

# QAOA MaxCut
edges = [(0, 1), (1, 2), (0, 2)]
result = qaoa_maxcut(edges, 3, init_params=[0.3, 0.3], maxiter=200)
print(result.value)  # ≈ 2.0
```

**预期输出**：

```
2.0
```

---

## 原理详解

### 电路图

![QAOA MaxCut circuit](/images/qaoa_maxcut_circuit.svg)

### 数学推导

**QAOA MaxCut 算法**

目标：解决最大割问题。

**算法步骤**：
1. 定义：定义图
2. 构建：构建 QAOA 电路
3. 优化：优化参数
4. 输出：输出最大割值

**数学推导**：
max Σ_{(i,j)∈E} (1 - Z_i Z_j)/2
使用 QAOA 近似求解

### 几何解释

QAOA MaxCut 的几何解释：

1. 图：节点和边
2. 分割：将节点分成两组
3. 最大割：最大化两组之间的边数

这就像在图上找最大割。

---

## 代码详解

```python
from quonic.algorithms import qaoa_maxcut  # 导入算法

# 定义图
edges = [(0, 1), (1, 2), (0, 2)]

# qaoa_maxcut(edges, n_qubits, init_params, maxiter)
# edges: 图的边
# n_qubits: 量子比特数
# init_params: 初始参数
# maxiter: 最大迭代次数
result = qaoa_maxcut(edges, 3, init_params=[0.3, 0.3], maxiter=200)

# result.value: 最大割值
print(result.value)  # ≈ 2.0
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `qaoa_maxcut(edges, n_qubits, init_params, maxiter)` | edges: 图的边, n_qubits: 量子比特数, init_params: 初始参数, maxiter: 最大迭代次数 | 执行 QAOA MaxCut |
| `result.value` | 无参数 | 最大割值 |

---

## 进阶用法

### 场景 1：不同图

```python
# 不同图
edges1 = [(0, 1), (1, 2), (0, 2)]
result1 = qaoa_maxcut(edges1, 3, init_params=[0.3, 0.3], maxiter=200)
print(result1.value)

edges2 = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
result2 = qaoa_maxcut(edges2, 4, init_params=[0.3, 0.3], maxiter=200)
print(result2.value)
```

### 场景 2：QAOA MaxCut 用于组合优化

```python
# QAOA MaxCut 可以用于组合优化
# 解决最大割问题
```

### 场景 3：QAOA MaxCut 用于图分割

```python
# QAOA MaxCut 可以用于图分割
# 分割图
```

---

## 适用场景

### 场景 1：组合优化

QAOA MaxCut 可以用于组合优化。

### 场景 2：图分割

QAOA MaxCut 可以用于图分割。

### 场景 3：量子算法教学

QAOA MaxCut 是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: QAOA MaxCut 的精度如何？

精度取决于参数优化。

### Q2: QAOA MaxCut 需要多少量子比特？

取决于图的大小。

### Q3: QAOA MaxCut 和经典算法有什么区别？

QAOA MaxCut 可以找到近似最优解。

### Q4: QAOA MaxCut 在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: QAOA MaxCut 的复杂度如何？

复杂度取决于图的大小。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- QAOA 算法
- 组合优化

### 继续学习

- 组合优化
- 图分割
- 量子算法教学

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本 QAOA MaxCut

```python
from quonic.algorithms import qaoa_maxcut

edges = [(0, 1), (1, 2), (0, 2)]
result = qaoa_maxcut(edges, 3, init_params=[0.3, 0.3], maxiter=200)
print(result.value)
```

### 示例 2：不同图

```python
from quonic.algorithms import qaoa_maxcut

edges1 = [(0, 1), (1, 2), (0, 2)]
result1 = qaoa_maxcut(edges1, 3, init_params=[0.3, 0.3], maxiter=200)
print(result1.value)

edges2 = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
result2 = qaoa_maxcut(edges2, 4, init_params=[0.3, 0.3], maxiter=200)
print(result2.value)
```

### 运行方式

```bash
python examples/qaoa_maxcut/qaoa_maxcut.py
```

---

## 下载

- [qaoa_maxcut.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qaoa_maxcut/qaoa_maxcut.py)
