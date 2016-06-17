from __future__ import division
# Dijkstra's algorithm for shortest paths
# David Eppstein, UC Irvine, 4 April 2002

# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/117228
# http://code.activestate.com/recipes/119466-dijkstras-algorithm-for-shortest-paths/
from priodict import priorityDictionary

NODE_VISIT_COST = 0.0


def Dijkstra(G, start, end=None):
	"""
	Find shortest paths from the start vertex to all
    vertices nearer than or equal to the end.

    The input graph G is assumed to have the following
    representation: A vertex can be any object that can
    be used as an index into a dictionary.  G is a
    dictionary, indexed by vertices.  For any vertex v,
    G[v] is itself a dictionary, indexed by the neighbors
    of v.  For any edge v->w, G[v][w] is the length of
    the edge.  This is related to the representation in
    <http://www.python.org/doc/essays/graphs.html>
    where Guido van Rossum suggests representing graphs
    as dictionaries mapping vertices to lists of neighbors,
    however dictionaries of edges have many advantages
    over lists: they can store extra information (here,
    the lengths), they support fast existence tests,
    and they allow easy modification of the graph by edge
    insertion and removal.  Such modifications are not
    needed here but are important in other graph algorithms.
    Since dictionaries obey iterator protocol, a graph
    represented as described here could be handed without
    modification to an algorithm using Guido's representation.

    Of course, G and G[v] need not be Python dict objects;
    they can be any other object that obeys dict protocol,
    for instance a wrapper in which vertices are URLs
    and a call to G[v] loads the web page and finds its links.

    The output is a pair (D,P) where D[v] is the distance
    from start to v and P[v] is the predecessor of v along
    the shortest path from s to v.

    Dijkstra's algorithm is only guaranteed to work correctly
    when all edge lengths are positive. This code does not
    verify this property for all edges (only the edges seen
    before the end vertex is reached), but will correctly
    compute shortest paths even for some graphs with negative
    edges, and will raise an exception if it discovers that
    a negative edge has caused it to make a mistake.
    """

    D = {}	# dictionary of final distances
    P = {}	# dictionary of predecessors
    Q = priorityDictionary()   # est.dist. of non-final vert.
    Q[start] = 0

	for v in Q:
		D[v] = Q[v]
		if v == end: break

		for w in G[v]:
			vwLength = D[v] + G[v][w] + NODE_VISIT_COST
			if w in D:
				if vwLength < D[w]:
					raise ValueError, \
  "Dijkstra: found better path to already-final vertex"
			elif w not in Q or vwLength < Q[w]:
				Q[w] = vwLength
				P[w] = v
	return (D,P)

def shortestPath(G,start,end):
	"""
	Find a single shortest path from the given start vertex
	to the given end vertex.
	The input has the same conventions as Dijkstra().
	The output is a list of the vertices in order along
	the shortest path.
	"""
	initial_end = end
	D,P = Dijkstra(G,start,end)
	Path = []
	while 1:
		Path.append(end)
		if end == start: break
		end = P[end]
	Path.reverse()
	return Path, D[initial_end]



"""
from dijkstra import shortestPath

class Station(object):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return 'Station(name=%s)' % (self.name,)

a = Station('a')
b = Station('b')
c = Station('c')
d = Station('d')
e = Station('e')
f = Station('f')
g = Station('g')
h = Station('h')
i = Station('i')
j = Station('j')
k = Station('k')

G = {
 a:{b:5},
 b:{a:5, c:3},
 c:{b:3, d:3},
 d:{c:3, h:10, e:2},
 e:{d:2, f:2, k:10},
 f:{e:2, g:5},
 g:{f:5, i:3},
 h:{d:10, i:1},
 i:{g:3, h:1, j:2},
 j:{i:2},
 k:{e:10},
 }

shortestPath(G, a, j)
"""
