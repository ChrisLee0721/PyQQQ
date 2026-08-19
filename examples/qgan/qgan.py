"""Quantum GAN (Generative Adversarial Network) demo.

Quantum generator + classical discriminator for data generation.
Output: generated distribution.
"""

from quonic.algorithms import qgan_demo

result = qgan_demo(n_steps=50)
print(result.counts)
