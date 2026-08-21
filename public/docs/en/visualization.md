# Visualization Suite

QuoNic provides 23 visualization types covering user needs, scheduler evidence, algorithm teaching, and quantum state.

## Circuit Visualization

### Circuit Diagram

```python
from quonic.viz import circuit_diagram
circuit_diagram(circuit)
```

### Gate Distribution

```python
from quonic.viz import gate_distribution
gate_distribution(circuit)
```

## State Visualization

### Bloch Sphere

```python
from quonic.viz import bloch_sphere
bloch_sphere(state)
```

### State Vector

```python
from quonic.viz import state_vector
state_vector(state)
```

## Measurement Visualization

### Histogram

```python
from quonic.viz import histogram
histogram(results)
```

### Probability Distribution

```python
from quonic.viz import probability_distribution
probability_distribution(results)
```

## Scheduler Visualization

### Gantt Chart

```python
from quonic.viz import gantt_chart
gantt_chart(schedule)
```

### Critical Path

```python
from quonic.viz import critical_path
critical_path(schedule)
```

## Next Steps

- [Quick Start](quickstart.md)
- [Examples](examples/example_bell.html)
