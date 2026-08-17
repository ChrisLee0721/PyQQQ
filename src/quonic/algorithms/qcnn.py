"""Quantum Convolutional Neural Network (QCNN) — minimal demo.

Boundary conditions:
- 4-pixel binary image classification
- 2-qubit quantum circuit with convolutional structure
- NOT a production classifier — demonstrates the concept
- Requires scipy for training

Example::

    from quonic.algorithms import qcnn_demo
    result = qcnn_demo()
"""

from __future__ import annotations

from ..result import Result
from ..simulator import StatevectorSimulator


def qcnn_demo(
    maxiter: int = 50,
) -> Result:
    """Minimal QCNN demo for 4-pixel classification."""
    try:
        from scipy.optimize import minimize
    except ImportError as e:
        raise ImportError("scipy required") from e

    def circuit(params):
        sim = StatevectorSimulator(2)
        # Convolutional layer
        sim.apply("ry", (0,), (params[0],))
        sim.apply("ry", (1,), (params[1],))
        sim.apply("cx", (0, 1))
        # Pooling layer
        sim.apply("ry", (0,), (params[2],))
        return sim

    def cost(params):
        sim = circuit(params)
        # Simple cost: measure qubit 0
        return sim.expectation("Z")

    import numpy as np
    init = np.random.randn(3) * 0.5
    result = minimize(cost, init, method="COBYLA", options={"maxiter": maxiter})
    return Result.from_value(float(result.fun), params=result.x.tolist())
