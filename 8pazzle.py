final_part = [1, 2, 3, 4, 5, 6, 7, 8, 0]
moves = {0: [1, 3],1: [0, 2, 4],2: [1, 5],3: [0, 4, 6],4: [1, 3, 5, 7],5: [2, 4, 8],6: [3, 7],7: [4, 6, 8],8: [5, 7]}
def zerof(arr):
    return arr.index(0)
def swap(lst, a, b):
    lst[a], lst[b] = lst[b], lst[a]
def bfs(start):
    visited = set()
    storage = [start]
    visited.add(tuple(start))
    parent = {tuple(start): None}
    while storage:
        arr = storage.pop(0)
        if arr == final_part:
            path = []
            node = tuple(arr)
            while node is not None:
                path.append(list(node))
                node = parent[node]
            path.reverse()
            #print(f"Moves required: {len(path)-1}")
            i=1
            for step in path:
            	print("step : "+str(i))
            	print(step[0:3])
            	print(step[3:6])
            	print(step[6:9])
            	i=i+1
            return
        i = zerof(arr)
        for q in moves[i]:
            new_arr = arr[:]
            swap(new_arr, q, i)
            if tuple(new_arr) not in visited:
                visited.add(tuple(new_arr))
                storage.append(new_arr)
                parent[tuple(new_arr)] = tuple(arr)
    return None
import random
def random_puzzle():
    p = list(range(9))
    random.shuffle(p)
    return p
p = random_puzzle()
print("inital state  : \n")
print(p[0:3])
print(p[3:6])
print(p[6:9])
print(bfs(random_puzzle()))
