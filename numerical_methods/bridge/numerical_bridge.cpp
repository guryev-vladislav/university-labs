// bridge/numerical_bridge.cpp
#include "numerical_bridge.h"
#include <msclr/marshal_cppstd.h>

using namespace System;
using namespace System::Collections::Generic;

numerical_bridge::numerical_bridge() {
    main_problem_ = new main_problem();
    test_problem_ = new test_problem();
    solver_ = new finite_difference_solver();
}

numerical_bridge::~numerical_bridge() {
    this->!numerical_bridge();
}

numerical_bridge::!numerical_bridge() {
    delete main_problem_;
    delete test_problem_;
    delete solver_;
    main_problem_ = nullptr;
    test_problem_ = nullptr;
    solver_ = nullptr;
}

Tuple<array<double>^, array<double>^, array<double>^, array<double>^, array<double>^>^
numerical_bridge::solve_main_problem(int nodes) {
    try {
        auto solution = solver_->solve(*main_problem_, nodes);
        auto double_solution = solver_->solve_double_grid(*main_problem_, nodes);

        task_data data(nodes);
        double h = 1.0 / (nodes - 1);

        // Заполняем данные
        for (int i = 0; i < nodes; i++) {
            double x = i * h;
            data.push(task_data::data_type::I, i);
            data.push(task_data::data_type::X, x);
            data.push(task_data::data_type::V, solution[i]);

            if (i * 2 < double_solution.size()) {
                data.push(task_data::data_type::X2, x);
                data.push(task_data::data_type::V2, double_solution[i * 2]);
                double diff = std::abs(double_solution[i * 2] - solution[i]);
                data.push(task_data::data_type::DIFF, diff);
            }
        }

        // Конвертируем в managed arrays
        array<double>^ x_array = gcnew array<double>(data.x.size());
        array<double>^ v_array = gcnew array<double>(data.v.size());
        array<double>^ x2_array = gcnew array<double>(data.x2.size());
        array<double>^ v2_array = gcnew array<double>(data.v2.size());
        array<double>^ diff_array = gcnew array<double>(data.diff.size());

        for (size_t i = 0; i < data.x.size(); i++) {
            x_array[i] = data.x[i];
            v_array[i] = data.v[i];
        }

        for (size_t i = 0; i < data.x2.size(); i++) {
            x2_array[i] = data.x2[i];
            v2_array[i] = data.v2[i];
        }

        for (size_t i = 0; i < data.diff.size(); i++) {
            diff_array[i] = data.diff[i];
        }

        return Tuple::Create(x_array, v_array, x2_array, v2_array, diff_array);

    } catch (const std::exception& e) {
        throw gcnew System::Exception(gcnew System::String(e.what()));
    }
}

Tuple<array<double>^, array<double>^, array<double>^, array<double>^>^
numerical_bridge::solve_test_problem(int nodes) {
    try {
        auto solution = solver_->solve(*test_problem_, nodes);

        task_data data(nodes);
        double h = 1.0 / (nodes - 1);

        // Заполняем данные
        for (int i = 0; i < nodes; i++) {
            double x = i * h;
            double exact = test_problem_->analytical_solution(x);

            data.push(task_data::data_type::I, i);
            data.push(task_data::data_type::X, x);
            data.push(task_data::data_type::V, solution[i]);
            data.push(task_data::data_type::U, exact);

            double diff = std::abs(exact - solution[i]);
            data.push(task_data::data_type::DIFF, diff);
        }

        // Конвертируем в managed arrays
        array<double>^ x_array = gcnew array<double>(data.x.size());
        array<double>^ v_array = gcnew array<double>(data.v.size());
        array<double>^ u_array = gcnew array<double>(data.u.size());
        array<double>^ diff_array = gcnew array<double>(data.diff.size());

        for (size_t i = 0; i < data.x.size(); i++) {
            x_array[i] = data.x[i];
            v_array[i] = data.v[i];
            u_array[i] = data.u[i];
            diff_array[i] = data.diff[i];
        }

        return Tuple::Create(x_array, v_array, u_array, diff_array);

    } catch (const std::exception& e) {
        throw gcnew System::Exception(gcnew System::String(e.what()));
    }
}