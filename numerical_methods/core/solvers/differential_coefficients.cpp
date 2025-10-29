// core/solvers/differential_coefficients.cpp
#include "differential_coefficients.h"
#include "../common/constants.h"

double differential_coefficients::effective_conductivity(double x, double h) const {
    double xi = interface_position();

    if (x <= xi - h) {
        return conductivity(x - h / 2.0);
    } else if (x >= xi) {
        return conductivity(x - h / 2.0);
    } else {
        double k1_val = conductivity((x - h + xi) / 2.0);
        double k2_val = conductivity((xi + x) / 2.0);
        return 1.0 / (1.0 / h * ((xi - x + h) / k1_val + (x - xi) / k2_val));
    }
}

double differential_coefficients::effective_reaction(double x, double h) const {
    double xi = interface_position();

    if (x + h / 2.0 <= xi) {
        return reaction(x);
    } else if (x - h / 2.0 >= xi) {
        return reaction(x);
    } else {
        return (reaction((xi + (x - h / 2.0)) / 2.0) * (xi - (x - h / 2.0)) +
                reaction((xi + x + h / 2.0) / 2.0) * (x + h / 2.0 - xi)) / h;
    }
}

double differential_coefficients::effective_source(double x, double h) const {
    double xi = interface_position();
    
    if (x + h / 2.0 <= xi) {
        return source(x);
    } else if (x - h / 2.0 >= xi) {
        return source(x);
    } else {
        return (source((xi + (x - h / 2.0)) / 2.0) * (xi - (x - h / 2.0)) + 
                source((xi + x + h / 2.0) / 2.0) * (x + h / 2.0 - xi)) / h;
    }
}