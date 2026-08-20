# Classical While / 经典循环

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

经典循环是量子计算中的经典控制流，允许重复执行操作直到满足条件。

**经典局限**：
- 经典循环：while 循环
- 量子循环：cwhile 循环

**量子优势**：
- 经典循环可以在测量后执行
- 经典循环可以用于迭代算法
- 经典循环是量子算法的重要组件

**实际应用**：
- 量子算法
- 量子纠错
- 量子控制

---

## 快速上手

```python
from quonic import qgate, cwhile, qshow
from quonic.gates import CX, H, X

# 创建叠加态
qgate(H, 0)

# 经典循环
cwhile(0).do(X, 1)

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

![Classical While circuit](/images/cwhile_circuit.svg)

### 数学推导

**经典循环的数学基础**

cwhile(0).do(X, 1) 的作用：

测量 q₀，如果结果是 |1⟩，对 q₁ 执行 X 门，然后重复。
如果结果是 |0⟩，停止循环。

**状态演化**

初始态：|ψ₀⟩ = (|0⟩ + |1⟩)/√2 ⊗ |0⟩

第一次测量：
- 50% 概率：|00⟩ → 停止
- 50% 概率：|10⟩ → 执行 X 门 → |11⟩

第二次测量：
- 50% 概率：|11⟩ → 停止
- 50% 概率：|10⟩ → 执行 X 门 → |11⟩

最终结果：
- 50% 概率：|00⟩
- 50% 概率：|11⟩

### 几何解释

经典循环的几何解释：

1. 初始态：在 Bloch 球上的点
2. 测量：坍缩到确定态
3. 循环：根据测量结果重复执行操作
4. 结果：经典关联态

这就像根据测量结果重复执行代码。

---

## 代码详解

```python
from quonic import qgate, cwhile, qshow  # 导入核心 API
from quonic.gates import CX, H, X        # 导入门定义

# 创建叠加态
qgate(H, 0)  # q₀ → (|0⟩+|1⟩)/√2

# 经典循环
cwhile(0).do(X, 1)  # 如果 q₀ 是 |1⟩，对 q₁ 执行 X 门，重复

# 测量
qshow()
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `cwhile(control).do(gate, target)` | control: 控制比特, gate: 门, target: 目标比特 | 经典循环 |
| `qshow()` | 无参数 | 运行电路并显示结果 |

---

## 进阶用法

### 场景 1：不同循环条件

```python
# cwhile(0).do(X, 1)
qgate(H, 0)
cwhile(0).do(X, 1)
qshow()

# cwhile(1).do(X, 0)
qgate(H, 1)
cwhile(1).do(X, 0)
qshow()
```

### 场景 2：多比特循环

```python
# 多比特循环
qgate(H, 0)
qgate(H, 1)
cwhile(0).do(X, 2)
cwhile(1).do(X, 2)
qshow()
```

### 场景 3：循环用于算法

```python
# 循环用于量子算法
# 例如：Grover 搜索
```

---

## 适用场景

### 场景 1：量子算法

经典循环是量子算法的重要组件。

### 场景 2：量子纠错

经典循环用于量子纠错码的实现。

### 场景 3：量子控制

经典循环用于量子控制和量子反馈。

---

## 常见问题

### Q1: cwhile 和 qif 有什么区别？

cwhile 是循环，qif 是条件分支。cwhile 会重复执行，qif 只执行一次。

### Q2: cwhile 可以嵌套吗？

可以。cwhile 可以嵌套使用。

### Q3: cwhile 的执行时间如何？

cwhile 的执行时间取决于循环次数和操作。

### Q4: cwhile 可以用于所有量子比特吗？

可以。cwhile 可以用于任何量子比特。

### Q5: cwhile 的精度如何？

cwhile 的精度取决于测量的精度。

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

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本经典循环

```python
from quonic import qgate, cwhile, qshow
from quonic.gates import H, X

qgate(H, 0)
cwhile(0).do(X, 1)
qshow()
```

### 示例 2：多比特循环

```python
from quonic import qgate, cwhile, qshow
from quonic.gates import H, X

qgate(H, 0)
qgate(H, 1)
cwhile(0).do(X, 2)
cwhile(1).do(X, 2)
qshow()
```

### 运行方式

```bash
python examples/cwhile/cwhile.py
```

---

## 下载

- [cwhile.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/cwhile/cwhile.py)
