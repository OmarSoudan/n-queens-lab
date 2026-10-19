from abc import ABC, abstractmethod
import random
from typing import List, Tuple, Optional

class BaseQueenSolver(ABC):
    """
    Abstract Base Class for N-Queens Solvers.
    Board representation: A 1D list where index represents the column (0 to N-1),
    and board[col] represents the row index (0 to N-1) of the queen in that column.
    """
    def __init__(self, n: int = 8):
        self.n = n
        self.metrics = {
            "iterations": 0,
            "runtime_sec": 0.0,
            "solved": False
        }

    @abstractmethod
    def solve(self) -> Optional[List[int]]:
        """Executes the solver and returns the board solution list."""
        pass

    def get_random_board(self) -> List[int]:
        """Generates a random board where each column has a random row."""
        return [random.randint(0, self.n - 1) for _ in range(self.n)]

    def get_random_permutation(self) -> List[int]:
        """Generates a random permutation guaranteeing no row-wise conflicts."""
        board = list(range(self.n))
        random.shuffle(board)
        return board

    @staticmethod
    def count_conflicts(board: List[int]) -> int:
        """
        Calculates total pairs of queens threatening each other.
        0 conflicts means a valid solution is reached.
        """
        n = len(board)
        conflicts = 0
        for i in range(n):
            for j in range(i + 1, n):
                # Row collision
                if board[i] == board[j]:
                    conflicts += 1
                # Diagonal collision
                elif abs(board[i] - board[j]) == abs(i - j):
                    conflicts += 1
        return conflicts