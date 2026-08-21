# VQR / 变分量子回归器

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

变分量子回归器用于回归问题。

**经典局限**：
- 经典回归器：经典计算
- 量子回归器：量子计算

**量子优势**：
- 可以处理高维数据
- 是量子机器学习的基础

**实际应用**：
- 回归问题
- 预测问题
- 量子机器学习

---

## 快速上手

```python
from quonic.algorithms import vqr

# 变分量子回归器
result = vqr(data, labels, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'00': 512, '11': 512}
```

---

## 原理详解

### 电路图

![VQR circuit](/images/vqr_circuit.svg)

### 数学推导

**变分量子回归器算法**

目标：回归数据。

**算法步骤**：
1. 初始化：参数化电路
2. 前向传播：计算输出
3. 反向传播：计算梯度
4. 更新：更新参数

**数学推导**：
y = f(x, θ)
minimize Σ (yᵢ - f(xᵢ, θ))²

### 几何解释

变分量子回归器的几何解释：

1. 数据点：在特征空间中的点
2. 回归曲线：通过数据点的曲线
3. 训练：优化回归曲线

这就像在特征空间中找最佳回归曲线。

---

## 代码详解

```python
from quonic.algorithms import vqr  # 导入算法

# vqr(data, labels, shots)
# data: 数据
# labels: 标签
# shots: 测量次数
result = vqr(data, labels, shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `vqr(data, labels, shots)` | data: 数据, labels: 标签, shots: 测量次数 | 执行变分量子回归器 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同数据

```python
# 不同数据
result = vqr(data1, labels1, shots=1024)
print(result.counts)

result = vqr(data2, labels2, shots=1024)
print(result.counts)
```

### 场景 2：变分量子回归器用于回归

```python
# 变分量子回归器可以用于回归
# 回归数据
```

### 场景 3：变分量子回归器用于预测

```python
# 变分量子回归器可以用于预测
# 预测数值
```

---

## 适用场景

### 场景 1：回归问题

变分量子回归器可以用于回归问题。

### 场景 2：预测问题

变分量子回归器可以用于预测问题。

### 场景 3：量子机器学习

变分量子回归器是量子机器学习的基础。

---

## 常见问题

### Q1: 变分量子回归器的精度如何？

精度取决于数据量和模型复杂度。

### Q2: 变分量子回归器需要多少量子比特？

取决于数据维度。

### Q3: 变分量子回归器和经典回归器有什么区别？

变分量子回归器可以处理高维数据。

### Q4: 变分量子回归器在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 变分量子回归器的复杂度如何？

复杂度取决于数据量和模型复杂度。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 量子机器学习
- 回归问题

### 继续学习

- 量子机器学习
- 回归问题
- 预测问题

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本变分量子回归器

```python
from quonic.algorithms import vqr

result = vqr(data, labels, shots=1024)
print(result.counts)
```

### 示例 2：不同数据

```python
from quonic.algorithms import vqr

result = vqr(data1, labels1, shots=1024)
print(result.counts)

result = vqr(data2, labels2, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/vqr/vqr.py
```

---

## 下载

- [vqr.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/vqr/vqr.py)
