"""Quantum Teleportation — teleport a qubit state using entanglement and classical communication.

Demonstrates the teleportation protocol:
1. Create Bell pair between Alice (q1) and Bob (q2)
2. Alice applies CNOT + H on her qubits (q0, q1)
3. Alice measures q0 and q1
4. Bob applies corrections based on Alice's measurement results

Usage:
    python examples/teleportation/teleportation.py
"""

import math

from quonic import qgate, qshow, reset
from quonic.gates import CX, CZ, H, Ry
from quonic.stack import current_circuit


def teleport():
    """Run quantum teleportation protocol."""
    # Prepare state to teleport: Ry(π/3)|0> on qubit 0
    qgate(Ry(math.pi / 3), 0)

    # Create Bell pair between q1 and q2
    qgate(H, 1)
    qgate(CX, 1, 2)

    # Alice's operations: CNOT(q0, q1) then H(q0)
    qgate(CX, 0, 1)
    qgate(H, 0)

    # Measure q0 and q1 (classical communication)
    # Bob applies corrections based on measurement results
    # For simplicity, we show the full circuit without mid-circuit measurement

    # Corrections (would be conditional in real implementation):
    # if q1 == 1: X(q2)
    # if q0 == 1: Z(q2)

    # For demo, apply both corrections (one will be identity)
    qgate(CX, 1, 2)
    qgate(CX, 0, 2)
    qgate(CZ, 0, 2)

    return current_circuit()


def main():
    reset()
    circuit = teleport()
    print("Quantum Teleportation:")
    print(f"  Circuit: {circuit.gate_count()} gates, {circuit.num_qubits} qubits")
    result = qshow()
    print(f"  Result: {result.counts}")


if __name__ == "__main__":
    main()
