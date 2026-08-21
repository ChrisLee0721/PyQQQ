# Quantum Machine Learning API / 量子机器学习 API

## train() — Hybrid Training / 混合训练

Train a parameterized quantum circuit using gradient descent.

使用梯度下降训练参数化量子电路。

```python
from quonic.ml import train

def ansatz(params):
    from quonic import qgate
    from quonic.gates import CX, Ry
    qgate(Ry(params[0]), 0)
    qgate(CX, 0, 1)
    qgate(Ry(params[1]), 1)

def loss_fn(params):
    # Compute expectation value
    ansatz(params)
    from quonic import qshow
    result = qshow()
    return abs(result.expectation("ZI"))

result = train(loss_fn, n_params=2, lr=0.1, maxiter=100)
print(result.params)  # Optimized parameters
print(result.loss)    # Final loss
```

### Gradient methods / 梯度方法

| Method | Description | Speed |
|--------|-------------|-------|
| `param_shift` | Parameter shift rule (参数移位规则) | Exact, 2 evals/param |
| `adjoint` | Adjoint differentiation (伴随微分) | Exact, O(1) evals |
| `spsa` | Simultaneous perturbation (同时扰动) | Approximate, 2 evals total |

## QMLPipeline — End-to-End QML / 端到端量子机器学习

```python
from quonic.ml import QMLPipeline

pipeline = QMLPipeline(
    encoding="angle",
    ansatz="hardware_efficient",
    n_layers=3,
    optimizer="adam",
)

# Train on data
pipeline.fit(X_train, y_train, epochs=50)

# Predict
predictions = pipeline.predict(X_test)
```

## Adjoint Differentiation / 伴随微分

O(1) backpropagation for quantum circuits — true gradient in one backward pass.

量子电路的 O(1) 反向传播——一次反向传播得到精确梯度。

```python
from quonic.ml import adjoint_grad_exact

grad = adjoint_grad_exact(circuit, params, observable)
# Returns exact gradient with O(1) circuit evaluations
```

## HybridModel — Classical + Quantum / 经典 + 量子混合模型

```python
from quonic.ml import HybridModel, ClassicalLayer, QNNLayer

model = HybridModel([
    ClassicalLayer(784, 128),   # Classical preprocessing
    QNNLayer(8, 4, layers=3),  # Quantum neural network
    ClassicalLayer(4, 10),     # Classical output
])

model.fit(X_train, y_train, epochs=20)
```

## Encoding Methods / 编码方法

```python
from quonic.ml import angle_encode, amplitude_encode, iqp_encode

# Angle encoding: data → rotation angles
# 角度编码：数据 → 旋转角
angle_encode(data, qubits=[0, 1, 2])

# Amplitude encoding: data → amplitudes
# 振幅编码：数据 → 振幅
amplitude_encode(data, n_qubits=3)

# IQP encoding: data → diagonal unitary
# IQP 编码：数据 → 对角酉算子
iqp_encode(data, qubits=[0, 1, 2])
```

## Loss Functions / 损失函数

```python
from quonic.ml import expectation_loss, fidelity_loss, cross_entropy_loss

# Expectation value loss
loss = expectation_loss(circuit, params, observable="ZZ")

# Fidelity loss (for state preparation)
loss = fidelity_loss(circuit, params, target_state)

# Cross-entropy loss (for classification)
loss = cross_entropy_loss(predictions, labels)
```
