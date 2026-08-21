# Fault-Tolerant Gates / 容错门

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

容错门用于在纠错码上执行门操作。

**经典局限**：
- 经典门：直接执行
- 量子门：需要容错执行

**量子优势**：
- 可以在纠错码上执行门操作
- 是量子纠错的基础

**实际应用**：
- 量子纠错
- 量子计算
- 量子算法教学

---

## 快速上手

```python
from quonic.qec import fault_tolerant_gate

# 容错门
result = fault_tolerant_gate(code, gate, shots=1000)
print(result.counts)
```

**预期输出**：

```
{'00': 512, '11': 512}
```

---

## 原理详解

### 电路图

![Fault-Tolerant Gates circuit](/images/ft_gate_circuit.svg)

### 数学推导

**容错门算法**

目标：在纠错码上执行门操作。

**算法步骤**：
1. 编码：编码量子态
2. 门操作：执行容错门
3. 解码：解码量子态

**数学推导**：
|ψ_L⟩ → U_L|ψ_L⟩
其中 U_L 是逻辑门

### 几何解释

容错门的几何解释：

1. 编码：编码量子态
2. 门操作：执行容错门
3. 解码：解码量子态

这就像在纠错码上执行门操作。

---

## 代码详解

```python
from quonic.qec import fault_tolerant_gate  # 导入容错门

# fault_tolerant_gate(code, gate, shots)
# code: 纠错码
# gate: 门操作
# shots: 测量次数
result = fault_tolerant_gate(code, gate, shots=1000)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `fault_tolerant_gate(code, gate, shots)` | code: 纠错码, gate: 门操作, shots: 测量次数 | 执行容错门 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同门操作

```python
# 不同门操作
result = fault_tolerant_gate(code, "H", shots=1000)
print(result.counts)

result = fault_tolerant_gate(code, "X", shots=1000)
print(result.counts)
```

### 场景 2：容错门用于量子纠错

```python
# 容错门可以用于量子纠错
# 在纠错码上执行门操作
```

### 场景 3：容错门用于量子计算

```python
# 容错门可以用于量子计算
# 在纠错码上执行计算
```

---

## 适用场景

### 场景 1：量子纠错

容错门可以用于量子纠错。

### 场景 2：量子计算

容错门可以用于量子计算。

### 场景 3：量子算法教学

容错门是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: 容错门的精度如何？

精度取决于纠错码和门操作。

### Q2: 容错门需要多少量子比特？

取决于纠错码。

### Q3: 容错门和普通门有什么区别？

容错门在纠错码上执行，普通门直接执行。

### Q4: 容错门在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 容错门的复杂度如何？

复杂度取决于纠错码和门操作。

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

### 示例 1：基本容错门

```python
from quonic.qec import fault_tolerant_gate

result = fault_tolerant_gate(code, "H", shots=1000)
print(result.counts)
```

### 示例 2：不同门操作

```python
from quonic.qec import fault_tolerant_gate

result = fault_tolerant_gate(code, "H", shots=1000)
print(result.counts)

result = fault_tolerant_gate(code, "X", shots=1000)
print(result.counts)
```

### 运行方式

```bash
python examples/ft_gate/ft_gate.py
```

---

## 下载

- [ft_gate.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/ft_gate/ft_gate.py)
