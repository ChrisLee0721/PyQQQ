# BB84 QKD / BB84 量子密钥分发

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

BB84 是第一个量子密钥分发协议，使用量子力学原理实现安全的密钥分发。

**经典局限**：
- 经典密钥分发：依赖可信信道或公钥密码
- 公钥密码：可能被量子计算机破解

**量子优势**：
- 基于量子力学原理（不可克隆定理）
- 窃听可检测：任何窃听都会引入错误
- 信息论安全：不依赖计算复杂度

**实际应用**：
- 安全通信（政府、军事、金融）
- 量子密钥分发网络
- 后量子密码学

---

## 快速上手

```python
import random
from quonic import qgate, reset
from quonic.backends import get_backend
from quonic.gates import H, X
from quonic.stack import current_circuit

def bb84_round(alice_basis, alice_bit, bob_basis):
    reset()
    if alice_bit == 1:
        qgate(X, 0)
    if alice_basis == 1:
        qgate(H, 0)
    if bob_basis == 1:
        qgate(H, 0)
    result = get_backend("native").run(current_circuit(), shots=1)
    return int(list(result.counts.keys())[0])

# 运行 20 轮
n_rounds = 20
alice_bases = [random.randint(0, 1) for _ in range(n_rounds)]
alice_bits = [random.randint(0, 1) for _ in range(n_rounds)]
bob_bases = [random.randint(0, 1) for _ in range(n_rounds)]

bob_results = [bb84_round(alice_bases[i], alice_bits[i], bob_bases[i])
               for i in range(n_rounds)]

# 筛选：只保留基匹配的
key = [alice_bits[i] for i in range(n_rounds)
       if alice_bases[i] == bob_bases[i]]

print(f"Key: {key}")
```

**预期输出**：

```
Key: [1, 0, 1, 1, 0, 1, 0, 0, 1, 1]
```

---

## 原理详解

### 电路图

![BB84 QKD circuit](/images/bb84_circuit.svg)

### 数学推导

**Step 1: Alice 准备**

Alice 随机选择基（Z 或 X）和比特（0 或 1）。
- Z 基：|0⟩ 或 |1⟩
- X 基：|+⟩ 或 |-⟩

**Step 2: Alice 发送**

Alice 通过量子信道发送量子比特。

**Step 3: Bob 测量**

Bob 随机选择基（Z 或 X）测量。

**Step 4: 基协商**

Alice 和 Bob 公开比较基（不比较结果）。
保留基匹配的轮次。

**Step 5: 窃听检测**

比较部分结果，检查错误率。
如果错误率 > 阈值，说明有窃听。

**Step 6: 密钥生成**

剩余的比特作为密钥。

### 几何解释

BB84 的几何解释：

1. Z 基：|0⟩ 和 |1⟩ 在 z 轴上
2. X 基：|+⟩ 和 |-⟩ 在 x 轴上
3. 窃听者不知道基，测量会引入错误
4. 通过检查错误率检测窃听

这就像用两个不同的坐标系编码信息。

---

## 代码详解

```python
import random
from quonic import qgate, reset
from quonic.backends import get_backend
from quonic.gates import H, X
from quonic.stack import current_circuit

def bb84_round(alice_basis, alice_bit, bob_basis):
    reset()  # 重置电路

    # Alice 准备
    if alice_bit == 1:
        qgate(X, 0)  # 编码比特
    if alice_basis == 1:
        qgate(H, 0)  # 切换到 X 基

    # Bob 测量
    if bob_basis == 1:
        qgate(H, 0)  # 切换到 X 基

    # 测量
    result = get_backend("native").run(current_circuit(), shots=1)
    return int(list(result.counts.keys())[0])

# 运行 20 轮
n_rounds = 20
alice_bases = [random.randint(0, 1) for _ in range(n_rounds)]
alice_bits = [random.randint(0, 1) for _ in range(n_rounds)]
bob_bases = [random.randint(0, 1) for _ in range(n_rounds)]

# 执行协议
bob_results = [bb84_round(alice_bases[i], alice_bits[i], bob_bases[i])
               for i in range(n_rounds)]

# 筛选：只保留基匹配的
key = [alice_bits[i] for i in range(n_rounds)
       if alice_bases[i] == bob_bases[i]]

print(f"Key: {key}")
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
| `qgate(X, 0)` | X: Pauli-X 门, 0: 量子比特索引 | 编码比特 |
| `qgate(H, 0)` | H: Hadamard 门, 0: 量子比特索引 | 切换基 |
| `get_backend("native").run(circuit, shots=1)` | backend: 后端, circuit: 电路, shots: 测量次数 | 执行测量 |

---

## 进阶用法

### 场景 1：不同轮数

```python
# 100 轮
n_rounds = 100
# ... 执行协议 ...
print(f"Key length: {len(key)}")
```

### 场景 2：窃听检测

```python
# 模拟窃听者
def bb84_with_eavesdropper(alice_basis, alice_bit, bob_basis):
    reset()
    if alice_bit == 1:
        qgate(X, 0)
    if alice_basis == 1:
        qgate(H, 0)
    # 窃听者测量
    qgate(H, 0)  # Eve 用 X 基测量
    qgate(H, 0)  # Eve 用 X 基发送
    if bob_basis == 1:
        qgate(H, 0)
    result = get_backend("native").run(current_circuit(), shots=1)
    return int(list(result.counts.keys())[0])
```

### 场景 3：错误率计算

```python
# 计算错误率
errors = sum(1 for i in range(n_rounds)
             if alice_bases[i] == bob_bases[i]
             and alice_bits[i] != bob_results[i])
error_rate = errors / len(key)
print(f"Error rate: {error_rate:.2%}")
```

---

## 适用场景

### 场景 1：安全通信

BB84 用于政府、军事、金融等领域的安全通信。

### 场景 2：量子密钥分发网络

BB84 可以用于构建量子密钥分发网络，实现城域或广域的安全通信。

### 场景 3：后量子密码学

BB84 不依赖计算复杂度，是后量子密码学的重要组成部分。

---

## 常见问题

### Q1: BB84 的安全性基于什么？

基于量子力学原理：不可克隆定理和测量扰动。任何窃听都会引入错误。

### Q2: BB84 的密钥生成率如何？

约 50% 的轮次基匹配，其中约 75% 的比特正确。所以密钥生成率约 37.5%。

### Q3: BB84 能抵抗量子计算机攻击吗？

能。BB84 的安全性基于物理原理，不依赖计算复杂度。

### Q4: BB84 的传输距离有限制吗？

有。光纤传输距离约 100-200 km，需要量子中继来扩展距离。

### Q5: BB84 和 E91 有什么区别？

BB84 使用单光子，E91 使用纠缠对。E91 的安全性基于 Bell 不等式。

---

## 学习路径

### 前置知识

- 量子比特和量子测量
- Hadamard 门和 Pauli-X 门
- 量子密钥分发的基本概念

### 继续学习

- E91 协议（基于纠缠的 QKD）
- 量子密钥分发网络
- 后量子密码学

### 难度等级

- 当前：中级
- 下一步：高级

---

## 完整示例代码

### 示例 1：基本 BB84

```python
import random
from quonic import qgate, reset
from quonic.backends import get_backend
from quonic.gates import H, X
from quonic.stack import current_circuit

def bb84_round(alice_basis, alice_bit, bob_basis):
    reset()
    if alice_bit == 1:
        qgate(X, 0)
    if alice_basis == 1:
        qgate(H, 0)
    if bob_basis == 1:
        qgate(H, 0)
    result = get_backend("native").run(current_circuit(), shots=1)
    return int(list(result.counts.keys())[0])

n_rounds = 20
alice_bases = [random.randint(0, 1) for _ in range(n_rounds)]
alice_bits = [random.randint(0, 1) for _ in range(n_rounds)]
bob_bases = [random.randint(0, 1) for _ in range(n_rounds)]
bob_results = [bb84_round(alice_bases[i], alice_bits[i], bob_bases[i])
               for i in range(n_rounds)]
key = [alice_bits[i] for i in range(n_rounds)
       if alice_bases[i] == bob_bases[i]]
print(f"Key: {key}")
```

### 示例 2：带窃听检测的 BB84

```python
import random
from quonic import qgate, reset
from quonic.backends import get_backend
from quonic.gates import H, X
from quonic.stack import current_circuit

def bb84_with_eavesdropper(alice_basis, alice_bit, bob_basis):
    reset()
    if alice_bit == 1:
        qgate(X, 0)
    if alice_basis == 1:
        qgate(H, 0)
    # 窃听者
    qgate(H, 0)
    qgate(H, 0)
    if bob_basis == 1:
        qgate(H, 0)
    result = get_backend("native").run(current_circuit(), shots=1)
    return int(list(result.counts.keys())[0])

n_rounds = 100
alice_bases = [random.randint(0, 1) for _ in range(n_rounds)]
alice_bits = [random.randint(0, 1) for _ in range(n_rounds)]
bob_bases = [random.randint(0, 1) for _ in range(n_rounds)]
bob_results = [bb84_with_eavesdropper(alice_bases[i], alice_bits[i], bob_bases[i])
               for i in range(n_rounds)]
key = [alice_bits[i] for i in range(n_rounds)
       if alice_bases[i] == bob_bases[i]]
errors = sum(1 for i in range(n_rounds)
             if alice_bases[i] == bob_bases[i]
             and alice_bits[i] != bob_results[i])
error_rate = errors / len(key) if key else 0
print(f"Key: {key}")
print(f"Error rate: {error_rate:.2%}")
```

### 运行方式

```bash
python examples/bb84/bb84.py
```

---

## 下载

- [bb84.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/bb84/bb84.py)
