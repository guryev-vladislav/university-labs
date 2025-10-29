// core/solvers/finite_difference_solver.cpp
#include "finite_difference_solver.h"
#include "../common/math_utils.h"

finite_difference_solver::finite_difference_solver(double left_bc, double right_bc)
    : left_boundary(left_bc), right_boundary(right_bc) {}

std::vector<double> finite_difference_solver::solve(const differential_coefficients& problem, int nodes) {
    math_utils::check_positive(nodes - 1, "Number of intervals");

    std::vector<double> a(nodes), b(nodes), c(nodes), phi(nodes);
    double h = 1.0 / (nodes - 1);

    // Граничные условия
    c[0] = 1.0;
    a[0] = 0.0;
    b[0] = 0.0;
    phi[0] = left_boundary;

    c[nodes - 1] = 1.0;
    a[nodes - 1] = 0.0;
    b[nodes - 1] = 0.0;
    phi[nodes - 1] = right_boundary;

    // Внутренние узлы
    double x = h;
    for (int i = 1; i < nodes - 1; i++) {
        double a_coef = problem.effective_conductivity(x, h) / (h * h);
        double d_coef = problem.effective_reaction(x, h);
        double phi_coef = problem.effective_source(x, h);

        a[i] = a_coef;
        c[i] = -((problem.effective_conductivity(x, h) + problem.effective_conductivity(x + h, h)) / (h * h) + d_coef);
        b[i] = problem.effective_conductivity(x + h, h) / (h * h);
        phi[i] = -phi_coef;

        x += h;
    }

    tridiagonal_solver solver(nodes);
    solver.solve(a, b, c, phi);
    return solver.get_solution();
}

std::vector<double> finite_difference_solver::solve_double_grid(const differential_coefficients& problem, int nodes) {
    int double_nodes = nodes * 2 - 1;
    return solve(problem, double_nodes);
}