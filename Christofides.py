import tsplib95
import networkx as nx
import matplotlib.pyplot as plt
import time

# Load TSPLIB file
def load_tsp_file(filename):
    problem = tsplib95.load(filename)
    cities = list(problem.get_nodes())
    graph = {i: {j: problem.get_weight(i, j) for j in cities} for i in cities}
    G = problem.get_graph()
    return cities, graph, problem, G

# Cost calculation
def calculate_cost(route, graph):
    total_cost = 0
    for i in range(len(route)):
        current = route[i]
        next_city = route[(i + 1) % len(route)]  # wrap around
        total_cost += graph[current][next_city]
    return total_cost

# Christofides Algorithm
def christofides_tsp(G):
    begin_time = time.time()
    # Step 1: Minimum Spanning Tree
    mst = nx.minimum_spanning_tree(G)

    # Step 2: Find odd degree nodes
    odd_nodes = [v for v, d in mst.degree() if d % 2 == 1] 

    # Step 3: Minimum Weight Perfect Matching among odd degree nodes
    subgraph = G.subgraph(odd_nodes)
    matching = nx.algorithms.matching.min_weight_matching(subgraph, maxcardinality=True)

    # Step 4: Combine MST and Matching
    eulerian_graph = nx.MultiGraph(mst)
    eulerian_graph.add_edges_from(matching)

    # Step 5: Find Eulerian Circuit
    euler_circuit = list(nx.eulerian_circuit(eulerian_graph))

    # Step 6: Shortcutting to TSP Tour
    tour = []
    visited = set()
    for u, v in euler_circuit:
        if u not in visited:
            tour.append(u)
            visited.add(u)
    tour.append(tour[0])
    end_time = time.time()
    return tour, begin_time, end_time

# Plotting function
def plot_route(route, problem):
    coords = problem.node_coords
    route_coords = [coords[city] for city in route]
    x_vals = [x for x, y in route_coords]
    y_vals = [y for x, y in route_coords]

    x_vals.append(x_vals[0])
    y_vals.append(y_vals[0])

    plt.plot(x_vals, y_vals, 'r-', marker='o')
    plt.title("Christofides TSP Route")
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.grid(False)
    plt.show()

# Main code
if __name__ == "__main__":
    filename = "./tsplib-master/nrw1379.tsp"  # Change path accordingly
    cities, graph, problem, G = load_tsp_file(filename)
    route, begin_time, end_time = christofides_tsp(G)
    cost = calculate_cost(route, graph)
    print("Best Route:", route)
    print("Number of Cities:", len(set(route)))
    print("Total Cost:", cost)
    print("Execution Time:", round(end_time - begin_time), "seconds")
    plot_route(route, problem)
