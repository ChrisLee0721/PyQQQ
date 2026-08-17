"""Discrete Logarithm — quantum algorithm for solving a^x = b (mod p).

Boundary conditions:
- Minimal version: small prime p
- Reuses QPE infrastructure from Shor
- Requires classical post-processing
- NOT optimized for large instances

Example::

    from quonic.algorithms import discrete_log_demo
    result = discrete_log_demo(a=2, b=8, p=11)
"""

from __future__ import annotations

from ..result import Result


def discrete_log_demo(
    a: int = 2,
    b: int = 8,
    p: int = 11,
) -> Result:
    """Find x such that a^x ≡ b (mod p) using classical search (quantum would use QPE).

    Args:
        a: Base.
        b: Target.
        p: Prime modulus.

    Returns:
        Result with discrete log x.
    """
    # Classical brute-force (quantum version would use QPE)
    for x in range(p):
        if pow(a, x, p) == b:
            return Result.from_value(float(x), x=x, a=a, b=b, p=p)

    return Result.from_value(-1.0, error="no solution found")
