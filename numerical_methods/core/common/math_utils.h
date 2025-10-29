// core/common/math_utils.h
#ifndef MATH_UTILS_H
#define MATH_UTILS_H

#include <cmath>
#include <stdexcept>

namespace math_utils {
    inline bool is_zero(double value, double tolerance = 1e-12) {
        return std::abs(value) < tolerance;
    }

    inline void check_positive(double value, const std::string& name) {
        if (value <= 0) {
            throw std::invalid_argument(name + " must be positive");
        }
    }
}

#endif