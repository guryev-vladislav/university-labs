#pragma once
#include <string>
#include <functional>
#include <memory>

namespace RungeKuttaSuite {

    class ODESystem {
    public:
        virtual ~ODESystem() = default;
        virtual double compute(double x, double u) const = 0;
        virtual std::string getName() const = 0;
    };

    class Task1System : public ODESystem {
    public:
        double compute(double x, double u) const override;
        std::string getName() const override { return "task1"; }
    };

    class TestSystem : public ODESystem {
    public:
        double compute(double x, double u) const override;
        std::string getName() const override { return "test"; }
    };

    class SecondOrderSystem {
    public:
        virtual ~SecondOrderSystem() = default;
        virtual double computeF1(double u1) const = 0;
        virtual double computeF2(double u, double u1) const = 0;
        virtual std::string getName() const = 0;
    };

    class Task2System : public SecondOrderSystem {
    private:
        double a_, b_;
    public:
        Task2System(double a, double b) : a_(a), b_(b) {}
        double computeF1(double u1) const override;
        double computeF2(double u, double u1) const override;
        std::string getName() const override { return "task2"; }
    };

    class SolverParameters {
    public:
        int steps;
        double tolerance;
        double right_boundary;
        double initial_value;
        double initial_derivative;
        double param_a;
        double param_b;

        SolverParameters() : steps(1000), tolerance(1e-6), right_boundary(1.0),
                            initial_value(1.0), initial_derivative(0.0),
                            param_a(1.0), param_b(1.0) {}
    };

    class SolutionPoint {
    public:
        double x;
        double u;
        double u1;
        double error_estimate;
        double step_size;
        int step_reductions;
        int step_increases;

        SolutionPoint(double x_val = 0.0, double u_val = 0.0, double u1_val = 0.0)
            : x(x_val), u(u_val), u1(u1_val), error_estimate(0.0),
              step_size(0.0), step_reductions(0), step_increases(0) {}
    };

}