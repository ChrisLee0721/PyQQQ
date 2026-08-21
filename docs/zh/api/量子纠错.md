# Quantum Error Correction API / 量子纠错 API

## qec_round_trip() — End-to-End QEC / 端到端纠错

Run a complete QEC simulation: encode → inject noise → decode → verify.

运行完整的 QEC 模拟：编码 → 注入噪声 → 解码 → 验证。

```python
from quonic.qec import qec_round_trip

# Bit-flip code with 1% error rate
# 比特翻转码，1% 错误率
result = qec_round_trip(code="bit_flip", error_rate=0.01, shots=1000)
print(result.success_rate)  # ~0.97 (97% success)
print(result.logical_error_rate)  # ~0.03
```

## Error Correction Codes / 纠错码

### BitFlipCode — 3-qubit repetition / 3 量子比特重复码

```python
from quonic.qec import BitFlipCode

code = BitFlipCode()
code.encode(qubit=0)           # |ψ⟩ → |ψψψ⟩
code.inject_noise(error_rate=0.05)
syndrome = code.syndrome()     # Detect which qubit flipped
code.correct(syndrome)         # Fix the error
```

### PhaseFlipCode — 3-qubit phase code / 3 量子比特相位码

```python
from quonic.qec import PhaseFlipCode

code = PhaseFlipCode()
code.encode(qubit=0)           # |ψ⟩ → phase-encoded
code.inject_noise(error_rate=0.05)
code.correct(code.syndrome())
```

### SteaneCode — 7-qubit CSS code / 7 量子比特 CSS 码

```python
from quonic.qec import SteaneCode

code = SteaneCode()
code.encode(qubit=0)           # 7-qubit encoding
code.inject_noise(error_rate=0.01)
code.correct(code.syndrome())  # Corrects any single error
```

### ShorCode — 9-qubit concatenated / 9 量子比特级联码

```python
from quonic.qec import ShorCode

code = ShorCode()
code.encode(qubit=0)           # 9-qubit encoding
code.inject_noise(error_rate=0.01)
code.correct(code.syndrome())  # Corrects any single error
```

## Stabilizer Formalism / 稳定子形式

```python
from quonic.qec import StabilizerCode

# Define stabilizers for 3-qubit bit-flip code
stabilizers = ["ZZI", "IZZ"]
code = StabilizerCode(stabilizers)
syndrome = code.compute_syndrome()
```

## Decoders / 解码器

```python
from quonic.qec import decode_mwpm, decode_lookup, UnionFindDecoder

# Minimum Weight Perfect Matching
syndrome = [1, 0, 1]
correction = decode_mwpm(syndrome, code)

# Lookup table (fast for small codes)
correction = decode_lookup(syndrome, code)

# Union-Find (scalable for surface codes)
decoder = UnionFindDecoder(code)
correction = decoder.decode(syndrome)
```

## Supported Codes / 支持的纠错码

| Code | Qubits | Corrects | Type |
|------|--------|----------|------|
| BitFlipCode | 3 | 1 bit-flip | Repetition |
| PhaseFlipCode | 3 | 1 phase-flip | Repetition |
| ShorCode | 9 | 1 arbitrary | Concatenated |
| SteaneCode | 7 | 1 arbitrary | CSS |
| SurfaceCode | d² | ⌊d/2⌋ | Topological |
| ColorCode | varies | 1 arbitrary | Topological |
| CSSCode | custom | varies | General CSS |
