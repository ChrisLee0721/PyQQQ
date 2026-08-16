# VQE 变分基态能量

变分求解横向场 Ising 模型 H = Z⊗Z + X⊗I + I⊗X 的基态能量，精确值 -√5 ≈ -2.236。
需要 scipy。

Variational ground-state energy of H = Z⊗Z + X⊗I + I⊗X; exact value -√5 ≈ -2.236.
Requires scipy.

## 运行 Run

```bash
python examples/vqe/vqe.py
```

## 预期输出 Expected output

约 -2.236（COBYLA 收敛到附近）。

Around -2.236 (COBYLA converges nearby).
