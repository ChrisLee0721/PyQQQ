# GPU Acceleration / GPU 加速

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

GPU 加速用于加速量子电路模拟。

**经典局限**：
- CPU 模拟：慢
- GPU 模拟：快

**量子优势**：
- 可以加速量子电路模拟
- 是量子计算的基础

**实际应用**：
- 量子电路模拟
- 量子算法
- 量子算法教学

---

## 快速上手

```python
from quonic import qgate, qshow

# GPU 加速
qgate(H, 0)
for i in range(19):
    qgate(CX, i, i + 1)
qshow(backend='cupy')
```

**预期输出**：

```
backend: cupy | shots: 1024
Result:
  |00000000000000000000>    512  ( 50.0%)  ####################
  |11111111111111111111>    512  ( 50.0%)  ####################
```

---

## 原理详解

### 电路图

![GPU Acceleration circuit](/images/gpu_demo_circuit.svg)

### 数学推导

**GPU 加速算法**

目标：加速量子电路模拟。

**算法步骤**：
1. 构建：构建量子电路
2. 运行：在 GPU 上运行
3. 获取：获取结果

**数学推导**：
|ψ⟩ = U|0⟩
在 GPU 上执行 U

### 几何解释

GPU 加速的几何解释：

1. 构建：构建量子电路
2. 运行：在 GPU 上运行
3. 获取：获取结果

这就像在 GPU 上运行量子电路。

---

## 代码详解

```python
from quonic import qgate, qshow  # 导入核心 API

# 构建电路
qgate(H, 0)
for i in range(19):
    qgate(CX, i, i + 1)

# 在 GPU 上运行
qshow(backend='cupy')
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `qshow(backend='cupy')` | backend: 后端 | 在 GPU 上运行 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同规模

```python
# 小规模
qgate(H, 0)
for i in range(9):
    qgate(CX, i, i + 1)
qshow(backend='cupy')

# 大规模
qgate(H, 0)
for i in range(19):
    qgate(CX, i, i + 1)
qshow(backend='cupy')
```

### 场景 2：GPU 加速用于量子电路模拟

```python
# GPU 加速可以用于量子电路模拟
# 加速模拟
```

### 场景 3：GPU 加速用于量子算法

```python
# GPU 加速可以用于量子算法
# 加速算法
```

---

## 适用场景

### 场景 1：量子电路模拟

GPU 加速可以用于量子电路模拟。

### 场景 2：量子算法

GPU 加速可以用于量子算法。

### 场景 3：量子算法教学

GPU 加速是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: GPU 加速的精度如何？

精度取决于硬件质量。

### Q2: GPU 加速需要多少量子比特？

取决于 GPU 内存。

### Q3: GPU 加速和 CPU 模拟有什么区别？

GPU 加速更快。

### Q4: GPU 加速在 NISQ 设备上能跑吗？

可以跑大规模的。

### Q5: GPU 加速的复杂度如何？

复杂度取决于电路规模。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 量子测量
- GPU 编程

### 继续学习

- 量子电路模拟
- 量子算法
- 量子算法教学

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本 GPU 加速

```python
from quonic import qgate, qshow

qgate(H, 0)
for i in range(19):
    qgate(CX, i, i + 1)
qshow(backend='cupy')
```

### 示例 2：不同规模

```python
from quonic import qgate, qshow

qgate(H, 0)
for i in range(9):
    qgate(CX, i, i + 1)
qshow(backend='cupy')

qgate(H, 0)
for i in range(19):
    qgate(CX, i, i + 1)
qshow(backend='cupy')
```

### 运行方式

```bash
python examples/gpu_demo/gpu_demo.py
```

---

## 下载

- [gpu_demo.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/gpu_demo/gpu_demo.py)
