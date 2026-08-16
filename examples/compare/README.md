# 比较器 qlt / qeq / qgt 与乘法 mul

比较器用量子寄存器与经典常数比较，返回一个标志比特（条件成立时为 1），寄存器
x 保持不变：

The comparator compares a quantum register against a classical constant and
returns a flag qubit (1 when the condition holds), leaving x unchanged:

```python
x = QInt(3, value=5)
lt = qlt(x, 4)   # 5 < 4? 否 -> 0
eq = qeq(x, 5)   # 5 == 5 -> 1
gt = qgt(x, 5)   # 5 > 5? 否 -> 0
```

- `qeq` 精确：用 `x - k mod 2^n` 是否为零判断。
- `qlt` 用 n+1 位补码：`x - k` 的符号位指示 `x < k`。
- `qgt` = `NOT qlt(k+1)`（即 `x > k ⟺ x >= k+1`）。

- `qeq` is exact: it checks whether `x - k mod 2^n` is zero.
- `qlt` uses (n+1)-bit two's complement: the sign bit of `x - k` marks `x < k`.
- `qgt` = `NOT qlt(k+1)` (since `x > k ⟺ x >= k+1`).

`mul(x, k)` 返回一个新 QInt，值为 `|x * k mod 2^n>`，x 保持不变（就地乘法只有
奇数 k 才可逆，所以乘法统一走结果寄存器）：

`mul(x, k)` returns a new QInt holding `|x * k mod 2^n>`, leaving x unchanged
(in-place multiply is only reversible for odd k, so multiply always uses a
fresh result register):

```python
x = QInt(3, value=5)
p = mul(x, 3)    # |5 * 3 mod 8> = |7>
```

## 运行 Run

```bash
python examples/compare/compare.py
```

## 预期输出 Expected output

均匀叠加 |0..7> 与 4 比较：约一半样本 flag=1（对应 x<4），一半 flag=0（x>=4）。
标志比特是最左边的量子比特（qubit 下标 n+1 = 4）。

A uniform |0..7> compared against 4: roughly half the samples have flag=1
(those with x<4) and half flag=0 (x>=4). The flag is the leftmost qubit
(qubit index n+1 = 4).
