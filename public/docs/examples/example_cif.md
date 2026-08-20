# Classical If / 经典条件分支

> **Advanced** / 高级 | 难度：中级 | 预计时间：10 分钟

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

经典条件分支是量子计算中的经典控制流。

**经典局限**：
- 经典条件分支：if-else 语句
- 量子条件分支：qif 语句

**量子优势**：
- 经典条件分支可以在测量后执行
- 经典条件分支可以用于经典控制流
- 经典条件分支是量子算法的重要组件

**实际应用**：
- 量子算法
- 量子纠错
- 量子控制

---

## 快速上手

```python
from quonic import qgate, cif, qshow
from quonic.gates import CX, H, X

# 创建叠加态
qgate(H, 0)

# 测量
qshow()

# 经典条件分支
cif(0).then(X, 1)

qshow()
```

**预期输出**：

```
第一次测量：
  |0>      512  ( 50.0%)  ####################
  |1>      512  ( 50.0%)  ####################

第二次测量：
  |00>     512  ( 50.0%)  ####################
  |11>     512  ( 50.0%)  ####################
```

---

## 原理详解

### 电路图

![Classical If circuit](/images/cif_circuit.svg)

### 数学推导

**经典条件分支的数学基础**

cif(0).then(X, 1) 的作用：

测量 q₀，如果结果是 |0⟩，不执行任何操作。
如果结果是 |1⟩，对 q₁ 执行 X 门。

**状态演化**

初始态：|ψ₀⟩ = (|0⟩ + |1⟩)/√2 ⊗ |0⟩

测量后：
- 50% 概率：|00⟩
- 50% 概率：|10⟩

cif(0).then(X, 1) 后：
- 50% 概率：|00⟩
- 50% 概率：|11⟩

### 几何解释

经典条件分支的几何解释：

1. 初始态：在 Bloch 球上的点
2. 测量：坍缩到确定态
3. 条件分支：根据测量结果执行不同操作
4. 结果：经典关联态

这就像根据测量结果执行不同的代码分支。

---

## 代码详解

```python
from quonic import qgate, cif, qshow  # 导入核心 API
from quonic.gates import CX, H, X     # 导入门定义

# 创建叠加态
qgate(H, 0)  # q₀ → (|0⟩+|1⟩)/√2

# 测量
qshow()  # 测量 q₀

# 经典条件分支
cif(0).then(X, 1)  # 如果 q₀ 是 |1⟩，对 q₁ 执行 X 门

# 再次测量
qshow()
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `cif(control).then(gate, target)` | control: 控制比特, gate: 门, target: 目标比特 | 经典条件分支 |
| `qshow()` | 无参数 | 运行电路并显示结果 |

---

## 进阶用法

### 场景 1：不同条件分支

```python
# cif(0).then(X, 1)
qgate(H, 0)
qshow()
cif(0).then(X, 1)
qshow()

# cif(1).then(X, 0)
qgate(H, 1)
qshow()
cif(1).then(X, 0)
qshow()
```

### 场景 2：多比特条件分支

```python
# 多比特条件分支
qgate(H, 0)
qgate(H, 1)
qshow()
cif(0).then(X, 2)
cif(1).then(X, 2)
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

经典条件分支是量子算法的重要组件。

### 场景 2：量子纠错

经典条件分支用于量子纠错码的实现。

### 场景 3：量子控制

经典条件分支用于量子控制和量子反馈。

---

## 常见问题

### Q1: cif 和 qif 有什么区别？

cif 在测量后执行，qif 在叠加态上执行。

### Q2: cif 可以嵌套吗？

可以。cif 可以嵌套使用。

### Q3: cif 的执行时间如何？

cif 的执行时间取决于条件和操作。

### Q4: cif 可以用于所有量子比特吗？

可以。cif 可以用于任何量子比特。

### Q5: cif 的精度如何？

cif 的精度取决于测量的精度。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 量子测量
- 经典控制流

### 继续学习

- 量子算法
- 量子纠错
- 量子控制

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本经典条件分支

```python
from quonic import qgate, cif, qshow
from quonic.gates import H, X

qgate(H, 0)
qshow()
cif(0).then(X, 1)
qshow()
```

### 示例 2：多比特条件分支

```python
from quonic import qgate, cif, qshow
from quonic.gates import H, X

qgate(H, 0)
qgate(H, 1)
qshow()
cif(0).then(X, 2)
cif(1).then(X, 2)
qshow()
```

### 运行方式

```bash
python examples/cif/cif.py
```

---

## 下载

- [cif.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/cif/cif.py)
