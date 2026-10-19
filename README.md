# ♛ N‑Queens AI & Heuristics Laboratory

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Author: Omar Soudan](https://img.shields.io/badge/Author-Omar%20Soudan-181717?logo=github)](https://github.com/OmarSoudan)

A compact experimental framework for solving the N‑Queens constraint-satisfaction problem using a variety of search and optimization paradigms. This lab provides deterministic and stochastic solvers, benchmarking utilities, and a lightweight interactive visualizer to compare algorithmic behavior, performance, and convergence.

Key design goals:
- Reproducible yet non-deterministic runs (every execution starts from a new randomized initial state).
- Lightweight, dependency-minimal GUI (built with built-in `tkinter`).
- A unified CLI for benchmarking and exporting publication-quality visualizations.

---

## Core Features

- Six algorithmic paradigms spanning exact search, local repair, metaheuristics, evolutionary computation, and swarm intelligence.
- Interactive chess-style GUI (Tkinter) with board rendering, piece vectors, and telemetry panels.
- Randomized initial states for each run to examine algorithm robustness.
- Built-in benchmarking: wall-clock time, iteration counts, state traversals, and automated chart generation.
- Minimal external dependencies: only numpy and matplotlib for plotting/exporting.

---

## Algorithms

| Algorithm | Paradigm | Expected Time (typical) | Space | Notes |
|---|---:|---:|---:|---|
| Randomized Backtracking | Exact DFS / CSP | Exponential (worst-case) | O(N) recursion | Exact solver; randomizes column/row search order to diversify solutions. |
| Min‑Conflicts | Local Repair CSP | ~O(N) (practical for many N) | O(N) | Fast and scalable; can get trapped in local minima without random tie-breaking. |
| Hill Climbing | Steepest‑Ascent Local Search | O(R · S · N^2) | O(N) | Uses pairwise swaps + random restarts to escape plateaus. |
| Simulated Annealing | Thermodynamic Metaheuristic | O(K · N) (K = steps) | O(N) | Metropolis acceptance (exp(-ΔE / T)) enables stochastic escapes from energy basins. |
| Genetic Algorithm (GA) | Evolutionary | O(G · P · N^2) | O(P · N) | Population-based search with selection, crossover, and mutation; stochastic. |
| Particle Swarm (PSO) | Swarm Intelligence | O(I · S · N^2) | O(S · N) | Particles update using personal & global bests; suited to continuous relaxations of discrete problems. |

---

## Repository Layout

```text
n-queens-ai-lab/
├── README.md
├── LICENSE
├── requirements.txt
├── main.py                    # Unified CLI and benchmark runner
└── solvers/
    ├── __init__.py
    ├── base.py                # Base solver, state representation, conflict metrics
    ├── backtracking.py        # Randomized DFS CSP solver
    ├── min_conflicts.py       # Heuristic local repair solver
    ├── hill_climbing.py       # Steepest-ascent with restarts
    ├── simulated_annealing.py # Simulated annealing solver
    ├── genetic.py             # Genetic Algorithm implementation
    ├── pso.py                 # Particle Swarm Optimizer
    ├── gui_visualizer.py      # Tkinter-based interactive visualizer
    └── visualizer.py          # CLI plotting & Matplotlib exports
```

---

## Getting Started

Requirements
- Python 3.8+
- (Optional) numpy, matplotlib — only needed for plotting/export features

Clone and install:

```bash
git clone https://github.com/OmarSoudan/n-queens-lab.git
cd n-queens-lab
pip install -r requirements.txt
```

---

## Usage

Run solvers from the command line using `main.py`. The CLI supports individual algorithms, combined runs, GUI mode, and plot exports.

Examples:

- Run the Genetic Algorithm with the interactive GUI (N = 8):
  ```bash
  python main.py -a genetic --n 8 --gui
  ```

- Run Min‑Conflicts with GUI (N = 16):
  ```bash
  python main.py -a min_conflicts --n 16 --gui
  ```

- Benchmark all solvers in the terminal (N = 8):
  ```bash
  python main.py --n 8
  ```

- Benchmark Min‑Conflicts on a larger board (N = 64):
  ```bash
  python main.py -a min_conflicts --n 64
  ```

- Export a static board plot for Simulated Annealing:
  ```bash
  python main.py -a annealing --n 8 --plot
  ```

- Generate a comparative benchmark chart for all solvers:
  ```bash
  python main.py -a all --n 8 --plot
  ```

See `python main.py --help` for full CLI options and configuration flags.

---

## Analytical Notes

- Phase transitions and solution density: The number of valid N‑Queens configurations grows rapidly; some heuristics (like Min‑Conflicts) exploit this density to scale well for large N.
- Escaping local minima: Greedy hill climbers can stall on diagonal-constraint plateaus. Simulated annealing and stochastic genetic operators provide mechanisms for escape (temperature schedule, mutation/crossover diversity).
- Completeness vs. scalability: Randomized backtracking is the only complete method here (able to prove unsatisfiable cases like N = 2, 3). Heuristic methods trade completeness for much better scalability on large boards.

---

## Contributing

Contributions, suggestions, and bug reports are welcome. Create issues or PRs on the repository. If you add new solvers or visualizations, please include tests and a short benchmark comparison.

---

## Author & License

Author: Omar Soudan — https://github.com/OmarSoudan

License: MIT — see LICENSE for details
