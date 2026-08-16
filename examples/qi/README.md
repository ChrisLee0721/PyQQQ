# 真实硬件：Quantum Inspire 超导真机（Tuna-9）

把贝尔态 `|00> + |11>` 提交到 Quantum Inspire 的 9 量子比特超导真机。

Runs a Bell state on Quantum Inspire's 9-qubit superconducting hardware.

## 前置条件 Prerequisites

1. 安装依赖（注意 qiskit 版本约束，建议用独立虚拟环境）：

   ```bash
   pip install 'quonic[quantum-inspire]'
   # 等价于： pip install 'qiskit-quantuminspire>=0.18' 'quantuminspire>=4.0' 'qiskit<2.4.0'
   ```

   `qiskit-quantuminspire` 0.18.x 要求 `qiskit<2.4.0`；若环境里已装 2.5.x，
   需临时降级 `qiskit==2.3.1`（qiskit-aer 无版本上界，不受影响）。

2. 登录（OAuth 设备流，浏览器授权一次即可）：

   ```bash
   qi login
   ```

   token 存于 `~/.quantuminspire/config.json`，请勿手写或贴出。

## 当前可用的 backend Available backends

| 名字 | 量子比特 | 类型 |
|------|---------|------|
| QX emulator | 10 | 模拟器 |
| Ry emulator | 9 | 模拟器 |
| Tuna-9 | 9 | 真机（默认） |
| Tuna-17 | 17 | 真机 |

（Starmon-5 已下线，由 Tuna 系列接替。）

## 先用 QX emulator 验证 Validate on the emulator first

真机提交会消耗机时，建议先用云端模拟器跑通「编译 → 提交 → 取回计数」链路：

```python
from quonic import qgate, reset
from quonic.gates import H, CX
from quonic.stack import current_circuit
from quonic.backends.qi import QuantumInspireBackend

qgate(H, 0)
qgate(CX, 0, 1)
result = QuantumInspireBackend("QX emulator").run(current_circuit(), shots=1024)
print(result.counts)
```

## 真机运行 Run on hardware

```bash
python examples/qi/qi.py
```

## 预期输出 Expected output

约一半样本 `|00>`、一半 `|11>`（真机有读取/门噪声，会出现少量 `|01>`/`|10>`）：

Roughly half the samples are `|00>` and half `|11>`; real hardware adds
readout/gate noise, so a few `|01>`/`|10>` also appear.

## 限制 Limitations

- 仅支持静态电路（门 + 末端测量）；`cif` / `cwhile`（中段测量反馈）在
  超导真机上不可用，会抛 `NotImplementedError`。
- 真实硬件无法注入去极化 `noise`，传 `noise=` 会抛 `ValueError`。
- 超过设备量子比特数或非本机拓扑的连线，由 `transpile` 自动 SWAP 路由。
