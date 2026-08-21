# Matrix Inversion / 矩阵求逆

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

矩阵求逆用于求解线性方程组。

**经典局限**：
- 经典算法：O(N³) 复杂度
- 量子算法：O(log N) 复杂度

**量子优势**：
- 指数加速
- 是量子机器学习的基础

**实际应用**：
- 机器学习
- 优化问题
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import quantum_matrix_inversion

# 矩阵求逆
result = quantum_matrix_inversion(matrix, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'00': 512, '11': 512}
```

---

## 原理详解

### 电路图

![Matrix Inversion circuit](/images/quantum_matrix_inversion_circuit.svg)

### 数学推导

**矩阵求逆算法**

目标：求解 Ax = b。

**算法步骤**：
1. 初始化：|b⟩
2. QPE：估计 A 的本征值
3. 旋转：根据本征值旋转
4. 逆 QPE：得到解

**数学推导**：
|ψ₀⟩ = |b⟩
|ψ₁⟩ = QPE |b⟩
|ψ₂⟩ = 旋转
|ψ₃⟩ = |x⟩ = A^{-1}|b⟩

### 几何解释

矩阵求逆的几何解释：

1. 初始态：向量 b
2. QPE：估计本征值
3. 旋转：根据本征值旋转
4. 结果：解向量 x

这就像用量子干涉来求解线性方程组。

---

## 代码详解

```python
from quonic.algorithms import quantum_matrix_inversion  # 导入算法

# quantum_matrix_inversion(matrix, shots)
# matrix: 系数矩阵
# shots: 测量次数
result = quantum_matrix_inversion(matrix, shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `quantum_matrix_inversion(matrix, shots)` | matrix: 系数矩阵, shots: 测量次数 | 执行矩阵求逆 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同矩阵

```python
# 不同矩阵
result = quantum_matrix_inversion(matrix1, shots=1024)
print(result.counts)

result = quantum_matrix_inversion(matrix2, shots=1024)
print(result.counts)
```

### 场景 2：矩阵求逆用于机器学习

```python
# 矩阵求逆可以用于机器学习
# 求解线性回归问题
```

### 场景 3：矩阵求逆用于优化问题

```python
# 矩阵求逆可以用于优化问题
# 求解二次规划问题
```

---

## 适用场景

### 场景 1：机器学习

矩阵求逆可以用于机器学习，求解线性回归问题。

### 场景 2：优化问题

矩阵求逆可以用于优化问题，求解二次规划问题。

### 场景 3：量子算法教学

矩阵求逆是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: 矩阵求逆的加速比是多少？

指数加速。

### Q2: 矩阵求逆需要多少量子比特？

取决于矩阵的大小。

### Q3: 矩阵求逆和 HHL 算法有什么区别？

矩阵求逆是 HHL 算法的应用。

### Q4: 矩阵求逆在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 矩阵求逆的精度如何？

精度取决于矩阵的条件数和量子比特数。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- HHL 算法
- 线性代数

### 继续学习

- 机器学习
- 优化问题
- 量子算法

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本矩阵求逆

```python
from quonic.algorithms import quantum_matrix_inversion

result = quantum_matrix_inversion(matrix, shots=1024)
print(result.counts)
```

### 示例 2：不同矩阵

```python
from quonic.algorithms import quantum_matrix_inversion

result = quantum_matrix_inversion(matrix1, shots=1024)
print(result.counts)

result = quantum_matrix_inversion(matrix2, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/quantum_matrix_inversion/quantum_matrix_inversion.py
```

---

## 下载

- [quantum_matrix_inversion.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/quantum_matrix_inversion/quantum_matrix_inversion.py)
