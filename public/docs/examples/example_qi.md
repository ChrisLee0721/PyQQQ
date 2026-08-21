# Quantum Inspire / Quantum Inspire 硬件

> **Backends** / 后端 | 难度：中级 | 预计时间：10 分钟

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

Quantum Inspire 是量子硬件后端。

**经典局限**：
- 经典模拟：模拟量子电路
- 真实硬件：运行量子电路

**量子优势**：
- 可以在真实硬件上运行
- 是量子计算的基础

**实际应用**：
- 量子计算
- 量子算法
- 量子算法教学

---

## 快速上手

```python
from quonic import qgate, qshow

# Quantum Inspire
qgate(H, 0)
qgate(CX, 0, 1)
qshow(backend='qi', device='Tuna-9')
```

**预期输出**：

```
backend: qi | shots: 1024
Result:
  |00>     512  ( 50.0%)  ####################
  |11>     512  ( 50.0%)  ####################
```

---

## 原理详解

### 电路图

![Quantum Inspire circuit](/images/qi_circuit.svg)

### 数学推导

**Quantum Inspire 算法**

目标：在真实硬件上运行量子电路。

**算法步骤**：
1. 构建：构建量子电路
2. 提交：提交到 Quantum Inspire
3. 运行：在真实硬件上运行
4. 获取：获取结果

**数学推导**：
|ψ⟩ = U|0⟩
在真实硬件上执行 U

### 几何解释

Quantum Inspire 的几何解释：

1. 构建：构建量子电路
2. 提交：提交到 Quantum Inspire
3. 运行：在真实硬件上运行
4. 获取：获取结果

这就像在真实量子计算机上运行电路。

---

## 代码详解

```python
from quonic import qgate, qshow  # 导入核心 API

# 构建电路
qgate(H, 0)      # Hadamard 门
qgate(CX, 0, 1)  # CNOT 门

# 在 Quantum Inspire 上运行
qshow(backend='qi', device='Tuna-9')
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `qshow(backend='qi', device='Tuna-9')` | backend: 后端, device: 设备 | 在 Quantum Inspire 上运行 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同设备

```python
# Tuna-9
qshow(backend='qi', device='Tuna-9')

# Tuna-17
qshow(backend='qi', device='Tuna-17')
```

### 场景 2：Quantum Inspire 用于量子计算

```python
# Quantum Inspire 可以用于量子计算
# 在真实硬件上运行量子电路
```

### 场景 3：Quantum Inspire 用于量子算法

```python
# Quantum Inspire 可以用于量子算法
# 在真实硬件上运行量子算法
```

---

## 适用场景

### 场景 1：量子计算

Quantum Inspire 可以用于量子计算。

### 场景 2：量子算法

Quantum Inspire 可以用于量子算法。

### 场景 3：量子算法教学

Quantum Inspire 是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: Quantum Inspire 的精度如何？

精度取决于硬件质量。

### Q2: Quantum Inspire 需要多少量子比特？

取决于设备。

### Q3: Quantum Inspire 和模拟器有什么区别？

Quantum Inspire 是真实硬件，模拟器是模拟。

### Q4: Quantum Inspire 在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: Quantum Inspire 的复杂度如何？

复杂度取决于电路规模。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 量子测量
- 量子硬件

### 继续学习

- 量子计算
- 量子算法
- 量子算法教学

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本 Quantum Inspire

```python
from quonic import qgate, qshow

qgate(H, 0)
qgate(CX, 0, 1)
qshow(backend='qi', device='Tuna-9')
```

### 示例 2：不同设备

```python
from quonic import qgate, qshow

qgate(H, 0)
qgate(CX, 0, 1)
qshow(backend='qi', device='Tuna-9')

qshow(backend='qi', device='Tuna-17')
```

### 运行方式

```bash
python examples/qi/qi.py
```

---

## 下载

- [qi.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qi/qi.py)
