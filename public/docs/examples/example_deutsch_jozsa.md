# Deutsch-Jozsa / Deutsch-Jozsa 算法

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

Deutsch-Jozsa 算法用于判断函数是常数还是平衡的，比经典算法快指数倍。

**经典局限**：
- 经典算法：最坏情况需要 2^{n-1}+1 次查询
- 量子算法：只需要 1 次查询

**量子优势**：
- 指数加速：O(1) vs O(2^{n-1})
- 是量子算法的经典例子

**实际应用**：
- 量子算法教学
- 量子优势演示

---

## 快速上手

```python
from quonic.algorithms import deutsch_jozsa

# 判断函数是常数还是平衡的
result = deutsch_jozsa("balanced", shots=1024)
print(result.counts)  # 非零结果表示平衡函数
```

**预期输出**：

```
{'1': 1024}
```

---

## 原理详解

### 电路图

![Deutsch-Jozsa circuit](/images/deutsch_jozsa_circuit.svg)

### 数学推导

**Deutsch-Jozsa 算法**

目标：判断函数 f 是常数还是平衡的。

Oracle：
- 常数函数：f(x) = 0 或 f(x) = 1
- 平衡函数：f(x) = 0 和 f(x) = 1 各一半

**算法步骤**：
1. 初始化：|0⟩^n |1⟩
2. Hadamard：创建叠加态
3. Oracle：应用 Oracle
4. Hadamard：干涉
5. 测量：判断函数类型

**数学推导**：
|ψ₀⟩ = |0⟩^n |1⟩
|ψ₁⟩ = |+⟩^n |-⟩
|ψ₂⟩ = (1/√N) Σ_x (-1)^{f(x)} |x⟩
|ψ₃⟩ = |0⟩^n（常数）或非零（平衡）

### 几何解释

Deutsch-Jozsa 的几何解释：

1. 初始态：|0⟩^n |1⟩
2. Hadamard：创建叠加态
3. Oracle：标记函数类型
4. 干涉：放大或抵消
5. 测量：判断函数类型

这就像用量子干涉来判断函数的性质。

---

## 代码详解

```python
from quonic.algorithms import deutsch_jozsa  # 导入算法

# deutsch_jozsa(function_type, shots)
# function_type: "constant" 或 "balanced"
# shots: 测量次数
result = deutsch_jozsa("balanced", shots=1024)

# result.counts: 测量结果
# 非零结果表示平衡函数
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `deutsch_jozsa(function_type, shots)` | function_type: "constant" 或 "balanced", shots: 测量次数 | 执行算法 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同函数类型

```python
# 常数函数
result = deutsch_jozsa("constant", shots=1024)
print(result.counts)

# 平衡函数
result = deutsch_jozsa("balanced", shots=1024)
print(result.counts)
```

### 场景 2：噪声下的算法

```python
# 无噪声
result = deutsch_jozsa("balanced", shots=1024, noise=0)
print(result.counts)

# 5% 噪声
result = deutsch_jozsa("balanced", shots=1024, noise=0.05)
print(result.counts)
```

### 场景 3：算法比较

```python
# Deutsch-Jozsa vs 经典算法
# 经典：最坏情况需要 2^{n-1}+1 次查询
# 量子：只需要 1 次查询
```

---

## 适用场景

### 场景 1：量子算法教学

Deutsch-Jozsa 算法是量子算法的经典例子，用于教学。

### 场景 2：量子优势演示

Deutsch-Jozsa 算法展示了量子计算的优势。

### 场景 3：函数性质判断

Deutsch-Jozsa 算法可以用于判断函数的性质。

---

## 常见问题

### Q1: Deutsch-Jozsa 算法的加速比是多少？

指数加速：O(1) vs O(2^{n-1})。

### Q2: Deutsch-Jozsa 算法需要多少量子比特？

需要 N+1 个量子比特，其中 N 是输入比特数。

### Q3: Deutsch-Jozsa 算法和 Bernstein-Vazirani 算法有什么区别？

Deutsch-Jozsa 判断函数类型，Bernstein-Vazirani 找隐藏比特串。

### Q4: Deutsch-Jozsa 算法在 NISQ 设备上能跑吗？

可以。Deutsch-Jozsa 算法对噪声有一定的鲁棒性。

### Q5: Deutsch-Jozsa 算法的精度如何？

理想情况下精度为 100%。实际中受噪声影响，精度会降低。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- Hadamard 门
- 量子测量

### 继续学习

- Bernstein-Vazirani 算法
- Simon 算法
- 量子密码学

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本 Deutsch-Jozsa

```python
from quonic.algorithms import deutsch_jozsa

result = deutsch_jozsa("balanced", shots=1024)
print(result.counts)
```

### 示例 2：不同函数类型

```python
from quonic.algorithms import deutsch_jozsa

result = deutsch_jozsa("constant", shots=1024)
print(result.counts)

result = deutsch_jozsa("balanced", shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/deutsch_jozsa/deutsch_jozsa.py
```

---

## 下载

- [deutsch_jozsa.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/deutsch_jozsa/deutsch_jozsa.py)
