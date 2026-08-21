# Groverize / Grover 化

> **Compiler** / 编译器 | 难度：高级 | 预计时间：15 分钟

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

Grover 化用于将经典循环转换为 Grover 电路。

**经典局限**：
- 经典循环：需要中段测量
- Grover 化：不需要中段测量

**量子优势**：
- 可以在不支持中段测量的设备上运行
- 是算法级编译的基础

**实际应用**：
- 量子编译
- 量子算法
- 量子算法教学

---

## 快速上手

```python
from quonic.compiler import groverize

# Grover 化
result = groverize(circuit, method="grover")
print(result)
```

**预期输出**：

```
Circuit with 103 operations
```

---

## 原理详解

### 电路图

![Groverize circuit](/images/groverize_circuit.svg)

### 数学推导

**Grover 化算法**

目标：将经典循环转换为 Grover 电路。

**算法步骤**：
1. 分析：分析循环结构
2. 构建：构建 Oracle
3. 迭代：应用 Grover 迭代
4. 输出：输出电路

**数学推导**：
|ψ⟩ = Grover^k |+⟩^n
其中 k 是迭代次数

### 几何解释

Grover 化的几何解释：

1. 循环：经典循环结构
2. Oracle：标记目标态
3. Grover 迭代：放大目标态概率
4. 输出：静态电路

这就像将动态循环转换为静态电路。

---

## 代码详解

```python
from quonic.compiler import groverize  # 导入编译器

# groverize(circuit, method)
# circuit: 量子电路
# method: 方法（"grover" 或 "fpaa"）
result = groverize(circuit, method="grover")

# result: Grover 化后的电路
print(result)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `groverize(circuit, method)` | circuit: 量子电路, method: 方法 | 执行 Grover 化 |
| `result` | 无参数 | Grover 化后的电路 |

---

## 进阶用法

### 场景 1：不同方法

```python
# Grover 方法
result = groverize(circuit, method="grover")
print(result)

# FPAA 方法
result = groverize(circuit, method="fpaa")
print(result)
```

### 场景 2：Grover 化用于量子编译

```python
# Grover 化可以用于量子编译
# 将经典循环转换为 Grover 电路
```

### 场景 3：Grover 化用于量子算法

```python
# Grover 化可以用于量子算法
# 例如：cwhile 循环
```

---

## 适用场景

### 场景 1：量子编译

Grover 化可以用于量子编译。

### 场景 2：量子算法

Grover 化可以用于量子算法。

### 场景 3：量子算法教学

Grover 化是量子算法的经典例子，用于教学。

---

## 常见问题

### Q1: Grover 化的精度如何？

精度取决于循环复杂度和方法。

### Q2: Grover 化需要多少量子比特？

取决于循环复杂度。

### Q3: Grover 化和经典循环有什么区别？

Grover 化不需要中段测量。

### Q4: Grover 化在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: Grover 化的复杂度如何？

复杂度取决于循环复杂度。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- Grover 搜索
- 量子编译

### 继续学习

- 量子编译
- 量子算法
- 量子算法教学

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本 Grover 化

```python
from quonic.compiler import groverize

result = groverize(circuit, method="grover")
print(result)
```

### 示例 2：不同方法

```python
from quonic.compiler import groverize

result = groverize(circuit, method="grover")
print(result)

result = groverize(circuit, method="fpaa")
print(result)
```

### 运行方式

```bash
python examples/groverize/groverize.py
```

---

## 下载

- [groverize.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/groverize/groverize.py)
