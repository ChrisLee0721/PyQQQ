"""BB84 Quantum Key Distribution protocol simulation.

Simulates the BB84 protocol classically: Alice prepares random bits in random
bases, Bob measures in random bases, they keep only matching-basis bits.

Boundary conditions:
- Fully classical simulation (no quantum circuit needed)
- Demonstrates the key distribution concept
- Eve (eavesdropper) can be optionally introduced
- Key rate ≈ 50% (matching bases) × 100% (no Eve)

Example::

    from quonic.algorithms import bb84
    result = bb84(n_bits=100)
    print(result["key"])  # shared secret key
"""

from __future__ import annotations

import random

from ..result import Result


def bb84(
    n_bits: int = 100,
    eve: bool = False,
) -> Result:
    """Simulate BB84 QKD protocol.

    Args:
        n_bits: Number of bits to exchange.
        eve: If True, introduce eavesdropper (50% error rate on intercepted bits).

    Returns:
        Result with shared key and statistics.
    """
    # Alice's random bits and bases
    alice_bits = [random.randint(0, 1) for _ in range(n_bits)]
    alice_bases = [random.randint(0, 1) for _ in range(n_bits)]  # 0=Z, 1=X

    # Bob's random bases
    bob_bases = [random.randint(0, 1) for _ in range(n_bits)]

    # Transmission (with optional Eve)
    received_bits = list(alice_bits)
    if eve:
        # Eve intercepts: measures in random basis, re-prepares
        eve_bases = [random.randint(0, 1) for _ in range(n_bits)]
        for i in range(n_bits):
            if eve_bases[i] != alice_bases[i]:
                # Wrong basis → 50% error
                received_bits[i] = random.randint(0, 1)

    # Bob measures
    bob_bits = []
    for i in range(n_bits):
        if bob_bases[i] == alice_bases[i]:
            # Same basis → correct measurement
            bob_bits.append(received_bits[i])
        else:
            # Different basis → random result
            bob_bits.append(random.randint(0, 1))

    # Sifting: keep only matching-basis bits
    key_alice = []
    key_bob = []
    for i in range(n_bits):
        if alice_bases[i] == bob_bases[i]:
            key_alice.append(alice_bits[i])
            key_bob.append(bob_bits[i])

    # Error rate
    errors = sum(1 for a, b in zip(key_alice, key_bob) if a != b)
    error_rate = errors / len(key_alice) if key_alice else 0

    key = "".join(str(b) for b in key_alice)
    return Result.from_value(
        float(len(key)),
        key=key,
        key_length=len(key),
        error_rate=error_rate,
        sift_ratio=len(key_alice) / n_bits,
    )
