import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class SolutionPlotter:
    def __init__(self):
        self.fig = None
        self.canvas = None

    def create_plot_frame(self, parent):
        frame = tk.Frame(parent)
        self.fig = plt.Figure(figsize=(10, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        return frame

    def plot_solution(self, solution_data: List[Dict[str, Any]], system_type: str):
        if not self.fig:
            logger.error("Plot figure not initialized")
            return

        self.fig.clear()

        if system_type == "task2":
            self._plot_second_order_solution(solution_data)
        else:
            self._plot_first_order_solution(solution_data)

        self.canvas.draw()

    def _plot_first_order_solution(self, solution_data: List[Dict[str, Any]]):
        x_vals = [point['x'] for point in solution_data]
        u_vals = [point['u'] for point in solution_data]
        step_sizes = [point['step_size'] for point in solution_data]
        error_estimates = [point['error_estimate'] for point in solution_data]

        ax1 = self.fig.add_subplot(221)
        ax1.plot(x_vals, u_vals, 'b-', linewidth=2)
        ax1.set_xlabel('x')
        ax1.set_ylabel('u(x)')
        ax1.set_title('Solution')
        ax1.grid(True)

        ax2 = self.fig.add_subplot(222)
        if any(h > 0 for h in step_sizes[1:]):
            ax2.semilogy(x_vals[1:], step_sizes[1:], 'g-', linewidth=2)
        else:
            ax2.plot(x_vals[1:], step_sizes[1:], 'g-', linewidth=2)
        ax2.set_xlabel('x')
        ax2.set_ylabel('Step size')
        ax2.set_title('Adaptive Step Size')
        ax2.grid(True)

        ax3 = self.fig.add_subplot(223)
        error_vals = [abs(e) for e in error_estimates[1:] if e != 0]
        if error_vals and any(e > 0 for e in error_vals):
            ax3.semilogy(x_vals[1:len(error_vals)+1], error_vals, 'r-', linewidth=2)
        else:
            ax3.plot(x_vals[1:], [abs(e) for e in error_estimates[1:]], 'r-', linewidth=2)
        ax3.set_xlabel('x')
        ax3.set_ylabel('Error estimate')
        ax3.set_title('Error Estimation')
        ax3.grid(True)

        ax4 = self.fig.add_subplot(224)
        reductions = [point['step_reductions'] for point in solution_data[1:]]
        increases = [point['step_increases'] for point in solution_data[1:]]
        x_reductions = x_vals[1:]
        ax4.plot(x_reductions, reductions, 'ro-', label='Reductions', markersize=4)
        ax4.plot(x_reductions, increases, 'go-', label='Increases', markersize=4)
        ax4.set_xlabel('x')
        ax4.set_ylabel('Step adjustments')
        ax4.set_title('Step Adjustments')
        ax4.legend()
        ax4.grid(True)

        self.fig.tight_layout()

    def _plot_second_order_solution(self, solution_data: List[Dict[str, Any]]):
        x_vals = [point['x'] for point in solution_data]
        u_vals = [point['u'] for point in solution_data]
        u1_vals = [point['u1'] for point in solution_data]
        step_sizes = [point['step_size'] for point in solution_data]

        ax1 = self.fig.add_subplot(221)
        ax1.plot(x_vals, u_vals, 'b-', linewidth=2, label='u(x)')
        ax1.plot(x_vals, u1_vals, 'r-', linewidth=2, label="u'(x)")
        ax1.set_xlabel('x')
        ax1.set_ylabel('Values')
        ax1.set_title('Solution and Derivative')
        ax1.legend()
        ax1.grid(True)

        ax2 = self.fig.add_subplot(222)
        ax2.plot(u_vals, u1_vals, 'purple', linewidth=2)
        ax2.set_xlabel('u')
        ax2.set_ylabel("u'")
        ax2.set_title('Phase Portrait')
        ax2.grid(True)

        ax3 = self.fig.add_subplot(223)
        if any(h > 0 for h in step_sizes[1:]):
            ax3.semilogy(x_vals[1:], step_sizes[1:], 'g-', linewidth=2)
        else:
            ax3.plot(x_vals[1:], step_sizes[1:], 'g-', linewidth=2)
        ax3.set_xlabel('x')
        ax3.set_ylabel('Step size')
        ax3.set_title('Adaptive Step Size')
        ax3.grid(True)

        ax4 = self.fig.add_subplot(224)
        reductions = [point['step_reductions'] for point in solution_data[1:]]
        increases = [point['step_increases'] for point in solution_data[1:]]
        x_reductions = x_vals[1:]
        ax4.plot(x_reductions, reductions, 'ro-', label='Reductions', markersize=4)
        ax4.plot(x_reductions, increases, 'go-', label='Increases', markersize=4)
        ax4.set_xlabel('x')
        ax4.set_ylabel('Step adjustments')
        ax4.set_title('Step Adjustments')
        ax4.legend()
        ax4.grid(True)

        self.fig.tight_layout()

    def clear_plot(self):
        if self.fig:
            self.fig.clear()
            if self.canvas:
                self.canvas.draw()