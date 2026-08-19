"""Quantum Fourier Transform.

The quantum analogue of the discrete Fourier transform.
Output: QFT of the input state.
"""

from quonic.algorithms import qft

result = qft(n_qubits=3, shots=1024)
print(result.counts)
