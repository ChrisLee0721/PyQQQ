"""Quantum Machine Learning Workflow / 量子机器学习工作流

Complete QML workflow with training and prediction.
带有训练和预测的完整 QML 工作流。

## Application / 应用场景
- Classification (分类)
- Regression (回归)
- Pattern recognition (模式识别)

## Output / 输出
Trained model with predictions.
带有预测的训练模型。"""

from quonic.ml import Ansatz, SPSAOptimizer, train, param_shift_grad, QMLPipeline
from quonic.ir import Circuit, GateOperation
import numpy as np

print("=== Quantum Machine Learning: VQC Classification ===")
print()

# Simple 2D classification problem
# Class 0: points near origin
# Class 1: points far from origin
X_train = [[0.1, 0.1], [0.2, 0.3], [0.15, 0.2], [0.3, 0.1]]
y_train = [0, 0, 0, 0]

X_test = [[0.8, 0.9], [0.7, 0.8], [0.9, 0.7]]
y_test = [1, 1, 1]

print("Training data:")
for i, (x, y) in enumerate(zip(X_train, y_train)):
    print(f"  {i}: {x} → class {y}")
print()

print("Test data:")
for i, (x, y) in enumerate(zip(X_test, y_test)):
    print(f"  {i}: {x} → class {y}")
print()

# Method 1: Manual VQC
print("--- Method 1: Manual VQC ---")
ansatz = Ansatz.hardware_efficient(n_qubits=2, layers=2)
opt = SPSAOptimizer(maxiter=100, lr=0.1)

def loss_fn(params):
    total_loss = 0.0
    for xi, yi in zip(X_train, y_train):
        # Encode features as rotation angles
        c = ansatz.build(params)
        from quonic.ml import expectation_loss
        pred = expectation_loss(c, "ZZ")
        total_loss += (pred - yi) ** 2
    return total_loss / len(X_train)

result = train(ansatz, opt, loss_fn, gradient="param_shift")
print(f"Final loss: {result.final_loss:.4f}")
print(f"Steps: {result.n_steps}")
print()

# Method 2: QML Pipeline
print("--- Method 2: QML Pipeline ---")
pipeline = QMLPipeline(n_qubits=2, layers=2, optimizer="spsa", lr=0.1)
pipeline_result = pipeline.fit(X_train, y_train, maxiter=50)
print(f"Final loss: {pipeline_result.train_result.final_loss:.4f}")
print()

# Prediction
print("--- Prediction ---")
predictions = pipeline.predict(X_test)
print("Test predictions:")
for i, (x, y, pred) in enumerate(zip(X_test, y_test, predictions)):
    print(f"  {i}: {x} → predicted={pred:.2f}, actual={y}")
print()

print("=== Conclusion ===")
print("QuoNic provides complete QML workflow:")
print("1. Ansatz library (hardware-efficient, QAOA, UCCSD)")
print("2. Data encoding (angle, amplitude, IQP)")
print("3. Parameter-shift gradient for training")
print("4. QML pipeline for end-to-end workflow")
