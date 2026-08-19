"""Quantum Convolutional Neural Network demo.

Quantum CNN for image classification tasks.
Output: classification accuracy.
"""

from quonic.algorithms import qcnn_demo

result = qcnn_demo(maxiter=50)
print(f"Accuracy: {result.value}")
