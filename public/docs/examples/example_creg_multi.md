# Multiple Classical Registers / 多经典寄存器

> **Foundational** / 基础 | 难度：中级 | 预计时间：10 分钟

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

多经典寄存器用于存储多个测量结果。

**经典局限**：
- 单寄存器：一个测量结果
- 多寄存器：多个测量结果

**量子优势**：
- 可以存储多个测量结果
- 是量子计算的基础

**实际应用**：
- 量子计算
- 量子算法
- 量子算法教学

---

## 快速上手

```python
from quonic import qgate, qshow, creg

# 多经典寄存器
c0 = creg(2, name="c0")
c1 = creg(2, name="c1")
qgate(H, 0)
qgate(CX, 0, 1)
qshow()
```

**预期输出**：

```
backend: native | shots: 1024
Result:
  |00>     512  ( 50.0%)  ####################
  |11>     512  ( 50.0%)  ####################
```

---

## 原理详解

### 电路图

![Multiple Classical Registers circuit](/images/creg_multi_circuit.svg)

### 数学推导

**多经典寄存器算法**

目标：存储多个测量结果。

**算法步骤**：
1. 定义：定义多个寄存器
2. 测量：测量量子比特
3. 存储：存储到不同寄存器

**数学推导**：
c₀ = measure(q₀)
c₁ = measure(q₁)

### 几何解释

多经典寄存器的几何解释：

1. 量子比特：在 Bloch 球上的点
2. 测量：坍缩到确定态
3. 存储：存储到寄存器

这就像将测量结果存储到不同的容器中。

---

## 代码详解

```python
from quonic import qgate, qshow, creg  # 导入核心 API

# creg(n, name)
# n: 比特数
# name: 寄存器名称
c0 = creg(2, name="c0")
c1 = creg(2, name="c1")

# 构建电路
qgate(H, 0)
qgate(CX, 0, 1)

# 测量
qshow()
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `creg(n, name)` | n: 比特数, name: 寄存器名称 | 创建经典寄存器 |
| `qshow()` | 无参数 | 运行电路并显示结果 |

---

## 进阶用法

### 场景 1：不同寄存器

```python
# 不同寄存器
c0 = creg(2, name="c0")
c1 = creg(2, name="c1")
qgate(H, 0)
qgate(CX, 0, 1)
qshow()
```

### 场景 2：多经典寄存器用于量子计算

```python
# 多经典寄存器可以用于量子计算
# 存储多个测量结果
```

### 场景 3：多经典寄存器用于量子算法

```python
# 多经典寄存器可以用于量子算法
# 存储算法结果
```

---

## 适用场景

### 场景 1：量子计算

多经典寄存器可以用于量子计算。

### 场景 2：量子算法

多经典寄存器可以用于量子算法。

### 场景 3：量子算法教学

多经典寄存器是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: 多经典寄存器的精度如何？

精度取决于测量精度。

### Q2: 多经典寄存器需要多少量子比特？

取决于寄存器数量。

### Q3: 多经典寄存器和单经典寄存器有什么区别？

多经典寄存器可以存储多个测量结果。

### Q4: 多经典寄存器在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 多经典寄存器的复杂度如何？

复杂度取决于寄存器数量。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 量子测量
- 经典寄存器

### 继续学习

- 量子计算
- 量子算法
- 量子算法教学

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本多经典寄存器

```python
from quonic import qgate, qshow, creg

c0 = creg(2, name="c0")
c1 = creg(2, name="c1")
qgate(H, 0)
qgate(CX, 0, 1)
qshow()
```

### 示例 2：不同寄存器

```python
from quonic import qgate, qshow, creg

c0 = creg(2, name="c0")
c1 = creg(2, name="c1")
qgate(H, 0)
qgate(CX, 0, 1)
qshow()
```

### 运行方式

```bash
python examples/creg_multi/creg_multi.py
```

---

## 下载

- [creg_multi.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/creg_multi/creg_multi.py)
