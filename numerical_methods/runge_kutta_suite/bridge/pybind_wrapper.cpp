#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include "../core/solver.h"
#include "../core/numerical_methods.h"

namespace py = pybind11;

PYBIND11_MODULE(runge_kutta_core, m) {
    m.doc() = "Runge-Kutta adaptive ODE solver core module";

    py::class_<RungeKuttaSuite::SolutionPoint>(m, "SolutionPoint")
        .def(py::init<>())
        .def_readwrite("x", &RungeKuttaSuite::SolutionPoint::x)
        .def_readwrite("u", &RungeKuttaSuite::SolutionPoint::u)
        .def_readwrite("u1", &RungeKuttaSuite::SolutionPoint::u1)
        .def_readwrite("error_estimate", &RungeKuttaSuite::SolutionPoint::error_estimate)
        .def_readwrite("step_size", &RungeKuttaSuite::SolutionPoint::step_size)
        .def_readwrite("step_reductions", &RungeKuttaSuite::SolutionPoint::step_reductions)
        .def_readwrite("step_increases", &RungeKuttaSuite::SolutionPoint::step_increases);

    py::class_<RungeKuttaSuite::SolverParameters>(m, "SolverParameters")
        .def(py::init<>())
        .def_readwrite("steps", &RungeKuttaSuite::SolverParameters::steps)
        .def_readwrite("tolerance", &RungeKuttaSuite::SolverParameters::tolerance)
        .def_readwrite("right_boundary", &RungeKuttaSuite::SolverParameters::right_boundary)
        .def_readwrite("initial_value", &RungeKuttaSuite::SolverParameters::initial_value)
        .def_readwrite("initial_derivative", &RungeKuttaSuite::SolverParameters::initial_derivative)
        .def_readwrite("param_a", &RungeKuttaSuite::SolverParameters::param_a)
        .def_readwrite("param_b", &RungeKuttaSuite::SolverParameters::param_b);

    py::class_<RungeKuttaSuite::AdaptiveSolver>(m, "AdaptiveSolver")
        .def("solve", &RungeKuttaSuite::AdaptiveSolver::solve)
        .def("get_system_name", &RungeKuttaSuite::AdaptiveSolver::getSystemName);

    py::class_<RungeKuttaSuite::SecondOrderSolver>(m, "SecondOrderSolver")
        .def("solve", &RungeKuttaSuite::SecondOrderSolver::solve)
        .def("get_system_name", &RungeKuttaSuite::SecondOrderSolver::getSystemName);

    m.def("create_first_order_solver", &RungeKuttaSuite::SolverFactory::createFirstOrderSolver,
          "Create first order ODE solver");

    m.def("create_second_order_solver", &RungeKuttaSuite::SolverFactory::createSecondOrderSolver,
          "Create second order ODE solver");

    m.def("create_task1_solver", [](const RungeKuttaSuite::SolverParameters& params) {
        return RungeKuttaSuite::SolverFactory::createFirstOrderSolver("task1", params);
    });

    m.def("create_test_solver", [](const RungeKuttaSuite::SolverParameters& params) {
        return RungeKuttaSuite::SolverFactory::createFirstOrderSolver("test", params);
    });
}