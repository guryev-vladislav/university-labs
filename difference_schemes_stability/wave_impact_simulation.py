import numpy as np
import matplotlib.pyplot as plt

L = 10.0
c = 1.0
v0 = 2.0
T_end = 7.0
Cr = 0.7
Nx = 100

dx = L / (Nx - 1)
dt = Cr * dx / c
Nt = int(T_end / dt) + 1

x = np.linspace(0, L, Nx)
v_prev = np.zeros(Nx)
v_curr = np.zeros(Nx)
v_next = np.zeros(Nx)

v_curr[:] = 0.0
v_prev[:] = 0.0

print("--- Simulation Setup ---")
print(f"L={L}, T_end={T_end}, c={c}, v0={v0}, Cr={Cr}")
print(f"Grid: Nx={Nx}, Nt={Nt}, dx={dx:.4f}, dt={dt:.4f}")
print("Starting time loop (Cross scheme)...")

for n in range(1, Nt):
    for i in range(1, Nx - 1):
        v_next[i] = (2 * (1 - Cr ** 2) * v_curr[i] +
                     Cr ** 2 * (v_curr[i + 1] + v_curr[i - 1]) -
                     v_prev[i])

    v_next[0] = v0
    v_next[-1] = v_next[-2]

    v_prev[:] = v_curr
    v_curr[:] = v_next

print("Time loop finished. Plotting results...")

plt.figure(figsize=(10, 6))

plt.plot(x, v_curr,
         'b',
         linewidth=2,
         alpha=0.8,
         label=f'Numerical Solution ($t={T_end:.1f}$ s)')

wave_front_position = c * T_end
if wave_front_position < L:
    v_analytical = np.where(x <= wave_front_position, v0, 0.0)

    plt.plot(x, v_analytical,
             'r--',
             linewidth=1.5,
             label='Analytical Solution (Ideal Step)')

    plt.axvline(x=wave_front_position, color='darkred', linestyle=':',
                alpha=0.9, label=f'Wave Front ($x={wave_front_position:.1f}$)')
else:
    plt.plot([0, L], [v0, v_curr[-1]], 'r--', linewidth=1.5,
             label='Analytical Solution ($v=v0$ across the bar)')
    plt.axvline(x=L, color='darkred', linestyle=':', alpha=0.9, label='End of Bar')

plt.grid(True, linestyle='-', which='major', alpha=0.5)
plt.minorticks_on()
plt.grid(True, which='minor', linestyle=':', alpha=0.3)

plt.xlabel('Spatial Coordinate $x$ (Bar Length, m)', fontsize=12)
plt.ylabel('Velocity $v$ (m/s)', fontsize=12)
plt.title(f'Wave Propagation in a Bar (Cross Scheme)\n'
          f'Courant Number $Cr={Cr}$, $\\frac{{c\\cdot dt}}{{dx}} = {Cr}$', fontsize=14)
plt.legend(loc='upper right', fontsize=10)

plt.text(0.98, 0.98,
         rf'$L={L}, c={c}$\n'
         rf'$\Delta x={dx:.4f}, \Delta t={dt:.4f}$\n'
         rf'$v_0={v0}, Cr={Cr}, N_x={Nx}, N_t={Nt}$',
         transform=plt.gca().transAxes,
         fontsize=9,
         verticalalignment='top',
         horizontalalignment='right',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8, edgecolor='gray'))

plt.xlim(0, L)
plt.ylim(min(-0.1, np.min(v_curr)), v0 * 1.2)

plt.tight_layout()
plt.show()

print("--- Simulation Results ---")
print(f"Final velocity at x=L: v({L:.1f}, {T_end:.1f}) = {v_curr[-1]:.4f} m/s")
print(f"Wave front position at T={T_end:.1f}: x_front = {wave_front_position:.2f}")
print("--------------------------")