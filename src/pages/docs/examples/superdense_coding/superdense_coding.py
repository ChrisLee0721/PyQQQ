"""Superdense Coding / 超密编码

Send 2 classical bits using 1 qubit.
用 1 个量子比特发送 2 个经典比特。

## Application / 应用场景
- Quantum communication (量子通信)
- Bandwidth doubling (带宽翻倍)
- Teleportation (隐形传态)

## Output / 输出
Decoded 2-bit message.
解码的 2 比特消息。"""

from quonic.algorithms import superdense_coding

for msg in ["00", "01", "10", "11"]:
    result = superdense_coding(message=msg, shots=100)
    # value is the decoded integer (0-3)
    decoded = f"{int(result.value):02b}"
    print(f"Sent: {msg}, Decoded: {decoded}")
