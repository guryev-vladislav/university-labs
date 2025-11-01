# Runge-Kutta Suite

A sophisticated numerical computing environment designed for solving systems of ordinary differential equations (ODEs) using state-of-the-art adaptive Runge-Kutta algorithms. The system architecture separates high-performance C++ computational engines from Python-based visualization and control layers, providing optimal efficiency while maintaining user accessibility.

Key capabilities include dynamic step-size control based on local error estimation, support for both first and second-order differential systems, and comprehensive solution analysis with convergence monitoring. The platform serves as both a practical tool for computational mathematics and an educational resource for understanding numerical methods in differential equations.
## Features

- **Adaptive Step Control**: Automatic step size adjustment for optimal accuracy and performance
- **Multiple Problem Types**:
    - First-order ODEs with custom functions
    - Second-order systems with configurable parameters
    - Test cases for validation
- **Real-time Visualization**: Live plotting of solutions, errors, and step size evolution
- **Performance Analytics**: Detailed statistics and convergence analysis
- **Export Results**: Save solutions, plots, and reports with timestamps

## Tech Stack

- **C++17** - high-performance computational core
- **Runge-Kutta Methods** - 4th order numerical integration with adaptive step control
- **PyBind11** - C++/Python interoperability
- **Python 3** - graphical interface and analytics
- **Tkinter** - desktop application framework
- **Matplotlib** - scientific visualization
- **CMake** - cross-platform build system

### Build & Run

```bash
# One-command build and launch
./run-app.sh
