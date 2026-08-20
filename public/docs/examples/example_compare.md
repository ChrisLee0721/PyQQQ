# Backend Comparison / 后端对比

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

后端对比可以帮助选择最适合的量子后端。

**经典局限**：
- 经典计算机：只有一个后端
- 量子计算机：有多个后端可选

**量子优势**：
- 不同后端有不同的优势
- 智能调度可以自动选择最佳后端
- 后端对比可以帮助理解各后端的特点

**实际应用**：
- 量子算法开发
- 量子硬件测试
- 性能优化

---

## 快速上手

```python
from quonic import qgate, reset, qshow
from quonic.gates import CX, H

# 创建电路
reset()
qgate(H, 0)
for i in range(9):
    qgate(CX, i, i + 1)

# 对比不同后端
for b in ['native', 'qiskit', 'cirq']:
    print(f"\n--- {b} ---")
    qshow(backend=b)
```

**预期输出**：

```
--- native ---
backend: native | shots: 1024
Result:
  |0000000000>    512  ( 50.0%)  ####################
  |1111111111>    512  ( 50.0%)  ####################

--- qiskit ---
backend: qiskit | shots: 1024
Result:
  |0000000000>    512  ( 50.0%)  ####################
  |1111111111>    512  ( 50.0%)  ####################

--- cirq ---
backend: cirq | shots: 1024
Result:
  |0000000000>    512  ( 50.0%)  ####################
  |1111111111>    512  ( 50.0%)  ####################
```

---

## 原理详解

### 电路图

![Backend Comparison circuit](/images/compare_circuit.svg)

### 数学推导

**后端对比的数学基础**

所有后端都模拟相同的量子电路，但实现方式不同：

1. native：Python 实现
2. qiskit：Qiskit Aer 实现
3. cirq：Google Cirq 实现

**结果一致性**

理想情况下，所有后端应该给出相同的结果。
实际中，由于浮点精度和随机性，结果可能略有不同。

### 几何解释

后端对比的几何解释：

1. 所有后端都模拟相同的量子态
2. 但实现方式不同
3. 结果应该一致

这就像用不同的计算器计算同一个数学问题。

---

## 代码详解

```python
from quonic import qgate, reset, qshow  # 导入核心 API
from quonic.gates import CX, H         # 导入门定义

# 创建电路
reset()  # 重置电路
qgate(H, 0)  # Hadamard 门
for i in range(9):
    qgate(CX, i, i + 1)  # CNOT 链

# 对比不同后端
for b in ['native', 'qiskit', 'cirq']:
    print(f"\n--- {b} ---")
    qshow(backend=b)  # 指定后端
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `qshow(backend='native')` | backend: 后端名称 | 使用 native 后端 |
| `qshow(backend='qiskit')` | backend: 后端名称 | 使用 qiskit 后端 |
| `qshow(backend='cirq')` | backend: 后端名称 | 使用 cirq 后端 |

---

## 进阶用法

### 场景 1：不同规模电路

```python
# 小规模电路
reset()
qgate(H, 0)
qgate(CX, 0, 1)
qshow(backend='native')

# 大规模电路
reset()
qgate(H, 0)
for i in range(19):
    qgate(CX, i, i + 1)
qshow(backend='native')
```

### 场景 2：不同后端的性能

```python
import time

# 测量不同后端的运行时间
for b in ['native', 'qiskit', 'cirq']:
    reset()
    qgate(H, 0)
    for i in range(9):
        qgate(CX, i, i + 1)
    t0 = time.time()
    qshow(backend=b)
    print(f"{b}: {time.time()-t0:.3f}s")
```

### 场景 3：智能调度

```python
# 智能调度：自动选择最佳后端
qshow()  # 不指定后端，自动选择
```

---

## 适用场景

### 场景 1：量子算法开发

后端对比可以帮助选择最适合的后端来开发量子算法。

### 场景 2：量子硬件测试

后端对比可以用于测试不同量子硬件的性能。

### 场景 3：性能优化

后端对比可以用于优化量子电路的性能。

---

## 常见问题

### Q1: 不同后端的结果应该一致吗？

理想情况下应该一致。实际中，由于浮点精度和随机性，结果可能略有不同。

### Q2: 如何选择最佳后端？

取决于电路规模、噪声要求、性能需求等。智能调度可以自动选择。

### Q3: native 后端和其他后端有什么区别？

native 是 Python 实现，其他后端使用各自的 SDK。native 通常更快，但功能更少。

### Q4: 后端对比需要多少时间？

取决于电路规模和后端数量。通常几秒到几分钟。

### Q5: 后端对比的结果如何分析？

比较结果的一致性、运行时间、内存使用等。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 量子测量
- 不同量子后端

### 继续学习

- 智能调度
- 性能优化
- 量子硬件测试

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本后端对比

```python
from quonic import qgate, reset, qshow
from quonic.gates import CX, H

reset()
qgate(H, 0)
for i in range(9):
    qgate(CX, i, i + 1)

for b in ['native', 'qiskit', 'cirq']:
    print(f"\n--- {b} ---")
    qshow(backend=b)
```

### 示例 2：性能对比

```python
import time
from quonic import qgate, reset, qshow
from quonic.gates import CX, H

for b in ['native', 'qiskit', 'cirq']:
    reset()
    qgate(H, 0)
    for i in range(9):
        qgate(CX, i, i + 1)
    t0 = time.time()
    qshow(backend=b)
    print(f"{b}: {time.time()-t0:.3f}s")
```

### 运行方式

```bash
python examples/compare/compare.py
```

---

## 下载

- [compare.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/compare/compare.py)
