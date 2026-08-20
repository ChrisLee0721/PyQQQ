"""Pulse-level differentiation for quantum circuits.

Computes gradients with respect to pulse parameters (amplitude, duration, phase)
rather than gate parameters. This enables optimization at the pulse level.

Example::

    from quonic.ml.pulse_grad import pulse_gradient

    grad = pulse_gradient(pulse_params, target_unitary, n_qubits)
"""

from __future__ import annotations

import numpy as np


def pulse_gradient(
    pulse_params: np.ndarray,
    target: np.ndarray,
    n_qubits: int,
    dt: float = 1.0,
    sigma: float = 0.01,
) -> np.ndarray:
    """Compute gradient of pulse parameters w.r.t. gate fidelity.

    Uses parameter-shift rule adapted for pulse-level control:
    ∂F/∂p_i = [F(p + π/2·e_i) - F(p - π/2·e_i)] / 2

    Args:
        pulse_params: pulse amplitude parameters (n_steps, 2) for [u_x, u_y]
        target: target unitary matrix
        n_qubits: number of qubits
        dt: time step duration
        sigma: perturbation magnitude

    Returns:
        Gradient vector of shape (n_steps * 2,).
    """
    len(pulse_params) // 2 if len(pulse_params.shape) == 1 else pulse_params.shape[0]
    params_flat = pulse_params.flatten()
    grad = np.zeros_like(params_flat)

    for i in range(len(params_flat)):
        params_plus = params_flat.copy()
        params_plus[i] += np.pi / 2
        params_minus = params_flat.copy()
        params_minus[i] -= np.pi / 2

        fid_plus = _pulse_fidelity(params_plus.reshape(-1, 2), target, dt)
        fid_minus = _pulse_fidelity(params_minus.reshape(-1, 2), target, dt)

        grad[i] = (fid_plus - fid_minus) / 2

    return grad.reshape(pulse_params.shape)


def _pulse_fidelity(
    pulse_params: np.ndarray,
    target: np.ndarray,
    dt: float,
) -> float:
    """Compute fidelity between pulse-evolved unitary and target.

    Args:
        pulse_params: pulse amplitudes (n_steps, 2)
        target: target unitary
        dt: time step

    Returns:
        Fidelity value between 0 and 1.
    """
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)

    # Build unitary from pulse
    U = np.eye(2, dtype=complex)
    for k in range(len(pulse_params)):
        H_k = pulse_params[k, 0] * X + pulse_params[k, 1] * Y
        U_k = _expm_i(H_k * dt)
        U = U_k @ U

    # Fidelity: |Tr(U†_target @ U)|^2 / 4
    overlap = np.trace(target.conj().T @ U)
    return float(np.abs(overlap) ** 2 / 4)


def _expm_i(H: np.ndarray) -> np.ndarray:
    """Compute exp(-iH) for a 2x2 Hermitian matrix."""
    eigvals, eigvecs = np.linalg.eigh(H)
    return eigvecs @ np.diag(np.exp(-1j * eigvals)) @ eigvecs.conj().T


def pulse_fisher_information(
    pulse_params: np.ndarray,
    target: np.ndarray,
    dt: float = 1.0,
    n_samples: int = 100,
    sigma: float = 0.01,
) -> np.ndarray:
    """Estimate quantum Fisher information matrix for pulse parameters.

    This enables natural gradient optimization at the pulse level.

    Args:
        pulse_params: pulse parameters
        target: target unitary
        dt: time step
        n_samples: number of samples
        sigma: perturbation magnitude

    Returns:
        Fisher information matrix.
    """
    rng = np.random.RandomState(42)
    n_params = pulse_params.size
    fisher = np.zeros((n_params, n_params))

    for _ in range(n_samples):
        delta = rng.choice([-1, 1], size=n_params)
        pulse_params.flatten() + sigma * delta
        pulse_params.flatten() - sigma * delta

        # Compute state derivatives
        for i in range(n_params):
            ei = np.zeros(n_params)
            ei[i] = sigma
            p_plus = pulse_params.flatten() + ei
            p_minus = pulse_params.flatten() - ei
            f_plus = _pulse_fidelity(p_plus.reshape(-1, 2), target, dt)
            f_minus = _pulse_fidelity(p_minus.reshape(-1, 2), target, dt)
            df_i = (f_plus - f_minus) / (2 * sigma)

            for j in range(i, n_params):
                ej = np.zeros(n_params)
                ej[j] = sigma
                p_plus = pulse_params.flatten() + ej
                p_minus = pulse_params.flatten() - ej
                f_plus = _pulse_fidelity(p_plus.reshape(-1, 2), target, dt)
                f_minus = _pulse_fidelity(p_minus.reshape(-1, 2), target, dt)
                df_j = (f_plus - f_minus) / (2 * sigma)

                fisher[i, j] += df_i * df_j
                fisher[j, i] = fisher[i, j]

    fisher /= n_samples
    fisher += 1e-4 * np.eye(n_params)  # regularization
    return fisher
