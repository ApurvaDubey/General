'''
Naive implementation of Kruskal's MST algorithm
Run time O(m x n)

@author: Apurva Dubey
'''

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

mst = {}
arrEdges = []
arrNodes = {}

    
class edgeClass():
    def __init__(self,node1,node2,length):
        self.edge = (node1,node2)
        self.length = length

    def show(self):
        return [self.edge,self.length]

for e in sorted(edges, key = lambda tup:-1*tup[2]):
    arrEdges.append(edgeClass(e[0],e[1],e[2]))

for i,n in enumerate(nodes):
    arrNodes[n] = n


while len(arrEdges) > 0:
    
    e = arrEdges.pop()
    
    if arrNodes[e.show()[0][0]] <> arrNodes[e.show()[0][1]]:
        
        mst[tuple(e.show())] = 1
        oldParent = arrNodes[e.show()[0][1]]
        newParent = arrNodes[e.show()[0][0]]

        for k,v in arrNodes.items():
            if v == oldParent:
                arrNodes[k] = newParent

print mst



