#include "solver.h"
#include <cmath>
#include <vector>
#include <stdexcept>
#include <iostream>

namespace RungeKuttaSuite {

AdaptiveSolver::AdaptiveSolver(std::unique_ptr<ODESystem> system, const SolverParameters& params)
    : system_(std::move(system)), params_(params) {}

SolutionPoint AdaptiveSolver::rungeKuttaStep(const SolutionPoint& current, double h) const {
    SolutionPoint result;
    std::vector<double> k(5);

    k[1] = system_->compute(current.x, current.u);
    k[2] = system_->compute(current.x + h/2, current.u + (h/2) * k[1]);
    k[3] = system_->compute(current.x + h/2, current.u + (h/2) * k[2]);
    k[4] = system_->compute(current.x + h, current.u + h * k[3]);

    result.x = current.x + h;
    result.u = current.u + (h/6) * (k[1] + 2*k[2] + 2*k[3] + k[4]);

    return result;
}

std::vector<SolutionPoint> AdaptiveSolver::solve() {
    std::vector<SolutionPoint> solution;
    SolutionPoint current;
    current.x = 0.0;
    current.u = params_.initial_value;

    solution.push_back(current);

    double h = (params_.right_boundary - current.x) / params_.steps;
    int max_iterations = params_.steps * 10;
    int iterations = 0;

    while (current.x < params_.right_boundary && iterations < max_iterations) {
        bool step_accepted = false;
        int step_reductions = 0;
        int step_increases = 0;

        while (!step_accepted && step_reductions < 100) {
            SolutionPoint single_step = rungeKuttaStep(current, h);

            if (params_.tolerance > 0) {
                SolutionPoint half_step1 = rungeKuttaStep(current, h/2);
                SolutionPoint half_step2 = rungeKuttaStep(half_step1, h/2);

                double error_estimate = (half_step2.u - single_step.u) / 15.0;

                if (std::abs(error_estimate) < params_.tolerance) {
                    step_accepted = true;
                    current = single_step;

                    if (std::abs(error_estimate) < params_.tolerance / 32.0) {
                        h *= 2.0;
                        step_increases++;
                    }
                } else {
                    h /= 2.0;
                    step_reductions++;
                }
            } else {
                step_accepted = true;
                current = single_step;
            }
        }

        if (step_reductions >= 100) {
            std::cerr << "Warning: Maximum step reductions reached" << std::endl;
            break;
        }

        current.step_size = h;
        current.step_reductions = step_reductions;
        current.step_increases = step_increases;
        solution.push_back(current);

        iterations++;
    }

    return solution;
}

SolutionPoint SecondOrderSolver::rungeKuttaStepSecondOrder(const SolutionPoint& current, double h) const {
    SolutionPoint result;
    std::vector<double> k(5), l(5);

    k[1] = system_->computeF1(current.u1);
    l[1] = system_->computeF2(current.u, current.u1);
    k[2] = system_->computeF1(current.u1 + (h/2)*l[1]);
    l[2] = system_->computeF2(current.u + (h/2)*k[1], current.u1 + (h/2)*l[1]);
    k[3] = system_->computeF1(current.u1 + (h/2)*l[2]);
    l[3] = system_->computeF2(current.u + (h/2)*k[2], current.u1 + (h/2)*l[2]);
    k[4] = system_->computeF1(current.u1 + h*l[3]);
    l[4] = system_->computeF2(current.u + h*k[3], current.u1 + h*l[3]);

    result.x = current.x + h;
    result.u = current.u + (h/6) * (k[1] + 2*k[2] + 2*k[3] + k[4]);
    result.u1 = current.u1 + (h/6) * (l[1] + 2*l[2] + 2*l[3] + l[4]);

    return result;
}

SecondOrderSolver::SecondOrderSolver(std::unique_ptr<SecondOrderSystem> system, const SolverParameters& params)
    : system_(std::move(system)), params_(params) {}

std::vector<SolutionPoint> SecondOrderSolver::solve() {
    std::vector<SolutionPoint> solution;
    SolutionPoint current;
    current.x = 0.0;
    current.u = params_.initial_value;
    current.u1 = params_.initial_derivative;

    solution.push_back(current);

    double h = (params_.right_boundary - current.x) / params_.steps;
    int max_iterations = params_.steps * 10;
    int iterations = 0;

    while (current.x < params_.right_boundary && iterations < max_iterations) {
        bool step_accepted = false;
        int step_reductions = 0;
        int step_increases = 0;

        while (!step_accepted && step_reductions < 100) {
            SolutionPoint single_step = rungeKuttaStepSecondOrder(current, h);

            if (params_.tolerance > 0) {
                SolutionPoint half_step1 = rungeKuttaStepSecondOrder(current, h/2);
                SolutionPoint half_step2 = rungeKuttaStepSecondOrder(half_step1, h/2);

                double error_estimate = (half_step2.u - single_step.u) / 15.0;

                if (std::abs(error_estimate) < params_.tolerance) {
                    step_accepted = true;
                    current = single_step;

                    if (std::abs(error_estimate) < params_.tolerance / 32.0) {
                        h *= 2.0;
                        step_increases++;
                    }
                } else {
                    h /= 2.0;
                    step_reductions++;
                }
            } else {
                step_accepted = true;
                current = single_step;
            }
        }

        if (step_reductions >= 100) {
            std::cerr << "Warning: Maximum step reductions reached" << std::endl;
            break;
        }

        current.step_size = h;
        current.step_reductions = step_reductions;
        current.step_increases = step_increases;
        solution.push_back(current);

        iterations++;
    }

    return solution;
}

std::unique_ptr<AdaptiveSolver> SolverFactory::createFirstOrderSolver(
    const std::string& system_type, const SolverParameters& params) {

    if (system_type == "task1") {
        return std::make_unique<AdaptiveSolver>(std::make_unique<Task1System>(), params);
    } else if (system_type == "test") {
        return std::make_unique<AdaptiveSolver>(std::make_unique<TestSystem>(), params);
    }

    throw std::invalid_argument("Unknown system type: " + system_type);
}

std::unique_ptr<SecondOrderSolver> SolverFactory::createSecondOrderSolver(const SolverParameters& params) {
    return std::make_unique<SecondOrderSolver>(
        std::make_unique<Task2System>(params.param_a, params.param_b), params);
}

}