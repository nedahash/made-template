#!/bin/bash

echo "Starting automated tests for the pipeline..."

# Clean data directory
rm -rf ../data
mkdir ../data

# Run Python test script
if python3 test.py; then
    echo "All tests passed successfully!"
    exit 0
else
    echo "Tests failed. Check logs above for details."
    exit 1
fi
