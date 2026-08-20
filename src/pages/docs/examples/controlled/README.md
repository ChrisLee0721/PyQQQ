# Controlled gate 通用受控门

controlled(Ry(0.7), 0, 1) 对目标比特施加受控单比特门，经 ZYZ 分解成基础门，
实现 |0><0|⊗I + |1><1|⊗Ry。controlled(X, 0, 1) 即 CNOT。

controlled(Ry(0.7), 0, 1) applies a controlled single-qubit gate, compiled to
basic gates via ZYZ, realizing |0><0|⊗I + |1><1|⊗Ry. controlled(X, 0, 1) is CNOT.

## 运行 Run

```bash
python examples/controlled/controlled.py
```

## 预期输出 Expected output

控制比特 |+>，目标经受控 Ry(0.7) 旋转：约 50% |00>，其余按旋转角分摊到
|10> 与 |11>。

Control in |+>, target under controlled Ry(0.7): roughly 50% |00>, the rest
split between |10> and |11> by the rotation angle.
