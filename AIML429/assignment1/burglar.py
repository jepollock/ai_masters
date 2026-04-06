import numpy as np
from belief_prop import *
from gibbs import run_gibbs, print_marginals

# This is the classic belief net example: burglar, earthquake, alarm.

def make_network():
    # Define the variables first.
    b = Multiplier('burglar', 2)
    e = Multiplier('earthquake', 2)
    a = Multiplier('alarm', 2)
    j = Multiplier(name="john_called", vlen=2)
    m = Multiplier(name="mary_called", vlen=2)
    # And now the factors, each with a phi matrix.
    B = Summer('B', [b], phi=np.array([.2, .8]))
    E = Summer('E', [e], phi=np.array([.4, .6]))
    A = Summer(name='A', edges=[b, e, a], phi=np.array([[[.9, .1], [.6, .4]], [[.3, .7], [.5, .5]]]))
    J = Summer(name='J', edges=[j, a], phi=np.array([[.95,.1],[.05,.9]]))
    M = Summer(name='M', edges=[m,a], phi=np.array([[.99,0.3],[.01,.07]]))
    return [b, e, a, m, j], [B, E, A, M, J]


if __name__ == '__main__':
    variables, factors = make_network()
    b, e, a, m, j = variables
    B, E, A, M, J = factors
    theNodes = variables + factors

    # Initialise all messages: every terminal node dings its neighbour.
    print('############################# Initialising all messages')
    for node in theNodes:
        if len(node.edges) == 1:  # i.e. it has one edge so it's a terminal node.
            node.initialDing()

    # Now we can get down to business....
    for node in variables:
        node.display()
    A.display()
    part_a_c=False
    part_d = False
    part_e = not part_d
    if (part_a_c):
        print('############################# observe', b.name)
        Observation(b, np.array([0.0, 1.0]))
        for node in variables:
            node.display()  # Notice e unchanged, despite message from A!
            # This wouldn't happen in a general MRF graph -- must be due to normalisation.

        print('############################# observe', a.name)
        Observation(a, np.array([0.0, 1.0]))
        for node in variables:
            node.display()  # e is different now: "explaining away"
        A.display()

    if (part_d):
        print('############################# observe', j.name)
        Observation(j, np.array([0.0, 1.0]))
        for node in variables:
            node.display()  # Notice e unchanged, despite message from A!
            # This wouldn't happen in a general MRF graph -- must be due to normalisation.

        print('############################# observe', m.name)
        Observation(m, np.array([0.0, 1.0]))
        for node in variables:
            node.display()  # e is different now: "explaining away"
        A.display()


    VERBOSE = False
    print('############################# Gibbs sampling (ground truth for comparison)')
    print('Prior:')
    variables2, factors2 = make_network()  # fresh graph: BP has modified the first one
    print_marginals(variables2, run_gibbs(variables2, factors2, seed=None))
    variables2, factors2 = make_network()
    b2, e2, a2, m2, j2 = variables2
    print(f'Observe {m2.name}=state1, {j2.name}=state1:')
    print_marginals(variables2, run_gibbs(variables2, factors2, observed={j2: 1, m2: 1}, seed=None))

