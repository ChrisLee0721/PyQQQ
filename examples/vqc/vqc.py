"""Variational Quantum Classifier (VQC) — simple demo.

Demonstrates a variational quantum circuit for binary classification:
1. Encode data into quantum state
2. Apply parameterized circuit
3. Measure to get classification result
4. Optimize parameters using classical optimizer

Usage:
    python examples/vqc/vqc.py
"""


import numpy as np
from scipy.optimize import minimize

from quonic import qgate, reset
from quonic.backends import get_backend
from quonic.gates import CX, Ry
from quonic.stack import current_circuit


def vqc_circuit(params, x):
    """Build a VQC circuit.

    Args:
        params: rotation angles [θ1, θ2, θ3, θ4]
        x: input features [x1, x2]

    Returns:
        Circuit with encoded data and parameterized rotations.
    """
    # Encode data: Ry(x1) on q0, Ry(x2) on q1
    qgate(Ry(float(x[0])), 0)
    qgate(Ry(float(x[1])), 1)

    # Entangle
    qgate(CX, 0, 1)

    # Parameterized rotations
    qgate(Ry(float(params[0])), 0)
    qgate(Ry(float(params[1])), 1)

    # Entangle again
    qgate(CX, 0, 1)

    # More rotations
    qgate(Ry(float(params[2])), 0)
    qgate(Ry(float(params[3])), 1)

    return current_circuit()


def predict(params, x):
    """Predict class label for input x."""
    reset()
    circuit = vqc_circuit(params, x)
    result = get_backend("native").run(circuit, shots=100)
    # Classify based on qubit 0 measurement
    p0 = result.counts.get("0", 0) / 100
    return 0 if p0 > 0.5 else 1


def loss(params, X, y):
    """Compute classification loss."""
    total_loss = 0.0
    for xi, yi in zip(X, y):
        pred = predict(params, xi)
        total_loss += (pred - yi) ** 2
    return total_loss / len(y)


def main():
    # Simple dataset: XOR-like
    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    y = [0, 1, 1, 0]

    print("Variational Quantum Classifier")
    print(f"  Dataset: {X} → {y}")

    # Train
    init_params = np.random.randn(4) * 0.5
    result = minimize(loss, init_params, args=(X, y), method="COBYLA", options={"maxiter": 200})
    print(f"  Final loss: {result.fun:.3f}")

    # Predict
    for xi, yi in zip(X, y):
        pred = predict(result.x, xi)
        print(f"  Input: {xi} → Predicted: {pred}, Actual: {yi}")


if __name__ == "__main__":
    main()
