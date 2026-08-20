# 性能优化计划

## 优化项

### 1. CuPy 多比特门向量化

**当前问题**：CX/CCX/SWAP/MCZ 用 Python 循环，n=20 时单次 CX 需循环 100 万次。

**优化方案**：用 numpy 索引操作替换 Python 循环。

```python
# 当前（慢）
for i in range(2**n):
    if (i >> control) & 1 == 1:
        j = i ^ (1 << target)
        new_sv[i] = sv[j]
        new_sv[j] = sv[i]

# 优化后（快）
idx = np.arange(2**n)
mask = (idx >> control) & 1 == 1
pairs = idx[mask] ^ (1 << target)
new_sv[mask] = sv[pairs]
new_sv[pairs] = sv[mask]
```

**收益**：真实电路 10x 加速。

### 2. 门融合 (Gate Fusion)

**当前问题**：连续单比特门逐个执行，每次都是 O(2^n) 矩阵乘法。

**优化方案**：将连续单比特门合并为一个矩阵，一次执行。

```python
# 当前
H(0) → Ry(0.5, 0) → Rz(0.3, 0)  # 3 次矩阵乘法

# 优化后
U = Rz(0.3) @ Ry(0.5) @ H  # 合并为一个矩阵
apply(U, qubit=0)  # 1 次矩阵乘法
```

**收益**：深电路 2-3x 加速。

### 3. 稀疏矩阵支持

**当前问题**：密度矩阵用完整 2^n × 2^n 矩阵存储，大电路内存爆炸。

**优化方案**：用 CSR 格式存储稀疏密度矩阵。

```python
# 当前
rho = np.zeros((2**n, 2**n))  # 完整矩阵

# 优化后
from scipy.sparse import csr_matrix
rho = csr_matrix((2**n, 2**n))  # 稀疏矩阵
```

**收益**：内存 10x 减少。

### 4. Numba JIT 编译

**当前问题**：Python 循环在大电路上很慢。

**优化方案**：用 Numba JIT 编译关键循环。

```python
import numba as nb

@nb.njit
def apply_cx(sv, control, target, n):
    for i in range(2**n):
        if (i >> control) & 1 == 1:
            j = i ^ (1 << target)
            sv[i], sv[j] = sv[j], sv[i]
    return sv
```

**收益**：10-100x 加速。

### 5. 电路缓存

**当前问题**：相同电路重复编译。

**优化方案**：缓存编译结果。

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def compile_circuit(circuit_key):
    # 编译电路
    return compiled
```

**收益**：重复电路 100x 加速。

## 实现优先级

| 优先级 | 优化项 | 收益 | 工作量 |
|---|---|---|---|
| P0 | CuPy 多比特门向量化 | 10x | 中 |
| P0 | 门融合 | 2-3x | 中 |
| P1 | 稀疏矩阵 | 内存 10x | 大 |
| P2 | Numba JIT | 10-100x | 中 |
| P3 | 电路缓存 | 100x | 小 |
