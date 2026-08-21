# E91 QKD / E91 量子密钥分发

> **Communication** / 通信 | 难度：中级 | 预计时间：10 分钟

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

E91 是基于纠缠的量子密钥分发协议。

**经典局限**：
- 经典密钥分发：依赖可信信道
- 量子密钥分发：基于物理原理

**量子优势**：
- 基于纠缠和 Bell 不等式
- 窃听可检测
- 信息论安全

**实际应用**：
- 安全通信
- 量子密钥分发网络
- 后量子密码学

---

## 快速上手

```python
from quonic.algorithms import e91

# E91 协议
result = e91(shots=1024)
print(result.counts)
```

**预期输出**：

```
{'00': 256, '01': 256, '10': 256, '11': 256}
```

---

## 原理详解

### 电路图

![E91 QKD circuit](/images/e91_circuit.svg)

### 数学推导

**E91 协议**

目标：使用纠缠实现安全的密钥分发。

**算法步骤**：
1. 创建 Bell 对
2. Alice 和 Bob 各自测量
3. 比较基
4. 检测窃听
5. 生成密钥

**数学推导**：
|ψ⟩ = (|00⟩+|11⟩)/√2
Alice 测量：得到 0 或 1
Bob 测量：得到 0 或 1
比较基：保留匹配的

### 几何解释

E91 的几何解释：

1. Bell 对：纠缠态
2. 测量：在 Bloch 球上投影
3. 窃听检测：Bell 不等式

这就像用纠缠来检测窃听。

---

## 代码详解

```python
from quonic.algorithms import e91  # 导入算法

# e91(shots)
# shots: 测量次数
result = e91(shots=1024)

# result.counts: 测量结果
print(result.counts)
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `e91(shots)` | shots: 测量次数 | 执行 E91 协议 |
| `result.counts` | 无参数 | 测量结果 |

---

## 进阶用法

### 场景 1：不同测量次数

```python
# 不同测量次数
result = e91(shots=1024)
print(result.counts)

result = e91(shots=4096)
print(result.counts)
```

### 场景 2：E91 用于安全通信

```python
# E91 可以用于安全通信
# 生成密钥
```

### 场景 3：E91 用于量子网络

```python
# E91 可以用于量子网络
# 分发纠缠
```

---

## 适用场景

### 场景 1：安全通信

E91 可以用于安全通信，生成密钥。

### 场景 2：量子密钥分发网络

E91 可以用于量子密钥分发网络。

### 场景 3：后量子密码学

E91 可以用于后量子密码学。

---

## 常见问题

### Q1: E91 和 BB84 有什么区别？

E91 使用纠缠，BB84 使用单光子。

### Q2: E91 需要多少量子比特？

需要 2 个量子比特：Alice 和 Bob 各一个。

### Q3: E91 的安全性基于什么？

基于 Bell 不等式。

### Q4: E91 在 NISQ 设备上能跑吗？

可以跑小规模的，但噪声会影响结果。

### Q5: E91 的密钥生成率如何？

约 50% 的轮次基匹配。

---

## 学习路径

### 前置知识

- 量子比特和量子门
- Bell 态
- 量子密钥分发基础

### 继续学习

- BB84
- 量子密钥分发网络
- 后量子密码学

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本 E91

```python
from quonic.algorithms import e91

result = e91(shots=1024)
print(result.counts)
```

### 示例 2：不同测量次数

```python
from quonic.algorithms import e91

result = e91(shots=1024)
print(result.counts)

result = e91(shots=4096)
print(result.counts)
```

### 运行方式

```bash
python examples/e91/e91.py
```

---

## 下载

- [e91.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/e91/e91.py)
