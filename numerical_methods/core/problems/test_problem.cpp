// core/problems/test_problem.cpp
#include "test_problem.h"
#include <cmath>

double TestProblem::conductivity(double x) const {
    return x < xi ? 0.5 : 1.25;
}

double TestProblem::reaction(double x) const {
    return x < xi ? 1.0 : 0.0625;
}

double TestProblem::source(double x) const {
    return x < xi ? 1.0 : 2.5;
}

double TestProblem::analytical_solution(double x) const {
    const double C1 = 0.58744204;
    const double C2 = -1.58744204;
    const double C3 = -16.23731987;
    const double C4 = -23.37825944;

    if (x < xi) {
        return C1 * std::exp(std::sqrt(2.) * x) + C2 * std::exp(-std::sqrt(2.) * x) + 1.0;
    } else {
        return C3 * std::exp(std::sqrt(0.05) * x) + C4 * std::exp(-std::sqrt(0.05) * x) + 40.0;
    }
}