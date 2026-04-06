"""
Inference in graphical models by message passing.
Marcus Frean and Tony Vignaux
"""
import numpy as np

VERBOSE = True

# set to False to suppress the message-passing trace

def listLessOne(alist, k):
    return alist[0:k] + alist[k+1:len(alist)]

class Node:
    def __init__(self, name=''):
        self.name = name
        self.edges = []
        self.msg = []

    def __str__(self):
        return self.name

    def ding(self, toNode, outboundMsg, depth):
        if depth < 10:
            depth += 1
            if VERBOSE:
                print(f'  [msg] {self.name} → {toNode.name}: {np.round(np.asarray(outboundMsg).ravel(), 4)}')
            toNode.respondToMessage(self, outboundMsg, depth)

    def respondToMessage(self, fromNode, inboundMsg, depth):
        k = self.edges.index(fromNode)
        self.msg[k] = inboundMsg
        receivers = listLessOne(self.edges, k)  # all neighbours except the sender
        for r in receivers:
            i = self.edges.index(r)
            newMsg = self.calcMessage(i)
            self.ding(r, newMsg, depth)

class Multiplier(Node):
    def __init__(self, name='', vlen=1):
        super().__init__(name)
        self.vlen = vlen
        self.edges = []
        self.msg = [np.ones(vlen)] * len(self.edges)  # Ensure messages are initialized correctly
        self.observed = False

    def display(self):
        print('--------------------------------------------')
        print(f'node {self.name}')
        if self.observed:
            print('has been observed')
        for i in range(len(self.edges)):
            print(f'from node: {self.edges[i]} msg:', self.msg[i])
        
        # Calculate the product across the first axis, assuming msg contains multiple arrays
        if len(self.msg) > 0:
            p = np.prod(np.stack(self.msg), axis=0)
            posterior = p / np.sum(p)  # Normalize to get probabilities
            print('posterior:', posterior)
        else:
            print("No messages received yet")

    def calcMessage(self, i):
        if len(self.msg) > 1:
            newMsg = np.prod(np.array(listLessOne(self.msg, i)), axis=0)
        else:
            newMsg = np.ones(self.vlen)  # Fallback if no other messages
        return newMsg

    def initialDing(self):
        print('Initial ding from terminal node', self.name, 'to', self.edges[0].name)
        depth = 0
        self.ding(self.edges[0], np.ones(self.vlen), depth)  # 1D uniform message

class Summer(Node):
    def __init__(self, name='', edges=None, phi=None):
        super().__init__(name)
        if edges is None:
            edges = []
        if phi is None:
            phi = np.array([])
        self.edges = edges
        self.msg = [1] * len(self.edges)
        self.phi = phi

        for i, neighbour in enumerate(self.edges):
            self.msg[i] = np.ravel(np.ones((1, neighbour.vlen)))
            neighbour.edges.append(self)
            neighbour.msg.append(self.msg[i])
            
        for i, edge in enumerate(edges):
            if edge.vlen != self.phi.shape[i]:
                raise ValueError(f"Shape mismatch: {self.name} phi shape and variable vlen do not match.")

    def calcMessage(self, i):
        nPhiDims = len(self.phi.shape)
        axesorder = [i] + listLessOne(list(range(nPhiDims)), i)
        z = np.transpose(self.phi, axes=axesorder)
        index = list(range(len(self.msg) - 1))
        index.reverse()
        othermsg = listLessOne(self.msg, i)
        for j in index:
            y = othermsg[j] * z
            z = np.transpose(np.sum(np.transpose(y), 0))
        return z

    def initialDing(self):
        print('Initial ding from terminal node', self.name, 'to', self.edges[0].name)
        depth = 0
        self.ding(self.edges[0], self.phi, depth)

    def display(self):
        print('--------------------------------------------')
        print(self.name)
        for i in range(len(self.edges)):
            print('intray ', self.edges[i], ' msg:', self.msg[i])
        print('phi is:')
        print(self.phi)


class Observation(Summer):
    def __init__(self, observedNode, obs=None):
        if obs is None:
            obs = np.array([])
        super().__init__('OBS', [observedNode], obs)
        self.initialDing()
        observedNode.observed = True  # just for humans, not used algorithmically

if __name__ == '__main__':
    print('belief_prop.py is a library. Run burglar.py or rain.py to see it in action.')
