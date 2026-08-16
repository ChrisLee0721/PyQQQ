# QuoNic 演示视频脚本 —《3 行代码，一键切换三个量子后端》

> 目标：30–45 秒短视频。核心卖点只有一个——**同一段代码，改一个参数，跑在 Qiskit / Cirq / PennyLane 三个后端上**。
>
> 画幅 9:16（竖屏，适配手机 / 短视频平台）或 16:9（B 站 / YouTube）。下面按「分镜 + 旁白 + 画面」给出。

---

## 分镜 1｜痛点钩子（0–6 秒）

**画面**：屏幕上快速滚动一堆 Qiskit / Cirq 官方示例代码，满屏 `QuantumCircuit`、`backend`、`transpile`、`measure_all`，文字被划掉。

**旁白**：
> 「想跑一个量子程序？先得学 8 个新概念、写 12 行代码——换一个框架，还得全部重写。这合理吗？」

**字幕（大字）**：量子编程，为什么这么难？

---

## 分镜 2｜三行代码（6–16 秒）

**画面**：终端 / Jupyter，逐行敲入：

```python
from quonic import qgate, qshow
from quonic.gates import H, CX

qgate(H, 0)
qgate(CX, 0, 1)
qshow()
```

**旁白**：
> 「QuoNic 把它简化成 3 行。你不需要懂量子电路，只需要两个词——`qgate` 加门，`qshow` 看结果。」

**字幕**：贝尔态，3 行搞定。

---

## 分镜 3｜一键切换（16–34 秒）—— 全片高潮

**画面**：同一段代码不动，只改 `qshow` 里的一个参数，连续跑三次：

```python
qshow(backend='qiskit')    # 第一次
qshow(backend='cirq')      # 第二次，改一个词
qshow(backend='pennylane') # 第三次，再改一个词
```

三次输出并排显示，都是 `{'00': ~50%, '11': ~50%}`，完全一致。

**旁白**：
> 「重点来了：从 Qiskit 切到 Cirq，再切到 PennyLane——不改代码，只改一个参数。三种后端，输出完全一致。一键切换，就是这么简单。」

**字幕**：一个参数 = 三个后端。

---

## 分镜 4｜收尾 CTA（34–42 秒）

**画面**：项目 logo + GitHub 链接 + 「pip install quonic」。

**旁白**：
> 「QuoNic，量子编程像写 Python 一样简单。GitHub 搜索 QuoNic，或者 pip install quonic，现在就试试。」

**字幕**：pip install quonic

---

## 拍摄 / 录制清单

| 事项 | 说明 |
|------|------|
| 录屏工具 | OBS Studio / 系统自带录屏 |
| 代码环境 | 提前装好 `quonic[qiskit,cirq,pennylane]`，三个后端都已验证通过 |
| 演示脚本 | 直接用 `docs/quickstart.md` 的贝尔态示例，不用临时改代码 |
| 字幕 | 用剪映 / CapCut 自动识别 + 手动校对 |
| BGM | 轻快、无版权，音量低于人声 |

## 一句话口播（备选）

> 「量子编程要学一堆新概念？不。QuoNic 让你 3 行代码跑通贝尔态，改一个参数切换三个后端。pip install quonic。」
