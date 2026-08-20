# Quantum Teleportation

量子隐形传态协议演示。

## 原理

1. Alice 和 Bob 共享 Bell 对
2. Alice 对她的量子比特做 CNOT + H 操作
3. Alice 测量并把结果发给 Bob
4. Bob 根据测量结果做修正操作

## 运行

```bash
python examples/teleportation/teleportation.py
```
