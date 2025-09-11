Goalstate = [1,2,3,4,5,6,7,8,0]

moves = {0: [1, 3],1: [0, 2, 4],2: [1, 5],3: [0, 4, 6],4: [1, 3, 5, 7],5: [2, 4, 8],6: [3, 7],7: [4, 6, 8],8: [5, 7]}

import copy

def swap(state, a, b):
    new_state = state[:]
    new_state[a], new_state[b] = new_state[b], new_state[a]
    return new_state

def zero_pos(state):
    return state.index(0)

def h_function(state):
    return sum([1 for i in range(9) if state[i] != Goalstate[i] and state[i] != 0])

def rbfs(node, f_limit, g, path, visited):
    f = max(g + h_function(node), f_limit)
    
    if node == Goalstate:
        return path + [node], 0
    successors = []
    zero = zero_pos(node)
    for move in moves[zero]:
        new_state = swap(node, zero, move)
        if tuple(new_state) not in visited:
            successors.append(new_state)
    if not successors:
        return None, float('inf')
    f_scores = []
    for s in successors:
        f_scores.append(max(g + 1 + h_function(s), f))
    while True:
        best_idx = min(range(len(successors)), key=lambda i: f_scores[i])
        best = successors[best_idx]
        best_f = f_scores[best_idx]
        if best_f > f_limit:
            return None, best_f
        alt = min([f_scores[i] for i in range(len(f_scores)) if i != best_idx], default=float('inf'))
        visited.add(tuple(best))
        result, f_new = rbfs(best, min(f_limit, alt), g + 1, path + [best], visited)
        visited.remove(tuple(best))
        f_scores[best_idx] = f_new
        if result is not None:
            return result, 0
def print_state(state):
    for i in range(0,9,3):
        print(state[i:i+3])
    print()
if __name__ == "__main__":
    start_state = [1,2,3,4,0,6,7,5,8]
    print("Start state:")
    print_state(start_state)
    solution, cost = rbfs(start_state, float('inf'), 0, [start_state], set([tuple(start_state)]))
    if solution:
        print(f"Solution found in {len(solution)-1} moves:")
        for step in solution:
            print_state(step)
    else:
        print("No solution found")
