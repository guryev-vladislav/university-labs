// core/solvers/finite_difference_solver.h
#ifndef FINITE_DIFFERENCE_SOLVER_H
#define FINITE_DIFFERENCE_SOLVER_H

#include "differential_coefficients.h"
#include "tridiagonal_solver.h"
#include <vector>

class finite_difference_solver {
private:
    double left_boundary;
    double right_boundary;

public:
    finite_difference_solver(double left_bc = 0.0, double right_bc = 1.0);

    std::vector<double> solve(const differential_coefficients& problem, int nodes);
    std::vector<double> solve_double_grid(const differential_coefficients& problem, int nodes);
};

#endif