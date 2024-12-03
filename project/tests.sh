#!/bin/bash

# ------------------------------------------
# Test Script for Running Automated Tests
# ------------------------------------------
# This script is designed to:
# 1. Run the `test.py` Python script that contains automated tests for the pipeline.
# 2. Report the results of the tests (pass/fail).
# 
# Instructions:
# 1. Ensure `test.py` is in the same directory as this script.
# 2. Make this script executable by running:
#    chmod +x tests.sh
# 3. Execute the script with:
#    .\tests.sh
#
# The script will:
# - Exit with code 0 if all tests pass.
# - Exit with code 1 if any test fails.
# ------------------------------------------

echo "Starting automated tests for the pipeline..."

# Run the Python test script
if python test.py; then
    # If the Python script runs successfully
    echo "All tests passed successfully!"
    exit 0
else
    # If the Python script fails (non-zero exit code)
    echo "Tests failed. Please check the output above for details."
    exit 1
fi
