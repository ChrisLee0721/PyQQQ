# Distributed Quantum Computing API / 分布式量子计算 API

Multi-node quantum computing with entanglement distribution and remote gates.

多节点量子计算，支持纠缠分发和远程门。

## Quick Start / 快速开始

```python
from quonic.distributed import QuantumNetwork, create_bell_pair, remote_cnot

# Create a 2-node network
network = QuantumNetwork(["Alice", "Bob"])

# Distribute entanglement
pair = create_bell_pair("Alice", "Bob")
network.add_entanglement(pair)

# Remote CNOT via teleportation
remote_cnot(network, control="Alice:0", target="Bob:0")
```

## QuantumNetwork — Network Topology / 网络拓扑

```python
from quonic.distributed import QuantumNetwork

# Create network with nodes
network = QuantumNetwork(["Node_A", "Node_B", "Node_C"])

# Add entanglement links
network.add_entanglement(create_bell_pair("Node_A", "Node_B"))
network.add_entanglement(create_bell_pair("Node_B", "Node_C"))

print(network.topology())  # Show network graph
```

## Entanglement / 纠缠

### create_bell_pair(node1, node2)

Create a Bell pair distributed between two nodes.

创建分布在两个节点之间的 Bell 对。

```python
from quonic.distributed import create_bell_pair

pair = create_bell_pair("Alice", "Bob")
print(pair.qubit_alice)  # Qubit index on Alice
print(pair.qubit_bob)    # Qubit index on Bob
```

### distribute_entanglement(network, pairs)

Distribute multiple entanglement pairs across the network.

在网络上分发多个纠缠对。

```python
from quonic.distributed import distribute_entanglement

pairs = distribute_entanglement(network, n_pairs=10)
```

## Remote Gates / 远程门

### remote_cnot(network, control, target)

Execute CNOT between qubits on different nodes via teleportation.

通过隐形传态在不同节点的量子比特之间执行 CNOT。

```python
from quonic.distributed import remote_cnot

# Remote CNOT: Alice's qubit 0 controls Bob's qubit 0
remote_cnot(network, control="Alice:0", target="Bob:0")
```

### teleport_state(network, source, target)

Teleport a quantum state from one node to another.

将量子态从一个节点隐形传态到另一个节点。

```python
from quonic.distributed import teleport_state

teleport_state(network, source="Alice:0", target="Bob:0")
```

## Task Scheduling / 任务调度

### schedule_task(network, circuit)

Schedule circuit execution across distributed nodes.

调度电路在分布式节点上的执行。

```python
from quonic.distributed import schedule_task

schedule = schedule_task(network, circuit)
for step in schedule.steps:
    print(f"  {step.node}: {step.operation}")
```

## Examples / 示例

### Distributed GHZ / 分布式 GHZ

```python
from quonic.distributed import QuantumNetwork, create_bell_pair, remote_cnot

# 3-node network
network = QuantumNetwork(["A", "B", "C"])
network.add_entanglement(create_bell_pair("A", "B"))
network.add_entanglement(create_bell_pair("B", "C"))

# Build distributed GHZ state
# H on A:0
# CX A:0 → B:0 (remote)
# CX B:0 → C:0 (remote)
remote_cnot(network, "A:0", "B:0")
remote_cnot(network, "B:0", "C:0")
```

### Quantum repeater / 量子中继

```python
from quonic.distributed import QuantumNetwork, create_bell_pair

# Linear chain: A — B — C — D
network = QuantumNetwork(["A", "B", "C", "D"])
for i, nodes in enumerate([("A","B"), ("B","C"), ("C","D")]):
    network.add_entanglement(create_bell_pair(*nodes))

# Entanglement swapping at B and C
# 纠缠交换在 B 和 C 处
```
