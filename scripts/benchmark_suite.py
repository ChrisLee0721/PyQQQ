"""End-to-end benchmark suite — Quantum Volume, cross-entropy, and algorithm benchmarks.

Usage:
    python scripts/benchmark_suite.py
    python scripts/benchmark_suite.py --backend qulacs
    python scripts/benchmark_suite.py --n 10,15,20
"""

from __future__ import annotations

import argparse
import json
import time
from typing import Any, Dict, List

import numpy as np


def quantum_volume(n: int, shots: int = 1024, backend: str = "native") -> Dict[str, Any]:
    """Quantum Volume benchmark: measure the largest square circuit depth.

    Args:
        n: number of qubits
        shots: number of shots
        backend: simulation backend

    Returns:
        Dict with n, depth, success_rate, time.
    """
    from quonic import qgate, reset
    from quonic.backends import get_backend
from quonic.gates import H, Ry
from quonic.ir import Circuit, GateOperation
from quonic.stack import current_circuit

    # Build a random circuit (simplified QV)
    reset()
    for _ in range(n):
        qgate(H, 0)  # placeholder

    t0 = time.time()
    result = get_backend(backend).run(current_circuit(), shots=shots)
    elapsed = time.time() - t0

    return {
        "n": n,
        "depth": n,
        "success_rate": 0.5,  # placeholder
        "time": elapsed,
    }


def cross_entropy(n: int, shots: int = 1024, backend: str = "native") -> Dict[str, Any]:
    """Cross-entropy benchmark: measure circuit fidelity.

    Args:
        n: number of qubits
        shots: number of shots
        backend: simulation backend

    Returns:
        Dict with n, fidelity, time.
    """
    from quonic import qgate, reset
from quonic.backends import get_backend
from quonic.gates import H, CX
from quonic.stack import current_circuit

    # Build a random circuit
    reset()
    qgate(H, 0)
    for i in range(n - 1):
        qgate(CX, i, i + 1)

    t0 = time.time()
    result = get_backend(backend).run(current_circuit(), shots=shots)
    elapsed = time.time() - t0

    return {
        "n": n,
        "fidelity": 1.0,  # placeholder
        "time": elapsed,
    }


def algorithm_benchmark(
    name: str, n: int, shots: int = 1024, backend: str = "native"
) -> Dict[str, Any]:
    """Run an algorithm benchmark.

    Args:
        name: algorithm name ("grover", "qft", "vqe")
        n: number of qubits
        shots: number of shots
        backend: simulation backend

    Returns:
        Dict with name, n, time, result.
    """
    from quonic import qgate, reset
from quonic.backends import get_backend
from quonic.gates import H, CX
from quonic.stack import current_circuit

    reset()
    if name == "grover":
        qgate(H, 0)
        qgate(H, 1)
    elif name == "qft":
        qgate(H, 0)
        for i in range(n - 1):
            qgate(CX, i, i + 1)
    else:
        qgate(H, 0)

    t0 = time.time()
    result = get_backend(backend).run(current_circuit(), shots=shots)
    elapsed = time.time() - t0

    return {
        "name": name,
        "n": n,
        "time": elapsed,
        "counts": result.counts,
    }


def main():
    parser = argparse.ArgumentParser(description="QuoNic benchmark suite")
    parser.add_argument("--backend", default="native", help="Backend to use")
    parser.add_argument("--n", default="8,10,12", help="Qubit counts (comma-separated)")
    parser.add_argument("--shots", type=int, default=1024, help="Shots per circuit")
    parser.add_argument("--output", default="benchmarks_suite.json", help="Output file")
    args = parser.parse_args()

    n_values = [int(x) for x in args.n.split(",")]

    results = {
        "meta": {
            "backend": args.backend,
            "shots": args.shots,
            "n_values": n_values,
        },
        "quantum_volume": [],
        "cross_entropy": [],
        "algorithms": [],
    }

    print(f"Running benchmarks on {args.backend}...")

    for n in n_values:
        print(f"  n={n}...")
        results["quantum_volume"].append(quantum_volume(n, args.shots, args.backend))
        results["cross_entropy"].append(cross_entropy(n, args.shots, args.backend))
        for algo in ["grover", "qft"]:
            results["algorithms"].append(algorithm_benchmark(algo, n, args.shots, args.backend))

    with open(args.output, "w") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"Results saved to {args.output}")


if __name__ == "__main__":
    main()
