"""Plugin base classes.

Users subclass these to create custom backends, passes, and algorithms.
"""

from __future__ import annotations

from typing import Any

from ..ir import Circuit
from ..result import Result


class Plugin:
    """Base class for all plugins."""

    name: str = ""
    version: str = "0.1.0"
    description: str = ""


class BackendPlugin(Plugin):
    """Custom backend plugin.

    Subclass this to add a new backend to QuoNic.

    Example::

        class MyBackend(BackendPlugin):
            name = "my_backend"
            def run(self, circuit, shots=1024, **kwargs):
                # Your simulation logic here
                return Result.from_counts(counts, shots)
    """

    def run(
        self,
        circuit: Circuit,
        shots: int = 1024,
        noise: Any = None,
        method: str = "statevector",
    ) -> Result:
        """Run a circuit and return results."""
        raise NotImplementedError


class PassPlugin(Plugin):
    """Custom optimization pass plugin.

    Subclass this to add a new optimization pass.

    Example::

        class MyPass(PassPlugin):
            name = "my_pass"
            def run(self, circuit):
                # Your optimization logic here
                return optimized_circuit
    """

    def run(self, circuit: Circuit) -> Circuit:
        """Apply optimization pass to a circuit."""
        raise NotImplementedError


class AlgorithmPlugin(Plugin):
    """Custom algorithm plugin.

    Subclass this to add a new algorithm template.

    Example::

        class MyAlgorithm(AlgorithmPlugin):
            name = "my_algorithm"
            def run(self, n_qubits=4, **kwargs):
                # Your algorithm logic here
                return result
    """

    def run(self, **kwargs) -> Any:
        """Run the algorithm."""
        raise NotImplementedError
