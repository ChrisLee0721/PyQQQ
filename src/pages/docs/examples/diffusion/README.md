# Diffusion 扩散算子原语

diffusion(n) 把振幅放大算子 2|s><s| - I 追加到当前电路，与 mark_state()
组合即完成一次 Grover 迭代。这里在 2 比特上搜索 |11>，单次迭代后几乎确定命中。

diffusion(n) appends the amplitude-amplification operator 2|s><s| - I to the
current circuit; combined with mark_state() it performs one Grover iteration.
Here it searches |11> on 2 qubits — one iteration hits it almost surely.

## 运行 Run

```bash
python examples/diffusion/diffusion.py
```

## 预期输出 Expected output

几乎确定测到 |11>。

Almost surely |11>.
