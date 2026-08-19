"""Quantum Reinforcement Learning demo.

Quantum agent learning in a classical environment.
Output: learned policy.
"""

from quonic.algorithms import qrl_demo

result = qrl_demo(n_episodes=10)
print(result.counts)
