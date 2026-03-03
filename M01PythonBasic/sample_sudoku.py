import copy
import random
import tkinter as tk
from tkinter import messagebox


class Sudoku:
    def __init__(self, size=9):
        self.size = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]
        self.solution = None

    def is_valid(self, board, row, col, num):
        # Check row
        for i in range(self.size):
            if board[row][i] == num:
                return False

        # Check column
        for i in range(self.size):
            if board[i][col] == num:
                return False

        # Check 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    def find_empty(self, board):
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == 0:
                    return i, j
        return None

    def solve(self, board):
        empty = self.find_empty(board)
        if not empty:
            return True
        row, col = empty

        numbers = list(range(1, 10))
        random.shuffle(numbers)  # Increase randomness to generate different boards

        for num in numbers:
            if self.is_valid(board, row, col, num):
                board[row][col] = num
                if self.solve(board):
                    return True
                board[row][col] = 0
        return False

    def generate_full_board(self):
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.solve(self.grid)
        self.solution = copy.deepcopy(self.grid)

    def remove_numbers(self, count):
        cells = [(i, j) for i in range(self.size) for j in range(self.size)]
        random.shuffle(cells)
        for i in range(count):
            row, col = cells[i]
            self.grid[row][col] = 0


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Sudoku Game")
        self.game = Sudoku()
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.original_grid = None
        self.difficulty = tk.IntVar(value=45)  # Default Medium

        self.setup_ui()
        self.new_game()

    def setup_ui(self):
        # Top control bar
        control_frame = tk.Frame(self.root, pady=10)
        control_frame.pack()

        tk.Label(control_frame, text="Difficulty: ").pack(side=tk.LEFT)
        tk.Radiobutton(control_frame, text="Easy", variable=self.difficulty, value=30).pack(side=tk.LEFT)
        tk.Radiobutton(control_frame, text="Medium", variable=self.difficulty, value=45).pack(side=tk.LEFT)
        tk.Radiobutton(control_frame, text="Hard", variable=self.difficulty, value=60).pack(side=tk.LEFT)

        tk.Button(control_frame, text="New Game", command=self.new_game).pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="Hint", command=self.give_hint).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Solve", command=self.solve_game).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Check", command=self.check_game).pack(side=tk.LEFT, padx=5)

        # Sudoku grid
        self.grid_frame = tk.Frame(self.root, bg="black", bd=2)
        self.grid_frame.pack(padx=20, pady=20)

        # Create 3x3 subgrid frames to show thick borders
        self.subgrid_frames = [[None for _ in range(3)] for _ in range(3)]
        for r in range(3):
            for c in range(3):
                f = tk.Frame(self.grid_frame, bg="black", bd=1)
                f.grid(row=r, column=c, padx=1, pady=1)
                self.subgrid_frames[r][c] = f

        # Create Entry grid
        vcmd = (self.root.register(self.validate_input), "%P")
        for r in range(9):
            for c in range(9):
                sub_r, sub_c = r // 3, c // 3
                entry = tk.Entry(self.subgrid_frames[sub_r][sub_c], width=2, font=("Arial", 18, "bold"),
                                 justify="center", bd=1, validate="key", validatecommand=vcmd)
                entry.grid(row=r % 3, column=c % 3, padx=1, pady=1, ipady=5)
                self.cells[r][c] = entry

    def validate_input(self, P):
        # Only allow empty string or a single digit 1-9
        if P == "" or (len(P) == 1 and P.isdigit() and P != "0"):
            return True
        return False

    def new_game(self):
        self.game.generate_full_board()
        self.game.remove_numbers(self.difficulty.get())
        self.original_grid = copy.deepcopy(self.game.grid)
        self.update_board()

    def update_board(self, show_solution=False):
        board = self.game.solution if show_solution else self.game.grid
        for r in range(9):
            for c in range(9):
                val = board[r][c]
                entry = self.cells[r][c]
                entry.config(state="normal")
                entry.delete(0, tk.END)

                if val != 0:
                    entry.insert(0, str(val))
                    # If it's an initial number, lock it and set it to blue
                    if self.original_grid[r][c] != 0 and not show_solution:
                        entry.config(disabledforeground="blue", state="disabled")
                    else:
                        entry.config(fg="black")
                else:
                    entry.config(fg="black")

    def get_current_grid(self):
        current_grid = [[0 for _ in range(9)] for _ in range(9)]
        for r in range(9):
            for c in range(9):
                val = self.cells[r][c].get()
                if val:
                    current_grid[r][c] = int(val)
        return current_grid

    def check_game(self):
        current_grid = self.get_current_grid()

        # Check if full
        is_full = True
        for r in range(9):
            for c in range(9):
                if current_grid[r][c] == 0:
                    is_full = False
                    break

        # Validation logic
        is_correct = True
        for r in range(9):
            for c in range(9):
                num = current_grid[r][c]
                if num == 0: continue

                # Temporarily remove the number for validation
                temp = current_grid[r][c]
                current_grid[r][c] = 0
                if not self.game.is_valid(current_grid, r, c, temp):
                    is_correct = False
                    current_grid[r][c] = temp
                    break
                current_grid[r][c] = temp
            if not is_correct: break

        if not is_correct:
            messagebox.showerror("Check Result", "There are errors or duplicate numbers, please check!")
        elif is_full:
            messagebox.showinfo("Congratulations", "Great! You correctly completed the Sudoku!")
        else:
            messagebox.showinfo("Check Result", "The current numbers are all valid, keep going!")

    def give_hint(self):
        current_grid = self.get_current_grid()
        empty_cells = [(r, c) for r in range(9) for c in range(9) if current_grid[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            hint_val = self.game.solution[r][c]
            self.game.grid[r][c] = hint_val
            entry = self.cells[r][c]
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, str(hint_val))
            entry.config(fg="green")  # Hint displayed in green
        else:
            messagebox.showinfo("Hint", "The board is full!")

    def solve_game(self):
        if messagebox.askyesno("Solve", "Are you sure you want to show the solution?"):
            self.update_board(show_solution=True)


def main():
    root = tk.Tk()
    root.resizable(False, False)
    gui = SudokuGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
