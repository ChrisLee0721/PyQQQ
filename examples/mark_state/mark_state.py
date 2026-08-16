"""mark_state: build an oracle callback that marks one basis state.

Search for |10> (qubit 0 = 0, qubit 1 = 1) among 2 qubits.
"""

from quonic.algorithms import grover, mark_state

result = grover(mark_state("10"), 2, shots=1024)
print(result.counts)  # dominated by |10>
