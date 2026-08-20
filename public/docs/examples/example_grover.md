# Grover Search / Grover 搜索

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

在无序数据库中查找目标，经典算法需要 O(N) 次查询，Grover 算法只需要 O(√N) 次。

**经典局限**：
- 经典搜索：最坏情况需要遍历所有 N 个元素
- 对于 N=10⁶，经典需要 10⁶ 次，量子只需要 10³ 次

**量子优势**：
- 二次加速：O(√N) vs O(N)
- 对于大规模搜索问题，加速效果显著
- 是许多量子算法的基础（振幅放大、量子计数）

**实际应用**：
- 数据库搜索
- 密码学（搜索密钥空间）
- 优化问题（寻找最优解）
- SAT 求解

---

## 快速上手

```python
from quonic.algorithms import grover

# 在 2 个量子比特中搜索 |11⟩
result = grover("11", 2, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'11': 1008, '00': 6, '01': 5, '10': 5}
```

---

## 原理详解

### 电路图

![Grover Search circuit](/images/grover_circuit.svg)

### 数学推导

**Step 1: 初始化**

对所有量子比特施加 H 门，创建均匀叠加态：
|ψ₀⟩ = (|00⟩ + |01⟩ + |10⟩ + |11⟩)/2

**Step 2: Oracle 标记**

Oracle 翻转目标态 |11⟩ 的相位：
|ψ₁⟩ = (|00⟩ + |01⟩ + |10⟩ - |11⟩)/2

**Step 3: Diffusion 算子**

Diffusion 算子关于平均振幅反射：
- 平均振幅 = (1/4 + 1/4 + 1/4 - 1/4)/4 = 1/8
- 反射后：|11⟩ 的振幅被放大

**Step 4: 迭代**

重复 Oracle + Diffusion，每次迭代都放大目标态的振幅。

**Step 5: 测量**

最优迭代次数 ≈ π√N/4，测量后目标态概率 ≈ 100%。

### 几何解释

Grover 算法的几何解释：

1. 初始态在均匀叠加态空间中
2. Oracle 标记目标态，翻转其相位
3. Diffusion 关于平均振幅反射
4. 每次迭代，目标态的振幅被放大
5. 经过 ~√N 次迭代，目标态概率接近 100%

这就像荡秋千一样，每次推一下，幅度越来越大。

---

## 代码详解

```python
from quonic.algorithms import grover  # 导入 Grover 算法

# grover(target, n_qubits, shots)
# target: 目标态的比特串
# n_qubits: 量子比特数
# shots: 测量次数
result = grover("11", 2, shots=1024)

# result.counts: 测量结果的统计
# 例如：{'11': 1008, '00': 6, '01': 5, '10': 5}
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `grover(target, n_qubits, shots)` | target: 目标态, n_qubits: 量子比特数, shots: 测量次数 | 执行 Grover 搜索 |
| `result.counts` | 无参数 | 测量结果的统计 |

---

## 进阶用法

### 场景 1：多量子比特搜索

```python
# 在 3 个量子比特中搜索 |101⟩
result = grover("101", 3, shots=1024)
print(result.counts)
```

### 场景 2：多目标搜索

```python
# 搜索多个目标
from quonic.algorithms import grover_multi
result = grover_multi(["00", "11"], 2, shots=1024)
print(result.counts)
```

### 场景 3：Grover 搜索用于优化

```python
# Grover 搜索可以用于寻找最优解
# 例如：在 4 个选项中找最优
result = grover("11", 2, shots=1024)
# |11⟩ 对应最优解
```

---

## 适用场景

### 场景 1：数据库搜索

在无序数据库中查找目标，经典需要 O(N)，量子只需要 O(√N)。

### 场景 2：密码学

搜索密钥空间，可以加速暴力破解。

### 场景 3：优化问题

寻找最优解，可以加速组合优化问题的求解。

---

## 常见问题

### Q1: Grover 搜索的加速比是多少？

二次加速：O(√N) vs O(N)。对于 N=10⁶，经典需要 10⁶ 次，量子只需要 10³ 次。

### Q2: Grover 搜索需要多少次迭代？

最优迭代次数 ≈ π√N/4。对于 N=4（2 量子比特），只需要 1 次迭代。

### Q3: Grover 搜索能找到所有目标吗？

Grover 搜索只能找到一个目标。如果需要找所有目标，需要多次运行。

### Q4: Grover 搜索的局限性是什么？

1) 需要知道目标态的描述；2) 只能找一个目标；3) 对于小规模问题，经典算法可能更快。

### Q5: Grover 搜索和振幅放大有什么区别？

Grover 搜索是振幅放大在均匀初始态下的特例。振幅放大更通用，支持任意初始态。

---

## 学习路径

### 前置知识

- 量子比特和叠加态
- Hadamard 门和 CNOT 门
- 量子测量

### 继续学习

- 振幅放大（Grover 的推广）
- 量子计数（计算目标数量）
- 量子优化算法

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本 Grover 搜索

```python
from quonic.algorithms import grover

result = grover("11", 2, shots=1024)
print(result.counts)
```

### 示例 2：3 量子比特 Grover 搜索

```python
from quonic.algorithms import grover

result = grover("101", 3, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/grover/grover.py
```

---

## 下载

- [grover.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/grover/grover.py)
