"""Quantum GAN — minimal demo of quantum generative adversarial network.

Boundary conditions:
- Quantum generator + classical discriminator
- Minimal: 1-qubit generator
- NOT a production GAN — demonstrates the concept

Example::

    from quonic.algorithms import qgan_demo
    result = qgan_demo()
"""

from __future__ import annotations

from ..result import Result
from ..simulator import StatevectorSimulator


def qgan_demo(n_steps: int = 10) -> Result:
    """Minimal QGAN demo."""
    import numpy as np

    # Target distribution: P(0) = 0.3, P(1) = 0.7
    target = [0.3, 0.7]

    # Generator: Ry(theta)
    theta = 0.5
    losses = []

    for _ in range(n_steps):
        # Generate samples
        sim = StatevectorSimulator(1)
        sim.apply("ry", (0,), (theta,))
        p_gen = (1 + sim.expectation("Z")) / 2

        # Discriminator loss (simplified)
        loss = abs(p_gen - target[0])
        losses.append(loss)

        # Update generator
        theta += 0.1 * (target[0] - p_gen)

    return Result.from_value(float(np.mean(losses)), final_theta=theta)
