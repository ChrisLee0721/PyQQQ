# Coupling Map / 耦合映射

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

耦合映射用于描述硬件拓扑。

**经典局限**：
- 经典拓扑：无
- 量子拓扑：有

**量子优势**：
- 可以描述硬件拓扑
- 是量子计算的基础

**实际应用**：
- 量子计算
- 量子算法
- 量子算法教学

---

## 快速上手

```python
from quonic import CouplingMap

# 耦合映射
cm = CouplingMap.from_line(4)
print(cm)
```

**预期输出**：

```
CouplingMap with 4 qubits, edges: [(0,1), (1,2), (2,3)]
```

---

## 原理详解

### 电路图

![Coupling Map circuit](/images/coupling_map_circuit.svg)

### 数学推导

**耦合映射算法**

目标：描述硬件拓扑。

**算法步骤**：
1. 定义：定义量子比特
2. 连接：定义连接
3. 输出：输出耦合映射

**数学推导**：
G = (V, E)
其中 V 是量子比特，E 是连接

### 几何解释

耦合映射的几何解释：

1. 量子比特：节点
2. 连接：边
3. 拓扑：图

这就像在图上定义连接。

---

## 代码详解

```python
from quonic import CouplingMap  # 导入耦合映射

# CouplingMap.from_line(n)
# n: 量子比特数
cm = CouplingMap.from_line(4)

# cm: 耦合映射
print(cm)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `CouplingMap.from_line(n)` | n: 量子比特数 | 创建线性耦合映射 |
| `CouplingMap.from_grid(rows, cols)` | rows: 行数, cols: 列数 | 创建网格耦合映射 |
| `CouplingMap.fully_connected(n)` | n: 量子比特数 | 创建全连接耦合映射 |

---

## 进阶用法

### 场景 1：不同拓扑

```python
# 线性拓扑
cm1 = CouplingMap.from_line(4)
print(cm1)

# 网格拓扑
cm2 = CouplingMap.from_grid(2, 2)
print(cm2)

# 全连接拓扑
cm3 = CouplingMap.fully_connected(4)
print(cm3)
```

### 场景 2：耦合映射用于量子计算

```python
# 耦合映射可以用于量子计算
# 描述硬件拓扑
```

### 场景 3：耦合映射用于量子算法

```python
# 耦合映射可以用于量子算法
# 编译量子算法
```

---

## 适用场景

### 场景 1：量子计算

耦合映射可以用于量子计算。

### 场景 2：量子算法

耦合映射可以用于量子算法。

### 场景 3：量子算法教学

耦合映射是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: 耦合映射的精度如何？

精度取决于拓扑结构。

### Q2: 耦合映射需要多少量子比特？

取决于拓扑结构。

### Q3: 耦合映射和拓扑有什么区别？

耦合映射是拓扑的数学描述。

### Q4: 耦合映射在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 耦合映射的复杂度如何？

复杂度取决于拓扑结构。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 量子测量
- 图论

### 继续学习

- 量子计算
- 量子算法
- 量子算法教学

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本耦合映射

```python
from quonic import CouplingMap

cm = CouplingMap.from_line(4)
print(cm)
```

### 示例 2：不同拓扑

```python
from quonic import CouplingMap

cm1 = CouplingMap.from_line(4)
print(cm1)

cm2 = CouplingMap.from_grid(2, 2)
print(cm2)
```

### 运行方式

```bash
python examples/coupling_map/coupling_map.py
```

---

## 下载

- [coupling_map.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/coupling_map/coupling_map.py)
