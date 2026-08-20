# Quantum If / 量子条件分支

> **Advanced** / 高级 | 难度：高级 | 预计时间：15 分钟

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

量子条件分支是量子计算中的高级特性，允许根据量子态执行不同操作。

**经典局限**：
- 经典条件分支：if-else 语句
- 量子条件分支：qif 语句

**量子优势**：
- 量子条件分支可以在叠加态上执行
- 量子条件分支可以创建分支叠加
- 量子条件分支是量子算法的重要组件

**实际应用**：
- 量子算法
- 量子纠错
- 量子控制

---

## 快速上手

```python
from quonic import qgate, qif, qshow
from quonic.gates import CX, H, X

# 创建叠加态
qgate(H, 0)

# 量子条件分支
qif(0).then(X, 1)

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

![Quantum If circuit](/images/qif_circuit.svg)

### 数学推导

**量子条件分支的数学基础**

qif(0).then(X, 1) 的作用：

如果 q₀ 是 |0⟩，不执行任何操作。
如果 q₀ 是 |1⟩，对 q₁ 执行 X 门。

**状态演化**

初始态：|ψ₀⟩ = (|0⟩ + |1⟩)/√2 ⊗ |0⟩

qif(0).then(X, 1) 后：
|ψ₁⟩ = (|00⟩ + |11⟩)/√2

**效果**

创建了 Bell 态。

### 几何解释

量子条件分支的几何解释：

1. 初始态：在 Bloch 球上的点
2. 条件分支：根据控制比特的状态执行不同操作
3. 结果：创建纠缠态

这就像根据条件执行不同的代码分支。

---

## 代码详解

```python
from quonic import qgate, qif, qshow  # 导入核心 API
from quonic.gates import CX, H, X     # 导入门定义

# 创建叠加态
qgate(H, 0)  # q₀ → (|0⟩+|1⟩)/√2

# 量子条件分支
qif(0).then(X, 1)  # 如果 q₀ 是 |1⟩，对 q₁ 执行 X 门

# 测量
qshow()
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `qif(control).then(gate, target)` | control: 控制比特, gate: 门, target: 目标比特 | 量子条件分支 |
| `qshow()` | 无参数 | 运行电路并显示结果 |

---

## 进阶用法

### 场景 1：不同条件分支

```python
# qif(0).then(X, 1)
qgate(H, 0)
qif(0).then(X, 1)
qshow()

# qif(1).then(X, 0)
qgate(H, 1)
qif(1).then(X, 0)
qshow()
```

### 场景 2：多比特条件分支

```python
# 多比特条件分支
qgate(H, 0)
qgate(H, 1)
qif(0).then(X, 2)
qif(1).then(X, 2)
qshow()
```

### 场景 3：条件分支用于算法

```python
# 条件分支用于量子算法
# 例如：量子隐形传态
```

---

## 适用场景

### 场景 1：量子算法

量子条件分支是量子算法的重要组件。

### 场景 2：量子纠错

量子条件分支用于量子纠错码的实现。

### 场景 3：量子控制

量子条件分支用于量子控制和量子反馈。

---

## 常见问题

### Q1: qif 和经典 if 有什么区别？

qif 在叠加态上执行，经典 if 在确定态上执行。

### Q2: qif 可以嵌套吗？

可以。qif 可以嵌套使用。

### Q3: qif 的执行时间如何？

qif 的执行时间取决于条件和操作。

### Q4: qif 可以用于所有量子比特吗？

可以。qif 可以用于任何量子比特。

### Q5: qif 的精度如何？

qif 的精度取决于量子门的精度。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 叠加态
- 量子测量

### 继续学习

- 量子算法
- 量子纠错
- 量子控制

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本量子条件分支

```python
from quonic import qgate, qif, qshow
from quonic.gates import H, X

qgate(H, 0)
qif(0).then(X, 1)
qshow()
```

### 示例 2：多比特条件分支

```python
from quonic import qgate, qif, qshow
from quonic.gates import H, X

qgate(H, 0)
qgate(H, 1)
qif(0).then(X, 2)
qif(1).then(X, 2)
qshow()
```

### 运行方式

```bash
python examples/qif/qif.py
```

---

## 下载

- [qif.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qif/qif.py)
