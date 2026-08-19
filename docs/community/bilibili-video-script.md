# B站视频脚本

---

## 视频 1：30 秒 QuoNic Demo

### 时长
30 秒

### 画面
屏幕录制 + 终端

### 脚本

```
[0:00 - 0:05] 标题卡
"QuoNic — 量子编程，像写 Python 一样简单"

[0:05 - 0:10] 终端输入
$ pip install quonic
$ python

[0:10 - 0:20] 代码输入（逐行出现）
>>> from quonic import qgate, qshow
>>> from quonic.gates import H, CX
>>> qgate(H, 0)
>>> qgate(CX, 0, 1)
>>> qshow()

[0:20 - 0:25] 结果输出
{'00': 512, '11': 512}
"贝尔态 — 量子计算最经典的结果"

[0:25 - 0:30] 结束卡
"QuoNic — 3 行代码，12+ 后端，智能调度"
"pip install quonic"
```

---

## 视频 2：5 分钟入门教程

### 时长
5 分钟

### 画面
屏幕录制 + 终端 + 代码编辑器

### 脚本

```
[0:00 - 0:15] 开场
"大家好，今天教大家用 QuoNic 写量子程序。QuoNic 是一个量子编程框架，
让你像写 Python 一样写量子代码。不需要学 Qiskit，不需要理解后端，
只需要会 Python 就行。"

[0:15 - 0:45] 第一步：安装
"首先安装 QuoNic：pip install quonic"
（终端输入 pip install quonic）

[0:45 - 1:30] 第二步：第一个量子电路
"现在写第一个量子电路——贝尔态。"
（代码输入）
from quonic import qgate, qshow
from quonic.gates import H, CX

qgate(H, 0)      # 对量子比特 0 施加 Hadamard 门
qgate(CX, 0, 1)  # CNOT：纠缠量子比特 0 和 1
qshow()           # 运行并显示结果

"3 行代码，贝尔态就出来了。{'00': 512, '11': 512}"

[1:30 - 2:15] 第三步：切换后端
"QuoNic 支持 12+ 个后端。同一段代码，不加修改，可以跑在任何后端上。"
qshow(backend='qiskit')
qshow(backend='qulacs')
qshow(method='gpu')

[2:15 - 3:00] 第四步：加噪声
"真实量子硬件有噪声。QuoNic 内置噪声模拟。"
qshow(noise=0.05)
"5% 去极化噪声，结果就不是完美的 50/50 了。"

[3:00 - 4:00] 第五步：误差缓解
"QuoNic 还有误差缓解——ZNE 零噪声外推。"
from quonic import zne
result = zne(circuit, noise=0.05, target="1", shots=1024)
print(f"ZNE 外推: {result.extrapolated:.3f}")
"噪声环境下，ZNE 能把成功率从 0.92 提高到 0.96。"

[4:00 - 4:45] 第六步：智能调度
"QuoNic 的智能调度能自动选最优后端。"
qshow(method='gpu')
"一个参数，QuoNic 自动选最快的 GPU 后端。"

[4:45 - 5:00] 结束
"QuoNic 是开源的，GitHub 链接在简介里。欢迎 star！"
"pip install quonic，开始你的量子编程之旅。"
```

---

## 视频 3：QuoNic vs Qiskit 对比

### 时长
3 分钟

### 脚本

```
[0:00 - 0:10] 开场
"QuoNic vs Qiskit，谁更适合量子编程？"

[0:10 - 0:40] 代码量对比
"贝尔态：Qiskit 10+ 行，QuoNic 3 行。"
（屏幕分屏对比）

[0:40 - 1:10] 后端切换
"Qiskit 只有 IBM 后端。QuoNic 有 12+ 个后端，一个参数切换。"
qshow(backend='qiskit')
qshow(backend='qulacs')
qshow(backend='cirq')

[1:10 - 1:40] GPU 加速
"QuoNic 有智能调度，自动选最优 GPU 后端。"
qshow(method='gpu')
"Qiskit 需要手动配置。"

[1:40 - 2:10] 误差缓解
"QuoNic 内置 ZNE + 读出校准。Qiskit 需要自己实现。"
result = zne(circuit, noise=0.05, target="1", shots=1024)

[2:10 - 2:40] 量子控制流
"QuoNic 有 qif（量子叠加控制）——Qiskit 没有的独有功能。"
qif(0).then(X, 1).else_(Z, 1)

[2:40 - 3:00] 结论
"QuoNic 不是 Qiskit 的替代品——它是 Qiskit 的抽象层。
用 QuoNic 写代码，底层可以跑 Qiskit、Cirq、Qulacs……任何后端。
pip install quonic，试试看。"
```

---

## 视频 4：QuoNic GPU 加速演示

### 时长
3 分钟

### 脚本

```
[0:00 - 0:10] 开场
"今天演示 QuoNic 的 GPU 加速功能。"

[0:10 - 0:40] 直接 GPU 执行
qshow(method='gpu')
"一个参数，自动选最优 GPU 后端。"

[0:40 - 1:10] 智能调度
from quonic.scheduler import recommend_backend_gpu, circuit_features
rec = recommend_backend_gpu(circuit_features(circuit))
print(f"推荐: {rec.backend}")
"QuoNic 根据电路特征自动选后端。"

[1:10 - 1:40] CuPy 兜底
"没有专属 GPU？CuPy 通用引擎兜底。"
qshow(backend='cupy', method='gpu')

[1:40 - 2:10] 性能对比
"GHZ-20 电路：CPU 0.53s，GPU 0.05s，10x 加速。"

[2:10 - 2:40] 后端覆盖
"QuoNic 支持 7 个 GPU 后端：Qulacs、TensorCircuit、CUDA-Q、
MindQuantum、QPanda、CuPy、Qiskit Aer。"

[2:40 - 3:00] 结束
"pip install 'quonic[gpu]'，开始 GPU 加速量子编程。"
```
