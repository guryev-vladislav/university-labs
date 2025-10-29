// core/data/solution_data.h
#ifndef SOLUTION_DATA_H
#define SOLUTION_DATA_H

#include <vector>
#include <string>
#include <algorithm>
#include <cmath>

struct solution_data {
    std::vector<double> indices;
    std::vector<double> coordinates;
    std::vector<double> solution;
    std::vector<double> reference_solution;
    std::vector<double> errors;

    enum class data_type { INDEX, COORDINATE, SOLUTION, REFERENCE, ERROR };

    void add_data_point(data_type type, double value) {
        switch (type) {
            case data_type::INDEX: indices.push_back(value); break;
            case data_type::COORDINATE: coordinates.push_back(value); break;
            case data_type::SOLUTION: solution.push_back(value); break;
            case data_type::REFERENCE: reference_solution.push_back(value); break;
            case data_type::ERROR: errors.push_back(value); break;
        }
    }

    void clear() {
        indices.clear();
        coordinates.clear();
        solution.clear();
        reference_solution.clear();
        errors.clear();
    }

    bool validate() const {
        return !coordinates.empty() &&
               coordinates.size() == solution.size() &&
               (reference_solution.empty() || reference_solution.size() == solution.size());
    }

    double max_error() const {
        if (errors.empty()) return 0.0;
        return *std::max_element(errors.begin(), errors.end());
    }

    double rms_error() const {
        if (errors.empty()) return 0.0;
        double sum = 0.0;
        for (double error : errors) {
            sum += error * error;
        }
        return std::sqrt(sum / errors.size());
    }
};

class solution_calculator {
public:
    static double calculate_error_norm(const solution_data& data) {
        return data.max_error();
    }
};

#endif