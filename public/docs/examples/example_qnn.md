# Quantum Neural Network / 量子神经网络

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

量子神经网络用于机器学习。

**经典局限**：
- 经典神经网络：经典计算
- 量子神经网络：量子计算

**量子优势**：
- 可以处理高维数据
- 是量子机器学习的基础

**实际应用**：
- 分类问题
- 回归问题
- 量子机器学习

---

## 快速上手

```python
from quonic.algorithms import quantum_nn

# 量子神经网络
result = quantum_nn(data, labels, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'00': 512, '11': 512}
```

---

## 原理详解

### 电路图

![Quantum Neural Network circuit](/images/qnn_circuit.svg)

### 数学推导

**量子神经网络算法**

目标：使用量子神经网络进行学习。

**算法步骤**：
1. 初始化：参数化电路
2. 前向传播：计算输出
3. 反向传播：计算梯度
4. 更新：更新参数

**数学推导**：
y = f(x, θ)
minimize Σ (yᵢ - f(xᵢ, θ))²

### 几何解释

量子神经网络的几何解释：

1. 参数空间：在参数空间中的点
2. 前向传播：计算输出
3. 反向传播：计算梯度
4. 更新：更新参数

这就像在参数空间中找最优解。

---

## 代码详解

```python
from quonic.algorithms import quantum_nn  # 导入算法

# quantum_nn(data, labels, shots)
# data: 数据
# labels: 标签
# shots: 测量次数
result = quantum_nn(data, labels, shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `quantum_nn(data, labels, shots)` | data: 数据, labels: 标签, shots: 测量次数 | 执行量子神经网络 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同数据

```python
# 不同数据
result = quantum_nn(data1, labels1, shots=1024)
print(result.counts)

result = quantum_nn(data2, labels2, shots=1024)
print(result.counts)
```

### 场景 2：量子神经网络用于分类

```python
# 量子神经网络可以用于分类
# 分类数据
```

### 场景 3：量子神经网络用于回归

```python
# 量子神经网络可以用于回归
# 预测数值
```

---

## 适用场景

### 场景 1：分类问题

量子神经网络可以用于分类问题。

### 场景 2：回归问题

量子神经网络可以用于回归问题。

### 场景 3：量子机器学习

量子神经网络是量子机器学习的基础。

---

## 常见问题

### Q1: 量子神经网络的精度如何？

精度取决于数据量和模型复杂度。

### Q2: 量子神经网络需要多少量子比特？

取决于数据维度。

### Q3: 量子神经网络和经典神经网络有什么区别？

量子神经网络可以处理高维数据。

### Q4: 量子神经网络在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 量子神经网络的复杂度如何？

复杂度取决于数据量和模型复杂度。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 量子机器学习
- 神经网络

### 继续学习

- 量子机器学习
- 分类问题
- 回归问题

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本量子神经网络

```python
from quonic.algorithms import quantum_nn

result = quantum_nn(data, labels, shots=1024)
print(result.counts)
```

### 示例 2：不同数据

```python
from quonic.algorithms import quantum_nn

result = quantum_nn(data1, labels1, shots=1024)
print(result.counts)

result = quantum_nn(data2, labels2, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/qnn/qnn.py
```

---

## 下载

- [qnn.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qnn/qnn.py)
