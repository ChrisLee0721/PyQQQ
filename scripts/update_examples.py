"""Update all examples with bilingual documentation."""

import os

# Template for each example
TEMPLATE = '''"""[PROBLEM]

[PROBLEM_DESC]

## Application / 应用场景
[APPLICATION]

## How it works / 原理
[HOW_IT_WORKS]

## Output / 输出说明
[OUTPUT]

## Classical vs Quantum / 经典 vs 量子
[CLASSICAL_VS_QUANTUM]
"""

[CODE]
'''

# Example updates
EXAMPLES = {
    "bell": {
        "problem": "Create a maximally entangled state / 创建最大纠缠态",
        "problem_desc": "Bell state is the simplest quantum entanglement. Two qubits become correlated: measuring one instantly determines the other.\nBell 态是最简单的量子纠缠。两个量子比特关联：测量一个立即确定另一个。",
        "application": "- Quantum teleportation (隐形传态)\n- Superdense coding (超密编码)\n- Quantum key distribution (量子密钥分发)\n- Testing quantum hardware (测试量子硬件)",
        "how_it_works": "H gate creates superposition, CX gate creates entanglement.\nH 门创建叠加态，CX 门创建纠缠。",
        "output": "Roughly 50% |00⟩ and 50% |11⟩. No |01⟩ or |10⟩ (proves entanglement).\n约 50% |00⟩ 和 50% |11⟩。没有 |01⟩ 或 |10⟩（证明纠缠）。",
        "classical_vs_quantum": "Classical: can't create this correlation. Quantum: instant correlation regardless of distance.\n经典：无法创建这种关联。量子：无论距离多远都是即时关联。",
    },
    "grover": {
        "problem": "Search an unsorted database / 搜索无序数据库",
        "problem_desc": "Find a specific item in an unsorted list. Classical: O(N) queries. Quantum: O(√N) queries.\n在无序列表中找到特定项。经典：O(N) 次查询。量子：O(√N) 次查询。",
        "application": "- Database search (数据库搜索)\n- Cryptography: searching key space (密码学：搜索密钥空间)\n- Optimization: finding optimal solution (优化：寻找最优解)\n- SAT solving (SAT 求解)",
        "how_it_works": "Oracle marks target state, diffusion amplifies its probability.\nOracle 标记目标态，diffusion 放大概率。",
        "output": "Target state appears with ~99% probability after optimal iterations.\n目标态在最优迭代后以 ~99% 概率出现。",
        "classical_vs_quantum": "For N=4: classical needs 3 queries, quantum needs 1.\n对于 N=4：经典需要 3 次查询，量子需要 1 次。",
    },
    "vqe": {
        "problem": "Find ground state energy / 寻找基态能量",
        "problem_desc": "Variational Quantum Eigensolver finds the lowest energy of a quantum system.\n变分量子本征求解器找到量子系统的最低能量。",
        "application": "- Quantum chemistry: molecular ground states (量子化学：分子基态)\n- Materials science: new materials (材料科学：新材料)\n- Drug discovery: molecular properties (药物发现：分子性质)",
        "how_it_works": "Parameterized circuit + classical optimizer minimize energy expectation.\n参数化电路 + 经典优化器最小化能量期望值。",
        "output": "Energy value converges to exact ground state energy.\n能量值收敛到精确基态能量。",
        "classical_vs_quantum": "Classical: exponential scaling with system size. Quantum: polynomial.\n经典：随系统规模指数增长。量子：多项式。",
    },
    "qft": {
        "problem": "Quantum Fourier Transform / 量子傅里叶变换",
        "problem_desc": "Quantum version of DFT. Foundation for many quantum algorithms.\n量子版 DFT。许多量子算法的基础。",
        "application": "- Shor's algorithm (Shor 算法)\n- Quantum phase estimation (量子相位估计)\n- Quantum counting (量子计数)\n- Signal processing (信号处理)",
        "how_it_works": "H gates + controlled rotations create frequency-domain representation.\nH 门 + 受控旋转创建频域表示。",
        "output": "Transforms computational basis to Fourier basis.\n将计算基变换到傅里叶基。",
        "classical_vs_quantum": "Classical FFT: O(N log N). Quantum QFT: O(log²N) — exponential speedup.\n经典 FFT：O(N log N)。量子 QFT：O(log²N) — 指数加速。",
    },
    "teleportation": {
        "problem": "Teleport quantum state / 隐形传态量子态",
        "problem_desc": "Transfer quantum state from one location to another using entanglement.\n使用纠缠将量子态从一个位置传送到另一个位置。",
        "application": "- Quantum communication (量子通信)\n- Quantum networks (量子网络)\n- Distributed quantum computing (分布式量子计算)",
        "how_it_works": "Bell pair + Bell measurement + classical communication + correction.\nBell 对 + Bell 测量 + 经典通信 + 纠正。",
        "output": "Target qubit receives the original state (with classical corrections).\n目标量子比特接收原始态（需要经典纠正）。",
        "classical_vs_quantum": "Classical: can't transmit unknown quantum state. Quantum: instant transfer.\n经典：无法传输未知量子态。量子：即时传输。",
    },
}

def update_example(name, info):
    """Update an example with bilingual documentation."""
    path = f"examples/{name}/{name}.py"
    if not os.path.exists(path):
        # Try alternative naming
        for f in os.listdir(f"examples/{name}"):
            if f.endswith('.py'):
                path = f"examples/{name}/{f}"
                break

    with open(path, 'r', encoding='utf-8') as f:
        code = f.read()

    # Extract the actual code (after docstring)
    lines = code.split('\n')
    code_start = 0
    in_docstring = False
    for i, line in enumerate(lines):
        if '"""' in line:
            in_docstring = not in_docstring
            if not in_docstring:
                code_start = i + 1
                break

    actual_code = '\n'.join(lines[code_start:])

    # Build new content
    new_content = f'''"""{info["problem"]}

{info["problem_desc"]}

## Application / 应用场景
{info["application"]}

## How it works / 原理
{info["how_it_works"]}

## Output / 输出说明
{info["output"]}

## Classical vs Quantum / 经典 vs 量子
{info["classical_vs_quantum"]}
"""

{actual_code}'''

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated: {path}")

if __name__ == "__main__":
    for name, info in EXAMPLES.items():
        update_example(name, info)
