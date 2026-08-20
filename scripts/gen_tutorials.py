"""Generate detailed tutorials from examples."""

import re
import sys
from pathlib import Path

# Tutorial metadata for each example
TUTORIALS = {
    "bell": {"title": "Bell State", "title_zh": "Bell 态", "category": "foundational"},
    "ghz": {"title": "GHZ State", "title_zh": "GHZ 态", "category": "foundational"},
    "grover": {"title": "Grover Search", "title_zh": "Grover 搜索", "category": "algorithms"},
    "vqe": {"title": "VQE", "title_zh": "变分量子本征求解器", "category": "algorithms"},
    "qft": {"title": "Quantum Fourier Transform", "title_zh": "量子傅里叶变换", "category": "algorithms"},
    "qpe": {"title": "Quantum Phase Estimation", "title_zh": "量子相位估计", "category": "algorithms"},
    "teleportation": {"title": "Quantum Teleportation", "title_zh": "量子隐形传态", "category": "communication"},
    "bb84": {"title": "BB84 QKD", "title_zh": "BB84 量子密钥分发", "category": "communication"},
    "shor": {"title": "Shor's Algorithm", "title_zh": "Shor 算法", "category": "algorithms"},
    "qaoa": {"title": "QAOA", "title_zh": "量子近似优化算法", "category": "algorithms"},
    "qif": {"title": "Quantum If", "title_zh": "量子条件分支", "category": "advanced"},
    "cif": {"title": "Classical If", "title_zh": "经典条件分支", "category": "advanced"},
    "cwhile": {"title": "Classical While", "title_zh": "经典循环", "category": "advanced"},
    "qint": {"title": "Quantum Integer", "title_zh": "量子整数运算", "category": "advanced"},
    "basic_gates": {"title": "Basic Gates", "title_zh": "基础门", "category": "foundational"},
    "controlled": {"title": "Controlled Gates", "title_zh": "受控门", "category": "foundational"},
    "decompose": {"title": "Gate Decomposition", "title_zh": "门分解", "category": "compiler"},
    "diffusion": {"title": "Diffusion Operator", "title_zh": "扩散算子", "category": "algorithms"},
    "oracle": {"title": "Oracle Construction", "title_zh": "Oracle 构造", "category": "algorithms"},
    "mark_state": {"title": "Mark State", "title_zh": "标记态", "category": "algorithms"},
    "noise": {"title": "Noise Simulation", "title_zh": "噪声模拟", "category": "noise"},
    "noise_model": {"title": "Noise Model", "title_zh": "噪声模型", "category": "noise"},
    "error_mitigation": {"title": "Error Mitigation", "title_zh": "误差缓解", "category": "noise"},
    "error_correction": {"title": "Error Correction", "title_zh": "量子纠错", "category": "qec"},
    "compare": {"title": "Backend Comparison", "title_zh": "后端对比", "category": "backends"},
    "coupling_map": {"title": "Coupling Map", "title_zh": "耦合映射", "category": "backends"},
    "creg_multi": {"title": "Multiple Classical Registers", "title_zh": "多经典寄存器", "category": "foundational"},
    "hardware_compile": {"title": "Hardware Compilation", "title_zh": "硬件编译", "category": "compiler"},
    "schedule": {"title": "Smart Scheduling", "title_zh": "智能调度", "category": "backends"},
    "gpu_demo": {"title": "GPU Acceleration", "title_zh": "GPU 加速", "category": "backends"},
    "from_qiskit_nature": {"title": "Qiskit Nature Integration", "title_zh": "Qiskit Nature 集成", "category": "integration"},
    "qaoa_maxcut": {"title": "QAOA MaxCut", "title_zh": "QAOA 最大割", "category": "algorithms"},
    "qaoa_mis": {"title": "QAOA MIS", "title_zh": "QAOA 最大独立集", "category": "algorithms"},
    "qaoa_knapsack": {"title": "QAOA Knapsack", "title_zh": "QAOA 背包问题", "category": "algorithms"},
    "qaoa_tsp": {"title": "QAOA TSP", "title_zh": "QAOA 旅行商问题", "category": "algorithms"},
    "bernstein_vazirani": {"title": "Bernstein-Vazirani", "title_zh": "Bernstein-Vazirani 算法", "category": "algorithms"},
    "deutsch_jozsa": {"title": "Deutsch-Jozsa", "title_zh": "Deutsch-Jozsa 算法", "category": "algorithms"},
    "simon": {"title": "Simon's Algorithm", "title_zh": "Simon 算法", "category": "algorithms"},
    "quantum_counting": {"title": "Quantum Counting", "title_zh": "量子计数", "category": "algorithms"},
    "swap_test": {"title": "SWAP Test", "title_zh": "SWAP 测试", "category": "algorithms"},
    "hadamard_test": {"title": "Hadamard Test", "title_zh": "Hadamard 测试", "category": "algorithms"},
    "superdense_coding": {"title": "Superdense Coding", "title_zh": "超密编码", "category": "communication"},
    "bit_flip_code": {"title": "Bit-Flip Code", "title_zh": "比特翻转码", "category": "qec"},
    "phase_flip_code": {"title": "Phase-Flip Code", "title_zh": "相位翻转码", "category": "qec"},
    "shor_code": {"title": "Shor Code", "title_zh": "Shor 码", "category": "qec"},
    "steane_code": {"title": "Steane Code", "title_zh": "Steane 码", "category": "qec"},
    "color_code": {"title": "Color Code", "title_zh": "颜色码", "category": "qec"},
    "stabilizer": {"title": "Stabilizer Formalism", "title_zh": "稳定子形式", "category": "qec"},
    "syndrome": {"title": "Syndrome Measurement", "title_zh": "伴随式测量", "category": "qec"},
    "ft_gate": {"title": "Fault-Tolerant Gates", "title_zh": "容错门", "category": "qec"},
    "trotter": {"title": "Trotterization", "title_zh": "Trotter 分解", "category": "algorithms"},
    "hamiltonian_simulation": {"title": "Hamiltonian Simulation", "title_zh": "哈密顿模拟", "category": "algorithms"},
    "molecule_vqe": {"title": "Molecular VQE", "title_zh": "分子 VQE", "category": "chemistry"},
    "jordan_wigner": {"title": "Jordan-Wigner", "title_zh": "Jordan-Wigner 变换", "category": "chemistry"},
    "hhl": {"title": "HHL Algorithm", "title_zh": "HHL 算法", "category": "algorithms"},
    "hsp": {"title": "Hidden Subgroup", "title_zh": "隐藏子群", "category": "algorithms"},
    "amplitude_amplification": {"title": "Amplitude Amplification", "title_zh": "振幅放大", "category": "algorithms"},
    "amplitude_estimation": {"title": "Amplitude Estimation", "title_zh": "振幅估计", "category": "algorithms"},
    "discrete_log": {"title": "Discrete Logarithm", "title_zh": "离散对数", "category": "algorithms"},
    "elliptic_curve": {"title": "Elliptic Curve", "title_zh": "椭圆曲线", "category": "algorithms"},
    "lattice_svp": {"title": "Lattice SVP", "title_zh": "格最短向量", "category": "algorithms"},
    "e91": {"title": "E91 QKD", "title_zh": "E91 量子密钥分发", "category": "communication"},
    "dqaoa": {"title": "Dynamic QAOA", "title_zh": "动态 QAOA", "category": "algorithms"},
    "dynamics_simulation": {"title": "Dynamics Simulation", "title_zh": "动力学模拟", "category": "algorithms"},
    "qbm": {"title": "Quantum Boltzmann Machine", "title_zh": "量子玻尔兹曼机", "category": "ml"},
    "qcnn": {"title": "Quantum CNN", "title_zh": "量子卷积网络", "category": "ml"},
    "qgan": {"title": "Quantum GAN", "title_zh": "量子生成对抗网络", "category": "ml"},
    "qgnn": {"title": "Quantum GNN", "title_zh": "量子图神经网络", "category": "ml"},
    "qng": {"title": "Quantum Natural Gradient", "title_zh": "量子自然梯度", "category": "ml"},
    "qnn": {"title": "Quantum Neural Network", "title_zh": "量子神经网络", "category": "ml"},
    "qpca": {"title": "Quantum PCA", "title_zh": "量子主成分分析", "category": "ml"},
    "qrl": {"title": "Quantum RL", "title_zh": "量子强化学习", "category": "ml"},
    "qsp": {"title": "Quantum Signal Processing", "title_zh": "量子信号处理", "category": "algorithms"},
    "qsvm": {"title": "Quantum SVM", "title_zh": "量子支持向量机", "category": "ml"},
    "qtda": {"title": "Quantum TDA", "title_zh": "量子拓扑数据分析", "category": "ml"},
    "qtransformer": {"title": "Quantum Transformer", "title_zh": "量子 Transformer", "category": "ml"},
    "quantum_annealing": {"title": "Quantum Annealing", "title_zh": "量子退火", "category": "algorithms"},
    "quantum_bayesian": {"title": "Quantum Bayesian", "title_zh": "量子贝叶斯", "category": "ml"},
    "quantum_clustering": {"title": "Quantum Clustering", "title_zh": "量子聚类", "category": "ml"},
    "quantum_eigenvalue": {"title": "Eigenvalue Estimation", "title_zh": "本征值估计", "category": "algorithms"},
    "quantum_fitting": {"title": "Quantum Fitting", "title_zh": "量子拟合", "category": "ml"},
    "quantum_kernel": {"title": "Quantum Kernel", "title_zh": "量子核方法", "category": "ml"},
    "quantum_matrix_inversion": {"title": "Matrix Inversion", "title_zh": "矩阵求逆", "category": "algorithms"},
    "quantum_monte_carlo": {"title": "Quantum Monte Carlo", "title_zh": "量子蒙特卡洛", "category": "algorithms"},
    "quantum_ode": {"title": "Quantum ODE", "title_zh": "量子微分方程", "category": "algorithms"},
    "quantum_pde": {"title": "Quantum PDE", "title_zh": "量子偏微分方程", "category": "algorithms"},
    "quantum_walk": {"title": "Quantum Walk", "title_zh": "量子行走", "category": "algorithms"},
    "rejection_sampling": {"title": "Rejection Sampling", "title_zh": "量子拒绝采样", "category": "algorithms"},
    "vqc": {"title": "VQC", "title_zh": "变分量子分类器", "category": "ml"},
    "vqr": {"title": "VQR", "title_zh": "变分量子回归器", "category": "ml"},
    "groverize": {"title": "Groverize", "title_zh": "Grover 化", "category": "compiler"},
    "surface_code": {"title": "Surface Code", "title_zh": "表面码", "category": "qec"},
    "qi": {"title": "Quantum Inspire", "title_zh": "Quantum Inspire 硬件", "category": "backends"},
}

CATEGORY_LABELS = {
    "foundational": ("Foundational", "基础"),
    "algorithms": ("Algorithms", "算法"),
    "advanced": ("Advanced", "高级"),
    "compiler": ("Compiler", "编译器"),
    "noise": ("Noise & Mitigation", "噪声与缓解"),
    "qec": ("Error Correction", "量子纠错"),
    "backends": ("Backends", "后端"),
    "communication": ("Communication", "通信"),
    "chemistry": ("Quantum Chemistry", "量子化学"),
    "ml": ("Quantum ML", "量子机器学习"),
    "integration": ("Integration", "集成"),
}


def extract_docstring(code):
    """Extract docstring and parse sections."""
    match = re.search(r'"""(.*?)"""', code, re.DOTALL)
    if not match:
        return {}
    raw = match.group(1).strip()

    sections = {}
    current_key = "intro"
    current_lines = []
    for line in raw.split('\n'):
        header = re.match(r'^##\s+(.+)', line)
        if header:
            sections[current_key] = '\n'.join(current_lines).strip()
            current_key = header.group(1).strip()
            current_lines = []
        else:
            current_lines.append(line)
    sections[current_key] = '\n'.join(current_lines).strip()
    return sections


def extract_code_body(code):
    """Extract code after the docstring."""
    # Find end of first docstring
    match = re.search(r'"""(.*?)"""', code, re.DOTALL)
    if not match:
        return code.strip()
    end = match.end()
    return code[end:].strip()


def extract_readme(example_dir):
    """Read README.md if it exists."""
    readme = example_dir / "README.md"
    if readme.exists():
        return readme.read_text(encoding='utf-8').strip()
    return ""


def gen_tutorial(name, info, example_path):
    """Generate a detailed bilingual tutorial from an example."""
    code = example_path.read_text(encoding='utf-8')
    example_dir = example_path.parent
    sections = extract_docstring(code)
    code_body = extract_code_body(code)
    readme = extract_readme(example_dir)

    title = info['title']
    title_zh = info.get('title_zh', title)
    category = info.get('category', 'general')
    cat_en, cat_zh = CATEGORY_LABELS.get(category, ("General", "通用"))

    # Parse intro for bilingual description
    intro = sections.get('intro', '')
    intro_lines = [l.strip() for l in intro.split('\n') if l.strip()]
    desc_en = intro_lines[0] if len(intro_lines) > 0 else ""
    desc_zh = intro_lines[1] if len(intro_lines) > 1 else ""

    # Application section
    app = sections.get('Application / 应用场景', sections.get('Application', ''))
    app_lines = [l.strip() for l in app.split('\n') if l.strip()]

    # How it works
    how = sections.get('How it works / 原理', sections.get('How it works', ''))
    how_lines = [l.strip() for l in how.split('\n') if l.strip()]

    # Output
    output = sections.get('Output / 输出说明', sections.get('Output', ''))
    output_lines = [l.strip() for l in output.split('\n') if l.strip()]

    # Build tutorial
    lines = []
    lines.append(f"# {title} / {title_zh}")
    lines.append("")
    lines.append(f"> **{cat_en}** / {cat_zh}")
    lines.append("")

    # Description
    if desc_en or desc_zh:
        lines.append("## Overview / 概述")
        lines.append("")
        if desc_en:
            lines.append(desc_en)
        if desc_zh and desc_zh != desc_en:
            lines.append("")
            lines.append(desc_zh)
        lines.append("")

    # Application scenarios
    if app_lines:
        lines.append("## Application / 应用场景")
        lines.append("")
        for l in app_lines:
            if l.startswith('- '):
                lines.append(l)
            else:
                lines.append(f"- {l}")
        lines.append("")

    # How it works
    if how_lines:
        lines.append("## How it works / 原理")
        lines.append("")
        for l in how_lines:
            lines.append(l)
        lines.append("")

    # Code
    lines.append("## Code / 代码")
    lines.append("")
    lines.append("```python")
    lines.append(code_body)
    lines.append("```")
    lines.append("")

    # Expected output
    if output_lines:
        lines.append("## Expected Output / 预期输出")
        lines.append("")
        for l in output_lines:
            lines.append(l)
        lines.append("")

    # Run instructions
    lines.append("## Run / 运行")
    lines.append("")
    lines.append("```bash")
    lines.append(f"python examples/{name}/{name}.py")
    lines.append("```")
    lines.append("")

    # Download
    lines.append("## Download / 下载")
    lines.append("")
    lines.append(f"[{name}.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/{name}/{name}.py)")
    lines.append("")

    return '\n'.join(lines)


def main():
    if len(sys.argv) > 1:
        examples_root = Path(sys.argv[1])
    else:
        examples_root = Path(__file__).resolve().parent.parent.parent / "PyQQQ" / "examples"
    tutorials_dir = Path(__file__).resolve().parent.parent / "public" / "docs" / "examples"
    tutorials_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for name, info in TUTORIALS.items():
        example_path = None
        for pattern in [
            examples_root / name / f"{name}.py",
            examples_root / f"{name}.py",
        ]:
            if pattern.exists():
                example_path = pattern
                break

        if example_path is None:
            print(f"  SKIP {name}: no example file found")
            continue

        tutorial = gen_tutorial(name, info, example_path)
        tutorial_path = tutorials_dir / f"example_{name}.md"
        tutorial_path.write_text(tutorial, encoding='utf-8')
        count += 1

    print(f"Generated {count} tutorials")


if __name__ == "__main__":
    main()
