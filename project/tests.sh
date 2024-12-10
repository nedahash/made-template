#!/bin/bash

echo "Starting automated tests for the pipeline..."

# Run the Python test script
if python3  test.py; then
    # If the Python script runs successfully
    echo "All tests passed successfully!"
    exit 0
else
    # If the Python script fails (non-zero exit code)
    echo "Tests failed. Please check the output above for details."
    exit 1
fi
