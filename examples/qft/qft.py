"""Quantum Fourier Transform / 量子傅里叶变换

Quantum version of DFT. Foundation for many quantum algorithms.
量子版 DFT。许多量子算法的基础。

## Application / 应用场景
- Shor's algorithm (Shor 算法)
- Quantum phase estimation (量子相位估计)
- Quantum counting (量子计数)
- Signal processing (信号处理)

## How it works / 原理
H gates + controlled rotations create frequency-domain representation.
H 门 + 受控旋转创建频域表示。

## Output / 输出说明
Transforms computational basis to Fourier basis.
将计算基变换到傅里叶基。

## Classical vs Quantum / 经典 vs 量子
Classical FFT: O(N log N). Quantum QFT: O(log²N) — exponential speedup.
经典 FFT：O(N log N)。量子 QFT：O(log²N) — 指数加速。
"""


from quonic.algorithms import qft

result = qft(n_qubits=3, shots=1024)
print(result.counts)
