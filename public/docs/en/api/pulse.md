# Pulse Control

QuoNic supports pulse-level control of quantum gates.

## Features

- Custom pulse shapes
- Pulse scheduling
- Calibrations

## Usage

```python
from quonic.pulse import Pulse

pulse = Pulse(duration=100, amplitude=1.0, shape='gaussian')
```
