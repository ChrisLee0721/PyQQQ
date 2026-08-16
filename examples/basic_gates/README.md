# Basic gates 基础门

演示 X、Y、Z、CZ、CCX（Toffoli）与显式 MEASURE：X 翻转比特，Y/Z 加相位（此处测量不可见），CCX 受控翻转，qshow() 自动补测未显式测量的比特。

Demonstrates X, Y, Z, CZ, CCX (Toffoli) and explicit MEASURE: X flips bits, Y/Z add phases (invisible here), CCX flips conditionally, and qshow() auto-measures the rest.

## 运行 Run

```bash
python examples/basic_gates/basic_gates.py
```

## 预期输出 Expected output

几乎确定测到 |110>（qubit0=0，qubit1、2=1）。

Almost surely |110> (qubit 0 = 0, qubits 1 and 2 = 1).
