# Error Mitigation / 误差缓解

> **Noise** / 噪声 | 难度：高级 | 预计时间：15 分钟

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

误差缓解是减少噪声影响的技术，不需要完整的量子纠错。

**经典局限**：
- 经典计算机：没有噪声问题
- 量子计算机：噪声是主要挑战

**量子优势**：
- 误差缓解可以在 NISQ 设备上使用
- 不需要额外的量子比特
- 可以显著提高结果精度

**实际应用**：
- NISQ 设备上的算法
- 量子化学计算
- 量子优化

---

## 快速上手

```python
from quonic import zne

# 零噪声外推
result = zne(circuit, noise=0.05, extrapolation="linear")
print(result.mitigated_value)  # 更接近真实值
```

**预期输出**：

```
0.987654321
```

---

## 原理详解

### 电路图

![Error Mitigation circuit](/images/error_mitigation_circuit.svg)

### 数学推导

**零噪声外推 (ZNE)**

1. 在不同噪声水平下运行电路
2. 拟合噪声-结果曲线
3. 外推到零噪声

**数学表达**

假设结果是噪声的线性函数：
f(p) = f(0) + αp

测量 f(p₁) 和 f(p₂)，外推 f(0)。

### 几何解释

ZNE 的几何解释：

1. 测量不同噪声水平下的结果
2. 拟合直线
3. 外推到零噪声

这就像在噪声中提取真实信号。

---

## 代码详解

```python
from quonic import zne  # 导入 ZNE 算法

# zne(circuit, noise, extrapolation)
# circuit: 量子电路
# noise: 噪声水平
# extrapolation: 外推方法
result = zne(circuit, noise=0.05, extrapolation="linear")

# result.mitigated_value: 缓解后的值
print(result.mitigated_value)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `zne(circuit, noise, extrapolation)` | circuit: 量子电路, noise: 噪声水平, extrapolation: 外推方法 | 执行 ZNE |
| `result.mitigated_value` | 无参数 | 缓解后的值 |

---

## 进阶用法

### 场景 1：不同外推方法

```python
# 线性外推
result = zne(circuit, noise=0.05, extrapolation="linear")
print(result.mitigated_value)

# 二次外推
result = zne(circuit, noise=0.05, extrapolation="quadratic")
print(result.mitigated_value)
```

### 场景 2：不同噪声水平

```python
# 5% 噪声
result = zne(circuit, noise=0.05, extrapolation="linear")
print(result.mitigated_value)

# 10% 噪声
result = zne(circuit, noise=0.10, extrapolation="linear")
print(result.mitigated_value)
```

### 场景 3：ZNE 用于 VQE

```python
# ZNE 可以用于提高 VQE 的精度
# 在噪声下运行 VQE，然后用 ZNE 缓解
```

---

## 适用场景

### 场景 1：NISQ 设备上的算法

ZNE 可以在 NISQ 设备上使用，提高算法的精度。

### 场景 2：量子化学计算

ZNE 可以用于提高量子化学计算的精度。

### 场景 3：量子优化

ZNE 可以用于提高量子优化算法的精度。

---

## 常见问题

### Q1: ZNE 需要额外的量子比特吗？

不需要。ZNE 只需要在不同噪声水平下运行电路。

### Q2: ZNE 的精度如何？

ZNE 的精度取决于噪声模型的准确性。对于线性噪声，ZNE 可以完全消除噪声影响。

### Q3: ZNE 和量子纠错有什么区别？

ZNE 是后处理技术，不需要额外的量子比特。量子纠错需要额外的量子比特。

### Q4: ZNE 有哪些外推方法？

常见的有线性外推、二次外推、指数外推等。

### Q5: ZNE 的计算开销如何？

ZNE 需要在多个噪声水平下运行电路，计算开销是单次运行的几倍。

---

## 学习路径

### 前置知识

- 量子噪声模型
- 量子测量
- 曲线拟合

### 继续学习

- 量子纠错
- 读出校准
- 噪声模型

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本 ZNE

```python
from quonic import zne

result = zne(circuit, noise=0.05, extrapolation="linear")
print(result.mitigated_value)
```

### 示例 2：不同外推方法

```python
from quonic import zne

result = zne(circuit, noise=0.05, extrapolation="linear")
print(result.mitigated_value)

result = zne(circuit, noise=0.05, extrapolation="quadratic")
print(result.mitigated_value)
```

### 运行方式

```bash
python examples/error_mitigation/error_mitigation.py
```

---

## 下载

- [error_mitigation.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/error_mitigation/error_mitigation.py)
