"""Quantum Bayesian inference demo.

Quantum version of Bayesian updating.
Output: posterior probabilities.
"""

from quonic.algorithms import quantum_bayesian_demo

result = quantum_bayesian_demo(prior_h0=0.5, likelihood_h0=0.8, likelihood_h1=0.3)
print(result.counts)
