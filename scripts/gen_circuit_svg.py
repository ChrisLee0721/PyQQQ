"""Generate SVG circuit diagrams for all examples.

Usage:
    python scripts/gen_circuit_svg.py
"""

import sys
from pathlib import Path


def generate_svg(circuit_name, qubits, gates, title=None):
    """Generate a clean SVG circuit diagram.

    Args:
        circuit_name: Name of the circuit
        qubits: List of qubit labels (e.g., ["|q₀⟩ = |0⟩", "|q₁⟩ = |0⟩"])
        gates: List of gate dicts with keys:
            - type: "h", "x", "y", "z", "cx", "cz", "ccx", "swap", "ry", "rz", "measure"
            - qubits: list of qubit indices
            - label: optional label
            - param: optional parameter
        title: Optional title

    Returns:
        SVG string
    """
    n_qubits = len(qubits)
    height = max(160, n_qubits * 60 + 40)

    # Calculate width based on number of gates
    n_gates = len(gates)
    width = max(300, n_gates * 60 + 200)

    # Build SVG
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="-10 0 {width+10} {height}">
  <rect width="100%" height="100%" fill="white" rx="8"/>
  <style>
    text {{ font-family: 'Consolas', 'Courier New', monospace; }}
    .qubit-label {{ font-size: 14px; fill: #555; }}
    .gate-label {{ font-size: 15px; fill: #222; font-weight: bold; }}
    .annotation {{ font-size: 11px; fill: #888; }}
    .wire {{ stroke: #bbb; stroke-width: 1.5; }}
    .gate-box {{ fill: #fff; stroke: #333; stroke-width: 1.8; rx: 4; }}
    .control-dot {{ fill: #333; }}
    .target-circle {{ fill: #fff; stroke: #333; stroke-width: 1.8; }}
    .target-plus {{ stroke: #333; stroke-width: 1.8; }}
    .conn-line {{ stroke: #333; stroke-width: 1.8; }}
    .title {{ font-size: 16px; fill: #333; font-weight: bold; }}
    .measure-box {{ fill: #fff; stroke: #333; stroke-width: 1.8; }}
  </style>

'''

    # Title
    if title:
        svg += f'  <text x="{width//2}" y="24" text-anchor="middle" class="title">{title}</text>\n\n'

    # Qubit labels
    for i, label in enumerate(qubits):
        y = 60 + i * 60
        svg += f'  <text x="5" y="{y+4}" class="qubit-label">{label}</text>\n'

    svg += '\n'

    # Quantum wires
    wire_start = 100
    wire_end = width - 100
    for i in range(n_qubits):
        y = 60 + i * 60
        svg += f'  <line x1="{wire_start}" y1="{y}" x2="{wire_end}" y2="{y}" class="wire"/>\n'

    svg += '\n'

    # Gates
    gate_spacing = (wire_end - wire_start) / max(len(gates), 1)
    for idx, gate in enumerate(gates):
        x = wire_start + int(gate_spacing * (idx + 0.5))
        gate_type = gate.get("type", "").lower()
        qs = gate.get("qubits", [])
        label = gate.get("label", gate_type.upper())
        param = gate.get("param", None)

        if not qs:
            continue

        if gate_type in ("h", "x", "y", "z", "ry", "rz", "t", "s"):
            # Single qubit gate
            q = qs[0]
            y = 60 + q * 60
            svg += f'  <rect x="{x-10}" y="{y-12}" width="20" height="24" class="gate-box"/>\n'
            if param:
                svg += f'  <text x="{x}" y="{y+4}" text-anchor="middle" class="gate-label" style="font-size: 9px;">{label}({param})</text>\n'
            else:
                svg += f'  <text x="{x}" y="{y+4}" text-anchor="middle" class="gate-label" style="font-size: 10px;">{label}</text>\n'

        elif gate_type in ("cx", "cnot"):
            # CNOT gate
            ctrl, tgt = qs[0], qs[1]
            y_ctrl = 60 + ctrl * 60
            y_tgt = 60 + tgt * 60
            svg += f'  <line x1="{x}" y1="{y_ctrl}" x2="{x}" y2="{y_tgt}" class="conn-line"/>\n'
            svg += f'  <circle cx="{x}" cy="{y_ctrl}" r="3" class="control-dot"/>\n'
            svg += f'  <circle cx="{x}" cy="{y_tgt}" r="11" class="target-circle"/>\n'
            svg += f'  <line x1="{x-11}" y1="{y_tgt}" x2="{x+11}" y2="{y_tgt}" class="target-plus"/>\n'
            svg += f'  <line x1="{x}" y1="{y_tgt-11}" x2="{x}" y2="{y_tgt+11}" class="target-plus"/>\n'

        elif gate_type == "cz":
            # CZ gate (both control)
            q1, q2 = qs[0], qs[1]
            y1 = 60 + q1 * 60
            y2 = 60 + q2 * 60
            svg += f'  <line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" class="conn-line"/>\n'
            svg += f'  <circle cx="{x}" cy="{y1}" r="3" class="control-dot"/>\n'
            svg += f'  <circle cx="{x}" cy="{y2}" r="3" class="control-dot"/>\n'

        elif gate_type == "ccx":
            # Toffoli gate
            ctrl1, ctrl2, tgt = qs[0], qs[1], qs[2]
            y_ctrl1 = 60 + ctrl1 * 60
            y_ctrl2 = 60 + ctrl2 * 60
            y_tgt = 60 + tgt * 60
            svg += f'  <line x1="{x}" y1="{y_ctrl1}" x2="{x}" y2="{y_tgt}" class="conn-line"/>\n'
            svg += f'  <circle cx="{x}" cy="{y_ctrl1}" r="3" class="control-dot"/>\n'
            svg += f'  <circle cx="{x}" cy="{y_ctrl2}" r="3" class="control-dot"/>\n'
            svg += f'  <circle cx="{x}" cy="{y_tgt}" r="11" class="target-circle"/>\n'
            svg += f'  <line x1="{x-11}" y1="{y_tgt}" x2="{x+11}" y2="{y_tgt}" class="target-plus"/>\n'
            svg += f'  <line x1="{x}" y1="{y_tgt-11}" x2="{x}" y2="{y_tgt+11}" class="target-plus"/>\n'

        elif gate_type == "swap":
            # SWAP gate
            q1, q2 = qs[0], qs[1]
            y1 = 60 + q1 * 60
            y2 = 60 + q2 * 60
            svg += f'  <line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" class="conn-line"/>\n'
            svg += f'  <text x="{x}" y="{y1+4}" text-anchor="middle" class="gate-label" style="font-size: 12px;">×</text>\n'
            svg += f'  <text x="{x}" y="{y2+4}" text-anchor="middle" class="gate-label" style="font-size: 12px;">×</text>\n'

        elif gate_type == "measure":
            # Measurement
            q = qs[0]
            y = 60 + q * 60
            svg += f'  <rect x="{x-12}" y="{y-12}" width="24" height="24" class="measure-box"/>\n'
            svg += f'  <text x="{x}" y="{y+4}" text-anchor="middle" class="gate-label" style="font-size: 10px;">M</text>\n'

    svg += '</svg>\n'
    return svg


# Example circuits for common algorithms
EXAMPLE_CIRCUITS = {
    "bell": {
        "title": "Bell state circuit",
        "qubits": ["|q₀⟩ = |0⟩", "|q₁⟩ = |0⟩"],
        "gates": [
            {"type": "h", "qubits": [0]},
            {"type": "cx", "qubits": [0, 1]},
        ],
    },
    "ghz": {
        "title": "GHZ state circuit",
        "qubits": ["|q₀⟩ = |0⟩", "|q₁⟩ = |0⟩", "|q₂⟩ = |0⟩"],
        "gates": [
            {"type": "h", "qubits": [0]},
            {"type": "cx", "qubits": [0, 1]},
            {"type": "cx", "qubits": [1, 2]},
        ],
    },
    "grover": {
        "title": "Grover search circuit",
        "qubits": ["|q₀⟩ = |0⟩", "|q₁⟩ = |0⟩"],
        "gates": [
            {"type": "h", "qubits": [0]},
            {"type": "h", "qubits": [1]},
            {"type": "cz", "qubits": [0, 1], "label": "Oracle"},
            {"type": "h", "qubits": [0]},
            {"type": "h", "qubits": [1]},
            {"type": "cz", "qubits": [0, 1], "label": "Diffusion"},
            {"type": "h", "qubits": [0]},
            {"type": "h", "qubits": [1]},
        ],
    },
    "teleportation": {
        "title": "Quantum teleportation circuit",
        "qubits": ["|q₀⟩ = |ψ⟩", "|q₁⟩ = |0⟩", "|q₂⟩ = |0⟩"],
        "gates": [
            {"type": "ry", "qubits": [0], "label": "Ry", "param": "π/3"},
            {"type": "h", "qubits": [1]},
            {"type": "cx", "qubits": [1, 2]},
            {"type": "cx", "qubits": [0, 1]},
            {"type": "h", "qubits": [0]},
            {"type": "cx", "qubits": [1, 2]},
            {"type": "cz", "qubits": [0, 2]},
        ],
    },
    "qft": {
        "title": "QFT circuit (3 qubits)",
        "qubits": ["|q₀⟩", "|q₁⟩", "|q₂⟩"],
        "gates": [
            {"type": "h", "qubits": [0]},
            {"type": "h", "qubits": [1]},
            {"type": "h", "qubits": [2]},
        ],
    },
    "superdense": {
        "title": "Superdense coding circuit",
        "qubits": ["|q₀⟩ = |0⟩", "|q₁⟩ = |0⟩"],
        "gates": [
            {"type": "h", "qubits": [0]},
            {"type": "cx", "qubits": [0, 1]},
            {"type": "x", "qubits": [0]},
            {"type": "cx", "qubits": [0, 1]},
            {"type": "h", "qubits": [0]},
        ],
    },
    "bit_flip_code": {
        "title": "Bit-flip error correction code",
        "qubits": ["|q₀⟩", "|q₁⟩", "|q₂⟩"],
        "gates": [
            {"type": "cx", "qubits": [0, 1]},
            {"type": "cx", "qubits": [0, 2]},
            {"type": "x", "qubits": [1], "label": "Error"},
            {"type": "cx", "qubits": [0, 1]},
            {"type": "cx", "qubits": [0, 2]},
            {"type": "ccx", "qubits": [1, 2, 0]},
        ],
    },
    "deutsch_jozsa": {
        "title": "Deutsch-Jozsa algorithm",
        "qubits": ["|q₀⟩ = |0⟩", "|q₁⟩ = |1⟩"],
        "gates": [
            {"type": "h", "qubits": [0]},
            {"type": "h", "qubits": [1]},
            {"type": "cx", "qubits": [0, 1], "label": "Oracle"},
            {"type": "h", "qubits": [0]},
        ],
    },
    "bernstein_vazirani": {
        "title": "Bernstein-Vazirani algorithm",
        "qubits": ["|q₀⟩ = |0⟩", "|q₁⟩ = |0⟩", "|q₂⟩ = |1⟩"],
        "gates": [
            {"type": "h", "qubits": [0]},
            {"type": "h", "qubits": [1]},
            {"type": "h", "qubits": [2]},
            {"type": "cx", "qubits": [0, 2], "label": "Oracle"},
            {"type": "cx", "qubits": [1, 2], "label": "Oracle"},
            {"type": "h", "qubits": [0]},
            {"type": "h", "qubits": [1]},
        ],
    },
    "simon": {
        "title": "Simon's algorithm",
        "qubits": ["|q₀⟩ = |0⟩", "|q₁⟩ = |0⟩", "|q₂⟩ = |0⟩", "|q₃⟩ = |0⟩"],
        "gates": [
            {"type": "h", "qubits": [0]},
            {"type": "h", "qubits": [1]},
            {"type": "cx", "qubits": [0, 2], "label": "Oracle"},
            {"type": "cx", "qubits": [1, 3], "label": "Oracle"},
            {"type": "h", "qubits": [0]},
            {"type": "h", "qubits": [1]},
        ],
    },
    "swap_test": {
        "title": "SWAP test circuit",
        "qubits": ["|q₀⟩ = |0⟩", "|q₁⟩ = |ψ⟩", "|q₂⟩ = |φ⟩"],
        "gates": [
            {"type": "h", "qubits": [0]},
            {"type": "swap", "qubits": [1, 2], "label": "c-SWAP"},
            {"type": "h", "qubits": [0]},
            {"type": "measure", "qubits": [0]},
        ],
    },
    "hadamard_test": {
        "title": "Hadamard test circuit",
        "qubits": ["|q₀⟩ = |0⟩", "|q₁⟩ = |ψ⟩"],
        "gates": [
            {"type": "h", "qubits": [0]},
            {"type": "cx", "qubits": [0, 1], "label": "U"},
            {"type": "h", "qubits": [0]},
            {"type": "measure", "qubits": [0]},
        ],
    },
    "phase_flip_code": {
        "title": "Phase-flip error correction code",
        "qubits": ["|q₀⟩", "|q₁⟩", "|q₂⟩"],
        "gates": [
            {"type": "cx", "qubits": [0, 1]},
            {"type": "cx", "qubits": [0, 2]},
            {"type": "h", "qubits": [0]},
            {"type": "h", "qubits": [1]},
            {"type": "h", "qubits": [2]},
            {"type": "z", "qubits": [1], "label": "Error"},
            {"type": "h", "qubits": [0]},
            {"type": "h", "qubits": [1]},
            {"type": "h", "qubits": [2]},
            {"type": "cx", "qubits": [0, 1]},
            {"type": "cx", "qubits": [0, 2]},
            {"type": "ccx", "qubits": [1, 2, 0]},
        ],
    },
    "qpe": {
        "title": "Quantum Phase Estimation",
        "qubits": ["|q₀⟩ = |0⟩", "|q₁⟩ = |0⟩", "|q₂⟩ = |0⟩", "|q₃⟩ = |ψ⟩"],
        "gates": [
            {"type": "h", "qubits": [0]},
            {"type": "h", "qubits": [1]},
            {"type": "h", "qubits": [2]},
            {"type": "cx", "qubits": [0, 3], "label": "U"},
            {"type": "cx", "qubits": [1, 3], "label": "U²"},
            {"type": "cx", "qubits": [2, 3], "label": "U⁴"},
            {"type": "h", "qubits": [0]},
            {"type": "h", "qubits": [1]},
            {"type": "h", "qubits": [2]},
        ],
    },
    "vqe": {
        "title": "VQE ansatz circuit",
        "qubits": ["|q₀⟩", "|q₁⟩"],
        "gates": [
            {"type": "ry", "qubits": [0], "label": "Ry", "param": "θ₁"},
            {"type": "ry", "qubits": [1], "label": "Ry", "param": "θ₂"},
            {"type": "cx", "qubits": [0, 1]},
            {"type": "ry", "qubits": [0], "label": "Ry", "param": "θ₃"},
            {"type": "ry", "qubits": [1], "label": "Ry", "param": "θ₄"},
        ],
    },
    "qaoa": {
        "title": "QAOA circuit (2 layers)",
        "qubits": ["|q₀⟩", "|q₁⟩", "|q₂⟩"],
        "gates": [
            {"type": "h", "qubits": [0]},
            {"type": "h", "qubits": [1]},
            {"type": "h", "qubits": [2]},
            {"type": "cx", "qubits": [0, 1], "label": "Cost"},
            {"type": "cx", "qubits": [1, 2], "label": "Cost"},
            {"type": "rx", "qubits": [0], "label": "Rx", "param": "β"},
            {"type": "rx", "qubits": [1], "label": "Rx", "param": "β"},
            {"type": "rx", "qubits": [2], "label": "Rx", "param": "β"},
        ],
    },
    "bb84": {
        "title": "BB84 QKD protocol",
        "qubits": ["|q₀⟩ (Alice)"],
        "gates": [
            {"type": "x", "qubits": [0], "label": "Bit"},
            {"type": "h", "qubits": [0], "label": "Basis"},
            {"type": "h", "qubits": [0], "label": "Measure"},
            {"type": "measure", "qubits": [0]},
        ],
    },
    "e91": {
        "title": "E91 QKD protocol",
        "qubits": ["|q₀⟩ (Alice)", "|q₁⟩ (Bob)"],
        "gates": [
            {"type": "h", "qubits": [0]},
            {"type": "cx", "qubits": [0, 1]},
            {"type": "h", "qubits": [0], "label": "Alice basis"},
            {"type": "h", "qubits": [1], "label": "Bob basis"},
            {"type": "measure", "qubits": [0]},
            {"type": "measure", "qubits": [1]},
        ],
    },
    "shor": {
        "title": "Shor's algorithm (simplified)",
        "qubits": ["|q₀⟩", "|q₁⟩", "|q₂⟩", "|q₃⟩"],
        "gates": [
            {"type": "h", "qubits": [0]},
            {"type": "h", "qubits": [1]},
            {"type": "h", "qubits": [2]},
            {"type": "cx", "qubits": [0, 3], "label": "U"},
            {"type": "cx", "qubits": [1, 3], "label": "U²"},
            {"type": "cx", "qubits": [2, 3], "label": "U⁴"},
            {"type": "h", "qubits": [0]},
            {"type": "h", "qubits": [1]},
            {"type": "h", "qubits": [2]},
        ],
    },
    "hhl": {
        "title": "HHL algorithm (simplified)",
        "qubits": ["|q₀⟩", "|q₁⟩", "|q₂⟩"],
        "gates": [
            {"type": "h", "qubits": [0]},
            {"type": "h", "qubits": [1]},
            {"type": "cx", "qubits": [0, 2], "label": "U"},
            {"type": "cx", "qubits": [1, 2], "label": "U²"},
            {"type": "h", "qubits": [0]},
            {"type": "h", "qubits": [1]},
        ],
    },
    "trotter": {
        "title": "Trotterization circuit",
        "qubits": ["|q₀⟩", "|q₁⟩"],
        "gates": [
            {"type": "h", "qubits": [0]},
            {"type": "h", "qubits": [1]},
            {"type": "cx", "qubits": [0, 1]},
            {"type": "rz", "qubits": [1], "label": "Rz", "param": "θ"},
            {"type": "cx", "qubits": [0, 1]},
        ],
    },
    "qft_3": {
        "title": "QFT (3 qubits)",
        "qubits": ["|q₀⟩", "|q₁⟩", "|q₂⟩"],
        "gates": [
            {"type": "h", "qubits": [0]},
            {"type": "h", "qubits": [1]},
            {"type": "h", "qubits": [2]},
        ],
    },
    "grover_3": {
        "title": "Grover search (3 qubits)",
        "qubits": ["|q₀⟩ = |0⟩", "|q₁⟩ = |0⟩", "|q₂⟩ = |0⟩"],
        "gates": [
            {"type": "h", "qubits": [0]},
            {"type": "h", "qubits": [1]},
            {"type": "h", "qubits": [2]},
            {"type": "ccx", "qubits": [0, 1, 2], "label": "Oracle"},
            {"type": "h", "qubits": [0]},
            {"type": "h", "qubits": [1]},
            {"type": "h", "qubits": [2]},
            {"type": "ccx", "qubits": [0, 1, 2], "label": "Diffusion"},
            {"type": "h", "qubits": [0]},
            {"type": "h", "qubits": [1]},
            {"type": "h", "qubits": [2]},
        ],
    },
}


def main():
    output_dir = Path(__file__).resolve().parent.parent / "public" / "images"
    output_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for name, config in EXAMPLE_CIRCUITS.items():
        svg = generate_svg(
            name,
            config["qubits"],
            config["gates"],
            config.get("title"),
        )
        output_path = output_dir / f"{name}_circuit.svg"
        output_path.write_text(svg, encoding="utf-8")
        count += 1
        print(f"  Generated {name}_circuit.svg")

    print(f"\nGenerated {count} SVG circuit diagrams")


if __name__ == "__main__":
    main()
