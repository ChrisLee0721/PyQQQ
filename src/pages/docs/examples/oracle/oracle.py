"""Oracle construction / 预言机构造

Oracle construction / 预言机构造

## Application / 应用场景
- Quantum computing (量子计算)
- Algorithm demonstration (算法演示)
- Educational (教学)

## Output / 输出
See code comments for output explanation.
参见代码注释了解输出说明。"""

from quonic.algorithms import grover, oracle


@oracle(3)
def is_five(x):
    return x == 5


result = grover(is_five, 3, shots=1024)
print(result.counts)  # dominated by |101>
