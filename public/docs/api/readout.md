# Readout Calibration API / 读出校准 API

Correct measurement errors by inverting the confusion matrix.

通过反转混淆矩阵校正测量误差。

## Quick Start / 快速开始

```python
from quonic.readout import calibrate

# Calibrate measurement errors
# 校准测量误差
cal = calibrate(backend="qiskit", n_qubits=2, shots=8192)

# Apply to results
corrected = cal.apply(raw_counts)
```

## calibrate() — Build Calibration Matrix / 构建校准矩阵

```python
from quonic.readout import calibrate

cal = calibrate(backend="native", n_qubits=2, shots=8192)
print(cal.matrix)
# [[0.98, 0.02],
#  [0.03, 0.97]]
```

## ReadoutCalibration — Apply Corrections / 应用校正

```python
from quonic.readout import ReadoutCalibration

cal = ReadoutCalibration(matrix)

# Correct raw counts
raw = {"00": 480, "01": 20, "10": 30, "11": 470}
corrected = cal.apply(raw)
# {"00": 500, "01": 0, "10": 0, "11": 500}
```

## Examples / 示例

### Full readout calibration / 完整读出校准

```python
from quonic.readout import calibrate
from quonic import qshow

# Step 1: Calibrate
cal = calibrate(backend="qiskit", n_qubits=3, shots=8192)

# Step 2: Run circuit
result = qshow(backend="qiskit")

# Step 3: Correct results
corrected = cal.apply(result.counts)
print(corrected)
```
