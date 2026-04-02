from . import min_heap

def dijkstra(G, s, d):
    """ MODIFIED Dijkstra implementation from final_project_part1.py, to match the logic of our a_star algo """
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())

    #Initialize priority queue/heap and distances
    for node in nodes:
        Q.insert(min_heap.Element(node, float("inf")))
        dist[node] = float("inf")

    Q.decrease_key(s, 0)
    dist[s]= 0

    nodes_explored = 0

    #Meat of the algorithm
    while not Q.is_empty():
        current_element = Q.extract_min()
        current_node = current_element.value

        nodes_explored += 1


        if current_node == d: break

        dist[current_node] = current_element.key
        for neighbour in G.adj[current_node]:
            if dist[current_node] + G.w(current_node, neighbour) < dist[neighbour]:
                Q.decrease_key(neighbour, dist[current_node] + G.w(current_node, neighbour))
                dist[neighbour] = dist[current_node] + G.w(current_node, neighbour)
                pred[neighbour] = current_node

    path = []
    if d in pred or s == d:
        cur = d
        while cur is not None:
            path.append(cur)
            cur = pred.get(cur)
        path.reverse()

    # NEW: Return the 3-tuple needed for the test suite
    return (pred, path, nodes_explored)