# CMakeLists.txt
cmake_minimum_required(VERSION 3.12)
project(numerical_methods)

find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

execute_process(
        COMMAND ${Python3_EXECUTABLE} -c "import pybind11; print(pybind11.get_cmake_dir())"
        OUTPUT_VARIABLE pybind11_DIR
        OUTPUT_STRIP_TRAILING_WHITESPACE
)

find_package(pybind11 REQUIRED)

pybind11_add_module(diffeq_solver
        bridge/cpp/pybind_wrapper.cpp
        core/problems/main_problem.cpp
        core/problems/test_problem.cpp
)

target_include_directories(diffeq_solver PRIVATE
        ${CMAKE_SOURCE_DIR}/core
        ${CMAKE_SOURCE_DIR}/core/data
        ${CMAKE_SOURCE_DIR}/core/problems
        ${CMAKE_SOURCE_DIR}/core/solvers
)