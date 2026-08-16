# Quantum phase estimation 量子相位估计

估计 Rz(π) 作用在 |1> 上的本征相位。3 个精度比特给出 j=2，即相位估计 "010"（输出比特串最右侧 3 位）。

Estimate the eigenvalue phase of Rz(π) on |1>. Three precision qubits give j = 2, i.e. phase estimate "010" (the rightmost 3 bits of the output).

## 运行 Run

```bash
python examples/qpe/qpe.py
```

## 预期输出 Expected output

计数直方图几乎全部集中在最右侧 3 位为 "010" 的比特串上。

The counts are almost entirely on the bitstring whose rightmost 3 bits are "010".
