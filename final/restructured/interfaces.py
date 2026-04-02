from abc import ABC, abstractmethod
from typing import List

# --- Graph Interfaces ---
class Graph(ABC):
    @abstractmethod
    def get_adj_nodes(self, node: int) -> List[int]:
        pass

    @abstractmethod
    def add_node(self, node: int):
        pass

    @abstractmethod
    def add_edge(self, start: int, end: int, w: float):
        pass

    @abstractmethod
    def get_num_of_nodes(self) -> int:
        pass
    
    @abstractmethod
    def w(self, node: int) -> float:
        pass

# --- Algorithm Interface ---
class SPAlgorithm(ABC):
    @abstractmethod
    def calc_sp(self, graph: Graph, source: int, dest: int) -> float:
        """
        Calculates the shortest path and returns the total weight/distance as a float.
        """
        pass