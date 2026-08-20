# Depolarizing noise 去极化噪声

在贝尔态上叠加 5% 去极化噪声，导致 |01>、|10> 泄漏（无噪声时应为 0）。

5% depolarizing noise on a Bell state leaks population into |01> and |10>.

## 运行 Run

```bash
python examples/noise/noise.py
```

## 预期输出 Expected output

|01> 和 |10> 出现少量计数（无噪声时为 0）。

|01> and |10> get a small count (zero without noise).
