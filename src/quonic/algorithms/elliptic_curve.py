"""Elliptic Curve Discrete Logarithm — minimal demo.

Boundary conditions:
- Minimal: small curve over small field
- Classical brute-force (quantum would use Shor variant)
- Demonstrates the concept only

Example::

    from quonic.algorithms import elliptic_curve_demo
    result = elliptic_curve_demo()
"""

from __future__ import annotations

from ..result import Result


def elliptic_curve_demo() -> Result:
    """Minimal elliptic curve DLP demo.

    Curve: y^2 = x^3 + ax + b (mod p)
    Find k such that k*P = Q
    """
    # Curve parameters: y^2 = x^3 + 2x + 3 (mod 97)
    p = 97
    a, b = 2, 3

    # Points on curve (precomputed)
    P = (3, 6)
    Q = (80, 10)  # 5*P

    # Brute-force DLP
    current = P
    for k in range(1, p):
        if current == Q:
            return Result.from_value(float(k), k=k, P=P, Q=Q, curve=f"y^2=x^3+{a}x+{b} mod {p}")
        # Point addition (simplified)
        # In real implementation, use proper elliptic curve arithmetic
        current = ((current[0] + P[0]) % p, (current[1] + P[1]) % p)

    return Result.from_value(-1.0, error="DLP not found")
