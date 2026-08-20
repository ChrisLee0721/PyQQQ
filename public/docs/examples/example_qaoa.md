# QAOA / 量子近似优化算法

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

QAOA 是混合量子-经典算法，用于解决组合优化问题。

**经典局限**：
- 组合优化问题：NP-hard，经典算法需要指数时间
- 例如 MaxCut、旅行商问题、背包问题

**量子优势**：
- QAOA 使用量子计算机探索解空间
- 经典优化器更新参数
- 对于某些问题，QAOA 可以提供多项式加速

**实际应用**：
- MaxCut（图分割）
- 旅行商问题
- 背包问题
- 投资组合优化

---

## 快速上手

```python
from quonic.algorithms import qaoa_maxcut

# MaxCut 问题
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

![QAOA circuit](/images/qaoa_circuit.svg)

### 数学推导

**Step 1: 定义问题**

MaxCut：将图的顶点分成两组，最大化两组之间的边数。

**Step 2: 构建哈密顿量**

H_C = Σ_{(i,j)∈E} (1 - Z_i Z_j)/2

**Step 3: QAOA 电路**

|ψ(γ,β)⟩ = e^{-iβ_p H_M} e^{-iγ_p H_C} ... e^{-iβ₁ H_M} e^{-iγ₁ H_C} |+⟩

**Step 4: 优化**

经典优化器找到最优的 γ 和 β。

**Step 5: 测量**

测量得到近似最优解。

### 几何解释

QAOA 的几何解释：

1. 初始态：均匀叠加态 |+⟩^n
2. Cost 算子：标记好解
3. Mixer 算子：探索解空间
4. 交替执行：逐步逼近最优解

这就像在解空间中搜索，每次迭代都更接近最优解。

---

## 代码详解

```python
from quonic.algorithms import qaoa_maxcut  # 导入 QAOA 算法

# 定义 MaxCut 问题
edges = [(0, 1), (1, 2), (0, 2)]  # 图的边

# qaoa_maxcut(edges, n_qubits, init_params, maxiter)
# edges: 图的边
# n_qubits: 量子比特数
# init_params: 初始参数 [γ, β]
# maxiter: 最大迭代次数
result = qaoa_maxcut(edges, 3, init_params=[0.3, 0.3], maxiter=200)

# result.value: MaxCut 值
print(result.value)  # ≈ 2.0
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `qaoa_maxcut(edges, n_qubits, init_params, maxiter)` | edges: 图的边, n_qubits: 量子比特数, init_params: 初始参数, maxiter: 最大迭代次数 | 执行 QAOA MaxCut |
| `result.value` | 无参数 | MaxCut 值 |

---

## 进阶用法

### 场景 1：不同图结构

```python
# 完全图
edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
result = qaoa_maxcut(edges, 4, init_params=[0.3, 0.3], maxiter=200)
print(result.value)

# 路径图
edges = [(0, 1), (1, 2), (2, 3)]
result = qaoa_maxcut(edges, 4, init_params=[0.3, 0.3], maxiter=200)
print(result.value)
```

### 场景 2：不同层数

```python
# 1 层 QAOA
result = qaoa_maxcut(edges, 3, init_params=[0.3], maxiter=200)
print(result.value)

# 2 层 QAOA
result = qaoa_maxcut(edges, 3, init_params=[0.3, 0.3], maxiter=200)
print(result.value)

# 3 层 QAOA
result = qaoa_maxcut(edges, 3, init_params=[0.3, 0.3, 0.3], maxiter=200)
print(result.value)
```

### 场景 3：QAOA 用于其他优化问题

```python
# QAOA 可以用于其他组合优化问题
# 例如：旅行商问题、背包问题
# 需要构建对应的问题哈密顿量
```

---

## 适用场景

### 场景 1：MaxCut

将图的顶点分成两组，最大化两组之间的边数。用于网络分割、社区发现等。

### 场景 2：旅行商问题

找到访问所有城市的最短路径。用于物流、路径规划等。

### 场景 3：投资组合优化

在风险和收益之间找到最优平衡。用于金融、投资等。

---

## 常见问题

### Q1: QAOA 的近似比如何？

对于 MaxCut，QAOA 的近似比约 0.69（1 层）。层数越多，近似比越高。

### Q2: QAOA 需要多少量子比特？

取决于问题规模。对于 n 个顶点的图，需要 n 个量子比特。

### Q3: QAOA 和 VQE 有什么区别？

QAOA 用于组合优化，VQE 用于寻找基态能量。两者都是变分算法，但应用场景不同。

### Q4: QAOA 在 NISQ 设备上能跑吗？

可以。QAOA 是 NISQ 设备上最实用的算法之一，因为它对噪声有一定的鲁棒性。

### Q5: QAOA 的收敛速度如何？

取决于问题规模和层数。对于简单问题，通常 100-200 次迭代就能收敛。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 组合优化问题
- 经典优化器

### 继续学习

- 量子优化算法
- 量子机器学习
- 量子模拟

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

### 示例 2：4 顶点 QAOA MaxCut

```python
from quonic.algorithms import qaoa_maxcut

edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
result = qaoa_maxcut(edges, 4, init_params=[0.3, 0.3], maxiter=200)
print(result.value)
```

### 运行方式

```bash
python examples/qaoa/qaoa.py
```

---

## 下载

- [qaoa.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qaoa/qaoa.py)
