// core/problems/test_problem.cpp
#include "test_problem.h"
#include <cmath>

double test_problem::conductivity(double x) const {
    return x < xi ? 0.5 : 1.25;
}

double test_problem::reaction(double x) const {
    return x < xi ? 1.0 : 0.0625;
}

double test_problem::source(double x) const {
    return x < xi ? 1.0 : 2.5;
}

double test_problem::analytical_solution(double x) const {
    const double c1 = 0.58744204;
    const double c2 = -1.58744204;
    const double c3 = -16.23731987;
    const double c4 = -23.37825944;

    if (x < xi) {
        return c1 * std::exp(std::sqrt(2.) * x) + c2 * std::exp(-std::sqrt(2.) * x) + 1.0;
    } else {
        return c3 * std::exp(std::sqrt(0.05) * x) + c4 * std::exp(-std::sqrt(0.05) * x) + 40.0;
    }
}