import math
import random
import time
from typing import List, Optional
from .base import BaseQueenSolver

class SimulatedAnnealingSolver(BaseQueenSolver):
    """
    Simulated Annealing metaheuristic.
    Initializes with a random permutation and perturbs state by swapping queens
    or reassigning rows using the Metropolis acceptance criterion.
    """
    def __init__(self, n: int = 8, initial_temp: float = 100.0, cooling_rate: float = 0.995, max_steps: int = 25000):
        super().__init__(n)
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.max_steps = max_steps

    def solve(self) -> Optional[List[int]]:
        start_time = time.perf_counter()
        current_board = self.get_random_permutation()
        current_energy = self.count_conflicts(current_board)
        temp = self.initial_temp

        for step in range(1, self.max_steps + 1):
            self.metrics["iterations"] = step
            if current_energy == 0:
                self.metrics["runtime_sec"] = time.perf_counter() - start_time
                self.metrics["solved"] = True
                return current_board

            next_board = list(current_board)
            col1, col2 = random.sample(range(self.n), 2)
            next_board[col1], next_board[col2] = next_board[col2], next_board[col1]

            next_energy = self.count_conflicts(next_board)
            delta_e = next_energy - current_energy

            if delta_e < 0 or random.random() < math.exp(-delta_e / max(temp, 1e-8)):
                current_board = next_board
                current_energy = next_energy

            temp *= self.cooling_rate

        self.metrics["runtime_sec"] = time.perf_counter() - start_time
        self.metrics["solved"] = (current_energy == 0)
        return current_board if self.metrics["solved"] else None