# schedule 调度器

circuit_features() 汇总电路特征（规模、深度、是否为 Clifford、树宽），schedule() 据此给出后端 + 模拟方法的推荐。

circuit_features() summarizes a circuit (size, depth, Clifford-ness, treewidth); schedule() turns that into a backend + method recommendation.

## 运行 Run

```bash
python examples/schedule/schedule.py
```

## 预期输出 Expected output

打印电路特征，再打印 backend 与 method 的推荐。

It prints the circuit features, then the recommended backend and method.
