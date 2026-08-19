"""Pulse definitions for quantum control.

Example::

    from quonic.pulse import GaussianPulse, DragPulse

    pulse = GaussianPulse(duration=20, sigma=5, amplitude=0.5)
    drag = DragPulse(duration=20, sigma=5, amplitude=0.5, beta=0.1)
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class GaussianPulse:
    """Gaussian pulse for single-qubit rotations.

    Args:
        duration: pulse duration in ns
        sigma: Gaussian width
        amplitude: peak amplitude
    """

    duration: int
    sigma: float
    amplitude: float

    def waveform(self) -> np.ndarray:
        """Generate the pulse waveform."""
        t = np.linspace(-self.duration / 2, self.duration / 2, self.duration)
        return self.amplitude * np.exp(-t**2 / (2 * self.sigma**2))


@dataclass
class DragPulse:
    """DRAG (Derivative Removal by Adiabatic Gate) pulse.

    Reduces leakage to non-computational states.

    Args:
        duration: pulse duration in ns
        sigma: Gaussian width
        amplitude: peak amplitude
        beta: DRAG coefficient
    """

    duration: int
    sigma: float
    amplitude: float
    beta: float

    def waveform(self) -> np.ndarray:
        """Generate the DRAG pulse waveform."""
        t = np.linspace(-self.duration / 2, self.duration / 2, self.duration)
        envelope = self.amplitude * np.exp(-t**2 / (2 * self.sigma**2))
        derivative = -t / self.sigma**2 * envelope
        return envelope + 1j * self.beta * derivative


@dataclass
class CrossResonancePulse:
    """Cross-resonance pulse for two-qubit gates.

    Args:
        duration: pulse duration in ns
        amplitude: pulse amplitude
        detuning: frequency detuning
    """

    duration: int
    amplitude: float
    detuning: float

    def waveform(self) -> np.ndarray:
        """Generate the CR pulse waveform."""
        t = np.linspace(0, self.duration, self.duration)
        return self.amplitude * np.exp(1j * 2 * np.pi * self.detuning * t)
