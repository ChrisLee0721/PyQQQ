# Tutorial 05: Advanced Features

Quantum control flow, multi-bit registers, and circuit optimization.

## Quantum Superposition Control (qif)

`qif` creates coherent superposition — both branches happen at once:

```python
from quonic import qif, qgate, qshow
from quonic.gates import H, X, Z, I

qgate(H, 0)  # Control qubit in superposition
qif(0).then(X, 1).else_(Z, 1)  # Both branches applied coherently
qshow()
```

## Multi-Qubit qif (v0.5.0+)

Control multi-qubit gates:

```python
from quonic.gates import CX, SWAP

# Controlled-CX = Toffoli
qif(0).then(CX, 1, 2).else_(I, 1, 2)

# Controlled-SWAP = Fredkin
qif(0).then(SWAP, 1, 2).else_(I, 1, 2)
```

## Nested qif (v0.5.0+)

```python
inner = qif(1).then(X, 2).else_(Z, 2)
qif(0).then_ops(inner).else_ops([inner[0]])
```

## Classical Control Flow (cif)

`cif` measures first, then branches:

```python
from quonic import cif, creg

qgate(H, 0)
cif(0).then(X, 1).else_(Z, 1)  # Measure q0, then branch
qshow()
```

## Multi-Bit Classical Registers

```python
reg = creg("reg", width=2)
reg.measure(0, bit=0)
reg.measure(1, bit=1)
cif(reg, 2).then(X, 2).else_(I, 2)  # Branch on reg == 2
```

## Repeat-Until-Success (cwhile)

```python
flag = creg("flag")
with cwhile(flag, until=0) as loop:
    qgate(H, 0)
    flag.measure(0)

static = loop.groverize()  # Compile to static Grover circuit
qshow(static)
```

## Circuit Optimization (v0.5.0+)

```python
from quonic import optimize

optimized = optimize(circuit)
print(f"Before: {circuit.gate_count()} gates")
print(f"After: {optimized.gate_count()} gates")
```

Available passes:
- **cancel**: Remove adjacent self-inverse pairs (X·X, H·H, CX·CX)
- **commute**: Reorder gates to enable more cancellations
- **peephole**: Replace known patterns (CX·CX·CX → SWAP)
