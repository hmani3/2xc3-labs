from . import min_heap

def a_star(G, s, d, h):
    """ A* algorithm for finding the shortest distance between start node s, to destination node d on graph G. h is the heuristic function
        as a dict, such that h[u] = estimated theoretical fastest way to reach s from u """
    
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())

    #Initialize priority queue/heap and distances
    for node in nodes:
        Q.insert(min_heap.Element(node, float("inf")))
        dist[node] = float("inf")

    # update start node by heuristic
    Q.decrease_key(s, h[s])
    dist[s] = 0


    nodes_explored = 0
    #Meat of the algorithm
    while not Q.is_empty():
        current_element = Q.extract_min()
        current_node = current_element.value
        nodes_explored += 1

        # if we reach d early exit
        if current_node == d: break

        for neighbour in G.adj[current_node]:
            if dist[current_node] + G.w(current_node, neighbour) < dist[neighbour]:

                # add heuristic prediction for reaching, where we now update the dist
                Q.decrease_key(neighbour, dist[current_node] + G.w(current_node, neighbour) + h[neighbour])
                dist[neighbour] = dist[current_node] + G.w(current_node, neighbour)
                pred[neighbour] = current_node

    # build the path backwards then reverse, the best path from s to d
    path = []
    if d in pred or s == d:
        cur = d
        while cur is not None:
            path.append(cur)
            cur = pred.get(cur)
        path.reverse()
        

    return (pred, path, nodes_explored)