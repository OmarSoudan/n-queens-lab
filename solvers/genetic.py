import random
import time
from typing import List, Tuple, Optional
from .base import BaseQueenSolver

class GeneticAlgorithmSolver(BaseQueenSolver):
    """
    Genetic Algorithm solver.
    Fitness is defined as (max_pairs - conflicts), where max_pairs = n*(n-1)/2.
    Uses tournament selection, single-point crossover, and random mutation.
    """
    def __init__(self, n: int = 8, population_size: int = 150, mutation_rate: float = 0.15, max_generations: int = 2000):
        super().__init__(n)
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations
        self.max_fitness = (n * (n - 1)) // 2

    def _fitness(self, individual: List[int]) -> int:
        return self.max_fitness - self.count_conflicts(individual)

    def _select_parent(self, population: List[List[int]], fitnesses: List[int]) -> List[int]:
        # Tournament selection
        candidates = random.sample(list(zip(population, fitnesses)), k=3)
        candidates.sort(key=lambda x: x[1], reverse=True)
        return list(candidates[0][0])

    def _crossover(self, p1: List[int], p2: List[int]) -> Tuple[List[int], List[int]]:
        c = random.randint(1, self.n - 1)
        child1 = p1[:c] + p2[c:]
        child2 = p2[:c] + p1[c:]
        return child1, child2

    def _mutate(self, individual: List[int]) -> None:
        if random.random() < self.mutation_rate:
            col = random.randint(0, self.n - 1)
            individual[col] = random.randint(0, self.n - 1)

    def solve(self) -> Optional[List[int]]:
        start_time = time.perf_counter()
        population = [self.get_random_board() for _ in range(self.population_size)]

        for gen in range(1, self.max_generations + 1):
            self.metrics["iterations"] = gen
            fitnesses = [self._fitness(ind) for ind in population]

            for idx, fit in enumerate(fitnesses):
                if fit == self.max_fitness:
                    self.metrics["runtime_sec"] = time.perf_counter() - start_time
                    self.metrics["solved"] = True
                    return population[idx]

            new_population = []
            while len(new_population) < self.population_size:
                p1 = self._select_parent(population, fitnesses)
                p2 = self._select_parent(population, fitnesses)
                c1, c2 = self._crossover(p1, p2)
                self._mutate(c1)
                self._mutate(c2)
                new_population.extend([c1, c2])

            population = new_population[:self.population_size]

        self.metrics["runtime_sec"] = time.perf_counter() - start_time
        self.metrics["solved"] = False
        return None
