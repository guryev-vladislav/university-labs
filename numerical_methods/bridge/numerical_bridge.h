// bridge/numerical_bridge.h
#ifndef NUMERICAL_BRIDGE_H
#define NUMERICAL_BRIDGE_H

#include "../core/problems/main_problem.h"
#include "../core/problems/test_problem.h"
#include "../core/solvers/finite_difference_solver.h"
#include "../core/data/task_data.h"

public ref class numerical_bridge {
private:
    main_problem* main_problem_;
    test_problem* test_problem_;
    finite_difference_solver* solver_;

public:
    numerical_bridge();
    ~numerical_bridge();
    !numerical_bridge();

    System::Tuple<
        array<double>^, // x
        array<double>^, // v
        array<double>^, // x2
        array<double>^, // v2
        array<double>^  // diff
    >^ solve_main_problem(int nodes);

    System::Tuple<
        array<double>^, // x
        array<double>^, // v
        array<double>^, // u
        array<double>^  // diff
    >^ solve_test_problem(int nodes);

    property array<System::String^>^ available_problems {
        array<System::String^>^ get() {
            return gcnew array<System::String^> { "main", "test" };
        }
    }
};

#endif