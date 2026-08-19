"""Find ground state energy / 寻找基态能量

Variational Quantum Eigensolver finds the lowest energy of a quantum system.
变分量子本征求解器找到量子系统的最低能量。

## Application / 应用场景
- Quantum chemistry: molecular ground states (量子化学：分子基态)
- Materials science: new materials (材料科学：新材料)
- Drug discovery: molecular properties (药物发现：分子性质)

## How it works / 原理
Parameterized circuit + classical optimizer minimize energy expectation.
参数化电路 + 经典优化器最小化能量期望值。

## Output / 输出说明
Energy value converges to exact ground state energy.
能量值收敛到精确基态能量。

## Classical vs Quantum / 经典 vs 量子
Classical: exponential scaling with system size. Quantum: polynomial.
经典：随系统规模指数增长。量子：多项式。
"""


from quonic.algorithms import vqe

hamiltonian = [(1.0, "ZZ"), (1.0, "XI"), (1.0, "IX")]
result = vqe(hamiltonian, 2, init_params=[0.1] * 4, maxiter=200)
print(result.value)  # ≈ -2.236
