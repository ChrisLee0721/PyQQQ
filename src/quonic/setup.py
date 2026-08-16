"""python -m quonic.setup — one-click onboarding entry for real-hardware backends.

By default it onboards Quantum Inspire (the current sole real-hardware backend); when later adding IBM / Braket /
domestic hardware, resolve the corresponding backend's setup description via --backend, reusing the onboarding engine.
"""

from __future__ import annotations

from ._i18n import tr
from .backends.qi import QuantumInspireBackend
from .backends.setup_guide import diagnose, guided_setup


def main() -> int:
    # the current sole real-hardware backend is qi; when extending later, map to the corresponding setup via --backend
    setup = QuantumInspireBackend.setup

    if diagnose(setup).ready:
        print(tr("setup.ready", name=setup["name"]))
        return 0

    ok = guided_setup(setup)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
