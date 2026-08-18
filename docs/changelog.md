# Changelog

See the [full changelog](https://github.com/ChrisLee0721/QuoNic/blob/main/CHANGELOG.md) on GitHub.

## Latest: v0.5.0 (2026-08-19)

### New
- GPU smart scheduling (`method="gpu"`)
- CuPy universal engine
- 7 backend GPU variants
- Circuit optimization passes (`optimize()`)
- `requires_grad` for autodiff-aware scheduling
- Multi-qubit qif (Toffoli, Fredkin, MCZ)
- Nested qif (`then_ops` / `else_ops`)
- GPU scheduler benchmark

### Fixed
- ZNE success metric extrapolation
- Readout calibration regularization
- CuPy multi-qubit gate vectorization
- TensorCircuit numpy patch isolation

### Stats
- 509 tests passed
- 12 backends
- 77 algorithm templates
