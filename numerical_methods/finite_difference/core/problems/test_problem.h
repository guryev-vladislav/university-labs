// core/problems/test_problem.h
#ifndef TEST_PROBLEM_H
#define TEST_PROBLEM_H

#include "../solvers/differential_coefficients.h"

class TestProblem : public DifferentialCoefficients {
private:
    double xi = 0.25;

public:
    double conductivity(double x) const override;
    double reaction(double x) const override;
    double source(double x) const override;
    double interface_position() const override { return xi; }

    double analytical_solution(double x) const;
};

#endif