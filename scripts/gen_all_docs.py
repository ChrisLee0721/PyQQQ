"""Generate complete documentation for all examples using metadata.

Usage:
    python scripts/gen_all_docs.py
"""

import re
import sys
from pathlib import Path

# Import metadata
sys.path.insert(0, str(Path(__file__).parent))
from example_metadata import EXAMPLES

# Import SVG generator
from gen_circuit_svg import generate_svg, EXAMPLE_CIRCUITS


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
    match = re.search(r'"""(.*?)"""', code, re.DOTALL)
    if not match:
        return code.strip()
    end = match.end()
    return code[end:].strip()


def generate_svg_for_example(name, code):
    """Generate SVG circuit diagram for an example."""
    # Check if we already have a predefined circuit
    if name in EXAMPLE_CIRCUITS:
        config = EXAMPLE_CIRCUITS[name]
        return generate_svg(
            name,
            config["qubits"],
            config["gates"],
            config.get("title"),
        )

    # Try to infer circuit from code
    qubits = set()
    gates = []

    # Parse qgate calls
    qgate_pattern = re.compile(r'qgate\((\w+),\s*(\d+)(?:,\s*(\d+))?\)')
    for match in qgate_pattern.finditer(code):
        gate_name = match.group(1).lower()
        q1 = int(match.group(2))
        q2 = int(match.group(3)) if match.group(3) else None

        qubits.add(q1)
        if q2 is not None:
            qubits.add(q2)

        gate_info = {"type": gate_name, "qubits": [q1]}
        if q2 is not None:
            gate_info["qubits"].append(q2)
        gates.append(gate_info)

    if not qubits:
        # Default: 2 qubits
        qubits = {0, 1}

    n_qubits = max(qubits) + 1
    qubit_labels = [f"|q{i}⟩" for i in range(n_qubits)]

    return generate_svg(
        name,
        qubit_labels,
        gates,
        f"{name.replace('_', ' ').title()} circuit",
    )


def generate_doc(name, info, code):
    """Generate documentation for an example using metadata."""
    code_body = extract_code_body(code)

    doc = f"""# {info['title']} / {info['title_zh']}

> **{info['category']}** / {info['category_zh']} | 难度：{info['difficulty']} | 预计时间：{info['time']}

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

{info['why_detailed']}

---

## 快速上手

```python
{info['quick_code']}
```

**预期输出**：

```
{info['exact_output']}
```

---

## 原理详解

### 电路图

![{info['title']} circuit](/images/{info['svg_name']})

### 数学推导

{info['math_derivation']}

### 几何解释

{info['geometric_explanation']}

---

## 代码详解

```python
{info['annotated_code']}
```

### API 说明

| API | 参数 | 说明 |
|-----|------|------|
{info['api_table']}

---

## 进阶用法

### 场景 1：{info['scenario_1']}

```python
{info['code_1']}
```

### 场景 2：{info['scenario_2']}

```python
{info['code_2']}
```

### 场景 3：{info['scenario_3']}

```python
{info['code_3']}
```

---

## 适用场景

### 场景 1：{info['use_case_1']}

{info['use_case_1_detail']}

### 场景 2：{info['use_case_2']}

{info['use_case_2_detail']}

### 场景 3：{info['use_case_3']}

{info['use_case_3_detail']}

---

## 常见问题

### Q1: {info['question_1']}

{info['answer_1']}

### Q2: {info['question_2']}

{info['answer_2']}

### Q3: {info['question_3']}

{info['answer_3']}

### Q4: {info['question_4']}

{info['answer_4']}

### Q5: {info['question_5']}

{info['answer_5']}

---

## 学习路径

### 前置知识

- {info['prerequisite_1']}
- {info['prerequisite_2']}
- {info['prerequisite_3']}

### 继续学习

- {info['next_1']}
- {info['next_2']}
- {info['next_3']}

### 难度等级

- 当前：{info['current_level']}
- 下一步：{info['next_level']}

---

## 完整示例代码

### 示例 1：{info['example_1_title']}

```python
{info['example_1_code']}
```

### 示例 2：{info['example_2_title']}

```python
{info['example_2_code']}
```

### 运行方式

```bash
python examples/{name}/{name}.py
```

---

## 下载

- [{name}.py](https://github.com/ChrisLee0721/QuoNic/blob/main/examples/{name}/{name}.py)
"""

    return doc


def main():
    examples_root = Path(__file__).resolve().parent.parent.parent / "PyQQQ" / "examples"
    output_dir = Path(__file__).resolve().parent.parent / "public" / "docs" / "examples"
    output_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for name, info in EXAMPLES.items():
        # Find example file
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

        # Read example code
        code = example_path.read_text(encoding="utf-8")

        # Generate SVG if not exists
        svg_path = Path(__file__).resolve().parent.parent / "public" / "images" / f"{info['svg_name']}"
        if not svg_path.exists():
            svg = generate_svg_for_example(name, code)
            svg_path.write_text(svg, encoding="utf-8")
            print(f"  Generated {info['svg_name']}")

        # Generate documentation
        doc = generate_doc(name, info, code)

        # Write documentation
        output_path = output_dir / f"example_{name}.md"
        output_path.write_text(doc, encoding="utf-8")
        count += 1
        print(f"  Generated example_{name}.md")

    print(f"\nGenerated {count} example documentation files")


if __name__ == "__main__":
    main()
