#!/bin/bash
# start_main.sh - Build and run numerical methods project

set -e  # Stop on errors

# Функция для graceful shutdown
cleanup() {
    echo "Завершение работы..."
    exit 0
}

# Ловим сигналы прерывания
trap cleanup SIGINT SIGTERM

echo "Building C++ module..."
rm -rf build
mkdir -p build
cd build
cmake ..
make -j4
cd ..

echo "Creating module symlink..."
ln -sf build/diffeq_solver.cpython-*.so diffeq_solver.so

echo "Starting Python application..."
echo "Use Ctrl+C to exit"
python3 main.py