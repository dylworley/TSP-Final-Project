import numpy as np
import random
import tsplib95
import itertools
import matplotlib.pyplot as plt
import time



# Set seed for reproducibility
np.random.seed(42)
random.seed(42)


# Function to load a TSPLIB file and extract cities and distances
def load_tsp_file(filename):
    problem = tsplib95.load(filename)
    cities = list(problem.get_nodes())
    graph = {i: {j: problem.get_weight(i, j) for j in cities} for i in cities}
    G = problem.get_graph()
    return cities, graph, problem

def calculate_cost(route, graph): 
    total_cost = 0
    n = len(route)
    for i in range(n):
        current_city = route[i]
        next_city = route[(i + 1) % n]  # Wrap around to the start of the route
        total_cost += graph[current_city][next_city]
    return total_cost


# Function to create a random initial route
def create_initial_route(cities):
    return random.sample(list(cities), len(cities))

# Function to create neighboring solutions
def get_neighbors(route):
    neighbors = []
    for i in range(len(route)):
        for j in range(i + 1, len(route)): 
            neighbor = route.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors

#hill climbing function
def hill_climbing(cities, graph):
    begin_time = time.time()
    current_route = create_initial_route(cities)
    current_distance = calculate_cost(current_route, graph)

    while True:
        neighbors = get_neighbors(current_route)
        next_route = min(neighbors, key= lambda x: calculate_cost(x,graph)) # lamb
        next_distance = calculate_cost(next_route, graph)
        
        if next_distance >= current_distance:
            break
        
        current_route, current_distance = next_route, next_distance
    end_time = time.time()
    return current_route, current_distance, begin_time, end_time



# Function to plot the route using matplotlib
def plot_route(cities, route, problem):
    # Get the coordinates of the cities from the problem
    city_coords = problem.node_coords

    # Plot the route
    route_coords = [city_coords[city] for city in route]
    route_x = [x for x, y in route_coords]
    route_y = [y for x, y in route_coords]
    
    # Add the return to the starting city to complete the loop
    route_x.append(route_x[0])
    route_y.append(route_y[0])

    plt.plot(route_x, route_y, 'r-', marker='o', markersize=5, label="Route")
    plt.title("Hill Climbing Visualisation")
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.grid(False)
    plt.legend()
    plt.show()


# Main Code
if __name__ == "__main__":
    filename = "./tsplib-master/gr202.tsp"  # Replace with your TSP file path
    cities, graph, problem = load_tsp_file(filename)
    best_route, best_distance, begin_time, end_time = hill_climbing(cities, graph)
    print("Best Route: ", best_route)
    print("Total Cost: ", best_distance)
    print("Execution Time: ", ((end_time - begin_time)))
    # Plot the best route
    plot_route(cities, best_route, problem)