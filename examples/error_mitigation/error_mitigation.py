"""Error mitigation demo — shows ZNE and readout calibration.

Demonstrates:
  1. Zero-noise extrapolation (ZNE) with linear and exponential fits
  2. Readout calibration (per-qubit and correlated)
  3. Stacking ZNE + readout calibration for best results

Usage:
    python examples/error_mitigation/error_mitigation.py
"""


from quonic import calibrate, qgate, reset, zne
from quonic.backends import get_backend
from quonic.gates import CX, H
from quonic.ir import Circuit, GateOperation
from quonic.noise import NoiseModel
from quonic.stack import current_circuit


def _take():
    c = current_circuit()
    reset()
    return c


def demo_zne():
    """Zero-noise extrapolation."""
    print("=" * 60)
    print("1. Zero-noise extrapolation (ZNE)")
    print("=" * 60)

    # Build a simple circuit: X gate on qubit 0
    c = Circuit()
    c.add(GateOperation("x", (0,)))
    c.add(GateOperation("measure", (0,)))

    noise = 0.05
    shots = 4096

    # Run with noise (no mitigation)
    be = get_backend("native")
    raw = be.run(circuit=c, shots=shots, noise=noise)
    raw_p = raw.counts.get("1", 0) / shots
    print(f"  Raw (noise={noise}): P(|1>) = {raw_p:.3f}")

    # ZNE with linear extrapolation
    res_lin = zne(c, noise=noise, target="1", shots=shots, extrapolation="linear")
    print(f"  ZNE linear:    P(|1>) = {res_lin.extrapolated:.3f}")
    print(f"    λ values:    {res_lin.values}")

    # ZNE with exponential extrapolation
    res_exp = zne(c, noise=noise, target="1", shots=shots, extrapolation="exponential")
    print(f"  ZNE exponential: P(|1>) = {res_exp.extrapolated:.3f}")

    print("  Ideal: P(|1>) = 1.000")
    print()


def demo_readout_calibration():
    """Readout calibration."""
    print("=" * 60)
    print("2. Readout calibration")
    print("=" * 60)

    n = 2
    noise = NoiseModel(readout=0.05)
    shots = 4096

    # Build a Bell circuit
    reset()
    qgate(H, 0)
    qgate(CX, 0, 1)
    circuit = _take()

    # Run with readout noise
    be = get_backend("native")
    raw = be.run(circuit, shots=shots, noise=noise)
    print(f"  Raw (readout noise={noise.readout}): {raw.counts}")

    # Per-qubit readout calibration
    cal = calibrate(n, backend="native", shots=shots, noise=noise)
    corrected = cal.apply(raw.counts, shots)
    print(f"  Per-qubit calibrated: {corrected}")

    # Correlated readout calibration
    cal_corr = calibrate(n, backend="native", shots=shots, noise=noise, correlated=True)
    corrected_corr = cal_corr.apply(raw.counts, shots)
    print(f"  Correlated calibrated: {corrected_corr}")
    print()


def demo_stacking():
    """Stacking ZNE + readout calibration."""
    print("=" * 60)
    print("3. Stacking ZNE + readout calibration")
    print("=" * 60)

    # Build a groverize circuit (success probability ~1)
    c = Circuit()
    c.add(GateOperation("x", (0,)))
    c.add(GateOperation("x", (1,)))
    c.add(GateOperation("ccx", (0, 1, 2)))
    c.add(GateOperation("measure", (0,)))
    c.add(GateOperation("measure", (1,)))
    c.add(GateOperation("measure", (2,)))

    noise = 0.05
    shots = 4096
    target = "111"

    # Raw
    be = get_backend("native")
    raw = be.run(circuit=c, shots=shots, noise=noise)
    raw_p = raw.counts.get(target, 0) / shots
    print(f"  Raw: P({target}) = {raw_p:.3f}")

    # ZNE only
    res_zne = zne(c, noise=noise, target=target, shots=shots, extrapolation="exponential")
    print(f"  ZNE exponential: P({target}) = {res_zne.extrapolated:.3f}")

    # Readout calibration only
    cal = calibrate(3, backend="native", shots=shots, noise=NoiseModel(readout=noise))
    corrected = cal.apply(raw.counts, shots)
    cal_p = corrected.get(target, 0) / shots
    print(f"  Readout cal: P({target}) = {cal_p:.3f}")

    # Stacked: ZNE + readout calibration
    res_stacked = zne(
        c, noise=noise, target=target, shots=shots,
        calibration=cal, extrapolation="exponential"
    )
    print(f"  Stacked (ZNE + cal): P({target}) = {res_stacked.extrapolated:.3f}")

    print(f"  Ideal: P({target}) = 1.000")
    print()


def main():
    print("QuoNic Error Mitigation Demo")
    print()

    demo_zne()
    demo_readout_calibration()
    demo_stacking()

    print("=" * 60)
    print("Done! Error mitigation improves result quality on noisy hardware.")
    print("Use zne() for zero-noise extrapolation and calibrate() for readout correction.")
    print("=" * 60)


if __name__ == "__main__":
    main()
