from .graph import Graph
from random import randint

# given `nodes` number of nodes, and `edges` number of edges,
# return a random correct graph with given nodes and edges equal to edges or maximum possible edges
def create_random_graph(nodes: int, edges: int) -> Graph:
    g = Graph(nodes)

    max_possible_edges = nodes * (nodes - 1) // 2
    if edges > max_possible_edges:
        print(f"{edges} edges is too many for {nodes} nodes. Capping at {max_possible_edges}")
        edges = max_possible_edges

    current_edges = 0
    while current_edges < edges:
        u, v = randint(0, nodes - 1), randint(0, nodes - 1)
        
        # correct graph: no self loops (u = v), dont repeat edges
        if u != v and not g.are_connected(u, v):
            g.add_edge(u, v)
            current_edges += 1
    return g

# print graph in a visual format for better analysis
def print_graph(g):
    # Check if graph is empty
    if not g.adj:
        print("Graph is empty.")
        return

    print(f"--- Graph Structure (Nodes: {len(g.adj)}) ---")

    # terate through nodes in sorted order (0, 1, 2...)
    # Sorting keys makes the output deterministic and easier to read.
    for node in sorted(g.adj.keys()):
        neighbors = g.adj[node]
        
        # Format the neighbor list
        if not neighbors:
            print(f"  Node {node}: <isolated>")
        else:
            # Convert neighbor IDs to strings and join with commas
            neighbors_str = ", ".join(map(str, sorted(neighbors)))
            print(f"  Node {node} -> [{neighbors_str}]")
