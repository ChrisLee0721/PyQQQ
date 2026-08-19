"""Quantum Error Correction Workflow / 量子纠错工作流

Complete workflow for quantum error correction using QEC module.

## Problem / 问题
Demonstrate quantum error correction with noise modeling and decoding.

## QuoNic Features Used / 使用的 QuoNic 功能
- QEC codes (量子纠错码)
- Stabilizer formalism (稳定子形式)
- Decoders (解码器)
- Noise modeling (噪声建模)
- Readout calibration (读出校准)

## Output / 输出
Error correction performance comparison.
"""

from quonic.qec import (
    BitFlipCode, PhaseFlipCode, SteaneCode,
    StabilizerCode, UnionFindDecoder,
    decode_mwpm, decode_lookup,
    qec_round_trip,
)
from quonic.ir import Circuit, GateOperation
import numpy as np

print("=== Quantum Error Correction Workflow ===")
print()

# 1. Bit-flip code
print("--- 1. Bit-flip Code ---")
code = BitFlipCode()
print(f"Code: [{code.n_total}, {code.n_data}, 3]")
print(f"Can correct: single bit-flip errors")
print()

# 2. End-to-end QEC
print("--- 2. End-to-End QEC ---")
for code_name in ["bit_flip", "phase_flip", "steane"]:
    result = qec_round_trip(code=code_name, error_rate=0.01, shots=10000)
    print(f"{code_name}:")
    print(f"  Physical error rate: {result.physical_error_rate:.4f}")
    print(f"  Logical error rate: {result.logical_error_rate:.4f}")
    print(f"  Improvement: {result.physical_error_rate / max(result.logical_error_rate, 0.0001):.1f}x")
print()

# 3. Stabilizer code
print("--- 3. Stabilizer Code ---")
stab = StabilizerCode(["ZZII", "IIZZ", "XIII", "IIXI"])
print(f"Stabilizers: {stab.stabilizers}")
print(f"Qubits: {stab.n_qubits}")
print(f"Distance: {stab.distance}")
print()

# 4. Decoders
print("--- 4. Decoders ---")
# MWPM decoder
correction = decode_mwpm([1, 0], BitFlipCode())
print(f"MWPM correction for syndrome [1,0]: {correction}")

# Lookup decoder
correction = decode_lookup([1, 0], BitFlipCode())
print(f"Lookup correction for syndrome [1,0]: {correction}")

# Union-Find decoder
decoder = UnionFindDecoder(BitFlipCode())
correction = decoder.decode([1, 0])
print(f"Union-Find correction for syndrome [1,0]: {correction}")
print()

# 5. Error rate analysis
print("--- 5. Error Rate Analysis ---")
error_rates = [0.001, 0.005, 0.01, 0.05, 0.1]
for rate in error_rates:
    result = qec_round_trip(code="bit_flip", error_rate=rate, shots=5000)
    print(f"  Physical: {rate:.3f} → Logical: {result.logical_error_rate:.4f}")
print()

print("=== Summary ===")
print("QuoNic provides complete QEC workflow:")
print("1. Multiple error correction codes")
print("2. Stabilizer formalism for syndrome extraction")
print("3. Multiple decoders (MWPM, lookup, Union-Find)")
print("4. End-to-end QEC simulation")
print("5. Error rate analysis")
