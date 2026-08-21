# Mark State / 标记态

> **Algorithms** / 算法 | 难度：中级 | 预计时间：10 分钟

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

标记态用于标记目标态。

**经典局限**：
- 经典标记：函数
- 量子标记：Oracle

**量子优势**：
- 可以标记目标态
- 是量子算法的基础

**实际应用**：
- 量子搜索
- 量子算法
- 量子算法教学

---

## 快速上手

```python
from quonic.algorithms import mark_state

# 标记态
oracle = mark_state("11")
print(oracle)
```

**预期输出**：

```
Oracle for state '11'
```

---

## 原理详解

### 电路图

![Mark State circuit](/images/mark_state_circuit.svg)

### 数学推导

**标记态算法**

目标：标记目标态。

**算法步骤**：
1. 定义：定义目标态
2. 构建：构建 Oracle
3. 输出：输出 Oracle

**数学推导**：
U|x⟩ = -|x⟩ if x = target
U|x⟩ = |x⟩ otherwise

### 几何解释

标记态的几何解释：

1. 目标态：要标记的态
2. Oracle：标记目标态
3. 输出：Oracle

这就像在 Bloch 球上标记目标态。

---

## 代码详解

```python
from quonic.algorithms import mark_state  # 导入算法

# mark_state(target)
# target: 目标态
oracle = mark_state("11")

# oracle: Oracle
print(oracle)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `mark_state(target)` | target: 目标态 | 创建标记态 Oracle |
| `oracle` | 无参数 | Oracle |

---

## 进阶用法

### 场景 1：不同目标态

```python
# 不同目标态
oracle1 = mark_state("00")
print(oracle1)

oracle2 = mark_state("11")
print(oracle2)
```

### 场景 2：标记态用于量子搜索

```python
# 标记态可以用于量子搜索
# 标记目标态
```

### 场景 3：标记态用于量子算法

```python
# 标记态可以用于量子算法
# 标记目标态
```

---

## 适用场景

### 场景 1：量子搜索

标记态可以用于量子搜索。

### 场景 2：量子算法

标记态可以用于量子算法。

### 场景 3：量子算法教学

标记态是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: 标记态的精度如何？

精度取决于目标态。

### Q2: 标记态需要多少量子比特？

取决于目标态。

### Q3: 标记态和 Oracle 有什么区别？

标记态是 Oracle 的特例。

### Q4: 标记态在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 标记态的复杂度如何？

复杂度取决于目标态。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 量子测量
- 量子算法基础

### 继续学习

- 量子搜索
- 量子算法
- 量子算法教学

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本标记态

```python
from quonic.algorithms import mark_state

oracle = mark_state("11")
print(oracle)
```

### 示例 2：不同目标态

```python
from quonic.algorithms import mark_state

oracle1 = mark_state("00")
print(oracle1)

oracle2 = mark_state("11")
print(oracle2)
```

### 运行方式

```bash
python examples/mark_state/mark_state.py
```

---

## 下载

- [mark_state.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/mark_state/mark_state.py)
