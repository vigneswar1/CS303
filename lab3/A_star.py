Goalstate=[1,2,3,4,5,6,7,8,0]

moves = {0: [1, 3],1: [0, 2, 4],2: [1, 5],3: [0, 4, 6],4: [1, 3, 5, 7],5: [2, 4, 8],6: [3, 7],7: [4, 6, 8],8: [5, 7]}

import heapq
import random

def swap(list,a,b):
    list[a],list[b]=list[b],list[a]
def zerop(arr):
    return arr.index(0)
def h_function(arr):
    k,c = 0,0
    for i in arr:
        if i!= Goalstate[k]:
            c=c+1
        k=k+1
    return c
def A_star(arr):
    pq=[(h_function(arr),arr)]
    visited=set()
    path={}
    while(pq):
        f,node=heapq.heappop(pq)
        if(node==Goalstate):
            return pathfind(path,node)
        if tuple(node) in visited:
            continue
        visited.add(tuple(node))
        i=zerop(node)
        for q in moves[i]:
            new_arr=node[:]
            swap(new_arr,q,i)
            if tuple(new_arr) not in visited:
                hn = h_function(new_arr)
                gn = f-h_function(node)
                heapq.heappush(pq, (1+gn+hn,new_arr))
                path[tuple(new_arr)]=tuple(node)
    return None
def pathfind(came, current):
    path = [list(current)]
    while tuple(current) in came:
        current = came[tuple(current)]
        path.append(list(current))
    path.reverse()
    return path
def random_puzzle():
    p = list(range(9))
    random.shuffle(p)
    return p
p=random_puzzle()
print("inital state : ")
print(p[0:3])
print(p[3:6])
print(p[6:9])
print("---")
path = A_star(p)
k = 1
if path:
    for i in path:
        print("Step :"+str(k))
        print(i[0:3])
        print(i[3:6])
        print(i[6:9])
        print("---")
        k = k+1
else:
    print("No solution found (might be unsolvable).")
    

