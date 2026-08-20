"""Mark state / 标记态

Mark state / 标记态"""

from quonic.algorithms import grover, mark_state

result = grover(mark_state("10"), 2, shots=1024)
print(result.counts)  # dominated by |10>
