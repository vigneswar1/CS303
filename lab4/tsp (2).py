import random

def objective_function(graph, tour):
    cost = 0
    for i in range(len(tour)):
        start = tour[i]
        end = tour[(i + 1) % len(tour)]
        if graph[start][end] == 0:
            return float('inf')
        cost += graph[start][end]
    return cost

def best_neighbor(graph, tour):
    current_cost = objective_function(graph, tour)
    best_tour = None
    for i in range(len(tour)):
        for j in range(i + 1, len(tour)):
            neighbor = tour[:]
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbor_cost = objective_function(graph, neighbor)
            if neighbor_cost < current_cost:
                current_cost = neighbor_cost
                best_tour = neighbor

    return best_tour, current_cost
    
def random_TSP(graph, max_restarts):
    n = len(graph)
    best_cost = float('inf')
    best_path = []

    for restart in range(max_restarts):
        current_tour = list(range(n))
        random.shuffle(current_tour)
        current_cost = objective_function(graph, current_tour)
        while current_cost != float('inf'):
            neighbor, neighbor_cost = best_neighbor(graph, current_tour)
            if neighbor is None or neighbor_cost >= current_cost:
            	break
            current_tour = neighbor
            current_cost = neighbor_cost
        if current_cost < best_cost:
            best_cost = current_cost
            best_path = current_tour
    if best_path:
        print(f"Number of restarts: {max_restarts}")
        print(f"Best path found: {best_path}")
        print(f"Best tour cost: {best_cost}")
    else:
        print("No valid tour found")

# Example usage
nodes = 8
graph = [[0]*nodes for _ in range(nodes)]
for i in range(nodes):
    for j in range(i+1, nodes):
        weight = random.randint(1, 100)
        graph[i][j] = weight
        graph[j][i] = weight
random_TSP(graph, max_restarts=10)

