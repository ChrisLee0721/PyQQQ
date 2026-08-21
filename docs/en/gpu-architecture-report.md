# GPU Architecture Report

## Overview

QuoNic supports GPU acceleration for quantum simulation using NVIDIA CUDA.

## Architecture

### CUDA Backend

QuoNic's CUDA backend uses NVIDIA's cuStateVec library for high-performance quantum simulation.

### Memory Management

GPU memory is managed automatically. Large circuits are split into chunks that fit in GPU memory.

### Multi-GPU Support

QuoNic supports multi-GPU simulation for very large circuits.

## Performance

### Single GPU

- 20 qubits: 0.1s
- 25 qubits: 2.5s
- 30 qubits: 80s

### Multi-GPU

- 30 qubits (2 GPUs): 45s
- 35 qubits (4 GPUs): 120s

## Requirements

- NVIDIA GPU with CUDA support
- CUDA 11.0 or later
- 8GB+ GPU memory recommended

## Next Steps

- [GPU Acceleration Tutorial](tutorials/gpu_acceleration.md)
- [Quick Start](quickstart.md)
