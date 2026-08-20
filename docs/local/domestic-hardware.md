# 国产硬件后端调研

为 QuoNic 后端抽象层（`quonic/backends/`）接入国产量子计算软件栈的可行性调研。
结论基于公开文档与 PyPI 元数据（2026-08），未做实机验证。

## 候选一：QPanda3（本源量子）— 可行

- **包名**：`pyqpanda3`（`pip install pyqpanda3`）；QPanda2 已弃用。
- **许可证**：Apache-2.0。**版本**：v0.3.4（0.x，API 可能变动），持续维护。
- **平台**：官方称支持 Windows/macOS/Linux；`pyqpanda3` 的 Windows wheel 未完全确认（旧 `pyqpanda` 有 Windows wheel）。

后端适配器需要用到的核心 API：

```python
from pyqpanda3.core import QProg, CPUQVM, H, X, Y, Z, RX, RY, RZ, CNOT, CZ, CCX, SWAP, measure

qvm = CPUQVM()                      # 本地模拟器
qvm.run(prog, shots)                # 运行
counts = qvm.result().get_counts()  # dict[str, int]
```

云真机（悟源 Wuyuan / 悟空 Wukong 芯片）：

```python
from pyqpanda3.qcloud import QCloudService
svc = QCloudService(api_key)        # api_key 从环境变量读，勿硬编码
svc.backend("WK_C180")              # 选择芯片
```

## 候选二：CqLib（中电信量子 + 国盾量子）— 部分可行

> **正名**：CqLib 不是北京量子院（BAQIS）的项目。PyPI 上的 `cqlib` 由
> **中电信量子 + 国盾量子** 维护，基于国产 QCIS 指令集，对接「天衍」云平台。
> BAQIS 运营的是 Quafu 云 + 中性原子编译器 ZAP，与 CqLib 无关。

- **包名**：`cqlib`（`pip install cqlib`，可选 `cqlib[simple-sim]`）。
- **许可证**：Apache-2.0。**Python**：3.10+，Windows 确认支持。
- **维护**：`tianyan_quantum`，gitee 托管，近期活跃。

后端适配器需要用到的核心 API：

```python
from cqlib import Circuit
from cqlib.simulator import StatevectorSimulator

c = Circuit(2); c.h(0); c.x(1); c.measure_all()
sim = StatevectorSimulator(); probs = sim.probs()   # 概率，计数 API 未明确
```

云真机：`TianYanPlatform` 登录 → `download_config` → `run_task(...)` → `task_id`。

## 结论与接入建议

| 候选 | 结论 | 一句话理由 |
|------|------|-----------|
| QPanda3 | **可行（优先）** | 门集全、有本地模拟器 + 云真机，API 直白；但 0.x API 会变、无 `P` 相位门（用 `RZ`/`U1` 代） |
| CqLib | **部分可行** | 面向 QCIS 指令集、计数 API 不清晰；更偏编译工具而非通用后端 |

**接入位置**：两者都只需在 `quonic/backends/` 新增一个 `Backend` 子类，
复用现有 `_apply` 模式（参考 `backends/cirq.py` 的门映射），把 QuoNic 的
`h/x/y/z/rx/ry/rz/cx/cz/ccx/swap` 映射到目标框架即可；`mcz`/`cif`/`cwhile`
在国产硬件上同样受「无中段测量反馈」约束，需显式降级。

**风险提示**：两家均为 0.x/1.x 早期生态，API 与 wheel 可用性漂移快；
接入前建议先在新虚拟环境验证 `pip install` + 最小跑通，再落地成正式后端。

## 参考资料

- [pyqpanda3 快速上手](https://qcloud.originqc.com.cn/document/pyqpanda3-docs/en/tutorial/getting-started)
- [pyqpanda3 模拟器](https://qcloud.originqc.com.cn/document/pyqpanda3-docs/en/tutorial/simulation)
- [pyqpanda3 QCloudService API](https://qcloud.originqc.com.cn/document/pyqpanda3-docs/zh/api/qcloud/service)
- [CqLib 概览](https://qc.zdxlz.com/mkdocs/zh/cqlib/01-overview.html)
