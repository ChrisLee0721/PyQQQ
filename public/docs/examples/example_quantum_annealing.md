# Quantum Annealing / 量子退火

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

量子退火用于优化问题。

**经典局限**：
- 经典退火：模拟退火
- 量子退火：量子退火

**量子优势**：
- 可以找到全局最优解
- 是量子优化的基础

**实际应用**：
- 组合优化
- 机器学习
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import quantum_annealing

# 量子退火
result = quantum_annealing(problem, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'00': 512, '11': 512}
```

---

## 原理详解

### 电路图

![Quantum Annealing circuit](/images/quantum_annealing_circuit.svg)

### 数学推导

**量子退火算法**

目标：找到全局最优解。

**算法步骤**：
1. 初始化：初始态
2. 退火：逐步降低温度
3. 测量：得到最优解

**数学推导**：
H(t) = (1-t/T) H₀ + (t/T) H₁
其中 H₀ 是初始哈密顿量，H₁ 是问题哈密顿量

### 几何解释

量子退火的几何解释：

1. 初始态：在能量面上的点
2. 退火：逐步降低温度
3. 结果：全局最优解

这就像在能量面上找最低点。

---

## 代码详解

```python
from quonic.algorithms import quantum_annealing  # 导入算法

# quantum_annealing(problem, shots)
# problem: 优化问题
# shots: 测量次数
result = quantum_annealing(problem, shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `quantum_annealing(problem, shots)` | problem: 优化问题, shots: 测量次数 | 执行量子退火 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同问题

```python
# 不同问题
result = quantum_annealing(problem1, shots=1024)
print(result.counts)

result = quantum_annealing(problem2, shots=1024)
print(result.counts)
```

### 场景 2：量子退火用于组合优化

```python
# 量子退火可以用于组合优化
# 例如：MaxCut
```

### 场景 3：量子退火用于机器学习

```python
# 量子退火可以用于机器学习
# 例如：聚类
```

---

## 适用场景

### 场景 1：组合优化

量子退火可以用于组合优化，例如 MaxCut。

### 场景 2：机器学习

量子退火可以用于机器学习，例如聚类。

### 场景 3：量子算法教学

量子退火是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: 量子退火的精度如何？

精度取决于退火时间和问题复杂度。

### Q2: 量子退火需要多少量子比特？

取决于问题的规模。

### Q3: 量子退火和经典退火有什么区别？

量子退火可以找到全局最优解。

### Q4: 量子退火在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 量子退火的复杂度如何？

复杂度取决于问题的规模。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 优化问题
- 量子退火基础

### 继续学习

- 组合优化
- 机器学习
- 量子算法

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本量子退火

```python
from quonic.algorithms import quantum_annealing

result = quantum_annealing(problem, shots=1024)
print(result.counts)
```

### 示例 2：不同问题

```python
from quonic.algorithms import quantum_annealing

result = quantum_annealing(problem1, shots=1024)
print(result.counts)

result = quantum_annealing(problem2, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/quantum_annealing/quantum_annealing.py
```

---

## 下载

- [quantum_annealing.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/quantum_annealing/quantum_annealing.py)
