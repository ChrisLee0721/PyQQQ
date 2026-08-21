# Syndrome Measurement / 伴随式测量

> **QEC** / 量子纠错 | 难度：中级 | 预计时间：10 分钟

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

伴随式测量用于检测量子错误。

**经典局限**：
- 经典测量：直接测量
- 量子测量：伴随式测量

**量子优势**：
- 可以检测错误而不破坏量子态
- 是量子纠错的基础

**实际应用**：
- 量子纠错
- 量子计算
- 量子算法教学

---

## 快速上手

```python
from quonic.qec import syndrome_measurement

# 伴随式测量
result = syndrome_measurement(code, error_rate=0.01, shots=1000)
print(result.counts)
```

**预期输出**：

```
{'00': 970, '01': 10, '10': 10, '11': 10}
```

---

## 原理详解

### 电路图

![Syndrome Measurement circuit](/images/syndrome_circuit.svg)

### 数学推导

**伴随式测量算法**

目标：检测量子错误。

**算法步骤**：
1. 编码：编码量子态
2. 错误：引入错误
3. 测量：测量伴随式
4. 纠正：根据伴随式纠正错误

**数学推导**：
S = {g : g|ψ⟩ = |ψ⟩}
测量 S 得到伴随式

### 几何解释

伴随式测量的几何解释：

1. 编码：编码量子态
2. 错误：引入错误
3. 测量：测量伴随式
4. 纠正：根据伴随式纠正错误

这就像用伴随式来检测错误。

---

## 代码详解

```python
from quonic.qec import syndrome_measurement  # 导入伴随式测量

# syndrome_measurement(code, error_rate, shots)
# code: 纠错码
# error_rate: 错误率
# shots: 测量次数
result = syndrome_measurement(code, error_rate=0.01, shots=1000)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `syndrome_measurement(code, error_rate, shots)` | code: 纠错码, error_rate: 错误率, shots: 测量次数 | 执行伴随式测量 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同错误率

```python
# 1% 错误率
result = syndrome_measurement(code, error_rate=0.01, shots=1000)
print(result.counts)

# 5% 错误率
result = syndrome_measurement(code, error_rate=0.05, shots=1000)
print(result.counts)
```

### 场景 2：伴随式测量用于量子纠错

```python
# 伴随式测量可以用于量子纠错
# 检测和纠正错误
```

### 场景 3：伴随式测量用于量子计算

```python
# 伴随式测量可以用于量子计算
# 保护量子态
```

---

## 适用场景

### 场景 1：量子纠错

伴随式测量可以用于量子纠错。

### 场景 2：量子计算

伴随式测量可以用于量子计算。

### 场景 3：量子算法教学

伴随式测量是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: 伴随式测量的精度如何？

精度取决于错误率和纠错码。

### Q2: 伴随式测量需要多少量子比特？

取决于纠错码。

### Q3: 伴随式测量和直接测量有什么区别？

伴随式测量不破坏量子态。

### Q4: 伴随式测量在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 伴随式测量的复杂度如何？

复杂度取决于纠错码。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 量子测量
- 量子纠错基础

### 继续学习

- 量子纠错
- 量子计算
- 量子算法

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本伴随式测量

```python
from quonic.qec import syndrome_measurement

result = syndrome_measurement(code, error_rate=0.01, shots=1000)
print(result.counts)
```

### 示例 2：不同错误率

```python
from quonic.qec import syndrome_measurement

result = syndrome_measurement(code, error_rate=0.01, shots=1000)
print(result.counts)

result = syndrome_measurement(code, error_rate=0.05, shots=1000)
print(result.counts)
```

### 运行方式

```bash
python examples/syndrome/syndrome.py
```

---

## 下载

- [syndrome.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/syndrome/syndrome.py)
