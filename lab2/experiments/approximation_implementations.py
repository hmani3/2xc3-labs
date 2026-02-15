from auxillary.graph import * 
from auxillary.helper import *
from random import choice
# create deep copies of graph
from copy import deepcopy

# implementation 1
def approx1(G: Graph) -> Graph:
    C = set()
    new_g = deepcopy(G)
    # we r done once all edges are 
    while new_g.adj:
        max_degree, max_node = -1, 0
        # find node with largest deg
        for u in new_g.adj:
            deg = len(new_g.adj[u])
            if deg > max_degree: max_degree, max_node = deg, u
        # if the best we can do is 0 connections all edges have been remoed
        if max_degree == 0: break
        # now remove the node from the graph by checking neighbours
        for v in new_g.adj[max_node]: new_g.adj[v].remove(max_node)
        # delete node after
        del new_g.adj[max_node]
        C.add(max_node)

    # once we r out of edges we r done, since our leftover edges are the non-conected edges
    return C

# implementation 2
def approx2(G: Graph) -> Graph:
    C = set()
    while not is_vertex_cover(G, C):
        # calculate availble nodesfrom python set subtraction and choose random
        available = set(G.adj.keys()) - C
        u = choice(list(available))
        # add the random to our set and remove from graph
        C.add(u)
    return C

# implementation 3
def approx3(G: Graph) -> Graph:
    C = set()
    new_g = deepcopy(G)
    while new_g.adj:
        # find nodes that have edges
        nodes_with_edges = [node for node, neighbors in new_g.adj.items() if neighbors]
        # if none we done
        if not nodes_with_edges: break

        u = choice(nodes_with_edges)
        v = choice(new_g.adj[u])

        C.add(u)
        C.add(v)

        for n in new_g.adj[u]: new_g.adj[n].remove(u)
        del new_g.adj[u]
        
        for n in new_g.adj[v]: new_g.adj[n].remove(v)
        del new_g.adj[v]
    return C
