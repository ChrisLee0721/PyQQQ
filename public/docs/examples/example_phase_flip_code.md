# Phase-Flip Code / 相位翻转码

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

相位翻转码用于纠正相位翻转错误。

**经典局限**：
- 经典纠错码：无法纠正相位错误
- 量子纠错码：可以纠正相位错误

**量子优势**：
- 可以纠正量子比特的相位错误
- 是量子纠错的基础

**实际应用**：
- 量子纠错
- 量子计算
- 量子算法教学

---

## 快速上手

```python
from quonic.qec import PhaseFlipCode, qec_round_trip

# 相位翻转码
result = qec_round_trip(code="phase_flip", error_rate=0.01, shots=1000)
print(result.success_rate)  # ~0.97
```

**预期输出**：

```
0.97
```

---

## 原理详解

### 电路图

![Phase-Flip Code circuit](/images/phase_flip_code_circuit.svg)

### 数学推导

**相位翻转码**

目标：纠正相位翻转错误。

**编码**：
|0⟩ → |+++⟩
|1⟩ → |---⟩

**错误**：
|+++⟩ → |++-⟩ (相位翻转)
|+++⟩ → |+-+⟩ (相位翻转)
|+++⟩ → |-++⟩ (相位翻转)

**纠正**：
测量伴随式，判断哪个比特相位翻转，然后纠正。

**数学推导**：
|ψ₀⟩ = α|0⟩ + β|1⟩
|ψ₁⟩ = α|+++⟩ + β|---⟩
|ψ₂⟩ = α|++-⟩ + β|---⟩ (错误)
|ψ₃⟩ = α|+++⟩ + β|---⟩ (纠正)

### 几何解释

相位翻转码的几何解释：

1. 编码：将 1 个量子比特编码为 3 个
2. 错误：某个比特可能相位翻转
3. 纠正：检测并纠正错误

这就像用冗余来保护相位信息。

---

## 代码详解

```python
from quonic.qec import PhaseFlipCode, qec_round_trip  # 导入纠错码

# qec_round_trip(code, error_rate, shots)
# code: 纠错码类型
# error_rate: 错误率
# shots: 测量次数
result = qec_round_trip(code="phase_flip", error_rate=0.01, shots=1000)

# result.success_rate: 成功率
print(result.success_rate)  # ~0.97
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
result = qec_round_trip(code="phase_flip", error_rate=0.01, shots=1000)
print(result.success_rate)

# 5% 错误率
result = qec_round_trip(code="phase_flip", error_rate=0.05, shots=1000)
print(result.success_rate)

# 10% 错误率
result = qec_round_trip(code="phase_flip", error_rate=0.10, shots=1000)
print(result.success_rate)
```

### 场景 2：不同纠错码

```python
# 相位翻转码
result = qec_round_trip(code="phase_flip", error_rate=0.01, shots=1000)
print(result.success_rate)

# 比特翻转码
result = qec_round_trip(code="bit_flip", error_rate=0.01, shots=1000)
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

相位翻转码可以用于纠正量子比特的相位错误。

### 场景 2：量子计算

相位翻转码可以用于保护量子计算。

### 场景 3：量子算法教学

相位翻转码是量子纠错的经典例子，用于教学。

---

## 常见问题

### Q1: 相位翻转码可以纠正哪些错误？

相位翻转码可以纠正相位翻转错误（Z 错误）。

### Q2: 相位翻转码需要多少量子比特？

需要 3 个量子比特：1 个逻辑量子比特 + 2 个冗余量子比特。

### Q3: 相位翻转码和比特翻转码有什么区别？

相位翻转码纠正 Z 错误，比特翻转码纠正 X 错误。

### Q4: 相位翻转码在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 相位翻转码的精度如何？

精度取决于错误率和纠错码的设计。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 量子测量
- 量子纠错基础

### 继续学习

- 比特翻转码
- Shor 码
- Steane 码

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本相位翻转码

```python
from quonic.qec import PhaseFlipCode, qec_round_trip

result = qec_round_trip(code="phase_flip", error_rate=0.01, shots=1000)
print(result.success_rate)
```

### 示例 2：不同错误率

```python
from quonic.qec import PhaseFlipCode, qec_round_trip

result = qec_round_trip(code="phase_flip", error_rate=0.01, shots=1000)
print(result.success_rate)

result = qec_round_trip(code="phase_flip", error_rate=0.05, shots=1000)
print(result.success_rate)
```

### 运行方式

```bash
python examples/phase_flip_code/phase_flip_code.py
```

---

## 下载

- [phase_flip_code.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/phase_flip_code/phase_flip_code.py)
