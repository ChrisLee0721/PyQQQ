"""后端适配器基类。"""

from abc import ABC, abstractmethod

from ..result import Result


class Backend(ABC):
    name: str = "base"
    # 后端支持的方法名集合（子类覆盖）。调度器据此做能力匹配与降级。
    methods: frozenset = frozenset({"statevector"})

    def supports(self, method: str) -> bool:
        """该后端是否支持给定的模拟 method。"""
        return method in self.methods

    @abstractmethod
    def run(self, circuit, shots: int = 1024, noise=None, method: str = "statevector") -> Result:
        """运行电路，返回一个 kind="counts" 的 Result。

        noise 可为 NoiseModel、一个 [0,1] 内的概率数值或 None（无噪声）。
        method 为模拟方法（如 "statevector" / "stabilizer" / "matrix_product_state"），
        仅对支持多方法的后端（如 Qiskit Aer）有意义，其余后端忽略。
        """
        raise NotImplementedError
