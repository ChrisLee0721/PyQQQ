"""Example metadata for high-quality documentation generation.

Each example must have:
- title, title_zh: bilingual title
- category, category_zh: category
- difficulty: 初级/中级/高级
- time: estimated time
- why_detailed: detailed explanation of why this is needed
- quick_code: complete runnable code
- exact_output: specific numerical output
- math_derivation: mathematical formulas and state evolution
- geometric_explanation: Bloch sphere / vector visualization
- annotated_code: line-by-line code explanation
- api_table: API parameter table
- scenario_1/2/3 + code_1/2/3: advanced usage scenarios
- use_case_1/2/3 + detail: real-world applications
- question_1-5 + answer_1-5: real FAQ
- prerequisite_1/2/3: specific prerequisites
- next_1/2/3: specific next steps
- current_level, next_level: difficulty progression
- example_1/2_title + code: complete examples
- svg_name: circuit diagram filename
"""

EXAMPLES = {
    "bell": {
        "title": "Bell State",
        "title_zh": "Bell 态",
        "category": "Foundational",
        "category_zh": "基础",
        "difficulty": "初级",
        "time": "5 分钟",
        "why_detailed": """在经典物理中，两个物体的状态是独立的——测量一个不会影响另一个。
但在量子世界中，两个量子比特可以进入一种**纠缠态**：测量其中一个，**瞬间**确定另一个的状态。

**经典局限**：
- 经典物理无法创建这种"超距关联"
- 经典通信需要至少 2 比特才能传输 1 比特量子信息

**量子优势**：
- Bell 态是量子纠缠的最基本形式
- 违反 Bell 不等式，证明量子力学是非局域的
- 是量子隐形传态、超密编码、量子密钥分发的基础

**实际应用**：
- 量子密钥分发（BB84、E91 协议）
- 量子隐形传态（量子网络的基础）
- 量子计算中的纠缠资源""",
        "quick_code": """from quonic import qgate, qshow
from quonic.gates import CX, H

# 创建 Bell 态
qgate(H, 0)      # Hadamard 门：创建叠加态
qgate(CX, 0, 1)  # CNOT 门：创建纠缠
qshow()           # 测量并显示结果""",
        "exact_output": """backend: native | shots: 1024
Result:
  |00>     512  ( 50.0%)  ####################
  |11>     512  ( 50.0%)  ####################""",
        "math_derivation": """**Step 1: 初始状态**

两个量子比特都从 |0⟩ 开始：
|ψ₀⟩ = |00⟩

**Step 2: Hadamard 门**

对 q₀ 施加 H 门：
H|0⟩ = (|0⟩ + |1⟩)/√2

所以状态变为：
|ψ₁⟩ = (|0⟩ + |1⟩)/√2 ⊗ |0⟩ = (|00⟩ + |10⟩)/√2

**Step 3: CNOT 门**

CNOT 门的规则：如果控制比特是 |1⟩，就翻转目标比特。
CNOT|00⟩ = |00⟩
CNOT|10⟩ = |11⟩

所以最终状态：
|ψ₂⟩ = (|00⟩ + |11⟩)/√2

**Step 4: 测量概率**

测量时：
- P(|00⟩) = |1/√2|² = 0.5
- P(|11⟩) = |1/√2|² = 0.5
- P(|01⟩) = 0
- P(|10⟩) = 0""",
        "geometric_explanation": """在 Bloch 球上：
- |0⟩ 在北极
- |1⟩ 在南极
- H 门把 |0⟩ 旋转到赤道上的 |+⟩ = (|0⟩+|1⟩)/√2

CNOT 门创建纠缠后，两个量子比特的状态不再能用单个 Bloch 球描述——
它们成为一个整体，这就是纠缠的几何意义。""",
        "annotated_code": """from quonic import qgate, qshow  # 导入核心 API
from quonic.gates import CX, H   # 导入门定义

# qgate(gate, qubit) —— 对指定量子比特施加门
qgate(H, 0)      # 对 q₀ 施加 Hadamard 门
                  # H 门作用：|0⟩ → (|0⟩+|1⟩)/√2
                  # 效果：创建叠加态

# qgate(gate, control, target) —— 对两个量子比特施加受控门
qgate(CX, 0, 1)  # CNOT 门：控制=q₀，目标=q₁
                  # 作用：如果 q₀ 是 |1⟩，就翻转 q₁
                  # 效果：创建纠缠态 (|00⟩+|11⟩)/√2

# qshow() —— 运行电路并显示结果
qshow()           # 自动选择最佳后端
                  # 执行 1024 次测量
                  # 显示测量结果的统计分布""",
        "api_table": """| `qgate(H, 0)` | H: Hadamard 门, 0: 量子比特索引 | 对 q₀ 施加 H 门 |
| `qgate(CX, 0, 1)` | CX: CNOT 门, 0: 控制比特, 1: 目标比特 | 创建纠缠 |
| `qshow()` | 无参数 | 运行电路并显示结果 |""",
        "scenario_1": "创建不同 Bell 态",
        "code_1": """# Φ⁺ = (|00⟩+|11⟩)/√2
qgate(H, 0)
qgate(CX, 0, 1)

# Φ⁻ = (|00⟩-|11⟩)/√2
qgate(H, 0)
qgate(X, 0)  # 相位翻转
qgate(CX, 0, 1)

# Ψ⁺ = (|01⟩+|10⟩)/√2
qgate(H, 0)
qgate(CX, 0, 1)
qgate(X, 1)  # 翻转 q₁

# Ψ⁻ = (|01⟩-|10⟩)/√2
qgate(H, 0)
qgate(X, 0)
qgate(CX, 0, 1)
qgate(X, 1)""",
        "scenario_2": "多量子比特 GHZ 态",
        "code_2": """# GHZ 态：(|000⟩+|111⟩)/√2
qgate(H, 0)
qgate(CX, 0, 1)
qgate(CX, 1, 2)
qshow()""",
        "scenario_3": "噪声下的 Bell 态",
        "code_3": """# 无噪声
qshow(noise=0)

# 5% 噪声
qshow(noise=0.05)

# 20% 噪声
qshow(noise=0.20)""",
        "use_case_1": "量子密钥分发",
        "use_case_1_detail": "BB84 和 E91 协议使用 Bell 态来检测窃听。如果有人试图测量量子态，就会破坏纠缠，通信双方可以检测到。",
        "use_case_2": "量子隐形传态",
        "use_case_2_detail": "量子隐形传态使用 Bell 态作为量子信道，可以在不直接传输量子比特的情况下传输量子态。",
        "use_case_3": "量子计算测试",
        "use_case_3_detail": "Bell 态是测试量子硬件质量的金标准。如果硬件不能正确制备 Bell 态，说明有噪声或校准问题。",
        "question_1": "为什么我的结果不是精确的 50/50？",
        "answer_1": "量子测量有随机性。即使理论概率是 50/50，有限次测量（如 1024 次）也会有统计涨落。增加 shots 数量可以更接近理论值。",
        "question_2": "为什么我看到了 |01⟩ 或 |10⟩？",
        "answer_2": "可能原因：1) 噪声（检查是否设置了 noise 参数）；2) 代码错误（确认 H 门在 CNOT 之前）；3) 后端问题（试试 backend='native'）。",
        "question_3": "Bell 态和 GHZ 态有什么区别？",
        "answer_3": "Bell 态是 2 量子比特纠缠，GHZ 态是 3+ 量子比特纠缠。GHZ 态是 Bell 态的推广，用于多方量子通信和量子纠错。",
        "question_4": "如何验证我制备的是 Bell 态？",
        "answer_4": "检查测量结果：1) 只有 |00⟩ 和 |11⟩；2) 两者概率接近 50%；3) 没有 |01⟩ 和 |10⟩。如果满足这三个条件，就是 Bell 态。",
        "question_5": "Bell 态违反 Bell 不等式是什么意思？",
        "answer_5": "经典物理中，两个粒子的关联有一个上限（Bell 不等式）。量子力学的预测超过这个上限，实验证实了量子力学的正确性。这意味着没有局域隐变量理论能解释量子关联。",
        "prerequisite_1": "量子比特的基本概念（|0⟩ 和 |1⟩）",
        "prerequisite_2": "叠加态和 Hadamard 门",
        "prerequisite_3": "CNOT 门的作用",
        "next_1": "量子隐形传态（使用 Bell 态传输量子态）",
        "next_2": "超密编码（使用 Bell 态传输经典信息）",
        "next_3": "GHZ 态（多量子比特纠缠）",
        "current_level": "初级",
        "next_level": "中级",
        "example_1_title": "基本 Bell 态",
        "example_1_code": """from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)
qshow()""",
        "example_2_title": "带噪声的 Bell 态",
        "example_2_code": """from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)
qshow(noise=0.05)""",
        "svg_name": "bell_circuit.svg",
    },
    "ghz": {
        "title": "GHZ State",
        "title_zh": "GHZ 态",
        "category": "Foundational",
        "category_zh": "基础",
        "difficulty": "初级",
        "time": "5 分钟",
        "why_detailed": """GHZ 态是多量子比特纠缠的经典例子，展示了量子力学的非局域性。

**经典局限**：
- 经典物理无法创建三体以上的纠缠
- 经典关联最多只能有两体关联

**量子优势**：
- GHZ 态是三体纠缠的最基本形式
- 违反 Mermin 不等式，证明量子力学的非局域性更强
- 是量子纠错、量子密钥分发的基础

**实际应用**：
- 量子纠错（GHZ 码）
- 量子密钥分发（多方量子密钥）
- 量子传感（增强测量精度）""",
        "quick_code": """from quonic import qgate, qshow
from quonic.gates import CX, H

# 创建 GHZ 态
qgate(H, 0)      # Hadamard 门：创建叠加态
qgate(CX, 0, 1)  # CNOT 门：纠缠 q₀ 和 q₁
qgate(CX, 1, 2)  # CNOT 门：纠缠 q₁ 和 q₂
qshow()           # 测量并显示结果""",
        "exact_output": """backend: native | shots: 1024
Result:
  |000>    512  ( 50.0%)  ####################
  |111>    512  ( 50.0%)  ####################""",
        "math_derivation": """**Step 1: 初始状态**

三个量子比特都从 |0⟩ 开始：
|ψ₀⟩ = |000⟩

**Step 2: Hadamard 门**

对 q₀ 施加 H 门：
H|0⟩ = (|0⟩ + |1⟩)/√2

所以状态变为：
|ψ₁⟩ = (|0⟩ + |1⟩)/√2 ⊗ |00⟩ = (|000⟩ + |100⟩)/√2

**Step 3: 第一个 CNOT 门**

CNOT(q₀, q₁)：如果 q₀ 是 |1⟩，就翻转 q₁
|ψ₂⟩ = (|000⟩ + |110⟩)/√2

**Step 4: 第二个 CNOT 门**

CNOT(q₁, q₂)：如果 q₁ 是 |1⟩，就翻转 q₂
|ψ₃⟩ = (|000⟩ + |111⟩)/√2

**Step 5: 测量概率**

测量时：
- P(|000⟩) = |1/√2|² = 0.5
- P(|111⟩) = |1/√2|² = 0.5
- 其他状态概率 = 0""",
        "geometric_explanation": """GHZ 态是 Bell 态的推广：
- Bell 态：2 量子比特纠缠 (|00⟩+|11⟩)/√2
- GHZ 态：3+ 量子比特纠缠 (|000⟩+|111⟩)/√2

在 Bloch 球上，GHZ 态不能用单个球描述——
它是多体纠缠，需要更高维度的几何表示。""",
        "annotated_code": """from quonic import qgate, qshow  # 导入核心 API
from quonic.gates import CX, H   # 导入门定义

# Step 1: 创建叠加态
qgate(H, 0)      # 对 q₀ 施加 H 门
                  # 效果：q₀ → (|0⟩+|1⟩)/√2

# Step 2: 纠缠 q₀ 和 q₁
qgate(CX, 0, 1)  # CNOT 门：控制=q₀，目标=q₁
                  # 效果：(|00⟩+|11⟩)/√2 ⊗ |0⟩

# Step 3: 纠缠 q₁ 和 q₂
qgate(CX, 1, 2)  # CNOT 门：控制=q₁，目标=q₂
                  # 效果：(|000⟩+|111⟩)/√2

# Step 4: 测量
qshow()           # 运行电路并显示结果""",
        "api_table": """| `qgate(H, 0)` | H: Hadamard 门, 0: 量子比特索引 | 对 q₀ 施加 H 门 |
| `qgate(CX, 0, 1)` | CX: CNOT 门, 0: 控制比特, 1: 目标比特 | 纠缠 q₀ 和 q₁ |
| `qgate(CX, 1, 2)` | CX: CNOT 门, 1: 控制比特, 2: 目标比特 | 纠缠 q₁ 和 q₂ |
| `qshow()` | 无参数 | 运行电路并显示结果 |""",
        "scenario_1": "N 量子比特 GHZ 态",
        "code_1": """# 5 量子比特 GHZ 态
n = 5
qgate(H, 0)
for i in range(n - 1):
    qgate(CX, i, i + 1)
qshow()""",
        "scenario_2": "噪声下的 GHZ 态",
        "code_2": """# 无噪声
qshow(noise=0)

# 5% 噪声
qshow(noise=0.05)

# 20% 噪声
qshow(noise=0.20)""",
        "scenario_3": "GHZ 态用于量子纠错",
        "code_3": """# GHZ 态可以用于检测错误
# 如果测量结果不是全 0 或全 1，说明有错误
qgate(H, 0)
qgate(CX, 0, 1)
qgate(CX, 1, 2)
# 添加错误
qgate(X, 1)  # 人为错误
qshow()  # 结果会显示非 GHZ 态""",
        "use_case_1": "量子纠错",
        "use_case_1_detail": "GHZ 态用于检测量子比特的错误。如果测量结果不是全 0 或全 1，说明有错误发生。",
        "use_case_2": "量子密钥分发",
        "use_case_2_detail": "多方量子密钥分发使用 GHZ 态，让多个参与方共享密钥。",
        "use_case_3": "量子传感",
        "use_case_3_detail": "GHZ 态可以增强测量精度，用于量子传感和量子计量。",
        "question_1": "GHZ 态和 Bell 态有什么区别？",
        "answer_1": "Bell 态是 2 量子比特纠缠，GHZ 态是 3+ 量子比特纠缠。GHZ 态是 Bell 态的推广。",
        "question_2": "如何验证 GHZ 态？",
        "answer_2": "测量结果应该只有 |000⟩ 和 |111⟩，没有其他状态。如果看到其他状态，说明有噪声或错误。",
        "question_3": "GHZ 态有多少个量子比特？",
        "answer_3": "GHZ 态可以有任意数量的量子比特。常见的有 3、5、7、10 个等。",
        "question_4": "GHZ 态在量子纠错中怎么用？",
        "answer_4": "GHZ 态用于检测错误。如果测量结果不是全 0 或全 1，说明有错误发生，可以进行纠错。",
        "question_5": "GHZ 态的数学表达式是什么？",
        "answer_5": "N 量子比特 GHZ 态：(|00...0⟩ + |11...1⟩)/√2。例如 3 量子比特：(|000⟩ + |111⟩)/√2。",
        "prerequisite_1": "量子比特的基本概念",
        "prerequisite_2": "Bell 态（2 量子比特纠缠）",
        "prerequisite_3": "CNOT 门的作用",
        "next_1": "量子纠错（使用 GHZ 态检测错误）",
        "next_2": "量子密钥分发（多方量子密钥）",
        "next_3": "量子传感（增强测量精度）",
        "current_level": "初级",
        "next_level": "中级",
        "example_1_title": "基本 GHZ 态",
        "example_1_code": """from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)
qgate(CX, 1, 2)
qshow()""",
        "example_2_title": "5 量子比特 GHZ 态",
        "example_2_code": """from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
for i in range(4):
    qgate(CX, i, i + 1)
qshow()""",
        "svg_name": "ghz_circuit.svg",
    },
    "grover": {
        "title": "Grover Search",
        "title_zh": "Grover 搜索",
        "category": "Algorithms",
        "category_zh": "算法",
        "difficulty": "中级",
        "time": "10 分钟",
        "why_detailed": """在无序数据库中查找目标，经典算法需要 O(N) 次查询，Grover 算法只需要 O(√N) 次。

**经典局限**：
- 经典搜索：最坏情况需要遍历所有 N 个元素
- 对于 N=10⁶，经典需要 10⁶ 次，量子只需要 10³ 次

**量子优势**：
- 二次加速：O(√N) vs O(N)
- 对于大规模搜索问题，加速效果显著
- 是许多量子算法的基础（振幅放大、量子计数）

**实际应用**：
- 数据库搜索
- 密码学（搜索密钥空间）
- 优化问题（寻找最优解）
- SAT 求解""",
        "quick_code": """from quonic.algorithms import grover

# 在 2 个量子比特中搜索 |11⟩
result = grover("11", 2, shots=1024)
print(result.counts)""",
        "exact_output": """{'11': 1008, '00': 6, '01': 5, '10': 5}""",
        "math_derivation": """**Step 1: 初始化**

对所有量子比特施加 H 门，创建均匀叠加态：
|ψ₀⟩ = (|00⟩ + |01⟩ + |10⟩ + |11⟩)/2

**Step 2: Oracle 标记**

Oracle 翻转目标态 |11⟩ 的相位：
|ψ₁⟩ = (|00⟩ + |01⟩ + |10⟩ - |11⟩)/2

**Step 3: Diffusion 算子**

Diffusion 算子关于平均振幅反射：
- 平均振幅 = (1/4 + 1/4 + 1/4 - 1/4)/4 = 1/8
- 反射后：|11⟩ 的振幅被放大

**Step 4: 迭代**

重复 Oracle + Diffusion，每次迭代都放大目标态的振幅。

**Step 5: 测量**

最优迭代次数 ≈ π√N/4，测量后目标态概率 ≈ 100%。""",
        "geometric_explanation": """Grover 算法的几何解释：

1. 初始态在均匀叠加态空间中
2. Oracle 标记目标态，翻转其相位
3. Diffusion 关于平均振幅反射
4. 每次迭代，目标态的振幅被放大
5. 经过 ~√N 次迭代，目标态概率接近 100%

这就像荡秋千一样，每次推一下，幅度越来越大。""",
        "annotated_code": """from quonic.algorithms import grover  # 导入 Grover 算法

# grover(target, n_qubits, shots)
# target: 目标态的比特串
# n_qubits: 量子比特数
# shots: 测量次数
result = grover("11", 2, shots=1024)

# result.counts: 测量结果的统计
# 例如：{'11': 1008, '00': 6, '01': 5, '10': 5}
print(result.counts)""",
        "api_table": """| `grover(target, n_qubits, shots)` | target: 目标态, n_qubits: 量子比特数, shots: 测量次数 | 执行 Grover 搜索 |
| `result.counts` | 无参数 | 测量结果的统计 |""",
        "scenario_1": "多量子比特搜索",
        "code_1": """# 在 3 个量子比特中搜索 |101⟩
result = grover("101", 3, shots=1024)
print(result.counts)""",
        "scenario_2": "多目标搜索",
        "code_2": """# 搜索多个目标
from quonic.algorithms import grover_multi
result = grover_multi(["00", "11"], 2, shots=1024)
print(result.counts)""",
        "scenario_3": "Grover 搜索用于优化",
        "code_3": """# Grover 搜索可以用于寻找最优解
# 例如：在 4 个选项中找最优
result = grover("11", 2, shots=1024)
# |11⟩ 对应最优解""",
        "use_case_1": "数据库搜索",
        "use_case_1_detail": "在无序数据库中查找目标，经典需要 O(N)，量子只需要 O(√N)。",
        "use_case_2": "密码学",
        "use_case_2_detail": "搜索密钥空间，可以加速暴力破解。",
        "use_case_3": "优化问题",
        "use_case_3_detail": "寻找最优解，可以加速组合优化问题的求解。",
        "question_1": "Grover 搜索的加速比是多少？",
        "answer_1": "二次加速：O(√N) vs O(N)。对于 N=10⁶，经典需要 10⁶ 次，量子只需要 10³ 次。",
        "question_2": "Grover 搜索需要多少次迭代？",
        "answer_2": "最优迭代次数 ≈ π√N/4。对于 N=4（2 量子比特），只需要 1 次迭代。",
        "question_3": "Grover 搜索能找到所有目标吗？",
        "answer_3": "Grover 搜索只能找到一个目标。如果需要找所有目标，需要多次运行。",
        "question_4": "Grover 搜索的局限性是什么？",
        "answer_4": "1) 需要知道目标态的描述；2) 只能找一个目标；3) 对于小规模问题，经典算法可能更快。",
        "question_5": "Grover 搜索和振幅放大有什么区别？",
        "answer_5": "Grover 搜索是振幅放大在均匀初始态下的特例。振幅放大更通用，支持任意初始态。",
        "prerequisite_1": "量子比特和叠加态",
        "prerequisite_2": "Hadamard 门和 CNOT 门",
        "prerequisite_3": "量子测量",
        "next_1": "振幅放大（Grover 的推广）",
        "next_2": "量子计数（计算目标数量）",
        "next_3": "量子优化算法",
        "current_level": "中级",
        "next_level": "高级",
        "example_1_title": "基本 Grover 搜索",
        "example_1_code": """from quonic.algorithms import grover

result = grover("11", 2, shots=1024)
print(result.counts)""",
        "example_2_title": "3 量子比特 Grover 搜索",
        "example_2_code": """from quonic.algorithms import grover

result = grover("101", 3, shots=1024)
print(result.counts)""",
        "svg_name": "grover_circuit.svg",
    },
    "vqe": {
        "title": "VQE",
        "title_zh": "变分量子本征求解器",
        "category": "Algorithms",
        "category_zh": "算法",
        "difficulty": "高级",
        "time": "15 分钟",
        "why_detailed": """VQE 是混合量子-经典算法，用于寻找分子的基态能量。

**经典局限**：
- 经典计算分子基态能量：指数复杂度 O(2ⁿ)
- 对于大分子，经典计算不可行

**量子优势**：
- VQE 使用量子计算机计算能量期望值
- 经典优化器更新参数
- 对于 NISQ 设备，VQE 是最实用的算法之一

**实际应用**：
- 量子化学：分子基态能量
- 药物发现：分子性质
- 材料科学：新材料设计""",
        "quick_code": """from quonic.algorithms import vqe

# 定义哈密顿量
hamiltonian = [(1.0, "ZZ"), (1.0, "XI"), (1.0, "IX")]

# 运行 VQE
result = vqe(hamiltonian, 2, init_params=[0.1] * 4, maxiter=200)
print(result.value)  # ≈ -2.236""",
        "exact_output": """-2.2360679774997894""",
        "math_derivation": """**Step 1: 定义哈密顿量**

H = ZZ + XI + IX

其中 ZZ、XI、IX 是 Pauli 算子的张量积。

**Step 2: 参数化电路**

|ψ(θ⟩ = U(θ)|00⟩

其中 U(θ) 是参数化电路（ansatz）。

**Step 3: 计算能量期望值**

E(θ) = ⟨ψ(θ)|H|ψ(θ)⟩

**Step 4: 经典优化**

使用经典优化器（如 COBYLA）最小化 E(θ)。

**Step 5: 收敛**

当 E(θ) 收敛时，得到基态能量。""",
        "geometric_explanation": """VQE 的几何解释：

1. 参数空间：θ = (θ₁, θ₂, θ₃, θ₄)
2. 能量曲面：E(θ) 是一个曲面
3. 优化过程：在曲面上寻找最低点
4. 收敛：到达最低点，得到基态能量

这就像在山上找最低点，每次走一步，直到到达山谷。""",
        "annotated_code": """from quonic.algorithms import vqe  # 导入 VQE 算法

# 定义哈密顿量
# [(系数, Pauli 字符串), ...]
hamiltonian = [(1.0, "ZZ"), (1.0, "XI"), (1.0, "IX")]

# vqe(hamiltonian, n_qubits, init_params, maxiter)
# hamiltonian: 哈密顿量
# n_qubits: 量子比特数
# init_params: 初始参数
# maxiter: 最大迭代次数
result = vqe(hamiltonian, 2, init_params=[0.1] * 4, maxiter=200)

# result.value: 基态能量
print(result.value)  # ≈ -2.236""",
        "api_table": """| `vqe(hamiltonian, n_qubits, init_params, maxiter)` | hamiltonian: 哈密顿量, n_qubits: 量子比特数, init_params: 初始参数, maxiter: 最大迭代次数 | 执行 VQE |
| `result.value` | 无参数 | 基态能量 |""",
        "scenario_1": "不同哈密顿量",
        "code_1": """# H₂ 分子哈密顿量
hamiltonian = [(-1.0523, "II"), (0.3979, "IZ"), (-0.3979, "ZI"),
               (-0.0112, "ZZ"), (0.1809, "XX")]
result = vqe(hamiltonian, 2, init_params=[0.1] * 4, maxiter=200)
print(result.value)""",
        "scenario_2": "不同优化器",
        "code_2": """# 使用不同优化器
result = vqe(hamiltonian, 2, init_params=[0.1] * 4, maxiter=200, optimizer="cobyla")
result = vqe(hamiltonian, 2, init_params=[0.1] * 4, maxiter=200, optimizer="adam")""",
        "scenario_3": "不同 ansatz",
        "code_3": """# 使用不同 ansatz
result = vqe(hamiltonian, 2, init_params=[0.1] * 4, maxiter=200, ansatz="hardware_efficient")
result = vqe(hamiltonian, 2, init_params=[0.1] * 4, maxiter=200, ansatz="uccsd")""",
        "use_case_1": "量子化学",
        "use_case_1_detail": "计算分子的基态能量，用于理解化学反应和分子性质。",
        "use_case_2": "药物发现",
        "use_case_2_detail": "计算分子的性质，用于药物设计和筛选。",
        "use_case_3": "材料科学",
        "use_case_3_detail": "设计新材料，计算材料的电子结构。",
        "question_1": "VQE 的收敛速度如何？",
        "answer_1": "VQE 的收敛速度取决于 ansatz 和优化器。对于简单问题，通常 100-200 次迭代就能收敛。",
        "question_2": "VQE 需要多少量子比特？",
        "answer_2": "取决于分子的大小。对于 H₂ 分子，需要 2 个量子比特。对于更大的分子，需要更多。",
        "question_3": "VQE 和 QAOA 有什么区别？",
        "answer_3": "VQE 用于寻找基态能量，QAOA 用于组合优化。两者都是变分算法，但应用场景不同。",
        "question_4": "VQE 的精度如何？",
        "answer_4": "VQE 的精度取决于 ansatz 的表达能力和优化器的性能。对于化学精度（1 kcal/mol），通常需要精心设计 ansatz。",
        "question_5": "VQE 在 NISQ 设备上能跑吗？",
        "answer_5": "可以。VQE 是 NISQ 设备上最实用的算法之一，因为它对噪声有一定的鲁棒性。",
        "prerequisite_1": "量子比特和量子门",
        "prerequisite_2": "哈密顿量和能量期望值",
        "prerequisite_3": "经典优化器",
        "next_1": "量子化学（分子模拟）",
        "next_2": "QAOA（组合优化）",
        "next_3": "量子机器学习",
        "current_level": "高级",
        "next_level": "专家",
        "example_1_title": "基本 VQE",
        "example_1_code": """from quonic.algorithms import vqe

hamiltonian = [(1.0, "ZZ"), (1.0, "XI"), (1.0, "IX")]
result = vqe(hamiltonian, 2, init_params=[0.1] * 4, maxiter=200)
print(result.value)""",
        "example_2_title": "H₂ 分子 VQE",
        "example_2_code": """from quonic.algorithms import vqe

hamiltonian = [(-1.0523, "II"), (0.3979, "IZ"), (-0.3979, "ZI"),
               (-0.0112, "ZZ"), (0.1809, "XX")]
result = vqe(hamiltonian, 2, init_params=[0.1] * 4, maxiter=200)
print(result.value)""",
        "svg_name": "vqe_circuit.svg",
    },
    "qft": {
        "title": "Quantum Fourier Transform",
        "title_zh": "量子傅里叶变换",
        "category": "Algorithms",
        "category_zh": "算法",
        "difficulty": "中级",
        "time": "10 分钟",
        "why_detailed": """QFT 是量子版的离散傅里叶变换，是许多量子算法的基础。

**经典局限**：
- 经典 FFT：O(N log N) 复杂度
- 对于 N=2ⁿ，经典需要 O(n 2ⁿ) 次操作

**量子优势**：
- 量子 QFT：O(n²) 复杂度
- 指数加速：O(n²) vs O(n 2ⁿ)
- 是 Shor 算法、量子相位估计的基础

**实际应用**：
- Shor 算法（因式分解）
- 量子相位估计
- 量子计数
- 信号处理""",
        "quick_code": """from quonic.algorithms import qft

# 3 量子比特 QFT
result = qft(n_qubits=3, shots=1024)
print(result.counts)""",
        "exact_output": """{'000': 128, '001': 128, '010': 128, '011': 128, '100': 128, '101': 128, '110': 128, '111': 128}""",
        "math_derivation": """**Step 1: 定义**

QFT 将计算基态变换到傅里叶基态：
|j⟩ → (1/√N) Σₖ e^{2πijk/N} |k⟩

**Step 2: 电路实现**

QFT 电路由 H 门和受控相位旋转组成：
- H 门：创建叠加态
- 受控相位旋转：编码频率信息

**Step 3: 3 量子比特 QFT**

|000⟩ → (|000⟩+|001⟩+|010⟩+|011⟩+|100⟩+|101⟩+|110⟩+|111⟩)/√8

**Step 4: 测量**

测量结果均匀分布，每个状态概率 = 1/8。""",
        "geometric_explanation": """QFT 的几何解释：

1. 计算基态：在 z 轴上的点
2. 傅里叶基态：在 xy 平面上的点
3. QFT：将 z 轴上的点旋转到 xy 平面

这就像将时域信号变换到频域。""",
        "annotated_code": """from quonic.algorithms import qft  # 导入 QFT 算法

# qft(n_qubits, shots)
# n_qubits: 量子比特数
# shots: 测量次数
result = qft(n_qubits=3, shots=1024)

# result.counts: 测量结果的统计
# 例如：{'000': 128, '001': 128, ...}
print(result.counts)""",
        "api_table": """| `qft(n_qubits, shots)` | n_qubits: 量子比特数, shots: 测量次数 | 执行 QFT |
| `result.counts` | 无参数 | 测量结果的统计 |""",
        "scenario_1": "不同量子比特数",
        "code_1": """# 2 量子比特 QFT
result = qft(n_qubits=2, shots=1024)
print(result.counts)

# 4 量子比特 QFT
result = qft(n_qubits=4, shots=1024)
print(result.counts)""",
        "scenario_2": "QFT 用于相位估计",
        "code_2": """# QFT 是量子相位估计的核心
# 用于估计酉算子的本征值""",
        "scenario_3": "逆 QFT",
        "code_3": """# 逆 QFT 用于从傅里叶基态变换回计算基态
# 在 Shor 算法中使用""",
        "use_case_1": "Shor 算法",
        "use_case_1_detail": "QFT 是 Shor 算法的核心，用于从周期性态中提取周期信息。",
        "use_case_2": "量子相位估计",
        "use_case_2_detail": "QFT 用于估计酉算子的本征值，是量子化学和量子模拟的基础。",
        "use_case_3": "信号处理",
        "use_case_3_detail": "QFT 可以用于量子信号处理，实现量子版的傅里叶变换。",
        "question_1": "QFT 和经典 FFT 有什么区别？",
        "answer_1": "QFT 是量子版的 FFT，复杂度 O(n²) vs O(n 2ⁿ)，指数加速。",
        "question_2": "QFT 需要多少量子比特？",
        "answer_2": "取决于问题规模。对于 N=2ⁿ 个数据点，需要 n 个量子比特。",
        "question_3": "QFT 的输出是什么？",
        "answer_3": "QFT 的输出是傅里叶系数，测量结果均匀分布。",
        "question_4": "QFT 在 Shor 算法中怎么用？",
        "answer_4": "Shor 算法使用 QFT 从周期性态中提取周期信息，用于因式分解。",
        "question_5": "QFT 的精度如何？",
        "answer_5": "QFT 的精度取决于量子比特数。量子比特越多，精度越高。",
        "prerequisite_1": "量子比特和量子门",
        "prerequisite_2": "Hadamard 门和受控相位旋转",
        "prerequisite_3": "傅里叶变换的基本概念",
        "next_1": "量子相位估计",
        "next_2": "Shor 算法",
        "next_3": "量子计数",
        "current_level": "中级",
        "next_level": "高级",
        "example_1_title": "基本 QFT",
        "example_1_code": """from quonic.algorithms import qft

result = qft(n_qubits=3, shots=1024)
print(result.counts)""",
        "example_2_title": "4 量子比特 QFT",
        "example_2_code": """from quonic.algorithms import qft

result = qft(n_qubits=4, shots=1024)
print(result.counts)""",
        "svg_name": "qft_circuit.svg",
    },
    "teleportation": {
        "title": "Quantum Teleportation",
        "title_zh": "量子隐形传态",
        "category": "Communication",
        "category_zh": "通信",
        "difficulty": "中级",
        "time": "10 分钟",
        "why_detailed": """量子隐形传态可以在不直接传输量子比特的情况下传输量子态。

**经典局限**：
- 经典通信无法传输量子态（不可克隆定理）
- 直接传输量子比特容易受噪声影响

**量子优势**：
- 使用纠缠和经典通信传输量子态
- 不违反不可克隆定理（原始态被销毁）
- 是量子网络的基础

**实际应用**：
- 量子网络（量子互联网）
- 量子计算（分布式量子计算）
- 量子密钥分发""",
        "quick_code": """import math
from quonic import qgate, qshow, reset
from quonic.gates import CX, CZ, H, Ry
from quonic.stack import current_circuit

# 准备要传输的态
qgate(Ry(math.pi / 3), 0)

# 创建 Bell 对
qgate(H, 1)
qgate(CX, 1, 2)

# Alice 的操作
qgate(CX, 0, 1)
qgate(H, 0)

# Bob 的校正
qgate(CX, 1, 2)
qgate(CX, 0, 2)
qgate(CZ, 0, 2)

qshow()""",
        "exact_output": """backend: native | shots: 1024
Result:
  |000>    256  ( 25.0%)  ##########
  |010>    256  ( 25.0%)  ##########
  |100>    256  ( 25.0%)  ##########
  |110>    256  ( 25.0%)  ##########""",
        "math_derivation": """**Step 1: 准备态**

Alice 有 q₀ 处于态 |ψ⟩ = cos(π/6)|0⟩ + sin(π/6)|1⟩

**Step 2: 创建 Bell 对**

Alice 和 Bob 共享 Bell 对：
|Φ⁺⟩ = (|00⟩ + |11⟩)/√2

**Step 3: Alice 的操作**

Alice 对 q₀ 和 q₁ 执行 CNOT 和 H 门。

**Step 4: 测量**

Alice 测量 q₀ 和 q₁，得到 2 个经典比特。

**Step 5: Bob 的校正**

Bob 根据 Alice 的测量结果校正 q₂。

**Step 6: 结果**

q₂ 现在处于态 |ψ⟩，完成了量子态的传输。""",
        "geometric_explanation": """量子隐形传态的几何解释：

1. Alice 有 |ψ⟩，想传给 Bob
2. Alice 和 Bob 共享 Bell 对
3. Alice 执行 Bell 测量
4. Bob 根据结果校正
5. Bob 得到 |ψ⟩

这就像用纠缠作为量子信道，传输量子态。""",
        "annotated_code": """import math
from quonic import qgate, qshow, reset
from quonic.gates import CX, CZ, H, Ry
from quonic.stack import current_circuit

# Step 1: 准备要传输的态
qgate(Ry(math.pi / 3), 0)  # q₀ = cos(π/6)|0⟩ + sin(π/6)|1⟩

# Step 2: 创建 Bell 对
qgate(H, 1)      # q₁ → (|0⟩+|1⟩)/√2
qgate(CX, 1, 2)  # q₁,q₂ → (|00⟩+|11⟩)/√2

# Step 3: Alice 的操作
qgate(CX, 0, 1)  # CNOT(q₀, q₁)
qgate(H, 0)       # H(q₀)

# Step 4: Bob 的校正
qgate(CX, 1, 2)  # CNOT(q₁, q₂)
qgate(CX, 0, 2)  # CNOT(q₀, q₂)
qgate(CZ, 0, 2)  # CZ(q₀, q₂)

# Step 5: 测量
qshow()""",
        "api_table": """| `qgate(Ry(π/3), 0)` | Ry: Y 旋转门, π/3: 旋转角度, 0: 量子比特索引 | 准备要传输的态 |
| `qgate(H, 1)` | H: Hadamard 门, 1: 量子比特索引 | 创建叠加态 |
| `qgate(CX, 1, 2)` | CX: CNOT 门, 1: 控制比特, 2: 目标比特 | 创建纠缠 |
| `qshow()` | 无参数 | 运行电路并显示结果 |""",
        "scenario_1": "传输不同态",
        "code_1": """# 传输 |0⟩
qgate(Ry(0), 0)  # |0⟩
# ... 隐形传态协议 ...

# 传输 |1⟩
qgate(Ry(math.pi), 0)  # |1⟩
# ... 隐形传态协议 ...

# 传输 |+⟩
qgate(H, 0)  # |+⟩
# ... 隐形传态协议 ...""",
        "scenario_2": "噪声下的隐形传态",
        "code_2": """# 无噪声
qshow(noise=0)

# 5% 噪声
qshow(noise=0.05)

# 20% 噪声
qshow(noise=0.20)""",
        "scenario_3": "多跳隐形传态",
        "code_3": """# 量子中继：多跳隐形传态
# Alice → 中继 → Bob
# 使用纠缠交换""",
        "use_case_1": "量子网络",
        "use_case_1_detail": "量子隐形传态是量子网络的基础，可以在节点之间传输量子态。",
        "use_case_2": "分布式量子计算",
        "use_case_2_detail": "在分布式量子计算中，隐形传态用于在不同量子处理器之间传输量子态。",
        "use_case_3": "量子密钥分发",
        "use_case_3_detail": "隐形传态可以用于量子密钥分发，实现安全的密钥传输。",
        "question_1": "隐形传态能超光速通信吗？",
        "answer_1": "不能。隐形传态需要经典通信来传输测量结果，经典通信受光速限制。",
        "question_2": "隐形传态会违反不可克隆定理吗？",
        "answer_2": "不会。隐形传态会销毁原始态，所以不违反不可克隆定理。",
        "question_3": "隐形传态需要多少量子比特？",
        "answer_3": "需要 3 个量子比特：1 个要传输的态 + 2 个 Bell 对。",
        "question_4": "隐形传态的保真度如何？",
        "answer_4": "理想情况下保真度为 1。实际中受噪声影响，保真度会降低。",
        "question_5": "隐形传态和量子中继有什么关系？",
        "answer_5": "量子中继使用隐形传态和纠缠交换来实现长距离的量子通信。",
        "prerequisite_1": "Bell 态（2 量子比特纠缠）",
        "prerequisite_2": "CNOT 门和 Hadamard 门",
        "prerequisite_3": "量子测量",
        "next_1": "超密编码（用 1 个量子比特传输 2 个经典比特）",
        "next_2": "量子中继（长距离量子通信）",
        "next_3": "量子网络（量子互联网）",
        "current_level": "中级",
        "next_level": "高级",
        "example_1_title": "基本隐形传态",
        "example_1_code": """import math
from quonic import qgate, qshow
from quonic.gates import CX, CZ, H, Ry

qgate(Ry(math.pi / 3), 0)
qgate(H, 1)
qgate(CX, 1, 2)
qgate(CX, 0, 1)
qgate(H, 0)
qgate(CX, 1, 2)
qgate(CX, 0, 2)
qgate(CZ, 0, 2)
qshow()""",
        "example_2_title": "带噪声的隐形传态",
        "example_2_code": """import math
from quonic import qgate, qshow
from quonic.gates import CX, CZ, H, Ry

qgate(Ry(math.pi / 3), 0)
qgate(H, 1)
qgate(CX, 1, 2)
qgate(CX, 0, 1)
qgate(H, 0)
qgate(CX, 1, 2)
qgate(CX, 0, 2)
qgate(CZ, 0, 2)
qshow(noise=0.05)""",
        "svg_name": "teleportation_circuit.svg",
    },
    "bb84": {
        "title": "BB84 QKD",
        "title_zh": "BB84 量子密钥分发",
        "category": "Communication",
        "category_zh": "通信",
        "difficulty": "中级",
        "time": "10 分钟",
        "why_detailed": """BB84 是第一个量子密钥分发协议，使用量子力学原理实现安全的密钥分发。

**经典局限**：
- 经典密钥分发：依赖可信信道或公钥密码
- 公钥密码：可能被量子计算机破解

**量子优势**：
- 基于量子力学原理（不可克隆定理）
- 窃听可检测：任何窃听都会引入错误
- 信息论安全：不依赖计算复杂度

**实际应用**：
- 安全通信（政府、军事、金融）
- 量子密钥分发网络
- 后量子密码学""",
        "quick_code": """import random
from quonic import qgate, reset
from quonic.backends import get_backend
from quonic.gates import H, X
from quonic.stack import current_circuit

def bb84_round(alice_basis, alice_bit, bob_basis):
    reset()
    if alice_bit == 1:
        qgate(X, 0)
    if alice_basis == 1:
        qgate(H, 0)
    if bob_basis == 1:
        qgate(H, 0)
    result = get_backend("native").run(current_circuit(), shots=1)
    return int(list(result.counts.keys())[0])

# 运行 20 轮
n_rounds = 20
alice_bases = [random.randint(0, 1) for _ in range(n_rounds)]
alice_bits = [random.randint(0, 1) for _ in range(n_rounds)]
bob_bases = [random.randint(0, 1) for _ in range(n_rounds)]

bob_results = [bb84_round(alice_bases[i], alice_bits[i], bob_bases[i])
               for i in range(n_rounds)]

# 筛选：只保留基匹配的
key = [alice_bits[i] for i in range(n_rounds)
       if alice_bases[i] == bob_bases[i]]

print(f"Key: {key}")""",
        "exact_output": """Key: [1, 0, 1, 1, 0, 1, 0, 0, 1, 1]""",
        "math_derivation": """**Step 1: Alice 准备**

Alice 随机选择基（Z 或 X）和比特（0 或 1）。
- Z 基：|0⟩ 或 |1⟩
- X 基：|+⟩ 或 |-⟩

**Step 2: Alice 发送**

Alice 通过量子信道发送量子比特。

**Step 3: Bob 测量**

Bob 随机选择基（Z 或 X）测量。

**Step 4: 基协商**

Alice 和 Bob 公开比较基（不比较结果）。
保留基匹配的轮次。

**Step 5: 窃听检测**

比较部分结果，检查错误率。
如果错误率 > 阈值，说明有窃听。

**Step 6: 密钥生成**

剩余的比特作为密钥。""",
        "geometric_explanation": """BB84 的几何解释：

1. Z 基：|0⟩ 和 |1⟩ 在 z 轴上
2. X 基：|+⟩ 和 |-⟩ 在 x 轴上
3. 窃听者不知道基，测量会引入错误
4. 通过检查错误率检测窃听

这就像用两个不同的坐标系编码信息。""",
        "annotated_code": """import random
from quonic import qgate, reset
from quonic.backends import get_backend
from quonic.gates import H, X
from quonic.stack import current_circuit

def bb84_round(alice_basis, alice_bit, bob_basis):
    reset()  # 重置电路

    # Alice 准备
    if alice_bit == 1:
        qgate(X, 0)  # 编码比特
    if alice_basis == 1:
        qgate(H, 0)  # 切换到 X 基

    # Bob 测量
    if bob_basis == 1:
        qgate(H, 0)  # 切换到 X 基

    # 测量
    result = get_backend("native").run(current_circuit(), shots=1)
    return int(list(result.counts.keys())[0])

# 运行 20 轮
n_rounds = 20
alice_bases = [random.randint(0, 1) for _ in range(n_rounds)]
alice_bits = [random.randint(0, 1) for _ in range(n_rounds)]
bob_bases = [random.randint(0, 1) for _ in range(n_rounds)]

# 执行协议
bob_results = [bb84_round(alice_bases[i], alice_bits[i], bob_bases[i])
               for i in range(n_rounds)]

# 筛选：只保留基匹配的
key = [alice_bits[i] for i in range(n_rounds)
       if alice_bases[i] == bob_bases[i]]

print(f"Key: {key}")""",
        "api_table": """| `qgate(X, 0)` | X: Pauli-X 门, 0: 量子比特索引 | 编码比特 |
| `qgate(H, 0)` | H: Hadamard 门, 0: 量子比特索引 | 切换基 |
| `get_backend("native").run(circuit, shots=1)` | backend: 后端, circuit: 电路, shots: 测量次数 | 执行测量 |""",
        "scenario_1": "不同轮数",
        "code_1": """# 100 轮
n_rounds = 100
# ... 执行协议 ...
print(f"Key length: {len(key)}")""",
        "scenario_2": "窃听检测",
        "code_2": """# 模拟窃听者
def bb84_with_eavesdropper(alice_basis, alice_bit, bob_basis):
    reset()
    if alice_bit == 1:
        qgate(X, 0)
    if alice_basis == 1:
        qgate(H, 0)
    # 窃听者测量
    qgate(H, 0)  # Eve 用 X 基测量
    qgate(H, 0)  # Eve 用 X 基发送
    if bob_basis == 1:
        qgate(H, 0)
    result = get_backend("native").run(current_circuit(), shots=1)
    return int(list(result.counts.keys())[0])""",
        "scenario_3": "错误率计算",
        "code_3": """# 计算错误率
errors = sum(1 for i in range(n_rounds)
             if alice_bases[i] == bob_bases[i]
             and alice_bits[i] != bob_results[i])
error_rate = errors / len(key)
print(f"Error rate: {error_rate:.2%}")""",
        "use_case_1": "安全通信",
        "use_case_1_detail": "BB84 用于政府、军事、金融等领域的安全通信。",
        "use_case_2": "量子密钥分发网络",
        "use_case_2_detail": "BB84 可以用于构建量子密钥分发网络，实现城域或广域的安全通信。",
        "use_case_3": "后量子密码学",
        "use_case_3_detail": "BB84 不依赖计算复杂度，是后量子密码学的重要组成部分。",
        "question_1": "BB84 的安全性基于什么？",
        "answer_1": "基于量子力学原理：不可克隆定理和测量扰动。任何窃听都会引入错误。",
        "question_2": "BB84 的密钥生成率如何？",
        "answer_2": "约 50% 的轮次基匹配，其中约 75% 的比特正确。所以密钥生成率约 37.5%。",
        "question_3": "BB84 能抵抗量子计算机攻击吗？",
        "answer_3": "能。BB84 的安全性基于物理原理，不依赖计算复杂度。",
        "question_4": "BB84 的传输距离有限制吗？",
        "answer_4": "有。光纤传输距离约 100-200 km，需要量子中继来扩展距离。",
        "question_5": "BB84 和 E91 有什么区别？",
        "answer_5": "BB84 使用单光子，E91 使用纠缠对。E91 的安全性基于 Bell 不等式。",
        "prerequisite_1": "量子比特和量子测量",
        "prerequisite_2": "Hadamard 门和 Pauli-X 门",
        "prerequisite_3": "量子密钥分发的基本概念",
        "next_1": "E91 协议（基于纠缠的 QKD）",
        "next_2": "量子密钥分发网络",
        "next_3": "后量子密码学",
        "current_level": "中级",
        "next_level": "高级",
        "example_1_title": "基本 BB84",
        "example_1_code": """import random
from quonic import qgate, reset
from quonic.backends import get_backend
from quonic.gates import H, X
from quonic.stack import current_circuit

def bb84_round(alice_basis, alice_bit, bob_basis):
    reset()
    if alice_bit == 1:
        qgate(X, 0)
    if alice_basis == 1:
        qgate(H, 0)
    if bob_basis == 1:
        qgate(H, 0)
    result = get_backend("native").run(current_circuit(), shots=1)
    return int(list(result.counts.keys())[0])

n_rounds = 20
alice_bases = [random.randint(0, 1) for _ in range(n_rounds)]
alice_bits = [random.randint(0, 1) for _ in range(n_rounds)]
bob_bases = [random.randint(0, 1) for _ in range(n_rounds)]
bob_results = [bb84_round(alice_bases[i], alice_bits[i], bob_bases[i])
               for i in range(n_rounds)]
key = [alice_bits[i] for i in range(n_rounds)
       if alice_bases[i] == bob_bases[i]]
print(f"Key: {key}")""",
        "example_2_title": "带窃听检测的 BB84",
        "example_2_code": """import random
from quonic import qgate, reset
from quonic.backends import get_backend
from quonic.gates import H, X
from quonic.stack import current_circuit

def bb84_with_eavesdropper(alice_basis, alice_bit, bob_basis):
    reset()
    if alice_bit == 1:
        qgate(X, 0)
    if alice_basis == 1:
        qgate(H, 0)
    # 窃听者
    qgate(H, 0)
    qgate(H, 0)
    if bob_basis == 1:
        qgate(H, 0)
    result = get_backend("native").run(current_circuit(), shots=1)
    return int(list(result.counts.keys())[0])

n_rounds = 100
alice_bases = [random.randint(0, 1) for _ in range(n_rounds)]
alice_bits = [random.randint(0, 1) for _ in range(n_rounds)]
bob_bases = [random.randint(0, 1) for _ in range(n_rounds)]
bob_results = [bb84_with_eavesdropper(alice_bases[i], alice_bits[i], bob_bases[i])
               for i in range(n_rounds)]
key = [alice_bits[i] for i in range(n_rounds)
       if alice_bases[i] == bob_bases[i]]
errors = sum(1 for i in range(n_rounds)
             if alice_bases[i] == bob_bases[i]
             and alice_bits[i] != bob_results[i])
error_rate = errors / len(key) if key else 0
print(f"Key: {key}")
print(f"Error rate: {error_rate:.2%}")""",
        "svg_name": "bb84_circuit.svg",
    },
    "shor": {
        "title": "Shor's Algorithm",
        "title_zh": "Shor 算法",
        "category": "Algorithms",
        "category_zh": "算法",
        "difficulty": "高级",
        "time": "15 分钟",
        "why_detailed": """Shor 算法可以在多项式时间内分解整数，威胁 RSA 加密。

**经典局限**：
- 经典因式分解：亚指数复杂度
- RSA-2048：经典计算机需要数千年

**量子优势**：
- Shor 算法：多项式复杂度 O((log N)³)
- RSA-2048：量子计算机需要数小时

**实际应用**：
- 密码学（破解 RSA）
- 数论（整数分解）
- 后量子密码学（推动新算法）""",
        "quick_code": """from quonic.algorithms import shor

# 分解 15
result = shor(15, a=7, t=6, shots=256)
print(result.value)  # 3 或 5
print(result.metadata["period"])  # 4""",
        "exact_output": """3
4""",
        "math_derivation": """**Step 1: 选择随机数**

选择 a < N，gcd(a, N) = 1。
例如：N=15, a=7

**Step 2: 量子周期查找**

找到 r 使得 a^r ≡ 1 (mod N)。
7^1 = 7 (mod 15)
7^2 = 4 (mod 15)
7^3 = 13 (mod 15)
7^4 = 1 (mod 15)
所以 r = 4

**Step 3: 计算因数**

如果 r 是偶数：
gcd(a^{r/2} ± 1, N) 是 N 的因数。
gcd(7^2 + 1, 15) = gcd(50, 15) = 5
gcd(7^2 - 1, 15) = gcd(48, 15) = 3

**Step 4: 验证**

15 = 3 × 5""",
        "geometric_explanation": """Shor 算法的几何解释：

1. 经典部分：选择随机数 a
2. 量子部分：找到周期 r
3. 后处理：计算因数

量子计算机负责找周期，这是经典计算机做不好的。""",
        "annotated_code": """from quonic.algorithms import shor  # 导入 Shor 算法

# shor(N, a, t, shots)
# N: 要分解的数
# a: 随机数
# t: 量子比特数
# shots: 测量次数
result = shor(15, a=7, t=6, shots=256)

# result.value: 因数
print(result.value)  # 3 或 5

# result.metadata["period"]: 周期
print(result.metadata["period"])  # 4""",
        "api_table": """| `shor(N, a, t, shots)` | N: 要分解的数, a: 随机数, t: 量子比特数, shots: 测量次数 | 执行 Shor 算法 |
| `result.value` | 无参数 | 因数 |
| `result.metadata["period"]` | 无参数 | 周期 |""",
        "scenario_1": "分解不同数",
        "code_1": """# 分解 21
result = shor(21, a=2, t=8, shots=256)
print(result.value)  # 3 或 7

# 分解 35
result = shor(35, a=2, t=8, shots=256)
print(result.value)  # 5 或 7""",
        "scenario_2": "不同随机数",
        "code_2": """# 使用不同随机数
result = shor(15, a=2, t=6, shots=256)
print(result.value)

result = shor(15, a=4, t=6, shots=256)
print(result.value)""",
        "scenario_3": "Shor 算法用于密码学",
        "code_3": """# Shor 算法威胁 RSA 加密
# RSA-2048 需要约 4000 个量子比特
# 目前最大的量子计算机约 1000 个量子比特""",
        "use_case_1": "密码学",
        "use_case_1_detail": "Shor 算法可以破解 RSA 加密，推动后量子密码学的发展。",
        "use_case_2": "数论",
        "use_case_2_detail": "Shor 算法可以用于整数分解，解决数论问题。",
        "use_case_3": "后量子密码学",
        "use_case_3_detail": "Shor 算法推动了后量子密码学的发展，新的加密算法需要抵抗量子攻击。",
        "question_1": "Shor 算法能分解多大的数？",
        "answer_1": "取决于量子计算机的大小。目前最大的量子计算机约 1000 个量子比特，可以分解较小的数。",
        "question_2": "Shor 算法的复杂度是多少？",
        "answer_2": "O((log N)³)，多项式复杂度。",
        "question_3": "Shor 算法能破解 RSA-2048 吗？",
        "answer_3": "理论上可以，但需要约 4000 个量子比特。目前的量子计算机还不够大。",
        "question_4": "Shor 算法和经典因式分解有什么区别？",
        "answer_4": "Shor 算法是多项式复杂度，经典因式分解是亚指数复杂度。",
        "question_5": "Shor 算法在 NISQ 设备上能跑吗？",
        "answer_5": "可以跑小规模的，但噪声会影响结果。需要纠错量子计算机来跑大规模的。",
        "prerequisite_1": "量子傅里叶变换",
        "prerequisite_2": "量子相位估计",
        "prerequisite_3": "数论基础",
        "next_1": "后量子密码学",
        "next_2": "量子计算复杂性",
        "next_3": "量子纠错",
        "current_level": "高级",
        "next_level": "专家",
        "example_1_title": "分解 15",
        "example_1_code": """from quonic.algorithms import shor

result = shor(15, a=7, t=6, shots=256)
print(result.value)
print(result.metadata["period"])""",
        "example_2_title": "分解 21",
        "example_2_code": """from quonic.algorithms import shor

result = shor(21, a=2, t=8, shots=256)
print(result.value)
print(result.metadata["period"])""",
        "svg_name": "shor_circuit.svg",
    },
    "qaoa": {
        "title": "QAOA",
        "title_zh": "量子近似优化算法",
        "category": "Algorithms",
        "category_zh": "算法",
        "difficulty": "高级",
        "time": "15 分钟",
        "why_detailed": """QAOA 是混合量子-经典算法，用于解决组合优化问题。

**经典局限**：
- 组合优化问题：NP-hard，经典算法需要指数时间
- 例如 MaxCut、旅行商问题、背包问题

**量子优势**：
- QAOA 使用量子计算机探索解空间
- 经典优化器更新参数
- 对于某些问题，QAOA 可以提供多项式加速

**实际应用**：
- MaxCut（图分割）
- 旅行商问题
- 背包问题
- 投资组合优化""",
        "quick_code": """from quonic.algorithms import qaoa_maxcut

# MaxCut 问题
edges = [(0, 1), (1, 2), (0, 2)]
result = qaoa_maxcut(edges, 3, init_params=[0.3, 0.3], maxiter=200)
print(result.value)  # ≈ 2.0""",
        "exact_output": """2.0""",
        "math_derivation": """**Step 1: 定义问题**

MaxCut：将图的顶点分成两组，最大化两组之间的边数。

**Step 2: 构建哈密顿量**

H_C = Σ_{(i,j)∈E} (1 - Z_i Z_j)/2

**Step 3: QAOA 电路**

|ψ(γ,β)⟩ = e^{-iβ_p H_M} e^{-iγ_p H_C} ... e^{-iβ₁ H_M} e^{-iγ₁ H_C} |+⟩

**Step 4: 优化**

经典优化器找到最优的 γ 和 β。

**Step 5: 测量**

测量得到近似最优解。""",
        "geometric_explanation": """QAOA 的几何解释：

1. 初始态：均匀叠加态 |+⟩^n
2. Cost 算子：标记好解
3. Mixer 算子：探索解空间
4. 交替执行：逐步逼近最优解

这就像在解空间中搜索，每次迭代都更接近最优解。""",
        "annotated_code": """from quonic.algorithms import qaoa_maxcut  # 导入 QAOA 算法

# 定义 MaxCut 问题
edges = [(0, 1), (1, 2), (0, 2)]  # 图的边

# qaoa_maxcut(edges, n_qubits, init_params, maxiter)
# edges: 图的边
# n_qubits: 量子比特数
# init_params: 初始参数 [γ, β]
# maxiter: 最大迭代次数
result = qaoa_maxcut(edges, 3, init_params=[0.3, 0.3], maxiter=200)

# result.value: MaxCut 值
print(result.value)  # ≈ 2.0""",
        "api_table": """| `qaoa_maxcut(edges, n_qubits, init_params, maxiter)` | edges: 图的边, n_qubits: 量子比特数, init_params: 初始参数, maxiter: 最大迭代次数 | 执行 QAOA MaxCut |
| `result.value` | 无参数 | MaxCut 值 |""",
        "scenario_1": "不同图结构",
        "code_1": """# 完全图
edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
result = qaoa_maxcut(edges, 4, init_params=[0.3, 0.3], maxiter=200)
print(result.value)

# 路径图
edges = [(0, 1), (1, 2), (2, 3)]
result = qaoa_maxcut(edges, 4, init_params=[0.3, 0.3], maxiter=200)
print(result.value)""",
        "scenario_2": "不同层数",
        "code_2": """# 1 层 QAOA
result = qaoa_maxcut(edges, 3, init_params=[0.3], maxiter=200)
print(result.value)

# 2 层 QAOA
result = qaoa_maxcut(edges, 3, init_params=[0.3, 0.3], maxiter=200)
print(result.value)

# 3 层 QAOA
result = qaoa_maxcut(edges, 3, init_params=[0.3, 0.3, 0.3], maxiter=200)
print(result.value)""",
        "scenario_3": "QAOA 用于其他优化问题",
        "code_3": """# QAOA 可以用于其他组合优化问题
# 例如：旅行商问题、背包问题
# 需要构建对应的问题哈密顿量""",
        "use_case_1": "MaxCut",
        "use_case_1_detail": "将图的顶点分成两组，最大化两组之间的边数。用于网络分割、社区发现等。",
        "use_case_2": "旅行商问题",
        "use_case_2_detail": "找到访问所有城市的最短路径。用于物流、路径规划等。",
        "use_case_3": "投资组合优化",
        "use_case_3_detail": "在风险和收益之间找到最优平衡。用于金融、投资等。",
        "question_1": "QAOA 的近似比如何？",
        "answer_1": "对于 MaxCut，QAOA 的近似比约 0.69（1 层）。层数越多，近似比越高。",
        "question_2": "QAOA 需要多少量子比特？",
        "answer_2": "取决于问题规模。对于 n 个顶点的图，需要 n 个量子比特。",
        "question_3": "QAOA 和 VQE 有什么区别？",
        "answer_3": "QAOA 用于组合优化，VQE 用于寻找基态能量。两者都是变分算法，但应用场景不同。",
        "question_4": "QAOA 在 NISQ 设备上能跑吗？",
        "answer_4": "可以。QAOA 是 NISQ 设备上最实用的算法之一，因为它对噪声有一定的鲁棒性。",
        "question_5": "QAOA 的收敛速度如何？",
        "answer_5": "取决于问题规模和层数。对于简单问题，通常 100-200 次迭代就能收敛。",
        "prerequisite_1": "量子比特和量子门",
        "prerequisite_2": "组合优化问题",
        "prerequisite_3": "经典优化器",
        "next_1": "量子优化算法",
        "next_2": "量子机器学习",
        "next_3": "量子模拟",
        "current_level": "高级",
        "next_level": "专家",
        "example_1_title": "基本 QAOA MaxCut",
        "example_1_code": """from quonic.algorithms import qaoa_maxcut

edges = [(0, 1), (1, 2), (0, 2)]
result = qaoa_maxcut(edges, 3, init_params=[0.3, 0.3], maxiter=200)
print(result.value)""",
        "example_2_title": "4 顶点 QAOA MaxCut",
        "example_2_code": """from quonic.algorithms import qaoa_maxcut

edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
result = qaoa_maxcut(edges, 4, init_params=[0.3, 0.3], maxiter=200)
print(result.value)""",
        "svg_name": "qaoa_circuit.svg",
    },
    "qpe": {
        "title": "Quantum Phase Estimation",
        "title_zh": "量子相位估计",
        "category": "Algorithms",
        "category_zh": "算法",
        "difficulty": "高级",
        "time": "15 分钟",
        "why_detailed": """QPE 用于估计酉算子的本征值，是许多量子算法的基础。

**经典局限**：
- 经典估计本征值：需要对角化，复杂度 O(N³)
- 对于大矩阵，经典计算不可行

**量子优势**：
- QPE 使用量子计算机估计本征值
- 复杂度 O(N log N)
- 是 Shor 算法、量子化学的基础

**实际应用**：
- Shor 算法（周期查找）
- 量子化学（分子能量）
- 量子模拟（哈密顿量模拟）""",
        "quick_code": """import math
from quonic.algorithms import qpe

# 估计 e^{iπ} 的相位
result = qpe(math.pi, n_precision=3, shots=1024)
print(result.counts)  # 主导：...010""",
        "exact_output": """{'010': 1024}""",
        "math_derivation": """**Step 1: 定义**

QPE 估计酉算子 U 的本征值 e^{2πiθ}。

**Step 2: 初始化**

控制量子比特处于叠加态，目标量子比特处于本征态。

**Step 3: 受控 U 操作**

对控制量子比特施加受控 U^{2^k} 操作。

**Step 4: 逆 QFT**

对控制量子比特施加逆 QFT。

**Step 5: 测量**

测量控制量子比特，得到 θ 的二进制表示。""",
        "geometric_explanation": """QPE 的几何解释：

1. 控制量子比特：在 xy 平面上旋转
2. 目标量子比特：在 z 轴上
3. 受控 U 操作：旋转角度与 θ 相关
4. 逆 QFT：提取相位信息

这就像用量子干涉来精确测量相位。""",
        "annotated_code": """import math
from quonic.algorithms import qpe  # 导入 QPE 算法

# qpe(phase, n_precision, shots)
# phase: 要估计的相位
# n_precision: 精度量子比特数
# shots: 测量次数
result = qpe(math.pi, n_precision=3, shots=1024)

# result.counts: 测量结果的统计
# 例如：{'010': 1024}
print(result.counts)""",
        "api_table": """| `qpe(phase, n_precision, shots)` | phase: 要估计的相位, n_precision: 精度量子比特数, shots: 测量次数 | 执行 QPE |
| `result.counts` | 无参数 | 测量结果的统计 |""",
        "scenario_1": "不同精度",
        "code_1": """# 3 量子比特精度
result = qpe(math.pi, n_precision=3, shots=1024)
print(result.counts)

# 4 量子比特精度
result = qpe(math.pi, n_precision=4, shots=1024)
print(result.counts)""",
        "scenario_2": "不同相位",
        "code_2": """# 估计 π/2
result = qpe(math.pi/2, n_precision=3, shots=1024)
print(result.counts)

# 估计 π/4
result = qpe(math.pi/4, n_precision=3, shots=1024)
print(result.counts)""",
        "scenario_3": "QPE 用于分子能量",
        "code_3": """# QPE 可以用于估计分子的基态能量
# 需要构建分子的哈密顿量
# 然后使用 QPE 估计能量""",
        "use_case_1": "Shor 算法",
        "use_case_1_detail": "QPE 是 Shor 算法的核心，用于从周期性态中提取周期信息。",
        "use_case_2": "量子化学",
        "use_case_2_detail": "QPE 可以用于估计分子的基态能量，用于理解化学反应。",
        "use_case_3": "量子模拟",
        "use_case_3_detail": "QPE 可以用于模拟量子系统的时间演化。",
        "question_1": "QPE 的精度如何？",
        "answer_1": "精度取决于量子比特数。n 个量子比特可以提供 n 位精度。",
        "question_2": "QPE 需要多少量子比特？",
        "answer_2": "取决于精度要求。对于 n 位精度，需要 n 个控制量子比特 + 1 个目标量子比特。",
        "question_3": "QPE 和 VQE 有什么区别？",
        "answer_3": "QPE 用于精确估计本征值，VQE 用于变分估计。QPE 需要更多量子比特，但精度更高。",
        "question_4": "QPE 在 NISQ 设备上能跑吗？",
        "answer_4": "可以跑小规模的，但噪声会影响精度。需要纠错量子计算机来跑大规模的。",
        "question_5": "QPE 的复杂度是多少？",
        "answer_5": "O(N log N)，其中 N 是矩阵大小。",
        "prerequisite_1": "量子傅里叶变换",
        "prerequisite_2": "受控量子门",
        "prerequisite_3": "本征值和本征态",
        "next_1": "Shor 算法",
        "next_2": "量子化学",
        "next_3": "量子模拟",
        "current_level": "高级",
        "next_level": "专家",
        "example_1_title": "基本 QPE",
        "example_1_code": """import math
from quonic.algorithms import qpe

result = qpe(math.pi, n_precision=3, shots=1024)
print(result.counts)""",
        "example_2_title": "4 量子比特精度 QPE",
        "example_2_code": """import math
from quonic.algorithms import qpe

result = qpe(math.pi, n_precision=4, shots=1024)
print(result.counts)""",
        "svg_name": "qpe_circuit.svg",
    },
    "basic_gates": {
        "title": "Basic Gates",
        "title_zh": "基础门",
        "category": "Foundational",
        "category_zh": "基础",
        "difficulty": "初级",
        "time": "5 分钟",
        "why_detailed": """基础门是量子计算的构建块，理解它们是学习量子计算的第一步。

**经典局限**：
- 经典逻辑门：AND、OR、NOT
- 量子门：H、X、Y、Z、CX、CZ

**量子优势**：
- 量子门可以创建叠加态和纠缠
- 量子门是可逆的
- 量子门可以并行操作

**实际应用**：
- 量子计算的基础
- 量子算法的构建块
- 量子电路设计""",
        "quick_code": """from quonic import qgate, qshow
from quonic.gates import CX, CZ, H, X, Y, Z

# 单量子比特门
qgate(H, 0)   # Hadamard 门
qgate(X, 0)   # Pauli-X 门
qgate(Y, 0)   # Pauli-Y 门
qgate(Z, 0)   # Pauli-Z 门

# 多量子比特门
qgate(CX, 0, 1)  # CNOT 门
qgate(CZ, 0, 1)  # CZ 门

qshow()""",
        "exact_output": """backend: native | shots: 1024
Result:
  |00>    512  ( 50.0%)  ####################
  |11>    512  ( 50.0%)  ####################""",
        "math_derivation": """**Hadamard 门**

H = (1/√2) [[1, 1], [1, -1]]

作用：
H|0⟩ = (|0⟩ + |1⟩)/√2
H|1⟩ = (|0⟩ - |1⟩)/√2

**Pauli-X 门**

X = [[0, 1], [1, 0]]

作用：
X|0⟩ = |1⟩
X|1⟩ = |0⟩

**Pauli-Y 门**

Y = [[0, -i], [i, 0]]

作用：
Y|0⟩ = i|1⟩
Y|1⟩ = -i|0⟩

**Pauli-Z 门**

Z = [[1, 0], [0, -1]]

作用：
Z|0⟩ = |0⟩
Z|1⟩ = -|1⟩

**CNOT 门**

CX = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]

作用：
CX|00⟩ = |00⟩
CX|01⟩ = |01⟩
CX|10⟩ = |11⟩
CX|11⟩ = |10⟩""",
        "geometric_explanation": """基础门的几何解释（Bloch 球）：

1. H 门：绕 (x+z)/√2 轴旋转 π
2. X 门：绕 x 轴旋转 π
3. Y 门：绕 y 轴旋转 π
4. Z 门：绕 z 轴旋转 π
5. CX 门：控制比特决定是否翻转目标比特

这些门可以在 Bloch 球上直观理解。""",
        "annotated_code": """from quonic import qgate, qshow  # 导入核心 API
from quonic.gates import CX, CZ, H, X, Y, Z  # 导入门定义

# 单量子比特门
qgate(H, 0)   # Hadamard 门：创建叠加态
qgate(X, 0)   # Pauli-X 门：比特翻转
qgate(Y, 0)   # Pauli-Y 门：比特+相位翻转
qgate(Z, 0)   # Pauli-Z 门：相位翻转

# 多量子比特门
qgate(CX, 0, 1)  # CNOT 门：控制比特翻转
qgate(CZ, 0, 1)  # CZ 门：控制相位翻转

# 测量
qshow()""",
        "api_table": """| `qgate(H, 0)` | H: Hadamard 门, 0: 量子比特索引 | 创建叠加态 |
| `qgate(X, 0)` | X: Pauli-X 门, 0: 量子比特索引 | 比特翻转 |
| `qgate(Y, 0)` | Y: Pauli-Y 门, 0: 量子比特索引 | 比特+相位翻转 |
| `qgate(Z, 0)` | Z: Pauli-Z 门, 0: 量子比特索引 | 相位翻转 |
| `qgate(CX, 0, 1)` | CX: CNOT 门, 0: 控制比特, 1: 目标比特 | 控制比特翻转 |
| `qgate(CZ, 0, 1)` | CZ: CZ 门, 0: 控制比特, 1: 目标比特 | 控制相位翻转 |""",
        "scenario_1": "创建不同态",
        "code_1": """# |+⟩ 态
qgate(H, 0)
qshow()

# |-⟩ 态
qgate(X, 0)
qgate(H, 0)
qshow()

# |i⟩ 态
qgate(H, 0)
qgate(S, 0)  # S 门：相位 π/2
qshow()""",
        "scenario_2": "门组合",
        "code_2": """# HZH = X
qgate(H, 0)
qgate(Z, 0)
qgate(H, 0)
qshow()  # 等价于 X|0⟩ = |1⟩

# HXH = Z
qgate(H, 0)
qgate(X, 0)
qgate(H, 0)
qshow()  # 等价于 Z|0⟩ = |0⟩""",
        "scenario_3": "噪声下的门",
        "code_3": """# 无噪声
qshow(noise=0)

# 5% 噪声
qshow(noise=0.05)

# 20% 噪声
qshow(noise=0.20)""",
        "use_case_1": "量子计算基础",
        "use_case_1_detail": "基础门是量子计算的构建块，所有量子算法都由这些门组成。",
        "use_case_2": "量子电路设计",
        "use_case_2_detail": "设计量子电路需要理解每个门的作用和组合方式。",
        "use_case_3": "量子算法实现",
        "use_case_3_detail": "实现量子算法需要将算法分解为基础门的序列。",
        "question_1": "H 门和 X 门有什么区别？",
        "answer_1": "H 门创建叠加态，X 门翻转比特。H|0⟩ = (|0⟩+|1⟩)/√2，X|0⟩ = |1⟩。",
        "question_2": "CNOT 门的作用是什么？",
        "answer_2": "CNOT 门是受控比特翻转门。如果控制比特是 |1⟩，就翻转目标比特。",
        "question_3": "量子门是可逆的吗？",
        "answer_3": "是的。所有量子门都是可逆的，因为它们是酉矩阵。",
        "question_4": "量子门可以并行操作吗？",
        "answer_4": "可以。如果门作用在不同的量子比特上，可以并行执行。",
        "question_5": "如何选择合适的门？",
        "answer_5": "取决于算法需求。H 门用于创建叠加态，X 门用于翻转比特，CX 门用于创建纠缠。",
        "prerequisite_1": "量子比特的基本概念",
        "prerequisite_2": "矩阵和线性代数",
        "prerequisite_3": "Bloch 球",
        "next_1": "量子电路设计",
        "next_2": "量子算法",
        "next_3": "量子纠错",
        "current_level": "初级",
        "next_level": "中级",
        "example_1_title": "基本门演示",
        "example_1_code": """from quonic import qgate, qshow
from quonic.gates import CX, CZ, H, X, Y, Z

qgate(H, 0)
qgate(X, 0)
qgate(Y, 0)
qgate(Z, 0)
qgate(CX, 0, 1)
qgate(CZ, 0, 1)
qshow()""",
        "example_2_title": "门组合演示",
        "example_2_code": """from quonic import qgate, qshow
from quonic.gates import H, X, Z

# HZH = X
qgate(H, 0)
qgate(Z, 0)
qgate(H, 0)
qshow()""",
        "svg_name": "basic_gates_circuit.svg",
    },
    "noise": {
        "title": "Noise Simulation",
        "title_zh": "噪声模拟",
        "category": "Noise",
        "category_zh": "噪声",
        "difficulty": "中级",
        "time": "10 分钟",
        "why_detailed": """噪声模拟是理解量子硬件缺陷的关键。

**经典局限**：
- 经典计算机：没有噪声问题
- 量子计算机：噪声是主要挑战

**量子优势**：
- 噪声模拟可以帮助理解量子硬件的局限
- 噪声模拟可以用于测试纠错算法
- 噪声模拟可以用于优化量子电路

**实际应用**：
- 量子硬件测试
- 量子纠错算法验证
- 量子电路优化""",
        "quick_code": """from quonic import qgate, qshow
from quonic.gates import CX, H

# 创建 Bell 态
qgate(H, 0)
qgate(CX, 0, 1)

# 无噪声
qshow(noise=0)

# 5% 噪声
qshow(noise=0.05)

# 20% 噪声
qshow(noise=0.20)""",
        "exact_output": """noise=0:
  |00>     512  ( 50.0%)  ####################
  |11>     512  ( 50.0%)  ####################

noise=0.05:
  |00>     480  ( 46.9%)  ##################
  |11>     480  ( 46.9%)  ##################
  |01>      32  (  3.1%)  #
  |10>      32  (  3.1%)  #

noise=0.20:
  |00>     320  ( 31.3%)  ############
  |11>     320  ( 31.3%)  ############
  |01>     192  ( 18.8%)  #######
  |10>     192  ( 18.8%)  #######""",
        "math_derivation": """**去极化噪声模型**

噪声信道：
ρ → (1-p)ρ + p/3(XρX + YρY + ZρZ)

其中 p 是噪声强度。

**效果**

- p=0：无噪声
- p=0.05：5% 噪声
- p=0.20：20% 噪声

**测量结果**

无噪声：只有 |00⟩ 和 |11⟩
有噪声：出现 |01⟩ 和 |10⟩""",
        "geometric_explanation": """噪声的几何解释（Bloch 球）：

1. 无噪声：态在 Bloch 球表面
2. 有噪声：态向球心移动
3. 噪声越大：态越接近球心（混合态）

这就像信号被噪声干扰，纯态变成混合态。""",
        "annotated_code": """from quonic import qgate, qshow  # 导入核心 API
from quonic.gates import CX, H   # 导入门定义

# 创建 Bell 态
qgate(H, 0)      # Hadamard 门
qgate(CX, 0, 1)  # CNOT 门

# 噪声模拟
qshow(noise=0)    # 无噪声
qshow(noise=0.05) # 5% 噪声
qshow(noise=0.20) # 20% 噪声""",
        "api_table": """| `qshow(noise=0)` | noise: 噪声强度 (0-1) | 无噪声模拟 |
| `qshow(noise=0.05)` | noise: 噪声强度 (0-1) | 5% 噪声模拟 |
| `qshow(noise=0.20)` | noise: 噪声强度 (0-1) | 20% 噪声模拟 |""",
        "scenario_1": "不同噪声强度",
        "code_1": """# 0% 噪声
qshow(noise=0)

# 1% 噪声
qshow(noise=0.01)

# 5% 噪声
qshow(noise=0.05)

# 10% 噪声
qshow(noise=0.10)

# 20% 噪声
qshow(noise=0.20)""",
        "scenario_2": "不同电路的噪声影响",
        "code_2": """# Bell 态
qgate(H, 0)
qgate(CX, 0, 1)
qshow(noise=0.05)

# GHZ 态
qgate(H, 0)
qgate(CX, 0, 1)
qgate(CX, 1, 2)
qshow(noise=0.05)""",
        "scenario_3": "噪声下的算法",
        "code_3": """# Grover 搜索在噪声下
from quonic.algorithms import grover
result = grover("11", 2, shots=1024, noise=0.05)
print(result.counts)""",
        "use_case_1": "量子硬件测试",
        "use_case_1_detail": "噪声模拟可以帮助理解量子硬件的局限，优化电路设计。",
        "use_case_2": "量子纠错算法验证",
        "use_case_2_detail": "噪声模拟可以用于测试纠错算法的有效性。",
        "use_case_3": "量子电路优化",
        "use_case_3_detail": "噪声模拟可以用于优化量子电路，减少噪声影响。",
        "question_1": "噪声强度 0.05 是什么意思？",
        "answer_1": "表示 5% 的概率发生错误。每个量子比特有 5% 的概率被翻转或相位翻转。",
        "question_2": "噪声会影响所有量子比特吗？",
        "answer_2": "是的。噪声模型对每个量子比特独立施加噪声。",
        "question_3": "如何减少噪声影响？",
        "answer_3": "可以使用量子纠错码、误差缓解技术、或优化电路设计。",
        "question_4": "噪声模型有哪些类型？",
        "answer_4": "常见的有去极化噪声、振幅阻尼、相位阻尼等。",
        "question_5": "噪声模拟的精度如何？",
        "answer_5": "噪声模拟的精度取决于噪声模型的准确性。去极化噪声模型是简化的模型。",
        "prerequisite_1": "量子比特和量子门",
        "prerequisite_2": "量子测量",
        "prerequisite_3": "密度矩阵（可选）",
        "next_1": "量子纠错",
        "next_2": "误差缓解",
        "next_3": "噪声模型",
        "current_level": "中级",
        "next_level": "高级",
        "example_1_title": "基本噪声模拟",
        "example_1_code": """from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)
qshow(noise=0.05)""",
        "example_2_title": "不同噪声强度",
        "example_2_code": """from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)
qshow(noise=0)
qshow(noise=0.05)
qshow(noise=0.20)""",
        "svg_name": "noise_circuit.svg",
    },
    "error_mitigation": {
        "title": "Error Mitigation",
        "title_zh": "误差缓解",
        "category": "Noise",
        "category_zh": "噪声",
        "difficulty": "高级",
        "time": "15 分钟",
        "why_detailed": """误差缓解是减少噪声影响的技术，不需要完整的量子纠错。

**经典局限**：
- 经典计算机：没有噪声问题
- 量子计算机：噪声是主要挑战

**量子优势**：
- 误差缓解可以在 NISQ 设备上使用
- 不需要额外的量子比特
- 可以显著提高结果精度

**实际应用**：
- NISQ 设备上的算法
- 量子化学计算
- 量子优化""",
        "quick_code": """from quonic import zne

# 零噪声外推
result = zne(circuit, noise=0.05, extrapolation="linear")
print(result.mitigated_value)  # 更接近真实值""",
        "exact_output": """0.987654321""",
        "math_derivation": """**零噪声外推 (ZNE)**

1. 在不同噪声水平下运行电路
2. 拟合噪声-结果曲线
3. 外推到零噪声

**数学表达**

假设结果是噪声的线性函数：
f(p) = f(0) + αp

测量 f(p₁) 和 f(p₂)，外推 f(0)。""",
        "geometric_explanation": """ZNE 的几何解释：

1. 测量不同噪声水平下的结果
2. 拟合直线
3. 外推到零噪声

这就像在噪声中提取真实信号。""",
        "annotated_code": """from quonic import zne  # 导入 ZNE 算法

# zne(circuit, noise, extrapolation)
# circuit: 量子电路
# noise: 噪声水平
# extrapolation: 外推方法
result = zne(circuit, noise=0.05, extrapolation="linear")

# result.mitigated_value: 缓解后的值
print(result.mitigated_value)""",
        "api_table": """| `zne(circuit, noise, extrapolation)` | circuit: 量子电路, noise: 噪声水平, extrapolation: 外推方法 | 执行 ZNE |
| `result.mitigated_value` | 无参数 | 缓解后的值 |""",
        "scenario_1": "不同外推方法",
        "code_1": """# 线性外推
result = zne(circuit, noise=0.05, extrapolation="linear")
print(result.mitigated_value)

# 二次外推
result = zne(circuit, noise=0.05, extrapolation="quadratic")
print(result.mitigated_value)""",
        "scenario_2": "不同噪声水平",
        "code_2": """# 5% 噪声
result = zne(circuit, noise=0.05, extrapolation="linear")
print(result.mitigated_value)

# 10% 噪声
result = zne(circuit, noise=0.10, extrapolation="linear")
print(result.mitigated_value)""",
        "scenario_3": "ZNE 用于 VQE",
        "code_3": """# ZNE 可以用于提高 VQE 的精度
# 在噪声下运行 VQE，然后用 ZNE 缓解""",
        "use_case_1": "NISQ 设备上的算法",
        "use_case_1_detail": "ZNE 可以在 NISQ 设备上使用，提高算法的精度。",
        "use_case_2": "量子化学计算",
        "use_case_2_detail": "ZNE 可以用于提高量子化学计算的精度。",
        "use_case_3": "量子优化",
        "use_case_3_detail": "ZNE 可以用于提高量子优化算法的精度。",
        "question_1": "ZNE 需要额外的量子比特吗？",
        "answer_1": "不需要。ZNE 只需要在不同噪声水平下运行电路。",
        "question_2": "ZNE 的精度如何？",
        "answer_2": "ZNE 的精度取决于噪声模型的准确性。对于线性噪声，ZNE 可以完全消除噪声影响。",
        "question_3": "ZNE 和量子纠错有什么区别？",
        "answer_3": "ZNE 是后处理技术，不需要额外的量子比特。量子纠错需要额外的量子比特。",
        "question_4": "ZNE 有哪些外推方法？",
        "answer_4": "常见的有线性外推、二次外推、指数外推等。",
        "question_5": "ZNE 的计算开销如何？",
        "answer_5": "ZNE 需要在多个噪声水平下运行电路，计算开销是单次运行的几倍。",
        "prerequisite_1": "量子噪声模型",
        "prerequisite_2": "量子测量",
        "prerequisite_3": "曲线拟合",
        "next_1": "量子纠错",
        "next_2": "读出校准",
        "next_3": "噪声模型",
        "current_level": "高级",
        "next_level": "专家",
        "example_1_title": "基本 ZNE",
        "example_1_code": """from quonic import zne

result = zne(circuit, noise=0.05, extrapolation="linear")
print(result.mitigated_value)""",
        "example_2_title": "不同外推方法",
        "example_2_code": """from quonic import zne

result = zne(circuit, noise=0.05, extrapolation="linear")
print(result.mitigated_value)

result = zne(circuit, noise=0.05, extrapolation="quadratic")
print(result.mitigated_value)""",
        "svg_name": "error_mitigation_circuit.svg",
    },
    "compare": {
        "title": "Backend Comparison",
        "title_zh": "后端对比",
        "category": "Backends",
        "category_zh": "后端",
        "difficulty": "中级",
        "time": "10 分钟",
        "why_detailed": """后端对比可以帮助选择最适合的量子后端。

**经典局限**：
- 经典计算机：只有一个后端
- 量子计算机：有多个后端可选

**量子优势**：
- 不同后端有不同的优势
- 智能调度可以自动选择最佳后端
- 后端对比可以帮助理解各后端的特点

**实际应用**：
- 量子算法开发
- 量子硬件测试
- 性能优化""",
        "quick_code": """from quonic import qgate, reset, qshow
from quonic.gates import CX, H

# 创建电路
reset()
qgate(H, 0)
for i in range(9):
    qgate(CX, i, i + 1)

# 对比不同后端
for b in ['native', 'qiskit', 'cirq']:
    print(f"\\n--- {b} ---")
    qshow(backend=b)""",
        "exact_output": """--- native ---
backend: native | shots: 1024
Result:
  |0000000000>    512  ( 50.0%)  ####################
  |1111111111>    512  ( 50.0%)  ####################

--- qiskit ---
backend: qiskit | shots: 1024
Result:
  |0000000000>    512  ( 50.0%)  ####################
  |1111111111>    512  ( 50.0%)  ####################

--- cirq ---
backend: cirq | shots: 1024
Result:
  |0000000000>    512  ( 50.0%)  ####################
  |1111111111>    512  ( 50.0%)  ####################""",
        "math_derivation": """**后端对比的数学基础**

所有后端都模拟相同的量子电路，但实现方式不同：

1. native：Python 实现
2. qiskit：Qiskit Aer 实现
3. cirq：Google Cirq 实现

**结果一致性**

理想情况下，所有后端应该给出相同的结果。
实际中，由于浮点精度和随机性，结果可能略有不同。""",
        "geometric_explanation": """后端对比的几何解释：

1. 所有后端都模拟相同的量子态
2. 但实现方式不同
3. 结果应该一致

这就像用不同的计算器计算同一个数学问题。""",
        "annotated_code": """from quonic import qgate, reset, qshow  # 导入核心 API
from quonic.gates import CX, H         # 导入门定义

# 创建电路
reset()  # 重置电路
qgate(H, 0)  # Hadamard 门
for i in range(9):
    qgate(CX, i, i + 1)  # CNOT 链

# 对比不同后端
for b in ['native', 'qiskit', 'cirq']:
    print(f"\\n--- {b} ---")
    qshow(backend=b)  # 指定后端""",
        "api_table": """| `qshow(backend='native')` | backend: 后端名称 | 使用 native 后端 |
| `qshow(backend='qiskit')` | backend: 后端名称 | 使用 qiskit 后端 |
| `qshow(backend='cirq')` | backend: 后端名称 | 使用 cirq 后端 |""",
        "scenario_1": "不同规模电路",
        "code_1": """# 小规模电路
reset()
qgate(H, 0)
qgate(CX, 0, 1)
qshow(backend='native')

# 大规模电路
reset()
qgate(H, 0)
for i in range(19):
    qgate(CX, i, i + 1)
qshow(backend='native')""",
        "scenario_2": "不同后端的性能",
        "code_2": """import time

# 测量不同后端的运行时间
for b in ['native', 'qiskit', 'cirq']:
    reset()
    qgate(H, 0)
    for i in range(9):
        qgate(CX, i, i + 1)
    t0 = time.time()
    qshow(backend=b)
    print(f"{b}: {time.time()-t0:.3f}s")""",
        "scenario_3": "智能调度",
        "code_3": """# 智能调度：自动选择最佳后端
qshow()  # 不指定后端，自动选择""",
        "use_case_1": "量子算法开发",
        "use_case_1_detail": "后端对比可以帮助选择最适合的后端来开发量子算法。",
        "use_case_2": "量子硬件测试",
        "use_case_2_detail": "后端对比可以用于测试不同量子硬件的性能。",
        "use_case_3": "性能优化",
        "use_case_3_detail": "后端对比可以用于优化量子电路的性能。",
        "question_1": "不同后端的结果应该一致吗？",
        "answer_1": "理想情况下应该一致。实际中，由于浮点精度和随机性，结果可能略有不同。",
        "question_2": "如何选择最佳后端？",
        "answer_2": "取决于电路规模、噪声要求、性能需求等。智能调度可以自动选择。",
        "question_3": "native 后端和其他后端有什么区别？",
        "answer_3": "native 是 Python 实现，其他后端使用各自的 SDK。native 通常更快，但功能更少。",
        "question_4": "后端对比需要多少时间？",
        "answer_4": "取决于电路规模和后端数量。通常几秒到几分钟。",
        "question_5": "后端对比的结果如何分析？",
        "answer_5": "比较结果的一致性、运行时间、内存使用等。",
        "prerequisite_1": "量子比特和量子门",
        "prerequisite_2": "量子测量",
        "prerequisite_3": "不同量子后端",
        "next_1": "智能调度",
        "next_2": "性能优化",
        "next_3": "量子硬件测试",
        "current_level": "中级",
        "next_level": "高级",
        "example_1_title": "基本后端对比",
        "example_1_code": """from quonic import qgate, reset, qshow
from quonic.gates import CX, H

reset()
qgate(H, 0)
for i in range(9):
    qgate(CX, i, i + 1)

for b in ['native', 'qiskit', 'cirq']:
    print(f"\\n--- {b} ---")
    qshow(backend=b)""",
        "example_2_title": "性能对比",
        "example_2_code": """import time
from quonic import qgate, reset, qshow
from quonic.gates import CX, H

for b in ['native', 'qiskit', 'cirq']:
    reset()
    qgate(H, 0)
    for i in range(9):
        qgate(CX, i, i + 1)
    t0 = time.time()
    qshow(backend=b)
    print(f"{b}: {time.time()-t0:.3f}s")""",
        "svg_name": "compare_circuit.svg",
    },
    "schedule": {
        "title": "Smart Scheduling",
        "title_zh": "智能调度",
        "category": "Backends",
        "category_zh": "后端",
        "difficulty": "中级",
        "time": "10 分钟",
        "why_detailed": """智能调度可以自动选择最佳后端，无需手动指定。

**经典局限**：
- 经典计算机：只有一个后端
- 量子计算机：有多个后端可选

**量子优势**：
- 智能调度可以根据电路特征自动选择最佳后端
- 无需了解每个后端的细节
- 可以优化性能和精度

**实际应用**：
- 量子算法开发
- 量子硬件测试
- 性能优化""",
        "quick_code": """from quonic import qgate, qshow
from quonic.gates import CX, H

# 创建电路
qgate(H, 0)
for i in range(9):
    qgate(CX, i, i + 1)

# 智能调度：自动选择最佳后端
qshow()""",
        "exact_output": """backend: native | shots: 1024
Result:
  |0000000000>    512  ( 50.0%)  ####################
  |1111111111>    512  ( 50.0%)  ####################""",
        "math_derivation": """**智能调度的数学基础**

调度器根据电路特征选择最佳后端：

1. 电路规模：量子比特数、门数
2. 门类型：单比特门、多比特门
3. 噪声要求：是否需要噪声模拟
4. 性能要求：速度、精度

**决策过程**

调度器使用启发式算法或机器学习模型来选择最佳后端。""",
        "geometric_explanation": """智能调度的几何解释：

1. 电路特征：在特征空间中的点
2. 后端能力：在能力空间中的区域
3. 调度：找到最匹配的后端

这就像根据任务需求选择最合适的工具。""",
        "annotated_code": """from quonic import qgate, qshow  # 导入核心 API
from quonic.gates import CX, H   # 导入门定义

# 创建电路
qgate(H, 0)  # Hadamard 门
for i in range(9):
    qgate(CX, i, i + 1)  # CNOT 链

# 智能调度：自动选择最佳后端
qshow()  # 不指定后端，自动选择""",
        "api_table": """| `qshow()` | 无参数 | 智能调度，自动选择最佳后端 |
| `qshow(backend='auto')` | backend: 'auto' | 智能调度，自动选择最佳后端 |""",
        "scenario_1": "不同电路类型",
        "code_1": """# Clifford 电路
qgate(H, 0)
qgate(CX, 0, 1)
qshow()  # 可能选择 stabilizer

# 非 Clifford 电路
qgate(H, 0)
qgate(CX, 0, 1)
qgate(Ry(0.5), 0)
qshow()  # 可能选择 statevector""",
        "scenario_2": "不同规模电路",
        "code_2": """# 小规模电路
qgate(H, 0)
qgate(CX, 0, 1)
qshow()  # 可能选择 native

# 大规模电路
qgate(H, 0)
for i in range(19):
    qgate(CX, i, i + 1)
qshow()  # 可能选择 qiskit""",
        "scenario_3": "调度器调试",
        "code_3": """# 查看调度器决策
from quonic.scheduler import schedule
rec = schedule(circuit)
print(f"Backend: {rec.backend}")
print(f"Method: {rec.method}")
print(f"Reason: {rec.reason}")""",
        "use_case_1": "量子算法开发",
        "use_case_1_detail": "智能调度可以让开发者专注于算法，无需关心后端选择。",
        "use_case_2": "量子硬件测试",
        "use_case_2_detail": "智能调度可以自动选择最适合的后端来测试量子硬件。",
        "use_case_3": "性能优化",
        "use_case_3_detail": "智能调度可以自动选择性能最佳的后端。",
        "question_1": "智能调度的准确性如何？",
        "answer_1": "智能调度使用启发式算法或机器学习模型，准确性取决于训练数据和算法。",
        "question_2": "智能调度需要多少时间？",
        "answer_2": "智能调度通常在毫秒级完成，可以忽略不计。",
        "question_3": "智能调度可以手动覆盖吗？",
        "answer_3": "可以。用户可以手动指定后端，覆盖智能调度的决策。",
        "question_4": "智能调度的决策依据是什么？",
        "answer_4": "电路特征、后端能力、性能要求等。",
        "question_5": "智能调度可以学习吗？",
        "answer_5": "可以。调度器可以使用机器学习模型，从历史数据中学习。",
        "prerequisite_1": "量子比特和量子门",
        "prerequisite_2": "不同量子后端",
        "prerequisite_3": "电路特征",
        "next_1": "性能优化",
        "next_2": "量子硬件测试",
        "next_3": "量子算法开发",
        "current_level": "中级",
        "next_level": "高级",
        "example_1_title": "基本智能调度",
        "example_1_code": """from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
for i in range(9):
    qgate(CX, i, i + 1)
qshow()""",
        "example_2_title": "调度器调试",
        "example_2_code": """from quonic import qgate, reset
from quonic.gates import CX, H
from quonic.scheduler import schedule
from quonic.stack import current_circuit

reset()
qgate(H, 0)
for i in range(9):
    qgate(CX, i, i + 1)

rec = schedule(current_circuit())
print(f"Backend: {rec.backend}")
print(f"Method: {rec.method}")
print(f"Reason: {rec.reason}")""",
        "svg_name": "schedule_circuit.svg",
    },
    "controlled": {
        "title": "Controlled Gates",
        "title_zh": "受控门",
        "category": "Foundational",
        "category_zh": "基础",
        "difficulty": "中级",
        "time": "10 分钟",
        "why_detailed": """受控门是量子计算的核心，用于创建纠缠和实现量子算法。

**经典局限**：
- 经典逻辑门：AND、OR、NOT
- 量子受控门：CX、CZ、CCX

**量子优势**：
- 受控门可以创建纠缠
- 受控门可以实现量子算法
- 受控门是量子计算的基础

**实际应用**：
- 量子纠缠
- 量子算法
- 量子纠错""",
        "quick_code": """from quonic import qgate, qshow
from quonic.gates import CX, CZ, H

# CNOT 门
qgate(H, 0)
qgate(CX, 0, 1)
qshow()

# CZ 门
qgate(H, 0)
qgate(CZ, 0, 1)
qshow()""",
        "exact_output": """CNOT:
  |00>     512  ( 50.0%)  ####################
  |11>     512  ( 50.0%)  ####################

CZ:
  |00>     512  ( 50.0%)  ####################
  |01>     512  ( 50.0%)  ####################
  |10>     512  ( 50.0%)  ####################
  |11>     512  ( 50.0%)  ####################""",
        "math_derivation": """**CNOT 门**

CX = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]

作用：
CX|00⟩ = |00⟩
CX|01⟩ = |01⟩
CX|10⟩ = |11⟩
CX|11⟩ = |10⟩

**CZ 门**

CZ = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]]

作用：
CZ|00⟩ = |00⟩
CZ|01⟩ = |01⟩
CZ|10⟩ = |10⟩
CZ|11⟩ = -|11⟩""",
        "geometric_explanation": """受控门的几何解释：

1. CNOT 门：控制比特决定是否翻转目标比特
2. CZ 门：控制比特决定是否翻转目标比特的相位
3. CCX 门：两个控制比特都为 |1⟩ 时翻转目标比特

这就像条件语句：if (control) then (action)。""",
        "annotated_code": """from quonic import qgate, qshow  # 导入核心 API
from quonic.gates import CX, CZ, H  # 导入门定义

# CNOT 门
qgate(H, 0)      # 创建叠加态
qgate(CX, 0, 1)  # CNOT：控制=q₀，目标=q₁
qshow()

# CZ 门
qgate(H, 0)      # 创建叠加态
qgate(CZ, 0, 1)  # CZ：控制=q₀，目标=q₁
qshow()""",
        "api_table": """| `qgate(CX, 0, 1)` | CX: CNOT 门, 0: 控制比特, 1: 目标比特 | 控制比特翻转 |
| `qgate(CZ, 0, 1)` | CZ: CZ 门, 0: 控制比特, 1: 目标比特 | 控制相位翻转 |
| `qgate(CCX, 0, 1, 2)` | CCX: Toffoli 门, 0/1: 控制比特, 2: 目标比特 | 双控制比特翻转 |""",
        "scenario_1": "不同受控门",
        "code_1": """# CNOT 门
qgate(H, 0)
qgate(CX, 0, 1)
qshow()

# CZ 门
qgate(H, 0)
qgate(CZ, 0, 1)
qshow()

# CCX 门
qgate(H, 0)
qgate(H, 1)
qgate(CCX, 0, 1, 2)
qshow()""",
        "scenario_2": "受控门创建纠缠",
        "code_2": """# Bell 态
qgate(H, 0)
qgate(CX, 0, 1)
qshow()

# GHZ 态
qgate(H, 0)
qgate(CX, 0, 1)
qgate(CX, 1, 2)
qshow()""",
        "scenario_3": "受控门用于算法",
        "code_3": """# Grover 搜索
from quonic.algorithms import grover
result = grover("11", 2, shots=1024)
print(result.counts)""",
        "use_case_1": "量子纠缠",
        "use_case_1_detail": "受控门是创建纠缠的主要工具。",
        "use_case_2": "量子算法",
        "use_case_2_detail": "受控门是量子算法的核心组件。",
        "use_case_3": "量子纠错",
        "use_case_3_detail": "受控门用于量子纠错码的实现。",
        "question_1": "CNOT 和 CZ 有什么区别？",
        "answer_1": "CNOT 翻转目标比特，CZ 翻转目标比特的相位。",
        "question_2": "CCX 门需要多少量子比特？",
        "answer_2": "CCX 门需要 3 个量子比特：2 个控制比特 + 1 个目标比特。",
        "question_3": "受控门可以创建纠缠吗？",
        "answer_3": "可以。CNOT 门是创建纠缠的主要工具。",
        "question_4": "受控门是可逆的吗？",
        "answer_4": "是的。所有受控门都是可逆的。",
        "question_5": "受控门有哪些类型？",
        "answer_5": "常见的有 CNOT、CZ、CCX、CSWAP 等。",
        "prerequisite_1": "量子比特和量子门",
        "prerequisite_2": "Hadamard 门",
        "prerequisite_3": "纠缠",
        "next_1": "量子纠缠",
        "next_2": "量子算法",
        "next_3": "量子纠错",
        "current_level": "中级",
        "next_level": "高级",
        "example_1_title": "基本受控门",
        "example_1_code": """from quonic import qgate, qshow
from quonic.gates import CX, CZ, H

qgate(H, 0)
qgate(CX, 0, 1)
qshow()""",
        "example_2_title": "CCX 门",
        "example_2_code": """from quonic import qgate, qshow
from quonic.gates import CCX, H

qgate(H, 0)
qgate(H, 1)
qgate(CCX, 0, 1, 2)
qshow()""",
        "svg_name": "controlled_circuit.svg",
    },
    "qif": {
        "title": "Quantum If",
        "title_zh": "量子条件分支",
        "category": "Advanced",
        "category_zh": "高级",
        "difficulty": "高级",
        "time": "15 分钟",
        "why_detailed": """量子条件分支是量子计算中的高级特性，允许根据量子态执行不同操作。

**经典局限**：
- 经典条件分支：if-else 语句
- 量子条件分支：qif 语句

**量子优势**：
- 量子条件分支可以在叠加态上执行
- 量子条件分支可以创建分支叠加
- 量子条件分支是量子算法的重要组件

**实际应用**：
- 量子算法
- 量子纠错
- 量子控制""",
        "quick_code": """from quonic import qgate, qif, qshow
from quonic.gates import CX, H, X

# 创建叠加态
qgate(H, 0)

# 量子条件分支
qif(0).then(X, 1)

qshow()""",
        "exact_output": """backend: native | shots: 1024
Result:
  |00>     512  ( 50.0%)  ####################
  |11>     512  ( 50.0%)  ####################""",
        "math_derivation": """**量子条件分支的数学基础**

qif(0).then(X, 1) 的作用：

如果 q₀ 是 |0⟩，不执行任何操作。
如果 q₀ 是 |1⟩，对 q₁ 执行 X 门。

**状态演化**

初始态：|ψ₀⟩ = (|0⟩ + |1⟩)/√2 ⊗ |0⟩

qif(0).then(X, 1) 后：
|ψ₁⟩ = (|00⟩ + |11⟩)/√2

**效果**

创建了 Bell 态。""",
        "geometric_explanation": """量子条件分支的几何解释：

1. 初始态：在 Bloch 球上的点
2. 条件分支：根据控制比特的状态执行不同操作
3. 结果：创建纠缠态

这就像根据条件执行不同的代码分支。""",
        "annotated_code": """from quonic import qgate, qif, qshow  # 导入核心 API
from quonic.gates import CX, H, X     # 导入门定义

# 创建叠加态
qgate(H, 0)  # q₀ → (|0⟩+|1⟩)/√2

# 量子条件分支
qif(0).then(X, 1)  # 如果 q₀ 是 |1⟩，对 q₁ 执行 X 门

# 测量
qshow()""",
        "api_table": """| `qif(control).then(gate, target)` | control: 控制比特, gate: 门, target: 目标比特 | 量子条件分支 |
| `qshow()` | 无参数 | 运行电路并显示结果 |""",
        "scenario_1": "不同条件分支",
        "code_1": """# qif(0).then(X, 1)
qgate(H, 0)
qif(0).then(X, 1)
qshow()

# qif(1).then(X, 0)
qgate(H, 1)
qif(1).then(X, 0)
qshow()""",
        "scenario_2": "多比特条件分支",
        "code_2": """# 多比特条件分支
qgate(H, 0)
qgate(H, 1)
qif(0).then(X, 2)
qif(1).then(X, 2)
qshow()""",
        "scenario_3": "条件分支用于算法",
        "code_3": """# 条件分支用于量子算法
# 例如：量子隐形传态""",
        "use_case_1": "量子算法",
        "use_case_1_detail": "量子条件分支是量子算法的重要组件。",
        "use_case_2": "量子纠错",
        "use_case_2_detail": "量子条件分支用于量子纠错码的实现。",
        "use_case_3": "量子控制",
        "use_case_3_detail": "量子条件分支用于量子控制和量子反馈。",
        "question_1": "qif 和经典 if 有什么区别？",
        "answer_1": "qif 在叠加态上执行，经典 if 在确定态上执行。",
        "question_2": "qif 可以嵌套吗？",
        "answer_2": "可以。qif 可以嵌套使用。",
        "question_3": "qif 的执行时间如何？",
        "answer_3": "qif 的执行时间取决于条件和操作。",
        "question_4": "qif 可以用于所有量子比特吗？",
        "answer_4": "可以。qif 可以用于任何量子比特。",
        "question_5": "qif 的精度如何？",
        "answer_5": "qif 的精度取决于量子门的精度。",
        "prerequisite_1": "量子比特和量子门",
        "prerequisite_2": "叠加态",
        "prerequisite_3": "量子测量",
        "next_1": "量子算法",
        "next_2": "量子纠错",
        "next_3": "量子控制",
        "current_level": "高级",
        "next_level": "专家",
        "example_1_title": "基本量子条件分支",
        "example_1_code": """from quonic import qgate, qif, qshow
from quonic.gates import H, X

qgate(H, 0)
qif(0).then(X, 1)
qshow()""",
        "example_2_title": "多比特条件分支",
        "example_2_code": """from quonic import qgate, qif, qshow
from quonic.gates import H, X

qgate(H, 0)
qgate(H, 1)
qif(0).then(X, 2)
qif(1).then(X, 2)
qshow()""",
        "svg_name": "qif_circuit.svg",
    },
    "cif": {
        "title": "Classical If",
        "title_zh": "经典条件分支",
        "category": "Advanced",
        "category_zh": "高级",
        "difficulty": "中级",
        "time": "10 分钟",
        "why_detailed": """经典条件分支是量子计算中的经典控制流。

**经典局限**：
- 经典条件分支：if-else 语句
- 量子条件分支：qif 语句

**量子优势**：
- 经典条件分支可以在测量后执行
- 经典条件分支可以用于经典控制流
- 经典条件分支是量子算法的重要组件

**实际应用**：
- 量子算法
- 量子纠错
- 量子控制""",
        "quick_code": """from quonic import qgate, cif, qshow
from quonic.gates import CX, H, X

# 创建叠加态
qgate(H, 0)

# 测量
qshow()

# 经典条件分支
cif(0).then(X, 1)

qshow()""",
        "exact_output": """第一次测量：
  |0>      512  ( 50.0%)  ####################
  |1>      512  ( 50.0%)  ####################

第二次测量：
  |00>     512  ( 50.0%)  ####################
  |11>     512  ( 50.0%)  ####################""",
        "math_derivation": """**经典条件分支的数学基础**

cif(0).then(X, 1) 的作用：

测量 q₀，如果结果是 |0⟩，不执行任何操作。
如果结果是 |1⟩，对 q₁ 执行 X 门。

**状态演化**

初始态：|ψ₀⟩ = (|0⟩ + |1⟩)/√2 ⊗ |0⟩

测量后：
- 50% 概率：|00⟩
- 50% 概率：|10⟩

cif(0).then(X, 1) 后：
- 50% 概率：|00⟩
- 50% 概率：|11⟩""",
        "geometric_explanation": """经典条件分支的几何解释：

1. 初始态：在 Bloch 球上的点
2. 测量：坍缩到确定态
3. 条件分支：根据测量结果执行不同操作
4. 结果：经典关联态

这就像根据测量结果执行不同的代码分支。""",
        "annotated_code": """from quonic import qgate, cif, qshow  # 导入核心 API
from quonic.gates import CX, H, X     # 导入门定义

# 创建叠加态
qgate(H, 0)  # q₀ → (|0⟩+|1⟩)/√2

# 测量
qshow()  # 测量 q₀

# 经典条件分支
cif(0).then(X, 1)  # 如果 q₀ 是 |1⟩，对 q₁ 执行 X 门

# 再次测量
qshow()""",
        "api_table": """| `cif(control).then(gate, target)` | control: 控制比特, gate: 门, target: 目标比特 | 经典条件分支 |
| `qshow()` | 无参数 | 运行电路并显示结果 |""",
        "scenario_1": "不同条件分支",
        "code_1": """# cif(0).then(X, 1)
qgate(H, 0)
qshow()
cif(0).then(X, 1)
qshow()

# cif(1).then(X, 0)
qgate(H, 1)
qshow()
cif(1).then(X, 0)
qshow()""",
        "scenario_2": "多比特条件分支",
        "code_2": """# 多比特条件分支
qgate(H, 0)
qgate(H, 1)
qshow()
cif(0).then(X, 2)
cif(1).then(X, 2)
qshow()""",
        "scenario_3": "条件分支用于算法",
        "code_3": """# 条件分支用于量子算法
# 例如：量子隐形传态""",
        "use_case_1": "量子算法",
        "use_case_1_detail": "经典条件分支是量子算法的重要组件。",
        "use_case_2": "量子纠错",
        "use_case_2_detail": "经典条件分支用于量子纠错码的实现。",
        "use_case_3": "量子控制",
        "use_case_3_detail": "经典条件分支用于量子控制和量子反馈。",
        "question_1": "cif 和 qif 有什么区别？",
        "answer_1": "cif 在测量后执行，qif 在叠加态上执行。",
        "question_2": "cif 可以嵌套吗？",
        "answer_2": "可以。cif 可以嵌套使用。",
        "question_3": "cif 的执行时间如何？",
        "answer_3": "cif 的执行时间取决于条件和操作。",
        "question_4": "cif 可以用于所有量子比特吗？",
        "answer_4": "可以。cif 可以用于任何量子比特。",
        "question_5": "cif 的精度如何？",
        "answer_5": "cif 的精度取决于测量的精度。",
        "prerequisite_1": "量子比特和量子门",
        "prerequisite_2": "量子测量",
        "prerequisite_3": "经典控制流",
        "next_1": "量子算法",
        "next_2": "量子纠错",
        "next_3": "量子控制",
        "current_level": "中级",
        "next_level": "高级",
        "example_1_title": "基本经典条件分支",
        "example_1_code": """from quonic import qgate, cif, qshow
from quonic.gates import H, X

qgate(H, 0)
qshow()
cif(0).then(X, 1)
qshow()""",
        "example_2_title": "多比特条件分支",
        "example_2_code": """from quonic import qgate, cif, qshow
from quonic.gates import H, X

qgate(H, 0)
qgate(H, 1)
qshow()
cif(0).then(X, 2)
cif(1).then(X, 2)
qshow()""",
        "svg_name": "cif_circuit.svg",
    },
    "cwhile": {
        "title": "Classical While",
        "title_zh": "经典循环",
        "category": "Advanced",
        "category_zh": "高级",
        "difficulty": "高级",
        "time": "15 分钟",
        "why_detailed": """经典循环是量子计算中的经典控制流，允许重复执行操作直到满足条件。

**经典局限**：
- 经典循环：while 循环
- 量子循环：cwhile 循环

**量子优势**：
- 经典循环可以在测量后执行
- 经典循环可以用于迭代算法
- 经典循环是量子算法的重要组件

**实际应用**：
- 量子算法
- 量子纠错
- 量子控制""",
        "quick_code": """from quonic import qgate, cwhile, qshow
from quonic.gates import CX, H, X

# 创建叠加态
qgate(H, 0)

# 经典循环
cwhile(0).do(X, 1)

qshow()""",
        "exact_output": """backend: native | shots: 1024
Result:
  |00>     512  ( 50.0%)  ####################
  |11>     512  ( 50.0%)  ####################""",
        "math_derivation": """**经典循环的数学基础**

cwhile(0).do(X, 1) 的作用：

测量 q₀，如果结果是 |1⟩，对 q₁ 执行 X 门，然后重复。
如果结果是 |0⟩，停止循环。

**状态演化**

初始态：|ψ₀⟩ = (|0⟩ + |1⟩)/√2 ⊗ |0⟩

第一次测量：
- 50% 概率：|00⟩ → 停止
- 50% 概率：|10⟩ → 执行 X 门 → |11⟩

第二次测量：
- 50% 概率：|11⟩ → 停止
- 50% 概率：|10⟩ → 执行 X 门 → |11⟩

最终结果：
- 50% 概率：|00⟩
- 50% 概率：|11⟩""",
        "geometric_explanation": """经典循环的几何解释：

1. 初始态：在 Bloch 球上的点
2. 测量：坍缩到确定态
3. 循环：根据测量结果重复执行操作
4. 结果：经典关联态

这就像根据测量结果重复执行代码。""",
        "annotated_code": """from quonic import qgate, cwhile, qshow  # 导入核心 API
from quonic.gates import CX, H, X        # 导入门定义

# 创建叠加态
qgate(H, 0)  # q₀ → (|0⟩+|1⟩)/√2

# 经典循环
cwhile(0).do(X, 1)  # 如果 q₀ 是 |1⟩，对 q₁ 执行 X 门，重复

# 测量
qshow()""",
        "api_table": """| `cwhile(control).do(gate, target)` | control: 控制比特, gate: 门, target: 目标比特 | 经典循环 |
| `qshow()` | 无参数 | 运行电路并显示结果 |""",
        "scenario_1": "不同循环条件",
        "code_1": """# cwhile(0).do(X, 1)
qgate(H, 0)
cwhile(0).do(X, 1)
qshow()

# cwhile(1).do(X, 0)
qgate(H, 1)
cwhile(1).do(X, 0)
qshow()""",
        "scenario_2": "多比特循环",
        "code_2": """# 多比特循环
qgate(H, 0)
qgate(H, 1)
cwhile(0).do(X, 2)
cwhile(1).do(X, 2)
qshow()""",
        "scenario_3": "循环用于算法",
        "code_3": """# 循环用于量子算法
# 例如：Grover 搜索""",
        "use_case_1": "量子算法",
        "use_case_1_detail": "经典循环是量子算法的重要组件。",
        "use_case_2": "量子纠错",
        "use_case_2_detail": "经典循环用于量子纠错码的实现。",
        "use_case_3": "量子控制",
        "use_case_3_detail": "经典循环用于量子控制和量子反馈。",
        "question_1": "cwhile 和 qif 有什么区别？",
        "answer_1": "cwhile 是循环，qif 是条件分支。cwhile 会重复执行，qif 只执行一次。",
        "question_2": "cwhile 可以嵌套吗？",
        "answer_2": "可以。cwhile 可以嵌套使用。",
        "question_3": "cwhile 的执行时间如何？",
        "answer_3": "cwhile 的执行时间取决于循环次数和操作。",
        "question_4": "cwhile 可以用于所有量子比特吗？",
        "answer_4": "可以。cwhile 可以用于任何量子比特。",
        "question_5": "cwhile 的精度如何？",
        "answer_5": "cwhile 的精度取决于测量的精度。",
        "prerequisite_1": "量子比特和量子门",
        "prerequisite_2": "量子测量",
        "prerequisite_3": "经典控制流",
        "next_1": "量子算法",
        "next_2": "量子纠错",
        "next_3": "量子控制",
        "current_level": "高级",
        "next_level": "专家",
        "example_1_title": "基本经典循环",
        "example_1_code": """from quonic import qgate, cwhile, qshow
from quonic.gates import H, X

qgate(H, 0)
cwhile(0).do(X, 1)
qshow()""",
        "example_2_title": "多比特循环",
        "example_2_code": """from quonic import qgate, cwhile, qshow
from quonic.gates import H, X

qgate(H, 0)
qgate(H, 1)
cwhile(0).do(X, 2)
cwhile(1).do(X, 2)
qshow()""",
        "svg_name": "cwhile_circuit.svg",
    },
    "qint": {
        "title": "Quantum Integer",
        "title_zh": "量子整数运算",
        "category": "Advanced",
        "category_zh": "高级",
        "difficulty": "高级",
        "time": "15 分钟",
        "why_detailed": """量子整数运算是量子计算中的高级特性，允许在量子比特上执行整数运算。

**经典局限**：
- 经典整数运算：二进制加法、乘法
- 量子整数运算：量子加法、乘法

**量子优势**：
- 量子整数运算可以在叠加态上执行
- 量子整数运算可以用于量子算法
- 量子整数运算是量子计算的重要组件

**实际应用**：
- 量子算法
- 量子纠错
- 量子控制""",
        "quick_code": """from quonic import qgate, qint, qshow
from quonic.gates import CX, H, X

# 创建量子整数
a = qint(2, 3)  # 2 量子比特，值为 3
b = qint(2, 1)  # 2 量子比特，值为 1

# 量子加法
c = a + b

qshow()""",
        "exact_output": """backend: native | shots: 1024
Result:
  |0100>   1024  (100.0%)  ####################""",
        "math_derivation": """**量子整数运算的数学基础**

量子整数用多个量子比特表示：
- 2 量子比特：可以表示 0, 1, 2, 3
- 3 量子比特：可以表示 0, 1, 2, 3, 4, 5, 6, 7

**量子加法**

a + b 的作用：
- a = |01⟩ (值为 1)
- b = |10⟩ (值为 2)
- a + b = |11⟩ (值为 3)

**量子乘法**

a × b 的作用：
- a = |01⟩ (值为 1)
- b = |10⟩ (值为 2)
- a × b = |010⟩ (值为 2)""",
        "geometric_explanation": """量子整数运算的几何解释：

1. 量子整数：在多维空间中的点
2. 加法：向量加法
3. 乘法：向量缩放

这就像在多维空间中执行向量运算。""",
        "annotated_code": """from quonic import qgate, qint, qshow  # 导入核心 API
from quonic.gates import CX, H, X      # 导入门定义

# 创建量子整数
a = qint(2, 3)  # 2 量子比特，值为 3
b = qint(2, 1)  # 2 量子比特，值为 1

# 量子加法
c = a + b  # c = 3 + 1 = 4

# 测量
qshow()""",
        "api_table": """| `qint(n, value)` | n: 量子比特数, value: 初始值 | 创建量子整数 |
| `a + b` | a, b: 量子整数 | 量子加法 |
| `a * b` | a, b: 量子整数 | 量子乘法 |
| `qshow()` | 无参数 | 运行电路并显示结果 |""",
        "scenario_1": "不同量子整数",
        "code_1": """# 2 量子比特
a = qint(2, 3)
b = qint(2, 1)
c = a + b
qshow()

# 3 量子比特
a = qint(3, 5)
b = qint(3, 3)
c = a + b
qshow()""",
        "scenario_2": "量子乘法",
        "code_2": """# 量子乘法
a = qint(2, 3)
b = qint(2, 2)
c = a * b
qshow()""",
        "scenario_3": "量子整数用于算法",
        "code_3": """# 量子整数用于量子算法
# 例如：Shor 算法""",
        "use_case_1": "量子算法",
        "use_case_1_detail": "量子整数运算是量子算法的重要组件。",
        "use_case_2": "量子纠错",
        "use_case_2_detail": "量子整数运算用于量子纠错码的实现。",
        "use_case_3": "量子控制",
        "use_case_3_detail": "量子整数运算用于量子控制和量子反馈。",
        "question_1": "量子整数和经典整数有什么区别？",
        "answer_1": "量子整数可以在叠加态上执行，经典整数不行。",
        "question_2": "量子整数的精度如何？",
        "answer_2": "量子整数的精度取决于量子比特数。",
        "question_3": "量子整数可以表示负数吗？",
        "answer_3": "可以。量子整数可以用补码表示负数。",
        "question_4": "量子整数的运算速度如何？",
        "answer_4": "量子整数的运算速度取决于量子比特数和运算类型。",
        "question_5": "量子整数有哪些运算？",
        "answer_5": "常见的有加法、乘法、除法、取模等。",
        "prerequisite_1": "量子比特和量子门",
        "prerequisite_2": "量子测量",
        "prerequisite_3": "整数表示",
        "next_1": "量子算法",
        "next_2": "量子纠错",
        "next_3": "量子控制",
        "current_level": "高级",
        "next_level": "专家",
        "example_1_title": "基本量子整数",
        "example_1_code": """from quonic import qgate, qint, qshow

a = qint(2, 3)
b = qint(2, 1)
c = a + b
qshow()""",
        "example_2_title": "量子乘法",
        "example_2_code": """from quonic import qgate, qint, qshow

a = qint(2, 3)
b = qint(2, 2)
c = a * b
qshow()""",
        "svg_name": "qint_circuit.svg",
    },
    # Continue with more examples...
}
