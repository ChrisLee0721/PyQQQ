"""Quantum Neural Network demo.

Variational quantum circuit as a neural network.
Output: trained model predictions.
"""

from quonic.algorithms import qnn_demo

result = qnn_demo(n_qubits=2, depth=2)
print(result.counts)
