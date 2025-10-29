#include "solution_data.h"
#include "../problems/main_problem.h"
#include "../problems/test_problem.h"
#include "../solvers/finite_difference_solver.h"
#include <stdexcept>

void SolutionData::addDataPoint(DataType type, double value) {
    switch (type) {
        case DataType::INDEX: indices.push_back(value); break;
        case DataType::COORDINATE: coordinates.push_back(value); break;
        case DataType::SOLUTION: solution.push_back(value); break;
        case DataType::REFERENCE: referenceSolution.push_back(value); break;
        case DataType::ERROR: errors.push_back(value); break;
    }
}

void SolutionData::clear() {
    indices.clear();
    coordinates.clear();
    solution.clear();
    referenceSolution.clear();
    errors.clear();
}

bool SolutionData::validate() const {
    return !coordinates.empty() && 
           coordinates.size() == solution.size() &&
           (referenceSolution.empty() || referenceSolution.size() == solution.size());
}

SolutionData SolutionCalculator::calculateMainProblem(int nodes) {
    MainProblem problem;
    FiniteDifferenceSolver solver(0.0, 1.0);
    
    auto solution = solver.solve(problem, nodes);
    auto doubleSolution = solver.solveDoubleGrid(problem, nodes);
    
    SolutionData data;
    double h = 1.0 / (nodes - 1);
    
    for (int i = 0; i < nodes; i++) {
        double x = i * h;
        data.addDataPoint(SolutionData::DataType::INDEX, i);
        data.addDataPoint(SolutionData::DataType::COORDINATE, x);
        data.addDataPoint(SolutionData::DataType::SOLUTION, solution[i]);
        
        if (i * 2 < doubleSolution.size()) {
            double error = std::abs(doubleSolution[i * 2] - solution[i]);
            data.addDataPoint(SolutionData::DataType::ERROR, error);
        }
    }
    
    return data;
}

SolutionData SolutionCalculator::calculateTestProblem(int nodes) {
    TestProblem problem;
    FiniteDifferenceSolver solver(0.0, 1.0);
    
    auto solution = solver.solve(problem, nodes);
    
    SolutionData data;
    double h = 1.0 / (nodes - 1);
    
    for (int i = 0; i < nodes; i++) {
        double x = i * h;
        double exact = problem.analyticalSolution(x);
        
        data.addDataPoint(SolutionData::DataType::INDEX, i);
        data.addDataPoint(SolutionData::DataType::COORDINATE, x);
        data.addDataPoint(SolutionData::DataType::SOLUTION, solution[i]);
        data.addDataPoint(SolutionData::DataType::REFERENCE, exact);
        data.addDataPoint(SolutionData::DataType::ERROR, std::abs(exact - solution[i]));
    }
    
    return data;
}

double SolutionCalculator::calculateErrorNorm(const SolutionData& data) {
    if (data.errors.empty()) return 0.0;
    
    double maxError = 0.0;
    for (double error : data.errors) {
        if (error > maxError) maxError = error;
    }
    return maxError;
}