import numpy as np
import tsplib95
import matplotlib.pyplot as plt
import time


# Load TSPLIB file using tsplib95
def load_tsp_file(filename):
    problem = tsplib95.load(filename)
    cities = list(problem.get_nodes())
    adj_matrix = np.array([[problem.get_weight(i, j) for j in cities] for i in cities]) # an adjacency matrix is a dis
    return adj_matrix, cities, problem

# Branch and Bound Functions
def first_min(adj, i): #finds the first minimum edge distance from i to any other node
    min_val = np.inf
    for k in range(len(adj)):
        if adj[i][k] < min_val and i != k:
            min_val = adj[i][k]
    return min_val

def second_min(adj, i): #finds the second minimum edge distance from i to any other node
    first, second = np.inf, np.inf
    for j in range(len(adj)):
        if i == j:
            continue
        if adj[i][j] <= first:
            second = first
            first = adj[i][j]
        elif adj[i][j] <= second:
            second = adj[i][j]
    return second

def tsp_rec(adj, current_bound, current_weight, level, current_path, visited, final_res, final_path): #recursive function to solve by pruning branches
    N = len(adj) 

    if level == N:
        if adj[current_path[level - 1]][current_path[0]] != 0:
            current_res = current_weight + adj[current_path[level - 1]][current_path[0]]
            if current_res < final_res[0]:
                final_path[:N + 1] = current_path[:]
                final_path[N] = current_path[0]
                final_res[0] = current_res
        return

    for i in range(N):
        if adj[current_path[level-1]][i] != 0 and not visited[i]:
            temp = current_bound
            current_weight += adj[current_path[level - 1]][i]

            if level == 1:
                current_bound -= (first_min(adj, current_path[level - 1]) + first_min(adj, i)) / 2
            else:
                current_bound -= (second_min(adj, current_path[level - 1]) + first_min(adj, i)) / 2

            if current_bound + current_weight < final_res[0]:
                current_path[level] = i
                visited[i] = True

                tsp_rec(adj, current_bound, current_weight, level + 1, current_path, visited, final_res, final_path)

            current_weight -= adj[current_path[level - 1]][i]
            current_bound = temp

            visited = [False] * N
            for j in range(level):
                if current_path[j] != -1:
                    visited[current_path[j]] = True

# Main TSP solver using Branch and Bound
def solve_tsp_branch_bound(adj):
    begin_time = time.time() #start the timer
    N = len(adj)
    current_bound = 0
    current_path = [-1] * (N + 1)
    visited = [False] * N

    final_res = [np.inf]
    final_path = [-1] * (N + 1)

    for i in range(N):
        current_bound += (first_min(adj, i) + second_min(adj, i))

    current_bound = np.ceil(current_bound / 2)

    visited[0] = True
    current_path[0] = 0

    tsp_rec(adj, current_bound, 0, 1, current_path, visited, final_res, final_path)
    end_time = time.time() #end the timer
    return final_res[0], final_path, begin_time, end_time

# Plotting the solution using matplotlib
# Function to plot the route using matplotlib
def plot_route(cities, route, problem):
    # Get the coordinates of the cities from the problem
    city_coords = problem.node_coords

    # Plot cities as red dots
    #plt.figure(figsize=(10, 8))
    #for city, (x, y) in city_coords.items():
        #plt.scatter(x, y, color='red', zorder=5)
        #plt.text(x + 20, y + 20, str(city), fontsize=12, color='black')

    # Plot the route
    route_coords = [city_coords[cities[city]] for city in route]

    route_x = [x for x, y in route_coords]
    route_y = [y for x, y in route_coords]
    
    # Add the return to the starting city to complete the loop
    route_x.append(route_x[0])
    route_y.append(route_y[0])
    
    plt.plot(route_x, route_y, 'r-', marker='o', markersize=5, label="Route")
    plt.title("Branch and Bound Visualisation")
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.grid(False)
    plt.legend()
    plt.show()

# Example usage
if __name__ == "__main__":
    filename = "./tsplib-master/ulysses16.tsp"  # Replace with your TSP file path 
    adj_matrix, cities, problem = load_tsp_file(filename)
    best_cost, best_route, begin_time, end_time = solve_tsp_branch_bound(adj_matrix)
    print("Total Cost:", best_cost)
    print("Number of Cities:", len(best_route))
    print("Optimal Path:", [cities[i] for i in best_route])
    print("Execution Time:", end_time - begin_time)
    plot_route(cities, best_route, problem)
