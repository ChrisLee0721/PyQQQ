# Pulse Control API / 脉冲控制 API

Pulse-level control for quantum gates. Optimize gate fidelity with GRAPE and Krotov.

量子门的脉冲级控制。用 GRAPE 和 Krotov 优化门保真度。

## Quick Start / 快速开始

```python
from quonic.pulse import grape_optimize
import numpy as np

# Target: X gate (π rotation around X)
target = np.array([[0, 1], [1, 0]], dtype=complex)

# Optimize pulse shape
result = grape_optimize(target, n_steps=50, T=10.0)
print(f"Fidelity: {result.fidelity:.6f}")
print(f"Pulse shape: {result.pulse.shape}")
```

## Pulse Definitions / 脉冲定义

### GaussianPulse

```python
from quonic.pulse import GaussianPulse

pulse = GaussianPulse(duration=10.0, sigma=2.0, amplitude=1.0)
```

### DragPulse (Derivative Removal by Adiabatic Gate)

```python
from quonic.pulse import DragPulse

pulse = DragPulse(duration=10.0, sigma=2.0, amplitude=1.0, beta=0.5)
```

### CrossResonancePulse

```python
from quonic.pulse import CrossResonancePulse

pulse = CrossResonancePulse(duration=20.0, amplitude=1.0)
```

## Optimization / 优化

### grape_optimize — GRAPE Algorithm / GRAPE 算法

Gradient Ascent Pulse Engineering. Optimizes pulse amplitudes.

梯度上升脉冲工程。优化脉冲幅度。

```python
from quonic.pulse import grape_optimize

result = grape_optimize(
    target_unitary,  # Target gate
    n_steps=50,      # Time steps
    T=10.0,          # Total duration (ns)
    maxiter=1000,    # Optimization iterations
)
```

### krotov_optimize — Krotov's Method / Krotov 方法

Monotonically convergent optimization.

单调收敛优化。

```python
from quonic.pulse import krotov_optimize

result = krotov_optimize(target_unitary, n_steps=50, T=10.0)
```

## Calibration / 校准

```python
from quonic.pulse import rabi_calibration, t1_calibration, t2_calibration

# Rabi oscillation: find π-pulse amplitude
rabi = rabi_calibration(n_points=50)

# T1 relaxation time
t1 = t1_calibration(n_points=50)

# T2 dephasing time
t2 = t2_calibration(n_points=50)
```

## Decoupling Sequences / 解耦序列

```python
from quonic.pulse import cpmg_sequence, xy4_sequence

# CPMG sequence for T2 extension
cpmg = cpmg_sequence(n_pulses=8, duration=100.0)

# XY-4 sequence (more robust)
xy4 = xy4_sequence(n_cycles=4, duration=100.0)
```

## Examples / 示例

### Optimize X gate / 优化 X 门

```python
from quonic.pulse import grape_optimize
import numpy as np

# X gate target
X = np.array([[0, 1], [1, 0]], dtype=complex)

result = grape_optimize(X, n_steps=50, T=10.0)
print(f"X gate fidelity: {result.fidelity:.6f}")
```

### Optimize CNOT gate / 优化 CNOT 门

```python
from quonic.pulse import grape_optimize
import numpy as np

# CNOT gate target (4x4 matrix)
CNOT = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0],
], dtype=complex)

result = grape_optimize(CNOT, n_steps=100, T=20.0)
print(f"CNOT fidelity: {result.fidelity:.6f}")
```
