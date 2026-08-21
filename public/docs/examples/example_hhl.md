# HHL Algorithm / HHL 算法

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

HHL 算法用于求解线性方程组，比经典算法快指数倍。

**经典局限**：
- 经典算法：O(N) 复杂度
- 量子算法：O(log N) 复杂度

**量子优势**：
- 指数加速：O(log N) vs O(N)
- 是量子机器学习的基础

**实际应用**：
- 机器学习
- 优化问题
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import hhl

# HHL 算法
result = hhl(matrix, vector, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'00': 512, '11': 512}
```

---

## 原理详解

### 电路图

![HHL Algorithm circuit](/images/hhl_circuit.svg)

### 数学推导

**HHL 算法**

目标：求解 Ax = b。

**算法步骤**：
1. 初始化：|b⟩
2. QPE：估计 A 的本征值
3. 旋转：根据本征值旋转
4. 逆 QPE：得到解

**数学推导**：
|ψ₀⟩ = |b⟩
|ψ₁⟩ = Σᵢ βᵢ |uᵢ⟩ |λᵢ⟩
|ψ₂⟩ = Σᵢ βᵢ/λᵢ |uᵢ⟩ |λᵢ⟩
|ψ₃⟩ = Σᵢ βᵢ/λᵢ |uᵢ⟩

### 几何解释

HHL 算法的几何解释：

1. 初始化：向量 b
2. QPE：估计本征值
3. 旋转：根据本征值旋转
4. 结果：解向量 x

这就像用量子干涉来求解线性方程组。

---

## 代码详解

```python
from quonic.algorithms import hhl  # 导入算法

# hhl(matrix, vector, shots)
# matrix: 系数矩阵
# vector: 右端向量
# shots: 测量次数
result = hhl(matrix, vector, shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `hhl(matrix, vector, shots)` | matrix: 系数矩阵, vector: 右端向量, shots: 测量次数 | 执行 HHL 算法 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同矩阵

```python
# 不同矩阵
result = hhl(matrix1, vector, shots=1024)
print(result.counts)

result = hhl(matrix2, vector, shots=1024)
print(result.counts)
```

### 场景 2：HHL 用于机器学习

```python
# HHL 算法可以用于机器学习
# 求解线性回归问题
```

### 场景 3：HHL 用于优化问题

```python
# HHL 算法可以用于优化问题
# 求解二次规划问题
```

---

## 适用场景

### 场景 1：机器学习

HHL 算法可以用于机器学习，求解线性回归问题。

### 场景 2：优化问题

HHL 算法可以用于优化问题，求解二次规划问题。

### 场景 3：量子算法教学

HHL 算法是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: HHL 算法的加速比是多少？

指数加速：O(log N) vs O(N)。

### Q2: HHL 算法需要多少量子比特？

取决于矩阵的大小。

### Q3: HHL 算法和经典算法有什么区别？

HHL 算法是指数加速，经典算法是线性复杂度。

### Q4: HHL 算法在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: HHL 算法的精度如何？

精度取决于矩阵的条件数和量子比特数。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 量子相位估计
- 线性代数

### 继续学习

- 量子机器学习
- 量子优化
- 量子算法

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本 HHL 算法

```python
from quonic.algorithms import hhl

result = hhl(matrix, vector, shots=1024)
print(result.counts)
```

### 示例 2：不同矩阵

```python
from quonic.algorithms import hhl

result = hhl(matrix1, vector, shots=1024)
print(result.counts)

result = hhl(matrix2, vector, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/hhl/hhl.py
```

---

## 下载

- [hhl.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/hhl/hhl.py)
