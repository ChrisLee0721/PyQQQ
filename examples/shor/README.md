# Shor's algorithm Shor 算法

用量子周期查找分解 15 = 3 × 5。固定基 a=7（阶为 4），小精度（t=6）跑一次即可返回 3 或 5。

Factor 15 = 3 × 5 via quantum period finding. With base a=7 (order 4), a single small-precision run returns 3 or 5.

## 运行 Run

```bash
python examples/shor/shor.py
```

## 预期输出 Expected output

约 3 或 5，且打印阶 period = 4。

3 or 5, and it prints the order period = 4.
