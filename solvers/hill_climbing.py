import random
import time
from typing import List, Optional
from .base import BaseQueenSolver

class RandomRestartHillClimbingSolver(BaseQueenSolver):
    """
    Steepest-Ascent Hill Climbing with Random Restarts.
    Finds the neighbor that yields the maximum decrease in conflicts.
    If trapped in a local optimum or plateau, it restarts from a fresh state.
    """
    def __init__(self, n: int = 8, max_restarts: int = 100, max_steps_per_run: int = 200):
        super().__init__(n)
        self.max_restarts = max_restarts
        self.max_steps_per_run = max_steps_per_run

    def solve(self) -> Optional[List[int]]:
        start_time = time.perf_counter()
        total_evaluations = 0

        for _ in range(self.max_restarts):
            board = self.get_random_permutation()
            current_conflicts = self.count_conflicts(board)

            for step in range(self.max_steps_per_run):
                total_evaluations += 1
                if current_conflicts == 0:
                    self.metrics["iterations"] = total_evaluations
                    self.metrics["runtime_sec"] = time.perf_counter() - start_time
                    self.metrics["solved"] = True
                    return board

                best_neighbors = []
                best_conflicts = current_conflicts

                # Examine pairwise swaps (maintains 1 queen per row and col)
                for i in range(self.n):
                    for j in range(i + 1, self.n):
                        board[i], board[j] = board[j], board[i]
                        c = self.count_conflicts(board)
                        if c < best_conflicts:
                            best_conflicts = c
                            best_neighbors = [(i, j)]
                        elif c == best_conflicts:
                            best_neighbors.append((i, j))
                        # Undo
                        board[i], board[j] = board[j], board[i]

                # If no strictly better neighbor exists, local minimum reached -> restart
                if best_conflicts >= current_conflicts or not best_neighbors:
                    break

                i, j = random.choice(best_neighbors)
                board[i], board[j] = board[j], board[i]
                current_conflicts = best_conflicts

        self.metrics["iterations"] = total_evaluations
        self.metrics["runtime_sec"] = time.perf_counter() - start_time
        self.metrics["solved"] = False
        return None