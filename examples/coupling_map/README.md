# CouplingMap 耦合图与 SWAP 路由

CX(0,2) 无法直接放在 3 比特链（0-1-2）上，compile() 抛 RoutingError；route_swaps() 插入 SWAP 修复。

CX(0,2) cannot be placed directly on a 3-qubit line (0-1-2); compile() raises RoutingError, and route_swaps() inserts SWAPs to fix it.

## 运行 Run

```bash
python examples/coupling_map/coupling_map.py
```

## 预期输出 Expected output

先打印 RoutingError（预期），再打印路由后的门序列 swap(0,1)、cx(1,2)。

It prints RoutingError (expected), then the routed sequence swap(0,1), cx(1,2).
