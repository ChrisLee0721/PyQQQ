# Quantum SVM / 量子支持向量机

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

量子 SVM 用于分类问题。

**经典局限**：
- 经典 SVM：线性核
- 量子 SVM：量子核

**量子优势**：
- 可以处理高维数据
- 是量子机器学习的基础

**实际应用**：
- 分类问题
- 模式识别
- 量子机器学习

---

## 快速上手

```python
from quonic.algorithms import quantum_svm

# 量子 SVM
result = quantum_svm(data, labels, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'00': 512, '11': 512}
```

---

## 原理详解

### 电路图

![Quantum SVM circuit](/images/qsvm_circuit.svg)

### 数学推导

**量子 SVM 算法**

目标：使用量子核进行分类。

**算法步骤**：
1. 初始化：数据编码
2. 核计算：计算量子核
3. 训练：训练 SVM
4. 预测：分类新数据

**数学推导**：
K(xᵢ, xⱼ) = |⟨φ(xᵢ)|φ(xⱼ)⟩|²
使用量子态计算核

### 几何解释

量子 SVM 的几何解释：

1. 数据点：在特征空间中的点
2. 量子核：在量子态空间中的内积
3. 分类：使用 SVM 进行分类

这就像在量子态空间中找最大间隔超平面。

---

## 代码详解

```python
from quonic.algorithms import quantum_svm  # 导入算法

# quantum_svm(data, labels, shots)
# data: 数据
# labels: 标签
# shots: 测量次数
result = quantum_svm(data, labels, shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `quantum_svm(data, labels, shots)` | data: 数据, labels: 标签, shots: 测量次数 | 执行量子 SVM |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同数据

```python
# 不同数据
result = quantum_svm(data1, labels1, shots=1024)
print(result.counts)

result = quantum_svm(data2, labels2, shots=1024)
print(result.counts)
```

### 场景 2：量子 SVM 用于分类

```python
# 量子 SVM 可以用于分类
# 分类数据
```

### 场景 3：量子 SVM 用于模式识别

```python
# 量子 SVM 可以用于模式识别
# 识别模式
```

---

## 适用场景

### 场景 1：分类问题

量子 SVM 可以用于分类问题。

### 场景 2：模式识别

量子 SVM 可以用于模式识别。

### 场景 3：量子机器学习

量子 SVM 是量子机器学习的基础。

---

## 常见问题

### Q1: 量子 SVM 的精度如何？

精度取决于数据量和模型复杂度。

### Q2: 量子 SVM 需要多少量子比特？

取决于数据维度。

### Q3: 量子 SVM 和经典 SVM 有什么区别？

量子 SVM 可以处理高维数据。

### Q4: 量子 SVM 在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 量子 SVM 的复杂度如何？

复杂度取决于数据量和模型复杂度。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 量子机器学习
- 支持向量机

### 继续学习

- 量子机器学习
- 分类问题
- 模式识别

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本量子 SVM

```python
from quonic.algorithms import quantum_svm

result = quantum_svm(data, labels, shots=1024)
print(result.counts)
```

### 示例 2：不同数据

```python
from quonic.algorithms import quantum_svm

result = quantum_svm(data1, labels1, shots=1024)
print(result.counts)

result = quantum_svm(data2, labels2, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/qsvm/qsvm.py
```

---

## 下载

- [qsvm.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qsvm/qsvm.py)
