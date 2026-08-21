# Amplitude Estimation / 振幅估计

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

振幅估计用于估计量子态的概率振幅。

**经典局限**：
- 经典算法：需要大量采样
- 量子算法：可以精确估计

**量子优势**：
- 可以精确估计概率振幅
- 是许多量子算法的基础

**实际应用**：
- 量子金融
- 量子优化
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import amplitude_estimation

# 振幅估计
result = amplitude_estimation(2, oracle, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'00': 512, '11': 512}
```

---

## 原理详解

### 电路图

![Amplitude Estimation circuit](/images/amplitude_estimation_circuit.svg)

### 数学推导

**振幅估计算法**

目标：估计概率振幅 a。

**算法步骤**：
1. 初始化：任意态 |ψ⟩
2. QPE：估计本征值
3. 测量：得到振幅估计

**数学推导**：
|ψ₀⟩ = |ψ⟩
|ψ₁⟩ = QPE |ψ⟩
|ψ₂⟩ = 测量得到振幅估计

### 几何解释

振幅估计的几何解释：

1. 初始态：任意态
2. QPE：估计本征值
3. 测量：得到振幅估计

这就像用量子干涉来估计概率。

---

## 代码详解

```python
from quonic.algorithms import amplitude_estimation  # 导入算法

# amplitude_estimation(n_qubits, oracle, shots)
# n_qubits: 量子比特数
# oracle: Oracle 函数
# shots: 测量次数
result = amplitude_estimation(2, oracle, shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `amplitude_estimation(n_qubits, oracle, shots)` | n_qubits: 量子比特数, oracle: Oracle 函数, shots: 测量次数 | 执行振幅估计 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同 Oracle

```python
# 不同 Oracle
result = amplitude_estimation(2, oracle1, shots=1024)
print(result.counts)

result = amplitude_estimation(2, oracle2, shots=1024)
print(result.counts)
```

### 场景 2：振幅估计用于量子金融

```python
# 振幅估计可以用于量子金融
# 估计期权价格
```

### 场景 3：振幅估计用于量子优化

```python
# 振幅估计可以用于量子优化
# 估计最优解的概率
```

---

## 适用场景

### 场景 1：量子金融

振幅估计可以用于量子金融，估计期权价格。

### 场景 2：量子优化

振幅估计可以用于量子优化，估计最优解的概率。

### 场景 3：量子算法教学

振幅估计是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: 振幅估计的精度如何？

精度取决于量子比特数。

### Q2: 振幅估计需要多少量子比特？

取决于精度要求。

### Q3: 振幅估计和振幅放大有什么区别？

振幅估计估计概率，振幅放大放大概率。

### Q4: 振幅估计在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 振幅估计的复杂度如何？

复杂度取决于精度要求。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 量子相位估计
- 量子算法基础

### 继续学习

- 量子金融
- 量子优化
- 量子算法

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本振幅估计

```python
from quonic.algorithms import amplitude_estimation

result = amplitude_estimation(2, oracle, shots=1024)
print(result.counts)
```

### 示例 2：不同 Oracle

```python
from quonic.algorithms import amplitude_estimation

result = amplitude_estimation(2, oracle1, shots=1024)
print(result.counts)

result = amplitude_estimation(2, oracle2, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/amplitude_estimation/amplitude_estimation.py
```

---

## 下载

- [amplitude_estimation.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/amplitude_estimation/amplitude_estimation.py)
