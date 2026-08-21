# Quantum Machine Learning

## Problem

Train a quantum model to classify data using variational circuits.

## Code

```python
from quonic.ml import QMLPipeline

# Create pipeline
pipeline = QMLPipeline(n_qubits=2, layers=2, optimizer="adam", lr=0.01)

# Training data
X_train = [[0.1, 0.2], [0.3, 0.4], [0.5, 0.6], [0.7, 0.8]]
y_train = [0.0, 0.3, 0.6, 0.9]

# Train
result = pipeline.fit(X_train, y_train, maxiter=50)
print(f"Final loss: {result.train_result.final_loss:.4f}")

# Predict
predictions = pipeline.predict([[0.2, 0.3]])
print(f"Prediction: {predictions[0]:.4f}")
```

## Output

```
Final loss: 0.0234
Prediction: 0.2891
```

## How it works

1. **Encoding**: Map classical data to quantum rotations
2. **Ansatz**: Parameterized quantum circuit
3. **Measurement**: Expectation value as output
4. **Training**: Parameter-shift gradient + optimizer

## Download

[Download vqc.py](docs/examples/vqc/vqc.py)
