# Core IR

The intermediate representation (IR) is the backbone of QuoNic. All circuits are represented as a list of operations on qubits.

::: quonic.ir.Circuit
    options:
      show_source: true
      members: [add, allocate, depth, gate_count, measured_qubits, unmeasured_qubits, is_empty]

::: quonic.ir.GateOperation
    options:
      show_source: true

::: quonic.ir.CMeasureOperation
    options:
      show_source: true

::: quonic.ir.ClassicalIfOperation
    options:
      show_source: true

::: quonic.ir.ClassicalWhileOperation
    options:
      show_source: true

::: quonic.ir.CRegCondition
    options:
      show_source: true
