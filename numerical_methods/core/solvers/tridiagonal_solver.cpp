// core/solvers/tridiagonal_solver.cpp
#include "tridiagonal_solver.h"
#include "../common/math_utils.h"

tridiagonal_solver::tridiagonal_solver(int n) : nodes(n) {
    v.resize(nodes);
    alpha.resize(nodes, 0.);
    beta.resize(nodes, 0.);
}

void tridiagonal_solver::normalize_system() {
    // Базовая реализация нормализации
}

void tridiagonal_solver::forward_sweep(const std::vector<double>& a, const std::vector<double>& b,
                                      const std::vector<double>& c, const std::vector<double>& phi) {
    // Нормировка первого уравнения
    double norm = c[0];
    if (math_utils::is_zero(norm)) {
        throw std::runtime_error("Zero diagonal element in forward sweep");
    }

    double b0_norm = b[0] / norm;
    double phi0_norm = phi[0] / norm;

    alpha[1] = -b0_norm;
    beta[1] = phi0_norm;

    for (int i = 1; i < (nodes - 1); i++) {
        double denominator = -c[i] - alpha[i] * a[i];
        if (math_utils::is_zero(denominator)) {
            throw std::runtime_error("Matrix is singular in forward sweep");
        }
        alpha[i + 1] = b[i] / denominator;
        beta[i + 1] = (-phi[i] + a[i] * beta[i]) / denominator;
    }
}

void tridiagonal_solver::backward_sweep(const std::vector<double>& a, const std::vector<double>& c,
                                       const std::vector<double>& phi) {
    // Нормировка последнего уравнения
    double norm = c[nodes - 1];
    if (math_utils::is_zero(norm)) {
        throw std::runtime_error("Zero diagonal element in backward sweep");
    }

    double a_norm = a[nodes - 1] / norm;
    double phi_norm = phi[nodes - 1] / norm;

    v[nodes - 1] = (a_norm * beta[nodes - 1] - phi_norm) / (-a_norm * alpha[nodes - 1] - 1.);

    for (int i = nodes - 2; i >= 0; i--) {
        v[i] = alpha[i + 1] * v[i + 1] + beta[i + 1];
    }
}

void tridiagonal_solver::solve(const std::vector<double>& a, const std::vector<double>& b,
                              const std::vector<double>& c, const std::vector<double>& phi) {
    if (a.size() != nodes || b.size() != nodes || c.size() != nodes || phi.size() != nodes) {
        throw std::invalid_argument("Vector sizes don't match node count");
    }

    forward_sweep(a, b, c, phi);
    backward_sweep(a, c, phi);
}

std::vector<double> tridiagonal_solver::get_solution() const {
    return v;
}

void tridiagonal_solver::resize(int n) {
    nodes = n;
    v.resize(nodes, 0.);
    alpha.resize(nodes, 0.);
    beta.resize(nodes, 0.);
}