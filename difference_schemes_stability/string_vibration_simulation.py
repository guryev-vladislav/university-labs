import numpy as np
import matplotlib.pyplot as plt

L = 1.0
T = 2.0
c = 1.0
Nx = 5
dt = 0.1
PI = np.pi

dx = L / (Nx - 1)
Nt = int(T / dt) + 1

r = c * dt / dx

print("--- Simulation Setup ---")
print(f"L={L}, T_end={T}, c={c}")
print(f"Grid: Nx={Nx}, Nt={Nt}, dx={dx:.2f}, dt={dt:.2f}")
print(f"Courant Number: r = {r:.6f}")

x = np.linspace(0, L, Nx)
t = np.linspace(0, T, Nt)
u = np.zeros((Nt, Nx))

for i in range(Nx):
    u[0, i] = np.sin(PI * x[i])

print("Initializing second layer using approximation...")

for i in range(1, Nx - 1):
    u[1, i] = u[0, i] + 0.5 * r ** 2 * (u[0, i + 1] - 2 * u[0, i] + u[0, i - 1])

u[1, 0] = 0
u[1, -1] = 0

print(f"Starting time loop (Cross scheme) for {Nt - 2} steps...")

for n in range(1, Nt - 1):
    for i in range(1, Nx - 1):
        u[n + 1, i] = (r ** 2 * (u[n, i + 1] + u[n, i - 1]) +
                       2 * (1 - r ** 2) * u[n, i] - u[n - 1, i])

    u[n + 1, 0] = 0
    u[n + 1, -1] = 0

print("Time loop finished. Plotting selected states...")

steps_to_plot = [0, Nt // 2, Nt - 1]
if Nt < 4:
    steps_to_plot = list(range(Nt))

plt.figure(figsize=(10, 7))
plt.style.use('seaborn-v0_8-darkgrid')

styles = [
    ('k--', 1.5, 'Initial State ($t={:.3f}$ s)'),  # 'o' убран
    ('r-', 1.0, 'Intermediate State ($t={:.3f}$ s)'),  # '-o' заменен на '-'
    ('b-', 2.5, 'Final State ($t={:.3f}$ s)')  # '-'
]

for k, n in enumerate(steps_to_plot):
    style_index = k if k < len(styles) else len(styles) - 1

    line_style, line_width, label_template = styles[style_index]

    plt.plot(x, u[n, :],
             line_style,
             linewidth=line_width,
             marker=('o' if k == 0 or k == len(steps_to_plot) - 1 else '^'),
             markersize=5,
             label=label_template.format(t[n]))

plt.title(f'String Vibration Simulation (Cross Scheme, $r={r:.2f}$)\n'
          r'Initial Condition $u(x,0) = \sin(\pi x)$',
          fontsize=14,
          fontweight='bold')
plt.xlabel('Coordinate $x$ (m)', fontsize=12)
plt.ylabel('Displacement $u(x,t)$ (m)', fontsize=12)

plt.grid(True, linestyle=':', alpha=0.6)
plt.axhline(y=0, color='gray', linestyle='-', alpha=0.5)

plt.ylim(-1.1 * np.max(np.abs(u)), 1.1 * np.max(np.abs(u)))
plt.xlim(0, L)

plt.legend(loc='lower right', fontsize=10, shadow=True)

plt.text(0.98, 0.98,
         rf'$L={L}, c={c}$\n'
         rf'$\Delta x={dx:.2f}, \Delta t={dt:.2f}$\n'
         rf'$N_x={Nx}, N_t={Nt}$',
         transform=plt.gca().transAxes,
         fontsize=10,
         verticalalignment='top',
         horizontalalignment='right',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8, edgecolor='gray'))

plt.tight_layout()
plt.show()

print("--- Simulation Results ---")
print(f"Maximum amplitude achieved: {np.max(np.abs(u)):.4f} m")
print(f"Final time: T = {t[-1]:.3f} s")
print("--------------------------")