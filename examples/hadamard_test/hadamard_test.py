"""Estimate Re(<ψ|U|ψ>) / 估计 Re(<ψ|U|ψ>)

Primitive for inner product estimation.
内积估计的基本操作。

## Application / 应用场景
- Quantum algorithms (量子算法)
- State overlap (态重叠)
- Expectation values (期望值)

## Output / 输出
Probability of |0⟩ encodes the real part.
|0⟩ 的概率编码实部。"""

from quonic import qgate
from quonic.algorithms import hadamard_test
from quonic.gates import X


# prepare_psi(circuit, qubit_index, n_qubits)
def prep_psi(circuit, q, n):
    qgate(X, q)  # |1>

# apply_u(circuit, qubit_index)
def apply_u(circuit, q):
    pass  # Identity

result = hadamard_test(1, prep_psi, apply_u, shots=10000)
print(result.counts)
