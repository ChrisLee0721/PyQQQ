"""SWAP Test / SWAP 测试

Estimate overlap between two quantum states.
估计两个量子态之间的重叠。

## Application / 应用场景
- State comparison (态比较)
- Kernel estimation (核估计)
- Fidelity measurement (保真度测量)

## Output / 输出
P(|0⟩) = (1 + |⟨a|b⟩|²) / 2."""

from quonic import qgate
from quonic.algorithms import swap_test
from quonic.gates import X


# prepare(circuit, qubit_index, n_qubits)
def prep_a(circuit, q, n):
    pass  # |0>

def prep_b(circuit, q, n):
    qgate(X, q)  # |1> — orthogonal to |0>

result = swap_test(1, prep_a, prep_b, shots=10000)
print(result.counts)
