# Difference Schemes Stability Analysis (Анализ устойчивости разностных схем)

Numerical modeling and stability analysis of hyperbolic partial differential equations (PDEs) using the Finite Difference Method (FDM).

## Project Goal

Development of computational software to simulate wave propagation and string vibration problems, focusing on the stability of explicit finite difference schemes (Cross scheme) based on the Courant–Friedrichs–Lewy (CFL) condition.

## Tech Stack & Methodology

* **Python 3.14.2** - Core language for implementation and analysis.
* **Finite Difference Method (FDM)** - Numerical discretization of the wave equation (hyperbolic PDE).
* **Cross Scheme (Explicit)** - The specific three-layer scheme used for time stepping.
* **Courant Number ($r$ or $Cr$)** - Key stability parameter for the analysis.
* **NumPy** - High-performance array processing for numerical calculations.
* **Matplotlib** - Scientific visualization and plotting of spatial solutions.
* **Clear Parameter Blocks** - Configuration parameters are consolidated at the top of each script for easy modification and analysis.

## Project Structure

The repository contains scripts demonstrating two classic problems solved using the Cross scheme.

| File | Description | Stability Parameter |
| :--- | :--- | :--- |
| `wave_impact_simulation.py` | Models the impact of a moving wall ($v_0$) on a stationary bar. | Courant Number ($Cr$) |
| `string_vibration_simulation.py` | Models the initial sine deflection of a fixed-end vibrating string. | Courant Number ($r$) |

## Quick Start (Running Simulations)

### 1. Requirements

Make sure you have Python 3 and the necessary libraries installed:

```bash
pip install numpy matplotlib