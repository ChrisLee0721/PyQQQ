"""后端适配器基类。"""

from abc import ABC, abstractmethod


class Backend(ABC):
    name: str = "base"

    @abstractmethod
    def run(self, circuit, shots: int = 1024) -> dict:
        """运行电路，返回 {'counts': {'00': 512, '11': 512}, 'shots': 1024}。"""
        raise NotImplementedError
