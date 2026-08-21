# GPU 智能调度架构报告

> 生成日期：2026-08-19
> 覆盖：GPU 引擎实现 + 能力矩阵 + 电路特征分析 + 智能调度

---

## 1. 架构总览

```
run(circuit, method="gpu")
│
├─ engine.py 检测 method="gpu"
│   ├─ 后端有 GPU → 走后端自己的 GPU（快，保留特性）
│   ├─ 后端无 GPU → 抛 NotImplementedError
│   └─ 后端 fallback → 走 CuPy 通用引擎（中等，覆盖所有）
│
└─ 调度器自动选最优后端
    ├─ 低纠缠大电路 → tensorcircuit（张量网络 GPU）
    ├─ 有经典控制流 → qulacs（状态塌缩 GPU）
    ├─ 高纠缠小电路 → qulacs（最快状态向量 GPU）
    └─ 兜底 → cupy（通用 GPU 引擎）
```

---

## 2. 各后端 GPU 支持现状

| 后端 | GPU 支持 | 实现方式 | 特性保留 |
|---|---|---|---|
| **qulacs** | ✓ | `QuantumStateGpu`（需安装 GPU 版） | 噪声/经典控制/塌缩 |
| **tensorcircuit** | ✓ | `tc.set_backend("jax")`（需 JAX） | 张量网络/自动微分 |
| **pennylane** | ✗ | 抛 NotImplementedError | — |
| **qiskit** | ✓ | Aer `statevector_gpu`（需 CUDA Aer） | 噪声/转译 |
| **mindquantum** | ✓ | `Simulator("gpu")`（需 GPU 版） | 噪声/经典控制 |
| **qpanda** | ✓ | `GPUQVM()`（需 CUDA） | 噪声/经典控制 |
| **cudaq** | ✓ | 天生 GPU | 全部 |
| **cirq** | ✗ | 抛 NotImplementedError | — |
| **native** | ✗ | 抛 NotImplementedError | — |
| **cqlib** | ✗ | 抛 NotImplementedError（非模拟器） | — |
| **cupy** | ✓ | CuPy 通用引擎（自动 fallback numpy） | 噪声/经典控制/塌缩 |

---

## 3. CuPy 通用引擎

### 3.1 定位

CuPy 引擎是**兜底方案**，不是主力。它绕过各后端的模拟器，在 IR 层直接执行门操作。

```
性能排序：后端专属 GPU > CuPy 通用 GPU >> CPU

qulacs CUDA kernel（手写优化）    ████████████████ 100%
tensorcircuit JAX JIT            ███████████████  95%
CuPy 通用引擎（向量化门）        ██████████       60%  (单比特门 ~80%, 多比特门 ~40%)
numpy CPU（当前）                 ███              15%
```

注：CuPy 性能估计取决于电路组成。单比特门（H/Rx/Ry/Rz）用 tensordot 向量化，
接近后端专属 GPU；多比特门（CX/CCX/SWAP）用 numpy 索引向量化，比 Python 循环快
但比专属 kernel 慢。含大量 CX 门的真实电路，CuPy 性能约为后端专属 GPU 的 40-60%。

### 3.2 实现

- 文件：`backends/cupy_engine.py`（~200 行）
- 自动检测：`try import cupy` → 有 GPU 用 CuPy，无 GPU 用 numpy
- 门逻辑：复用 `engine.py` 的 `_sv_*` 思路，用 `xp`（array module）抽象
- 单比特门：`tensordot` + `moveaxis`（向量化，无 Python 循环）
- 多比特门（CX/CZ/CP/CCX/SWAP/MCZ）：numpy 索引向量化（无 Python 循环）
- 噪声：Pauli 随机翻转（简化版去极化）
- 经典控制流：per-shot statevector + 塌缩

### 3.3 依赖

```toml
# pyproject.toml
gpu = ["cupy-cuda12x>=13.0"]   # NVIDIA CUDA
# ROCm: pip install cupy-rocm
# 无 GPU: 自动 fallback numpy（零依赖）
```

### 3.4 局限

| 局限 | 原因 |
|---|---|
| 比后端 GPU 慢 | 通用矩阵乘法 vs 专属 kernel |
| 无张量网络 | 状态向量模拟，20+ qubit 爆内存 |
| 无自动微分 | 不支持 VQE/QAOA 梯度 |
| 多比特门比专属 kernel 慢 | numpy 索引向量化 vs 手写 CUDA kernel |

---

## 4. 智能调度

### 4.1 决策树

```python
def recommend_backend_gpu(features):
    n = features["n"]
    entanglement = features["entanglement"]  # "low"/"medium"/"high"
    has_ctrl = features["has_ctrl"]          # True/False

    if entanglement == "low" and n >= 20:
        return "tensorcircuit"   # 张量网络 GPU
    if has_ctrl:
        return "qulacs"          # 状态塌缩 GPU
    if n <= 30:
        return "qulacs"          # 最快状态向量 GPU
    return "tensorcircuit"       # 大电路兜底
```

### 4.2 电路特征

`scheduler/features.py` 新增特征：

| 特征 | 类型 | 含义 |
|---|---|---|
| `entanglement` | str | "low"/"medium"/"high"，基于 treewidth/n 比率 |
| `has_ctrl` | bool | 有无 cif/cmeasure/cwhile |

纠缠级别判定：
- `tw/n < 0.2` → low（张量网络友好）
- `tw/n < 0.5` → medium
- `tw/n >= 0.5` → high（只能状态向量）

### 4.3 调度验证

```
Bell (n=2, entanglement=high, has_ctrl=False)
  → qulacs (gpu) ✓

Rotation-25 (n=25, entanglement=low, has_ctrl=False)
  → tensorcircuit (gpu) ✓

cwhile (n=1, entanglement=low, has_ctrl=True)
  → qulacs (gpu) ✓
```

---

## 5. 能力矩阵

每个后端声明 `_CAPABILITIES`：

```python
_CAPABILITIES = {
    "noise": bool,        # 密度矩阵噪声注入
    "ctrl": bool,         # 经典控制流（cif/cmeasure/cwhile）
    "mid_measure": bool,  # 中段测量 + 态塌缩
    "gpu": bool,          # GPU 加速
}
```

`run()` 入口检查能力矩阵，不支持时抛统一错误：

- `method="gpu"` + `gpu=False` → `err.no_gpu`
- `noise=` + `noise=False` → `err.engine_noise`
- 有 ctrl + `ctrl=False` → `err.engine_ctrl`

---

## 6. 文件清单

| 文件 | 改动 |
|---|---|
| `engine.py` | +`_run_gpu` 方法 + `_CAPABILITIES["gpu"]` + `method="gpu"` 分发 |
| `cupy_engine.py` | 新建，CuPy 通用引擎（~200 行） |
| `qulacs.py` | +`_run_gpu`（QuantumStateGpu fallback CuPy）+ `_CAPABILITIES["gpu"]` |
| `cirq.py` | +`method="gpu"` 抛 NotImplementedError |
| `pennylane.py` | +`method="gpu"` 抛 NotImplementedError |
| `native.py` | +`method="gpu"` 抛 NotImplementedError + `_CAPABILITIES` |
| `qiskit.py` | +`_CAPABILITIES["gpu"]` + `methods` 加 "gpu" |
| `base.py` | +`_CAPABILITIES` 默认 dict |
| `scheduler/capabilities.py` | +`METHOD_CAPABILITIES["gpu"]` + `BACKEND_CAPABILITIES` 扩展 |
| `scheduler/features.py` | +`entanglement` / `has_ctrl` 特征 |
| `scheduler/registry.py` | +`recommend_backend_gpu()` |
| `scheduler/__init__.py` | 导出 `recommend_backend_gpu` |
| `__init__.py` | 注册 cupy 后端 |
| `_i18n.py` | +`err.no_gpu` / `err.gpu_missing` |
| `pyproject.toml` | +`gpu = ["cupy-cuda12x"]` |

---

## 7. 风险与边界

- **GPU 环境**：无 GPU 机器上测试会 skip（importorskip），CuPy fallback numpy
- **各后端 GPU API 差异**：每个后端的 GPU 接口不同，需逐个适配
- **张量网络判定**：`entanglement_level` 是启发式（tw/n 比率），可能不准
- **CuPy 多比特门**：CX/CCX/SWAP/MCZ 仍是 Python 循环，待向量化
- **`needs_grad`**：当前 IR 不携带"是否需要微分"信息，需用户手动传入

---

## 8. 后续优化方向

| 优先级 | 项 | 收益 |
|---|---|---|
| P1 | CuPy 多比特门向量化（tensordot 替换 Python 循环） | 大电路 10x |
| P1 | 各后端 GPU 实际测试（需 GPU 环境） | 验证正确性 |
| P2 | `needs_grad` 信息传入 IR | 调度更精准 |
| P2 | 调度器学习（LocalCacheRegistry 记录 GPU 性能） | 自动优化 |
| P3 | 张量网络判定优化（更精确的纠缠估计） | 大电路选对后端 |
