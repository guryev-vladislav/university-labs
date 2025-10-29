// core/solvers/tridiagonal_solver.h
#ifndef TRIDIAGONAL_SOLVER_H
#define TRIDIAGONAL_SOLVER_H

#include <vector>
#include <stdexcept>
#include <cmath>

class tridiagonal_solver {
private:
    int nodes;
    std::vector<double> v;
    std::vector<double> alpha;
    std::vector<double> beta;

    void normalize_system();
    void forward_sweep(const std::vector<double>& a, const std::vector<double>& b,
                      const std::vector<double>& c, const std::vector<double>& phi);
    void backward_sweep(const std::vector<double>& a, const std::vector<double>& c,
                       const std::vector<double>& phi);

public:
    explicit tridiagonal_solver(int n);
    void solve(const std::vector<double>& a, const std::vector<double>& b,
               const std::vector<double>& c, const std::vector<double>& phi);
    std::vector<double> get_solution() const;
    void resize(int n);
};

#endif