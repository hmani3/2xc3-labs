from .interfaces import SPAlgorithm, Graph
from .graphs import HeuristicGraph
from . import min_heap

class Dijkstra(SPAlgorithm):
    def calc_sp(self, graph: Graph, source: int, dest: int) -> float:
        """ Standard Dijkstra implementation """
        pred = {} 
        dist = {} 
        Q = min_heap.MinHeap([])
    
        nodes = list(graph.adj.keys())

        # Initialize priority queue/heap and distances
        for node in nodes:
            Q.insert(min_heap.Element(node, float("inf")))
            dist[node] = float("inf")

        Q.decrease_key(source, 0)
        dist[source] = 0


        # Meat of the algorithm
        while not Q.is_empty():
            current_element = Q.extract_min()
            current_node = current_element.value

            if current_node == dest: 
                break

            for neighbour in graph.get_adj_nodes(current_node):
                weight = graph.w(current_node, neighbour)
                if dist[current_node] + weight < dist[neighbour]:
                    Q.decrease_key(neighbour, dist[current_node] + weight)
                    dist[neighbour] = dist[current_node] + weight
                    pred[neighbour] = current_node

        # Returning the specific float distance, the path, and the node count
        return dist[dest]
    

class A_Star(SPAlgorithm):
    def calc_sp(self, graph: Graph, source: int, dest: int) -> float:
        """ A* algorithm acting as an adapter for HeuristicGraph. """
        
        if not isinstance(graph, HeuristicGraph):
            raise TypeError("A_Star requires a HeuristicGraph to access the spatial heuristic.")
            
        # Extract the heuristic dictionary from the graph
        h = graph.get_heuristic()
        
        pred = {} 
        dist = {} 
        Q = min_heap.MinHeap([])
        nodes = list(graph.adj.keys())

        for node in nodes:
            Q.insert(min_heap.Element(node, float("inf")))
            dist[node] = float("inf")

        # Update start node by heuristic (Priority is G-score + H-score)
        Q.decrease_key(source, h.get(source, 0))
        dist[source] = 0


        while not Q.is_empty():
            current_element = Q.extract_min()
            current_node = current_element.value

            if current_node == dest: 
                break

            for neighbour in graph.get_adj_nodes(current_node):
                weight = graph.w(current_node, neighbour)
                # dist tracks the actual travel time (G-score)
                if dist[current_node] + weight < dist[neighbour]:
                    dist[neighbour] = dist[current_node] + weight
                    
                    # Q tracks G-score + Heuristic (F-score)
                    f_score = dist[neighbour] + h.get(neighbour, 0)
                    Q.decrease_key(neighbour, f_score)
                    
                    pred[neighbour] = current_node

        return dist[dest]
    

class Bellman_Ford(SPAlgorithm):
    def calc_sp(self, graph: Graph, source: int, dest: int) -> float:
        """ Bellman-Ford shortest path algorithm. """
        pred = {} 
        dist = {} 
        nodes = list(graph.adj.keys())

        for node in nodes:
            dist[node] = float("inf")
        dist[source] = 0

        # Bellman-Ford loops V-1 times
        for _ in range(graph.get_num_of_nodes() - 1):
            for node in nodes:
                
                for neighbour in graph.get_adj_nodes(node):
                    weight = graph.w(node, neighbour)
                    if dist[node] + weight < dist[neighbour]:
                        dist[neighbour] = dist[node] + weight
                        pred[neighbour] = node


        return dist[dest]