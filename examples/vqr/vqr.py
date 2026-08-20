"""Variational Quantum Regressor / 变分量子回归器

Quantum model for regression tasks.
用于回归任务的量子模型。

## Application / 应用场景
- Regression (回归)
- Prediction (预测)
- Function fitting (函数拟合)

## Output / 输出
Predicted values.
预测值。"""

from quonic.algorithms import vqr

X = [[0.0], [0.5], [1.0], [1.5]]
y = [0.0, 0.479, 0.841, 0.997]
result = vqr(X, y, n_params=2, maxiter=100)
print(f"Final loss: {result.value}")
