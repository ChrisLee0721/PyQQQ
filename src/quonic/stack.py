"""全局电路栈。

qgate() 把门加到"当前电路"上。默认只有一个全局电路；
将来自定义门 / 函数作用域会 push / pop 新电路，所以用栈而非单变量。
"""

from .ir import Circuit


class CircuitStack:
    def __init__(self):
        self._stack = [Circuit()]

    @property
    def current(self):
        return self._stack[-1]

    def push(self):
        self._stack.append(Circuit())

    def pop(self):
        if len(self._stack) == 1:
            raise RuntimeError("电路栈已到底层，无法继续 pop")
        return self._stack.pop()

    def reset(self):
        self._stack = [Circuit()]


_default = CircuitStack()


def current_circuit():
    return _default.current


def reset():
    _default.reset()


def push():
    """压入一个新电路作用域（供 cwhile 等捕获循环体）。"""
    _default.push()


def pop():
    """弹出当前电路作用域，返回该电路。"""
    return _default.pop()
