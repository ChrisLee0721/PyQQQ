# PyQQQ 快速入门

5 分钟上手：三个核心概念，三个示例。

## 三个核心概念

| 概念 | 作用 |
|------|------|
| **`qgate(gate, *qubits)`** | 向电路添加一个门。门对象从 `pyqqq.gates` 导入（推荐），也支持字符串（如 `qgate("h", 0)`） |
| **`qshow()`** | 运行当前电路并显示结果。没写 `measure` 的量子比特会被自动测量；运行后自动清空电路 |
| **`if`** | 条件门（经典控制）与量子叠加控制（"if = 叠加态"）均在规划中，尚未实现 |

## 示例一：贝尔态（Bell State）

```python
from pyqqq import qgate, qshow
from pyqqq.gates import H, CX

qgate(H, 0)
qgate(CX, 0, 1)
qshow()
```

输出约 50% 的 `|00>` 和 50% 的 `|11>`。

## 示例二：GHZ 态

```python
from pyqqq import qgate, qshow
from pyqqq.gates import H, CX

qgate(H, 0)
qgate(CX, 0, 1)
qgate(CX, 1, 2)
qshow()
```

输出约 50% 的 `|000>` 和 50% 的 `|111>`。

## 示例三：单层 if（规划中）

```python
from pyqqq import qgate, qshow
from pyqqq.gates import H, X, Z, MEASURE

qgate(H, 0)
qgate(MEASURE, 0)
# 规划中：基于测量结果的条件门（经典控制）
# if qgate(MEASURE, 0) == 0:
#     qgate(X, 1)
# else:
#     qgate(Z, 1)
qshow()
```

> 说明：上面的 `if` 是"先测量、再按结果分支"的**经典控制**，属于"坍缩之后的经典分支"；
> 而"if = 叠加态"（两种分支同时发生）是 PyQQQ 的长期方向，需要自研条件编译器，暂未实现。
> 两者会被明确区分，不会把经典分支包装成叠加态。
