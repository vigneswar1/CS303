import random
final_state=[1,2,3,4,5,6,7,8,0]

moves={0: [1, 3],1: [0, 2, 4],2: [1, 5],3: [0, 4, 6],4: [1, 3, 5, 7],5: [2, 4, 8],6: [3, 7],7: [4, 6, 8],8: [5, 7]}

def zerop(arr):
    return arr.index(0)
        
def swap(arr,i,j):
    arr[i],arr[j]=arr[j],arr[i]

def objective_function(arr):
    value,k=0,0
    for i in range(0,len(arr)):
        if arr[i]!=final_state[k]:
            value=value+1
        k=k+1
    return value

def isSolvable(board):
    noOfinversions = 0
    for i in range(0,len(board)):
        for j in range(i+1,len(board)):
            if(board[i]!=0 and board[j]!=0 and board[i]>board[j]):
                noOfinversions += 1 
    if(noOfinversions&1 == 0): return True
    return False

def best_neighbour(arr):
    current_object=objective_function(arr)
    new_neighbour=[]
    objective=[]
    k=0
    i=zerop(arr)
    for j in moves[i]:
        new_arr=arr[:]
        swap(new_arr,i,j)
        new_neighbour.append(new_arr)
        objective.append(objective_function(new_arr))
        k=k+1
    idx = objective.index(min(objective))
    return new_neighbour[idx], min(objective)

def random_8_puzzle(maxvalue):
    no_of_starts=0
    while no_of_starts<=maxvalue:
        start=list(range(9))
        random.shuffle(start)
        current_object=objective_function(start)
        if isSolvable(start):
            while(current_object>0):
                next_board,newboard_obvalue=best_neighbour(start)
                if newboard_obvalue>=current_object:
                    break
                start = next_board
                current_object=newboard_obvalue
            no_of_starts+=1
            if current_object==0:
                print("We found the solution !!")
                print("No. of restarts required to solve 8-puzzle {}".format(no_of_starts))
                print(start)
                return
    print(start)
    print("Failed to reach the solution (Terminated as restart count exceeded maxvalue)")
    return
        

random_8_puzzle(200)


        
