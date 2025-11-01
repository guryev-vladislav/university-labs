#!/bin/bash

# Script to build and run Runge-Kutta Suite
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="$PROJECT_DIR/build"

echo "Runge-Kutta Suite Build & Run Script"

# Remove existing build directory
if [ -d "$BUILD_DIR" ]; then
    echo "Removing existing build directory..."
    rm -rf "$BUILD_DIR"
fi

# Create and enter build directory
echo "Creating build directory..."
mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"

# Configure project
echo "Configuring project with CMake..."
cmake ..

# Build project
echo "Building project..."
cmake --build .

# Run application
echo "Starting application..."
python3 app.py