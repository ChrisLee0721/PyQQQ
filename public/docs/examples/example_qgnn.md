# Quantum GNN / 量子图神经网络

> **ML** / 量子机器学习 | 难度：高级 | 预计时间：15 分钟

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

量子 GNN 用于图数据。

**经典局限**：
- 经典 GNN：经典计算
- 量子 GNN：量子计算

**量子优势**：
- 可以处理高维数据
- 是量子机器学习的基础

**实际应用**：
- 图分类
- 节点分类
- 量子机器学习

---

## 快速上手

```python
from quonic.algorithms import quantum_gnn

# 量子 GNN
result = quantum_gnn(graph, shots=1024)
print(result.counts)
```

**预期输出**：

```
{'00': 512, '11': 512}
```

---

## 原理详解

### 电路图

![Quantum GNN circuit](/images/qgnn_circuit.svg)

### 数学推导

**量子 GNN 算法**

目标：处理图数据。

**算法步骤**：
1. 初始化：图编码
2. 消息传递：聚合邻居信息
3. 更新：更新节点特征
4. 输出：得到输出

**数学推导**：
h_v^{(k+1)} = UPDATE(h_v^{(k)}, AGGREGATE({h_u^{(k)} : u ∈ N(v)}))
使用量子态表示节点特征

### 几何解释

量子 GNN 的几何解释：

1. 图：节点和边
2. 消息传递：聚合邻居信息
3. 更新：更新节点特征

这就像在图上传播信息。

---

## 代码详解

```python
from quonic.algorithms import quantum_gnn  # 导入算法

# quantum_gnn(graph, shots)
# graph: 图
# shots: 测量次数
result = quantum_gnn(graph, shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `quantum_gnn(graph, shots)` | graph: 图, shots: 测量次数 | 执行量子 GNN |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同图

```python
# 不同图
result = quantum_gnn(graph1, shots=1024)
print(result.counts)

result = quantum_gnn(graph2, shots=1024)
print(result.counts)
```

### 场景 2：量子 GNN 用于图分类

```python
# 量子 GNN 可以用于图分类
# 分类图
```

### 场景 3：量子 GNN 用于节点分类

```python
# 量子 GNN 可以用于节点分类
# 分类节点
```

---

## 适用场景

### 场景 1：图分类

量子 GNN 可以用于图分类。

### 场景 2：节点分类

量子 GNN 可以用于节点分类。

### 场景 3：量子机器学习

量子 GNN 是量子机器学习的基础。

---

## 常见问题

### Q1: 量子 GNN 的精度如何？

精度取决于图大小和模型复杂度。

### Q2: 量子 GNN 需要多少量子比特？

取决于图大小。

### Q3: 量子 GNN 和经典 GNN 有什么区别？

量子 GNN 可以处理高维数据。

### Q4: 量子 GNN 在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: 量子 GNN 的复杂度如何？

复杂度取决于图大小和模型复杂度。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- 量子机器学习
- 图神经网络

### 继续学习

- 量子机器学习
- 图分类
- 节点分类

### 难度等级

- 当前：高级
- 下一步：专家

---

## 完整示例代码

### 示例 1：基本量子 GNN

```python
from quonic.algorithms import quantum_gnn

result = quantum_gnn(graph, shots=1024)
print(result.counts)
```

### 示例 2：不同图

```python
from quonic.algorithms import quantum_gnn

result = quantum_gnn(graph1, shots=1024)
print(result.counts)

result = quantum_gnn(graph2, shots=1024)
print(result.counts)
```

### 运行方式

```bash
python examples/qgnn/qgnn.py
```

---

## 下载

- [qgnn.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/qgnn/qgnn.py)
