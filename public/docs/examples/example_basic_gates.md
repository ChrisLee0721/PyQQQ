# Basic Gates / 基础门

> **Foundational** / 基础 | 难度：初级 | 预计时间：5 分钟

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

基础门是量子计算的构建块，理解它们是学习量子计算的第一步。

**经典局限**：
- 经典逻辑门：AND、OR、NOT
- 量子门：H、X、Y、Z、CX、CZ

**量子优势**：
- 量子门可以创建叠加态和纠缠
- 量子门是可逆的
- 量子门可以并行操作

**实际应用**：
- 量子计算的基础
- 量子算法的构建块
- 量子电路设计

---

## 快速上手

```python
from quonic import qgate, qshow
from quonic.gates import CX, CZ, H, X, Y, Z

# 单量子比特门
qgate(H, 0)   # Hadamard 门
qgate(X, 0)   # Pauli-X 门
qgate(Y, 0)   # Pauli-Y 门
qgate(Z, 0)   # Pauli-Z 门

# 多量子比特门
qgate(CX, 0, 1)  # CNOT 门
qgate(CZ, 0, 1)  # CZ 门

qshow()
```

**预期输出**：

```
backend: native | shots: 1024
Result:
  |00>    512  ( 50.0%)  ####################
  |11>    512  ( 50.0%)  ####################
```

---

## 原理详解

### 电路图

![Basic Gates circuit](/images/basic_gates_circuit.svg)

### 数学推导

**Hadamard 门**

H = (1/√2) [[1, 1], [1, -1]]

作用：
H|0⟩ = (|0⟩ + |1⟩)/√2
H|1⟩ = (|0⟩ - |1⟩)/√2

**Pauli-X 门**

X = [[0, 1], [1, 0]]

作用：
X|0⟩ = |1⟩
X|1⟩ = |0⟩

**Pauli-Y 门**

Y = [[0, -i], [i, 0]]

作用：
Y|0⟩ = i|1⟩
Y|1⟩ = -i|0⟩

**Pauli-Z 门**

Z = [[1, 0], [0, -1]]

作用：
Z|0⟩ = |0⟩
Z|1⟩ = -|1⟩

**CNOT 门**

CX = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]

作用：
CX|00⟩ = |00⟩
CX|01⟩ = |01⟩
CX|10⟩ = |11⟩
CX|11⟩ = |10⟩

### 几何解释

基础门的几何解释（Bloch 球）：

1. H 门：绕 (x+z)/√2 轴旋转 π
2. X 门：绕 x 轴旋转 π
3. Y 门：绕 y 轴旋转 π
4. Z 门：绕 z 轴旋转 π
5. CX 门：控制比特决定是否翻转目标比特

这些门可以在 Bloch 球上直观理解。

---

## 代码详解

```python
from quonic import qgate, qshow  # 导入核心 API
from quonic.gates import CX, CZ, H, X, Y, Z  # 导入门定义

# 单量子比特门
qgate(H, 0)   # Hadamard 门：创建叠加态
qgate(X, 0)   # Pauli-X 门：比特翻转
qgate(Y, 0)   # Pauli-Y 门：比特+相位翻转
qgate(Z, 0)   # Pauli-Z 门：相位翻转

# 多量子比特门
qgate(CX, 0, 1)  # CNOT 门：控制比特翻转
qgate(CZ, 0, 1)  # CZ 门：控制相位翻转

# 测量
qshow()
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `qgate(H, 0)` | H: Hadamard 门, 0: 量子比特索引 | 创建叠加态 |
| `qgate(X, 0)` | X: Pauli-X 门, 0: 量子比特索引 | 比特翻转 |
| `qgate(Y, 0)` | Y: Pauli-Y 门, 0: 量子比特索引 | 比特+相位翻转 |
| `qgate(Z, 0)` | Z: Pauli-Z 门, 0: 量子比特索引 | 相位翻转 |
| `qgate(CX, 0, 1)` | CX: CNOT 门, 0: 控制比特, 1: 目标比特 | 控制比特翻转 |
| `qgate(CZ, 0, 1)` | CZ: CZ 门, 0: 控制比特, 1: 目标比特 | 控制相位翻转 |

---

## 进阶用法

### 场景 1：创建不同态

```python
# |+⟩ 态
qgate(H, 0)
qshow()

# |-⟩ 态
qgate(X, 0)
qgate(H, 0)
qshow()

# |i⟩ 态
qgate(H, 0)
qgate(S, 0)  # S 门：相位 π/2
qshow()
```

### 场景 2：门组合

```python
# HZH = X
qgate(H, 0)
qgate(Z, 0)
qgate(H, 0)
qshow()  # 等价于 X|0⟩ = |1⟩

# HXH = Z
qgate(H, 0)
qgate(X, 0)
qgate(H, 0)
qshow()  # 等价于 Z|0⟩ = |0⟩
```

### 场景 3：噪声下的门

```python
# 无噪声
qshow(noise=0)

# 5% 噪声
qshow(noise=0.05)

# 20% 噪声
qshow(noise=0.20)
```

---

## 适用场景

### 场景 1：量子计算基础

基础门是量子计算的构建块，所有量子算法都由这些门组成。

### 场景 2：量子电路设计

设计量子电路需要理解每个门的作用和组合方式。

### 场景 3：量子算法实现

实现量子算法需要将算法分解为基础门的序列。

---

## 常见问题

### Q1: H 门和 X 门有什么区别？

H 门创建叠加态，X 门翻转比特。H|0⟩ = (|0⟩+|1⟩)/√2，X|0⟩ = |1⟩。

### Q2: CNOT 门的作用是什么？

CNOT 门是受控比特翻转门。如果控制比特是 |1⟩，就翻转目标比特。

### Q3: 量子门是可逆的吗？

是的。所有量子门都是可逆的，因为它们是酉矩阵。

### Q4: 量子门可以并行操作吗？

可以。如果门作用在不同的量子比特上，可以并行执行。

### Q5: 如何选择合适的门？

取决于算法需求。H 门用于创建叠加态，X 门用于翻转比特，CX 门用于创建纠缠。

---

## 学习路径

### 前置知识

- 量子比特的基本概念
- 矩阵和线性代数
- Bloch 球

### 继续学习

- 量子电路设计
- 量子算法
- 量子纠错

### 难度等级

- 当前：初级
- 下一步：中级

---

## 完整示例代码

### 示例 1：基本门演示

```python
from quonic import qgate, qshow
from quonic.gates import CX, CZ, H, X, Y, Z

qgate(H, 0)
qgate(X, 0)
qgate(Y, 0)
qgate(Z, 0)
qgate(CX, 0, 1)
qgate(CZ, 0, 1)
qshow()
```

### 示例 2：门组合演示

```python
from quonic import qgate, qshow
from quonic.gates import H, X, Z

# HZH = X
qgate(H, 0)
qgate(Z, 0)
qgate(H, 0)
qshow()
```

### 运行方式

```bash
python examples/basic_gates/basic_gates.py
```

---

## 下载

- [basic_gates.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/basic_gates/basic_gates.py)
