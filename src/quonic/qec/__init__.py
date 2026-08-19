"""Quantum Error Correction — stabilizer codes, syndrome extraction, and decoding.

Example::

    from quonic.qec import BitFlipCode, SteaneCode
    from quonic.qec import decode_mwpm

    code = BitFlipCode()
    encoded = code.encode(circuit)
    syndrome = code.syndrome(circuit)
    corrected = decode_mwpm(syndrome, code)
"""

from .code import BitFlipCode, ColorCode, CSSCode, PhaseFlipCode, ShorCode, SteaneCode, SurfaceCode
from .decoder import UnionFindDecoder, decode_lookup, decode_mwpm
from .end_to_end import QECResult, qec_round_trip
from .stabilizer import StabilizerCode

__all__ = [
    "BitFlipCode",
    "PhaseFlipCode",
    "ShorCode",
    "SteaneCode",
    "SurfaceCode",
    "ColorCode",
    "CSSCode",
    "StabilizerCode",
    "UnionFindDecoder",
    "decode_mwpm",
    "decode_lookup",
    "QECResult",
    "qec_round_trip",
]
