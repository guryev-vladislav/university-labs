// core/problems/main_problem.cpp
#include "main_problem.h"
#include <cmath>

double MainProblem::conductivity(double x) const {
    return x < xi ? std::sqrt(x) : x + 1.0;
}

double MainProblem::reaction(double x) const {
    return x < xi ? 1.0 : std::pow(x, 2.0);
}

double MainProblem::source(double x) const {
    return x < xi ? 1.0 : 2.0 + std::sqrt(x);
}