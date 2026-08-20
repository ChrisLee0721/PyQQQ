"""Oracle construction / 预言机构造

Oracle construction / 预言机构造"""

from quonic.algorithms import grover, oracle


@oracle(3)
def is_five(x):
    return x == 5


result = grover(is_five, 3, shots=1024)
print(result.counts)  # dominated by |101>
