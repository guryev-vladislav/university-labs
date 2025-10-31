// bridge/cpp/pybind_wrapper.cpp
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "../core/problems/main_problem.h"
#include "../core/problems/test_problem.h"
#include "../core/data/task_data.h"
#include "../core/solvers/finite_difference_solver.h"

namespace py = pybind11;

TaskData solve_problem(const std::string& problem_type, int nodes) {
    FiniteDifferenceSolver solver;

    if (problem_type == "main") {
        MainProblem problem;
        auto solution = solver.solve(problem, nodes);
        auto double_solution = solver.solve_double_grid(problem, nodes);

        TaskData data(nodes);
        double h = 1.0 / (nodes - 1);

        for (int i = 0; i < nodes; i++) {
            double x = i * h;
            data.push(TaskData::DataType::I, i);
            data.push(TaskData::DataType::X, x);
            data.push(TaskData::DataType::V, solution[i]);

            if (static_cast<size_t>(i * 2) < double_solution.size()) {
                data.push(TaskData::DataType::V2, double_solution[i * 2]);
                double diff = std::abs(double_solution[i * 2] - solution[i]);
                data.push(TaskData::DataType::DIFF, diff);
            }
        }
        return data;
    } else {
        TestProblem problem;
        auto solution = solver.solve(problem, nodes);

        TaskData data(nodes);
        double h = 1.0 / (nodes - 1);

        for (int i = 0; i < nodes; i++) {
            double x = i * h;
            double exact = problem.analytical_solution(x);

            data.push(TaskData::DataType::I, i);
            data.push(TaskData::DataType::X, x);
            data.push(TaskData::DataType::V, solution[i]);
            data.push(TaskData::DataType::U, exact);

            double diff = std::abs(exact - solution[i]);
            data.push(TaskData::DataType::DIFF, diff);
        }
        return data;
    }
}

PYBIND11_MODULE(diffeq_solver, m) {
    m.doc() = "Differential equation solver module";

    py::class_<TaskData>(m, "TaskData")
        .def(py::init<>())
        .def(py::init<int>())
        .def_readwrite("i", &TaskData::i)
        .def_readwrite("x", &TaskData::x)
        .def_readwrite("v", &TaskData::v)
        .def_readwrite("u", &TaskData::u)
        .def_readwrite("x2", &TaskData::x2)
        .def_readwrite("v2", &TaskData::v2)
        .def_readwrite("diff", &TaskData::diff);

    m.def("solve", &solve_problem, "Solve differential equation",
          py::arg("problem_type"), py::arg("nodes"));
}