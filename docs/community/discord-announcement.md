# Discord 公告文案

## 频道结构建议

```
#general — 一般讨论
#help — 使用帮助
#showcase — 用户项目展示
#dev — 开发讨论
#announcements — 版本发布
#tutorials — 教程讨论
#algorithms — 算法讨论
```

---

## 版本发布公告（v0.8.0）

```
🚀 QuoNic v0.8.0 发布！

本次更新：
• 量子机器学习框架（ansatz/encoding/optimizer/loss/trainer）
• 量子纠错框架（7种纠错码 + 稳定子 + 解码器）
• 插件系统（自定义后端/优化pass/算法模板）
• 脉冲控制（Gaussian/DRAG/脉冲 + Rabi/T1/T2校准）
• 分布式量子计算（量子网络 + 远程纠缠门）
• 7个硬件后端骨架（IBM/AWS/Azure/IonQ/Rigetti/Xanadu/QuEra）
• 5个新example（teleportation/BB84/比特翻转/VQC/Trotter）
• 智能错误提示（"Did you mean..." fuzzy matching）
• 616 tests，19 后端

安装：
pip install 'quonic[all-sim]'

详情：https://github.com/ChrisLee0721/QuoNic/releases/tag/v0.8.0
```

---

## 新功能介绍帖

```
🔬 QuoNic 新功能：量子机器学习框架

从今天开始，你可以用 QuoNic 训练量子神经网络：

from quonic.ml import Ansatz, angle_encode, SPSAOptimizer, train

ansatz = Ansatz.hardware_efficient(n_qubits=4, layers=3)
opt = SPSAOptimizer(maxiter=100)
result = train(ansatz, opt, loss_fn=my_loss)

支持：
• 硬件高效 / QAOA / UCCSD ansatz
• 振幅 / 角度 / IQP 编码
• SPSA / Adam / QNG 优化器
• 期望值 / 保真度 / 交叉熵损失函数

示例：examples/vqc/vqc.py
文档：https://chrislee0721.github.io/QuoNic/
```

---

## 使用帮助帖

```
❓ 常见问题

Q: 如何切换后端？
A: qshow(backend='qulacs') — 一个参数搞定

Q: 如何用 GPU 加速？
A: qshow(method='gpu') — 自动选最优 GPU 后端

Q: 如何加噪声？
A: qshow(noise=0.05) — 5% 去极化噪声

Q: 如何用 ZNE 误差缓解？
A: result = zne(circuit, noise=0.05, target="1", shots=1024)

Q: 如何定义自定义门？
A: my_gate = Gate.from_matrix("my_h", np.array([[1,1],[1,-1]])/np.sqrt(2))

Q: 如何访问态矢量？
A: sv = get_backend("native").run(circuit, return_state=True)

更多问题请在 #help 频道提问！
```
