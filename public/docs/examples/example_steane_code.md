# Steane Code / Steane 码

> **QEC** / 量子纠错 | 难度：高级 | 预计时间：15 分钟

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

Steane 码是 CSS 码的经典例子，可以纠正任意单量子比特错误。

**经典局限**：
- 经典纠错码：无法纠正量子错误
- 量子纠错码：可以纠正量子错误

**量子优势**：
- 可以纠正任意单量子比特错误
- 比 Shor 码更高效

**实际应用**：
- 量子纠错
- 量子计算
- 量子算法教学

---

## 快速上手

```python
from quonic.qec import SteaneCode, qec_round_trip

# Steane 码
result = qec_round_trip(code="steane", error_rate=0.01, shots=1000)
print(result.success_rate)  # ~0.99
```

**预期输出**：

```
0.99
```

---

## 原理详解

### 电路图

![Steane Code circuit](/images/steane_code_circuit.svg)

### 数学推导

**Steane 码**

目标：纠正任意单量子比特错误。

**编码**：
使用 [7,1,3] 汉明码的 CSS 构造。

**错误**：
可以纠正任意单量子比特错误（X、Y、Z）。

**纠正**：
测量伴随式，判断错误类型和位置，然后纠正。

**数学推导**：
|ψ₀⟩ = α|0⟩ + β|1⟩
|ψ₁⟩ = α|0_L⟩ + β|1_L⟩
|ψ₂⟩ = 错误
|ψ₃⟩ = 纠正

### 几何解释

Steane 码的几何解释：

1. 编码：将 1 个量子比特编码为 7 个
2. 错误：任意单量子比特错误
3. 纠正：检测并纠正错误

这就像用汉明码保护量子信息。

---

## 代码详解

```python
from quonic.qec import SteaneCode, qec_round_trip  # 导入纠错码

# qec_round_trip(code, error_rate, shots)
# code: 纠错码类型
# error_rate: 错误率
# shots: 测量次数
result = qec_round_trip(code="steane", error_rate=0.01, shots=1000)

# result.success_rate: 成功率
print(result.success_rate)  # ~0.99
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `qec_round_trip(code, error_rate, shots)` | code: 纠错码类型, error_rate: 错误率, shots: 测量次数 | 执行纠错 |
| `result.success_rate` | 无参数 | 成功率 |

---

## 进阶用法

### 场景 1：不同错误率

```python
# 1% 错误率
result = qec_round_trip(code="steane", error_rate=0.01, shots=1000)
print(result.success_rate)

# 5% 错误率
result = qec_round_trip(code="steane", error_rate=0.05, shots=1000)
print(result.success_rate)

# 10% 错误率
result = qec_round_trip(code="steane", error_rate=0.10, shots=1000)
print(result.success_rate)
```

### 场景 2：不同纠错码

```python
# Steane 码
result = qec_round_trip(code="steane", error_rate=0.01, shots=1000)
print(result.success_rate)

# Shor 码
result = qec_round_trip(code="shor", error_rate=0.01, shots=1000)
print(result.success_rate)
```

### 场景 3：纠错码用于量子计算

```python
# 纠错码可以用于保护量子计算
# 在噪声环境下运行量子算法
```

---

## 适用场景

### 场景 1：量子纠错

Steane 码可以用于纠正任意单量子比特错误。

### 场景 2：量子计算

Steane 码可以用于保护量子计算。

### 场景 3：量子算法教学

Steane 码是量子纠错的经典例子，用于教学。

---

## 常见问题

### Q1: Steane 码可以纠正哪些错误？

Steane 码可以纠正任意单量子比特错误（X、Y、Z）。

### Q2: Steane 码需要多少量子比特？

需要 7 个量子比特：1 个逻辑量子比特 + 6 个冗余量子比特。

### Q3: Steane 码和 Shor 码有什么区别？

Steane 码需要 7 个量子比特，Shor 码需要 9 个量子比特。

### Q4: Steane 码在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: Steane 码的精度如何？

精度取决于错误率和纠错码的设计。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 量子测量
- 量子纠错基础

### 继续学习

- Shor 码
- 表面码
- 量子纠错

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本 Steane 码

```python
from quonic.qec import SteaneCode, qec_round_trip

result = qec_round_trip(code="steane", error_rate=0.01, shots=1000)
print(result.success_rate)
```

### 示例 2：不同错误率

```python
from quonic.qec import SteaneCode, qec_round_trip

result = qec_round_trip(code="steane", error_rate=0.01, shots=1000)
print(result.success_rate)

result = qec_round_trip(code="steane", error_rate=0.05, shots=1000)
print(result.success_rate)
```

### 运行方式

```bash
python examples/steane_code/steane_code.py
```

---

## 下载

- [steane_code.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/steane_code/steane_code.py)
