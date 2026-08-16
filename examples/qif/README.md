# Quantum if 量子叠加 if

用 if/else 写受控门：qif(0).then(X,1).else_(I,1) 等价于 CNOT(0,1)。
控制比特不被测量，两分支相干叠加，产生真纠缠。

Write a controlled gate as if/else: qif(0).then(X,1).else_(I,1) is a CNOT(0,1).
The control qubit is NOT measured; both branches superpose coherently.

## 运行 Run

```bash
python examples/qif/qif.py
```

## 预期输出 Expected output

约 50% 的 |00> 和 50% 的 |11>（与贝尔态一致）。

Roughly 50% |00> and 50% |11> (same as the Bell state).
