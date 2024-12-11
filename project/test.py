import os
import sqlite3
import subprocess

# Define file paths relative to the root data directory
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
EIA_FILE = os.path.join(DATA_DIR, "eia_emissions.xlsx")
COVID_FILE = os.path.join(DATA_DIR, "covid_cases.csv")
DB_FILE = os.path.join(DATA_DIR, "combined_data.db")
PIPELINE_SCRIPT = os.path.join(os.path.dirname(__file__), "pipeline.py")


def test_pipeline_execution():
    result = subprocess.run(["python3", PIPELINE_SCRIPT], capture_output=True, text=True)
    assert result.returncode == 0, f"Pipeline execution failed: {result.stderr}"


def test_output_files_exist():
    assert os.path.exists(EIA_FILE), f"Missing file: {EIA_FILE}"
    assert os.path.exists(COVID_FILE), f"Missing file: {COVID_FILE}"
    assert os.path.exists(DB_FILE), f"Missing file: {DB_FILE}"


def test_database_table_exists():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='eia_covid_data';")
    assert cursor.fetchone(), "Table 'eia_covid_data' does not exist in the database."
    conn.close()


def test_database_table_contains_data():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM eia_covid_data;")
    row_count = cursor.fetchone()[0]
    assert row_count > 0, "Table 'eia_covid_data' is empty."
    conn.close()


if __name__ == "__main__":
    test_pipeline_execution()
    test_output_files_exist()
    test_database_table_exists()
    test_database_table_contains_data()
    print("All tests passed!")
