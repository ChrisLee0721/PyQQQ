# NoiseModel 噪声模型

单比特 1%、双比特 5% 的去极化噪声作用在贝尔态上，导致 |01>、|10> 少量泄漏（无噪声时为 0）。

1% single-qubit and 5% two-qubit depolarizing noise on a Bell state leaks a little population into |01> and |10> (zero without noise).

## 运行 Run

```bash
python examples/noise_model/noise_model.py
```

## 预期输出 Expected output

|01> 和 |10> 出现少量计数（无噪声时为 0）。

|01> and |10> get a small count (zero without noise).
