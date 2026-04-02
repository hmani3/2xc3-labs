from interfaces import Graph
from typing import Dict, List, Tuple

class DirectedWeightedGraph(Graph):

    def __init__(self) -> None:
        # adj maps an integer (node) to a list of integers (neighboring nodes)
        self.adj: Dict[int, List[int]] = {}
        
        # weights maps a tuple of two integers (node1, node2) to a float (weight)
        self.weights: Dict[Tuple[int, int], float] = {}

    def are_connected(self, node1: int, node2: int) -> bool:
        for neighbour in self.adj[node1]:
            if neighbour == node2: return True
        return False

    def get_adj_nodes(self, node: int) -> List[int]:
        return self.adj[node]

    def add_node(self, node: int) -> None:
        self.adj[node] = []

    def add_edge(self, node1: int, node2: int, weight: float) -> None:
        if node2 not in self.adj[node1]:
            self.adj[node1].append(node2)
        self.weights[(node1, node2)] = weight

    def get_num_of_nodes(self) -> int:
        return len(self.adj)

    def w(self, node1: int, node2: int) -> float:
        if self.are_connected(node1, node2): return self.weights[(node1, node2)]
        return float('inf')  # return inf instead of a none case

    
class HeuristicGraph(DirectedWeightedGraph):
    def __init__(self):
        super().__init__()
        self._heuristic: Dict[int,float] = {}

    def get_heuristic(self) -> Dict[int, float]: return self._heuristic

    def set_heuristic(self, heuristic_dict: Dict[int, float]) -> Dict[int, float]: self._heuristic = heuristic_dict
