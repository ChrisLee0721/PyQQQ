# Classical if 经典控制流

cif(0).then(X,1).else_(Z,1) 会**先测量**控制比特，再按结果二选一施加分支门，
产生经典混合态（无纠缠）。与 qif（量子叠加 if）的根本区别就在「先测量再分支」。

cif(0).then(X,1).else_(Z,1) MEASURES the control qubit first, then applies one
branch — a classical mixed state (no entanglement). The measure-then-branch
semantics is what distinguishes it from qif.

## 运行 Run

```bash
python examples/cif/cif.py
```

## 预期输出 Expected output

控制比特处于叠加态时，最后的 H⊗H 旋转把计数摊到四个基态，各约 25%
（纠缠的 qif 会给出 |00>/|11> 各约 50%，且 |01>/|10> 消失）。

With the control in superposition, the final H⊗H rotation spreads counts
across all four basis states at ~25% each (the entangled qif would instead
give ~50% |00> and ~50% |11>, with |01>/|10> vanishing).
