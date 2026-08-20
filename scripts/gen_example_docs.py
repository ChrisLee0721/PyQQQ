"""Generate complete documentation for all examples.

Usage:
    python scripts/gen_example_docs.py
"""

import re
import sys
from pathlib import Path

# Template for example documentation
TEMPLATE = """# {title} / {title_zh}

> **{category}** / {category_zh}

---

## 目录

- [为什么需要？](#为什么需要)
- [快速上手](#快速上手)
- [原理详解](#原理详解)
- [代码详解](#代码详解)
- [进阶用法](#进阶用法)
- [适用场景](#适用场景)
- [常见问题](#常见问题)
- [学习路径](#学习路径)
- [完整示例代码](#完整示例代码)

---

## 为什么需要？

{why_section}

---

## 快速上手

```python
{quick_code}
```

**预期输出**：

```
{expected_output}
```

---

## 原理详解

### 电路图

![{title} circuit](/images/{svg_name})

{principle_section}

---

## 代码详解

{code_section}

---

## 进阶用法

{advanced_section}

---

## 适用场景

{use_cases_section}

---

## 常见问题

{faq_section}

---

## 学习路径

### 前置知识

{prerequisites}

### 继续学习

{next_steps}

---

## 完整示例代码

```python
{full_code}
```

### 运行方式

```bash
python examples/{name}/{name}.py
```

---

## 下载

- [{name}.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/{name}/{name}.py)
"""

# Example metadata
EXAMPLES = {
    "bell": {
        "title": "Bell State",
        "title_zh": "Bell 态",
        "category": "Foundational",
        "category_zh": "基础",
        "why": "Bell 态是最简单的量子纠缠态，是量子计算的 Hello World。它展示了量子力学的非局域性，是量子隐形传态、超密编码、量子密钥分发的基础。",
        "quick_code": """from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)      # Hadamard: 把 q₀ 变成叠加态
qgate(CX, 0, 1)  # CNOT:    让 q₁ 跟着 q₀ 纠缠
qshow()           # 测量并显示结果""",
        "expected_output": """backend: native | shots: 1024
Result:
  |00>     512  ( 50.0%)  ####################
  |11>     512  ( 50.0%)  ####################""",
        "principle": """Bell 态的创建过程：

1. **初始态**：两个量子比特都从 |0⟩ 开始
2. **Hadamard 门**：对 q₀ 施加 H 门，创建叠加态 (|0⟩+|1⟩)/√2
3. **CNOT 门**：让 q₁ 跟着 q₀ 纠缠，最终得到 (|00⟩+|11⟩)/√2

关键点：测量结果只有 |00⟩ 和 |11⟩，没有 |01⟩ 和 |10⟩，这证明了纠缠。""",
        "code": """from quonic import qgate, qshow
from quonic.gates import CX, H

# Step 1: 创建叠加态
qgate(H, 0)      # q₀ → (|0⟩+|1⟩)/√2

# Step 2: 创建纠缠
qgate(CX, 0, 1)  # q₀,q₁ → (|00⟩+|11⟩)/√2

# Step 3: 测量
qshow()""",
        "advanced": """### 1. 查看态向量

```python
from quonic import qgate, reset
from quonic.gates import CX, H
from quonic.backends import get_backend
from quonic.stack import current_circuit

reset()
qgate(H, 0)
qgate(CX, 0, 1)

backend = get_backend("native")
result = backend.run(current_circuit(), shots=1)
print(result.statevector)
# [0.707+0j, 0+0j, 0+0j, 0.707+0j]
```

### 2. 噪声测试

```python
qshow(noise=0.05)  # 5% 噪声
```

### 3. 全部 4 个 Bell 态

| 名称 | 电路 | 数学表达式 |
|------|------|-----------|
| Φ⁺ | H, CX | (|00⟩+|11⟩)/√2 |
| Φ⁻ | H, X, CX | (|00⟩-|11⟩)/√2 |
| Ψ⁺ | H, CX, X | (|01⟩+|10⟩)/√2 |
| Ψ⁻ | H, X, CX, X | (|01⟩-|10⟩)/√2 |""",
        "use_cases": """- **量子隐形传态**：用 Bell 态传输量子态
- **超密编码**：用 Bell 态传输经典信息
- **量子密钥分发**：用 Bell 态检测窃听
- **测试量子硬件**：Bell 态是测试硬件质量的"金标准" """,
        "faq": """### Q1: 为什么我的结果不是精确的 50/50？

量子测量有随机性。增加 shots：`qshow(shots=10000)`

### Q2: 为什么我看到了 |01⟩ 或 |10⟩？

可能原因：噪声、代码错误、后端问题。检查 H 门是否在 CNOT 之前。

### Q3: Bell 态和 GHZ 态有什么区别？

Bell 态是 2 量子比特纠缠，GHZ 态是 3+ 量子比特纠缠。""",
        "prerequisites": "- 量子比特、叠加态、量子门",
        "next_steps": "- 量子隐形传态、超密编码、GHZ 态",
        "svg_name": "bell_circuit.svg",
    },
    "ghz": {
        "title": "GHZ State",
        "title_zh": "GHZ 态",
        "category": "Foundational",
        "category_zh": "基础",
        "why": "GHZ 态是多量子比特纠缠的经典例子，展示了量子力学的非局域性。它是量子纠错、量子密钥分发的基础。",
        "quick_code": """from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)
qgate(CX, 0, 1)
qgate(CX, 1, 2)
qshow()""",
        "expected_output": """backend: native | shots: 1024
Result:
  |000>    512  ( 50.0%)  ####################
  |111>    512  ( 50.0%)  ####################""",
        "principle": """GHZ 态的创建过程：

1. **初始态**：三个量子比特都从 |0⟩ 开始
2. **Hadamard 门**：对 q₀ 施加 H 门，创建叠加态
3. **CNOT 链**：q₀→q₁→q₂，创建三体纠缠

最终态：(|000⟩+|111⟩)/√2""",
        "code": """from quonic import qgate, qshow
from quonic.gates import CX, H

qgate(H, 0)      # 叠加态
qgate(CX, 0, 1)  # 纠缠 q₀ 和 q₁
qgate(CX, 1, 2)  # 纠缠 q₁ 和 q₂
qshow()""",
        "advanced": """### 1. N 量子比特 GHZ 态

```python
n = 5
qgate(H, 0)
for i in range(n - 1):
    qgate(CX, i, i + 1)
qshow()
```

### 2. 噪声影响

```python
qshow(noise=0.05)  # 5% 噪声
```""",
        "use_cases": """- **量子纠错**：GHZ 态用于测试纠错码
- **量子密钥分发**：多方量子密钥
- **量子传感**：增强测量精度""",
        "faq": """### Q1: GHZ 态和 Bell 态有什么区别？

Bell 态是 2 量子比特纠缠，GHZ 态是 3+ 量子比特纠缠。

### Q2: 如何验证 GHZ 态？

测量结果应该只有 |000⟩ 和 |111⟩，没有其他状态。""",
        "prerequisites": "- Bell 态、CNOT 门",
        "next_steps": "- 量子纠错、量子密钥分发",
        "svg_name": "ghz_circuit.svg",
    },
    # Add more examples here...
}


def generate_doc(name, info, example_code):
    """Generate documentation for an example."""
    # Parse example code
    lines = example_code.strip().split('\n')
    code_body = '\n'.join(lines)

    # Generate documentation
    doc = TEMPLATE.format(
        title=info["title"],
        title_zh=info["title_zh"],
        category=info["category"],
        category_zh=info["category_zh"],
        why_section=info["why"],
        quick_code=info["quick_code"],
        expected_output=info["expected_output"],
        svg_name=info["svg_name"],
        principle_section=info["principle"],
        code_section=f"```python\n{info['code']}\n```",
        advanced_section=info["advanced"],
        use_cases_section=info["use_cases"],
        faq_section=info["faq"],
        prerequisites=info["prerequisites"],
        next_steps=info["next_steps"],
        full_code=code_body,
        name=name,
    )

    return doc


def main():
    examples_dir = Path(__file__).resolve().parent.parent.parent / "PyQQQ" / "examples"
    output_dir = Path(__file__).resolve().parent.parent / "public" / "docs" / "examples"
    output_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for name, info in EXAMPLES.items():
        # Find example file
        example_path = None
        for pattern in [
            examples_dir / name / f"{name}.py",
            examples_dir / f"{name}.py",
        ]:
            if pattern.exists():
                example_path = pattern
                break

        if example_path is None:
            print(f"  SKIP {name}: no example file found")
            continue

        # Read example code
        example_code = example_path.read_text(encoding="utf-8")

        # Generate documentation
        doc = generate_doc(name, info, example_code)

        # Write documentation
        output_path = output_dir / f"example_{name}.md"
        output_path.write_text(doc, encoding="utf-8")
        count += 1
        print(f"  Generated example_{name}.md")

    print(f"\nGenerated {count} example documentation files")


if __name__ == "__main__":
    main()
