import random
import time
from typing import List, Optional
from .base import BaseQueenSolver

class RandomizedBacktrackingSolver(BaseQueenSolver):
    """
    Constraint satisfaction via depth-first search.
    Randomizes the candidate row evaluation order per column to yield
    different valid solutions on each run.
    """
    def solve(self) -> Optional[List[int]]:
        start_time = time.perf_counter()
        self.metrics["iterations"] = 0
        board = [-1] * self.n

        def is_safe(row: int, col: int) -> bool:
            for c in range(col):
                r = board[c]
                if r == row or abs(r - row) == abs(c - col):
                    return False
            return True

        def place_queen(col: int) -> bool:
            if col == self.n:
                return True

            rows = list(range(self.n))
            random.shuffle(rows)  # Ensures a randomized traversal path

            for row in rows:
                self.metrics["iterations"] += 1
                if is_safe(row, col):
                    board[col] = row
                    if place_queen(col + 1):
                        return True
                    board[col] = -1
            return False

        success = place_queen(0)
        self.metrics["runtime_sec"] = time.perf_counter() - start_time
        self.metrics["solved"] = success
        return board if success else None