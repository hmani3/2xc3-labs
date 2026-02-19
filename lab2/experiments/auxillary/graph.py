from collections import deque

#Undirected graph using an adjacency list
class Graph:

    def __init__(self, n):
        self.adj = {}
        for i in range(n):
            self.adj[i] = []

    def are_connected(self, node1, node2):
        return node2 in self.adj[node1]

    def adjacent_nodes(self, node):
        return self.adj[node]

    def add_node(self):
        self.adj[len(self.adj)] = []

    def add_edge(self, node1, node2):
        if node1 not in self.adj[node2]:
            self.adj[node1].append(node2)
            self.adj[node2].append(node1)

    # had to fix this, dont know what was intended here
    def number_of_nodes(self):
        return len(self.adj)


#Breadth First Search
def BFS(G, node1, node2):
    Q = deque([node1])
    marked = {node1 : True}
    for node in G.adj:
        if node != node1:
            marked[node] = False
    while len(Q) != 0:
        current_node = Q.popleft()
        for node in G.adj[current_node]:
            if node == node2:
                return True
            if not marked[node]:
                Q.append(node)
                marked[node] = True
    return False


#Depth First Search
def DFS(G, node1, node2):
    S = [node1]
    marked = {}
    for node in G.adj:
        marked[node] = False
    while len(S) != 0:
        current_node = S.pop()
        if not marked[current_node]:
            marked[current_node] = True
            for node in G.adj[current_node]:
                if node == node2:
                    return True
                S.append(node)
    return False

#BFS DFS VARIATIONS FOR QUESTION 1

# BFS2: 1 path
def BFS2(G, node1, node2):
    # check if we are not moving
    if node1 == node2: return [node1]

    Q = deque([node1])
    # track parents so we can remember the path. Also, we dont need visited now
    # since we track visited nodes in the parent, if a node is in the parent, we have visited it before
    parent = {node1 : None}

    while Q:
        current_node = Q.popleft()
        for node in G.adj[current_node]:
            if node == node2:
                # we reached the end, at the parent, track a trace from our current node back to node1 through the parent
                parent[node] = current_node
                trace = [node]
                while node != node1:
                    node = parent[node]
                    trace.append(node)
                trace.reverse()
                return trace
            
            if node not in parent:
                parent[node] = current_node
                Q.append(node)
                
    # we never found our goal, there is no valid path starting at node1 -> node2
    return []

# DFS2: 1 path (copy BFS)
def DFS2(G, node1, node2):
    if node1 == node2: return [node1]

    parent = {node1 : None}
    S = [node1]

    while S:
        current_node = S.pop()
        # use the same logic as our bFs
        for node in G.adj[current_node]:  
            if node == node2:
                parent[node] = current_node
                trace = [node]
                while node != node1:
                    node = parent[node]
                    trace.append(node)
                trace.reverse()
                return trace
            
            if node not in parent:
                parent[node] = current_node
                S.append(node)

    return []

# BFS3: All paths  from node 1
def BFS3(G, node1):
    Q = deque([node1])
    parent = {node1 : None}

    while Q:
        current_node = Q.popleft()
        for node in G.adj[current_node]:
            if node not in parent:
                # update parent only if we are viisitign for the first time
                parent[node] = current_node
                Q.append(node)
                
    # remove first element
    del parent[node1]
    return parent

# DFS3: all paths (copy BFS)
def DFS3(G, node1):

    parent = {}
    # we can track pairs of node : parent in the stack
    S = [(node1, None)]

    while S:
        current_node, parent_node = S.pop()
        # doubles as visite,d and so we only claim the parent when we pop to have proper deptht raversal
        if current_node not in parent:
            parent[current_node] = parent_node
            for node in G.adj[current_node]:
                if node not in parent:
                    S.append((node, current_node))
    
    del parent[node1]
    return parent

# CYCLE DETECTION AND CONNECTIVITY DETECTION IMPLEMENTATIONS

# CYCLE DETECTION
def has_cycle (G):
    # the idea here is that a cycle means we see an already visited node that is not our parent
    # we use dfs (doesnt really matter for what we r using it for)
    visited = set()

    for node in G.adj:
        # if node not visited its our start
        if node not in visited:
            # storing node w its parent
            S = [(node, None)]
            while S:
                current_node, parent_node = S.pop()
                if current_node in visited:
                    # we have a cycle if we see a visited node that is not our parent
                    return True
                else:
                    visited.add(current_node)
                    for neighbor in G.adj[current_node]:
                        if neighbor != parent_node: S.append((neighbor, current_node))
    return False

# CONNECTIVITY DETECTION
def is_connected(G):
    # empty graph is connected
    if not G.adj: return True
    # the idea is that if all nodes are connected, then for any arbitrary root node,
    # we should have all nodes in our parent dict, i.e., our parent dict keys match all the nodes in our graph
    # (subtract 1 since the way we return our BFS3 excludes root)
    start_node = next(iter(G.adj))
    return G.number_of_nodes() - 1 == len(BFS3(G, start_node))


#Use the methods below to determine minimum vertex covers

def add_to_each(sets, element):
    copy = sets.copy()
    for set in copy:
        set.append(element)
    return copy

def power_set(set):
    if set == []:
        return [[]]
    return power_set(set[1:]) + add_to_each(power_set(set[1:]), set[0])

def is_vertex_cover(G, C):
    for start in G.adj:
        for end in G.adj[start]:
            if not(start in C or end in C):
                return False
    return True

def MVC(G):
    # the implementation used get_size (?) doesnt exist replaced it with the probably intended number_of_nodes
    nodes = [i for i in range(G.number_of_nodes())]
    subsets = power_set(nodes)
    min_cover = nodes
    for subset in subsets:
        if is_vertex_cover(G, subset):
            if len(subset) < len(min_cover):
                min_cover = subset
    return min_cover


