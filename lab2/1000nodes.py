import random
import time
import heapq
from collections import deque

# -------------------- Graph Generation --------------------
def generate_weighted_graph(n, edge_prob=0.01, max_weight=10):
    graph = {i: [] for i in range(n)}
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < edge_prob:
                w = random.randint(1, max_weight)
                graph[u].append((v, w))
                graph[v].append((u, w))
    return graph
    
def is_connected(graph):
    visited = set()
    def dfs(node):
        visited.add(node)
        for neighbor, _ in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
    dfs(0)
    return len(visited) == len(graph)

def generate_connected_graph(n, edge_prob=0.01, max_weight=10):
    while True:
        g = generate_weighted_graph(n, edge_prob, max_weight)
        if is_connected(g):
            return g

# -------------------- DFS --------------------
def dfs(graph, start, goal):
    stack = [(start, [start], 0)]
    visited = set()
    while stack:
        node, path, cost = stack.pop()
        if node == goal:
            return path, cost, len(visited)
        if node not in visited:
            visited.add(node)
            for neighbor, w in graph[node]:
                stack.append((neighbor, path + [neighbor], cost + w))
    return None, float("inf"), len(visited)

# -------------------- BFS --------------------
def bfs(graph, start, goal):
    queue = deque([(start, [start], 0)])
    visited = set([start])
    while queue:
        node, path, cost = queue.popleft()
        if node == goal:
            return path, cost, len(visited)
        for neighbor, w in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor], cost + w))
    return None, float("inf"), len(visited)

# -------------------- UCS --------------------
def ucs(graph, start, goal):
    pq = [(0, start, [start])]
    visited = set()
    while pq:
        cost, node, path = heapq.heappop(pq)
        if node == goal:
            return path, cost, len(visited)
        if node not in visited:
            visited.add(node)
            for neighbor, w in graph[node]:
                heapq.heappush(pq, (cost + w, neighbor, path + [neighbor]))
    return None, float("inf"), len(visited)

# -------------------- IDS --------------------
def dls(graph, start, goal, limit):
    stack = [(start, [start], 0)]
    visited = set()
    while stack:
        node, path, cost = stack.pop()
        if node == goal:
            return path, cost, len(visited)
        if len(path) - 1 < limit:
            visited.add(node)
            for neighbor, w in graph[node]:
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor], cost + w))
    return None, None, len(visited)

def ids(graph, start, goal, max_depth=50):
    total_visited = 0
    for depth in range(max_depth):
        path, cost, visited = dls(graph, start, goal, depth)
        total_visited += visited
        if path:
            return path, cost, total_visited
    return None, None, total_visited

# -------------------- Experiment --------------------
def run_experiment(n, trials):
    graph = generate_connected_graph(n, edge_prob=0.01)
    algorithm = [("DFS", dfs), ("BFS", bfs), ("UCS", ucs), ("IDS", ids)]

    print("Algorithm | Avg Visited | Avg Time (s) | Avg Cost")
    print("-----------------------------------------------")

    for name, algo in algorithm:
        total_time = 0
        total_visited = 0
        total_cost = 0

        for i in range(trials):
            start, goal = random.sample(range(n), 2)
            t0 = time.time()
            path, cost, visited = algo(graph, start, goal)
            t1 = time.time()

            total_time += t1 - t0
            total_visited += visited
            total_cost += cost if cost is not None else 0

        avg_time = total_time / trials
        avg_visited = total_visited / trials
        avg_cost = total_cost / trials

        # Use .format() for compatibility
        print("{:<9} | {:>11.2f} | {:>12.5f} | {:>8.2f}".format(
            name, avg_visited, avg_time, avg_cost))

        
# -------------------- Run --------------------

run_experiment(1000, 5)



