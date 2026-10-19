import random
import time
from typing import List, Optional
from .base import BaseQueenSolver

class Particle:
    def __init__(self, n: int):
        self.position = list(range(n))
        random.shuffle(self.position)
        self.pbest = list(self.position)
        self.pbest_conflicts = BaseQueenSolver.count_conflicts(self.position)

class ParticleSwarmOptimizationSolver(BaseQueenSolver):
    """
    Continuous/Discrete hybrid Particle Swarm Optimization (PSO).
    Particles represent candidate queen vectors. Position updates are guided
    by individual best (cognitive) and swarm best (social) attractor permutations.
    """
    def __init__(self, n: int = 8, num_particles: int = 60, max_iterations: int = 1500, c1: float = 1.4, c2: float = 1.4):
        super().__init__(n)
        self.num_particles = num_particles
        self.max_iterations = max_iterations
        self.c1 = c1
        self.c2 = c2

    def solve(self) -> Optional[List[int]]:
        start_time = time.perf_counter()
        swarm = [Particle(self.n) for _ in range(self.num_particles)]

        gbest = list(swarm[0].position)
        gbest_conflicts = self.count_conflicts(gbest)

        for p in swarm:
            if p.pbest_conflicts < gbest_conflicts:
                gbest = list(p.position)
                gbest_conflicts = p.pbest_conflicts

        for iteration in range(1, self.max_iterations + 1):
            self.metrics["iterations"] = iteration
            if gbest_conflicts == 0:
                self.metrics["runtime_sec"] = time.perf_counter() - start_time
                self.metrics["solved"] = True
                return gbest

            for particle in swarm:
                # Cognitive attractor (move toward personal best)
                if random.random() < self.c1 / 2.0:
                    i, j = random.sample(range(self.n), 2)
                    particle.position[i] = particle.pbest[i]

                # Social attractor (move toward global best)
                if random.random() < self.c2 / 2.0:
                    i = random.randint(0, self.n - 1)
                    particle.position[i] = gbest[i]

                # Random perturbation (mutation/velocity)
                if random.random() < 0.2:
                    col = random.randint(0, self.n - 1)
                    particle.position[col] = random.randint(0, self.n - 1)

                current_conflicts = self.count_conflicts(particle.position)

                # Update particle best
                if current_conflicts < particle.pbest_conflicts:
                    particle.pbest = list(particle.position)
                    particle.pbest_conflicts = current_conflicts

                # Update swarm best
                if current_conflicts < gbest_conflicts:
                    gbest = list(particle.position)
                    gbest_conflicts = current_conflicts
                    if gbest_conflicts == 0:
                        self.metrics["runtime_sec"] = time.perf_counter() - start_time
                        self.metrics["solved"] = True
                        return gbest

        self.metrics["runtime_sec"] = time.perf_counter() - start_time
        self.metrics["solved"] = (gbest_conflicts == 0)
        return gbest if self.metrics["solved"] else None