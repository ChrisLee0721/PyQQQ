# Changelog

All notable changes to this project are documented here.

## [0.11.0] - 2026-08-20

Exhaustive testing + real hardware verification + API lock.

### Added

- Exhaustive tests: cross-backend consistency + edge cases + integration, 771 tests passing
- Real hardware: Origin Quantum WK_C180 + AWS Rigetti Cepheus + Quantum Inspire Tuna
- ML framework complete: adjoint diff + GPU + batch + hybrid model + visualization
- MPS tensor network: expectation + canonicalize + DMRG + noise + custom gates
- ZX-calculus: 7 rewrite rules + circuit extraction + pattern matching

### API Freeze

After v1.0.0, follow semver 2.0.0:
- Patch (1.0.x): bug fix, no API change
- Minor (1.x.0): new feature, backward compatible
- Major (x.0.0): breaking change

## [0.10.0] - 2026-08-15

Initial public release.

### Features

- 12+ quantum backends
- 77 algorithm templates
- GPU acceleration
- Quantum error correction
- Quantum machine learning
