# Eigenvalue Estimation / 本征值估计

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

本征值估计用于估计矩阵的本征值。

**经典局限**：
- 经典算法：O(N³) 复杂度
- 量子算法：O(log N) 复杂度

**量子优势**：
- 指数加速
- 是量子化学的基础

**实际应用**：
- 量子化学
- 量子材料科学
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import quantum_eigenvalue

# 本征值估计
result = quantum_eigenvalue(matrix, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'00': 512, '11': 512}
```

---

## 原理详解

### 电路图

![Eigenvalue Estimation circuit](/images/quantum_eigenvalue_circuit.svg)

### 数学推导

**本征值估计算法**

目标：估计矩阵的本征值。

**算法步骤**：
1. 初始化：|ψ⟩
2. QPE：估计本征值
3. 测量：得到本征值

**数学推导**：
A|ψ⟩ = λ|ψ⟩
QPE 得到 λ

### 几何解释

本征值估计的几何解释：

1. 初始态：任意态
2. QPE：估计本征值
3. 测量：得到本征值

这就像用量子干涉来估计本征值。

---

## 代码详解

```python
from quonic.algorithms import quantum_eigenvalue  # 导入算法

# quantum_eigenvalue(matrix, shots)
# matrix: 矩阵
# shots: 测量次数
result = quantum_eigenvalue(matrix, shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `quantum_eigenvalue(matrix, shots)` | matrix: 矩阵, shots: 测量次数 | 执行本征值估计 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同矩阵

```python
# 不同矩阵
result = quantum_eigenvalue(matrix1, shots=1024)
print(result.counts)

result = quantum_eigenvalue(matrix2, shots=1024)
print(result.counts)
```

### 场景 2：本征值估计用于量子化学

```python
# 本征值估计可以用于量子化学
# 估计分子的本征值
```

### 场景 3：本征值估计用于量子材料科学

```python
# 本征值估计可以用于量子材料科学
# 估计材料的本征值
```

---

## 适用场景

### 场景 1：量子化学

本征值估计可以用于量子化学，估计分子的本征值。

### 场景 2：量子材料科学

本征值估计可以用于量子材料科学，估计材料的本征值。

### 场景 3：量子算法教学

本征值估计是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: 本征值估计的精度如何？

精度取决于量子比特数。

### Q2: 本征值估计需要多少量子比特？

取决于矩阵的大小。

### Q3: 本征值估计和 QPE 有什么区别？

本征值估计是 QPE 的应用。

### Q4: 本征值估计在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 本征值估计的复杂度如何？

复杂度取决于矩阵的大小。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 量子相位估计
- 线性代数

### 继续学习

- 量子化学
- 量子材料科学
- 量子算法

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本本征值估计

```python
from quonic.algorithms import quantum_eigenvalue

result = quantum_eigenvalue(matrix, shots=1024)
print(result.counts)
```

### 示例 2：不同矩阵

```python
from quonic.algorithms import quantum_eigenvalue

result = quantum_eigenvalue(matrix1, shots=1024)
print(result.counts)

result = quantum_eigenvalue(matrix2, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/quantum_eigenvalue/quantum_eigenvalue.py
```

---

## 下载

- [quantum_eigenvalue.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/quantum_eigenvalue/quantum_eigenvalue.py)
