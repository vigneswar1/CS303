import time
import tracemalloc

computer = 'X'
human = 'O'

def who_is_the_winner(board):
    # row
    for row in range(3):
        if board[3*row] != " " and board[3*row] == board[(3*row)+1] == board[(3*row)+2]:
            return board[3*row]
    # col
    for col in range(3):
        if board[col] != " " and board[col] == board[col+3] == board[col+6]:
            return board[col]
    # leftside diagonal
    if board[0] != " " and board[0] == board[4] == board[8]:
        return board[0]
    # rightside diagonal
    if board[2] != " " and board[2] == board[4] == board[6]:
        return board[2]
    return None

def is_board_filled(board):
    if " " in board:
        return False
    return True

def terminal_test(board):
    if who_is_the_winner(board) is not None:
        return True
    elif is_board_filled(board):
        return True
    return False

def utility(board):
    result = who_is_the_winner(board)
    if result == "X":
        return 1
    elif result == "O":
        return -1
    else:
        return 0

def possible_actions(board):
    actions = [pos for pos in range(len(board)) if board[pos] == " "]
    return actions

def resulting_board(board, action, player):
    new_board = board[:]
    new_board[action] = player
    return new_board

def max_value(board):
    if terminal_test(board):
        return utility(board)
    
    alpha = -1*float('inf')
    for action in possible_actions(board):
        alpha = max(alpha, min_value(resulting_board(board, action, "X")))
    return alpha

def min_value(board):
    if terminal_test(board):
        return utility(board)
    
    beta = float('inf')
    for action in possible_actions(board):
        beta = min(beta, max_value(resulting_board(board, action, "O")))
    return beta

def minimax_algo(board):
    best_score = -1*float('inf')
    best_action = None
    for action in possible_actions(board):
        curr_score = min_value(resulting_board(board, action, "X"))
        if curr_score > best_score:
            best_score = curr_score
            best_action = action
    return best_action

def max_value_alpha_beta(board, alpha, beta):
    if terminal_test(board):
        return utility(board)
    
    value = -1*float('inf')
    for action in possible_actions(board):
        value = max(value, min_value_alpha_beta(resulting_board(board, action, "X"), alpha, beta))
        alpha = max(alpha, value)
        if alpha >= beta:
            break
    return value

def min_value_alpha_beta(board, alpha, beta):
    if terminal_test(board):
        return utility(board)
    
    value = float('inf')
    for action in possible_actions(board):
        value = min(value, max_value_alpha_beta(resulting_board(board, action, "O"), alpha, beta))
        beta = min(beta, value)
        if alpha >= beta:
            break
    return value

def alpha_beta_minimax(board):
    best_score = -1*float('inf')
    best_action = None
    alpha = -1*float('inf')
    beta = float('inf')
    for action in possible_actions(board):
        curr_score = min_value_alpha_beta(resulting_board(board, action, "X"), alpha, beta)
        if curr_score > best_score:
            best_score = curr_score
            best_action = action
        alpha = max(alpha, best_score)
    return best_action

def print_board(board):
    for i in range(0, 3):
        print(board[3*i:(3*i)+3])

print("\nTic-Tac-Toe Game\n")

print("Positions on board are indicated as following")
board = [i for i in range(9)]
print_board(board)

board = [" " for _ in range(9)]

print("\nMini-Max Adversarial Search Algorithm\n")
minimax_time = 0.0
minimax_space = 0.0

print("Initial setup:")
print_board(board)

player = computer
while True:
    if player == computer:
        print("\nComputer plays its move\n")
        tracemalloc.start()
        START = time.time()
        move = minimax_algo(board)
        END = time.time()
        _, memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        minimax_time += (END - START)
        minimax_space += memory
        board[move] = computer
    else:
        move = int(input("Enter the move: "))
        if board[move] != " ":
            print("Invalid input try again")
            continue
        board[move] = human
        print("\nHuman plays his move\n")
    print_board(board)

    result = who_is_the_winner(board)
    if result is not None:
        if result == computer:
            print("\nResult: Won by Computer\n")
        elif result == human:
            print("\nResult: Won by Human\n")
        break

    if is_board_filled(board):
        print("\nResult: It is a draw\n")
        break

    if player == computer:
        player = human
    else:
        player = computer

board = [" " for _ in range(9)]

print("\nAlpha-Beta Mini-Max Adversarial Search Algorithm\n")
alphabeta_time = 0.0
alphabeta_space = 0.0

print("Initial setup:")
print_board(board)

player = computer
while True:
    if player == computer:
        print("\nComputer plays its move\n")
        tracemalloc.start()
        START = time.time()
        move = alpha_beta_minimax(board)
        END = time.time()
        _, memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        alphabeta_time += (END - START)
        alphabeta_space += memory
        board[move] = computer
    else:
        move = int(input("Enter the move: "))
        board[move] = human
        print("\nHuman plays his move\n")
    print_board(board)

    result = who_is_the_winner(board)
    if result is not None:
        if result == computer:
            print("\nResult: Won by Computer\n")
        elif result == human:
            print("\nResult: Won by Human\n")
        break

    if is_board_filled(board):
        print("\nResult: It is a draw\n")
        break

    if player == computer:
        player = human
    else:
        player = computer

print(" \t |\t Time \t| Space \t")
print("-----------------------------------")
print(" Minimax | {} sec | {} KB".format(round(minimax_time, 5), round(minimax_space / 1024, 5))) 
print("Alpha-Beta| {} sec | {} KB".format(round(alphabeta_time, 5), round(alphabeta_space / 1024, 5)))
print("-----------------------------------")
