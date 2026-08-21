# Color Code / 颜色码

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

颜色码是拓扑量子纠错码。

**经典局限**：
- 经典纠错码：无法纠正量子错误
- 量子纠错码：可以纠正量子错误

**量子优势**：
- 可以纠正任意单量子比特错误
- 是量子纠错的基础

**实际应用**：
- 量子纠错
- 量子计算
- 量子算法教学

---

## 快速上手

```python
from quonic.qec import ColorCode, qec_round_trip

# 颜色码
result = qec_round_trip(code="color", error_rate=0.01, shots=1000)
print(result.success_rate)
```

**预期输出**：

```
0.99
```

---

## 原理详解

### 电路图

![Color Code circuit](/images/color_code_circuit.svg)

### 数学推导

**颜色码**

目标：纠正任意单量子比特错误。

**编码**：
使用颜色码的 CSS 构造。

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

颜色码的几何解释：

1. 编码：将量子比特排列在颜色码上
2. 错误：任意单量子比特错误
3. 纠正：检测并纠正错误

这就像在颜色码上保护量子信息。

---

## 代码详解

```python
from quonic.qec import ColorCode, qec_round_trip  # 导入纠错码

# qec_round_trip(code, error_rate, shots)
# code: 纠错码类型
# error_rate: 错误率
# shots: 测量次数
result = qec_round_trip(code="color", error_rate=0.01, shots=1000)

# result.success_rate: 成功率
print(result.success_rate)
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
result = qec_round_trip(code="color", error_rate=0.01, shots=1000)
print(result.success_rate)

# 5% 错误率
result = qec_round_trip(code="color", error_rate=0.05, shots=1000)
print(result.success_rate)
```

### 场景 2：不同纠错码

```python
# 颜色码
result = qec_round_trip(code="color", error_rate=0.01, shots=1000)
print(result.success_rate)

# 表面码
result = qec_round_trip(code="surface", error_rate=0.01, shots=1000)
print(result.success_rate)
```

### 场景 3：颜色码用于量子计算

```python
# 颜色码可以用于量子计算
# 在噪声环境下运行量子算法
```

---

## 适用场景

### 场景 1：量子纠错

颜色码可以用于纠正任意单量子比特错误。

### 场景 2：量子计算

颜色码可以用于保护量子计算。

### 场景 3：量子算法教学

颜色码是量子纠错的经典例子，用于教学。

---

## 常见问题

### Q1: 颜色码可以纠正哪些错误？

颜色码可以纠正任意单量子比特错误（X、Y、Z）。

### Q2: 颜色码需要多少量子比特？

取决于码距。

### Q3: 颜色码和表面码有什么区别？

颜色码是拓扑码，表面码也是拓扑码。

### Q4: 颜色码在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 颜色码的精度如何？

精度取决于错误率和码距。

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

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本颜色码

```python
from quonic.qec import ColorCode, qec_round_trip

result = qec_round_trip(code="color", error_rate=0.01, shots=1000)
print(result.success_rate)
```

### 示例 2：不同错误率

```python
from quonic.qec import ColorCode, qec_round_trip

result = qec_round_trip(code="color", error_rate=0.01, shots=1000)
print(result.success_rate)

result = qec_round_trip(code="color", error_rate=0.05, shots=1000)
print(result.success_rate)
```

### 运行方式

```bash
python examples/color_code/color_code.py
```

---

## 下载

- [color_code.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/color_code/color_code.py)
