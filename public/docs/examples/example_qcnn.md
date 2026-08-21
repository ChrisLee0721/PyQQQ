# Quantum CNN / 量子卷积网络

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

量子 CNN 用于图像处理。

**经典局限**：
- 经典 CNN：经典计算
- 量子 CNN：量子计算

**量子优势**：
- 可以处理高维数据
- 是量子机器学习的基础

**实际应用**：
- 图像分类
- 目标检测
- 量子机器学习

---

## 快速上手

```python
from quonic.algorithms import quantum_cnn

# 量子 CNN
result = quantum_cnn(image, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'00': 512, '11': 512}
```

---

## 原理详解

### 电路图

![Quantum CNN circuit](/images/qcnn_circuit.svg)

### 数学推导

**量子 CNN 算法**

目标：处理图像。

**算法步骤**：
1. 初始化：图像编码
2. 卷积：应用卷积操作
3. 池化：池化操作
4. 输出：得到输出

**数学推导**：
y = f(x * w + b)
使用量子态表示卷积操作

### 几何解释

量子 CNN 的几何解释：

1. 图像：在像素空间中的矩阵
2. 卷积：提取特征
3. 池化：降低维度

这就像在图像上提取特征。

---

## 代码详解

```python
from quonic.algorithms import quantum_cnn  # 导入算法

# quantum_cnn(image, shots)
# image: 图像
# shots: 测量次数
result = quantum_cnn(image, shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `quantum_cnn(image, shots)` | image: 图像, shots: 测量次数 | 执行量子 CNN |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同图像

```python
# 不同图像
result = quantum_cnn(image1, shots=1024)
print(result.counts)

result = quantum_cnn(image2, shots=1024)
print(result.counts)
```

### 场景 2：量子 CNN 用于图像分类

```python
# 量子 CNN 可以用于图像分类
# 分类图像
```

### 场景 3：量子 CNN 用于目标检测

```python
# 量子 CNN 可以用于目标检测
# 检测目标
```

---

## 适用场景

### 场景 1：图像分类

量子 CNN 可以用于图像分类。

### 场景 2：目标检测

量子 CNN 可以用于目标检测。

### 场景 3：量子机器学习

量子 CNN 是量子机器学习的基础。

---

## 常见问题

### Q1: 量子 CNN 的精度如何？

精度取决于图像大小和模型复杂度。

### Q2: 量子 CNN 需要多少量子比特？

取决于图像大小。

### Q3: 量子 CNN 和经典 CNN 有什么区别？

量子 CNN 可以处理高维数据。

### Q4: 量子 CNN 在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 量子 CNN 的复杂度如何？

复杂度取决于图像大小和模型复杂度。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 量子机器学习
- 卷积神经网络

### 继续学习

- 量子机器学习
- 图像分类
- 目标检测

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本量子 CNN

```python
from quonic.algorithms import quantum_cnn

result = quantum_cnn(image, shots=1024)
print(result.counts)
```

### 示例 2：不同图像

```python
from quonic.algorithms import quantum_cnn

result = quantum_cnn(image1, shots=1024)
print(result.counts)

result = quantum_cnn(image2, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/qcnn/qcnn.py
```

---

## 下载

- [qcnn.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qcnn/qcnn.py)
