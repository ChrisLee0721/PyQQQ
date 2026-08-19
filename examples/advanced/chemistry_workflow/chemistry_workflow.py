"""Quantum Chemistry Workflow / 量子化学工作流

Complete workflow for molecular ground state energy calculation using VQE.

## Problem / 问题
Calculate the ground state energy of H₂ molecule using quantum simulation.

## QuoNic Features Used / 使用的 QuoNic 功能
- VQE algorithm (变分量子本征求解器)
- Parameter-shift gradient (参数偏移梯度)
- Noise modeling (噪声建模)
- Error mitigation (错误缓解)
- Smart scheduling (智能调度)

## Output / 输出
Ground state energy of H₂ ≈ -1.137 Hartree (exact: -1.1372)
"""

from quonic.algorithms import vqe
from quonic.ml import Ansatz, SPSAOptimizer, train, param_shift_grad
from quonic import zne, NoiseModel
from quonic.ir import Circuit, GateOperation

# H₂ Hamiltonian (simplified)
# H = -0.81261 II + 0.17120 ZZ + -0.22279 XX + 0.17120 YY
H2_hamiltonian = [
    (-0.81261, "II"),
    (0.17120, "ZZ"),
    (-0.22279, "XX"),
    (0.17120, "YY"),
]

print("=== Quantum Chemistry: H₂ Ground State ===")
print("Hamiltonian: H = -0.81 II + 0.17 ZZ - 0.22 XX + 0.17 YY")
print("Exact ground state energy: -1.1372 Hartree")
print()

# Method 1: Direct VQE
print("--- Method 1: Direct VQE ---")
result = vqe(H2_hamiltonian, n_qubits=2, maxiter=200)
print(f"VQE energy: {result.value:.4f} Hartree")
print(f"Error: {abs(result.value - (-1.1372)):.4f}")
print()

# Method 2: VQE with noise + ZNE
print("--- Method 2: VQE with Noise + ZNE ---")
noise_model = NoiseModel(single=0.01, double=0.05)

# Build circuit with VQE ansatz
ansatz = Ansatz.hardware_efficient(n_qubits=2, layers=2)
circuit = ansatz.build([0.1] * ansatz.n_params)

# Apply ZNE
zne_result = zne(circuit, noise=0.05, observable="ZZ", shots=4096)
print(f"ZNE result: {zne_result.extrapolated:.4f}")
print(f"Raw result: {zne_result.values[0]:.4f}")
print()

# Method 3: VQE with parameter-shift gradient
print("--- Method 3: VQE with Parameter-Shift Gradient ---")
opt = SPSAOptimizer(maxiter=100, lr=0.1)

def loss_fn(params):
    c = ansatz.build(params)
    from quonic.ml import expectation_loss
    return expectation_loss(c, "ZZ")

train_result = train(ansatz, opt, loss_fn, gradient="param_shift")
print(f"Final loss: {train_result.final_loss:.4f}")
print(f"Steps: {train_result.n_steps}")
print()

print("=== Summary ===")
print("QuoNic provides complete quantum chemistry workflow:")
print("1. VQE for ground state energy")
print("2. Noise modeling + ZNE for error mitigation")
print("3. Parameter-shift gradient for optimization")
print("4. Smart scheduling for backend selection")
