import argparse
import tkinter as tk
from solvers import (
    RandomizedBacktrackingSolver,
    MinConflictsSolver,
    SimulatedAnnealingSolver,
    GeneticAlgorithmSolver,
    RandomRestartHillClimbingSolver,
    ParticleSwarmOptimizationSolver,
    Visualizer
)

SOLVER_MAP = {
    "backtracking": RandomizedBacktrackingSolver,
    "min_conflicts": MinConflictsSolver,
    "hill_climbing": RandomRestartHillClimbingSolver,
    "annealing": SimulatedAnnealingSolver,
    "genetic": GeneticAlgorithmSolver,
    "pso": ParticleSwarmOptimizationSolver
}

def run():
    parser = argparse.ArgumentParser(description="N-Queens AI & Heuristics Benchmark Lab")
    parser.add_argument(
        "--algorithm", "-a",
        choices=list(SOLVER_MAP.keys()) + ["all"],
        default="all",
        help="Algorithm to run (default: all)"
    )
    parser.add_argument("--n", type=int, default=8, help="Board dimension / Queen count (default: 8)")
    parser.add_argument("--gui", action="store_true", help="Launch interactive Chess.com-styled GUI analysis window")
    parser.add_argument("--plot", action="store_true", help="Export static PNG plots")
    args = parser.parse_args()

    selected = list(SOLVER_MAP.keys()) if args.algorithm == "all" else [args.algorithm]
    benchmark_results = {}

    print(f"\n=======================================================")
    print(f"       N-QUEENS SEARCH BENCHMARK (N = {args.n})        ")
    print(f"=======================================================")

    # Initialize a root Tk instance if GUI mode is requested
    root = None
    if args.gui:
        root = tk.Tk()
        root.withdraw()  # Hide root master, each solver opens its own Toplevel window

    for name in selected:
        solver_class = SOLVER_MAP[name]
        solver = solver_class(n=args.n)
        solution = solver.solve()

        if solution:
            Visualizer.print_board(solution, solver_name=solver_class.__name__)
            print(f"Status: SOLVED | Iterations/Steps: {solver.metrics['iterations']} | Time: {solver.metrics['runtime_sec']:.5f}s")
            benchmark_results[name] = solver.metrics

            if args.gui:
                Visualizer.open_chess_window(solver_class.__name__, solution, solver.metrics)

            if args.plot and args.algorithm != "all":
                Visualizer.plot_board(solution, solver_name=solver_class.__name__, filename=f"{name}_solution.png")
        else:
            print(f"\n[{solver_class.__name__}] Failed to converge within constraints.")

    if args.plot and len(benchmark_results) > 1:
        Visualizer.plot_comparison_chart(benchmark_results, filename="benchmark_comparison.png")

    if args.gui and root:
        print("\n[GUI] All analysis windows launched. Close the windows to exit.")
        root.mainloop()

if __name__ == "__main__":
    run()
