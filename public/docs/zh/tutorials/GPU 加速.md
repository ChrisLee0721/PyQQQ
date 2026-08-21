# GPU 加速

学习如何使用 GPU 加速量子模拟，提高计算速度。

## 为什么需要 GPU 加速？

量子模拟需要处理指数级增长的状态空间。对于 $n$ 个量子比特，状态空间大小为 $2^n$。GPU 可以并行处理大量计算，显著加速量子模拟。

## 使用 GPU 后端

```python
from quonic import qgate, qshow
from quonic.gates import H, CX

# 创建电路
qgate(H, 0)
qgate(CX, 0, 1)

# 使用 GPU 后端
qshow(backend='gpu')
```

## 性能对比

```python
import time

# CPU 后端
start = time.time()
qshow(backend='native')
cpu_time = time.time() - start

# GPU 后端
start = time.time()
qshow(backend='gpu')
gpu_time = time.time() - start

print(f"CPU: {cpu_time:.3f}s")
print(f"GPU: {gpu_time:.3f}s")
print(f"Speedup: {cpu_time/gpu_time:.1f}x")
```

## 大规模电路

GPU 在大规模电路上优势更明显：

```python
from quonic import qgate, qshow
from quonic.gates import H, CX

# 创建大规模电路
n_qubits = 20
for i in range(n_qubits):
    qgate(H, i)
for i in range(n_qubits - 1):
    qgate(CX, i, i+1)

# GPU 后端
qshow(backend='gpu')
```

## CUDA 支持

QuoNic 支持 CUDA 加速：

```python
# 检查 CUDA 是否可用
from quonic.backends import gpu
print(f"CUDA available: {gpu.is_available()}")
print(f"GPU: {gpu.device_name()}")
```

## 注意事项

1. GPU 加速需要 NVIDIA GPU 和 CUDA 支持
2. 对于小规模电路，CPU 可能更快（GPU 有启动开销）
3. GPU 内存有限，超大电路可能需要分批处理

## 下一步

- [量子算法](量子算法.md) - 学习基本量子算法
- [噪声缓解](噪声缓解.md) - 处理量子噪声
- [高级特性](高级特性.md) - 学习高级功能
