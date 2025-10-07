import random, time, tracemalloc

# ---------------- Board Generator (unchanged) ----------------
sample_board = [[4,5,6,7,8,9,1,2,3],[7,8,9,1,2,3,4,5,6],[1,2,3,4,5,6,7,8,9],
                [8,9,1,2,3,4,5,6,7],[2,3,4,5,6,7,8,9,1],[5,6,7,8,9,1,2,3,4],
                [6,7,8,9,1,2,3,4,5],[9,1,2,3,4,5,6,7,8],[3,4,5,6,7,8,9,1,2]]

def generate_random_board(sample_board):
    def randomise_digits(board):
        temp = list(range(1,10))
        random.shuffle(temp)
        return [[temp[val-1] for val in row] for row in board]
    
    def swap_row_groups(board):
        g1,g2 = random.sample(range(0,3),2)
        for i in range(3):
            board[3*g1+i],board[3*g2+i] = board[3*g2+i],board[3*g1+i]
        
    def transpose(board):
        for i in range(9):
            for j in range(i+1,9):
                board[i][j],board[j][i] = board[j][i],board[i][j]
                
    def make_blanks(board):
        blanks = random.randint(30,40)
        while blanks:
            pos = random.randint(0,80)
            if board[pos//9][pos%9] != 0:
                board[pos//9][pos%9] = 0
                blanks -= 1
        
    board = [row[:] for row in sample_board]
    board = randomise_digits(board)
    swap_row_groups(board)
    transpose(board)
    make_blanks(board)
    return board


# ---------------- Helper Functions ----------------
def find_empty(board):
    """Find first empty cell (row, col), or None if full."""
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return r, c
    return None

def valid(board, r, c, val):
    """Check if val can be placed at (r, c)."""
    if val in board[r]: return False                      # Row
    if val in [board[i][c] for i in range(9)]: return False # Col
    br, bc = 3*(r//3), 3*(c//3)
    for i in range(br, br+3):
        for j in range(bc, bc+3):
            if board[i][j] == val: return False
    return True

def domain(board, r, c):
    """Return all possible values for (r,c)."""
    return [v for v in range(1,10) if valid(board, r, c, v)]


# ---------------- Solver Without Heuristics ----------------
def solve_no_heuristics(board):
    pos = find_empty(board)
    if not pos: return True
    r,c = pos
    for val in domain(board, r, c):
        board[r][c] = val
        if solve_no_heuristics(board): return True
        board[r][c] = 0
    return False


# ---------------- Solver With Heuristics (MRV + LCV) ----------------
def solve_with_heuristics(board):
    # Find empty cells with MRV
    empties = [(r,c) for r in range(9) for c in range(9) if board[r][c]==0]
    if not empties: return True
    r,c = min(empties, key=lambda pos: len(domain(board, pos[0], pos[1])))
    
    # LCV ordering
    values = sorted(domain(board, r, c), key=lambda v: sum(v in domain(board, x,y) for (x,y) in empties if (x,y)!=(r,c)))
    
    for val in values:
        board[r][c] = val
        if solve_with_heuristics(board): return True
        board[r][c] = 0
    return False


# ---------------- Run & Compare ----------------
sudoku_board = generate_random_board(sample_board)
board1 = [row[:] for row in sudoku_board]
board2 = [row[:] for row in sudoku_board]

# Without heuristics
tracemalloc.start(); t1 = time.time()
solve_no_heuristics(board1)
t1 = round(time.time()-t1,5); _,m1 = tracemalloc.get_traced_memory(); tracemalloc.stop()

# With heuristics
tracemalloc.start(); t2 = time.time()
solve_with_heuristics(board2)
t2 = round(time.time()-t2,5); _,m2 = tracemalloc.get_traced_memory(); tracemalloc.stop()

# Print results
print("\n-- Sudoku Solution (No Heuristics) --")
for row in board1: print(row)

print("\n-- Sudoku Solution (With Heuristics) --")
for row in board2: print(row)

print("\n---- Time & Memory ----")
print("No Heuristics:  {}s | {} MB".format(t1, round(m1/1024/1024,5)))
print("With Heuristics: {}s | {} MB".format(t2, round(m2/1024/1024,5)))
