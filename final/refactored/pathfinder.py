from .interfaces import Graph, SPAlgorithm

class ShortPathFinder:
    def __init__(self):
        # aggregation. 
        # HAS a graph and HAS an algorithm.
        self.graph = None
        self.algorithm = None

    def set_graph(self, graph: Graph):
        self.graph = graph

    def set_algorithm(self, algorithm: SPAlgorithm):
        self.algorithm = algorithm

    def calc_short_path(self, source: int, dest: int) -> float:
        if self.graph is None or self.algorithm is None:
            raise ValueError("Both graph and algorithm must be set before calculating path.")
            
        # Delegate the calculation to whichever strategy is currently loaded
        return self.algorithm.calc_sp(self.graph, source, dest)