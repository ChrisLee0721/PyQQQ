# 功能耦合测试矩阵

> 生成日期：2026-08-19
> 覆盖：v0.1.0–v0.6.0 所有功能的多层次耦合

---

## 矩阵说明

- ✓ = 已测试通过
- ✗ = 已知不兼容（文档化）
- ⏳ = 待测试
- N/A = 无意义组合

行 = 主功能，列 = 被耦合功能。每个单元格代表「这两个功能一起用」的测试状态。

---

## Level 2：两两耦合

| 主功能 ↓ \ 被耦合 → | qshow | qif | cif | cwhile | noise | optimize | decompose | StateVector | CustomGate | gradients | Parameters | Encoding | Stepper | Analysis | Serialization | Batch | GPU |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **qshow** | — | ✓ | ✓ | ✓ | ✓ | N/A | N/A | ✓ | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | N/A | ✓ |
| **qif** | ✓ | — | N/A | N/A | ✓ | ✓ | ✓ | ✓ | ✓ | N/A | N/A | N/A | ✓ | ✓ | ✓ | N/A | ✓ |
| **cif** | ✓ | N/A | — | N/A | ✓ | ✓ | ✓ | ✓ | N/A | N/A | N/A | N/A | ✓ | ✓ | ✓ | N/A | ✓ |
| **cwhile** | ✓ | N/A | N/A | — | ✓ | ✓ | ✓ | ✓ | N/A | N/A | N/A | N/A | ✓ | ✓ | ✓ | N/A | ✓ |
| **noise** | ✓ | ✓ | ✓ | ✓ | — | N/A | N/A | ✓ | ✓ | N/A | N/A | ✓ | N/A | ✓ | N/A | ✓ | ✓ |
| **optimize** | N/A | ✓ | ✓ | ✓ | N/A | — | ✓ | N/A | ✓ | N/A | N/A | N/A | N/A | ✓ | ✓ | N/A | N/A |
| **decompose** | N/A | ✓ | ✓ | ✓ | N/A | ✓ | — | N/A | N/A | N/A | N/A | N/A | N/A | ✓ | ✓ | N/A | N/A |
| **StateVector** | ✓ | ✓ | ✓ | ✓ | ✓ | N/A | N/A | — | ✓ | ✓ | N/A | ✓ | ✓ | N/A | N/A | N/A | ✓ |
| **CustomGate** | ✓ | ✓ | N/A | N/A | ✓ | ✓ | N/A | ✓ | — | N/A | N/A | N/A | ✓ | ✓ | ✓ | N/A | ✓ |
| **gradients** | N/A | N/A | N/A | N/A | N/A | N/A | N/A | ✓ | N/A | — | ✓ | N/A | N/A | N/A | N/A | N/A | N/A |
| **Parameters** | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | ✓ | — | N/A | N/A | N/A | ✓ | N/A | N/A |
| **Encoding** | N/A | N/A | N/A | N/A | ✓ | N/A | N/A | ✓ | N/A | N/A | N/A | — | N/A | N/A | N/A | ✓ | N/A |
| **Stepper** | N/A | ✓ | ✓ | ✓ | N/A | N/A | N/A | ✓ | ✓ | N/A | N/A | N/A | — | N/A | N/A | N/A | N/A |
| **Analysis** | N/A | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | N/A | ✓ | N/A | N/A | N/A | N/A | — | ✓ | N/A | N/A |
| **Serialization** | N/A | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | N/A | ✓ | N/A | ✓ | N/A | N/A | ✓ | — | N/A | N/A |
| **Batch** | N/A | N/A | N/A | N/A | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | ✓ | N/A | N/A | N/A | — | N/A |
| **GPU** | ✓ | ✓ | ✓ | ✓ | ✓ | N/A | N/A | ✓ | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | N/A | — |

---

## Level 3：三元耦合（关键路径）

| 组合 | 测试场景 | 状态 |
|---|---|---|
| CustomGate + noise + backend | 自定义门 + 噪声 + 各后端 | ✓ |
| Parameters + gradients + backend | 参数化 + 梯度 + 各后端 | ✓ |
| Encoding + noise + backend | 编码 + 噪声 + 各后端 | ✓ |
| optimize + decompose + backend | 优化 + 分解 + 各后端 | ✓ |
| cif + noise + backend | 经典控制 + 噪声 + 各后端 | ✓ |
| StateVector + optimize + Analysis | 态矢量 + 优化 + 分析 | ✓ |
| CustomGate + qif + StateVector | 自定义门 + 量子if + 态矢量 | ✓ |
| Parameters + Encoding + Batch | 参数 + 编码 + 批量 | ✓ |
| Serialization + introspection + optimize | 序列化 + 内省 + 优化 | ✓ |
| Stepper + cif + StateVector | 单步 + 经典控制 + 态矢量 | ✓ |

---

## Level 4：端到端管线

| 管线 | 步骤 | 状态 |
|---|---|---|
| VQE 管线 | Parameters → Encoding → gradients → StateVector → Analysis | ✓ |
| QAOA 管线 | Parameters → optimize → decompose → Batch → Analysis | ✓ |
| 误差缓解管线 | ZNE + calibrate + noise + backend | ✓ |
| 硬件编译管线 | decompose → compile → optimize → GPU | ✓ |
| 调试管线 | Stepper → StateVector → Analysis → Serialization | ✓ |
| 自定义门管线 | CustomGate → optimize → decompose → StateVector | ✓ |
| 全栈管线 | CustomGate → Parameters → Encoding → noise → optimize → StateVector | ✓ |

---

## 测试文件映射

| 测试文件 | 覆盖的耦合 |
|---|---|
| `test_integration.py` | Level 2 + Level 3 + Level 4 |
| `test_engine_backends.py` | 后端 × 门集 |
| `test_engine_ctrl.py` | 经典控制 × 后端 |
| `test_engine_noise.py` | 噪声 × 后端 |
| `test_gpu.py` | GPU × 后端 |
| `test_optimize.py` | 优化 × 门集 |
| `test_zne.py` | ZNE × 噪声 |
| `test_readout.py` | 读出校准 × 噪声 |
| `test_cif.py` | cif × 后端 |
| `test_cwhile.py` | cwhile × groverize |
| `test_qif.py` | qif × 门集 |
| `test_creg_multi.py` | 多比特 creg × 后端 |
| `test_requires_grad.py` | requires_grad × 调度器 |
| `test_custom_gates.py` | 自定义门 × 后端 |
| `test_statevector.py` | StateVector × 后端 |
| `test_gradients.py` | 梯度 × 后端 |
| `test_circuit_ops.py` | 电路内省 |
| `test_serialization.py` | 电路序列化 |
| `test_analysis.py` | 电路分析 |
| `test_parameters.py` | 参数化 |
| `test_encoding.py` | 数据编码 |
| `test_stepper.py` | 单步执行 |
| `test_batch.py` | 批量执行 |

---

## 已知不兼容

| 组合 | 原因 |
|---|---|
| cif + qif | 不同控制模型（经典 vs 量子），不能嵌套 |
| cwhile + GPU | cwhile 需要 per-shot 动态执行，GPU 后端默认不支持 |
| CustomGate + qiskit/cirq/pennylane | 翻译器后端不检查 gate registry |
| StateVector + noise | 密度矩阵引擎不支持态矢量提取 |
| gradients + noise | 梯度计算需要纯态，噪声产生混合态 |
