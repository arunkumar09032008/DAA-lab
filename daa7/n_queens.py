"""
N-Queens Problem solved using Backtracking.

board[row] = col  ->  a queen is placed at (row, col).
Only one column value is stored per row because a valid solution
never has two queens in the same row, so this representation makes
row/column conflict checks trivial.
"""


def is_safe(board, row, col):
    """Check whether placing a queen at (row, col) is safe given the
    queens already placed in rows 0..row-1."""
    for prev_row in range(row):
        placed_col = board[prev_row]

        if placed_col == col:  # same column
            return False

        if abs(prev_row - row) == abs(placed_col - col):  # same diagonal
            return False

    return True


def solve_n_queens(n):
    """Return (list_of_solutions, backtrack_count) for the N-Queens problem.

    Each solution is a list where index = row, value = column of the queen.
    backtrack_count counts every placement attempt (successful or not) as a
    rough measure of search effort.
    """
    board = [-1] * n
    solutions = []
    backtrack_count = [0]

    def backtrack(row):
        if row == n:
            solutions.append(board[:])
            return

        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(row + 1)
                board[row] = -1  # undo (backtrack)
            backtrack_count[0] += 1

    backtrack(0)
    return solutions, backtrack_count[0]


def board_to_text(solution, n):
    """Render a single solution as an ASCII chessboard string."""
    lines = []
    border = " +" + "---+" * n
    lines.append(border)
    for row in range(n):
        cells = "".join(" Q |" if solution[row] == col else " . |" for col in range(n))
        lines.append(" |" + cells)
        lines.append(border)
    return "\n".join(lines)


def display_board(solution, n):
    print(board_to_text(solution, n))


if __name__ == "__main__":
    # Solve for a few board sizes; show full boards only for the small one.
    for n in [4, 6, 8]:
        solutions, backtracks = solve_n_queens(n)
        print(f"N={n}: {len(solutions)} solutions, {backtracks} backtracks")

        if n == 4:
            print(f"\nAll solutions for {n}-Queens:")
            for i, sol in enumerate(solutions, 1):
                print(f"\nSolution {i}: {sol}")
                display_board(sol, n)
