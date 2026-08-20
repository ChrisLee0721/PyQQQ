"""Quantum Error Correction Workflow / 量子纠错工作流

Complete QEC workflow with noise modeling and decoding.
带有噪声建模和解码的完整 QEC 工作流。

## Application / 应用场景
- Fault-tolerant computing (容错计算)
- Quantum memory (量子存储)
- Logical qubits (逻辑比特)

## Output / 输出
Error correction performance comparison.
纠错性能对比。"""


from quonic.qec import (
    BitFlipCode,
    StabilizerCode,
    UnionFindDecoder,
    decode_lookup,
    decode_mwpm,
    qec_round_trip,
)

print("=== Quantum Error Correction Workflow ===")
print()

# 1. Bit-flip code
print("--- 1. Bit-flip Code ---")
code = BitFlipCode()
print(f"Code: [{code.n_total}, {code.n_data}, 3]")
print("Can correct: single bit-flip errors")
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
