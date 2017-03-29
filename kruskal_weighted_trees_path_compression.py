'''
Advanced implementation of Kruskal's MST algorithm
using quick union with path compression
Run time O(m x log(n))

@author: Apurva Dubey
'''

"""
"""
INF = 10**10
nodes = ['a','b','c','d','e','f','g']

edges = [
    ('a','b',7),
    ('a','d',5),
    ('b','c',8),
    ('b','d',9),
    ('b','e',7),
    ('c','e',5),
    ('d','e',15),
    ('d','f',6),
    ('e','f',8),
    ('e','g',9),
    ('f','g',11)
    ]

mst = {} # empty MST

class UnionFind:
    """Weighted quick-union with path compression.
    The original Java implementation is introduced at
    https://www.cs.princeton.edu/~rs/AlgsDS07/01UnionFind.pdf
    """

    def __init__(self, nodeList):
        self._id = {i:i for i in nodeList}
        self._sz = {i:1 for i in nodeList}

    def _root(self, i):
        '''Keep rolling up till parent = child'''
        tmp = i
        while (tmp != self._id[tmp]):
            self._id[tmp] = self._id[self._id[tmp]]
            tmp = self._id[tmp]
        return tmp

    def find(self, p, q):
        return self._root(p) == self._root(q)
    
    def union(self, p, q):
        i = self._root(p)
        j = self._root(q)
        if i == j:
            return
        if (self._sz[i] < self._sz[j]):
            self._id[i] = j
            self._sz[j] += self._sz[i]
        else:
            self._id[j] = i
            self._sz[i] += self._sz[j]


class edgeClass():
    '''Edge data structure'''
    def __init__(self,node1,node2,length):
        self.edge = (node1,node2)
        self.length = length

    def show(self):
        return [self.edge,self.length]


# define a UF data structure
uf = UnionFind(['a','b','c','d','e','f','g'])

# sort the edges by length
for e in sorted(edges, key = lambda tup:-1*tup[2]):
    arrEdges.append(edgeClass(e[0],e[1],e[2]))

# pop the edges: small --> large   
while len(arrEdges) > 0:
    
    e = arrEdges.pop()

    # if the node of the edges are not in the same set
    # then put that edge in MST else move on
    if uf.find(e.show()[0][0],e.show()[0][1]) == False:
        mst[tuple(e.show())] = 1
        uf.union(e.show()[0][0],e.show()[0][1])

print mst



