import random

def objective_function(arr):
    value=0
    for i in range(len(arr)):
        for j in range(i+1,len(arr)):
            if(arr[i]==arr[j] or abs(arr[i] - arr[j]) == abs(i-j)):
                value+=1
    return value

def best_neighbour(board):
    current_object=objective_function(board)
    best_neighbour=[]
    for  i in range(len(board)):
        for j in range(len(board)):
            if(i!=j):
                new_board=board[:]
                new_board[i]=j
                new_objfunval=objective_function(new_board)
                if current_object > new_objfunval:
                    current_object=new_objfunval
                    best_neighbour = new_board[:]
    return best_neighbour,current_object

def random_8_Queens(maxvalue):
    no_of_start=0
    while no_of_start<=maxvalue:
        start=list(range(0,8))
        random.shuffle(start)
        curr_objfuncvalue = objective_function(start)
        while curr_objfuncvalue > 0:
            neighbour, new_objfuncvalue = best_neighbour(start)
            if new_objfuncvalue >= curr_objfuncvalue: 
                break
            start = neighbour
            curr_objfuncvalue = new_objfuncvalue
        no_of_start += 1
        
        if curr_objfuncvalue == 0:
            print("We found the solution !!")
            print("No. of restarts required to solve this configuration: {}".format(no_of_start))
            print(start)
            return
    print("Failed to reach the solution (Terminated as restart count exceeded threshold)")
    return
            
random_8_Queens(20)
