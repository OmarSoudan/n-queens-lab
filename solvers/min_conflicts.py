import random
import time
from typing import List, Optional
from .base import BaseQueenSolver

class MinConflictsSolver(BaseQueenSolver):
    """
    Min-Conflicts CSP heuristic solver.
    Starts from a random permutation and moves conflicted queens to rows
    minimizing total conflicts.
    """
    def __init__(self, n: int = 8, max_steps: int = 1000):
        super().__init__(n)
        self.max_steps = max_steps

    def solve(self) -> Optional[List[int]]:
        start_time = time.perf_counter()
        board = self.get_random_permutation()

        for step in range(1, self.max_steps + 1):
            self.metrics["iterations"] = step
            conflicts = self.count_conflicts(board)
            if conflicts == 0:
                self.metrics["runtime_sec"] = time.perf_counter() - start_time
                self.metrics["solved"] = True
                return board

            # Find columns with conflicting queens
            conflicted_cols = []
            for col in range(self.n):
                for other_col in range(self.n):
                    if col == other_col:
                        continue
                    if (board[col] == board[other_col] or 
                        abs(board[col] - board[other_col]) == abs(col - other_col)):
                        conflicted_cols.append(col)
                        break

            chosen_col = random.choice(conflicted_cols)

            # Evaluate row choices in chosen_col
            min_c = float("inf")
            best_rows = []
            for r in range(self.n):
                original_r = board[chosen_col]
                board[chosen_col] = r
                c_count = self.count_conflicts(board)
                if c_count < min_c:
                    min_c = c_count
                    best_rows = [r]
                elif c_count == min_c:
                    best_rows.append(r)
                board[chosen_col] = original_r

            board[chosen_col] = random.choice(best_rows)

        self.metrics["runtime_sec"] = time.perf_counter() - start_time
        self.metrics["solved"] = (self.count_conflicts(board) == 0)
        return board if self.metrics["solved"] else None