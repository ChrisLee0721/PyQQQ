"""creg + cwhile: repeat-until-success (RUS) prepares |0> deterministically.

A single qubit is measured repeatedly: each H + measure has a 50% chance of
yielding 0. The loop retries until it sees 0, so the final state is |0> with
certainty — the iteration count is random, the outcome is not.
"""

from quonic import creg, cwhile, qgate, qshow
from quonic.gates import H

flag = creg("flag")
with cwhile(flag, until=0):
    qgate(H, 0)
    flag.measure(0)

qshow(backend="native")  # cwhile 逐 shot 动态执行，仅 native 后端支持
