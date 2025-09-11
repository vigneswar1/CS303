import random
import time
import tracemalloc,sys
sys.setrecursionlimit(25000)


def planar_graph(n):
    graph = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(i + 1, min(i + 4, n)):
            graph[i].append(j)
            graph[j].append(i)
    return graph
    
def is_consistent(assignment,graph, var, value):
    for neighbor in graph[var]:
        if neighbor in assignment and assignment[neighbor] == value:
            return False
    return True

def backtrack(assignment, variables, values, graph):
    if len(assignment) == len(variables):
        return assignment

    unassigned = [v for v in variables if v not in assignment]
    var = unassigned[0]

    for val in values:
        if is_consistent(assignment,graph,var, val):
            assignment[var] = val
            result = backtrack(assignment, variables, values, graph)
            if result:
                return result
            del assignment[var]
    return None

def run_experiment(n, colors):
    graph = planar_graph(n)
    variables = list(graph.keys())
    assignment = {}
    values = colors
    tracemalloc.start()
    start_time = time.time()
    solution = backtrack(assignment, variables, values, graph)
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        'nodes': n,
        'edges': sum(len(v) for v in graph.values()) // 2,
        'time_sec': round(end_time - start_time, 4),
        'memory_kb': round(peak / (1024), 2),
        'solved': solution is not None
    }



colors = ['Red', 'Green', 'Blue', 'Yellow']
sizes = [100, 1000, 10000]

print(f"{'Nodes':>6} | {'Edges':>6} | {'Time(s)':>8} | {'Memory(MB)':>10} | {'Solved':>7}")
print("-" * 55)
for size in sizes:
    stats = run_experiment(size, colors)
    memory_mb = stats['memory_kb'] / 1024  # Convert KB to MB
    print(f"{stats['nodes']:6} | {stats['edges']:6} | {stats['time_sec']:8.4f} | {memory_mb:10.4f} | {str(stats['solved']):>7}")


