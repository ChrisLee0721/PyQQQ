"""Jordan-Wigner transform / Jordan-Wigner 变换

Map fermionic Hamiltonian to qubit Hamiltonian.
将费米子哈密顿量映射到量子比特哈密顿量。

## Application / 应用场景
- Quantum chemistry (量子化学)
- Fermionic systems (费米子系统)
- Hubbard model (Hubbard 模型)

## Output / 输出
Qubit Hamiltonian for simulation.
用于模拟的量子比特哈密顿量。"""

from quonic.algorithms import jordan_wigner_2site

result = jordan_wigner_2site(t=1.0, U=2.0)
print(result.counts)
