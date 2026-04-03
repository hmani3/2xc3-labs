import min_heap
import random
import time
import matplotlib.pyplot as plt
import math 

#--------------------------------------------------------------------------------------------------------------
# the given fuctions and graph class  
class DirectedWeightedGraph:

    def __init__(self):
        self.adj = {}
        self.weights = {}

    def are_connected(self, node1, node2):
        for neighbour in self.adj[node1]:
            if neighbour == node2:
                return True
        return False

    def adjacent_nodes(self, node):
        return self.adj[node]

    def add_node(self, node):
        self.adj[node] = []

    def add_edge(self, node1, node2, weight):
        if node2 not in self.adj[node1]:
            self.adj[node1].append(node2)
        self.weights[(node1, node2)] = weight

    def w(self, node1, node2):
        if self.are_connected(node1, node2):
            return self.weights[(node1, node2)]

    def number_of_nodes(self):
        return len(self.adj)


def dijkstra(G, source):
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())

    #Initialize priority queue/heap and distances
    for node in nodes:
        Q.insert(min_heap.Element(node, float("inf")))
        dist[node] = float("inf")
    Q.decrease_key(source, 0)

    #Meat of the algorithm
    while not Q.is_empty():
        current_element = Q.extract_min()
        current_node = current_element.value
        dist[current_node] = current_element.key
        for neighbour in G.adj[current_node]:
            if dist[current_node] + G.w(current_node, neighbour) < dist[neighbour]:
                Q.decrease_key(neighbour, dist[current_node] + G.w(current_node, neighbour))
                dist[neighbour] = dist[current_node] + G.w(current_node, neighbour)
                pred[neighbour] = current_node
    return dist


def bellman_ford(G, source):
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    nodes = list(G.adj.keys())

    #Initialize distances
    for node in nodes:
        dist[node] = float("inf")
    dist[source] = 0

    #Meat of the algorithm
    for _ in range(G.number_of_nodes()):
        for node in nodes:
            for neighbour in G.adj[node]:
                if dist[neighbour] > dist[node] + G.w(node, neighbour):
                    dist[neighbour] = dist[node] + G.w(node, neighbour)
                    pred[neighbour] = node
    return dist


def total_dist(dist):
    total = 0
    for key in dist.keys():
        total += dist[key]
    return total

def create_random_complete_graph(n,upper):
    G = DirectedWeightedGraph()
    for i in range(n):
        G.add_node(i)
    for i in range(n):
        for j in range(n):
            if i != j:
                G.add_edge(i,j,random.randint(1,upper))
    return G
#--------------------------------------------------------------------------------------------------------------

#Assumes G represents its nodes as integers 0,1,...,(n-1)
def mystery(G):
    n = G.number_of_nodes()
    d = init_d(G)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][j] > d[i][k] + d[k][j]: 
                    d[i][j] = d[i][k] + d[k][j]
    return d

def init_d(G):
    n = G.number_of_nodes()
    d = [[float("inf") for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if G.are_connected(i, j):
                d[i][j] = G.w(i, j)
        d[i][i] = 0
    return d




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


#---------------------------------------------------------------------------------

#Experiment code below


# creates a random directed weighted graph where we can control the density 
def create_random_graph(n, density, upper, seed=None): # n is the number of nodes, density is how likely extra edges are added,upper is the max edge weight, make the randoms graph reproducable
    rng = random.Random(seed) # random number generater using seed, so we can get the same graph later if need be
    G = DirectedWeightedGraph() # generate a empty graph

    for i in range(n):  # add nodes 1 through n to the graph
        G.add_node(i)

    # force reachability from 0 to all nodes
    for i in range(n - 1):
        G.add_edge(i, i + 1, rng.randint(1, upper))

    # add random extra edges, so skipping self loops add a random edge with probaility density, if added give it a random weight from 1 to upper
    for i in range(n):
        for j in range(n):
            if i != j and not G.are_connected(i, j):
                if rng.random() < density:
                    G.add_edge(i, j, rng.randint(1, upper))

    return G


# sums only finite distances
def finite_total_dist(dist):
    total = 0 # 0 as default  
    for value in dist.values():
        if value != float("inf"): # only add finite values
            total += value
    return total


# average runtime for one function call
def measure_runtime(func, G, source, k, repeats=3):
    total_time = 0
    for _ in range(repeats):
        start = time.perf_counter()
        func(G, source, k)
        end = time.perf_counter()  # record the start and end time for each run 
        total_time += (end - start)
    return total_time / repeats # returns the avg runtime to resuce noise


# -------------------------------
# Experiment 1: effect of k
# x-axis: k
# y-axis: average total finite distance
# -------------------------------
def experiment_k():
    ks = [1, 2, 3, 4, 5, 10]  # try several values of k to se how it changes
    n = 20  # number of nodes is 20
    upper = 20 # weights are between 1 and 20
    num_graphs = 5 # avg over 5 random graphs to reduce noise

    dijkstra_totals = []  # store the value for distance from dijkstra approx for each k
    bellman_totals = [] # same thing for bellman ford approx
    exact_totals = [] # total distance from exact dijkstra, to see how close the approximations are to the true value for each k

    for k in ks:
        d_total_sum = 0  # sum for avg start at 0
        b_total_sum = 0
        exact_total_sum = 0
# loop for all graphs
        for g in range(num_graphs):
            random.seed(1000 + g)
            G = create_random_complete_graph(n, upper)
# run the algorithms    
            exact_dist = dijkstra(G, 0)
            d_dist = dijkstra_approx(G, 0, k)
            b_dist = bellman_ford_approx(G, 0, k)
# convert to to one number
            exact_total_sum += finite_total_dist(exact_dist)
            d_total_sum += finite_total_dist(d_dist)
            b_total_sum += finite_total_dist(b_dist)
#avg over the graphs
        exact_totals.append(exact_total_sum / num_graphs)
        dijkstra_totals.append(d_total_sum / num_graphs)
        bellman_totals.append(b_total_sum / num_graphs)
# plot the results
    plt.figure(figsize=(8, 5))
    plt.plot(ks, dijkstra_totals, marker="o", label="Dijkstra Approx")
    plt.plot(ks, bellman_totals, marker="s", label="Bellman-Ford Approx")
    plt.plot(ks, exact_totals, linestyle="--", marker="^", label="Exact Dijkstra")
    plt.xlabel("k (max relaxations per node)")
    plt.ylabel("Average total finite distance")
    plt.title("Experiment 1: Effect of k on Approximation Quality")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("experiment1_k_effect.png", dpi=300)
    plt.show()


# -------------------------------
# Experiment 2: effect of graph size
# x-axis: number of nodes
# y-axis: average runtime
# -------------------------------
def experiment_graph_size():
    sizes = [10, 20, 40, 60, 80] # sizes we will test
    density = 0.3  # density is 0.3 
    upper = 20  # max weight is 20
    k = 3  # number of relaxations
    num_graphs = 3 # number of graphs to avg over for each size 

    dijkstra_times = [] # runtime for this
    bellman_times = [] # runtime for this
    # for the different sizes 
    for n in sizes:
        d_time_sum = 0
        b_time_sum = 0

        for g in range(num_graphs):
            G = create_random_graph(n, density, upper, seed=2000 + 100 * n + g)
            # time both approzimate algorithms 
            d_time_sum += measure_runtime(dijkstra_approx, G, 0, k)
            b_time_sum += measure_runtime(bellman_ford_approx, G, 0, k)

        dijkstra_times.append(d_time_sum / num_graphs)
        bellman_times.append(b_time_sum / num_graphs)
    # plot the results
    plt.figure(figsize=(8, 5))
    plt.plot(sizes, dijkstra_times, marker="o", label="Dijkstra Approx")
    plt.plot(sizes, bellman_times, marker="s", label="Bellman-Ford Approx")
    plt.xlabel("Number of nodes")
    plt.ylabel("Average runtime (seconds)")
    plt.title("Experiment 2: Effect of Graph Size on Runtime")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("experiment2_graph_size.png", dpi=300)
    plt.show()


# -------------------------------
# Experiment 3: effect of graph density
# x-axis: density
# y-axis: average runtime
# -------------------------------
def experiment_graph_density():
    densities = [0.1, 0.2, 0.4, 0.6, 0.8] # again densities we will test
    n = 60 # nodes
    upper = 20 # max weight
    k = 3 # relaxations
    num_graphs = 3 # number of graphs to avg over for each density
    
    # results store like before
    dijkstra_times = []
    bellman_times = []
 
    # try for each density
    for density in densities:
        d_time_sum = 0
        b_time_sum = 0

        # measue how the runtime changes with more dense graphs and avg them out over several random graphs for each density to reduce noise
        for g in range(num_graphs):
            G = create_random_graph(n, density, upper, seed=3000 + 100 * g + int(density * 100))

            d_time_sum += measure_runtime(dijkstra_approx, G, 0, k)
            b_time_sum += measure_runtime(bellman_ford_approx, G, 0, k)

        dijkstra_times.append(d_time_sum / num_graphs)
        bellman_times.append(b_time_sum / num_graphs)
# plot the results 
    plt.figure(figsize=(8, 5))
    plt.plot(densities, dijkstra_times, marker="o", label="Dijkstra Approx")
    plt.plot(densities, bellman_times, marker="s", label="Bellman-Ford Approx")
    plt.xlabel("Graph density")
    plt.ylabel("Average runtime (seconds)")
    plt.title("Experiment 3: Effect of Graph Density on Runtime")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("experiment3_graph_density.png", dpi=300)
    plt.show()


# run all three experiments
experiment_k()
experiment_graph_size()
experiment_graph_density()

#-------------------------------------------------------------------------------
# this is the mystery function experiment

# -------------------------------
# Mystery algorithm tests
# -------------------------------


# this just runs dijkstra for every source node
def all_pairs_dijkstra(G):
    n = G.number_of_nodes()
    matrix = []
    for source in range(n):
        dist = dijkstra(G, source)
        row = []
        for j in range(n):
            row.append(dist[j])
        matrix.append(row)
    return matrix

# this just runs Bellman-Ford for every source node
def all_pairs_bellman_ford(G):
    n = G.number_of_nodes()
    matrix = []
    for source in range(n):
        dist = bellman_ford(G, source)
        row = []
        for j in range(n):
            row.append(dist[j])
        matrix.append(row)
    return matrix

# returns boolean true or false
def matrices_equal(A, B):
    return A == B

# We build a small graph with only positive weights
def build_mystery_positive_graph():
    G = DirectedWeightedGraph()
    for i in range(4):
        G.add_node(i)

    G.add_edge(0, 1, 3)
    G.add_edge(0, 2, 10)
    G.add_edge(1, 2, 2)
    G.add_edge(1, 3, 7)
    G.add_edge(2, 3, 1)

    return G

#build a small graph with negative weights
def build_mystery_negative_graph():
    G = DirectedWeightedGraph()
    for i in range(4):
        G.add_node(i)

    G.add_edge(0, 1, 4)
    G.add_edge(0, 2, 8)
    G.add_edge(1, 2, -2)
    G.add_edge(1, 3, 6)
    G.add_edge(2, 3, 3)

    return G

# check for 2 things: compute the mystery positive then the Disjstra and compare them
def test_mystery_correctness():
    G_pos = build_mystery_positive_graph()
    mystery_pos = mystery(G_pos)
    dijkstra_pos = all_pairs_dijkstra(G_pos)
    # if they match then myster() computes all the pairs hosrtest path on postive graphs
    print("Mystery matches repeated Dijkstra on positive graph:",
          matrices_equal(mystery_pos, dijkstra_pos))
    # we do the same thing for the negative bellman ford
    G_neg = build_mystery_negative_graph()
    mystery_neg = mystery(G_neg)
    bellman_neg = all_pairs_bellman_ford(G_neg)
    # if they match then myster() computes all the pairs hosrtest path on negative graphs
    print("Mystery matches repeated Bellman-Ford on negative-edge graph:",
          matrices_equal(mystery_neg, bellman_neg))


# how long does myster(G) takes on average, repeated to clear out some of the noise
def measure_mystery_runtime(G, repeats=3):
    total_time = 0
    for _ in range(repeats):
        start = time.perf_counter()
        mystery(G)
        end = time.perf_counter()
        total_time += (end - start)
    return total_time / repeats

# test on different sizes 
def experiment_mystery_runtime():
    sizes = [10, 20, 30, 40, 50, 60, 80, 100]
    upper = 20
    runtimes = []

    for n in sizes:
        random.seed(7000 + n)
        G = create_random_complete_graph(n, upper)
        t = measure_mystery_runtime(G, repeats=3)
        runtimes.append(t)

    print("sizes =", sizes)
    print("times =", runtimes)

    # make a reference line proportional to n^3
    # choose c so the reference line lines up roughly with the first data point
    c = runtimes[0] / (sizes[0] ** 3)
    cubic_ref = [c * (n ** 3) for n in sizes]
# plot the data
    plt.figure(figsize=(8, 5))
    plt.loglog(sizes, runtimes, marker="o", label="Measured runtime")
    plt.loglog(sizes, cubic_ref, linestyle="--", label="Reference line ~ n^3")

    plt.xlabel("Number of nodes (log scale)")
    plt.ylabel("Average runtime (log scale)")
    plt.title("Mystery Algorithm Log-Log Runtime Plot")
    plt.grid(True, which="both")
    plt.legend()
    plt.tight_layout()
    plt.savefig("mystery_loglog.png", dpi=300)
    plt.show()

test_mystery_correctness()
experiment_mystery_runtime()