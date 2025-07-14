import tsplib95
import math
import time
import matplotlib.pyplot as plt

# Function to load a TSPLIB file, extracting both distance matrix and problem data
def load_tsp_file(filename):
    problem = tsplib95.load(filename)
    cities = list(problem.get_nodes())
    num_cities = len(cities)
    distance_matrix = [[problem.get_weight(cities[i], cities[j]) for j in range(num_cities)] for i in range(num_cities)]
    return problem, cities, distance_matrix

# Function to solve TSP using dynamic programming
def tsp_dynamic_programming(filename):
    begin_time = time.time() #start the timer
    problem, cities, distances = load_tsp_file(filename)

    #Step 1: Initialise the DP table
    n = len(distances)
    dp = [[math.inf] * n for _ in range(1 << n)] 
    parent = [[None] * n for _ in range(1 << n)]

    dp[1][0] = 0 

    #Step 2: Fill the DP table
    for mask in range(1 << n): 
        for last_visited in range(n):
            if not (mask & (1 << last_visited)):
                continue
            for next in range(n):
                if mask & (1 << next):
                    continue
                new_mask = mask | (1 << next)
                new_dist = dp[mask][last_visited] + distances[last_visited][next]
                if new_dist < dp[new_mask][next]:
                    dp[new_mask][next] = new_dist
                    parent[new_mask][next] = last_visited

    #Step 3: Find the minimum cost and reconstruct the path
    min_cost = math.inf
    end_city = None
    full_mask = (1 << n) - 1 
    for last_visited in range(1, n):
        cost = dp[full_mask][last_visited] + distances[last_visited][0]
        if cost < min_cost:
            min_cost = cost
            end_city = last_visited

    #Step 4: Reconstruct the optimal path
    tour = []
    mask = full_mask
    last_visited = end_city
    while last_visited is not None:
        tour.append(cities[last_visited])
        new_last_visited = parent[mask][last_visited]
        mask ^= (1 << last_visited)
        last_visited = new_last_visited

    # Step 5: Reverse the path to get the correct order
    tour = tour[::-1]
    tour.append(cities[0]) 
    
    # Step 6: Return the result and end timer
    end_time = time.time() #end the timer
    return problem, cities, tour, min_cost, begin_time, end_time

# Function to plot the route using matplotlib
def plot_route(cities, route, problem):
    city_coords = problem.node_coords

    route_coords = [city_coords[city] for city in route]
    route_x = [x for x, y in route_coords]
    route_y = [y for x, y in route_coords]

    plt.figure(figsize=(8, 6))
    plt.plot(route_x, route_y, 'r-', marker='o', markersize=5, label="Route")
    
    plt.title("Held Karp Visualisation")
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.grid(False)
    plt.legend()
    plt.show()

# Main execution
if __name__ == "__main__":
    filename = "./tsplib-master/ulysses16.tsp"
    problem, cities, best_path, min_cost, begin_time, end_time = tsp_dynamic_programming(filename) 
    print("Best path:", best_path)
    print("Number of cities:", len(cities))
    print("Total cost:", min_cost)
    print("Execution time:", (end_time - begin_time), "seconds")
    plot_route(cities, best_path, problem)
