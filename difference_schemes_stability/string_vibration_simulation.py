import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def solve_vibration_cross_scheme(L, T_end, c, Nx, r):
    PI = np.pi
    dx = L / (Nx - 1)

    if c == 0:
        logger.error("Wave speed 'c' cannot be zero.")
        return None, None, None, None, None

    dt = r * dx / c

    if dt <= 0:
        logger.error("Time step dt must be greater than zero.")
        return None, None, None, None, None

    Nt = int(T_end / dt) + 1

    if r > 1.0:
        logger.warning(f"Courant Number r={r:.4f} > 1. The scheme might be unstable.")
    else:
        logger.info(f"Courant Number: r={r:.4f}. The scheme is stable.")

    x = np.linspace(0, L, Nx)
    t = np.linspace(0, T_end, Nt)
    u = np.zeros((Nt, Nx))

    for i in range(Nx):
        u[0, i] = np.sin(PI * x[i])

    for i in range(1, Nx - 1):
        u[1, i] = u[0, i] + 0.5 * r ** 2 * (u[0, i + 1] - 2 * u[0, i] + u[0, i - 1])
    u[1, 0] = 0
    u[1, -1] = 0

    for n in range(1, Nt - 1):
        for i in range(1, Nx - 1):
            u[n + 1, i] = (r ** 2 * (u[n, i + 1] + u[n, i - 1]) +
                           2 * (1 - r ** 2) * u[n, i] - u[n - 1, i])

        u[n + 1, 0] = 0
        u[n + 1, -1] = 0

    return x, t, u, r, dt

class VibrationSolverApp:
    def __init__(self, master):
        self.master = master
        master.title("String Vibration Simulation ('Cross' Scheme)")

        self.u_solution = None
        self.t_points = None
        self.x_points = None
        self.r_cfl = None

        self._create_widgets()

    def _create_widgets(self):
        params_frame = ttk.LabelFrame(self.master, text="Simulation Parameters")
        params_frame.pack(padx=10, pady=10, fill="x")

        self.vars = {
            "L": {"label": "String Length L (m):", "value": tk.DoubleVar(value=1.0)},
            "T": {"label": "End Time T (s):", "value": tk.DoubleVar(value=2.0)},
            "c": {"label": "Wave Speed c (m/s):", "value": tk.DoubleVar(value=1.0)},
            "Nx": {"label": "Space Steps Nx:", "value": tk.IntVar(value=21)},
            "Cr": {"label": "Courant Number r:", "value": tk.DoubleVar(value=0.8)},
        }

        row = 0
        for key, config in self.vars.items():
            ttk.Label(params_frame, text=config["label"]).grid(row=row, column=0, padx=5, pady=2, sticky="w")
            ttk.Entry(params_frame, textvariable=config["value"], width=10).grid(row=row, column=1, padx=5, pady=2,
                                                                                 sticky="e")
            row += 1

        ttk.Button(params_frame, text="Run Simulation", command=self.run_simulation).grid(row=row, column=0,
                                                                                          columnspan=2, pady=10)

        plot_frame = ttk.Frame(self.master)
        plot_frame.pack(padx=10, pady=5, fill="both", expand=True)

        self.fig, self.ax = plt.subplots(figsize=(10, 5))
        self.line, = self.ax.plot([], [], 'r-', linewidth=2, marker='o', markersize=5)
        self.ax.set_ylim(-1.1, 1.1)
        self.ax.set_xlim(0, 1.0)
        self.ax.set_xlabel("Coordinate x (m)")
        self.ax.set_ylabel("Displacement u(x, t) (m)")
        self.plot_title = self.ax.set_title("Press 'Run Simulation'")
        self.ax.grid(True)

        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        control_frame = ttk.LabelFrame(self.master, text="Time Navigation")
        control_frame.pack(padx=10, pady=10, fill="x")

        self.time_step_var = tk.IntVar(value=0)
        self.time_slider = ttk.Scale(control_frame, from_=0, to=1, orient=tk.HORIZONTAL,
                                     command=self.update_plot_from_slider, variable=self.time_step_var,
                                     state=tk.DISABLED)
        self.time_slider.pack(fill="x", padx=10, pady=5)

        self.time_label = ttk.Label(control_frame, text="t = 0.0000 s / Step 0")
        self.time_label.pack(pady=5)

        self.cfl_label = ttk.Label(control_frame, text="r = N/A | dt = N/A")
        self.cfl_label.pack(pady=5)

    def run_simulation(self):
        try:
            L = self.vars["L"]["value"].get()
            T_end = self.vars["T"]["value"].get()
            c = self.vars["c"]["value"].get()
            Nx = self.vars["Nx"]["value"].get()
            r = self.vars["Cr"]["value"].get()

            if Nx < 3 or r <= 0:
                raise ValueError("Nx must be >= 3 and Courant Number r > 0.")

            logger.info("--- Simulation Setup ---")
            logger.info(f"L={L}, T_end={T_end}, c={c}, Nx={Nx}, r={r}")
            logger.info("Starting time loop...")

            self.x_points, self.t_points, self.u_solution, self.r_cfl, dt_calc = \
                solve_vibration_cross_scheme(L, T_end, c, Nx, r)

            if self.u_solution is None:
                self.time_slider.config(state=tk.DISABLED)
                return

            Nt = len(self.t_points)

            self.time_step_var.set(0)
            self.time_slider.config(to=Nt - 1, state=tk.NORMAL)
            self.ax.set_xlim(0, L)

            max_amp = np.max(np.abs(self.u_solution))
            self.ax.set_ylim(-1.1 * max_amp, 1.1 * max_amp)

            self.cfl_label.config(text=f"r = {self.r_cfl:.4f} (Stability: r ≤ 1) | dt = {dt_calc:.6f} s")

            self.update_plot(0)

            logger.info(f"Simulation finished. Total steps: {Nt - 1}.")

        except Exception as e:
            messagebox.showerror("Simulation Error", f"An error occurred: {e}")
            self.time_slider.config(state=tk.DISABLED)

    def update_plot_from_slider(self, val):
        if self.u_solution is not None:
            step = int(float(val))
            self.update_plot(step)

    def update_plot(self, step):
        if self.u_solution is not None:
            self.line.set_data(self.x_points, self.u_solution[step, :])

            current_time = self.t_points[step]
            self.plot_title.set_text(f"String Vibration ('Cross' Scheme)")
            self.time_label.config(text=f"t = {current_time:.4f} s / Step {step} of {len(self.t_points) - 1}")

            self.canvas.draw()

if __name__ == "__main__":
    plt.ion()
    root = tk.Tk()
    app = VibrationSolverApp(root)
    root.mainloop()