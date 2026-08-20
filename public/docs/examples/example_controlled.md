# Controlled Gates / 受控门

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

受控门是量子计算的核心，用于创建纠缠和实现量子算法。

**经典局限**：
- 经典逻辑门：AND、OR、NOT
- 量子受控门：CX、CZ、CCX

**量子优势**：
- 受控门可以创建纠缠
- 受控门可以实现量子算法
- 受控门是量子计算的基础

**实际应用**：
- 量子纠缠
- 量子算法
- 量子纠错

---

## 快速上手

```python
from quonic import qgate, qshow
from quonic.gates import CX, CZ, H

# CNOT 门
qgate(H, 0)
qgate(CX, 0, 1)
qshow()

# CZ 门
qgate(H, 0)
qgate(CZ, 0, 1)
qshow()
```

**预期输出**：

```
CNOT:
  |00>     512  ( 50.0%)  ####################
  |11>     512  ( 50.0%)  ####################

CZ:
  |00>     512  ( 50.0%)  ####################
  |01>     512  ( 50.0%)  ####################
  |10>     512  ( 50.0%)  ####################
  |11>     512  ( 50.0%)  ####################
```

---

## 原理详解

### 电路图

![Controlled Gates circuit](/images/controlled_circuit.svg)

### 数学推导

**CNOT 门**

CX = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]

作用：
CX|00⟩ = |00⟩
CX|01⟩ = |01⟩
CX|10⟩ = |11⟩
CX|11⟩ = |10⟩

**CZ 门**

CZ = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]]

作用：
CZ|00⟩ = |00⟩
CZ|01⟩ = |01⟩
CZ|10⟩ = |10⟩
CZ|11⟩ = -|11⟩

### 几何解释

受控门的几何解释：

1. CNOT 门：控制比特决定是否翻转目标比特
2. CZ 门：控制比特决定是否翻转目标比特的相位
3. CCX 门：两个控制比特都为 |1⟩ 时翻转目标比特

这就像条件语句：if (control) then (action)。

---

## 代码详解

```python
from quonic import qgate, qshow  # 导入核心 API
from quonic.gates import CX, CZ, H  # 导入门定义

# CNOT 门
qgate(H, 0)      # 创建叠加态
qgate(CX, 0, 1)  # CNOT：控制=q₀，目标=q₁
qshow()

# CZ 门
qgate(H, 0)      # 创建叠加态
qgate(CZ, 0, 1)  # CZ：控制=q₀，目标=q₁
qshow()
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `qgate(CX, 0, 1)` | CX: CNOT 门, 0: 控制比特, 1: 目标比特 | 控制比特翻转 |
| `qgate(CZ, 0, 1)` | CZ: CZ 门, 0: 控制比特, 1: 目标比特 | 控制相位翻转 |
| `qgate(CCX, 0, 1, 2)` | CCX: Toffoli 门, 0/1: 控制比特, 2: 目标比特 | 双控制比特翻转 |

---

## 进阶用法

### 场景 1：不同受控门

```python
# CNOT 门
qgate(H, 0)
qgate(CX, 0, 1)
qshow()

# CZ 门
qgate(H, 0)
qgate(CZ, 0, 1)
qshow()

# CCX 门
qgate(H, 0)
qgate(H, 1)
qgate(CCX, 0, 1, 2)
qshow()
```

### 场景 2：受控门创建纠缠

```python
# Bell 态
qgate(H, 0)
qgate(CX, 0, 1)
qshow()

# GHZ 态
qgate(H, 0)
qgate(CX, 0, 1)
qgate(CX, 1, 2)
qshow()
```

### 场景 3：受控门用于算法

```python
# Grover 搜索
from quonic.algorithms import grover
result = grover("11", 2, shots=1024)
print(result.counts)
```

---

## 适用场景

### 场景 1：量子纠缠

受控门是创建纠缠的主要工具。

### 场景 2：量子算法

受控门是量子算法的核心组件。

### 场景 3：量子纠错

受控门用于量子纠错码的实现。

---

## 常见问题

### Q1: CNOT 和 CZ 有什么区别？

CNOT 翻转目标比特，CZ 翻转目标比特的相位。

### Q2: CCX 门需要多少量子比特？

CCX 门需要 3 个量子比特：2 个控制比特 + 1 个目标比特。

### Q3: 受控门可以创建纠缠吗？

可以。CNOT 门是创建纠缠的主要工具。

### Q4: 受控门是可逆的吗？

是的。所有受控门都是可逆的。

### Q5: 受控门有哪些类型？

常见的有 CNOT、CZ、CCX、CSWAP 等。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- Hadamard 门
- 纠缠

### 继续学习

- 量子纠缠
- 量子算法
- 量子纠错

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本受控门

```python
from quonic import qgate, qshow
from quonic.gates import CX, CZ, H

qgate(H, 0)
qgate(CX, 0, 1)
qshow()
```

### 示例 2：CCX 门

```python
from quonic import qgate, qshow
from quonic.gates import CCX, H

qgate(H, 0)
qgate(H, 1)
qgate(CCX, 0, 1, 2)
qshow()
```

### 运行方式

```bash
python examples/controlled/controlled.py
```

---

## 下载

- [controlled.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/controlled/controlled.py)
