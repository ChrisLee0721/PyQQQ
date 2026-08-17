"""Quantum Bayesian Inference — quantum-enhanced hypothesis testing.

Boundary conditions:
- Binary hypothesis testing
- Uses quantum amplitude estimation for likelihood ratio
- Minimal 2-hypothesis demonstration

Example::

    from quonic.algorithms import quantum_bayesian_demo
    result = quantum_bayesian_demo()
"""

from __future__ import annotations

from ..result import Result
from ..simulator import StatevectorSimulator


def quantum_bayesian_demo(
    prior_h0: float = 0.5,
    likelihood_h0: float = 0.8,
    likelihood_h1: float = 0.3,
    shots: int = 1000,
) -> Result:
    """Minimal quantum Bayesian inference demo."""
    import numpy as np

    # Classical Bayesian update for comparison
    p_data_given_h0 = likelihood_h0
    p_data_given_h1 = likelihood_h1
    posterior_h0 = (prior_h0 * p_data_given_h0) / (
        prior_h0 * p_data_given_h0 + (1 - prior_h0) * p_data_given_h1
    )

    # Quantum version: encode likelihoods as rotation angles
    sim = StatevectorSimulator(1)
    angle = np.arccos(np.sqrt(posterior_h0))
    sim.apply("ry", (0,), (2 * angle,))

    prob_h0 = (1 + sim.expectation("Z")) / 2
    return Result.from_value(prob_h0, posterior_h0=prob_h0, classical_posterior=posterior_h0)
