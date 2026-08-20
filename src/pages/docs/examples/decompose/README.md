# decompose 门分解

把 Toffoli（CCX）展开成基础门集（单比特门 + CX），无需辅助比特。

Expand a Toffoli (CCX) into the basic gate set (single-qubit gates + CX), no ancilla needed.

## 运行 Run

```bash
python examples/decompose/decompose.py
```

## 预期输出 Expected output

打印 15 个基础门的名字（h / cx / p ...）。

It prints the names of 15 basic gates (h / cx / p ...).
