# Smart Scheduling / 智能调度

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

智能调度可以自动选择最佳后端，无需手动指定。

**经典局限**：
- 经典计算机：只有一个后端
- 量子计算机：有多个后端可选

**量子优势**：
- 智能调度可以根据电路特征自动选择最佳后端
- 无需了解每个后端的细节
- 可以优化性能和精度

**实际应用**：
- 量子算法开发
- 量子硬件测试
- 性能优化

---

## 快速上手

```python
from quonic import qgate, qshow
from quonic.gates import CX, H

# 创建电路
qgate(H, 0)
for i in range(9):
    qgate(CX, i, i + 1)

# 智能调度：自动选择最佳后端
qshow()
```

**预期输出**：

```
backend: native | shots: 1024
Result:
  |0000000000>    512  ( 50.0%)  ####################
  |1111111111>    512  ( 50.0%)  ####################
```

---

## 原理详解

### 电路图

![Smart Scheduling circuit](/images/schedule_circuit.svg)

### 数学推导

**智能调度的数学基础**

调度器根据电路特征选择最佳后端：

1. 电路规模：量子比特数、门数
2. 门类型：单比特门、多比特门
3. 噪声要求：是否需要噪声模拟
4. 性能要求：速度、精度

**决策过程**

调度器使用启发式算法或机器学习模型来选择最佳后端。

### 几何解释

智能调度的几何解释：

1. 电路特征：在特征空间中的点
2. 后端能力：在能力空间中的区域
3. 调度：找到最匹配的后端

这就像根据任务需求选择最合适的工具。

---

## 代码详解

```python
from quonic import qgate, qshow  # 导入核心 API
from quonic.gates import CX, H   # 导入门定义

# 创建电路
qgate(H, 0)  # Hadamard 门
for i in range(9):
    qgate(CX, i, i + 1)  # CNOT 链

# 智能调度：自动选择最佳后端
qshow()  # 不指定后端，自动选择
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `qshow()` | 无参数 | 智能调度，自动选择最佳后端 |
| `qshow(backend='auto')` | backend: 'auto' | 智能调度，自动选择最佳后端 |

---

## 进阶用法

### 场景 1：不同电路类型

```python
# Clifford 电路
qgate(H, 0)
qgate(CX, 0, 1)
qshow()  # 可能选择 stabilizer

# 非 Clifford 电路
qgate(H, 0)
qgate(CX, 0, 1)
qgate(Ry(0.5), 0)
qshow()  # 可能选择 statevector
```

### 场景 2：不同规模电路

```python
# 小规模电路
qgate(H, 0)
qgate(CX, 0, 1)
qshow()  # 可能选择 native

# 大规模电路
qgate(H, 0)
for i in range(19):
    qgate(CX, i, i + 1)
qshow()  # 可能选择 qiskit
```

### 场景 3：调度器调试

```python
# 查看调度器决策
from quonic.scheduler import schedule
rec = schedule(circuit)
print(f"Backend: {rec.backend}")
print(f"Method: {rec.method}")
print(f"Reason: {rec.reason}")
```

---

## 适用场景

### 场景 1：量子算法开发

智能调度可以让开发者专注于算法，无需关心后端选择。

### 场景 2：量子硬件测试

智能调度可以自动选择最适合的后端来测试量子硬件。

### 场景 3：性能优化

智能调度可以自动选择性能最佳的后端。

---

## 常见问题

### Q1: 智能调度的准确性如何？

智能调度使用启发式算法或机器学习模型，准确性取决于训练数据和算法。

### Q2: 智能调度需要多少时间？

智能调度通常在毫秒级完成，可以忽略不计。

### Q3: 智能调度可以手动覆盖吗？

可以。用户可以手动指定后端，覆盖智能调度的决策。

### Q4: 智能调度的决策依据是什么？

电路特征、后端能力、性能要求等。

### Q5: 智能调度可以学习吗？

可以。调度器可以使用机器学习模型，从历史数据中学习。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 不同量子后端
- 电路特征

### 继续学习

- 性能优化
- 量子硬件测试
- 量子算法开发

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本智能调度

```python
from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
for i in range(9):
    qgate(CX, i, i + 1)
qshow()
```

### 示例 2：调度器调试

```python
from quonic import qgate, reset
from quonic.gates import CX, H
from quonic.scheduler import schedule
from quonic.stack import current_circuit

reset()
qgate(H, 0)
for i in range(9):
    qgate(CX, i, i + 1)

rec = schedule(current_circuit())
print(f"Backend: {rec.backend}")
print(f"Method: {rec.method}")
print(f"Reason: {rec.reason}")
```

### 运行方式

```bash
python examples/schedule/schedule.py
```

---

## 下载

- [schedule.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/schedule/schedule.py)
