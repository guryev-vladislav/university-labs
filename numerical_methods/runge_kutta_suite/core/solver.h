#pragma once
#include "numerical_methods.h"
#include <vector>
#include <string>
#include <memory>

namespace RungeKuttaSuite {

    class AdaptiveSolver {
    private:
        std::unique_ptr<ODESystem> system_;
        SolverParameters params_;

        SolutionPoint rungeKuttaStep(const SolutionPoint& current, double h) const;

    public:
        AdaptiveSolver(std::unique_ptr<ODESystem> system, const SolverParameters& params);

        std::vector<SolutionPoint> solve();
        std::string getSystemName() const { return system_->getName(); }
    };

    class SecondOrderSolver {
    private:
        std::unique_ptr<SecondOrderSystem> system_;
        SolverParameters params_;

        SolutionPoint rungeKuttaStepSecondOrder(const SolutionPoint& current, double h) const;

    public:
        SecondOrderSolver(std::unique_ptr<SecondOrderSystem> system, const SolverParameters& params);

        std::vector<SolutionPoint> solve();
        std::string getSystemName() const { return system_->getName(); }
    };

    class SolverFactory {
    public:
        static std::unique_ptr<AdaptiveSolver> createFirstOrderSolver(
            const std::string& system_type, const SolverParameters& params);

        static std::unique_ptr<SecondOrderSolver> createSecondOrderSolver(
            const SolverParameters& params);
    };

}