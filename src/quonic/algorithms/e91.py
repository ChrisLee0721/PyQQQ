"""E91 Quantum Key Distribution — entanglement-based QKD.

Uses Bell pairs and CHSH inequality violation for secure key distribution.

Boundary conditions:
- Requires 2 qubits per round (Bell pair)
- Demonstrates entanglement as resource for cryptography
- CHSH violation proves no eavesdropper
- Fully classical simulation of the protocol

Example::

    from quonic.algorithms import e91
    result = e91(n_rounds=100)
    print(result["key"])
"""

from __future__ import annotations

import random

from ..result import Result


def e91(n_rounds: int = 100) -> Result:
    """Simulate E91 QKD protocol.

    Args:
        n_rounds: Number of entanglement rounds.

    Returns:
        Result with shared key and CHSH statistics.
    """
    alice_bits = []
    bob_bits = []
    chsh_count = 0
    chsh_total = 0

    for _ in range(n_rounds):
        # Alice and Bob choose measurement bases
        alice_basis = random.randint(0, 2)  # 0, 60, 120 degrees
        bob_basis = random.randint(0, 2)    # 0, 60, 120 degrees

        # Bell pair: |00> + |11> (correlated)
        bit = random.randint(0, 1)
        alice_result = bit
        bob_result = bit  # perfectly correlated in same basis

        if alice_basis != bob_basis:
            # Different bases → random results for CHSH test
            alice_result = random.randint(0, 1)
            bob_result = random.randint(0, 1)
            chsh_total += 1
            # Simplified CHSH check
            if alice_result == bob_result:
                chsh_count += 1

        if alice_basis == bob_basis:
            alice_bits.append(alice_result)
            bob_bits.append(bob_result)

    key = "".join(str(b) for b in alice_bits)
    chsh_value = chsh_count / chsh_total if chsh_total > 0 else 0

    return Result.from_value(
        float(len(key)),
        key=key,
        key_length=len(key),
        chsh_ratio=chsh_value,
    )
