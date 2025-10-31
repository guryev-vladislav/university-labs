// core/solvers/tridiagonal_solver.h
#ifndef TRIDIAGONAL_SOLVER_H
#define TRIDIAGONAL_SOLVER_H

#include <vector>
#include <stdexcept>
#include <cmath>

class TridiagonalSolver {
private:
    int nodes;
    std::vector<double> V;
    std::vector<double> alpha;
    std::vector<double> beta;

public:
    explicit TridiagonalSolver(int n) : nodes(n) {
        V.resize(nodes);
        alpha.resize(nodes, 0.);
        beta.resize(nodes, 0.);
    }

    void solve(const std::vector<double>& A, const std::vector<double>& B,
           const std::vector<double>& C, const std::vector<double>& Phi) {
        // Используем size_t для сравнения
        if (A.size() != static_cast<size_t>(nodes) ||
            B.size() != static_cast<size_t>(nodes) ||
            C.size() != static_cast<size_t>(nodes) ||
            Phi.size() != static_cast<size_t>(nodes)) {
            throw std::invalid_argument("Vector sizes don't match node count");
            }

        // Прямой ход
        alpha[1] = -B[0] / C[0];
        beta[1] = Phi[0] / C[0];

        for (int i = 1; i < nodes - 1; i++) {
            double denom = C[i] + A[i] * alpha[i];
            if (std::abs(denom) < 1e-12) {
                throw std::runtime_error("Matrix is singular");
            }
            alpha[i + 1] = -B[i] / denom;
            beta[i + 1] = (Phi[i] - A[i] * beta[i]) / denom;
        }

        // Обратный ход
        V[nodes - 1] = (Phi[nodes - 1] - A[nodes - 1] * beta[nodes - 1]) /
                       (C[nodes - 1] + A[nodes - 1] * alpha[nodes - 1]);

        for (int i = nodes - 2; i >= 0; i--) {
            V[i] = alpha[i + 1] * V[i + 1] + beta[i + 1];
        }
    }

    std::vector<double> get_solution() const { return V; }

    void resize(int n) {
        nodes = n;
        V.resize(nodes, 0.);
        alpha.resize(nodes, 0.);
        beta.resize(nodes, 0.);
    }
};

#endif