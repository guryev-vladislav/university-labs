cmake_minimum_required(VERSION 3.15)
project(runge_kutta_suite)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)

execute_process(
        COMMAND ${Python_EXECUTABLE} -c "import pybind11; print(pybind11.get_cmake_dir())"
        OUTPUT_VARIABLE pybind11_DIR
        OUTPUT_STRIP_TRAILING_WHITESPACE
)

find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(runge_kutta_core
        bridge/pybind_wrapper.cpp
        core/solver.cpp
        core/numerical_methods.cpp
)

target_include_directories(runge_kutta_core
        PRIVATE
        ${PYTHON_INCLUDE_DIRS}
        PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}/core
)

if(MSVC)
    target_compile_options(runge_kutta_core PRIVATE /W4)
else()
    target_compile_options(runge_kutta_core PRIVATE -Wall -Wextra -O2)
endif()

set_target_properties(runge_kutta_core PROPERTIES
        SUFFIX "${PYTHON_MODULE_EXTENSION}"
        OUTPUT_NAME "runge_kutta_core"
)

if(WIN32)
    set(OUTPUT_DIR "${CMAKE_BINARY_DIR}/$<CONFIG>")
else()
    set(OUTPUT_DIR "${CMAKE_BINARY_DIR}")
endif()

add_custom_command(TARGET runge_kutta_core POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:runge_kutta_core> ${OUTPUT_DIR}
        COMMENT "Copying Python module to build directory"
)

add_custom_target(copy_python_files ALL
        COMMAND ${CMAKE_COMMAND} -E copy_directory
        ${CMAKE_SOURCE_DIR}/ui
        ${OUTPUT_DIR}/ui
        COMMAND ${CMAKE_COMMAND} -E copy
        ${CMAKE_SOURCE_DIR}/app.py
        ${OUTPUT_DIR}/app.py
        COMMENT "Copying Python files to build directory"
)