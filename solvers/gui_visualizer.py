import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Any

# Algorithmic theoretical dossiers for live dashboard inspection
ALGO_ANALYSIS_DATA: Dict[str, Dict[str, str]] = {
    "RandomizedBacktrackingSolver": {
        "paradigm": "Constraint Satisfaction Problem (CSP) / Depth-First Search",
        "completeness": "Guaranteed Complete (Exact)",
        "time_complexity": "O(N!) worst-case, empirical << O(N!)",
        "space_complexity": "O(N) recursion call stack",
        "mechanism": (
            "Traverses column-by-column, testing candidate rows against already placed queens. "
            "Unlike deterministic DFS, candidate rows for each column are randomly shuffled, "
            "sampling an arbitrary branch of the state space tree to guarantee a unique solution each run."
        ),
        "strengths": "Guarantees a valid solution if one exists; proves insolvability for N=2,3 quickly.",
        "bottlenecks": "Exponential combinatorial blowup when scaling to large N (>30)."
    },
    "MinConflictsSolver": {
        "paradigm": "Heuristic Local Repair (CSP)",
        "completeness": "Incomplete (Can get trapped in local minima)",
        "time_complexity": "O(N) empirical for N <= 1,000,000",
        "space_complexity": "O(N) vector footprint",
        "mechanism": (
            "Starts from a random permutation with zero row/col conflicts. At each step, a conflicted "
            "queen is chosen at random and moved to the row in its column that minimizes the total count "
            "of diagonal and row attacks, breaking ties randomly."
        ),
        "strengths": "Ultra-fast convergence; solves 100,000-Queens in seconds.",
        "bottlenecks": "Can cycle or get trapped in local minima if tie-breaking is not randomized."
    },
    "RandomRestartHillClimbingSolver": {
        "paradigm": "Steepest-Ascent Greedy Search with Stochastic Restarts",
        "completeness": "Incomplete (Bounded by max restarts)",
        "time_complexity": "O(R * S * N^2) (Restarts * Steps * Swaps)",
        "space_complexity": "O(N)",
        "mechanism": (
            "Evaluates the complete pairwise-swap neighborhood (N*(N-1)/2 neighbors). Moves greedily "
            "to the configuration with the lowest objective conflict score. If no neighbor yields "
            "strict improvement (a local plateau/basin), it executes a random restart."
        ),
        "strengths": "Simple and effective for small-to-medium discrete landscapes.",
        "bottlenecks": "Neighborhood evaluations scale quadratically with N; susceptible to flat shoulders."
    },
    "SimulatedAnnealingSolver": {
        "paradigm": "Thermodynamic Metaheuristic Search",
        "completeness": "Asymptotically Complete as T -> 0 slowly",
        "time_complexity": "O(Steps * N)",
        "space_complexity": "O(N)",
        "mechanism": (
            "Simulates cooling metallurgy. Proposes random queen swaps. Downhill (improving) moves "
            "are accepted unconditionally. Uphill (worse) moves are accepted probabilistically based on "
            "the Metropolis criterion P = exp(-delta_E / T), enabling the search to escape local minima."
        ),
        "strengths": "Naturally hops out of local traps; smooth parameter tuning via cooling rate.",
        "bottlenecks": "Sensitive to annealing schedule (initial temperature, cooling factor)."
    },
    "GeneticAlgorithmSolver": {
        "paradigm": "Evolutionary Artificial Intelligence",
        "completeness": "Incomplete / Stochastic",
        "time_complexity": "O(Generations * PopSize * N^2)",
        "space_complexity": "O(PopSize * N)",
        "mechanism": (
            "Maintains a population of chromosome states. Fitness is measured as non-attacking pairs: "
            "Fitness = [N*(N-1)/2] - conflicts. High-fitness candidates are selected via tournament selection, "
            "recombined using single-point crossover, and perturbed via column gene mutations."
        ),
        "strengths": "Explores wide multi-modal regions concurrently without getting stuck in a single basin.",
        "bottlenecks": "High computational overhead per generation due to conflict evaluations across the population."
    },
    "ParticleSwarmOptimizationSolver": {
        "paradigm": "Swarm Intelligence (Continuous/Discrete Hybrid)",
        "completeness": "Incomplete / Stochastic",
        "time_complexity": "O(Iterations * Particles * N^2)",
        "space_complexity": "O(Particles * N)",
        "mechanism": (
            "A flock of candidate particle vectors navigate through the N-dimensional discrete search space. "
            "Particles iteratively update their coordinates influenced by both their personal historical best (cognitive) "
            "and the entire swarm's overall best configuration (social attractor)."
        ),
        "strengths": "Coordinated decentralized exploration; resilient against premature convergence.",
        "bottlenecks": "Velocity damping and discrete coordinate discretization require careful balance."
    }
}


class ChessBoardWindow:
    """
    Renders an interactive, standalone Chess.com-styled GUI window
    featuring modern board theming, high-DPI canvas glyphs, coordinate labels,
    and a complete algorithm analysis panel.
    """
    def __init__(self, solver_name: str, board: List[int], metrics: Dict[str, Any]):
        self.solver_name = solver_name
        self.board = board
        self.n = len(board)
        self.metrics = metrics
        self.dossier = ALGO_ANALYSIS_DATA.get(solver_name, {
            "paradigm": "Heuristic Algorithm",
            "completeness": "Stochastic",
            "time_complexity": "N/A",
            "space_complexity": "O(N)",
            "mechanism": "Custom heuristic search strategy.",
            "strengths": "Modular search solver.",
            "bottlenecks": "Standard combinatorial bounds."
        })

        self.root = tk.Toplevel()
        self.root.title(f"{solver_name} — Safe Placement & Engine Telemetry")
        self.root.configure(bg="#1E1E1E")
        self.root.resizable(False, False)

        # Theme Colors (Modern Dark / Chess.com Olive theme)
        self.LIGHT_SQ = "#EEEED2"
        self.DARK_SQ = "#769656"
        self.PANEL_BG = "#262522"
        self.CARD_BG = "#312E2B"
        self.ACCENT = "#81B64C"
        self.TEXT_MAIN = "#FFFFFF"
        self.TEXT_MUTED = "#BABABA"
        self.THREAT_RAY = "#E74C3C"

        self._build_layout()

    def _build_layout(self):
        container = tk.Frame(self.root, bg="#1E1E1E", padx=15, pady=15)
        container.pack(fill=tk.BOTH, expand=True)

        # Left Column: Chessboard
        left_frame = tk.Frame(container, bg="#1E1E1E")
        left_frame.grid(row=0, column=0, padx=(0, 15), sticky="n")

        # Board Sizing (capped for display)
        self.sq_size = max(55, min(80, 640 // self.n))
        self.board_px = self.n * self.sq_size
        self.margin = 28

        self.canvas = tk.Canvas(
            left_frame,
            width=self.board_px + 2 * self.margin,
            height=self.board_px + 2 * self.margin,
            bg="#21201D",
            highlightthickness=0
        )
        self.canvas.pack()

        # Legend / Status bar below board
        legend_frame = tk.Frame(left_frame, bg="#21201D", pady=6)
        legend_frame.pack(fill=tk.X)
        tk.Label(
            legend_frame,
            text=f"Configuration: {self.board}",
            bg="#21201D",
            fg=self.TEXT_MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w", padx=10)

        # Right Column: Analysis Dashboard
        right_frame = tk.Frame(container, bg=self.PANEL_BG, width=440, padx=20, pady=20)
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.pack_propagate(False)

        self._render_analysis_panel(right_frame)
        self._draw_board()

    def _render_analysis_panel(self, parent: tk.Frame):
        # Algorithm Title
        clean_title = self.solver_name.replace("Solver", "")
        tk.Label(
            parent,
            text=clean_title,
            font=("Segoe UI", 16, "bold"),
            bg=self.PANEL_BG,
            fg=self.ACCENT
        ).pack(anchor="w")

        tk.Label(
            parent,
            text=self.dossier["paradigm"],
            font=("Segoe UI", 9, "italic"),
            bg=self.PANEL_BG,
            fg=self.TEXT_MUTED
        ).pack(anchor="w", pady=(0, 12))

        # Metrics Card
        metrics_card = tk.Frame(parent, bg=self.CARD_BG, padx=12, pady=10)
        metrics_card.pack(fill=tk.X, pady=(0, 12))

        runtime = self.metrics.get("runtime_sec", 0.0)
        iterations = self.metrics.get("iterations", 0)

        self._add_stat_row(metrics_card, "Status", "✓ ZERO CONFLICTS (SOLVED)", self.ACCENT)
        self._add_stat_row(metrics_card, "Execution Time", f"{runtime:.5f} sec", self.TEXT_MAIN)
        self._add_stat_row(metrics_card, "Iterations / Steps", f"{iterations:,}", self.TEXT_MAIN)
        self._add_stat_row(metrics_card, "Board Dimension", f"{self.n} × {self.n} ({self.n**2} squares)", self.TEXT_MAIN)

        # Complexity Card
        comp_card = tk.Frame(parent, bg=self.CARD_BG, padx=12, pady=10)
        comp_card.pack(fill=tk.X, pady=(0, 12))

        self._add_stat_row(comp_card, "Completeness", self.dossier["completeness"], self.TEXT_MAIN)
        self._add_stat_row(comp_card, "Time Complexity", self.dossier["time_complexity"], self.TEXT_MAIN)
        self._add_stat_row(comp_card, "Space Complexity", self.dossier["space_complexity"], self.TEXT_MAIN)

        # Deep Mechanics & Breakdown
        tk.Label(
            parent,
            text="How This Engine Solved It:",
            font=("Segoe UI", 10, "bold"),
            bg=self.PANEL_BG,
            fg=self.TEXT_MAIN
        ).pack(anchor="w", pady=(4, 2))

        tk.Message(
            parent,
            text=self.dossier["mechanism"],
            font=("Segoe UI", 9),
            bg=self.PANEL_BG,
            fg=self.TEXT_MUTED,
            width=400
        ).pack(anchor="w", pady=(0, 8))

        # Key Characteristics / Trade-offs
        tradeoff_frame = tk.Frame(parent, bg=self.CARD_BG, padx=12, pady=8)
        tradeoff_frame.pack(fill=tk.X)

        tk.Label(
            tradeoff_frame,
            text="• Strength: " + self.dossier["strengths"],
            font=("Segoe UI", 8),
            bg=self.CARD_BG,
            fg="#A3E635",
            wraplength=380,
            justify="left"
        ).pack(anchor="w", pady=2)

        tk.Label(
            tradeoff_frame,
            text="• Trade-off: " + self.dossier["bottlenecks"],
            font=("Segoe UI", 8),
            bg=self.CARD_BG,
            fg="#F87171",
            wraplength=380,
            justify="left"
        ).pack(anchor="w", pady=2)

    def _add_stat_row(self, parent: tk.Frame, label: str, val: str, val_color: str):
        row = tk.Frame(parent, bg=self.CARD_BG)
        row.pack(fill=tk.X, pady=2)
        tk.Label(row, text=label, font=("Segoe UI", 9), bg=self.CARD_BG, fg=self.TEXT_MUTED).pack(side=tk.LEFT)
        tk.Label(row, text=val, font=("Segoe UI", 9, "bold"), bg=self.CARD_BG, fg=val_color).pack(side=tk.RIGHT)

    def _draw_board(self):
        # Coordinates (Files: a-z, Ranks: 1-N)
        for i in range(self.n):
            # Files (Bottom)
            file_char = chr(ord('a') + i)
            x = self.margin + i * self.sq_size + self.sq_size / 2
            self.canvas.create_text(
                x, self.board_px + self.margin + 14,
                text=file_char, fill="#8B8987", font=("Segoe UI", 10, "bold")
            )
            # Ranks (Left)
            rank_char = str(self.n - i)
            y = self.margin + i * self.sq_size + self.sq_size / 2
            self.canvas.create_text(
                self.margin - 14, y,
                text=rank_char, fill="#8B8987", font=("Segoe UI", 10, "bold")
            )

        # Chessboard Squares
        for r in range(self.n):
            for c in range(self.n):
                color = self.LIGHT_SQ if (r + c) % 2 == 0 else self.DARK_SQ
                x0 = self.margin + c * self.sq_size
                y0 = self.margin + r * self.sq_size
                x1 = x0 + self.sq_size
                y1 = y0 + self.sq_size

                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

        # Place Queens (Render with soft shadow & vector-like styling)
        piece_font_size = int(self.sq_size * 0.58)
        for col, row in enumerate(self.board):
            cx = self.margin + col * self.sq_size + self.sq_size / 2
            cy = self.margin + row * self.sq_size + self.sq_size / 2

            # Drop shadow
            self.canvas.create_text(
                cx + 2, cy + 2,
                text="♛",
                font=("Arial", piece_font_size),
                fill="#242424"
            )
            # Primary Queen body (Glossy dark graphite piece)
            self.canvas.create_text(
                cx, cy,
                text="♛",
                font=("Arial", piece_font_size),
                fill="#111111"
            )