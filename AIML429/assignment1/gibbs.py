"""
gibbs.py -- Gibbs sampling for factor graphs defined with markov.py

Each Summer node already stores phi (the CPT/potential) and edges (the
connected Multiplier nodes in order).  The sampler reads those directly,
so markov.py needs no changes at all.
"""

import numpy as np
import belief_prop
from belief_prop import Multiplier, Summer

# Silence the message-passing trace from belief_prop.py while building networks.


def gibbs_conditional(var, factors, states):
    """Return the normalised conditional distribution P(var | all others)."""
    cond = np.ones(var.vlen)
    for f in factors:
        if var not in f.edges:
            continue
        # Slice f.phi: ':' on var's axis, current state on every other axis.
        idx = tuple(slice(None) if f.edges[j] is var else states[f.edges[j]]
                    for j in range(len(f.edges)))
        cond *= f.phi[idx]
    cond /= cond.sum()
    return cond


def run_gibbs(variables, factors, n_samples=20000, burnin=2000,
              observed=None, seed=None):
    """
    Gibbs sampling on a factor graph.

    variables : list of Multiplier (variable) nodes
    factors   : list of Summer (factor / CPT) nodes
    n_samples : samples to collect after burn-in
    burnin    : initial samples to discard
    observed  : dict {Multiplier: state_index} for hard evidence
    seed      : optional int for reproducibility

    Returns {Multiplier: marginal probability array}.
    """
    if observed is None:
        observed = {}
    rng = np.random.default_rng(seed)

    # Initialise states: fix observed variables, randomise the rest.
    states = {v: (observed[v] if v in observed else int(rng.integers(v.vlen)))
              for v in variables}
    free = [v for v in variables if v not in observed]
    counts = {v: np.zeros(v.vlen) for v in variables}

    for t in range(burnin + n_samples):
        for v in free:
            p = gibbs_conditional(v, factors, states)
            states[v] = int(rng.choice(v.vlen, p=p))
        if t >= burnin:
            for v in variables:
                counts[v][states[v]] += 1

    return {v: counts[v] / counts[v].sum() for v in variables}


def print_marginals(variables, marginals):
    for v in variables:
        print(f'    {v.name:12s}: {np.round(marginals[v], 4)}')


if __name__ == '__main__':
    print('gibbs.py is a library. Run burglar.py or rain.py to see BP and Gibbs compared.')
