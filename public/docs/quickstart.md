# QuoNic 快速入门

5 分钟上手：三个核心概念，三个示例。

## 三个核心概念

| 概念 | 作用 |
|------|------|
| **`qgate(gate, *qubits)`** | 向电路添加一个门。门对象从 `quonic.gates` 导入（推荐），也支持字符串（如 `qgate("h", 0)`） |
| **`qshow()`** | 运行当前电路并显示结果。没写 `measure` 的量子比特会被自动测量；运行后自动清空电路 |
| **`qif(control).then(...).else_(...)`** | 量子叠加 if：不测量控制比特，两分支相干叠加；经典分支用 `cif` / `cwhile`（中段测量反馈） |

## 示例一：贝尔态（Bell State）

```python
from quonic import qgate, qshow
from quonic.gates import H, CX

qgate(H, 0)
qgate(CX, 0, 1)
qshow()
```

输出约 50% 的 `|00>` 和 50% 的 `|11>`。

## 示例二：GHZ 态

```python
from quonic import qgate, qshow
from quonic.gates import H, CX

qgate(H, 0)
qgate(CX, 0, 1)
qgate(CX, 1, 2)
qshow()
```

输出约 50% 的 `|000>` 和 50% 的 `|111>`。

## 示例三：量子叠加 if（`qif`）

```python
from quonic import qgate, qif, qshow
from quonic.gates import H, X, I

qgate(H, 0)                       # 控制比特进入叠加态 (|0>+|1>)/√2
qif(0).then(X, 1).else_(I, 1)     # q0==1 翻转 q1，否则不动
qshow()
```

输出约 50% 的 `|00>` 和 50% 的 `|11>`——与贝尔态电路等价，但用 `if/else` 的
直觉写出来。关键在于：控制比特**不被测量**，两个分支相干叠加，产生的是真纠缠
态，而不是「先测量再二选一」的经典混合态。

`else_` 分支可以是任何单比特门（如 `Z`），`I` 是恒等门，让「受控门 = qif 特例」
写得自然：

```python
qif(0).then(X, 1).else_(I, 1)   # 等价于受控 X（CNOT）
```

> 说明：经典控制（先测量、再按结果二选一）用 `cif`（经典 if）或 `cwhile`（经典 while）实现，
> 属于「坍缩之后的经典分支」，与 `qif` 的相干叠加被严格区分，不会混为一谈。

## 进阶：三个算法模板

QuoNic 内置三个开箱即用的算法模板，只需填空即可运行。使用前安装依赖：

```bash
pip install 'quonic[algorithms]'
```

### 模板一：Grover 搜索

搜索一个计算基态，直接传比特串即可（`mark_state` 自动生成神谕）：

```python
from quonic.algorithms import grover

result = grover("11", 2, shots=1024)   # 在 2 比特中搜索 |11>
print(result.counts)  # {'11': ~1024}
```

如果要标记更复杂的状态，用 `mark_state` 显式生成神谕（它也支持 `0` 位，如 `mark_state("10")` 标记 `|10>`），或自己写 `oracle(circuit)` 回调。

### 模板二：VQE 求基态能量

给出用泡利项表示的哈密顿量，即可变分求解基态能量：

```python
from quonic.algorithms import vqe

# H = Z⊗Z + X⊗I + I⊗X，基态能量 = -√5 ≈ -2.236
hamiltonian = [(1.0, "ZZ"), (1.0, "XI"), (1.0, "IX")]
result = vqe(hamiltonian, 2)
print(result.value)  # ≈ -2.236
```

> **哈密顿量从哪来？** QuoNic 不内置化学数据库。分子的电子结构哈密顿量需用 Qiskit Nature 或 OpenFermion 自行生成，再用 `from_qiskit_nature(qubit_op)` 一键转成上面的 `[(系数, 泡利串)]` 格式。

### 模板三：QAOA 求解 MaxCut

给出无向图的边列表，QAOA 自动变分求最大割：

```python
from quonic.algorithms import qaoa_maxcut

edges = [(0, 1), (1, 2), (0, 2)]  # 三角形图
result = qaoa_maxcut(edges, 3)
print(result.value)  # ≈ 2.0（三角形最大割）
```

> **图从哪来？** 你需要把实际问题（物流、社交网络、排班等）先建模成图：顶点 = 对象，边 = 关系。QuoNic 只负责「给定图，求最大割」这一步。

## 关于后端与真实硬件

`qshow()` 默认用 Qiskit，可用 `qshow(backend='cirq')` 或 `qshow(backend='pennylane')` 一键切换，同一段代码跑在不同后端上，输出一致。

真实硬件走 Quantum Inspire（`qi` 后端），并提供设备捷径：

```python
qshow(backend='qx')      # QX emulator（云端模拟器，提交前验证）
qshow(backend='tuna9')   # Tuna-9 超导真机（9 qubit）
qshow(backend='tuna17')  # Tuna-17 超导真机（17 qubit）
```

> **注意**：真机需一次性安装并登录：
> `pip install 'quonic[quantum-inspire]'` 然后 `qi login`（token 存于
> `~/.quantuminspire/config.json`，勿手写贴出）。真机不支持注入 `noise=`，
> `cif` / `cwhile` 需在支持中段测量反馈的模拟器（qiskit / native）上跑。

## 更多示例

以上示例（以及 GHZ、`qif`、`QInt`、噪声等）都在 [`examples/`](../examples/) 目录里，每个案例一个文件夹（英文代码 + 中英双语 README），直接 `python examples/bell/bell.py` 复制即跑。
