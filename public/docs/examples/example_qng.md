# Quantum Natural Gradient / 量子自然梯度

> **ML** / 量子机器学习 | 难度：高级 | 预计时间：15 分钟

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

量子自然梯度用于优化。

**经典局限**：
- 经典梯度：梯度下降
- 量子自然梯度：自然梯度

**量子优势**：
- 收敛更快
- 是量子机器学习的基础

**实际应用**：
- 优化问题
- 量子机器学习
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import quantum_ng

# 量子自然梯度
result = quantum_ng(loss_function, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'00': 512, '11': 512}
```

---

## 原理详解

### 电路图

![Quantum Natural Gradient circuit](/images/qng_circuit.svg)

### 数学推导

**量子自然梯度算法**

目标：优化损失函数。

**算法步骤**：
1. 初始化：参数
2. 计算梯度：计算自然梯度
3. 更新：更新参数
4. 重复：直到收敛

**数学推导**：
θ_{t+1} = θ_t - η F^{-1} ∇L(θ_t)
其中 F 是 Fisher 信息矩阵

### 几何解释

量子自然梯度的几何解释：

1. 参数空间：在参数空间中的点
2. 自然梯度：考虑参数空间的几何
3. 更新：沿自然梯度方向更新

这就像在参数空间中沿最速下降方向移动。

---

## 代码详解

```python
from quonic.algorithms import quantum_ng  # 导入算法

# quantum_ng(loss_function, shots)
# loss_function: 损失函数
# shots: 测量次数
result = quantum_ng(loss_function, shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `quantum_ng(loss_function, shots)` | loss_function: 损失函数, shots: 测量次数 | 执行量子自然梯度 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同损失函数

```python
# 不同损失函数
result = quantum_ng(loss_function1, shots=1024)
print(result.counts)

result = quantum_ng(loss_function2, shots=1024)
print(result.counts)
```

### 场景 2：量子自然梯度用于优化

```python
# 量子自然梯度可以用于优化
# 优化损失函数
```

### 场景 3：量子自然梯度用于量子机器学习

```python
# 量子自然梯度可以用于量子机器学习
# 训练模型
```

---

## 适用场景

### 场景 1：优化问题

量子自然梯度可以用于优化问题。

### 场景 2：量子机器学习

量子自然梯度可以用于量子机器学习。

### 场景 3：量子算法教学

量子自然梯度是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: 量子自然梯度的精度如何？

精度取决于损失函数和优化算法。

### Q2: 量子自然梯度需要多少量子比特？

取决于参数数量。

### Q3: 量子自然梯度和经典梯度有什么区别？

量子自然梯度收敛更快。

### Q4: 量子自然梯度在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 量子自然梯度的复杂度如何？

复杂度取决于参数数量。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 量子机器学习
- 自然梯度

### 继续学习

- 量子机器学习
- 优化问题
- 量子算法

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本量子自然梯度

```python
from quonic.algorithms import quantum_ng

result = quantum_ng(loss_function, shots=1024)
print(result.counts)
```

### 示例 2：不同损失函数

```python
from quonic.algorithms import quantum_ng

result = quantum_ng(loss_function1, shots=1024)
print(result.counts)

result = quantum_ng(loss_function2, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/qng/qng.py
```

---

## 下载

- [qng.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qng/qng.py)
