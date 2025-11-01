import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import logging
from typing import Dict, Any
import os
import json
import time
from datetime import datetime

from .visualization.plotter import SolutionPlotter
from .analytics.analyzer import SolutionAnalyzer

logger = logging.getLogger(__name__)

class SolverInterface:
    def __init__(self, root):
        self.root = root
        self.plotter = SolutionPlotter()
        self.analyzer = SolutionAnalyzer()
        self.current_solution = None
        self.current_problem_type = None

        self.setup_logging()
        self.create_widgets()
        self.setup_core_bindings()

        # Create results directory in project root
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.results_dir = os.path.join(project_root, "results")
        os.makedirs(self.results_dir, exist_ok=True)
        logger.info(f"Results directory: {self.results_dir}")

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)

    def setup_core_bindings(self):
        try:
            from runge_kutta_core import (
                SolverParameters, create_task1_solver,
                create_test_solver, create_second_order_solver
            )
            self.SolverParameters = SolverParameters
            self.create_task1_solver = create_task1_solver
            self.create_test_solver = create_test_solver
            self.create_second_order_solver = create_second_order_solver
            self.core_available = True
            logger.info("C++ core successfully loaded")
        except ImportError as e:
            logger.error(f"C++ core not available: {e}")
            self.core_available = False
            messagebox.showwarning("Warning", "C++ core not available. Using demo mode.")

    def create_widgets(self):
        self.root.title("Runge-Kutta Suite")
        self.root.geometry("1400x900")

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        self.create_control_frame(main_frame)
        self.create_plot_frame(main_frame)
        self.create_output_frame(main_frame)

    def create_control_frame(self, parent):
        control_frame = ttk.LabelFrame(parent, text="Solver Controls", padding="10")
        control_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(control_frame, text="Problem Type:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.problem_var = tk.StringVar(value="task1")
        problem_combo = ttk.Combobox(control_frame, textvariable=self.problem_var,
                                     values=["task1", "test", "task2"], state="readonly")
        problem_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        problem_combo.bind('<<ComboboxSelected>>', self.on_problem_change)

        self.param_frame = ttk.Frame(control_frame)
        self.param_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))

        self.create_parameter_fields()

        # Button frame with centered buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=(15, 5), sticky=(tk.W, tk.E))

        solve_button = ttk.Button(button_frame, text="Solve", command=self.solve_problem)
        solve_button.pack(side=tk.LEFT, padx=(0, 10))

        clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_solution)
        clear_button.pack(side=tk.LEFT, padx=(0, 10))

        save_button = ttk.Button(button_frame, text="Save Results", command=self.save_results)
        save_button.pack(side=tk.LEFT)

        # Center the button frame
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(3, weight=1)

        control_frame.columnconfigure(1, weight=1)

    def create_parameter_fields(self):
        for widget in self.param_frame.winfo_children():
            widget.destroy()

        problem_type = self.problem_var.get()

        self.parameters = {}
        row = 0

        common_params = [
            ("steps", "Number of steps", "1000"),
            ("tolerance", "Tolerance", "1e-6"),
            ("right_boundary", "Right boundary", "1.0"),
            ("initial_value", "Initial value u(0)", "1.0"),
        ]

        for param_id, label, default in common_params:
            ttk.Label(self.param_frame, text=label).grid(row=row, column=0, sticky=tk.W, padx=(0, 10))
            var = tk.StringVar(value=default)
            entry = ttk.Entry(self.param_frame, textvariable=var, width=15)
            entry.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
            self.parameters[param_id] = var
            row += 1

        if problem_type == "task2":
            ttk.Label(self.param_frame, text="Initial derivative u'(0)").grid(row=row, column=0, sticky=tk.W, padx=(0, 10))
            var = tk.StringVar(value="0.0")
            entry = ttk.Entry(self.param_frame, textvariable=var, width=15)
            entry.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
            self.parameters["initial_derivative"] = var
            row += 1

            ttk.Label(self.param_frame, text="Parameter a").grid(row=row, column=0, sticky=tk.W, padx=(0, 10))
            var = tk.StringVar(value="1.0")
            entry = ttk.Entry(self.param_frame, textvariable=var, width=15)
            entry.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
            self.parameters["param_a"] = var
            row += 1

            ttk.Label(self.param_frame, text="Parameter b").grid(row=row, column=0, sticky=tk.W, padx=(0, 10))
            var = tk.StringVar(value="1.0")
            entry = ttk.Entry(self.param_frame, textvariable=var, width=15)
            entry.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
            self.parameters["param_b"] = var

        self.param_frame.columnconfigure(1, weight=1)

    def create_plot_frame(self, parent):
        plot_frame = ttk.LabelFrame(parent, text="Solution Visualization", padding="5")
        plot_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        plot_frame.columnconfigure(0, weight=1)
        plot_frame.rowconfigure(0, weight=1)

        self.plot_container = self.plotter.create_plot_frame(plot_frame)
        self.plot_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    def create_output_frame(self, parent):
        output_frame = ttk.LabelFrame(parent, text="Analysis Output", padding="5")
        output_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)

        self.output_text = scrolledtext.ScrolledText(output_frame, width=40, height=20)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    def on_problem_change(self, event=None):
        self.create_parameter_fields()

    def get_parameters(self) -> Dict[str, Any]:
        params = {}
        problem_type = self.problem_var.get()

        try:
            params['steps'] = int(self.parameters['steps'].get())
            params['tolerance'] = float(self.parameters['tolerance'].get())
            params['right_boundary'] = float(self.parameters['right_boundary'].get())
            params['initial_value'] = float(self.parameters['initial_value'].get())

            if problem_type == "task2":
                params['initial_derivative'] = float(self.parameters['initial_derivative'].get())
                params['param_a'] = float(self.parameters['param_a'].get())
                params['param_b'] = float(self.parameters['param_b'].get())

            return params

        except ValueError as e:
            logger.error(f"Parameter conversion error: {e}")
            raise ValueError("Invalid parameter values. Please check your inputs.")

    def solve_problem(self):
        try:
            problem_type = self.problem_var.get()
            params = self.get_parameters()

            self.output_text.insert(tk.END, f"Solving {problem_type}...\n")
            self.output_text.see(tk.END)
            self.root.update()

            if not self.core_available:
                solution_data = self._get_demo_solution(problem_type, params)
            else:
                solution_data = self._solve_with_core(problem_type, params)

            self.current_solution = solution_data
            self.current_problem_type = problem_type

            self.analyzer.set_solution_data(solution_data, problem_type)
            self.plotter.plot_solution(solution_data, problem_type)

            report = self.analyzer.generate_report()
            self.output_text.insert(tk.END, f"\n{report}\n")
            self.output_text.insert(tk.END, "-" * 50 + "\n")
            self.output_text.see(tk.END)

            logger.info(f"Successfully solved {problem_type}")

        except Exception as e:
            logger.error(f"Solution error: {e}")
            messagebox.showerror("Error", f"Failed to solve problem: {str(e)}")

    def _solve_with_core(self, problem_type: str, parameters: dict) -> list:
        params_obj = self.SolverParameters()
        params_obj.steps = parameters['steps']
        params_obj.tolerance = parameters['tolerance']
        params_obj.right_boundary = parameters['right_boundary']
        params_obj.initial_value = parameters['initial_value']

        if problem_type == "task1":
            solver = self.create_task1_solver(params_obj)
        elif problem_type == "test":
            solver = self.create_test_solver(params_obj)
        elif problem_type == "task2":
            params_obj.initial_derivative = parameters['initial_derivative']
            params_obj.param_a = parameters['param_a']
            params_obj.param_b = parameters['param_b']
            solver = self.create_second_order_solver(params_obj)
        else:
            raise ValueError(f"Unknown problem type: {problem_type}")

        solution_points = solver.solve()

        solution_data = []
        for point in solution_points:
            data_point = {
                'x': point.x,
                'u': point.u,
                'u1': point.u1,
                'error_estimate': point.error_estimate,
                'step_size': point.step_size,
                'step_reductions': point.step_reductions,
                'step_increases': point.step_increases
            }
            solution_data.append(data_point)

        return solution_data

    def _get_demo_solution(self, problem_type: str, parameters: dict) -> list:
        import numpy as np

        x_end = parameters['right_boundary']
        n_steps = parameters['steps']
        u0 = parameters['initial_value']

        x_vals = np.linspace(0, x_end, n_steps)

        if problem_type == "test":
            u_vals = u0 * np.exp(x_vals)
        elif problem_type == "task1":
            u_vals = u0 * np.exp(x_vals) * np.sin(10 * x_vals)
        else:
            u_vals = u0 * np.sin(5 * x_vals)

        solution_data = []
        for i, x in enumerate(x_vals):
            solution_data.append({
                'x': x,
                'u': u_vals[i],
                'u1': 0.0,
                'error_estimate': 0.0,
                'step_size': x_end / n_steps,
                'step_reductions': 0,
                'step_increases': 0
            })

        return solution_data

    def save_results(self):
        if not self.current_solution:
            messagebox.showwarning("Warning", "No solution to save. Please solve a problem first.")
            return

        try:
            # Create timestamp and folder name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            folder_name = f"{self.current_problem_type}_{timestamp}"
            save_path = os.path.join(self.results_dir, folder_name)
            os.makedirs(save_path, exist_ok=True)

            # Save solution data as JSON
            solution_file = os.path.join(save_path, "solution_data.json")
            with open(solution_file, 'w') as f:
                json.dump({
                    'problem_type': self.current_problem_type,
                    'parameters': self.get_parameters(),
                    'solution': self.current_solution
                }, f, indent=2)

            # Save analysis report
            report_file = os.path.join(save_path, "analysis_report.txt")
            with open(report_file, 'w') as f:
                f.write(self.analyzer.generate_report())

            # Save plot
            plot_file = os.path.join(save_path, "solution_plot.png")
            if self.plotter.fig:
                self.plotter.fig.savefig(plot_file, dpi=150, bbox_inches='tight')

            self.output_text.insert(tk.END, f"Results saved to: {save_path}\n")
            self.output_text.see(tk.END)
            logger.info(f"Results saved to {save_path}")
            messagebox.showinfo("Success", f"Results saved to:\n{save_path}")

        except Exception as e:
            logger.error(f"Save error: {e}")
            messagebox.showerror("Error", f"Failed to save results: {str(e)}")

    def clear_solution(self):
        self.plotter.clear_plot()
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Output cleared.\n")
        self.current_solution = None
        self.current_problem_type = None