from typing import List, Dict
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import tkinter as tk
from .gui_visualizer import ChessBoardWindow

class Visualizer:
    @staticmethod
    def print_board(board: List[int], solver_name: str = "") -> None:
        n = len(board)
        header = f"=== {solver_name} Solution ({n}x{n}) ==="
        print("\n" + header)
        print("    " + "   ".join([chr(ord('a') + i) for i in range(n)]))
        print("  +" + "---+" * n)
        for r in range(n):
            row_str = f"{n - r} |"
            for c in range(n):
                row_str += " ♛ |" if board[c] == r else "   |"
            print(row_str + f" {n - r}")
            print("  +" + "---+" * n)
        print("    " + "   ".join([chr(ord('a') + i) for i in range(n)]))
        print("State Vector [col -> row]: " + str(board))

    @staticmethod
    def open_chess_window(solver_name: str, board: List[int], metrics: dict) -> None:
        """Launches the dedicated Chess.com styled GUI window."""
        ChessBoardWindow(solver_name, board, metrics)

    @staticmethod
    def plot_board(board: List[int], solver_name: str, filename: str = "solution.png") -> None:
        n = len(board)
        fig, ax = plt.subplots(figsize=(8, 8), dpi=300)

        light_square = "#F0D9B5"
        dark_square = "#B58863"
        border_color = "#3E2723"

        for r in range(n):
            for c in range(n):
                color = light_square if (r + c) % 2 == 0 else dark_square
                rect = patches.Rectangle((c, n - 1 - r), 1, 1, facecolor=color, edgecolor="none")
                ax.add_patch(rect)

        for col, row in enumerate(board):
            display_row = n - 1 - row
            ax.text(col + 0.52, display_row + 0.48, "♛", fontsize=min(32, int(220 / n)),
                    ha="center", va="center", color="#202020", alpha=0.35, fontfamily="DejaVu Sans")
            ax.text(col + 0.50, display_row + 0.50, "♛", fontsize=min(32, int(220 / n)),
                    ha="center", va="center", color="#111111", fontfamily="DejaVu Sans")

        ax.set_xlim(0, n)
        ax.set_ylim(0, n)
        ax.set_aspect("equal")

        ax.set_xticks([i + 0.5 for i in range(n)])
        ax.set_xticklabels([chr(ord('a') + i) for i in range(n)], fontsize=12, fontweight="bold", color="#3E2723")
        ax.set_yticks([i + 0.5 for i in range(n)])
        ax.set_yticklabels([str(i + 1) for i in range(n)], fontsize=12, fontweight="bold", color="#3E2723")

        for spine in ax.spines.values():
            spine.set_edgecolor(border_color)
            spine.set_linewidth(4)

        ax.tick_params(length=0)
        ax.set_title(f"{solver_name} — Safe Placement (N={n})", fontsize=15, fontweight="bold", pad=15, color="#212121")

        plt.tight_layout()
        plt.savefig(filename, dpi=300)
        plt.close()
        print(f"[Visualizer] High-res board saved to: {filename}")

    @staticmethod
    def plot_comparison_chart(results: Dict[str, dict], filename: str = "benchmark.png") -> None:
        names = list(results.keys())
        runtimes = [results[k]["runtime_sec"] for k in names]
        steps = [results[k]["iterations"] for k in names]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), dpi=300)
        colors = ["#2b5c8f", "#d95f02", "#7570b3", "#e7298a", "#66a61e", "#e6ab02"]

        ax1.barh(names, runtimes, color=colors[:len(names)], edgecolor="#333333")
        ax1.set_xlabel("Runtime (seconds)", fontweight="bold")
        ax1.set_title("Execution Time (Lower is Better)", fontweight="bold")
        ax1.grid(axis="x", linestyle="--", alpha=0.6)

        ax2.barh(names, steps, color=colors[:len(names)], edgecolor="#333333")
        ax2.set_xlabel("Steps / Iterations / Generations", fontweight="bold")
        ax2.set_title("Search Depth / Iterations Explored", fontweight="bold")
        ax2.grid(axis="x", linestyle="--", alpha=0.6)

        plt.suptitle("N-Queens Algorithm Comparative Benchmark", fontsize=16, fontweight="bold", y=1.02)
        plt.tight_layout()
        plt.savefig(filename, dpi=300)
        plt.close()
        print(f"[Visualizer] Benchmark metrics chart saved to: {filename}")