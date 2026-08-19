"""Training loop for variational quantum algorithms.

Example::

    from quonic.ml import Ansatz, angle_encode, SPSAOptimizer, expectation_loss, train

    ansatz = Ansatz.hardware_efficient(n_qubits=4, layers=3)
    opt = SPSAOptimizer(maxiter=100)
    result = train(ansatz, opt, loss_fn=lambda p: expectation_loss(ansatz.build(p), "ZZII"))
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, List, Optional

import numpy as np

from .ansatz import AnsatzBuilder


@dataclass
class TrainResult:
    """Result of a training run."""

    params: np.ndarray
    loss_history: List[float]
    final_loss: float
    n_steps: int


def train(
    ansatz: AnsatzBuilder,
    optimizer: Any,
    loss_fn: Callable[[np.ndarray], float],
    init_params: Optional[np.ndarray] = None,
    seed: int = 42,
    verbose: bool = False,
) -> TrainResult:
    """Train a variational quantum circuit.

    Args:
        ansatz: ansatz builder with n_params attribute
        optimizer: optimizer with init() and step() methods
        loss_fn: loss function(params) -> float
        init_params: initial parameters (random if None)
        seed: random seed
        verbose: print progress

    Returns:
        TrainResult with optimized parameters and loss history.
    """
    rng = np.random.RandomState(seed)

    if init_params is None:
        init_params = rng.randn(ansatz.n_params) * 0.1

    params = init_params.copy()
    loss_history = []

    for step in range(optimizer.maxiter):
        loss = loss_fn(params)
        loss_history.append(loss)

        if verbose and step % 10 == 0:
            print(f"  Step {step:4d}: loss = {loss:.6f}")

        # Estimate gradient (SPSA or parameter-shift)
        if hasattr(optimizer, "estimate_grad"):
            grad = optimizer.estimate_grad(loss_fn, params)
        else:
            # Numerical gradient
            grad = np.zeros_like(params)
            eps = 1e-5
            for i in range(len(params)):
                params_plus = params.copy()
                params_plus[i] += eps
                params_minus = params.copy()
                params_minus[i] -= eps
                grad[i] = (loss_fn(params_plus) - loss_fn(params_minus)) / (2 * eps)

        params = optimizer.step(params, grad)

    return TrainResult(
        params=params,
        loss_history=loss_history,
        final_loss=loss_history[-1] if loss_history else float("inf"),
        n_steps=len(loss_history),
    )
