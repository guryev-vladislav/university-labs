#include "numerical_methods.h"
#include <cmath>
#include <stdexcept>

namespace RungeKuttaSuite {

    double Task1System::compute(double x, double u) const {
        return (x / (1.0 + x * x)) * u * u + u - u * u * u * sin(10.0 * x);
    }

    double TestSystem::compute(double /*x*/, double u) const {
        return u;
    }

    double Task2System::computeF1(double u1) const {
        return u1;
    }

    double Task2System::computeF2(double u, double u1) const {
        return -a_ * u1 - b_ * sin(u);
    }

}