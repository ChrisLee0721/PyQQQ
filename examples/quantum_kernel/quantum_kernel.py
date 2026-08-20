"""Quantum Kernel Estimation / 量子核估计

Compute quantum kernel matrix for ML.
计算用于机器学习的量子核矩阵。

## Application / 应用场景
- Kernel methods (核方法)
- SVM (支持向量机)
- Quantum ML (量子机器学习)

## Output / 输出
Kernel matrix entries.
核矩阵元素。"""

from quonic.algorithms import quantum_kernel

X = [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]]
result = quantum_kernel(X, n_qubits=2, shots=10000)
print(result.counts)
