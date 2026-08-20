"""Convert from Qiskit Nature / 从 Qiskit Nature 转换

Convert from Qiskit Nature / 从 Qiskit Nature 转换

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

from qiskit.quantum_info import SparsePauliOp

from quonic.algorithms import from_qiskit_nature, vqe

op = SparsePauliOp.from_list([("ZZ", 1.0), ("XI", 1.0), ("IX", 1.0)])
terms = from_qiskit_nature(op)
print(terms)  # [(1.0, "ZZ"), (1.0, "XI"), (1.0, "IX")]

result = vqe(terms, 2, maxiter=200)
print(result.value)  # ~ -2.236
