"""@oracle: turn a classical predicate into a Grover phase oracle.

The predicate marks x == 5 (|101>); Grover search then amplifies that state.
"""

from quonic.algorithms import grover, oracle


@oracle(3)
def is_five(x):
    return x == 5


result = grover(is_five, 3, shots=1024)
print(result.counts)  # dominated by |101>
