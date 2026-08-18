# Changelog

本项目所有重要变更都记录于此。All notable changes to this project are documented here.

## [0.5.0] — 2026-08-19

GPU 智能调度 + 7 个新后端 + 误差缓解增强 + 大量 bug 修复。GPU smart scheduling,
7 new backends, error mitigation enhancements, and numerous bug fixes.

### 新增 Added

- **GPU 智能调度** `method="gpu"` + `recommend_backend_gpu()`：根据电路特征（纠缠级别 /
  经典控制流 / 电路大小）自动选择最优 GPU 后端。CuPy 通用引擎作为兜底。
  **GPU smart scheduling** `method="gpu"` + `recommend_backend_gpu()`: automatically selects
  the best GPU backend based on circuit features (entanglement / classical control / size).
  CuPy universal engine as fallback.

- **CuPy 通用引擎** `backends/cupy_engine.py`：基于 CuPy（numpy GPU drop-in）的状态向量
  模拟器，支持噪声注入和经典控制流，自动检测 CUDA/ROCm，无 GPU 时 fallback numpy。
  **CuPy universal engine**: CuPy-based statevector simulator with noise and classical control
  flow support, auto-detects CUDA/ROCm, falls back to numpy when no GPU.

- **7 个后端 GPU 变体**：qulacs / tensorcircuit / pennylane / qiskit / mindquantum / qpanda /
  cudaq 各自接入原生 GPU（QuantumStateGpu / JAX / lightning.gpu / Aer GPU 等）。
  **7 backend GPU variants**: each backend connects to its native GPU implementation.

- **能力矩阵** `_CAPABILITIES`：每个后端声明支持的特性（noise / ctrl / mid_measure / gpu），
  `run()` 入口检查，不支持时抛统一错误。
  **Capability matrix**: each backend declares supported features, `run()` checks at entry.

- **电路特征扩展** `scheduler/features.py`：新增 `entanglement`（纠缠级别）和 `has_ctrl`
  （经典控制流）特征，用于 GPU 调度决策。
  **Circuit features**: new `entanglement` and `has_ctrl` features for GPU scheduling.

- **cirq / pennylane 多比特 creg**：`cmeasure` 支持 `bit > 0`，`cif` 支持 `CRegCondition`
  （多比特寄存器相等判据）。
  **cirq / pennylane multi-bit creg**: `cmeasure` supports `bit > 0`, `cif` supports
  `CRegCondition` (multi-bit register equality).

- **新 example**：`gpu_demo/`（GPU 加速演示）、`error_mitigation/`（误差缓解演示）。
  **New examples**: `gpu_demo/` (GPU acceleration), `error_mitigation/` (ZNE + readout calibration).

- **新测试**：`test_gpu.py`（GPU 分发 / CuPy 引擎 / 能力矩阵 / 智能调度）。
  **New tests**: GPU dispatch, CuPy engine, capability matrix, smart scheduling.

### 变更 Changed

- **TensorCircuit numpy patch 隔离**：`_tc_compat()` 上下文管理器，patch 入口 restore 出口，
  不再全局污染 numpy。
  **TensorCircuit numpy patch isolation**: context manager patches on entry, restores on exit.

- **向量化 `_apply_readout_noise`**：从逐 shot Python 循环改为 numpy tensordot 张量收缩。
  **Vectorized readout noise**: numpy tensordot instead of per-shot Python loop.

- **CuPy 多比特门向量化**：CX / CCX / CZ / CP / SWAP / MCZ 全部用 numpy 索引替代
  Python 循环。
  **CuPy multi-qubit gate vectorization**: all gates use numpy indexing instead of Python loops.

- **`_i18n.py`**：新增 `err.no_gpu` / `err.gpu_missing` / `err.gpu_fallback_failed` 错误消息。
  **i18n**: new GPU error messages.

- **`pyproject.toml`**：新增 `gpu = ["cupy-cuda12x"]` 可选依赖。
  **pyproject.toml**: new `gpu` optional dependency.

### 修复 Fixed

- **ZNE success metric 外推被忽略**：`zne.py` success metric 路径硬编码线性外推，现改为
  使用 `extrapolation` 参数 + 成功概率 clamp 到 [0,1]。
  **ZNE success metric extrapolation ignored**: now uses the `extrapolation` parameter
  and clamps success probability to [0,1].

- **读出校准混淆矩阵奇异**：`readout.py` 捕获 `LinAlgError`，fallback Tikhonov 正则化。
  **Readout calibration singular matrix**: falls back to Tikhonov regularization.

- **读出校准无比特数校验**：`apply()` 加 n>20 时显存用量 warning。
  **Readout calibration no qubit limit**: `apply()` warns when n>20.

- **qshow_all 多进程 + CUDA**：加 warning（CUDA context 不可跨进程继承）。
  **qshow_all multiprocessing + CUDA**: added warning about CUDA context.

- **GPU 显存预检查**：CuPy 引擎在分配前检查可用显存，不足时抛 MemoryError。
  **GPU memory pre-check**: CuPy engine checks available memory before allocation.

- **CuPy fallback 错误信息**：捕获 CuPy 异常，重新抛出带原始后端名的错误。
  **CuPy fallback error messages**: re-raises with original backend name.

引擎后端全面升级、77 个算法模板、并行执行支持。Major release: engine backend upgrades,
77 algorithm templates, and parallel execution support.

### 新增 Added

- **6 个引擎后端升级为完整后端**：Qulacs / TensorCircuit / CUDA-Q / MindQuantum / QPanda3 / Cqlib 现支持密度矩阵模拟、噪声注入（退极化通道）、经典控制流（cif/cmeasure/cwhile 逐 shot 动态执行）。
  **6 engine backends upgraded to full-featured**: Qulacs / TensorCircuit / CUDA-Q / MindQuantum / QPanda3 / Cqlib now support density matrix simulation, noise injection (depolarizing channels), and classical control flow (cif/cmeasure/cwhile via per-shot dynamic execution).

- **EngineBackend v2 架构**：`run()` 三路分发（clean SV / noisy DM / dynamic per-shot），新增可选钩子 `_create_dm` / `_apply_noise_after_gate` / `_measure_qubit`。
  **EngineBackend v2 architecture**: `run()` three-way dispatch with optional hooks for density matrix, noise, and mid-circuit measurement.

- **`qshow_all(backends)`**：同一电路在多个后端上并行执行，每个后端独立进程。
  **`qshow_all(backends)`**: run the same circuit on multiple backends in parallel (each in a separate process).

- **`run_circuits(builders, backend)`**：多个不同电路并行执行，每个构建函数独立进程。
  **`run_circuits(builders, backend)`**: run different circuits in parallel (each builder in a separate process).

- **77 个算法模板**（从 6 个扩展），覆盖 10 大领域：
  **77 algorithm templates** (up from 6), covering 10 domains:
  - 基石算法（9）：QFT、Deutsch-Jozsa、Bernstein-Vazirani、Simon、SWAP 测试、Hadamard 测试、振幅放大、振幅估计、QPE
    Foundational (9): QFT, Deutsch-Jozsa, Bernstein-Vazirani, Simon, SWAP test, Hadamard test, amplitude amplification, amplitude estimation, QPE
  - 搜索优化（7）：QAOA 通用/TSP/MIS/背包、Grover、量子计数、量子随机行走、量子退火
    Search & Optimization (7): QAOA generic/TSP/MIS/Knapsack, Grover, quantum counting, quantum walk, quantum annealing
  - 量子化学（8）：VQE、哈密顿量导入（OpenFermion/PennyLane/手写）、Trotter、哈密顿量模拟、动态模拟、费米子映射、QSP、分子 VQE
    Quantum Chemistry (8): VQE, Hamiltonian import (OpenFermion/PennyLane/string), Trotter, Hamiltonian simulation, dynamics simulation, fermion mapping, QSP, molecular VQE
  - 线性代数（6）：HHL、矩阵求逆、特征值求解、PDE/ODE 求解、数据拟合
    Linear Algebra (6): HHL, matrix inversion, eigenvalue solver, PDE/ODE solver, data fitting
  - 通信密码（6）：隐形传态、BB84、E91、超密编码、Shor、离散对数
    Communication & Crypto (6): teleportation, BB84, E91, superdense coding, Shor, discrete log
  - 混合算法（7）：VQC、量子核方法、QNG、VQR、QNN、QSVM、量子退火混合
    Hybrid (7): VQC, quantum kernel, QNG, VQR, QNN, QSVM, quantum annealing hybrid
  - 量子纠错（9）：比特/相位翻转码、Shor 9 比特、Steane 7 比特、稳定子、syndrome、表面码、颜色码、容错门
    Error Correction (9): bit/phase flip code, Shor 9-qubit, Steane 7-qubit, stabilizer, syndrome, surface code, color code, FT gates
  - 统计采样（3）：量子蒙特卡洛、拒绝采样、贝叶斯推理
    Statistical (3): quantum Monte Carlo, rejection sampling, Bayesian inference
  - 代数（3）：隐藏子群、格问题、椭圆曲线
    Algebraic (3): hidden subgroup, lattice SVP, elliptic curve
  - 前沿演示（10）：QCNN、QGNN、分布式 QAOA、QTransformer、QRL、QTDA、QPCA、聚类、QGAN、QBM
    Cutting-edge (10): QCNN, QGNN, distributed QAOA, QTransformer, QRL, QTDA, QPCA, clustering, QGAN, QBM

- **cswap 门**：新增原生 CSWAP（Fredkin）门到 IR + `translators/cswap.py` 翻译器。
  **cswap gate**: native CSWAP (Fredkin) gate added to IR + translator.

- **新增测试**：`test_engine_backends.py`、`test_engine_noise.py`、`test_engine_ctrl.py`、`test_foundational_algorithms.py`、`test_search_algorithms.py`。
  **New tests**: engine backends, noise injection, classical control flow, foundational algorithms, search algorithms.

### 变更 Changed

- **TensorCircuit numpy 兼容**：monkey-patch `np.reshape` 和 `np.ComplexWarning` 以兼容 numpy 2.x。
  **TensorCircuit numpy compat**: monkey-patch `np.reshape` and `np.ComplexWarning` for numpy 2.x.

- **QPanda3 API 适配**：`CCX` → `TOFFOLI`、`directly_run` → `CPUQVM` + `QProg` + `measure()`。
  **QPanda3 API adaptation**: `CCX` → `TOFFOLI`, `directly_run` → `CPUQVM` + `QProg` + `measure()`.

- **Cqlib 后端**：确认无本地模拟器，`_sample` 抛出清晰错误。
  **Cqlib backend**: confirmed no local simulator; `_sample` raises clear error.

- **Scheduler 能力矩阵**：新增 `BACKEND_CAPABILITIES` 映射。
  **Scheduler capabilities**: new `BACKEND_CAPABILITIES` mapping.

- **.gitignore**：新增 `.venv312` 和 `.mimocode/`。
  **.gitignore**: added `.venv312` and `.mimocode/`.

### 移除 Removed

- **Paddle Quantum 后端**：因 paddle 3.x 依赖冲突（不支持 complex matmul）彻底移除。
  **Paddle Quantum backend**: removed entirely due to paddle 3.x dependency conflicts (no complex matmul support).

### 修复 Fixed

- **Qulacs `cp` 门**：从错误的 CZ+U1 近似改为正确的 CNOT+P+CNOT 分解。
  **Qulacs `cp` gate**: fixed incorrect CZ+U1 approximation to proper CNOT+P+CNOT decomposition.

- **CUDA-Q `p`/`cp` 门**：修复 `p` 错误近似为 `rz`、`cp` 错误近似为单比特 `rz`。
  **CUDA-Q `p`/`cp` gates**: fixed incorrect `p` ≈ `rz` and `cp` ≈ single-qubit `rz`.

- **QPanda3 `p` 门**：修复 `p` 错误近似为 `rz`。
  **QPanda3 `p` gate**: fixed incorrect `p` ≈ `rz`.

- **读出噪声**：修复 `_apply_readout_noise` 对同一比特串所有 shot 应用相同翻转的 bug。
  **Readout noise**: fixed bug where all shots with the same bitstring got the same flip.

---

## [0.3.0] — 2026-08-17

补齐五块缺口并加入误差缓解：多比特经典寄存器、路由编译、ZNE、读出校准，以及四个新
example。This release fills five gaps and adds error mitigation: multi-bit classical
registers, route-aware compilation, ZNE, readout calibration, and four new examples.

### 新增 Added

- **多比特经典寄存器** `creg(name, width=N)`；`cwhile(reg, until=v)` / `cif(reg, v)`
  支持整数值或比特串判据；`groverize()` 推广到 N 比特成功态。
  **Multi-bit classical registers** `creg(name, width=N)`; `cwhile`/`cif` accept integer
  or bitstring criteria; `groverize()` generalizes to N-bit success states.

- **路由编译** `compile(circuit, coupling_map, route=True)` 自动 `decompose` + `route_swaps`。
  **Route-aware compilation** `compile(..., route=True)` decomposes then routes onto the
  coupling map.

- **ZNE 误差缓解** `zne()` / `fold()`：全局酉折叠 + 线性或指数（三参数）外推，成功率与
  期望值两种指标；`plot_zne()` 可视化。
  **ZNE** `zne()` / `fold()`: global unitary folding with linear or exponential (3-param)
  extrapolation, success and expectation metrics; `plot_zne()` visualization.

- **读出校准** `calibrate()` / `ReadoutCalibration`：逐比特（张量积）与关联（完整 2ⁿ 矩阵）
  两种混淆矩阵模型。
  **Readout calibration** `calibrate()` / `ReadoutCalibration`: per-qubit (tensor-product)
  and correlated (full 2ⁿ matrix) confusion-matrix models.

- **`DensityMatrixEngine.expectation()`** 计算泡利串可观测量期望值。
  **`DensityMatrixEngine.expectation()`** for Pauli-string observables.

- **cmeasure 支持 cirq / pennylane** 后端翻译。
  **cmeasure translation** for the cirq and pennylane backends.

- **新 example**：`creg_multi`、`groverize`、`hardware_compile`、`qi_hardware`。
  **New examples**: `creg_multi`, `groverize`, `hardware_compile`, `qi_hardware`.

### 变更 Changed

- 后端门翻译重构为共享 `translators/` 模块。
  Backend gate translation factored into a shared `translators/` module.

- `NoiseModel` 新增 `readout` 字段（测量比特翻转）。
  `NoiseModel` gained a `readout` (measurement bit-flip) field.

- qi 后端 job 超时 30 → 60 分钟（Tuna-17 排队）。
  qi backend job timeout relaxed 30 → 60 minutes (Tuna-17 queue).

- qi 依赖冲突指南默认改走 venv 方案。
  qi dependency-conflict guide now defaults to the venv workaround.
