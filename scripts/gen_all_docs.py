"""Generate documentation for all examples automatically.

Usage:
    python scripts/gen_all_docs.py
"""

import re
import sys
from pathlib import Path

# Import the SVG generator
sys.path.insert(0, str(Path(__file__).parent))
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


def generate_doc(name, code, sections):
    """Generate documentation for an example."""
    code_body = extract_code_body(code)

    # Parse sections
    intro = sections.get("intro", "")
    intro_lines = [l.strip() for l in intro.split('\n') if l.strip()]
    desc_en = intro_lines[0] if len(intro_lines) > 0 else ""
    desc_zh = intro_lines[1] if len(intro_lines) > 1 else ""

    app = sections.get('Application / 应用场景', sections.get('Application', ''))
    app_lines = [l.strip() for l in app.split('\n') if l.strip()]

    how = sections.get('How it works / 原理', sections.get('How it works', ''))
    how_lines = [l.strip() for l in how.split('\n') if l.strip()]

    output = sections.get('Output / 输出说明', sections.get('Output', ''))
    output_lines = [l.strip() for l in output.split('\n') if l.strip()]

    # Build documentation
    doc = f"""# {name.replace('_', ' ').title()} / {desc_zh if desc_zh else name.replace('_', ' ').title()}

> **Example** / 示例

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

{desc_en if desc_en else f"This example demonstrates {name.replace('_', ' ')}."}

{desc_zh if desc_zh else ""}

---

## 快速上手

```python
{code_body}
```

**预期输出**：

```
{chr(10).join(output_lines) if output_lines else "See code comments for output explanation."}
```

---

## 原理详解

### 电路图

![{name.replace('_', ' ').title()} circuit](/images/{name}_circuit.svg)

{chr(10).join(how_lines) if how_lines else "See code comments for explanation."}

---

## 代码详解

```python
{code_body}
```

---

## 进阶用法

See the full example code below for more advanced usage.

---

## 适用场景

{chr(10).join(f"- {l}" for l in app_lines) if app_lines else "- Quantum computing demonstrations\n- Algorithm examples\n- Educational purposes"}

---

## 常见问题

### Q1: How to run this example?

```bash
python examples/{name}/{name}.py
```

### Q2: What backend is used?

The example uses the default backend. You can specify a different one:

```python
qshow(backend='qiskit')
```

---

## 学习路径

### 前置知识

- Basic quantum computing concepts
- QuoNic API basics

### 继续学习

- Other examples in this documentation
- QuoNic API reference

---

## 完整示例代码

```python
{code}
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

    # Get all example directories
    example_dirs = [d for d in examples_root.iterdir() if d.is_dir() and not d.name.startswith('.')]

    count = 0
    for example_dir in sorted(example_dirs):
        name = example_dir.name
        example_file = example_dir / f"{name}.py"

        if not example_file.exists():
            print(f"  SKIP {name}: no {name}.py found")
            continue

        # Read example code
        code = example_file.read_text(encoding="utf-8")

        # Extract docstring sections
        sections = extract_docstring(code)

        # Generate SVG if not exists
        svg_path = Path(__file__).resolve().parent.parent / "public" / "images" / f"{name}_circuit.svg"
        if not svg_path.exists():
            svg = generate_svg_for_example(name, code)
            svg_path.write_text(svg, encoding="utf-8")
            print(f"  Generated {name}_circuit.svg")

        # Generate documentation
        doc = generate_doc(name, code, sections)

        # Write documentation
        output_path = output_dir / f"example_{name}.md"
        output_path.write_text(doc, encoding="utf-8")
        count += 1
        print(f"  Generated example_{name}.md")

    print(f"\nGenerated {count} example documentation files")


if __name__ == "__main__":
    main()
