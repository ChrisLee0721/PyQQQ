"""Search an unsorted database / 搜索无序数据库

Find a specific item in an unsorted list. Classical: O(N) queries. Quantum: O(√N) queries.
在无序列表中找到特定项。经典：O(N) 次查询。量子：O(√N) 次查询。

## Application / 应用场景
- Database search (数据库搜索)
- Cryptography: searching key space (密码学：搜索密钥空间)
- Optimization: finding optimal solution (优化：寻找最优解)
- SAT solving (SAT 求解)

## How it works / 原理
Oracle marks target state, diffusion amplifies its probability.
Oracle 标记目标态，diffusion 放大概率。

## Output / 输出说明
Target state appears with ~99% probability after optimal iterations.
目标态在最优迭代后以 ~99% 概率出现。

## Classical vs Quantum / 经典 vs 量子
For N=4: classical needs 3 queries, quantum needs 1.
对于 N=4：经典需要 3 次查询，量子需要 1 次。
"""


from quonic.algorithms import grover

result = grover("11", 2, shots=1024)
print(result.counts)
