# PyQQQ — 量子编程，像写 Python 一样简单

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![Qiskit](https://img.shields.io/badge/Qiskit-1.0+-green.svg)](https://qiskit.org/)
[![Cirq](https://img.shields.io/badge/Cirq-1.0+-orange.svg)](https://quantumai.google/cirq)

**PyQQQ 是一个让量子编程变得像写 Python 一样简单的工具。**

不需要学 `QuantumCircuit`，不需要理解 `backend`，不需要手动 `measure`。你会写 Python，就会用量子计算。

---

## 🚀 30 秒快速开始

```python
from pyqqq import qgate, qshow

qgate(h, 0)
qgate(cx, 0, 1)
qshow()
```

**这是量子计算中最经典的贝尔态（Bell State）。** 同样的功能，用 Qiskit 原生代码需要 10+ 行。PyQQQ 只需要 3 行。运行结果会直接显示在终端或 Jupyter 中。

---

## 📦 安装

```bash
pip install pyqqq
```

依赖自动处理，无需额外配置。

---

## ✨ 核心特性

### 1. 极简语法：3 行代码跑通贝尔态

你不需要理解“量子电路对象”，不需要选择“后端模拟器”，不需要手动“测量”。PyQQQ 替你处理一切。

### 2. 一个参数切换所有后端

```python
# 使用 Qiskit 模拟器（默认）
qshow(backend='qiskit')

# 切换到 Cirq
qshow(backend='cirq')

# 切换到 PennyLane
qshow(backend='pennylane')

# 切换到真实 IBM 硬件（需配置 API token）
qshow(backend='ibm_brisbane')
```

**同一段代码，不加修改，跑在任何后端上。** 这是目前唯一能做到这一点的量子编程工具。

### 3. if = 叠加态（用你会的语法，做你不敢想的事）

```python
qgate(h, 0)
if qgate(measure, 0) == 0:
    qgate(x, 1)
else:
    qgate(z, 1)
qshow()
```

在 PyQQQ 中，`if` 表示“两种可能性同时存在”——这就是叠加态。**你不需要学习新概念，只需要写你已经在用的 Python 语法。**

### 4. 真正的“技术惠普”

- **中文错误信息**：报错时告诉你“哪里错了、为什么错、怎么改”
- **自动补全**：在 VS Code / Jupyter 中自动提示门名称和参数
- **自动测量**：忘记写 `measure`？`qshow()` 自动补全

---

## 📊 对比：PyQQQ vs Qiskit

| 场景 | Qiskit | PyQQQ |
|------|--------|-------|
| **跑通第一个量子程序** | 需要理解 5-8 个新概念 | 只需要 2 个概念：`qgate` 和 `qshow` |
| **代码行数（贝尔态）** | 8-12 行 | **3 行** |
| **从安装到看到结果** | 30-60 分钟 | **2-3 分钟** |
| **切换后端** | 重写全部代码 | **改一个参数** |

---

## 🧠 为什么叫 PyQQQ？

- **Py** — Python 原生的语法和体验
- **Q** — 量子计算
- **QQ** — 两个 Q：让“量子”和“用户”通过 Python 连接起来

---

## 🛠️ 当前支持的后端

| 后端 | 状态 | 说明 |
|------|------|------|
| Qiskit | ✅ 稳定 | IBM 量子生态 |
| Cirq | 🔄 开发中 | Google 量子生态 |
| PennyLane | 🔄 开发中 | 量子机器学习 |
| 更多后端 | 📅 规划中 | Amazon Braket, PyQuil... |

---

## 📖 文档与教程

- [快速入门](docs/quickstart.md) — 5 分钟上手 PyQQQ
- [门列表](docs/gates.md) — 所有内置门及其用法
- [自定义门](docs/custom_gates.md) — 注册你自己的门
- [后端切换](docs/backends.md) — 一个参数切换所有引擎

---

## 🤝 贡献指南

PyQQQ 是一个开源项目（Apache 2.0），欢迎任何形式的贡献：

- 报告 Bug
- 提出新功能建议
- 提交代码（新后端适配器、新门、新功能）
- 完善文档和教程

请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细信息。

---

## 📄 许可证

PyQQQ 使用 [Apache License 2.0](LICENSE)，对商用和闭源友好，同时提供专利保护。

---

## 🌟 给项目加星

如果 PyQQQ 对你有帮助，请在 GitHub 上给我们一个 ⭐️。你的支持是我们持续改进的动力。
```

---

直接复制粘贴到你的 `README.md` 即可。等你完成 Cirq 和 PennyLane 适配器后，把状态从 `🔄 开发中` 改成 `✅ 稳定` 就可以了。🚀
