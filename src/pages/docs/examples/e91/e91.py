"""E91 key distribution / E91 密钥分发

E91 protocol using entangled pairs and Bell inequality.
E91 协议使用纠缠对和 Bell 不等式。

## Application / 应用场景
- Quantum key distribution (量子密钥分发)
- Entanglement verification (纠缠验证)
- Device-independent QKD (设备无关 QKD)

## Output / 输出
Shared secret key with security verification.
带有安全验证的共享密钥。"""

from quonic.algorithms import e91

result = e91(n_rounds=100)
print(f"Result: {result.value}")
