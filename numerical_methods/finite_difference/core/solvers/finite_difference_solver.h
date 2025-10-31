// core/solvers/finite_difference_solver.h
#ifndef FINITE_DIFFERENCE_SOLVER_H
#define FINITE_DIFFERENCE_SOLVER_H

#include "differential_coefficients.h"
#include "tridiagonal_solver.h"
#include <vector>
#include <stdexcept>

class FiniteDifferenceSolver {
private:
    double left_boundary = 0.0;
    double right_boundary = 1.0;

public:
    FiniteDifferenceSolver(double leftBC = 0.0, double rightBC = 1.0)
        : left_boundary(leftBC), right_boundary(rightBC) {}

    std::vector<double> solve(const DifferentialCoefficients& problem, int nodes) {
        if (nodes < 3) {
            throw std::invalid_argument("Number of nodes must be at least 3");
        }

        std::vector<double> A(nodes), B(nodes), C(nodes), Phi(nodes);
        double h = 1.0 / (nodes - 1);

        // Граничные условия
        C[0] = 1.0;
        A[0] = 0.0;
        B[0] = 0.0;
        Phi[0] = left_boundary;

        C[nodes - 1] = 1.0;
        A[nodes - 1] = 0.0;
        B[nodes - 1] = 0.0;
        Phi[nodes - 1] = right_boundary;

        // Внутренние узлы
        double x = h;
        for (int i = 1; i < nodes - 1; i++) {
            double a_coef = problem.effective_conductivity(x, h) / (h * h);
            double d_coef = problem.effective_reaction(x, h);
            double phi_coef = problem.effective_source(x, h);

            A[i] = a_coef;
            C[i] = -((problem.effective_conductivity(x, h) + problem.effective_conductivity(x + h, h)) / (h * h) + d_coef);
            B[i] = problem.effective_conductivity(x + h, h) / (h * h);
            Phi[i] = -phi_coef;

            x += h;
        }

        TridiagonalSolver solver(nodes);
        solver.solve(A, B, C, Phi);
        return solver.get_solution();
    }

    std::vector<double> solve_double_grid(const DifferentialCoefficients& problem, int nodes) {
        int double_nodes = nodes * 2 - 1;
        return solve(problem, double_nodes);
    }
};

#endif