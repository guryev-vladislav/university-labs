// core/problems/test_problem.h
#ifndef TEST_PROBLEM_H
#define TEST_PROBLEM_H

#include "../solvers/differential_coefficients.h"
#include "differential_equation.h"

class test_problem : public differential_coefficients, public differential_equation {
private:
    double xi = 0.25;

public:
    double conductivity(double x) const override;
    double reaction(double x) const override;
    double source(double x) const override;
    double interface_position() const override { return xi; }

    double get_left_boundary() const override { return 0.0; }
    double get_right_boundary() const override { return 1.0; }
    int get_min_nodes() const override { return 5; }

    // Аналитическое решение для проверки
    double analytical_solution(double x) const;
};

#endif