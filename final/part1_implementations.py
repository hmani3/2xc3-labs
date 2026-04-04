import implementations.min_heap as min_heap
#----------------------------------------------------------------------------------------------

# the aprox versions with bounded k
# Dijkstra and Bellman-Ford with k relaxations   

def dijkstra_approx(G, source, k):
    pred = {}  # Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {}  # Distance dictionary
    relax_count = {}  # Tracks how many times each node has been relaxed
    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())

    # Initialize priority queue/heap, distances, and relaxation counts
    for node in nodes:
        Q.insert(min_heap.Element(node, float("inf")))
        dist[node] = float("inf")
        relax_count[node] = 0 # every node starts with 0 relaxations consumed
    Q.decrease_key(source, 0)
    dist[source] = 0  # just saying that source is 0 distance from itself

    # Meat of the algorithm
    while not Q.is_empty():
        current_element = Q.extract_min()
        current_node = current_element.value
        dist[current_node] = current_element.key
        for neighbour in G.adj[current_node]:
            if neighbour in Q.map and dist[current_node] + G.w(current_node, neighbour) < dist[neighbour] and relax_count[neighbour] < k:   # updated with relax constraints
                Q.decrease_key(neighbour, dist[current_node] + G.w(current_node, neighbour))
                dist[neighbour] = dist[current_node] + G.w(current_node, neighbour)
                pred[neighbour] = current_node
                relax_count[neighbour] += 1 # update the relax count
    return dist


def bellman_ford_approx(G, source, k):
    pred = {}  # Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {}  # Distance dictionary
    relax_count = {}  # Tracks how many times each node has been relaxed
    nodes = list(G.adj.keys())

    # Initialize distances and relaxation counts
    for node in nodes:
        dist[node] = float("inf")
        relax_count[node] = 0 # every node starts with 0 relaxations consumed
    dist[source] = 0 # just saying that source is 0 distance from itself

    # Meat of the algorithm
    for _ in range(G.number_of_nodes()):
        for node in nodes:
            for neighbour in G.adj[node]:
                if dist[node] != float("inf") and dist[neighbour] > dist[node] + G.w(node, neighbour) and relax_count[neighbour] < k: # updated relaxation constraints
                    dist[neighbour] = dist[node] + G.w(node, neighbour)
                    pred[neighbour] = node
                    relax_count[neighbour] += 1 # update the relax count
    return dist
