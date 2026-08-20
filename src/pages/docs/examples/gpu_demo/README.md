# GPU 加速演示

展示 QuoNic 的 GPU 加速功能，包括直接 GPU 执行、智能调度和 CuPy 兜底引擎。

## 功能

1. **直接 GPU 执行** — 通过 `method="gpu"` 直接在 GPU 上运行电路
2. **智能调度** — 通过 `recommend_backend_gpu()` 自动选择最优 GPU 后端
3. **CuPy 兜底** — 当原生 GPU 不可用时，自动 fallback 到 CuPy 通用引擎
4. **错误处理** — 不支持 GPU 的后端会抛出清晰的错误信息

## 运行

```bash
python examples/gpu_demo/gpu_demo.py
```

## 智能调度逻辑

| 电路特征 | 选择的后端 | 原因 |
|---|---|---|
| 高纠缠、小电路 | qulacs | 最快状态向量 GPU |
| 低纠缠、大电路 | tensorcircuit | 张量网络 GPU |
| 有经典控制流 | qulacs | 支持状态塌缩 |
| 兜底 | cupy | 通用 GPU 引擎 |

## 依赖

- **qulacs GPU**：需要安装 GPU 版 qulacs（`pip install qulacs-gpu`）
- **tensorcircuit GPU**：需要安装 JAX（`pip install jax jaxlib`）
- **CuPy**：需要安装 CuPy（`pip install cupy-cuda12x`）
- **无 GPU**：CuPy 会自动 fallback 到 numpy（CPU）

## 示例输出

```
QuoNic GPU Acceleration Demo

============================================================
1. Direct GPU execution
============================================================
  qulacs       GPU: {'11': 521, '00': 503}  (0.106s)
  cupy         GPU: {'11': 525, '00': 499}  (0.001s)
  qulacs       CPU: {'00': 513, '11': 511}  (0.001s)

============================================================
2. Smart scheduling
============================================================
  GHZ-3 (n=3, entanglement=high):
    → qulacs (gpu)
  Rotation-25 (n=25, entanglement=low):
    → tensorcircuit (gpu)
  Grover (n=2, has_ctrl=False):
    → qulacs (gpu)

============================================================
3. CuPy fallback
============================================================
  qulacs GPU: {'00000': 524, '11111': 500}  (0.002s)
  cupy GPU:   {'00000': 469, '11111': 555}  (0.002s)
  native CPU: {'11111': 498, '00000': 526}  (0.001s)

============================================================
4. Error handling
============================================================
  cirq: correctly rejected — cirq backend does not support GPU acceleration
  native: correctly rejected — native backend does not support GPU acceleration
```
