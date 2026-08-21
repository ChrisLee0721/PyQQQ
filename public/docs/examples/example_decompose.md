# Gate Decomposition / 门分解

> **Compiler** / 编译器 | 难度：中级 | 预计时间：10 分钟

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

门分解用于将高级门分解为基础门。

**经典局限**：
- 高级门：不能直接执行
- 基础门：可以直接执行

**量子优势**：
- 可以将高级门分解为基础门
- 是量子计算的基础

**实际应用**：
- 量子计算
- 量子算法
- 量子算法教学

---

## 快速上手

```python
from quonic.compiler import decompose

# 门分解
result = decompose(circuit)
print(result)
```

**预期输出**：

```
Decomposed circuit with 100 operations
```

---

## 原理详解

### 电路图

![Gate Decomposition circuit](/images/decompose_circuit.svg)

### 数学推导

**门分解算法**

目标：将高级门分解为基础门。

**算法步骤**：
1. 分析：分析门结构
2. 分解：分解为基础门
3. 输出：输出分解后的电路

**数学推导**：
U → U₁ U₂ ... Uₙ
其中 Uᵢ 是基础门

### 几何解释

门分解的几何解释：

1. 高级门：复杂门
2. 基础门：简单门
3. 分解：将复杂门分解为简单门

这就像将复杂操作分解为简单操作。

---

## 代码详解

```python
from quonic.compiler import decompose  # 导入编译器

# decompose(circuit)
# circuit: 量子电路
result = decompose(circuit)

# result: 分解后的电路
print(result)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `decompose(circuit)` | circuit: 量子电路 | 执行门分解 |
| `result` | 无参数 | 分解后的电路 |

---

## 进阶用法

### 场景 1：不同电路

```python
# 不同电路
result = decompose(circuit1)
print(result)

result = decompose(circuit2)
print(result)
```

### 场景 2：门分解用于量子计算

```python
# 门分解可以用于量子计算
# 分解高级门
```

### 场景 3：门分解用于量子算法

```python
# 门分解可以用于量子算法
# 分解量子算法
```

---

## 适用场景

### 场景 1：量子计算

门分解可以用于量子计算。

### 场景 2：量子算法

门分解可以用于量子算法。

### 场景 3：量子算法教学

门分解是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: 门分解的精度如何？

精度取决于门结构。

### Q2: 门分解需要多少量子比特？

取决于门结构。

### Q3: 门分解和门优化有什么区别？

门分解将高级门分解为基础门，门优化减少门数量。

### Q4: 门分解在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 门分解的复杂度如何？

复杂度取决于门结构。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 量子测量
- 量子编译

### 继续学习

- 量子计算
- 量子算法
- 量子算法教学

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本门分解

```python
from quonic.compiler import decompose

result = decompose(circuit)
print(result)
```

### 示例 2：不同电路

```python
from quonic.compiler import decompose

result = decompose(circuit1)
print(result)

result = decompose(circuit2)
print(result)
```

### 运行方式

```bash
python examples/decompose/decompose.py
```

---

## 下载

- [decompose.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/decompose/decompose.py)
