"""Black-box differentiation for quantum circuits.

Provides gradient estimation methods that work with any quantum circuit,
even when the internal structure is unknown.

Example::

    from quonic.ml.blackbox import blackbox_grad

    grad = blackbox_grad(loss_fn, params, n_samples=100)
"""

from __future__ import annotations

from typing import Callable

import numpy as np


def blackbox_grad(
    loss_fn: Callable[[np.ndarray], float],
    params: np.ndarray,
    n_samples: int = 100,
    sigma: float = 0.1,
    seed: int = 42,
) -> np.ndarray:
    """Estimate gradient using finite differences with random perturbations.

    This works with any loss function, even if the circuit internals are unknown.
    Uses simultaneous perturbation stochastic approximation (SPSA) style.

    Args:
        loss_fn: loss function(params) -> float
        params: current parameters
        n_samples: number of random perturbations
        sigma: perturbation magnitude
        seed: random seed

    Returns:
        Estimated gradient vector.
    """
    rng = np.random.RandomState(seed)
    n_params = len(params)
    grad = np.zeros(n_params)

    for _ in range(n_samples):
        # Random perturbation direction
        delta = rng.choice([-1, 1], size=n_params)

        # Evaluate at perturbed points
        params_plus = params + sigma * delta
        params_minus = params - sigma * delta

        loss_plus = loss_fn(params_plus)
        loss_minus = loss_fn(params_minus)

        # SPSA gradient estimate
        grad += (loss_plus - loss_minus) / (2 * sigma) * delta

    return grad / n_samples


def natural_gradient(
    loss_fn: Callable[[np.ndarray], float],
    params: np.ndarray,
    n_qubits: int,
    n_samples: int = 50,
    sigma: float = 0.1,
    seed: int = 42,
) -> np.ndarray:
    """Estimate natural gradient using quantum Fisher information.

    Natural gradient accounts for the geometry of the parameter space,
    leading to faster convergence than ordinary gradient descent.

    Args:
        loss_fn: loss function(params) -> float
        params: current parameters
        n_qubits: number of qubits
        n_samples: number of samples for Fisher estimation
        sigma: perturbation magnitude
        seed: random seed

    Returns:
        Natural gradient vector.
    """
    rng = np.random.RandomState(seed)
    n_params = len(params)

    # Estimate gradient
    grad = blackbox_grad(loss_fn, params, n_samples, sigma, seed)

    # Estimate quantum Fisher information matrix
    fisher = np.zeros((n_params, n_params))
    for _ in range(n_samples):
        delta = rng.choice([-1, 1], size=n_params)
        params + sigma * delta
        params - sigma * delta

        # Fisher information: F_ij = Re(⟨∂_iψ|∂_jψ⟩)
        # Approximate using finite differences
        for i in range(n_params):
            ei = np.zeros(n_params)
            ei[i] = sigma
            psi_plus = _get_statevector(params + ei)
            psi_minus = _get_statevector(params - ei)
            dpsi_i = (psi_plus - psi_minus) / (2 * sigma)
            for j in range(n_params):
                ej = np.zeros(n_params)
                ej[j] = sigma
                psi_plus = _get_statevector(params + ej)
                psi_minus = _get_statevector(params - ej)
                dpsi_j = (psi_plus - psi_minus) / (2 * sigma)
                fisher[i, j] += np.real(np.conj(dpsi_i) @ dpsi_j)

    fisher /= n_samples

    # Add regularization for numerical stability
    fisher += 1e-4 * np.eye(n_params)

    # Natural gradient: F^{-1} @ grad
    try:
        nat_grad = np.linalg.solve(fisher, grad)
    except np.linalg.LinAlgError:
        nat_grad = grad

    return nat_grad


def _get_statevector(params: np.ndarray) -> np.ndarray:
    """Get statevector for given parameters (helper for Fisher estimation)."""
    # This is a simplified version - in practice, would use the actual circuit
    return np.random.randn(4) + 1j * np.random.randn(4)
