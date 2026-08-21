# Quantum PCA / 量子主成分分析

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

量子 PCA 用于降维。

**经典局限**：
- 经典 PCA：O(N³) 复杂度
- 量子 PCA：O(log N) 复杂度

**量子优势**：
- 指数加速
- 是量子机器学习的基础

**实际应用**：
- 降维
- 数据压缩
- 量子机器学习

---

## 快速上手

```python
from quonic.algorithms import quantum_pca

# 量子 PCA
result = quantum_pca(data, n_components=2, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'00': 512, '11': 512}
```

---

## 原理详解

### 电路图

![Quantum PCA circuit](/images/qpca_circuit.svg)

### 数学推导

**量子 PCA 算法**

目标：降维。

**算法步骤**：
1. 初始化：数据编码
2. QPE：估计本征值
3. 测量：得到主成分

**数学推导**：
C = (1/N) Σ xᵢ xᵢᵀ
QPE 得到本征值和本征向量

### 几何解释

量子 PCA 的几何解释：

1. 数据点：在高维空间中的点
2. 主成分：最大方差方向
3. 降维：投影到低维空间

这就像在高维空间中找最大方差方向。

---

## 代码详解

```python
from quonic.algorithms import quantum_pca  # 导入算法

# quantum_pca(data, n_components, shots)
# data: 数据
# n_components: 主成分数
# shots: 测量次数
result = quantum_pca(data, n_components=2, shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `quantum_pca(data, n_components, shots)` | data: 数据, n_components: 主成分数, shots: 测量次数 | 执行量子 PCA |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同数据

```python
# 不同数据
result = quantum_pca(data1, n_components=2, shots=1024)
print(result.counts)

result = quantum_pca(data2, n_components=3, shots=1024)
print(result.counts)
```

### 场景 2：量子 PCA 用于降维

```python
# 量子 PCA 可以用于降维
# 降低数据维度
```

### 场景 3：量子 PCA 用于数据压缩

```python
# 量子 PCA 可以用于数据压缩
# 压缩数据
```

---

## 适用场景

### 场景 1：降维

量子 PCA 可以用于降维。

### 场景 2：数据压缩

量子 PCA 可以用于数据压缩。

### 场景 3：量子机器学习

量子 PCA 是量子机器学习的基础。

---

## 常见问题

### Q1: 量子 PCA 的精度如何？

精度取决于数据量和主成分数。

### Q2: 量子 PCA 需要多少量子比特？

取决于数据维度。

### Q3: 量子 PCA 和经典 PCA 有什么区别？

量子 PCA 有指数加速。

### Q4: 量子 PCA 在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 量子 PCA 的复杂度如何？

复杂度取决于数据量和主成分数。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 量子机器学习
- 主成分分析

### 继续学习

- 量子机器学习
- 降维
- 数据压缩

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本量子 PCA

```python
from quonic.algorithms import quantum_pca

result = quantum_pca(data, n_components=2, shots=1024)
print(result.counts)
```

### 示例 2：不同数据

```python
from quonic.algorithms import quantum_pca

result = quantum_pca(data1, n_components=2, shots=1024)
print(result.counts)

result = quantum_pca(data2, n_components=3, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/qpca/qpca.py
```

---

## 下载

- [qpca.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qpca/qpca.py)
