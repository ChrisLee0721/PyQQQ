# 04_gpu_acceleration 中文版

参见 [英文版](04_gpu_acceleration.md)


Speed up quantum simulation with GPU backends.

## Direct GPU Execution

```python
from quonic import qgate, qshow
from quonic.gates import H, CX

qgate(H, 0)
qgate(CX, 0, 1)
qshow(method='gpu')  # Run on GPU
```

## Smart Scheduling

The scheduler picks the best GPU backend automatically:

```python
from quonic.scheduler import recommend_backend_gpu, circuit_features

feats = circuit_features(circuit)
rec = recommend_backend_gpu(feats)
print(f"Best GPU backend: {rec.backend}")
```

| Circuit Type | Best Backend | Why |
|---|---|---|
| High entanglement, small n | qulacs | Fastest statevector GPU |
| Low entanglement, large n | tensorcircuit | Tensor network on GPU |
| Classical control flow | qulacs | Stateful collapse |
| Fallback | cupy | Universal GPU engine |

## CuPy Fallback

When a backend has no native GPU, it falls back to CuPy:

```python
# qulacs GPU → CuPy fallback if no qulacs GPU
qshow(backend='qulacs', method='gpu')
```

## Installing GPU Support

```bash
pip install 'quonic[gpu]'        # CuPy (NVIDIA CUDA)
pip install 'quonic[qulacs]'     # Qulacs (native GPU)
```

## Performance

On RTX 2070 (8GB):

| Circuit | CPU (native) | GPU (CuPy) | Speedup |
|---------|-------------|------------|---------|
| GHZ-8 | 0.015s | 0.007s | 2x |
| GHZ-16 | 0.12s | 0.02s | 6x |
| GHZ-20 | 0.53s | 0.05s | 10x |
