import os
import sqlite3
import subprocess

# Define file paths
DATA_DIR = "./data"
EIA_FILE = os.path.join(DATA_DIR, "eia_emissions.xlsx")
COVID_FILE = os.path.join(DATA_DIR, "covid_cases.csv")
DB_FILE = os.path.join(DATA_DIR, "combined_data.db")
PIPELINE_SCRIPT = "./pipeline.py"


def test_pipeline_execution():
    """Test if the pipeline script runs without errors."""
    print("Running the data pipeline...")
    result = subprocess.run(["python", PIPELINE_SCRIPT], capture_output=True, text=True)
    if result.returncode == 0:
        print("Pipeline executed successfully.")
    else:
        print("Pipeline execution failed.")
        print("Error Output:", result.stderr)
        raise AssertionError("Pipeline execution failed.")


def test_output_files_exist():
    """Test if the required output files are created by the pipeline."""
    print("Checking if output files are generated...")
    if os.path.exists(EIA_FILE):
        print(f"EIA emissions file exists: {EIA_FILE}")
    else:
        raise AssertionError(f"EIA emissions file is missing: {EIA_FILE}")

    if os.path.exists(COVID_FILE):
        print(f"COVID-19 cases file exists: {COVID_FILE}")
    else:
        raise AssertionError(f"COVID-19 cases file is missing: {COVID_FILE}")

    if os.path.exists(DB_FILE):
        print(f"Database file exists: {DB_FILE}")
    else:
        raise AssertionError(f"Database file is missing: {DB_FILE}")


def test_database_table_exists():
    """Test if the required database table is created."""
    print("Validating database table...")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='eia_covid_data';")
    table = cursor.fetchone()
    conn.close()

    if table:
        print("Database table 'eia_covid_data' exists.")
    else:
        raise AssertionError("Database table 'eia_covid_data' is missing or not created properly.")


def test_database_table_contains_data():
    """Test if the database table contains data."""
    print("Checking if the 'eia_covid_data' table contains data...")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM eia_covid_data;")
    row_count = cursor.fetchone()[0]
    conn.close()

    if row_count > 0:
        print(f"Database table 'eia_covid_data' contains {row_count} rows.")
    else:
        raise AssertionError("Database table 'eia_covid_data' is empty.")


if __name__ == "__main__":
    try:
        print("Starting tests...")
        # Test 1: Pipeline execution
        test_pipeline_execution()

        # Test 2: Validate output files
        test_output_files_exist()

        # Test 3: Validate database table
        test_database_table_exists()

        # Test 4: Validate database table contains data
        test_database_table_contains_data()

        print("All tests passed successfully!")
    except AssertionError as e:
        print(f"Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        exit(1)
