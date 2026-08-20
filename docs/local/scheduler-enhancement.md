# 调度器增强计划

## 当前状态

调度器基于静态规则：
- `recommend_method()`: noise → density_matrix, clifford → stabilizer, etc.
- `recommend_backend_gpu()`: entanglement + n → qulacs/tensorcircuit/cupy
- 数据来源：hardcoded thresholds + `benchmarks.json`

## 增强项

### 1. 学习型调度 (Learning Scheduler)

**问题**：hardcoded 阈值没有 benchmark 数据支撑。

**方案**：用 `LocalCacheRegistry` 记录用户运行历史，自动调优。

```python
# 当前
rec = recommend_backend_gpu(features)  # 硬编码阈值

# 增强后
rec = recommend_backend_gpu(features)  # 先查 measured data
# measured data 来自用户的实际运行记录
```

**实现**：
1. `LocalCacheRegistry` 记录每次运行的 (features → backend, time)
2. 调度器读取缓存，用加权平均计算最优后端
3. 新电路直接用缓存数据，无需重新 benchmark

### 2. 电路指纹 (Circuit Fingerprint)

**问题**：当前特征太粗糙（n, depth, gate_types）。

**方案**：更精细的特征提取。

```python
features = {
    "n": 10,
    "depth": 50,
    "gate_count": 200,
    "cx_count": 80,           # 新增：CNOT 数量
    "t_count": 20,            # 新增：T 门数量
    "parameterized": True,    # 新增：是否参数化
    "has_noise": False,       # 新增：是否需要噪声
    "entanglement_ratio": 0.3, # 新增：纠缠门比例
}
```

### 3. 后端健康检查 (Backend Health Check)

**问题**：后端可能不可用（GPU 内存不足、队列满）。

**方案**：运行前检查后端健康状态。

```python
def check_backend_health(backend_name):
    """检查后端是否可用。"""
    if backend_name == "qulacs":
        # 检查 GPU 内存
        import cupy
        free, _ = cupy.cuda.Device().mem_info
        return free > 2**30  # 至少 1GB
    elif backend_name == "qi":
        # 检查队列状态
        ...
    return True
```

### 4. 动态降级 (Dynamic Fallback)

**问题**：OOM 时直接崩溃。

**方案**：运行时 OOM 自动降级到更小后端。

```python
def run_with_fallback(circuit, backend, shots):
    """运行电路，OOM 时自动降级。"""
    try:
        return backend.run(circuit, shots=shots)
    except (MemoryError, RuntimeError):
        # 降级到 native
        return get_backend("native").run(circuit, shots=shots)
```

### 5. 成本感知调度 (Cost-Aware Scheduling)

**问题**：不考虑后端价格。

**方案**：调度器考虑 QPU 秒数和价格。

```python
costs = {
    "ibm": 1.5,      # $/QPU-second
    "braket": 0.30,
    "ionq": 0.01,    # $/shot
    "native": 0,     # 免费
}

def recommend_with_cost(features, budget):
    """考虑预算的调度。"""
    rec = recommend_backend_gpu(features)
    if costs.get(rec.backend, 0) > budget:
        return Recommendation("native", "statevector")  # 降级到免费
    return rec
```

## 实现优先级

| 优先级 | 增强项 | 收益 | 工作量 |
|---|---|---|---|
| P0 | 学习型调度 | 自动优化 | 中 |
| P0 | 后端健康检查 | 鲁棒性 | 小 |
| P1 | 动态降级 | 鲁棒性 | 小 |
| P2 | 电路指纹 | 调度精度 | 中 |
| P3 | 成本感知 | 成本优化 | 中 |
