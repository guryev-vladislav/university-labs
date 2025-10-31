#!/bin/bash
# start_main.sh - Build and run numerical methods project

set -e  # Stop on errors

echo "Installing Python dependencies..."
python3 -m pip install matplotlib numpy pybind11

echo "Building C++ module..."
rm -rf build
mkdir -p build
cd build
cmake ..
make -j4
cd ..

echo "Creating module symlink..."
ln -sf build/diffeq_solver.cpython-*.so diffeq_solver.so

echo "Testing C++ module..."
python3 -c "
import diffeq_solver
result = diffeq_solver.solve('test', 11)
print('C++ module test passed - nodes:', len(result.x))
"

echo "Starting Python application..."
python3 main.py