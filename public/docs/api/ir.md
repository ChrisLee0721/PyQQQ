# Core IR API

The intermediate representation (IR) is the backbone of QuoNic. All circuits are represented as a list of operations on qubits.

中间表示（IR）是 QuoNic 的核心。所有电路都表示为量子比特上的操作列表。

## Circuit — Circuit Representation / 电路表示

```python
from quonic.ir import Circuit

circuit = Circuit()
circuit.add(GateOperation("h", [0]))
circuit.add(GateOperation("cx", [0, 1]))

print(circuit.gate_count())  # 2
print(circuit.num_qubits)    # 2
print(circuit.depth())        # 2
```

### Circuit properties / 电路属性

| Property | Description |
|----------|-------------|
| `gate_count()` | Number of gates |
| `num_qubits` | Number of qubits |
| `depth()` | Circuit depth |
| `measured_qubits()` | Qubits that are measured |
| `unmeasured_qubits()` | Qubits not measured |
| `is_empty()` | True if no operations |

## GateOperation — Gate Operation / 门操作

```python
from quonic.ir import GateOperation

op = GateOperation("h", [0])           # H on qubit 0
op = GateOperation("cx", [0, 1])       # CNOT: control=0, target=1
op = GateOperation("ry", [0], [0.5])   # Ry(0.5) on qubit 0
```

## CMeasureOperation — Mid-Circuit Measurement / 中段测量

```python
from quonic.ir import CMeasureOperation

# Measure qubit 0 into classical register "c"
op = CMeasureOperation(qubit=0, creg="c")
```

## ClassicalIfOperation — Classical Conditional / 经典条件

```python
from quonic.ir import ClassicalIfOperation, CRegCondition

# if c[0] == 1: apply X
condition = CRegCondition(creg="c", index=0, value=1)
op = ClassicalIfOperation(condition, then_ops=[GateOperation("x", [1])])
```

## ClassicalWhileOperation — Classical Loop / 经典循环

```python
from quonic.ir import ClassicalWhileOperation, CRegCondition

# while c[0] == 0: apply gate and measure
condition = CRegCondition(creg="c", index=0, value=0)
body = [GateOperation("h", [0]), CMeasureOperation(0, "c")]
op = ClassicalWhileOperation(condition, body)
```

## Examples / 示例

### Build circuit manually / 手动构建电路

```python
from quonic.ir import Circuit, GateOperation

circuit = Circuit()
circuit.add(GateOperation("h", [0]))
for i in range(7):
    circuit.add(GateOperation("cx", [i, i + 1]))

print(f"GHZ-8: {circuit.gate_count()} gates, depth {circuit.depth()}")
```

### Access circuit operations / 访问电路操作

```python
for op in circuit.operations:
    print(f"{op.name} on qubits {op.qubits}")
```
