# 知乎文章文案

---

## 文章 1：QuoNic — 量子编程，像写 Python 一样简单

### 标题
QuoNic：让量子编程像写 Python 一样简单 | 12+ 后端统一抽象层

### 正文

**你有没有想过，写量子程序可以像写 Python 一样简单？**

```python
from quonic import qgate, qshow
from quonic.gates import H, CX

qgate(H, 0)
qgate(CX, 0, 1)
qshow()
```

这就是 QuoNic —— 3 行代码，跑通量子计算最经典的贝尔态。同样的功能，用 Qiskit 需要 10+ 行。

**QuoNic 不是另一个量子编程框架。** 它是量子计算的抽象层——像 Docker 抽象容器运行时、JDBC 抽象数据库驱动一样，QuoNic 抽象量子后端。

**核心特性：**

1. **极简语法**：不需要学 `QuantumCircuit`，不需要理解 `backend`，不需要手动 `measure`
2. **12+ 后端统一**：Qiskit、Cirq、PennyLane、Qulacs、TensorCircuit、CUDA-Q、MindQuantum、QPanda3……同一个 API，切换只需一个参数
3. **智能调度**：根据电路特征自动选最优后端（CPU/GPU/张量网络/稳定子）
4. **误差缓解**：ZNE 零噪声外推 + 读出校准，真实硬件验证过
5. **量子控制流**：`qif`（量子叠加控制）、`cif`（经典控制）、`cwhile`（重复直到成功）
6. **77 个算法模板**：从 Grover 到 VQE 到 QAOA 到量子纠错

**为什么需要 QuoNic？**

量子计算最大的问题不是算法，而是碎片化。Qiskit、Cirq、PennyLane、Qulacs……每个框架都有自己的 API、自己的后端、自己的噪声模型。用户一旦选定框架，就被锁死了。

QuoNic 解决这个问题：**写一次代码，跑任何后端。** 同一段代码，不加修改，可以在 Qiskit、Cirq、Qulacs 上运行。QuoNic 自动处理后端差异。

**快速开始：**

```bash
pip install quonic
```

```python
from quonic import qgate, qshow
from quonic.gates import H, CX

# 贝尔态
qgate(H, 0)
qgate(CX, 0, 1)
qshow()  # 自动选最优后端

# 切换后端
qshow(backend='qulacs')  # Qulacs C++ 高性能
qshow(backend='qiskit')  # IBM Qiskit
qshow(backend='cirq')    # Google Cirq

# GPU 加速
qshow(method='gpu')  # 自动选最优 GPU 后端

# 误差缓解
from quonic import zne
result = zne(circuit, noise=0.05, target="1", shots=1024)
print(f"ZNE 外推: {result.extrapolated:.3f}")
```

**QuoNic vs Qiskit：**

| 场景 | Qiskit | QuoNic |
|------|--------|--------|
| 跑通第一个量子程序 | 需要理解 5-8 个新概念 | 只需要 2 个：`qgate` 和 `qshow` |
| 代码行数（贝尔态） | 8-12 行 | 3 行 |
| 切换后端 | 重写全部代码 | 改一个参数 |
| GPU 加速 | 需要配置 | 一个参数 |
| 误差缓解 | 需要自己实现 | 内置 ZNE + 读出校准 |

**QuoNic 是开源的：** https://github.com/ChrisLee0721/QuoNic

欢迎 star、fork、提 issue！

---

## 文章 2：QuoNic GPU 智能调度

### 标题
QuoNic GPU 智能调度：让你的量子模拟自动选最快的后端

### 正文

**你有没有遇到过这种情况：写了一个量子电路，不知道该用哪个后端跑最快？**

Qiskit 有 Aer，Cirq 有 Simulator，Qulacs 有 C++ 引擎，TensorCircuit 有 JAX……每个后端都有自己的 GPU 版本。选错了，可能慢 10 倍。

QuoNic 解决这个问题：**智能调度。**

```python
from quonic import qshow
qshow(method='gpu')  # 自动选最优 GPU 后端
```

就这么简单。QuoNic 根据电路特征（纠缠深度、比特数、是否需要经典控制）自动选最优后端。

**调度逻辑：**

| 电路特征 | 选哪个后端 | 原因 |
|----------|-----------|------|
| 高纠缠、小电路 | Qulacs | 最快状态向量 GPU |
| 低纠缠、大电路 | TensorCircuit | 张量网络 GPU |
| 有经典控制流 | Qulacs | 支持状态塌缩 |
| 兜底 | CuPy | 通用 GPU 引擎 |

**实测数据（RTX 2070）：**

| 电路 | CPU (native) | GPU (CuPy) | 加速比 |
|------|-------------|------------|--------|
| GHZ-8 | 0.015s | 0.007s | 2x |
| GHZ-16 | 0.12s | 0.02s | 6x |
| GHZ-20 | 0.53s | 0.05s | 10x |

**如何使用：**

```python
from quonic import qshow
from quonic.scheduler import recommend_backend_gpu, circuit_features

# 方式 1：自动调度
qshow(method='gpu')

# 方式 2：查看调度建议
feats = circuit_features(circuit)
rec = recommend_backend_gpu(feats)
print(f"推荐后端: {rec.backend}")

# 方式 3：手动指定
qshow(backend='qulacs', method='gpu')
```

**QuoNic GPU 智能调度的护城河：**

1. **统一入口**：不管用哪个后端，`method='gpu'` 就行
2. **自动降级**：没有 GPU？自动 fallback 到 CPU
3. **学习型**：运行历史会被记录，下次自动选更快的后端
4. **覆盖广**：12 个后端，7 个有 GPU 支持

**安装：**

```bash
pip install 'quonic[gpu]'      # CuPy 通用 GPU
pip install 'quonic[qulacs]'   # Qulacs 原生 GPU
```

**QuoNic 是开源的：** https://github.com/ChrisLee0721/QuoNic
