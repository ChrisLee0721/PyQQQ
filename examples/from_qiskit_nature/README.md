# from_qiskit_nature 从 Qiskit 导入哈密顿量

把 Qiskit 的 SparsePauliOp（H = Z⊗Z + X⊗I + I⊗X）转成 vqe() 所需的 [(系数, 泡利串)] 格式，再变分求解基态能量 -√5 ≈ -2.236。需要 qiskit + scipy。

Convert a Qiskit SparsePauliOp (H = Z⊗Z + X⊗I + I⊗X) into the [(coeff, pauli)] form vqe() expects, then solve for the ground energy -√5 ≈ -2.236. Requires qiskit + scipy.

## 运行 Run

```bash
python examples/from_qiskit_nature/from_qiskit_nature.py
```

## 预期输出 Expected output

先打印三项泡利串，再打印约 -2.236。

It prints the three Pauli terms, then around -2.236.
