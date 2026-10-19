# ♛ N-Queens AI & Heuristics Laboratory

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Profile](https://img.shields.io/badge/Author-Omar%20Soudan-181717?logo=github)](https://github.com/OmarSoudan)

A multi-paradigm benchmark laboratory and analysis framework exploring classical search, metaheuristics, evolutionary computation, and swarm intelligence to solve the famous **N-Queens Constraint Satisfaction Problem (CSP)**.

The lab guarantees non-deterministic initializations on every run—producing distinct valid placements across invocations without caching history—and pairs each execution with high-resolution visual boards and engine telemetry.

---

## ⚡ Core Features

- **6 Distinct Paradigms**: Spanning deterministic tree search, repair heuristics, thermal annealing, bio-inspired genetics, and swarm velocity dynamics.
- **Interactive Chess.com GUI**: Standalone Tkinter-powered visualizer featuring authentic board styling, vector-styled pieces, coordinate files/ranks, and side-by-side algorithmic telemetry cards.
- **Dynamic Initial States**: Every solver begins from an independently randomized configuration or permutation, ensuring each run yields a distinct valid solution.
- **Comparative Profiler**: Benchmarking pipeline tracking wall-clock latency, iteration counts, search state traversals, and automated comparative chart generation.
- **Zero-Dependency Core GUI**: Clean, native GUI engine built entirely on Python's built-in `tkinter`—no fragile image assets or heavy desktop frameworks required.

---

## 🔬 Solvers & Algorithmic Matrix

| Algorithm | Paradigm | Time Complexity (Avg) | Space Complexity | Completeness | Non-Determinism Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Randomized Backtracking** | Exact CSP / Depth-First Search | O(N!) worst; << O(N!) empirical | O(N) recursion depth | **Yes** (Exact) | Randomizes row search permutation per column at every recursive frame. |
| **Min-Conflicts** | Heuristic Local Repair CSP | ~ O(N) for N <= 10^6 | O(N) vector | **No** (Local minima) | Seeds random permutations; resolves conflicting queen moves via randomized tie-breaking. |
| **Hill Climbing** | Steepest-Ascent Local Search | O(R * S * N^2) | O(N) vector | **No** (Bounded restarts) | Pairwise swap neighbor evaluation combined with random restarts upon hitting plateaus. |
| **Simulated Annealing** | Thermodynamic Metaheuristic | O(K * N) (K = steps) | O(N) vector | **Asymptotically** | Metropolis criterion P = exp(-delta_E / T) enables stochastic escapes from energy basins. |
| **Genetic Algorithm (GA)** | Evolutionary AI | O(G * P * N^2) | O(P * N) (P = pop) | **No** (Stochastic) | Tournament selection, single-point crossover slicing, and random gene mutation. |
| **Particle Swarm (PSO)** | Swarm Intelligence | O(I * S * N^2) | O(S * N) (S = swarm) | **No** (Stochastic) | Particles update coordinates driven by personal best (c1) and global swarm best (c2). |

---

## 📁 Repository Structure

```text
n-queens-ai-lab/
├── README.md
├── requirements.txt
├── main.py                    # Unified entrypoint & CLI benchmark runner
└── solvers/
    ├── __init__.py
    ├── base.py                # Abstract base solver, state representations, conflict metrics
    ├── backtracking.py        # Stochastic DFS CSP solver
    ├── min_conflicts.py       # Heuristic local repair solver
    ├── hill_climbing.py       # Steepest-ascent with random restarts
    ├── simulated_annealing.py # Thermodynamic annealing solver
    ├── genetic.py             # Evolutionary chromosome solver
    ├── pso.py                 # Particle swarm optimization solver
    ├── gui_visualizer.py      # Chess.com-style interactive GUI window
    └── visualizer.py          # Terminal rendering & Matplotlib static exports



    🚀 Getting Started
Prerequisites
Python 3.8 or higher

matplotlib & numpy (for benchmark plotting exports)


# Clone the repository
git clone [https://github.com/OmarSoudan/n-queens-ai-lab.git](https://github.com/OmarSoudan/n-queens-lab.git)
cd n-queens-lab

# Install dependencies
pip install -r requirements.txt


💻 Usage & CLI Reference
1. Interactive Chess.com GUI Mode
Launch dedicated visual windows displaying the solved board along with an analysis dossier:

# Run Genetic Algorithm with interactive GUI (N=8)
python main.py -a genetic --n 8 --gui

# Run Min-Conflicts with interactive GUI on a larger board (N=16)
python main.py -a min_conflicts --n 16 --gui

# Run all 6 algorithms simultaneously and inspect their GUI windows side by side
python main.py -a all --n 8 --gui

2. Terminal Benchmarking
Run solvers directly in your console to compare execution speed and convergence iterations:

# Benchmark all solvers on standard 8-Queens
python main.py --n 8

# Benchmark Min-Conflicts on large-scale boards
python main.py -a min_conflicts --n 64

3. Export High-Resolution Visual Plots
Generate publication-ready static PNGs of the board and comparative bar charts:

# Export static board plot for a specific algorithm
python main.py -a annealing --n 8 --plot

# Generate full benchmark comparison chart across all engines
python main.py -a all --n 8 --plot

📊 Analytical Insights
CSP Phase Transitions & Solution Density: For the N-Queens problem, the density of valid solutions grows dramatically as N increases. As a consequence, Min-Conflicts solves configurations where N >= 1,000 in near-linear time (O(N)), while exhaustive backtracking suffers combinatorial state explosion.

Escaping Local Basins: Pure greedy hill climbers easily stall on diagonal conflict plateaus. By introducing thermal probability distribution (exp(-delta_E / T) in Annealing) or diverse candidate gene pools (Genetic Algorithm), metaheuristic strategies step backward through the fitness landscape to escape suboptimal traps.

Completeness vs. Scalability: While Randomized Backtracking is the only method guaranteed to prove unsolvability (e.g., N=2, 3) or explore the full state space tree, stochastic heuristic methods scale significantly better for large practical board dimensions.

👨‍💻 Author
Omar Soudan

GitHub: @OmarSoudan

📜 License
Distributed under the MIT License. See LICENSE for more information.
